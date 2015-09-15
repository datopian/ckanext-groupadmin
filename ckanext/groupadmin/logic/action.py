from ckan import model
from ckan.logic import validate
from ckan.plugins import toolkit
from ckan.logic.action.get import \
    group_list_authz as core_group_list_authz
import ckan.authz as authz
import ckan.lib.dictization.model_dictize as model_dictize

from ckanext.groupadmin.logic import schema
from ckanext.groupadmin.model import GroupAdmin

import logging
log = logging.getLogger(__name__)


@validate(schema.group_admin_schema)
def group_admin_create(context, data_dict):
    toolkit.check_access('group_admin_create', context, data_dict)
    session = context['session']
    username = data_dict['username']
    user_object = model.User.get(username)
    if GroupAdmin.exists(session, user_id=user_object.id):
        raise toolkit.ValidationError(
            'user {0} is already a Group admin'.format(username)
        )
    return GroupAdmin.create(session, user_id=user_object.id)


@validate(schema.group_admin_schema)
def group_admin_delete(context, data_dict):
    toolkit.check_access('group_admin_delete', context, data_dict)
    session = context['session']
    username = data_dict['username']
    user_object = model.User.get(username)
    admin = GroupAdmin.get(session, user_id=user_object.id)
    if admin:
        session.delete(admin)
        session.commit()
    else:
        raise toolkit.ValidationError(
            'user {0} is not a Group admin'.format(username)
        )


def group_admin_list(context, data_dict):
    toolkit.check_access('group_admin_list', context, data_dict)
    session = context['session']
    user_ids = GroupAdmin.get_group_admin_ids(session)
    return [toolkit.get_action('user_show')(data_dict={'id': user_id})
            for user_id in user_ids]


def group_list_authz(context, data_dict):
    '''Return the list of groups that the user is authorized to edit. Replaces
    the core authz method of the same name.'''

    user = context['user']
    model = context['model']

    user_id = authz.get_user_id_for_username(user, allow_none=True)

    if GroupAdmin.is_user_group_admin(model.Session, user_id):
        q = model.Session.query(model.Group) \
            .filter(model.Group.is_organization == False) \
            .filter(model.Group.state == 'active')

        groups = q.all()

        group_list = model_dictize.group_list_dictize(groups, context)
        return group_list
    else:
        # defer to core method
        return core_group_list_authz(context, data_dict)
