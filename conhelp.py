import sqlalchemy

# Hier den Connection-String direkt festlegen
connection_string = "postgresql+psycopg2://scott:tiger@localhost/test"

try:
    engine = sqlalchemy.create_engine(connection_string)
    connection = engine.connect()

    print("Connection String is valid.")
    connection.close()
except Exception as e:
    print(f"Invalid Connection String: {e}")
