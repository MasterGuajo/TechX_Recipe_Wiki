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

    def upload(self):
        pass

    def sign_up(self, new_user, username):
        storage_client = storage.Client()
        bucket = storage_client.bucket("userpass")
        blob = bucket.blob(username)
        with blob.open("w") as f:
            f.write(json.dumps(new_user))
        return storage.Blob(bucket=bucket, name=username).exists(storage_client)

    def sign_in(self, existing_user, username):
        '''storage_client = storage.Client()
        blobs = storage_client.list_blobs("userpass")
        for blob in blobs:
            if json.dumps(existing_user) == blob.download_as_string(client=None):
                return True
            else:
                return False'''
        storage_client = storage.Client()
        bucket = storage_client.bucket("userpass")
        blob = bucket.blob(username)
        if blob.exists():
            return True
        else:
            return False



    def get_image(self):
        pass

