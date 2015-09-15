import logging
from ckan.model.domain_object import DomainObject
from ckan.model import meta
from ckan import model
from sqlalchemy import Column, ForeignKey, Table, types

log = logging.getLogger(__name__)

group_admin_table = None


def setup():
    if group_admin_table is None:
        define_group_admin_table()
        log.debug('GroupAdmin table defined in memory')

    if model.user_table.exists():
        if not group_admin_table.exists():
            group_admin_table.create()
            log.debug('GroupAdmin table create')
        else:
            log.debug('GroupAdmin table already exists')
    else:
        log.debug('GroupAdmin table creation deferred')


class GroupBaseModel(DomainObject):
    @classmethod
    def filter(cls, session, **kwargs):
        return session.query(cls).filter_by(**kwargs)

    @classmethod
    def exists(cls, session, **kwargs):
        if cls.filter(session, **kwargs).first():
            return True
        else:
            return False

    @classmethod
    def get(cls, session, **kwargs):
        instance = cls.filter(session, **kwargs).first()
        return instance

    @classmethod
    def create(cls, session, **kwargs):
        instance = cls(**kwargs)
        session.add(instance)
        session.commit()
        return instance.as_dict()


class GroupAdmin(GroupBaseModel):
    @classmethod
    def get_group_admin_ids(cls, session):
        return [i for (i, ) in session.query(cls.user_id).all()]

    @classmethod
    def is_user_group_admin(cls, session, user):
        if cls.get(session, user_id=user):
            return True
        else:
            return False


def define_group_admin_table():
    global group_admin_table

    group_admin_table = Table(
        'group_admin',
        meta.metadata,
        Column('user_id',
               types.UnicodeText,
               ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'),
               primary_key=True, nullable=False)
    )

    meta.mapper(GroupAdmin, group_admin_table)
