import sys

from durable.lang import ruleset, when_all, m, post, get_host
import pandas as pd
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
import os

FILE_EXTENSIONS = [".xlsx", ".csv", ".xlsb"]

# Define a ruleset for comparison rules
with ruleset('comparison_rules'):
    # Define a rule for checking if the row count of two dataframes is equal
    @when_all(m.rule == 'equal_row_count')
    def equal_rows(c):
        """
        Checks if the row count of the source and target dataframes is equal.

        If the row count is not equal, prints a validation failure message and sets the result to False.
        If the row count is equal, prints a validation success message and sets the result to True.

        Parameters:
        c (Context): The context object, which contains the source and target dataframes.
        """
        source = pd.DataFrame(c.m.source)
        target = pd.DataFrame(c.m.target)

        if len(source) != len(target):
            print(f"Validation failed: Row count does not match (source: {len(source)}, target: {len(target)})")
            c.s.result = False
        else:
            print(f"Validation succeeded: Row count matches (source: {len(source)}, target: {len(target)})")
            c.s.result = True
        c.update(c.s)

    # Define a rule for checking if the rows of two dataframes match
    @when_all(m.rule == 'rows_match')
    def rows_match(c):
        """
        Checks if the rows of the source and target dataframes match.

        If the rows do not match, prints a message and sets the result to False.
        If the rows match, prints a message and sets the result to True.

        Parameters:
        c (Context): The context object, which contains the source and target dataframes.
        """
        source = pd.DataFrame(c.m.source)
        target = pd.DataFrame(c.m.target)

        if source.equals(target):
            print(f"Rows match between both source and target")
            c.s.result = True
        else:
            print(f"Rows do not match between both source and target")
            c.s.result = False
        c.update

    # Define a rule for checking if a dataframe has any null values
    @when_all(m.rule == 'not_null')
    def not_null(c):
        """
        Checks if the target dataframe has any null values.

        If the dataframe has null values, prints a message and returns False.
        If the dataframe does not have null values, prints a message and returns True.

        Parameters:
        c (Context): The context object, which contains the target dataframe.
        """
        target = pd.DataFrame(c.m.target)
        if target.notnull().all().all():
            print(f"No Nulls")
            c.s.result = True
        else:
            print(f"Empty Values")
            c.s.result = False
        c.update

    @when_all(m.rule == 'sharepoint_download')
    def sharepoint_download(c, ):
        """
            The rule 'sharepoint_download' takes the Absolute Sharepoint file path as an input & downloads the file
            from SharePoint to the  local directory "./data_validation_test/" after renaming it to
            "source.<file_extension>".

            Parameters:
            - c.m.file_path: Complete/Absoulte path of a Sharepoint File .
            """
        try:
            # retrieve the file path from the context
            file = c.m.file_path
            # remove any query parameters from the file path
            file = file.split("?")[0]
            # Validating the file path
            valid_format = [extension for extension in FILE_EXTENSIONS if file.endswith(extension)]

            if not (file.startswith("https://") and file.__contains__("sites") and valid_format):
                raise ValueError("File path is not correct. file path should be a valid sharepoint file path. "
                                 "Example file path format: https://ecoatm.sharepoint.com/sites/<SiteName>/<FolderPath>/<FileName>")
            # Extract the file name, sharepoint site name, sharepoint site url, and folder url from the file path
            file_name = file.split("/")[-1]
            share_point_site_name = file.split("/sites/")[1].split("/")[0]
            share_point_site = "/".join([file.split("/sites/")[0], "sites", share_point_site_name])
            folder = file.strip(file_name).split(share_point_site_name)[1].strip('/')

            # Connect to SharePoint using the provided credentials
            print("creating context & connecting to sharepoint..")
            ctx = ClientContext(share_point_site).with_credentials(
                UserCredential(
                    os.getenv("office_365_username"),
                    os.getenv("office_365_password")
                )
            )
            file_url = "/".join(["/sites", share_point_site_name, folder, file_name])
            # Fetch the binary file content from given sharepoint file path
            response = File.open_binary(ctx, server_relative_url=file_url)
            print("connected..")

            # Download the file if the response status code is 200
            if response.status_code == 200:

                # Extract the project main folder path, file extension and build the new file name
                main_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                file_type = file_name.split(".")[-1]
                new_file_name = f"source.{file_type}"

                # Build local file path
                local_file_path = os.path.join(main_folder, "data_validation_tests", new_file_name)

                # Save the file to the local directory
                with open(local_file_path, "wb") as file_obj:
                    file_obj.write(response.content)
                    print("File has been downloaded successfully")
                    c.s.result = True

            else:
                raise Exception(f"Failed to download the file. Status code: {response.status_code}")

        except Exception as e:
            c.s.result = False
            exc_type, value, tb = sys.exc_info()
            exception_details = (f"Exception Type: {exc_type} Exception value: {value} "
                                 f"at line no: {tb.tb_lineno}")
            print(exception_details)
            raise Exception(e)
        finally:
            c.update
