import ckan.plugins.toolkit as toolkit
import ckan.lib.base as base
import ckan.lib.helpers as h
import datetime, os, re, json

from pylons import config
from ckan.common import c, g, _, OrderedDict, request

import ckan.model as model
session = model.Session

import logging
log = logging.getLogger(__name__)



class S3Controller(base.BaseController):
  def config(self):
    pass