import ckan.lib.base as base
import ckan.lib.helpers as h

import ckan.lib.app_globals as app_globals

from pylons import config
from ckan.common import request

import ckan.model as model
session = model.Session

import logging
log = logging.getLogger(__name__)

from ckanext.cloud_connector.controllers.uploader import (
  additional_config,
  get_uploaders)

import ckanext.cloud_connector.action.schema as schema
from ckan.lib.navl.dictization_functions import validate
from ckan.logic import ValidationError


def _update_config(data):
  if 'save' in data:
    data, errors = validate(data, schema.default_cloud_connector_schema())
    if errors:
      raise ValidationError(errors)

    for item in additional_config:
      if item in data:
        app_globals.set_global(item, data[item])
    app_globals.reset()
    h.redirect_to(
      controller='ckanext.cloud_connector.controllers.controller:S3Controller',
      action='config')

  data = {}
  for item in additional_config:
    data[item] = config.get(item)
  return data


class S3Controller(base.BaseController):

  def config(self):
    data = dict([x for x in request.POST.items()])
    error_summary = {}
    errors = {}
    try:
      data = _update_config(data)
    except ValidationError, e:
      errors = e.error_dict
      error_summary = e.error_summary

    implemented_connectors = get_uploaders()
    conn_markdown = [{'value': item[0], 'text': item[1]['title']}
                     for item in implemented_connectors.items()]

    vars = {
      'data': data,
      'errors': errors,
      'form_items': additional_config,
      'error_summary': error_summary,
      'implemented_connectors': implemented_connectors,
      'conn_markdown': conn_markdown
      }
    return base.render('admin/cloud_connector_config.html', extra_vars=vars)

  def reset_config(self):
    if 'cancel' in request.params:
      h.redirect_to(
       controller=
        'ckanext.cloud_connector.controllers.controller:S3Controller',
        action='config')

    if request.method == 'POST':
      # remove sys info items
      for item in additional_config:
        app_globals.delete_global(item)
      # reset to values in config
      app_globals.reset()

    h.redirect_to(
      controller='ckanext.cloud_connector.controllers.controller:S3Controller',
      action='config')
