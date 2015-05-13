import pylons
import logging

from ckan.lib.uploader import ResourceUpload

from boto.s3.connection import S3Connection
from boto.s3.key import Key

config = pylons.config
log = logging.getLogger(__name__)

from ckan.lib.uploader import (
  get_storage_path,
  get_max_image_size,
  get_max_resource_size,
)

class S3Upload(ResourceUpload):
  def __init__(self, resource):
    super(S3Upload, self).__init__(resource)

    AWS_KEY = config.get('s3.aws_key')
    AWS_SECRET = config.get('s3.aws_secret')
    _s3_conn = S3Connection(AWS_KEY, AWS_SECRET) if AWS_KEY and AWS_SECRET else None
    self.s3_conn = _s3_conn
    if not _s3_conn:
      return
    self.bucket_name = 'ckan_bucket_' + config.get('ckan.site_id', 'ckan_site_id')
    bucket = _s3_conn.lookup(self.bucket_name)
    if not bucket:
      bucket = _s3_conn.create_bucket(self.bucket_name)

    self.bucket = bucket

  def upload(self, id, max_size=10):
    if not self.s3_conn or not self.bucket:
      super(S3Upload, self).upload(id, max_size)
      return

    directory = 'resource'
    filepath = '/'.join((directory, id))

    bucket_key = Key(self.bucket)

    bucket_key.key = filepath
    if self.filename:
      self.upload_file.seek(0)
      bucket_key.set_contents_from_file(self.upload_file)
      bucket_key.close()

  def _clean_whole_bucket(self):
    if self.s3_conn or self.bucket:
      for key in self.bucket.list():
        key.delete()
