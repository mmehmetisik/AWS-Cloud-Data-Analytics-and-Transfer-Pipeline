import boto3
import os
import pandas as pd
import re
from tqdm import tqdm

class S3Bucket:
    def __init__(self, bucket_name, access_key_id, secret_access_key):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

    def upload_file(self, file_path, object_name=None):
        if object_name is None:
            object_name = file_path
        self.s3.upload_file(file_path, self.bucket_name, object_name)
        print(f"File {file_path} uploaded to {self.bucket_name}/{object_name}")

    def clean_data(self, file_path):
        # Veri temizleme işlemleri
        data = pd.read_excel(file_path)
        data.columns = data.columns.str.lower()
        data = data[pd.to_datetime(data['tarih'], errors='coerce').notna()]
        data['tarih'] = pd.to_datetime(data['tarih'])
        data = data.fillna(0)

        def contains_special_characters(val):
            if pd.isna(val):
                return False
            return bool(re.search(r'[^a-zA-Z0-9\s,.]', str(val)))

        for col in data.columns:
            special_chars = data[col].apply(contains_special_characters)
            if special_chars.any():
                data[col] = data[col].astype(str).str.replace(r'[^a-zA-Z0-9\s,.]', '', regex=True)

        return data

    @staticmethod
    def list_all_buckets():
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        for bucket in response['Buckets']:
            print(bucket['Name'])

    def sync_s3_bucket_to_directory(self, directory):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(self.bucket_name)

        if not os.path.exists(directory):
            os.makedirs(directory)

        for obj in tqdm(bucket.objects.all(), desc="Downloading files from S3"):
            file_path = os.path.join(directory, obj.key)
            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))
            bucket.download_file(obj.key, file_path)

    def sync_directory_to_s3_bucket(self, directory):
        s3 = boto3.client('s3')
        for root, _, filenames in os.walk(directory):
            for filename in tqdm(filenames, desc="Processing files"):
                local_path = os.path.join(root, filename)
                if local_path.endswith('.xlsx'):
                   
                    data = self.clean_data(local_path)
                    csv_path = local_path.replace('.xlsx', '.csv')
                    data.to_csv(csv_path, index=False)
                    print(f"Converted {local_path} to {csv_path}")

                    relative_path = os.path.relpath(csv_path, directory)
                    s3_path = f"data/{relative_path}"


                    s3.upload_file(csv_path, self.bucket_name, s3_path)
                    print(f"Uploaded {csv_path} to s3://{self.bucket_name}/{s3_path}")

                    # CSV dosyasını S3'e yükle
                    relative_path = os.path.relpath(csv_path, directory)
                    s3_path = os.path.join(self.bucket_name, relative_path).replace('\\', '/')
                    s3.upload_file(csv_path, self.bucket_name, s3_path)
                    print(f"Uploaded {csv_path} to s3://{s3_path}")

if __name__ == "__main__":
    directory_path = "/Users/nursahsgt/Desktop/grup5/ALL"
    bucket = S3Bucket(bucket_name="projegroup5", access_key_id="your_access_key_id", secret_access_key="your_secret_access_key")
    bucket.sync_directory_to_s3_bucket(directory_path)
