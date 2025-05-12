import pytest
import os
import logging
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, DateTime

from api.main import app
from api.db.db import Base, get_db
from api.db.models import Study

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up test database
TEST_DB_DIR = "test_db"
os.makedirs(TEST_DB_DIR, exist_ok=True)
TEST_DB_PATH = os.path.join(TEST_DB_DIR, "test.db")

# Remove existing database file if it exists
if os.path.exists(TEST_DB_PATH):
    logger.info(f"Removing existing test database: {TEST_DB_PATH}")
    os.remove(TEST_DB_PATH)

# Prepare SQLite file URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"
logger.info(f"Using test database at: {TEST_DB_PATH}")

# Create SQLAlchemy test engine
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)

# Create test sessions
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# Function to get test database session
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to check if tables exist
def check_tables():
    inspector = inspect(test_engine)
    tables = inspector.get_table_names()
    logger.info(f"Tables in database: {tables}")
    return "studies" in tables


# Fixture to initialize the database before all tests
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    logger.info("Setting up test database...")
    Base.metadata.create_all(bind=test_engine)

    if not check_tables():
        logger.error("Tables were not created properly!")

        TempBase = declarative_base()

        class TempStudy(TempBase):
            __tablename__ = "studies"

            id = Column(String, primary_key=True)
            title = Column(String, nullable=False)
            organization_name = Column(String, nullable=False)
            organization_type = Column(String, nullable=False)
            created_at = Column(DateTime, nullable=False)
            updated_at = Column(DateTime, nullable=False)

        TempBase.metadata.create_all(bind=test_engine)

        if not check_tables():
            logger.error("Failed to create tables even with explicit definition!")
        else:
            logger.info("Tables created with explicit definition.")
    else:
        logger.info("Tables created successfully.")

    yield

    # Check tables before teardown
    logger.info("Checking tables before teardown...")
    check_tables()


# Fixture to clean tables between tests
@pytest.fixture(scope="function")
def clean_tables():
    yield
    # Clean tables after each test
    db = TestingSessionLocal()
    try:
        logger.info("Cleaning tables after test...")
        if check_tables():
            db.query(Study).delete()
            db.commit()
        else:
            logger.error("Cannot clean tables - they don't exist!")
    finally:
        db.close()


# Fixture to override get_db dependency
@pytest.fixture(scope="function")
def app_with_test_db():
    # Save original dependencies
    original_dependencies = app.dependency_overrides.copy()

    # Set up test DB
    logger.info("Setting test database dependency override...")
    app.dependency_overrides[get_db] = override_get_db

    yield app

    # Restore original dependencies
    app.dependency_overrides = original_dependencies


# Fixture for test client
@pytest.fixture(scope="function")
def client(app_with_test_db):
    logger.info("Creating test client...")
    with TestClient(app_with_test_db) as test_client:
        yield test_client


# Fixture for database session
@pytest.fixture(scope="function")
def db():
    logger.info("Creating database session...")
    db = TestingSessionLocal()
    try:
        check_tables()
        yield db
    finally:
        db.close()
