import ckan.model as model
import ckan.logic.action.update as origin
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

__all__ = ['resource_update']

def resource_update(context, data_dict):
    if False:
        return origin.resource_update(context, data_dict)

    model = context['model']
    user = context['user']
    id = _get_or_bust(data_dict, "id")

    resource = model.Resource.get(id)
    context["resource"] = resource

    if not resource:
        log.error('Could not find resource ' + id)
        raise NotFound(_('Resource was not found.'))

    _check_access('resource_update', context, data_dict)
    del context["resource"]

    package_id = resource.resource_group.package.id
    pkg_dict = _get_action('package_show')(context, {'id': package_id})

    for n, p in enumerate(pkg_dict['resources']):
        if p['id'] == id:
            break
    else:
        log.error('Could not find resource ' + id)
        raise NotFound(_('Resource was not found.'))

    upload = uploader.S3Upload(data_dict)

    pkg_dict['resources'][n] = data_dict

    try:
        context['defer_commit'] = True
        context['use_cache'] = False
        pkg_dict = _get_action('package_update')(context, pkg_dict)
        context.pop('defer_commit')
    except ValidationError, e:
        errors = e.error_dict['resources'][n]
        raise ValidationError(errors)

    upload.upload(id, uploader.get_max_resource_size())
    model.repo.commit()
    return _get_action('resource_show')(context, {'id': id})


resource_update.__doc__ = origin.resource_update.__doc__
