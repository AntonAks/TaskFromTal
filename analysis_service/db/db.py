from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from settings import settings

main_engine = create_engine(settings.MAIN_DATABASE_URL, echo=True)
main_db_session = sessionmaker(autocommit=False, autoflush=False, bind=main_engine)

analysis_engine = create_engine(settings.ANALYSIS_DATABASE_URL, echo=True)
analysis_engine_session = sessionmaker(autocommit=False, autoflush=False, bind=analysis_engine)

Base = declarative_base()


def get_main_db():
    db = main_db_session()
    try:
        yield db
    finally:
        db.close()


def get_analysis_db():
    db = analysis_engine_session()
    try:
        yield db
    finally:
        db.close()
