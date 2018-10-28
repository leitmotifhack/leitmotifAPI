from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
import secrets

engine = create_engine(
    "postgres://"
    + secrets.postgresqlusername
    + ":"
    + secrets.postgresqlpassword
    + "@"
    + secrets.dbhost
    + "/"
    + secrets.dbname,
    convert_unicode=True,
)
metadata = MetaData()
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


def init_db():
    metadata.create_all(bind=engine)
