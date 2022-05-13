# piccolo_conf.py
from piccolo.engine.postgres import PostgresEngine


DB = PostgresEngine(config={
    'host': 'localhost',
    'database': 'my_app',
    'user': 'postgres',
    'password': 'pwdPostgreSQL'
})
