import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.logic as logic
import ckan.lib.app_globals as app_globals
import ckan.plugins.toolkit as tk
from pylons import config
from ckan.common import request

import ckan.model as model

import logging

from ckanext.cloud_connector.controllers.uploader import (
  additional_config,
  get_uploaders)

import ckanext.cloud_connector.action.schema as schema
from ckan.lib.navl.dictization_functions import validate
from ckan.logic import ValidationError
import ckanext.cloud_connector.controllers.uploader as uploader
from pylons.decorators import jsonify

session = model.Session
log = logging.getLogger(__name__)
c = base.c


def _update_config(data):
  if 'save' in data:
    data, errors = validate(data, schema.default_cloud_connector_schema())
    if errors:
      raise ValidationError(errors)

    items = map(lambda i: (i, data[i]),
                filter(lambda x: x in data, additional_config))

    data = logic.get_action('config_option_update')(
              {'user': c.user}, dict(items))
    h.redirect_to(
      controller='ckanext.cloud_connector.controllers.controller:CCController',
      action='config')

  data = {}
  for item in additional_config:
    data[item] = config.get(item)
  data['ckan.cloud_storage_enable'] = tk.asbool(
    data['ckan.cloud_storage_enable'] or 'false'
    )
  return data


class CCController(base.BaseController):

  _controller = 'ckanext.cloud_connector.controllers.controller:CCController'

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
       controller=self._controller,
       action='config')

    if request.method == 'POST':
      for item in additional_config:
        app_globals.delete_global(item)
      app_globals.reset()

    h.redirect_to(
      controller=self._controller,
      action='config')

  @jsonify
  def test_config(self):
    result = uploader.test_config(
      request.params['provider'],
      request.params.getall('values[]'))

    return result
