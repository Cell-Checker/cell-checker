import yaml
import typer
from libs.check_keys import *
from libs.connector_factory import ConnectorFactory
from libs.data_service import *
from pathlib import Path
from typing_extensions import Annotated


def main(config: Annotated[Path, typer.Option(help="Path to test config file")]):
    """
    Main function to check if a YAML test file contains the required keys.

    Parameters:
    test (Path): Path to the test YAML file.
    """
    test_case = {}
    required_keys = {'name', 'target', 'source', 'comparison_rules'}

    # Read and load the test file if the path is provided
    if config:
        test_case = yaml.load(config.read_text(), Loader=yaml.Loader)
        # Check for the required keys in the test case
        result, missing_keys = check_keys_in_list(test_case['test'], required_keys)
        if result:
            assert isinstance(result, object)
            source_connector = ConnectorFactory.get_connector(test_case['test']['source'])
            data_service = DataService(source_connector)
            source_df = data_service.process_data()
            target_connector = ConnectorFactory.get_connector(test_case['test']['target'])
            data_service = DataService(target_connector)
            target_df = data_service.process_data()
            print(source_df)
            print(target_df)
        else:
            print(f"Test Case Is Missing The Following Information: {missing_keys}")


if __name__ == "__main__":
    # Run the main function using Typer
    typer.run(main)
