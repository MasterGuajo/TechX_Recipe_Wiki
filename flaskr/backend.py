from google.cloud import storage
import json

# TODO(Project 1): Implement Backend according to the requirements.
class Backend:

    def __init__(self):
        pass
        
    #changed to check id instead of name
    def get_wiki_page(self, id):
        storage_client = storage.Client()
        blobs = storage_client.list_blobs("nrjcontent")
        for blob in blobs:
            page_data = json.loads(blob.download_as_string(client=None))
            if id == int(page_data["page_id"]):
                return page_data

    #changed to return full list of page data instead of names
    def get_all_pages(self):
        storage_client = storage.Client()
        blobs = storage_client.list_blobs("nrjcontent")
        all_pages_data = []
        for blob in blobs:
            page_data = json.loads(blob.download_as_string(client=None))
            all_pages_data.append(page_data)
        return all_pages_data

    def upload(self):
        pass

    def sign_up(self):
        pass

    def sign_in(self):
        pass

    def get_image(self):
        pass

