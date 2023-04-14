from google.cloud import storage
from flask import Flask, flash, request, redirect, url_for, send_file
import base64
import io
import json
"""Backend Class for Program, Retrieves Data from Cloud Storage for Use.

Typical usage example:

from flaskr.backend import Backend

  backend = Backend(0)
  Backend.get_wiki_page(None, 0)
"""
#teeest


class Backend:
    '''def __init__(self,client):
        self.client = client'''

    def __init__(self, storage_client=storage.Client()):
        self.storage_client = storage_client

    #changed to check id instead of name
    def get_wiki_page(self, id):
        storage_client = storage.Client()
        blobs = storage_client.list_blobs("nrjcontent",
                                          prefix="pages/",
                                          delimiter="/")
        for blob in blobs:
            page_data = json.loads(blob.download_as_bytes(client=None))
            if id == int(page_data["id"]):
                return page_data

    """Function for retrieving a page with specific ID.

    Searches the content/pages bucket for a blob matching a specific id parameter. Returns
    a JSON object with the data of object with that id.

    Returns:
        Populated JSON object.
    """

    def get_all_pages(self):
        storage_client = storage.Client()
        blobs = storage_client.list_blobs("nrjcontent",
                                          prefix="pages/",
                                          delimiter="/")
        all_pages_data = []
        for blob in blobs:
            page_data = json.loads(blob.download_as_bytes(client=None))
            all_pages_data.append(page_data)
        return all_pages_data

    """Function for retrieving all page objects.

    Adds all JSON objects within the the content/pages bucket into a list to return.

    Returns:
        List of all page JSON objects.
    """

    def upload(self, bucket_name, blob_name):

        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)

        blob = bucket.blob("pages/" + blob_name)

        blob.upload_from_filename(blob_name)

        return

    """ Uploads allowed files into bucket
        After checking that its a valid file from pages.py, we take in the object we would
        like to upload and specfiy the route in which our file will be stored

    Args:
        bucket_name: Shows us where the object will be stored
        blob_name: The file that is going to be uploaded
    
    Returns:
        Doesn't return anything as we are only communicating it with our backend

    """

    def sign_up(self, new_user, password):
        """If username and password combination do not exist,
        create a blob with said information and send it to the
        userpass bucket to keep. Return if blobs exists after writing, 
        or false if it already existed.

        Args:
          new_user: User object that holds username.
          password: String that holds hashed password with prefix.
        """
        #storage_client = storage.Client()
        bucket = self.storage_client.bucket("userpass")
        blob = bucket.blob(new_user.username)
        info = dict()
        info["password"] = password
        info["preferences"] = []
        #info["favorites"] = []
        if blob.exists():
            return False
        with blob.open("w") as f:
            f.write(json.dumps(info))
        return storage.Blob(bucket=bucket,
                            name=new_user.username).exists(self.storage_client)

    def sign_in(self, existing_user, password):
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
            user_data = json.loads(blob.download_as_bytes(client=None))
            if user_data["password"] == password:
                return True
            else:
                return False
        else:
            return False

    def get_image(self, blob_name):

        storage_client = storage.Client()
        bucket = storage_client.bucket("nrjcontent")
        # bucket = storage_client.bucket("nrjcontent/images/authors")
        blob = bucket.blob(blob_name)

        imageObj = blob.open('rb')
        imageBytes = imageObj.read()

        return base64.b64encode(imageBytes)

    """ Retrieves images from Bucket

    Retrieves images specified from pages.py from predetermined bucket
    and encodes them so they can be used in HTML.

    Args:
        blob_name: Takes in name of files that are going to be retrieved. 
        Ex: 'image.png'
    Returns:
        The Bytes of the image with base64 encoding.
    """

    def get_recipe_categories(self):

        storage_client = storage.Client()
        blobs = storage_client.list_blobs("nrjcontent",
                                          prefix="pages/",
                                          delimiter="/")

        recipe_categories = set()

        for blob in blobs:
            page_data = json.loads(blob.download_as_bytes(client=None))

            if 'cate' not in page_data:
                continue

            elif page_data['cate'] not in recipe_categories:
                if page_data['cate'] != "":
                    recipe_categories.add(page_data['cate'])

        return recipe_categories

    """ Obtains categories available in recipes
    Parses through JSON files and adds newly seen categories to a set so that they can be
    displayed in HTML

    Args:
        Self
    Returns:
        A set of categories found
    """

    def get_selected_categories(self, selected_categories):

        storage_client = storage.Client()
        blobs = storage_client.list_blobs("nrjcontent",
                                          prefix="pages/",
                                          delimiter="/")

        resulting_pages = []

        for blob in blobs:
            page_data = json.loads(blob.download_as_bytes(client=None))

            if 'cate' not in page_data:
                continue

            elif page_data['cate'] in selected_categories:

                if page_data['cate'] != "":
                    resulting_pages.append(page_data)

        return resulting_pages

    """ Gets recipes that fall into selected categories
    Parses through the JSON recipes and compares their categories to see 
    if they will be returned

    Args:
        selected_categories: An array of user preferences
    Returns:
        resulting_pages: An array of recipes that fall with user preferences
    """

    def get_preferences(self, user):
        storage_client = storage.Client()
        bucket = storage_client.bucket("userpass")
        blob = bucket.blob(user.username)
        if blob.exists():
            user_data = json.loads(blob.download_as_bytes(client=None))
            return user_data["preferences"]
        else:
            return []

    def store_preferences(self, user, new_preferences):
        storage_client = storage.Client()
        bucket = storage_client.bucket("userpass")
        blob = bucket.blob(user.username)
        if blob.exists():
            user_data = json.loads(blob.download_as_bytes(client=None))
            for pref in new_preferences:
                user_data["preferences"].append(pref)
            with blob.open("w") as f:
                f.write(json.dumps(user_data))
            return True
        else:
            return False

    def reset_preferences(self, user):
        storage_client = storage.Client()
        bucket = storage_client.bucket("userpass")
        blob = bucket.blob(user.username)
        if blob.exists():
            user_data = json.loads(blob.download_as_bytes(client=None))
            user_data["preferences"] = []
            with blob.open("w") as f:
                f.write(json.dumps(user_data))
            return
