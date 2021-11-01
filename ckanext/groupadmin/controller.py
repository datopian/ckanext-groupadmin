from ckan import model
from ckan.lib import helpers
from ckan.plugins import toolkit



def manage():
    context = {'model': model, 'session': model.Session,
                'user': toolkit.c.user or toolkit.c.author}
    try:
        toolkit.check_access('sysadmin', context, {})
    except toolkit.NotAuthorized:
        toolkit.abort(401, toolkit._('User not authorized to view page'))

    controller = 'group_controller'
    username = toolkit.request.params.get('username')
    if toolkit.request.method == 'POST' and username:
        try:
            toolkit.get_action('group_admin_create')(
                data_dict={'username': username}
            )
        except toolkit.NotAuthorized:
            toolkit.abort(401,
                            toolkit._('Unauthorized to perform that action'))
        except toolkit.ObjectNotFound:
            helpers.flash_error(
                toolkit._("User '{0}' not found.").format(username))
        except toolkit.ValidationError as e:
            helpers.flash_notice(e.error_summary)
        else:
            helpers.flash_success(
                toolkit._('The user is now a Group Admin'))

        return toolkit.redirect_to(toolkit.url_for(controller=controller,
                                                    action='manage'))

    group_admin_list = toolkit.get_action('group_admin_list')()
    return toolkit.render(
        'admin/manage_group_admin.html',
        extra_vars={
            'group_admin_list': group_admin_list,
        }
    )

def remove():
    context = {'model': model, 'session': model.Session,
                'user': toolkit.c.user or toolkit.c.author}

    controller = 'group_controller'
    try:
        toolkit.check_access('sysadmin', context, {})
    except toolkit.NotAuthorized:
        toolkit.abort(401,
                        toolkit._('User not authorized to view page'))

    if 'cancel' in toolkit.request.params:
        toolkit.redirect_to(controller=controller, action='manage')

    user_id = toolkit.request.params['user']
    if toolkit.request.method == 'POST' and user_id:
        try:
            toolkit.get_action('group_admin_delete')(
                data_dict={'username': user_id})
        except toolkit.NotAuthorized:
            toolkit.abort(401,
                            toolkit._('Unauthorized to perform that action'))
        except toolkit.ObjectNotFound:
            helpers.flash_error(
                toolkit._('The user is not a Group Admin'))
        else:
            helpers.flash_success(
                toolkit._('The user is no longer a Group Admin'))

        return toolkit.redirect_to(
            helpers.url_for(controller=controller, action='manage'))

    user_dict = toolkit.get_action('user_show')(data_dict={'id': user_id})
    return toolkit.render(
        'admin/confirm_remove_group_admin.html',
        extra_vars={
            'user_dict': user_dict,
        }
    )
