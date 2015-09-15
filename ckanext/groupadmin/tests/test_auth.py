from nose import tools as nosetools

import ckan.plugins.toolkit as toolkit
import ckan.tests.factories as factories
import ckan.tests.helpers as helpers


class TestGroupAdminCreateAuth(helpers.FunctionalTestBase):

    def test_group_admin_create_no_user(self):
        '''
        Calling group admin create with no user raises NotAuthorized.
        '''

        context = {'user': None, 'model': None}
        nosetools.assert_raises(toolkit.NotAuthorized, helpers.call_auth,
                                'group_admin_create', context=context)

    def test_group_admin_create_correct_creds(self):
        '''
        Calling group admin create by a sysadmin doesn't raise NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        context = {'user': a_sysadmin['name'], 'model': None}
        helpers.call_auth('group_admin_create', context=context)

    def test_group_admin_create_unauthorized_creds(self):
        '''
        Calling group admin create with unauthorized user raises
        NotAuthorized.
        '''
        not_a_sysadmin = factories.User()
        context = {'user': not_a_sysadmin['name'], 'model': None}
        nosetools.assert_raises(toolkit.NotAuthorized, helpers.call_auth,
                                'group_admin_create', context=context)


class TestGroupAdminRemoveAuth(helpers.FunctionalTestBase):

    def test_group_admin_delete_no_user(self):
        '''
        Calling group admin delete with no user raises NotAuthorized.
        '''

        context = {'user': None, 'model': None}
        nosetools.assert_raises(toolkit.NotAuthorized, helpers.call_auth,
                                'group_admin_delete',
                                context=context)

    def test_group_admin_delete_correct_creds(self):
        '''
        Calling group admin delete by a sysadmin doesn't raise NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        context = {'user': a_sysadmin['name'], 'model': None}
        helpers.call_auth('group_admin_delete', context=context)

    def test_group_admin_delete_unauthorized_creds(self):
        '''
        Calling group admin delete with unauthorized user raises
        NotAuthorized.
        '''
        not_a_sysadmin = factories.User()
        context = {'user': not_a_sysadmin['name'], 'model': None}
        nosetools.assert_raises(toolkit.NotAuthorized, helpers.call_auth,
                                'group_admin_delete',
                                context=context)


class TestGroupAdminListAuth(helpers.FunctionalTestBase):

    def test_group_admin_list_no_user(self):
        '''
        Calling group admin list with no user raises NotAuthorized.
        '''

        context = {'user': None, 'model': None}
        nosetools.assert_raises(toolkit.NotAuthorized, helpers.call_auth,
                                'group_admin_list', context=context)

    def test_group_admin_list_correct_creds(self):
        '''
        Calling group admin list by a sysadmin doesn't raise
        NotAuthorized.
        '''
        a_sysadmin = factories.Sysadmin()
        context = {'user': a_sysadmin['name'], 'model': None}
        helpers.call_auth('group_admin_list', context=context)

    def test_group_admin_list_unauthorized_creds(self):
        '''
        Calling group admin list with unauthorized user raises
        NotAuthorized.
        '''
        not_a_sysadmin = factories.User()
        context = {'user': not_a_sysadmin['name'], 'model': None}
        nosetools.assert_raises(toolkit.NotAuthorized, helpers.call_auth,
                                'group_admin_list', context=context)


class TestGroupAdminViewGroupManagePage(helpers.FunctionalTestBase):

    def test_auth_anon_user_cant_view_group_manage_page(self):
        '''
        An anon (not logged in) user can't access the manage group page.
        '''
        factories.Group(name='my-group')

        app = self._get_test_app()
        app.get("/group/edit/my-group", status=302)

    def test_auth_logged_in_user_cant_view_group_manage_page(self):
        '''
        A logged in user can't access the manage group page.
        '''
        factories.Group(name='my-group')

        app = self._get_test_app()
        user = factories.User()
        app.get("/group/edit/my-group", status=401,
                extra_environ={'REMOTE_USER': str(user['name'])})

    def test_auth_sysadmin_can_view_group_manage_page(self):
        '''
        A sysadmin can access the manage group page.
        '''
        factories.Group(name='my-group')

        app = self._get_test_app()
        user = factories.Sysadmin()
        app.get("/group/edit/my-group", status=200,
                extra_environ={'REMOTE_USER': str(user['name'])})

    def test_auth_group_admin_can_view_group_manage_page(self):
        '''
        A group admin can access the manage group page.
        '''
        factories.Group(name='my-group')

        app = self._get_test_app()
        user_to_add = factories.User()

        app.get("/group/edit/my-group", status=401,
                extra_environ={'REMOTE_USER': str(user_to_add['name'])})

        helpers.call_action('group_admin_create', context={},
                            username=user_to_add['name'])

        app.get("/group/edit/my-group", status=200,
                extra_environ={'REMOTE_USER': str(user_to_add['name'])})


class TestGroupAuthManageGroupAdmins(helpers.FunctionalTestBase):

    def test_auth_anon_user_cant_view_group_admin_manage_page(self):
        '''
        An anon (not logged in) user can't access the manage group admin
        page.
        '''
        factories.Group(name='my-group')

        app = self._get_test_app()
        app.get("/ckan-admin/group_admins", status=302)

    def test_auth_logged_in_user_cant_view_group_admin_manage_page(self):
        '''
        A logged in user can't access the manage group admin page.
        '''
        factories.Group(name='my-group')

        app = self._get_test_app()
        user = factories.User()
        app.get("/ckan-admin/group_admins", status=401,
                extra_environ={'REMOTE_USER': str(user['name'])})

    def test_auth_sysadmin_can_view_group_admin_manage_page(self):
        '''
        A sysadmin can access the manage group admin page.
        '''
        factories.Group(name='my-group')

        app = self._get_test_app()
        user = factories.Sysadmin()
        app.get("/ckan-admin/group_admins", status=200,
                extra_environ={'REMOTE_USER': str(user['name'])})

    def test_auth_logged_in_group_admin_cant_view_group_admin_manage_page(self):
        '''
        A logged in group admin can't access the manage group admin page.
        '''
        factories.Group(name='my-group')

        app = self._get_test_app()
        user = factories.User()

        helpers.call_action('group_admin_create', context={},
                            username=user['name'])

        app.get("/ckan-admin/group_admins", status=401,
                extra_environ={'REMOTE_USER': str(user['name'])})
