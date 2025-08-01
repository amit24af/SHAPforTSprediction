import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload

SERVICE_ACCOUNT_INFO = os.environ.get('GDRIVE_SERVICE_ACCOUNT')

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# FILE_ID1 = '18EesyISDITHMX-VLI4mjvDF4nOQ7fDsz'
# FILE_ID2 = '1wY7X3QV_0O1uS3D7s0qmanF8O2aNA331'
# FILE_ID3 = '1nLmPj6MKZecHK7ywYXKiWKtg4dr1jtUu'
# FILE_ID4 = '1iuDYJ7wqm4Bh8iIPvPKylCBnsc0aLPN6'

# OUTPUT_FILE1 = 'experiment_FBProphet.ipynb'
# OUTPUT_FILE2 = 'experiment_ARIMA.ipynb'
# OUTPUT_FILE2 = 'experiment_LSTM.ipynb'
# OUTPUT_FILE2 = 'descriptive_stats_experiment_data.ipynb'

FILES_TO_DOWNLOAD = [
    ('18EesyISDITHMX-VLI4mjvDF4nOQ7fDsz', 'experiment_FBProphet.ipynb'),
    ('1wY7X3QV_0O1uS3D7s0qmanF8O2aNA331', 'experiment_ARIMA.ipynb'),
    ('1nLmPj6MKZecHK7ywYXKiWKtg4dr1jtUu', 'experiment_LSTM.ipynb'),
    ('1iuDYJ7wqm4Bh8iIPvPKylCBnsc0aLPN6', 'descriptive_stats_experiment_data.ipynb')
]

def download_file(service, file_id, output_file):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(output_file, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Downloading {output_file}: {int(status.progress() * 100)}%")

def main():
    service_account_info = json.loads(SERVICE_ACCOUNT_INFO)
    creds = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    for file_id, output_file in FILES_TO_DOWNLOAD:
        download_file(service, file_id, output_file)
        print(f"File {output_file} successfully downloaded.")

if __name__ == '__main__':
    main()
