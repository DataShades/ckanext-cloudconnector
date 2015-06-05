import ckan.lib.navl.validators as v


def default_cloud_connector_schema():
  schema = {
    'ckan.cloud_storage_enable': [],
    'ckan.cloud_failover': [],
    'ckan.s3_aws_key': [v.ignore_missing, v.not_empty],
    'ckan.s3_secret_key': [v.ignore_missing, v.not_empty],
    'save': [v.ignore],
  }
  return schema
