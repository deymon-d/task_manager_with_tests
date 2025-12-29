from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    due_date = Column(DateTime, nullable=True)

class Database:
    def __init__(self, db_name='tasks.db'):
        self.engine = create_engine(f'sqlite:///{db_name}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def add_task(self, title, description="", due_date=None):
        task = Task(title=title, description=description, due_date=due_date)
        self.session.add(task)
        self.session.commit()
        return task
    
    def get_all_tasks(self):
        return self.session.query(Task).order_by(Task.created_at.desc()).all()
    
    def get_task(self, task_id):
        return self.session.query(Task).filter(Task.id == task_id).first()
    
    def complete_task(self, task_id):
        task = self.get_task(task_id)
        if task:
            task.completed = True
            self.session.commit()
        return task
    
    def delete_task(self, task_id):
        task = self.get_task(task_id)
        if task:
            self.session.delete(task)
            self.session.commit()
        return task
    
    def get_pending_tasks(self):
        return self.session.query(Task).filter(Task.completed == False).all()
    
    def close(self):
        self.session.close()
