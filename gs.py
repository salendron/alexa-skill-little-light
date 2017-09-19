from gcloud import storage
from gcloud.storage.blob import Blob

class xamoom_acl(object):

    #actors
    ALL = 0
    ALL_AUTH = 1
    DOMAIN = 2
    GROUP = 3
    USER = 4

    #rights
    GRANT_READ = 0
    GRANT_WRITE = 1
    GRANT_OWNER = 2
    REVOKE_READ = 3
    REVOKE_WRITE = 4
    REVOKE_OWNER = 5

    #members
    actor = None
    actor_name = None
    right = None

    def __init__(self,actor,right,actor_name=None):
        self.actor = actor
        self.actor_name = actor_name
        self.right = right

    def apply_acl(self,obj):
        obj_acl = None
        if self.actor == xamoom_acl.ALL:
            obj_acl = obj.acl.all()
        elif self.actor == xamoom_acl.ALL_AUTH:
            obj_acl = obj.acl.all_authenticated()
        elif self.actor == xamoom_acl.DOMAIN:
            obj_acl = obj.acl.domain(self.actor_name)
        elif self.actor == xamoom_acl.GROUP:
            obj_acl = obj.acl.group(self.actor_name)
        elif self.actor == xamoom_acl.USER:
            obj_acl = obj.acl.user(self.actor_name)

        #set acl
        if self.right == xamoom_acl.GRANT_READ:
            obj_acl.grant_read()
        elif self.right == xamoom_acl.GRANT_WRITE:
            obj_acl.grant_write()
        elif self.right == xamoom_acl.GRANT_OWNER:
            obj_acl.grant_owner()
        elif self.right == xamoom_acl.REVOKE_READ:
            obj_acl.revoke_read()
        elif self.right == xamoom_acl.REVOKE_WRITE:
            obj_acl.revoke_write()
        elif self.right == xamoom_acl.REVOKE_OWNER:
            obj_acl.revoke_owner()

        obj.acl.save()

class xamoom_storage(object):

    def __init__(self):
        self.__client = storage.Client()

    def list_blobs(self, bucket_name, dir_only=False, prefix=None):
        bucket = self.__client.get_bucket(bucket_name)

        # add slash on end
        if prefix != None and prefix.endswith('/') == False:
            prefix = prefix + '/'

        if dir_only == True:
            return bucket.list_blobs(prefix = prefix, delimiter='/')
        else:
            return bucket.list_blobs()

    def copy_blob(self, blob, destination_bucket_name, new_name=None):
        destination_bucket = self.__client.get_bucket(destination_bucket_name)
        blob.bucket.copy_blob(blob, destination_bucket, new_name=new_name)

    def upload_blob(self, source_path, destination_path,
                    destination_bucket_name, content_type):
        destination_bucket = self.__client.get_bucket(destination_bucket_name)
        blob = Blob(destination_path, destination_bucket)

        with open(source_path, 'rb') as f:
            blob.upload_from_file(f, content_type=content_type)

    def read_blob(self,bucket_name,file_name,destination_file=None):
        blob = self.download_blob(bucket_name,file_name)

        if destination_file != None:
            with open(destination_file, 'wb') as f:
                blob.download_to_file(f)
        else:
            return blob.download_as_string()

    def download_blob(self, bucket_name, file_name):
        bucket = self.__client.get_bucket(bucket_name)
        blob = bucket.get_blob(file_name)
        return blob

    def set_acl(self,bucket_name,acl,file_name=None):
        obj = self.__client.get_bucket(bucket_name)

        if file_name != None:
            obj = obj.get_blob(file_name)

        acl.apply_acl(obj)
