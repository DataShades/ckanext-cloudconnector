import pylons
import logging
from md5 import md5
from ckan.lib.uploader import ResourceUpload

from boto.s3.connection import S3Connection
from boto.s3.key import Key

config = pylons.config
log = logging.getLogger(__name__)

bucket_postfix = md5(config.get('app_instance_uuid')).hexdigest()
AWS_KEY = config.get('ckan.s3_aws_key')
AWS_SECRET = config.get('ckan.s3_secret_key')
_s3_conn = S3Connection(AWS_KEY, AWS_SECRET) if AWS_KEY and AWS_SECRET else None

from ckan.lib.uploader import (
  get_storage_path,
  get_max_image_size,
  get_max_resource_size,
)

class S3Upload(ResourceUpload):
  def __init__(self, resource):
    uploaded_file = resource.get('upload')
    if uploaded_file != None:
      self.content_type = uploaded_file.type
    else:
      self.content_type = None
    super(S3Upload, self).__init__(resource)

    self.s3_conn = _s3_conn
    if not _s3_conn:
      return
    self.bucket_name = config.get('ckan.site_id', 'ckan_site_id') + bucket_postfix
    bucket = _s3_conn.lookup(self.bucket_name)
    if not bucket:
      bucket = _s3_conn.create_bucket(self.bucket_name)
    resource['url_type'] = ''
    # resource['url'] = 'asdf'
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
      if self.content_type:
        bucket_key.content_type = self.content_type
      self.upload_file.seek(0)
      bucket_key.set_contents_from_file(self.upload_file)
      bucket_key.make_public()
      bucket_key.close()
    return self.bucket_name + '/' + filepath

  def _clean_whole_bucket(self):
    if self.s3_conn or self.bucket:
      for key in self.bucket.list():
        key.delete()
