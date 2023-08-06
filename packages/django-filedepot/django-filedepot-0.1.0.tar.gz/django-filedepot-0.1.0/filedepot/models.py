import logging
import os
import shutil

from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.core.files import File

User = get_user_model()

#-------------------------------------------------------------------------------
def file_depot_base_path():
    return settings.FILE_DEPOT_BASE_PATH

#-------------------------------------------------------------------------------
class DjangoFile(File):
    def __init__(self, file):
        super(DjangoFile, self).__init__(open(file.full_filename, "rb"))
        self.name = file.flow_filename

#-------------------------------------------------------------------------------
class File(models.Model):
    uuid = models.CharField(max_length=64, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chunks_directory = models.FilePathField(
        path=file_depot_base_path,
        max_length=1024,
        blank=True,
        null=True
    )

    is_complete = models.BooleanField(default=False)
    flow_filename = models.CharField(max_length=255)
    flow_total_chunks = models.PositiveIntegerField()
    flow_chunk_size = models.PositiveIntegerField()
    flow_total_size = models.PositiveIntegerField()

    # TODO: Not supporting directory uploads for now.
    # flow_relative_path = ...

    #---------------------------------------------------------------------------
    def django_file(self):
        """Return an instance of django.file.File that can be saved.
        """
        return DjangoFile(self)

    def ensure_directory(self):
        if not self.chunks_directory:
            self.chunks_directory = os.path.join(
                settings.FILE_DEPOT_BASE_PATH,
                self.uuid,
            )
            self.save()
        if not os.path.exists(self.chunks_directory):
           os.makedirs(self.chunks_directory)
        if not os.path.isdir(self.chunks_directory):
            error_message = "File Depot can't create directory because file is in the way: {0}".format(self.chunks_directory)
            logging.log(msg=error_message, level=logging.ERROR)
            raise IOError(error_message)

    #---------------------------------------------------------------------------
    def check_if_finished(self):
        for i in range(1, self.flow_total_chunks + 1):
            filename = self.chunk_finished_filename(i)
            if os.path.exists(filename):
                continue
            else:
                return False

        return True

    #---------------------------------------------------------------------------
    def join_chunks(self):
        with open(self.full_filename, "wb") as full_file_fd:
            for i in range(1, self.flow_total_chunks + 1):
                filename = self.chunk_filename(i)
                with open(filename, "rb") as chunk_fd:
                    full_file_fd.write(chunk_fd.read())

    #---------------------------------------------------------------------------
    def verify_chunk(self, chunk_number):
        chunk_filename = self.chunk_filename(chunk_number)
        if not os.path.exists(chunk_filename):
            return False
        return True

    #---------------------------------------------------------------------------
    def chunk_filename(self, chunk_number):
        filename = '{}.chunk'.format(chunk_number)
        return os.path.join(self.chunks_directory, filename)

    #---------------------------------------------------------------------------
    def chunk_finished_filename(self, chunk_number):
        filename = '{}.chunk.finished'.format(chunk_number)
        return os.path.join(self.chunks_directory, filename)

    #---------------------------------------------------------------------------
    @property
    def full_filename(self):
        return os.path.join(self.chunks_directory, 'full-file')

    #---------------------------------------------------------------------------
    def delete_chunks(self):
        if not self.chunks_directory:
            return
        if os.path.exists(self.chunks_directory):
            shutil.rmtree(self.chunks_directory)

    #---------------------------------------------------------------------------
    def delete(self, *args, **kwargs):
        self.delete_chunks()
        super(File, self).delete(*args, **kwargs)
