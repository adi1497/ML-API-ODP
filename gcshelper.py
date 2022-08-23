# # GCS Import
from google.oauth2 import service_account
from google.cloud.storage import client
import json
# GCS
with open('service_account_google.json') as f:
    SERVICE_ACCOUNT = json.load(f)
#bucket from google cloud storage
BUCKET = "mysiis_ms_odp_classification"
#Using the service token to create the client
credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

client = client.Client(
    credentials=credentials,
    project=credentials.project_id,
)
# End GCS

# Helper
#Save and download functions
def save_file(local_filename, remote_filename, remote_path):
    prefix = '/'
    remote_full_path = remote_path+prefix+remote_filename
    bucket = client.get_bucket(BUCKET)
    blob = bucket.blob(remote_full_path)
    blob.upload_from_filename(local_filename)

def download_file(local_filename, remote_filename):
    bucket = client.get_bucket(BUCKET)
    blob = bucket.blob(remote_filename)
    blob.download_to_filename(local_filename)
# End Helper