from ckan.plugins import toolkit


not_missing = toolkit.get_validator('not_missing')
user_exists = toolkit.get_validator('user_id_or_name_exists')


def group_admin_schema():
    return {
        'username': [not_missing, unicode, user_exists],
    }
