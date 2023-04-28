import unittest
from app.core.schemas import inspector_schemas as schemas
from app.services.inspector_service import InspectorService
from app.core.models.models import Inspector
from sqlalchemy.orm import Session
from unittest.mock import Mock


class TestInspectorService(unittest.TestCase):
    def setUp(self):
        self.db_mock = Mock(Session)
        self.service = InspectorService(db=self.db_mock)

    def test_create_inspector(self):
        # Arrange
        inspector_create = schemas.InspectorCreate(name='John Doe', email='john.doe@example.com', timezone='Madrid')

        # Act
        result = self.service.create_inspector(inspector_create)

        # Asserts
        self.assertIsInstance(result, Inspector)
        self.assertEqual(result.name, inspector_create.name)
        self.assertEqual(result.email, inspector_create.email)

        self.db_mock.add.assert_called_once_with(result)
        self.db_mock.commit.assert_called_once()
        self.db_mock.refresh.assert_called_once_with(result)

    def test_create_inspector_exception(self):
        # Arrange
        inspector_create = schemas.InspectorCreate(name='John Doe', email='john.doe@example.com', timezone='Madrid')

        # Act
        result = self.service.create_inspector(inspector_create)

        # Assert
        self.assertIsInstance(result, Inspector)
        self.assertEqual(result.name, inspector_create.name)
        self.assertEqual(result.email, inspector_create.email)

        self.db_mock.add.assert_called_once_with(result)
        self.db_mock.commit.assert_called_once()
        self.db_mock.refresh.assert_called_once_with(result)

    def test_get_inspector(self):
        # Arrange
        inspector_id = '123e4567-e89b-12d3-a456-426614174000'
        inspector = Inspector(id=inspector_id, name='John Doe', email='john.doe@example.com')
        self.db_mock.query().filter().first.return_value = inspector

        # Act
        result = self.service.get_inspector(inspector_id)

        # Assert
        self.assertIsInstance(result, Inspector)
        self.assertEqual(result.id, inspector_id)
        self.assertEqual(result.name, inspector.name)
        self.assertEqual(result.email, inspector.email)

    def test_get_inspectors(self):
        # Arrange
        inspectors = [Inspector(name='John Doe', email='john.doe@example.com') for _ in range(3)]
        self.db_mock.query().all.return_value = inspectors

        # Act
        result = self.service.get_inspectors()

        # Assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(inspectors))

    def test_update_inspector(self):
        # Arrange
        inspector_id = '123e4567-e89b-12d3-a456-426614174000'
        inspector_update = schemas.InspectorUpdate(name='Jane Doe', email='john.doe@example.com', timezone='Mexico city')
        inspector = Inspector(id=inspector_id, name='John Doe', email='john.doe@example.com', timezone='Madrid')
        self.db_mock.query().filter().first.return_value = inspector

        # Act
        result = self.service.update_inspector(inspector_id, inspector_update)

        # Assert
        self.assertIsInstance(result, Inspector)
        self.assertEqual(result.id, inspector_id)
        self.assertEqual(result.name, inspector_update.name)
        self.assertEqual(result.email, inspector.email)

        self.db_mock.commit.assert_called_once()
        self.db_mock.refresh.assert_called_once_with(result)

    def test_delete_inspector(self):
        # Arrange
        inspector_id = '123e4567-e89b-12d3-a456-426614174000'
        inspector = Inspector(id=inspector_id, name='John Doe', email='john.doe@example.com')
        self.db_mock.query().filter().first.return_value = inspector

        # Act
        self.service.delete_inspector(inspector_id)

        # Assert
        self.db_mock.delete.assert_called_once_with(inspector)
        self.db_mock.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
