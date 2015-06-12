import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


import ckanext.cloud_connector.action as action
import logging
log = logging.getLogger(__name__)

import ckanext.cloud_connector.controllers.s3
import ckanext.cloud_connector.controllers.azure


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
    toolkit.add_resource('fanstatic', 'cloud_connector')

  def before_map(self, map):
    map.connect(
      'cloud_connector_config', '/ckan-admin/cloud_connector_config',
      controller='ckanext.cloud_connector.controllers.controller:CCController',
      action='config', ckan_icon='cloud')
    map.connect(
      'cloud_connector_config_reset',
      '/ckan-admin/cloud_connector_config_reset',
      controller='ckanext.cloud_connector.controllers.controller:CCController',
      action='reset_config')
    map.connect(
      'cloud_connector_config_test',
      '/ckan-admin/cloud_connector_config_test',
      controller='ckanext.cloud_connector.controllers.controller:CCController',
      action='test_config')
    return map
