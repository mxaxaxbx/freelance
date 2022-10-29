import firebase_admin
from firebase_admin import credentials

from google.cloud import firestore, storage, exceptions

if not firebase_admin._apps:
    cred = credentials.Certificate('service_account.json')
    app = firebase_admin.initialize_app( cred )

try:
    db = firestore.Client()

except Exception as e:
    print("Firestore Client Exception: ", e)
    raise e

DEFAULT_BUCKET = "yesplayer-17bbe.appspot.com"

class StorageFile:

    def get_default_bucket() -> object:
        try:
            storage_client = storage.Client()
            default_bucket = storage_client.get_bucket( DEFAULT_BUCKET )
            return default_bucket
        
        except exceptions.NotFound as e:
            print("StorageFile get_default_bucket Exception:", e)
            return None

    @staticmethod
    def save_file( file_name: str, blob_content: bytes, file_content_type: str, meta_data: object, folder_path: str, make_public: bool, from_origin: str, save_log: bool, options: object ) -> object:
       
        store_file_path = "{}/{}".format( folder_path, file_name )

        try:
            bucket = StorageFile.get_default_bucket()

            if not bucket: return { 'error': "Unexpected Error: Bucket '{0}', Not Found".format( DEFAULT_BUCKET ) }

            blob = bucket.blob( store_file_path )
           
            blob.upload_from_string( blob_content, content_type=file_content_type )

            update_meta_data  = None
            allow_public      = False
            allow_make_public = False
           
            if make_public is True or allow_public is True:
                allow_make_public = True
                blob.make_public()

            return {
                'storage_id' : blob.id,
                'url'        : blob.public_url if allow_make_public is True else store_file_path,
                'is_public'  : allow_make_public,
                'meta_data'  : update_meta_data,
            }

        except Exception as e:
            print("An error occurred while saving the file to gcs.")
            print("StorageFile save_file Exception: {0}".format(str(e)))

            return { 'error': str(e) }
