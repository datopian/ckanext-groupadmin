from ckan import model
from ckan.logic import validate
from ckan.plugins import toolkit
from ckanext.groupadmin.logic import schema
from ckanext.groupadmin.model import GroupAdmin


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
