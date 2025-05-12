import pytest
import uuid
from datetime import datetime
from fastapi import status

from api.db.models import Study


@pytest.mark.usefixtures("db")
@pytest.mark.usefixtures("clean_tables")
class TestStudyEndpoints:
    def test_create_study(self, client):
        study_data = {
            "title": "Test Study",
            "organization_name": "Test Organization",
            "organization_type": "Academic",
        }
        response = client.post("/api/studies/", json=study_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == study_data["title"]
        assert data["organization_name"] == study_data["organization_name"]
        assert data["organization_type"] == study_data["organization_type"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_get_studies_empty(self, client):
        response = client.get("/api/studies/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_studies(self, client, db):
        """Test getting a list of studies."""
        # Create two test studies
        study1 = Study(
            id=str(uuid.uuid4()),
            title="Study 1",
            organization_name="Org 1",
            organization_type="Academic",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        study2 = Study(
            id=str(uuid.uuid4()),
            title="Study 2",
            organization_name="Org 2",
            organization_type="Commercial",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        db.add(study1)
        db.add(study2)
        db.commit()

        # Test getting the list
        response = client.get("/api/studies/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        # Check that both studies are in the list
        titles = [study["title"] for study in data]
        assert "Study 1" in titles
        assert "Study 2" in titles

    def test_get_study_by_id(self, client, db):
        """Test getting a specific study by ID."""
        # Create a test study
        study_id = str(uuid.uuid4())
        study = Study(
            id=study_id,
            title="Test Study",
            organization_name="Test Org",
            organization_type="Academic",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        db.add(study)
        db.commit()

        # Test getting by ID
        response = client.get(f"/api/studies/{study_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == study_id
        assert data["title"] == "Test Study"
        assert data["organization_name"] == "Test Org"
        assert data["organization_type"] == "Academic"

    def test_get_nonexistent_study(self, client):
        """Test getting a non-existent study."""
        non_existent_id = str(uuid.uuid4())

        response = client.get(f"/api/studies/{non_existent_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Study not found"

    def test_update_study(self, client, db):
        """Test updating a study."""
        # Create a test study
        study_id = str(uuid.uuid4())
        study = Study(
            id=study_id,
            title="Original Title",
            organization_name="Original Org",
            organization_type="Academic",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        db.add(study)
        db.commit()

        # Data for update
        update_data = {"title": "Updated Title", "organization_name": "Updated Org"}

        # Test update
        response = client.put(f"/api/studies/{study_id}", json=update_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["organization_name"] == "Updated Org"
        # organization_type doesn't change since it wasn't included in the request
        assert data["organization_type"] == "Academic"

    def test_update_nonexistent_study(self, client):
        """Test updating a non-existent study."""
        non_existent_id = str(uuid.uuid4())
        update_data = {"title": "Updated Title"}

        response = client.put(f"/api/studies/{non_existent_id}", json=update_data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Study not found"

    def test_delete_study(self, client, db):
        """Test deleting a study."""
        # Create a test study
        study_id = str(uuid.uuid4())
        study = Study(
            id=study_id,
            title="Study to Delete",
            organization_name="Delete Org",
            organization_type="Academic",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        db.add(study)
        db.commit()

        # Test deletion
        response = client.delete(f"/api/studies/{study_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Check that the study is actually deleted
        deleted_study = db.query(Study).filter(Study.id == study_id).first()
        assert deleted_study is None

    def test_delete_nonexistent_study(self, client):
        """Test deleting a non-existent study."""
        non_existent_id = str(uuid.uuid4())

        response = client.delete(f"/api/studies/{non_existent_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Study not found"

    def test_filter_studies_by_title(self, client, db):
        """Test filtering studies by title."""
        # Create test studies with different titles
        study1 = Study(
            id=str(uuid.uuid4()),
            title="Machine Learning Study",
            organization_name="Org 1",
            organization_type="Academic",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        study2 = Study(
            id=str(uuid.uuid4()),
            title="Data Science Research",
            organization_name="Org 2",
            organization_type="Commercial",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        db.add(study1)
        db.add(study2)
        db.commit()

        # Test filtering by title
        response = client.get("/api/studies/", params={"title": "Machine"})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Machine Learning Study"

        # Test filtering by part of title (case insensitivity)
        response = client.get("/api/studies/", params={"title": "research"})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Data Science Research"

    def test_filter_studies_by_organization_name(self, client, db):
        """Test filtering studies by organization name."""
        # Create test studies with different organizations
        study1 = Study(
            id=str(uuid.uuid4()),
            title="Study 1",
            organization_name="University of Science",
            organization_type="Academic",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        study2 = Study(
            id=str(uuid.uuid4()),
            title="Study 2",
            organization_name="Tech Company",
            organization_type="Commercial",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        db.add(study1)
        db.add(study2)
        db.commit()

        # Test filtering by organization name
        response = client.get(
            "/api/studies/", params={"organization_name": "University"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["organization_name"] == "University of Science"

    def test_pagination(self, client, db):
        """Test pagination of studies list."""
        # Create 5 test studies
        for i in range(5):
            study = Study(
                id=str(uuid.uuid4()),
                title=f"Study {i + 1}",
                organization_name=f"Org {i + 1}",
                organization_type="Academic",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            db.add(study)
        db.commit()

        # Test first page with limit of 2 records
        response = client.get("/api/studies/", params={"skip": 0, "limit": 2})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2

        # Test second page with limit of 2 records
        response = client.get("/api/studies/", params={"skip": 2, "limit": 2})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2

        # Test third page with limit of 2 records
        response = client.get("/api/studies/", params={"skip": 4, "limit": 2})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1  # Only one record on the last page
