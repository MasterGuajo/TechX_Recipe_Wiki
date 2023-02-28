from google.cloud import storage
import json

# TODO(Project 1): Implement Backend according to the requirements.
class Backend:

    def __init__(self):
        pass
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self,bucket_name,blob_name):
        
        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)

        blob = bucket.blob(blob_name)

        blob.upload_from_filename(blob_name)

        return

    def sign_up(self):
        pass

    def sign_in(self):
        pass

    def get_image(self,bucket_name,blob_name):
        pass
