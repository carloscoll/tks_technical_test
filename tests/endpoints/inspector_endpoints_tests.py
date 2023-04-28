import unittest
from fastapi.testclient import TestClient
import app
from app.core.db.session import Session
from app.services.inspector_service import InspectorService
from app.core.schemas import inspector_schemas
import requests
from requests.structures import CaseInsensitiveDict


class TestEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.db = Session()

    def tearDown(self):
        self.db.close()

    def test_get_inspector(self):
        inspector_id = '0bdaa72b-fa28-443f-870a-8c69a8242bab'
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        response = requests.get(f"http://localhost/inspector_id={inspector_id}", headers=headers)
        self.assertEqual(response.status_code, 200)
        inspector = inspector_schemas.Inspector(**response.json())
        self.assertEqual(inspector.id, inspector_id)

    def test_get_all_inspectors(self):
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        response = requests.get("http://localhost/all/", headers=headers)
        self.assertEqual(response.status_code, 200)
        inspectors = [inspector_schemas.Inspector(**data) for data in response.json()]
        self.assertGreater(len(inspectors), 0)

    def test_create_inspector(self):
        inspector_data = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "location": "Madrid"
        }
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        response = requests.post("http://localhost/", headers=headers, json=inspector_data)
        self.assertEqual(response.status_code, 200)
        inspector = inspector_schemas.Inspector(**response.json())
        self.assertIsNotNone(inspector.id)

    def test_update_inspector(self):
        inspector_id = '0bdaa72b-fa28-443f-870a-8c69a8242bab'
        inspector_data = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "location": "Madrid"
        }
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        response = requests.put(f"http://localhost/inspector_id={inspector_id}", headers=headers, json=inspector_data)
        self.assertEqual(response.status_code, 200)
        inspector = inspector_schemas.Inspector(**response.json())
        self.assertEqual(inspector.name, inspector_data['name'])

    def test_delete_inspector(self):
        inspector_id = '0bdaa72b-fa28-443f-870a-8c69a8242bab'
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        response = requests.delete(f"http://localhost/inspector_id={inspector_id}", headers=headers)
        self.assertEqual(response.status_code, 200)
        # Verify that the inspector has been deleted
        service = InspectorService(self.db)
        inspector = service.get_inspector(inspector_id)
        self.assertIsNone(inspector)
