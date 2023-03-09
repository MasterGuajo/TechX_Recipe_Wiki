from google.cloud import storage
import json
# TODO(Project 1): Implement Backend according to the requirements.
class Backend:

    def __init__(self,client):
        self.client = client
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

    def sign_up(self, new_user, password):
        """If username and password combination do not exist,
        create a blob with said information and send it to the
        userpass bucket to keep. Return if blobs exists after writing, 
        or false if it already existed.                       

        Args:
          new_user: User object that holds username.
          password: String that holds hashed password with prefix.
        """
        storage_client = self.client
        bucket = storage_client.bucket("userpass")
        blob = bucket.blob(new_user.username)
        info = {"password" : password}
        if blob.exists():
            return False                                 
        with blob.open("w") as f:
            f.write(json.dumps(info))
        return storage.Blob(bucket=bucket, name=new_user.username).exists(storage_client)

    def sign_in(self, existing_user,password):
        """If blob with username do not exist,
        return False. Return true only if blob
        with usename exists and the blob data 
        matches the username and password 
        combination.         

        Args:
          existing_user: User object that holds username.
          password: String that holds hashed password with prefix.
        """
        storage_client = storage.Client()
        bucket = storage_client.bucket("userpass")
        blob = bucket.blob(existing_user.username)
        if blob.exists():
            user_data = json.loads(blob.download_as_string(client=None))
            if user_data["password"] == password:
                return True
            else:
                return False
        else:
            return False



    def get_image(self,bucket_name,blob_name):
        # imageObj = open(blob_name, 'rb')
        # imageBytes = imageObj.read()

        # return send_file(io.BytesIO(imageBytes))
        pass