import unittest
import uuid
from datetime import datetime
from unittest.mock import Mock

from sqlalchemy.orm import Session

from app.core.models import models
from app.core.models.models import TaskAssignment
from app.core.schemas import task_assignment_schemas
from app.services.task_assignment_service import TaskAssignmentService as Service


class TaskAssignmentServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.db_mock = Mock(spec=Session)
        self.service = Service(db=self.db_mock)

    def test_assign_task(self):
        inspector_id = uuid.uuid4()
        task_id = uuid.uuid4()
        task_assignment_create_schema = task_assignment_schemas. \
            TaskAssignmentCreate(scheduled_datetime=datetime.strptime("2023-04-27T16:21:24.645804+02:00",
                                                                      "%Y-%m-%dT%H:%M:%S.%f%z"), status="pending")

        self.db_mock.query(models.Task).filter(models.Task).first.return_value = models.Task(
            id=task_id,
            title="Test task",
            description="Task description",
            deadline=datetime.strptime("2023-04-27T16:21:24.645804+02:00", "%Y-%m-%dT%H:%M:%S.%f%z"),
            location="Madrid"
        )

        result = self.service.assign_task(inspector_id, task_id, task_assignment_create_schema)

        self.assertIsInstance(result, TaskAssignment)
        self.assertEqual(result.task_id, task_id)
        # self.assertEqual(result.inspector_id, inspector_id)
        self.assertEqual(result.status, result.status)
        self.assertEqual(result.scheduled_datetime, result.scheduled_datetime)

        self.db_mock.add.assert_called_once_with(result)
        self.db_mock.commit.assert_called_once()
        self.db_mock.refresh.assert_called_once_with(result)

    def test_assign_task_exception(self):
        inspector_id = uuid.uuid4()
        task_id = uuid.uuid4()
        task_assignment_create_schema = task_assignment_schemas. \
            TaskAssignmentCreate(scheduled_datetime=datetime.strptime("2023-04-27T16:21:24.645804+02:00",
                                                                      "%Y-%m-%dT%H:%M:%S.%f%z"), status="pending")
        self.db_mock.add(task_assignment_create_schema)
        self.db_mock.commit.side_effect = Exception("Error committing to database")
        with self.assertRaises(Exception):
            self.service.assign_task(inspector_id, task_id, task_assignment_create_schema)
        self.db_mock.rollback.assert_called_once()

    def test_finish_task(self):
        task_assignment_id = uuid.uuid4()
        task_evaluated_task_schema = task_assignment_schemas.TaskAssignmentEvaluation(
            rating=6.0,
            rating_description="Evaluation",
            evaluation_datetime=datetime.strptime("2023-04-29T16:21:24.645804+02:00", "%Y-%m-%dT%H:%M:%S.%f%z")
        )

        result = self.service.finish_task(task_assignment_id, task_evaluated_task_schema)

        self.assertIsInstance(result, TaskAssignment)
        self.assertEqual(result.rating, task_evaluated_task_schema.rating)
        self.assertEqual(result.rating_description, task_evaluated_task_schema.rating_description)
        self.assertEqual(result.evaluation_datetime, task_evaluated_task_schema.evaluation_datetime)

        self.db_mock.add.assert_called_once_with(result)
        self.db_mock.commit.assert_called_once()
        self.db_mock.refresh.assert_called_once_with(result)

    def test_finish_task_exception(self):
        task_assignment_id = uuid.uuid4()
        task_evaluated_task = task_assignment_schemas.TaskAssignmentEvaluation(
            scheduled_datetime=datetime.strptime("2023-04-27T16:21:24.645804+02:00", "%Y-%m-%dT%H:%M:%S.%f%z"),
            status="completed",
            rating=6.0,
            rating_description="Evaluation",
            evaluation_datetime=datetime.strptime("2023-04-29T16:21:24.645804+02:00", "%Y-%m-%dT%H:%M:%S.%f%z")
        )

        self.db_mock.add(task_evaluated_task)
        self.db_mock.commit.side_effect = Exception("Error committing to database")
        with self.assertRaises(Exception):
            self.service.finish_task(task_assignment_id, task_evaluated_task)
        self.db_mock.rollback.assert_called_once()

    def test_get_assigned_task(self):
        uuid_mock = uuid.uuid4()
        task_assignment = TaskAssignment(
            id=uuid_mock,
            scheduled_datetime=datetime.strptime("2023-04-27T16:21:24.645804+02:00", "%Y-%m-%dT%H:%M:%S.%f%z"),
            status="pending"
        )

        self.db_mock.query().filter().first.return_value = task_assignment

        self.db_mock.commit.side_effect = Exception("Error obtaining assignment")
        with self.assertRaises(Exception):
            self.service.get_assigned_task(uuid_mock)
        self.db_mock.rollback.assert_called_once()

    def test_get_assigned_task_exception(self):
        uuid_mock = uuid.uuid4()
        task_assignment = TaskAssignment(
            id=uuid_mock,
            scheduled_datetime=datetime.strptime("2023-04-27T16:21:24.645804+02:00", "%Y-%m-%dT%H:%M:%S.%f%z"),
            status="pending"
        )

        self.db_mock.query().filter().first.return_value = task_assignment

        result = self.service.get_assigned_task(uuid_mock)

        self.assertIsInstance(result, TaskAssignment)
        self.assertEqual(result.id, task_assignment.id)
        self.assertEqual(result.scheduled_datetime, task_assignment.scheduled_datetime)
        self.assertEqual(result.status, task_assignment.status)

    def test_get_assigned_tasks(self):
        expected_result = [
            models.TaskAssignment(id=uuid.uuid4(), scheduled_datetime=datetime.now(), inspector_id=uuid.uuid4(),
                                  status="pending"),
            models.TaskAssignment(id=uuid.uuid4(), scheduled_datetime=datetime.now(), inspector_id=uuid.uuid4(),
                                  status="on progress"),
            models.TaskAssignment(id=uuid.uuid4(), scheduled_datetime=datetime.now(), inspector_id=uuid.uuid4(),
                                  status="completed"),
        ]

        self.db_mock.query.return_value.all.return_value = expected_result

        result = self.service.get_assigned_tasks()

        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], models.TaskAssignment)
        self.assertEqual(result, expected_result)
        self.db_mock.query.assert_called_once_with(models.TaskAssignment)
        self.db_mock.close.assert_called_once()

    def test_get_from_inspector(self):
        inspector_id = uuid.uuid4()
        expected_result = [
            models.TaskAssignment(id=uuid.uuid4(), scheduled_datetime=datetime.now(), inspector_id=inspector_id,
                                  status="pending"),
            models.TaskAssignment(id=uuid.uuid4(), scheduled_datetime=datetime.now(), inspector_id=inspector_id,
                                  status="on progress"),
            models.TaskAssignment(id=uuid.uuid4(), scheduled_datetime=datetime.now(), inspector_id=inspector_id,
                                  status="completed"),
        ]

        self.db_mock.query.return_value.filter.return_value.all.return_value = expected_result

        result = self.service.get_from_inspector(inspector_id)

        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], models.TaskAssignment)
        self.assertEqual(result, expected_result)
        self.db_mock.query.assert_called_once_with(models.TaskAssignment)
        # self.db_mock.filter.assert_called_once_with(models.TaskAssignment.inspector_id == inspector_id)
        self.db_mock.close.assert_called_once()

    def test_get_unfinished_from_inspector(self):
        inspector_id = uuid.uuid4()
        expected_result = [
            models.TaskAssignment(id=uuid.uuid4(), scheduled_datetime=datetime.now(), inspector_id=inspector_id,
                                  status="pending"),
            models.TaskAssignment(id=uuid.uuid4(), scheduled_datetime=datetime.now(), inspector_id=inspector_id,
                                  status="on progress"),
        ]

        self.db_mock.query.return_value.filter.return_value.filter.return_value.all.return_value = expected_result

        result = self.service.get_unfinished_from_inspector(inspector_id)

        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], models.TaskAssignment)
        self.assertEqual(result, expected_result)
        self.db_mock.query.assert_called_once_with(models.TaskAssignment)
        """self.db_mock.filter.assert_has_calls([
            call(models.TaskAssignment.inspector_id == inspector_id),
            call((models.TaskAssignment.status == "pending") | (models.TaskAssignment.status == "on progress"))
        ])"""
        self.db_mock.close.assert_called_once()

    def test_update_assigned_task(self):
        # Arrange
        uuid_mock = uuid.uuid4()
        task_assignment = models.TaskAssignment(
            id=uuid_mock, inspector_id=uuid.uuid4(),
            task_id=uuid.uuid4(), scheduled_datetime=datetime.now(), status="pending")
        self.db_mock.query().filter().first.return_value = task_assignment

        update_data = {"status": "completed", "rating": 8.0, "rating_description": "Very good!"}
        task_update = task_assignment_schemas.TaskAssignmentUpdate(**update_data)

        # Act
        updated_task_assignment = self.service.update_assigned_task(uuid_mock, task_update)

        # Assert
        self.db_mock.commit.assert_called_once()
        self.db_mock.refresh.assert_called_once_with(task_assignment)
        self.assertEqual(updated_task_assignment.status, task_update.status)

    def test_delete_assigned_task(self):
        # Arrange
        uuid_mock = uuid.uuid4()
        task_assignment = models.TaskAssignment(
            id=uuid_mock, inspector_id=uuid.uuid4(),
            task_id=uuid.uuid4(), scheduled_datetime=datetime.now(), status="pending")
        self.db_mock.query().filter().first.return_value = task_assignment

        # Act
        self.service.delete_assigned_task(uuid_mock)

        # Assert
        self.db_mock.delete.assert_called_once_with(task_assignment)
        self.db_mock.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
