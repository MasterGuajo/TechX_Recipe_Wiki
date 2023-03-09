from google.cloud import storage
from flask import Flask, flash, request, redirect, url_for, send_file

# Imports for get_image
import base64
import io

import json

# TODO(Project 1): Implement Backend according to the requirements.
class Backend:

    
    def __init__(self, storage_client = storage.Client()):
        self.storage_client = storage_client
        
        
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

    def get_image(self,blob_name):

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