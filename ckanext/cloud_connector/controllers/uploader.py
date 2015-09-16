from pylons import config
from ckan.lib.base import abort
import ckan.lib.app_globals as app_globals
from ckan.lib.uploader import ResourceUpload

import logging
log = logging.getLogger(__name__)

additional_config = {}

s3_option_items = {
  'ckan.cloud_storage_enable': {'default': 'False'},
  'ckan.cloud_storage_provider': {'default': 'S3Upload'},
  'ckan.cloud_failover': {'default': '1'},
}


def add_storage_globals(options):
  additional_config.update(options)
  app_globals.app_globals_from_config_details.update(options)

add_storage_globals(s3_option_items)


def get_uploaders():
  uploaders = dict([(item.__name__, item.__friendly_info__()) for
                    item in AbstractConnectorUpload.__subclasses__()])
  return uploaders


def get_current_uploader(provider=None):
  uploaders = get_uploaders()
  if provider is None:
    provider = config.get('ckan.cloud_storage_provider')
  uploader = uploaders[provider]['class']

  return uploader


def make_uploader(data_dict):
  uploader = get_current_uploader()(data_dict)

  return uploader


def test_config(provider, data):
  return get_current_uploader(provider).test_config(data)


class AbstractConnectorUpload(ResourceUpload):

  cloud_base_link = None

  @classmethod
  def __friendly_info__(cls):
    raise NameError('Abstract method not implemented')

  def __init__(self, resource):
    uploaded_file = resource.get('upload')
    if uploaded_file is not None:
      self.content_type = uploaded_file.type
    else:
      self.content_type = None
    super(AbstractConnectorUpload, self).__init__(resource)

    self.failover = config.get('ckan.cloud_failover')

  def upload(self, id, max_size=10):
    if self.failover == '1':
      return super(AbstractConnectorUpload, self).upload(id, max_size)
    elif self.failover == '2':
      abort('404', 'Problem with cloud')

  @staticmethod
  def test_config(data):
    result = {
      'status': 'failed',
      'message': 'Test not implemented'
    }
    return result
