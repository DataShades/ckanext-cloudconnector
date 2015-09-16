import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from routes.mapper import SubMapper
from ckanext.cloud_connector.action.schema import schema as cloud_schema

import ckanext.cloud_connector.action as action
import logging
log = logging.getLogger(__name__)

import ckanext.cloud_connector.controllers.s3
# import ckanext.cloud_connector.controllers.azure


class S3Plugin(plugins.SingletonPlugin):
  plugins.implements(plugins.IActions)
  plugins.implements(plugins.IRoutes, inherit=True)
  plugins.implements(plugins.IConfigurer)

  _controller = 'ckanext.cloud_connector.controllers.controller:CCController'

  def get_actions(self):
    return {
      'resource_create': action.resource_create,
      'resource_update': action.resource_update,
    }

  def update_config(self, config):
    toolkit.add_template_directory(config, 'templates')
    toolkit.add_resource('fanstatic', 'cloud_connector')

  def update_config_schema(self, schema):
    schema.update(cloud_schema)

    return schema

  def before_map(self, map):
    with SubMapper(map, controller=self._controller) as m:
      m.connect(
        'cloud_connector_config', '/ckan-admin/cloud_connector_config',
        action='config', ckan_icon='cloud')
      m.connect(
        'cloud_connector_config_reset',
        '/ckan-admin/cloud_connector_config_reset',
        action='reset_config')
      m.connect(
        'cloud_connector_config_test',
        '/ckan-admin/cloud_connector_config_test',
        action='test_config')
    return map
