from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
import os

share_point_site_name = "DataEngineeringTest"
share_point_doc = "SharedDocuments"
share_point_site = "https://ecoatm.sharepoint.com/sites/DataEngineeringTest"
office_365_username = "auction_365_qa@ecoatm.com"
office_365_password = "Eco19Oct2023!"
print("connecting..")

ctx = ClientContext(share_point_site).with_credentials(
                UserCredential(
                    office_365_username,
                    office_365_password
                )
            )
print("connected..")
path = os.path.join("/sites", share_point_site_name, share_point_doc)
files = ctx.web.get_folder_by_server_relative_path(path).get_files().execute_query_retry(max_retry=2,
                                                                                         timeout_secs=5)
print(files)

