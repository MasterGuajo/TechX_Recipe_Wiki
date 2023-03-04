from google.cloud import storage
import json
# TODO(Project 1): Implement Backend according to the requirements.
class Backend:

    def __init__(self):
        pass
        
    #changed to check id instead of name
    def get_wiki_page(self, id):
        storage_client = storage.Client()
        blobs = storage_client.list_blobs("nrjcontent", prefix="pages/", delimiter="/")
        for blob in blobs:
            page_data = json.loads(blob.download_as_string(client=None))
            if id == int(page_data["id"]):
                return page_data

    #changed to return full list of page data instead of names
    def get_all_pages(self):
        storage_client = storage.Client()
        blobs = storage_client.list_blobs("nrjcontent", prefix="pages/", delimiter="/")
        all_pages_data = []
        for blob in blobs:
            page_data = json.loads(blob.download_as_string(client=None))
            all_pages_data.append(page_data)
        return all_pages_data

    def upload(self,bucket_name,blob_name):
        
        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)

        blob = bucket.blob(blob_name)

        blob.upload_from_filename(blob_name)

        return

    def sign_up(self, new_user, username):
        storage_client = storage.Client()
        bucket = storage_client.bucket("userpass")
        blob = bucket.blob(username)
        if blob.exists():
            return False
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



    def get_image(self,bucket_name,blob_name):
        # imageObj = open(blob_name, 'rb')
        # imageBytes = imageObj.read()

        # return send_file(io.BytesIO(imageBytes))
        pass