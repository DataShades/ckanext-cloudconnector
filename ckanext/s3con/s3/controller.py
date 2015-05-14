import ckan.plugins.toolkit as toolkit
import ckan.lib.base as base
import ckan.lib.helpers as h
import datetime
import os
import re
import json

import ckan.lib.app_globals as app_globals

from pylons import config
from ckan.common import c, g, _, OrderedDict, request

import ckan.model as model
session = model.Session

import logging
log = logging.getLogger(__name__)

from ckanext.s3con.action.update import s3_option_items

class S3Controller(base.BaseController):

  def config(self):
    data = request.POST
    if 'save' in data:
      # update config from form
      for item in s3_option_items:
        if item in data:
          value = data[item]
        else:
          value = ''

        app_globals.set_global(item, value)
      app_globals.reset()
      h.redirect_to(controller='ckanext.s3con.s3.controller:S3Controller', action='config')

    data = {}
    for item in s3_option_items:
      data[item] = config.get(item)

    vars = {'data': data, 'errors': {}, 'form_items': s3_option_items}
    return base.render('admin/cloud_connector_config.html',
                           extra_vars = vars)

