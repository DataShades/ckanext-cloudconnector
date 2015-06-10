import pylons

from ckan.lib.uploader import ResourceUpload

config = pylons.config

import logging
log = logging.getLogger(__name__)

from ckan.lib.base import abort

import ckan.lib.app_globals as app_globals

auto_update = app_globals.auto_update
config_details = app_globals.config_details

additional_config = {}

s3_option_items = {
  'ckan.cloud_storage_enable': {'default': 'False'},
  'ckan.cloud_storage_provider': {'default': 'S3Upload'},
  'ckan.cloud_failover': {'default': '1'},
}


def add_storage_globals(options):
  auto_update.extend(options.keys())
  config_details.update(options)
  additional_config.update(options)

add_storage_globals(s3_option_items)


def get_uploaders():
  uploaders = dict([(item.__name__, item.__friendly_info__()) for
                    item in AbstractConnectorUpload.__subclasses__()])
  return uploaders


def make_uploader(data_dict):
  uploaders = get_uploaders()
  uploader = uploaders[
    config.get('ckan.cloud_storage_provider')
    ]['class'](data_dict)

  return uploader


class AbstractConnectorUpload(ResourceUpload):

  cloud_base_link = None

  __friendly_name__ = 'Abstract and not implemented'

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
