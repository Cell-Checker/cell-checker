import yaml
import typer
from libs.check_keys import *
from libs.process_data import *
from pathlib import Path
from typing_extensions import Annotated
from libs.comparison_rules import *
from durable.lang import post, get_host
from libs.render_html import *
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
        # Check if the required keys are present in the test case
        result, missing_keys = check_keys_in_list(test_case['test'], required_keys)
        if result:
            # Process the data if the required keys are present
            source_df, target_df = process_data(test_case)

            target_df = target_df.replace(np.nan, 'NaN')

            # Convert the dataframes to dictionaries for comparison
            source_data = source_df.to_dict(orient='records')
            target_data = target_df.to_dict(orient='records')
            print(target_data)
            summary_rows = {}

            # Post the comparison rules and data to the ruleset for evaluation
            for comparison_rule in test_case['test']['comparison_rules']:
                session_id = f"{comparison_rule}_{test_case['test']['name']}"
                post('comparison_rules', dict(rule=comparison_rule, source=source_data, target=target_data, sid=session_id))
                state = get_host().get_state('comparison_rules', session_id)
                print(state['result'])
                if session_id == f"not_null_{test_case['test']['name']}":
                    summary_rows.update(({comparison_rule: f"{state['target_size']}"}))
                else:
                    summary_rows.update(({comparison_rule: f"{state['source_size']}/{state['target_size']}"}))
            context = {
                'title': test_case['test']['name'],
                'rules': test_case['test']['comparison_rules'],
                'summary_rows': summary_rows
            }

            # Render the template
            rendered_html = render_html('template.html', context)

            # Output the rendered HTML (for example, save to a file or print to console)
            with open('test_results.html', 'w') as f:
                print(rendered_html, file=f)
            print("Open test_results.html")

        else:
            # Print an error message if the required keys are missing
            print(f"Test Case Is Missing The Following Information: {missing_keys}")

if __name__ == "__main__":
    # Run the main function using Typer for command-line argument parsing
    typer.run(main)
