import configparser
import pathlib
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()  #экземпляр конфига
config.read(file_config)  #файл инициализации

username = config.get('DB_DEV', 'user')
password = config.get('DB_DEV', 'password')
db_name = config.get('DB_DEV', 'db_name')
host = config.get('DB_DEV', 'host')
port = config.get('DB_DEV', 'port')

url_to_db = f'postgresql://{username}:{password}@{host}:{port}/{db_name}'

engine = create_engine(url_to_db, echo=True, pool_size=5)
Session = sessionmaker(bind=engine)
session = Session()