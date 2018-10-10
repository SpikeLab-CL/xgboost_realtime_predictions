from config import config
from google.cloud import storage
from google.cloud.storage import Blob

def download_model(bucket, path_to_model):
    client = storage.Client()
    bucket = client.get_bucket(bucket)
    blob = Blob(path_to_model, bucket)
    obj = blob.download_as_string()
    return obj