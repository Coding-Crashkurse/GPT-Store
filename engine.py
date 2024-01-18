from sqlalchemy import create_engine

CONNECTION_STRING = "postgresql+psycopg2://myuser:mypw@127.0.0.1:5432/mydb"
engine = create_engine(CONNECTION_STRING)
