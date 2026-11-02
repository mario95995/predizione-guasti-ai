from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#creazione del file locale
SQLALCHEMY_DATABASE_URL = "sqlite:///./manutenzione.db"

#creazione dell'engine per le comunicazioni 
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread" : False})

#creazione della fabbrica di sessioni per le query al db
SessionLocal= sessionmaker(autocommit = False, autoflush= False, bind=engine)

#creazione della classe base dove vengono ereditati i modelli 
base = declarative_base()

#funzione per ottenere una sessione col database 
def get_db() : 
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()