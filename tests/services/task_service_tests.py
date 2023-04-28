import unittest
import uuid
from datetime import datetime
from typing import List
from unittest.mock import Mock

from sqlalchemy.orm import Session

from app.core.models import models
from app.core.models.models import Task
from app.core.schemas import task_schemas as schemas
from app.services.task_service import TaskService


class TaskServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.db_mock = Mock(spec=Session)
        self.service = TaskService(db=self.db_mock)

    def test_create_task(self):
        task_create_schema = schemas.TaskCreate(title="Test task", description="Task description",
                                                deadline=datetime.now(), location="Madrid")

        result = self.service.create_task(task_create_schema)

        self.assertIsInstance(result, Task)
        self.assertEqual(result.title, task_create_schema.title)
        self.assertEqual(result.description, task_create_schema.description)
        self.assertEqual(result.deadline, task_create_schema.deadline)
        self.assertEqual(result.location, task_create_schema.location)

        self.db_mock.add.assert_called_once_with(result)
        self.db_mock.commit.assert_called_once()
        self.db_mock.refresh.assert_called_once_with(result)

    def test_create_task_exception(self):
        task_create_schema = schemas.TaskCreate(
            title="Test task",
            description="Task description",
            deadline=datetime.now(),
            location="Madrid"
        )
        self.db_mock.add(task_create_schema)
        self.db_mock.commit.side_effect = Exception("Error committing to database")
        with self.assertRaises(Exception):
            self.service.create_task(task_create_schema)
        self.db_mock.rollback.assert_called_once()

    def test_get_task(self):
        uuid_mock = uuid.uuid4()
        task = Task(
            id=uuid_mock,
            title="Test task",
            description="Task description",
            deadline=datetime.now(),
            location="Madrid"
        )
        self.db_mock.query().filter().first.return_value = task

        result = self.service.get_task(uuid_mock)

        self.assertIsInstance(result, Task)
        self.assertEqual(result.id, task.id)
        self.assertEqual(result.title, task.title)
        self.assertEqual(result.description, task.description)
        self.assertEqual(result.deadline, task.deadline)
        self.assertEqual(result.location, task.location)

    def test_get_task_exception(self):
        uuid_mock = uuid.uuid4()
        self.db_mock.query.return_value.filter.return_value.first.side_effect = Exception("Error querying database")
        with self.assertRaises(Exception):
            self.service.get_task(uuid_mock)
        self.db_mock.rollback.assert_called_once()

    def test_get_tasks(self):
        task = models.Task(
            id=uuid.uuid4(),
            title="Test task",
            description="Task description",
            deadline=datetime.now(),
            location="Madrid"
        )
        self.db_mock.query.return_value.all.return_value = [task]

        result = self.service.get_tasks()

        self.assertIsInstance(result, List)
        self.assertEqual(result[0].id, task.id)
        self.assertEqual(result[0].title, task.title)
        self.assertEqual(result[0].description, task.description)
        self.assertEqual(result[0].deadline, task.deadline)
        self.assertEqual(result[0].location, task.location)

    def test_get_tasks_exception(self):
        self.db_mock.query.return_value.all.side_effect = Exception("Error querying database")
        with self.assertRaises(Exception):
            self.service.get_tasks()
        self.db_mock.rollback.assert_called_once()

    def test_get_available_tasks(self):
        task = models.Task(
            id=uuid.uuid4(),
            title="Test task",
            description="Task description",
            deadline=datetime.now(),
            location="Madrid"
        )
        self.db_mock.query.return_value.join.return_value.filter.return_value.all.return_value = [task]

        result = self.service.get_available_tasks()

        self.assertIsInstance(result, List)
        self.assertEqual(result[0].id, task.id)
        self.assertEqual(result[0].title, task.title)
        self.assertEqual(result[0].description, task.description)
        self.assertEqual(result[0].deadline, task.deadline)
        self.assertEqual(result[0].location, task.location)

    def test_get_available_tasks_exception(self):
        self.db_mock.query.return_value.join.return_value.filter.return_value.all.side_effect = \
            Exception("Error querying database")

        with self.assertRaises(Exception):
            self.service.get_available_tasks()
        self.db_mock.rollback.assert_called_once()

    def test_update_task(self):
        uuid_mock = uuid.uuid4()
        task_update = schemas.TaskUpdate(title="Updated task", description="Updated task description",
                                         deadline=datetime.now(), location="New York")
        task = models.Task(id=uuid_mock, title="Test task", description="Task description", deadline=datetime.now(),
                           location="Madrid")
        self.db_mock.query().filter().first.return_value = task

        result = self.service.update_task(uuid_mock, task_update)

        self.assertIsInstance(result, Task)
        self.assertEqual(result.id, task.id)
        self.assertEqual(result.title, task_update.title)
        self.assertEqual(result.description, task_update.description)
        self.assertEqual(result.deadline, task_update.deadline)
        self.assertEqual(result.location, task_update.location)

    def test_update_task_exception(self):
        uuid_mock = uuid.uuid4()
        task_update = schemas.TaskUpdate(title="Updated task", description="Updated task description",
                                         deadline=datetime.now(), location="New York")
        self.db_mock.query.return_value.filter.return_value.first.side_effect = \
            Exception("Error updating task in database")

        with self.assertRaises(Exception) as context:
            self.service.update_task(uuid.uuid4(), task_update)

        self.assertEqual(str(context.exception), "Error updating task in database")
        #self.db_mock.rollback.assert_called_once()

    def test_delete_task(self):
        uuid_mock = uuid.uuid4()
        task = models.Task(id=uuid_mock, title="Test task", description="Task description", deadline=datetime.now(),
                           location="Madrid")
        self.db_mock.query().filter().first.return_value = task

        # Act
        self.service.delete_task(uuid_mock)

        # Assert
        self.db_mock.delete.assert_called_once_with(task)
        self.db_mock.commit.assert_called_once()

    def test_delete_task_exception(self):
        uuid_mock = uuid.uuid4()
        self.db_mock.query().filter().first.side_effect = Exception("Error deleting task in database")

        # Act
        with self.assertRaises(Exception) as context:
            self.service.delete_task(uuid.uuid4())

        self.assertEqual(str(context.exception), "Error deleting task in database")


if __name__ == '__main__':
    unittest.main()
