import ckan.model as model
import ckan.logic.action.create as origin
import ckanext.s3con.s3.uploader as uploader

from ckan.logic import (
    NotFound,
    ValidationError,
    get_or_bust as _get_or_bust,
    check_access as _check_access,
    get_action as _get_action,
)

import logging
log = logging.getLogger(__name__)

__all__ = ['resource_create']

def resource_create(context, data_dict):
    if False:
        return origin.resource_create(context, data_dict)
    
    model = context['model']
    user = context['user']

    package_id = _get_or_bust(data_dict, 'package_id')
    data_dict.pop('package_id')

    pkg_dict = _get_action('package_show')(context, {'id': package_id})

    _check_access('resource_create', context, data_dict)

    if not 'resources' in pkg_dict:
        pkg_dict['resources'] = []

    upload = uploader.S3Upload(data_dict)

    pkg_dict['resources'].append(data_dict)

    try:
        context['defer_commit'] = True
        context['use_cache'] = False
        _get_action('package_update')(context, pkg_dict)
        context.pop('defer_commit')
    except ValidationError, e:
        errors = e.error_dict['resources'][-1]
        raise ValidationError(errors)

    ## Get out resource_id resource from model as it will not appear in
    ## package_show until after commit
    upload.upload(context['package'].resources[-1].id,
                  uploader.get_max_resource_size())
    model.repo.commit()

    ##  Run package show again to get out actual last_resource
    pkg_dict = _get_action('package_show')(context, {'id': package_id})
    resource = pkg_dict['resources'][-1]

    return resource

resource_create.__doc__ = origin.resource_create.__doc__