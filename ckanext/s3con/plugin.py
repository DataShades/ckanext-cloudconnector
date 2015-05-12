#encoding=utf-8
import ckan.plugins as plugins

import logging
log = logging.getLogger(__name__)

class S3Plugin(plugins.SingletonPlugin):
  plugins.implements(plugins.IRoutes, inherit=True)

  def after_map(self, map):
    # log.warn(help(map))
    map.connect('s3_upload', '/dataset/{id}/resource/{resource_id}/download/{filename}', controller='ckanext.s3con.controller:S3Controller', action='file_upload')
    map.connect('s3_original_ckan_upload', '/dataset/{id}/resource/{resource_id}/original/download/{filename}', controller='package', action='resource_download')
    return map


