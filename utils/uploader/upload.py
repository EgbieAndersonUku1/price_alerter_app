
from settings import UPLOAD_FOLDER
from os.path import join as join_files

class Uploader(object):
    """"""
    @staticmethod
    def create_upload_folder_path(file_name):
        """"""
        return join_files(UPLOAD_FOLDER, 'user', file_name)
