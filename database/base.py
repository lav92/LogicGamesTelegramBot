from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, BigInteger, Integer, Text, Table, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


user_task_binding = Table(
    'user_task',
    Base.metadata,
    Column('user_id', BigInteger, ForeignKey('users.user_id')),
    Column('task_id', BigInteger, ForeignKey('tasks.id'))
)


class User(Base):
    __tablename__ = 'users'
    user_id = Column(BigInteger, unique=True, primary_key=True)
    tasks = relationship('Task', secondary=user_task_binding, back_populates='users')

    def __str__(self):
        return f'User(user_id={self.user_id})'


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    text = Column(Text, nullable=False)
    answer = Column(VARCHAR, nullable=False)
    level = Column(Integer, default=1)
    users = relationship('User', secondary=user_task_binding, back_populates='tasks')

    def __str__(self):
        return f'Task(text={self.text}, id={self.id})'

    def __eq__(self, other):
        return self.id == other.id
