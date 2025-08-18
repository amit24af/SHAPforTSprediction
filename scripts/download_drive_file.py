import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload

SERVICE_ACCOUNT_INFO = os.environ.get('GDRIVE_SERVICE_ACCOUNT')

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
FOLDER_TO_DOWNLOAD = ('1gTo-lWF8KePNcNbhXSlaP6B6OusKnTeJ', 'data') 

# FILE_ID1 = '18EesyISDITHMX-VLI4mjvDF4nOQ7fDsz'
# FILE_ID2 = '1wY7X3QV_0O1uS3D7s0qmanF8O2aNA331'
# FILE_ID3 = '1nLmPj6MKZecHK7ywYXKiWKtg4dr1jtUu'
# FILE_ID4 = '1iuDYJ7wqm4Bh8iIPvPKylCBnsc0aLPN6'
# OUTPUT_FILE1 = 'experiment_FBProphet.ipynb'
# OUTPUT_FILE2 = 'experiment_CatBoost.ipynb'
# OUTPUT_FILE2 = 'experiment_LSTM.ipynb'
# OUTPUT_FILE2 = 'descriptive_stats_experiment_data.ipynb'

FILES_TO_DOWNLOAD = [
    ('1LMBcxc6szfgdVrZi_3GTTvmexpUVZCL7', 'experiment_FBProphet.ipynb'),
    ('1wY7X3QV_0O1uS3D7s0qmanF8O2aNA331', 'experiment_XGBoost.ipynb'),
    ('1nLmPj6MKZecHK7ywYXKiWKtg4dr1jtUu', 'experiment_LSTM.ipynb')
    #,('1iuDYJ7wqm4Bh8iIPvPKylCBnsc0aLPN6', 'descriptive_stats_experiment_data.ipynb')
]

def download_file(service, file_id, output_file):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(output_file, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Downloading {output_file}: {int(status.progress() * 100)}%")

def download_folder_content(service, folder_id, output_folder_path):
    """Recursively downloads all files from a Google Drive folder."""
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
        print(f"Created directory: {output_folder_path}")

    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])

    if not items:
        print(f"No files found in folder {folder_id}.")
        return

    for item in items:
        file_name = item['name']
        file_id = item['id']
        mime_type = item['mimeType']
        
        item_path = os.path.join(output_folder_path, file_name)

        if mime_type == 'application/vnd.google-apps.folder':
            print(f"Found subfolder: {file_name}. Entering...")
            download_folder_content(service, file_id, item_path)
        else:
            download_file(service, file_id, item_path)
            
def main():
    service_account_info = json.loads(SERVICE_ACCOUNT_INFO)
    creds = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    for file_id, output_file in FILES_TO_DOWNLOAD:
        download_file(service, file_id, output_file)
        print(f"File {output_file} successfully downloaded.")
    
    folder_id, output_folder_name = FOLDER_TO_DOWNLOAD
    download_folder_content(service, folder_id, output_folder_name)
    print(f"Folder '{output_folder_name}' and its contents successfully downloaded.")


if __name__ == '__main__':
    main()
