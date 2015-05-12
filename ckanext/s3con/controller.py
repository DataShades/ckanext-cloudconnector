import ckan.plugins as plugins
get_action = plugins.toolkit.get_action

import ckan.model as model
from ckan.common import c, request, response

from ckan.lib.base import abort, redirect
import paste.fileapp

import ckanext.s3con.s3_uploader as uploader

import logging
log = logging.getLogger(__name__)


class S3Controller(plugins.toolkit.BaseController):
  def file_upload(self):
    """
    Provides a direct download by either redirecting the user to the url stored
     or downloading an uploaded file directly.
    """
    log.warn('AAAAAAAAAACCCKKKKKKKBBBBBBBBBBBBBAAAAAAAAAAAAAAAAARRRRRRRRRRRRRRRR!!!!!!!!!')
    context = {'model': model, 'session': model.Session,
               'user': c.user or c.author, 'auth_user_obj': c.userobj}

    try:
        rsc = get_action('resource_show')(context, {'id': resource_id})
        pkg = get_action('package_show')(context, {'id': id})
    except NotFound:
        abort(404, _('Resource not found'))
    except NotAuthorized:
        abort(401, _('Unauthorized to read resource %s') % id)

    if rsc.get('url_type') == 'upload':
        upload = uploader.ResourceUpload(rsc)
        filepath = upload.get_path(rsc['id'])
        fileapp = paste.fileapp.FileApp(filepath)
        try:
           status, headers, app_iter = request.call_application(fileapp)
        except OSError:
           abort(404, _('Resource data not found'))
        response.headers.update(dict(headers))
        content_type, content_enc = mimetypes.guess_type(rsc.get('url',''))
        if content_type:
            response.headers['Content-Type'] = content_type
        response.status = status
        return app_iter
    elif not 'url' in rsc:
        abort(404, _('No download is available'))
    redirect(rsc['url'])
