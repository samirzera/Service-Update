import boto3
import os
import tarfile
import zipfile
import shutil
import logging
from ultralytics import YOLO
from botocore.exceptions import NoCredentialsError

logging.basicConfig(level=logging.INFO)  # Configura o nível de log para INFO

def download_file_from_s3(bucket_name, s3_key, local_path, s3_client):
    try:
        s3_client.download_file(bucket_name, s3_key, local_path)
        logging.info(f'Successfully downloaded {s3_key} to {local_path}')
    except NoCredentialsError:
        logging.error('Credentials not available')

def extract_file(file_path, extract_to):
    try:
        if file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
        elif file_path.endswith('.tar') or file_path.endswith('.tar.gz'):
            with tarfile.open(file_path, 'r:*') as tar_ref:
                tar_ref.extractall(extract_to)
        logging.info(f'Extracted {file_path} to {extract_to}')
    except Exception as e:
        logging.error(f'Error extracting file: {e}')

def get_download_link(model_txt_path):
    try:
        with open(model_txt_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        logging.error(f'{model_txt_path} not found')
        return None

def update_model_txt_and_download_best(base_path, aws_access_key_id, aws_secret_access_key):
    app_path = os.path.join(base_path, 'deploy', 'app')
    model_txt_path_in_app = os.path.join(app_path, 'model.txt')
    model_txt_path_in_base = os.path.join(base_path, 'model.txt')

    if not os.path.exists(model_txt_path_in_base):
        shutil.copy(model_txt_path_in_app, model_txt_path_in_base)
        logging.info(f'Copied model.txt from {app_path} to {base_path}')
        download_best_pt(get_download_link(model_txt_path_in_app), os.path.join(base_path, 'files', 'models', 'detection', 'best.pt'), aws_access_key_id, aws_secret_access_key)
    else:
        download_link_in_app = get_download_link(model_txt_path_in_app)
        download_link_in_base = get_download_link(model_txt_path_in_base)

        if download_link_in_app and download_link_in_base:
            if download_link_in_app != download_link_in_base:
                shutil.copy(model_txt_path_in_app, model_txt_path_in_base)
                logging.info(f'Updated model.txt in {base_path} and downloading best.pt')
                download_best_pt(download_link_in_app, os.path.join(base_path, 'files', 'models', 'detection', 'best.pt'), aws_access_key_id, aws_secret_access_key)
            else:
                logging.info('model.txt in base is already up-to-date')

def download_best_pt(download_link, download_path, aws_access_key_id, aws_secret_access_key):
    try:
        os.makedirs(os.path.dirname(download_path), exist_ok=True)
        
        s3_client = boto3.client('s3',
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)
        parts = download_link.replace("s3://", "").split('/', 1)
        bucket_name = parts[0]
        s3_key = parts[1]
        s3_client.download_file(bucket_name, s3_key, download_path)
        logging.info(f'Downloaded best.pt to {download_path}')

        # Convert best.pt to best.engine
        convert_to_engine(download_path)
    except NoCredentialsError:
        logging.error('Credentials not available')
    except Exception as e:
        logging.error(f'Error downloading best.pt: {e}')

def convert_to_engine(best_pt_path):
    try:
        model = YOLO(best_pt_path)
        model.export(format="engine", half=True, imgsz=640)
        logging.info(f'Converted {best_pt_path} to engine format')
    except Exception as e:
        logging.error(f'Error converting {best_pt_path} to engine format: {e}')

def main():
    aws_access_key_id = '*************'  # Substitua com suas credenciais AWS
    aws_secret_access_key = '*************'  # Substitua com suas credenciais AWS
    
    base_path = os.getenv('********************')
    if not base_path:
        logging.error('Environment variable *************** not set')
        return

    deploy_path = os.path.join(base_path, 'deploy')
    local_zip_path = os.path.join(deploy_path, 'deploy.zip')
    extract_path = base_path

    os.makedirs(deploy_path, exist_ok=True) 

    s3_client = boto3.client('s3',
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)
    bucket_name = '*************'
    s3_key = '************************'

    download_file_from_s3(bucket_name, s3_key, local_zip_path, s3_client)
    extract_file(local_zip_path, extract_path)

    update_model_txt_and_download_best(extract_path, aws_access_key_id, aws_secret_access_key)

if __name__ == "__main__":
    main()
