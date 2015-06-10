import ckan.lib.navl.validators as v

schema = {
    'ckan.cloud_storage_enable': [],
    'ckan.cloud_storage_provider': [],
    'ckan.cloud_failover': [],
    'save': [v.ignore],
  }


def default_cloud_connector_schema():
  return schema


def default_cloud_connector_schema_update(changes):
  schema.update(changes)
