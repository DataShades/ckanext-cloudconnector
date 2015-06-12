from boto.s3.connection import S3Connection
from boto.s3.key import Key
import pylons
from md5 import md5
import ckan.lib.navl.validators as v
from ckanext.cloud_connector.controllers.uploader import (
  AbstractConnectorUpload,
  add_storage_globals)

from ckanext.cloud_connector.action.schema import (
  default_cloud_connector_schema_update)

import logging
log = logging.getLogger(__name__)

config = pylons.config
bucket_postfix = md5(config.get('app_instance_uuid')).hexdigest()


azure_option_items = {
  'ckan.azure_aws_key': {'default': ''},
  'ckan.azure_secret_key': {'default': ''},
}

add_storage_globals(azure_option_items)

schema_changes = {
  'ckan.azure_aws_key': [v.ignore_missing, v.not_empty],
  'ckan.azure_secret_key': [v.ignore_missing, v.not_empty],
}
default_cloud_connector_schema_update(schema_changes)


markdown = [
  {
    'name': 'ckan.azure_aws_key',
    'control': 'input',
    'label': 'Azure Key',
    'placeholder': 'Microsoft Azure Access Key',
    'classes': 'disablable required-for-testing'},
  {
    'name': 'ckan.azure_secret_key',
    'control': 'input',
    'label': 'Azure Secret Key',
    'placeholder': 'Microsoft Azure Secret Key',
    'classes': 'disablable required-for-testing'},
]


class AzureUpload(AbstractConnectorUpload):

  cloud_base_link = 'https://s3.amazonaws.com/'

  @classmethod
  def __friendly_info__(cls):
    return {
      'title': 'Microsoft Azure',
      'name': 'Azure',
      'class': cls,
      'markdown': markdown
      }

  def __init__(self, resource):
    super(AzureUpload, self).__init__(resource)

    AZURE_KEY = config.get('ckan.azure_aws_key')
    AZURE_SECRET = config.get('ckan.azure_secret_key')
    _s3_conn = S3Connection(
      AZURE_KEY,
      AZURE_SECRET
      ) if AZURE_KEY and AZURE_SECRET else None

    self.cloud_conn = _s3_conn
    if not _s3_conn:
      return
    self.bucket_name = config.get(
      'ckan.site_id', 'ckan_site_id'
      ) + bucket_postfix

    bucket = _s3_conn.lookup(self.bucket_name)
    if not bucket:
      try:
        bucket = _s3_conn.create_bucket(self.bucket_name)
      except Exception, e:
        log.warn(e)
        if self.failover == '1':
          self.cloud_conn = None
          return
        elif self.failover == '2':
          raise e

    self.bucket = bucket

  def upload(self, id, max_size=10):
    if not self.cloud_conn or not self.bucket:
      return super(AzureUpload, self).upload(id, max_size)

    self.directory = 'resource'

    try:
      bucket_key = Key(self.bucket)

      if self.filename:
        filepath = '/'.join((self.directory, id, self.filename))
        bucket_key.key = filepath
        if self.content_type:
          bucket_key.content_type = self.content_type
        self.upload_file.seek(0)
        bucket_key.set_contents_from_file(self.upload_file)
        bucket_key.make_public()
        bucket_key.close()
      return self.cloud_base_link + self.bucket_name + '/' + filepath
    except Exception, e:
      log.warn(e)
