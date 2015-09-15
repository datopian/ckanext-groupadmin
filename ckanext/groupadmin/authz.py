'''This module monkey patches functions in ckan/authz.py and replaces the
default roles with custom roles and decorates
has_user_permission_for_group_org_org to allow a GroupAdmin to admin groups.
GroupAdmins can manage all organizations/groups, but have no other sysadmin
powers.
'''
from ckan import authz, model
from ckan.plugins import toolkit
from ckanext.groupadmin.model import GroupAdmin

authz.ROLE_PERMISSIONS.update({'group_admin': ['read', 'manage_group']})


def _trans_role_group_admin():
    return toolkit._('Group Admin')

authz._trans_role_group_admin = _trans_role_group_admin


def is_group_admin_decorator(method):
    def decorate_has_user_permission_for_group_or_org(group_id, user_name,
                                                      permission):
        user_id = authz.get_user_id_for_username(user_name, allow_none=True)
        if not user_id:
            return False
        if GroupAdmin.is_user_group_admin(model.Session, user_id):
            return True
        return method(group_id, user_name, permission)
    return decorate_has_user_permission_for_group_or_org


authz.has_user_permission_for_group_or_org = is_group_admin_decorator(
    authz.has_user_permission_for_group_or_org)
