import yaml
import typer
from libs.check_keys import *
from libs.process_data import *
from pathlib import Path
from typing_extensions import Annotated

def main(config: Annotated[Path, typer.Option(help="Path to test config file")]):
    """
    Main function to
    1. Check if a YAML test file contains the required keys.
    2. Extract the source and target data and load into a dataframe
    3. Compare the two dataframes based on rules ( To Do )
    4. Generate a report ( To Do )

    Parameters:
    config (Path): Path to the test YAML file.
    """
    test_case = {}
    required_keys = {'name', 'target', 'source', 'comparison_rules'}

    # Read and load the test file if the path is provided
    if config:
        # Load the YAML file into a dictionary
        test_case = yaml.load(config.read_text(), Loader=yaml.Loader)
        # Check if the required keys are present in the test case
        result, missing_keys = check_keys_in_list(test_case['test'], required_keys)
        if result:
            # Process the data if the required keys are present
            source_df, target_df = process_data(test_case)
            print(source_df)
            print(target_df)
        else:
            # Print an error message if the required keys are missing
            print(f"Test Case Is Missing The Following Information: {missing_keys}")


if __name__ == "__main__":
    # Run the main function using Typer for command-line argument parsing
    typer.run(main)