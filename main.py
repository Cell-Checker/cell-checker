import os
import time
import urllib

import yaml
import typer
from libs.check_keys import *
from libs.process_data import *
from pathlib import Path
from typing_extensions import Annotated
from libs.comparison_rules import *
from libs.preprocessor import *
from durable.lang import post, get_host
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv(override=True)


def main(config: Annotated[Path, typer.Option(help="Path to test config file")]):
    """
    Main function to:
    1. Check if a YAML test file contains the required keys.
    2. Extract the source and target data and load them into dataframes.
    3. Compare the two dataframes based on rules (To Do).
    4. Generate a report (To Do).

    Parameters:
    config (Path): Path to the test YAML file.
    """
    test_case = {}
    required_keys = {'name', 'target', 'source', 'comparison_rules'}

    # Read and load the test file if the path is provided
    if config:
        # Load the YAML file into a dictionary
        test_case = yaml.load(config.read_text(), Loader=yaml.Loader)

        # Fetch the secrets from the environment and update the YAML configuration
        def update_secrets_in_yaml(test_case):
            for key, value in test_case.items():
                if isinstance(value, dict):
                    update_secrets_in_yaml(value)
                elif isinstance(value, str) and (value.startswith("SOURCE_") or value.startswith("TARGET_")):
                    if os.environ.get(value):
                        if "PASSWORD" in value:
                            password = os.environ.get(value)
                            encoded_password = urllib.parse.quote_plus(password)
                            test_case[key] = encoded_password
                        else:
                            test_case[key] = os.environ.get(value)
            return test_case

        test_case = update_secrets_in_yaml(test_case)
        # Check if the required keys are present in the test case
        result, missing_keys = check_keys_in_list(test_case['test'], required_keys)
        if result:
            # Performing preprocessing if available
            if 'preprocessor' in test_case['test']:
                preprocessor = test_case['test'].get('preprocessor')
                if preprocessor:
                    for key, value in preprocessor.items():
                        if key == "sharepoint_download":
                            sharepoint_file = value
                            if sharepoint_file:
                                session_id = f"sharepoint_download_{test_case['test']['name']}"
                                post('preprocessor',
                                     dict(rule="sharepoint_download", file_path=sharepoint_file, sid=session_id))
                                state = get_host().get_state('preprocessor', session_id)
                                if "exception" in state:
                                    print(f"Error: {state}")
                                    raise Exception(f"Error: {state['exception']}")

            # Process the data if the required keys are present
            source_df, target_df = process_data(test_case)

            # Convert the dataframes to dictionaries for comparison
            source_data = source_df.to_dict(orient='records')
            target_data = target_df.to_dict(orient='records')


            # Post the comparison rules and data to the ruleset for evaluation
            for comparison_rule in test_case['test']['comparison_rules']:
                session_id = f"{comparison_rule}_{test_case['test']['name']}"
                post('comparison_rules', dict(rule=comparison_rule, source=source_data, target=target_data, sid=session_id))
                state = get_host().get_state('comparison_rules', session_id)
        else:
            # Print an error message if the required keys are missing
            print(f"Test Case Is Missing The Following Information: {missing_keys}")


if __name__ == "__main__":
    # Run the main function using Typer for command-line argument parsing
    typer.run(main)
