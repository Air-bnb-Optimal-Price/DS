from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from decouple import config
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.sqlite3', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'users'
    host_id = Column(BigInteger, primary_key=True)
    list_id = Column(BigInteger, nullable=False)

    def __init__(self, host_id=None, list_id=None):
        self.host_id = host_id
        self.list_id = list_id

    def __repr__(self):
        return f'<User {self.host_id}>'


def add_user(host_id, list_id):
    try:
        db_user = User(host_id=host_id, list_id=list_id)
        db_session.add(db_user)
    except Exception as e:
        print(f'Error Processing {e}')
        raise e
    else:
        db_session.commit()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)


Base.metadata.create_all(engine)
