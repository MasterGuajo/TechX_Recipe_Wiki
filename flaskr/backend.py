from google.cloud import storage
from flask import Flask, flash, request, redirect, url_for, send_file
import base64
import io
import json
import random
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
        bucket = self.storage_client.bucket("userpass")
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
        resulting_pages: An array of the user's prefered categories.
    """

    def get_preferences(self, user):
        """ Gets user preferences from user json file.
        If user does not have a preferences key, return an
        empty list.

        Args:
            user: User to extract json file from.
        Returns:
            preferences: An array of recipes that fall with user preferences
        """
        storage_client = storage.Client()
        bucket = storage_client.bucket("userpass")
        blob = bucket.blob(user.username)
        if blob.exists():
            user_data = json.loads(blob.download_as_bytes(client=None))
            if 'preferences' not in user_data:
                return []
            else:
                return user_data["preferences"]
        else:
            return []

    def store_preferences(self, user, new_preferences):
        """ Stores user preferences into user json file.
        If user does not have a preferences key, call 
        reset preferences to create preferences key with
        an empty array.

        Args:
            user: User to write json file into.
        Returns:
            boolean: True if storing was successful, false otherwise.
        """
        storage_client = storage.Client()
        bucket = storage_client.bucket("userpass")
        blob = bucket.blob(user.username)
        if blob.exists():
            user_data = json.loads(blob.download_as_bytes(client=None))
            if 'preferences' not in user_data:
                self.reset_preferences(user)
                user_data = json.loads(blob.download_as_bytes(client=None))
            for pref in new_preferences:
                if pref not in user_data["preferences"]:
                    user_data["preferences"].append(pref)
            with blob.open("w") as f:
                f.write(json.dumps(user_data))
            return True
        else:
            return False

    def reset_preferences(self, user):
        """ Overwrites user preferences from user json file.

        Args:
            user: User to write json file into.
        """
        storage_client = storage.Client()
        bucket = storage_client.bucket("userpass")
        blob = bucket.blob(user.username)
        if blob.exists():
            user_data = json.loads(blob.download_as_bytes(client=None))
            user_data["preferences"] = []
            with blob.open("w") as f:
                f.write(json.dumps(user_data))
            return

    def delete_preferences(self, user, deleted_preferences):
        """ Deletes selected preferences from user json file.

        Args:
            user: User to extract json file from.
        Returns:
            result: An array of the remaining categories.
        """
        storage_client = storage.Client()
        bucket = storage_client.bucket("userpass")
        blob = bucket.blob(user.username)
        if blob.exists():
            user_data = json.loads(blob.download_as_bytes(client=None))
            original = user_data["preferences"]
            delete = deleted_preferences

            result = [element for element in original if element not in delete]

            user_data["preferences"] = result
            with blob.open("w") as f:
                f.write(json.dumps(user_data))
            return result

    """ Deletes preferences from user input
    Accesses the current users preferences, and using list comprehension, makes a new list that 
    removes only the elements that the user selected

    Args:
        User and list of soon to be deleted_preferences

    Returns:
        Newly updated user_preferences
    """

    def belongs_to_game(self, game_titles):
        """Iterate through pages, evaluate if their game title
            belongs to the list of titles the user chose.
            Return all pages that match the game title.        

        Args:
          game_titles: List of game titles selected by the user.
        """
        result_pages = []
        storage_client = storage.Client()
        blobs = storage_client.list_blobs("nrjcontent",
                                          prefix="pages/",
                                          delimiter="/")
        for blob in blobs:
            page_data = json.loads(blob.download_as_bytes(client=None))
            for game in game_titles:
                if game.lower() == page_data["game"].lower():
                    result_pages.append(page_data)
        return result_pages

    def is_quick_enough(self, time_range):
        """Iterate through pages, evaluate if their time
            belongs to the time the user chose.
            Return all pages that match the time.        

        Args:
          time_range: Int value representing minutes.
        """
        result_pages = []
        storage_client = storage.Client()
        blobs = storage_client.list_blobs("nrjcontent",
                                          prefix="pages/",
                                          delimiter="/")
        for blob in blobs:
            page_data = json.loads(blob.download_as_bytes(client=None))
            if int(time_range) >= int(page_data["time"]):
                result_pages.append(page_data)
        return result_pages

    def surprise_me(self):
        """Returns a random page my using the random
            module to select a randomized index from 
            the list of all recipe pages.
        """
        storage_client = storage.Client()
        blobs = list(
            storage_client.list_blobs("nrjcontent",
                                      prefix="pages/",
                                      delimiter="/"))
        index = random.randint(0, len(blobs) - 1)
        blob = blobs[index]
        page_data = json.loads(blob.download_as_bytes(client=None))
        return page_data

    def create_copy_file(self, json_string):
        try:
            json_object = json.loads(json_string)
        except ValueError:
            return  #Bad json input passed

        storage_client = storage.Client()
        bucket = storage_client.bucket("nrjcontent")

        #creation of unique temp name for new blob
        counter = 1
        new_blob_name = None
        while True:
            new_blob_name = json_object["blobname"][:-5] + "(" + str(
                counter) + ")" + json_object["blobname"][-5:]
            if storage.Blob(bucket=bucket, name="pages/temp/" +
                            new_blob_name).exists(storage_client):
                counter += 1
                continue
            else:
                break

        blob = bucket.blob("pages/temp/" + new_blob_name)
        blob.upload_from_string(json.dumps(json_object))
        return blob.name

    """ Creates a blob in temp folder from json object

    Gets a json string as a parameter, and encodes it. Creates a unique filename for the new blob
    to be stored in the temp/ folder and uploads that json data into it. To be used with forms in
    /check_page route, see pages.py.

    Args:
        json_string: a string containing a json object to be encoded
        Ex: '{ "test":"test", "test2":"test2" }'
    Returns:
        Creates new object in temp/ folder from json data, returns nothing.
    """

    def overwrite_original_file(self, old_blob_name):
        storage_client = storage.Client()
        bucket = storage_client.bucket("nrjcontent")

        if old_blob_name[-5:] != ".json" or old_blob_name[
                -6] != ")" or old_blob_name[-8] != "(":
            return  #Bad input string

        new_blob_name = old_blob_name[:-8] + old_blob_name[-5:]

        destination = bucket.blob("pages/" + new_blob_name)
        sources = [bucket.blob("pages/temp/" + old_blob_name)]
        destination.compose(sources)
        sources[0].delete()
        return

    """ Gets a blob from temp/ folder and overwrites blob with same name in pages/ with it.

    Gets a string with a blob name as a param, gets the blob with that name in temp/ folder. 
    Then overwrites original file in pages/ with that temp/ blob removing the version number [(2)].
    To be used with the admin approvals and update the original pages of the wiki. To be used with forms in
    /check_page route, see pages.py.

    Args:
        old_blob_name: string with input of the blob name
        MUST be in format of "whatevername(2).json" -- anything before the parentheses
        doesn't matter, but it must end with "(*number*).json"
        Ex: 'pages_test_file(1).json'
    Returns:
        Updates original file and deletes temp/ file, returns nothing.
    """

    def get_game_categories(self):

        storage_client = storage.Client()
        blobs = storage_client.list_blobs("nrjcontent",
                                          prefix="pages/",
                                          delimiter="/")

        game_categories = set()

        for blob in blobs:
            page_data = json.loads(blob.download_as_bytes(client=None))

            if 'game' not in page_data:
                continue

            elif page_data['game'] not in game_categories:
                if page_data['game'] != "":
                    game_categories.add(page_data['game'])

        return game_categories

    """ Obtains all game titles in current recipes
    Parses through all recipe JSONs in our bucket and creates a set of 
    all game titles available

    Args:
        None

    Returns:
        A set of game titles
    """

    def get_time_ranges(self):

        storage_client = storage.Client()
        blobs = storage_client.list_blobs("nrjcontent",
                                          prefix="pages/",
                                          delimiter="/")

        time_ranges = set()

        for blob in blobs:
            page_data = json.loads(blob.download_as_bytes(client=None))

            if 'time' not in page_data:
                continue

            elif page_data['time'] not in time_ranges:
                if page_data['time'] != "":
                    time_ranges.add(page_data['time'])

        return time_ranges

    """ Obrains all time ranges in current recipes
    Parses through all recipe JSONs in bucket and creates a set of all 
    time ranges available

    Args:
        None

    Returns:
        A set of time ranges    
    """
