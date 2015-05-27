import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from pylons import config

import ckanext.s3con.action as action
import ckan.model as model
import logging
log = logging.getLogger(__name__)

class S3Plugin(plugins.SingletonPlugin):
  plugins.implements(plugins.IActions)
  plugins.implements(plugins.IRoutes, inherit=True)
  plugins.implements(plugins.IConfigurer)

  def get_actions(self):
    return {
      'resource_create': action.resource_create,
      'resource_update': action.resource_update,
    }

  def update_config(self, config):
    toolkit.add_template_directory(config, 'templates')
    toolkit.add_resource('fanstatic', 's3con')

  def before_map(self, map):
    map.connect(
      'cloud_connector_config', '/ckan-admin/cloud_connector_config',
      controller='ckanext.s3con.s3.controller:S3Controller',
      action='config', ckan_icon='cloud')
    map.connect(
      'cloud_connector_config_reset', '/ckan-admin/cloud_connector_config_reset',
      controller='ckanext.s3con.s3.controller:S3Controller',
      action='reset_config')
    return map



