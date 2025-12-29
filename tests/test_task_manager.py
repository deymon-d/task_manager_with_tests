import pytest
import tempfile
import os
from task_manager.database import Database
from datetime import datetime

@pytest.fixture
def temp_db():
    """Создание временной базы данных для тестов"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    db = Database(db_path)
    yield db
    
    # Очистка после тестов
    db.close()
    os.unlink(db_path)

def test_add_task(temp_db):
    """Тест добавления задачи"""
    task = temp_db.add_task("Test task", "Test description")
    
    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.completed == False
    assert isinstance(task.created_at, datetime)

def test_get_all_tasks(temp_db):
    """Тест получения всех задач"""
    temp_db.add_task("Task 1")
    temp_db.add_task("Task 2")
    
    tasks = temp_db.get_all_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Task 2"  # Сортировка по дате создания

def test_complete_task(temp_db):
    """Тест отметки задачи как выполненной"""
    task = temp_db.add_task("Test task")
    completed_task = temp_db.complete_task(1)
    
    assert completed_task.completed == True

def test_delete_task(temp_db):
    """Тест удаления задачи"""
    task = temp_db.add_task("Test task")
    tasks_before = temp_db.get_all_tasks()
    assert len(tasks_before) == 1
    
    temp_db.delete_task(1)
    tasks_after = temp_db.get_all_tasks()
    assert len(tasks_after) == 0

def test_get_pending_tasks(temp_db):
    """Тест получения невыполненных задач"""
    temp_db.add_task("Task 1")
    temp_db.add_task("Task 2")
    temp_db.complete_task(1)
    
    pending = temp_db.get_pending_tasks()
    assert len(pending) == 1
    assert pending[0].title == "Task 2"
