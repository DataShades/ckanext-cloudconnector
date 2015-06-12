from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto import connect_s3
import pylons
from md5 import md5
import ckan.lib.navl.validators as v
from ckanext.cloud_connector.controllers.uploader import (
  AbstractConnectorUpload,
  add_storage_globals)
import boto.exception as exception

from ckanext.cloud_connector.action.schema import (
  default_cloud_connector_schema_update)

import logging
log = logging.getLogger(__name__)

config = pylons.config
bucket_postfix = md5(config.get('app_instance_uuid')).hexdigest()

s3_option_items = {
  'ckan.s3_aws_key': {'default': ''},
  'ckan.s3_secret_key': {'default': ''},
}
add_storage_globals(s3_option_items)

schema_changes = {
    'ckan.s3_aws_key': [v.ignore_missing, v.not_empty],
    'ckan.s3_secret_key': [v.ignore_missing, v.not_empty],
}
default_cloud_connector_schema_update(schema_changes)


markdown = [
  {
    'name': 'ckan.s3_aws_key',
    'control': 'input',
    'label': 'AWS Access Key',
    'placeholder': 'AWS Access Key',
    'classes': 'disablable required-for-testing'},
  {
    'name': 'ckan.s3_secret_key',
    'control': 'input',
    'label': 'AWS Secret Key',
    'placeholder': 'AWS Secret Key',
    'classes': 'disablable required-for-testing'},
]


class S3Upload(AbstractConnectorUpload):

  cloud_base_link = 'https://s3.amazonaws.com/'

  @classmethod
  def __friendly_info__(cls):
    return {
      'title': 'Amazon S3',
      'name': 'S3',
      'class': cls,
      'markdown': markdown
      }

  def __init__(self, resource):
    super(S3Upload, self).__init__(resource)

    AWS_KEY = config.get('ckan.s3_aws_key')
    AWS_SECRET = config.get('ckan.s3_secret_key')
    _s3_conn = S3Connection(
      AWS_KEY,
      AWS_SECRET
      ) if AWS_KEY and AWS_SECRET else None

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
      return super(S3Upload, self).upload(id, max_size)

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

  @staticmethod
  def test_config(data):
    try:
      test_bucket = bucket_postfix + 'test_connection'
      connect_s3(*data).create_bucket(test_bucket).delete()
      result = {
        'status': 'success',
        'message': 'OK',
      }
    except exception.BotoServerError, e:
      result = {
        'status': 'failed',
        'message': e.message
      }
    return result
