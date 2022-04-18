import sqlalchemy
from .db_session import SqlAlchemyBase


class QuickSaves(SqlAlchemyBase):
    __tablename__ = 'quick_saves'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    image = sqlalchemy.Column(sqlalchemy.String)
    address = sqlalchemy.Column(sqlalchemy.String)
    title = sqlalchemy.Column(sqlalchemy.String)
