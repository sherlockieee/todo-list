# Write your code here
# Write your code here

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class ToDo(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_task():
    new_task = input("\nEnter task")
    new_deadline = datetime.strptime(input("Enter deadline (format: YYYY-MM-DD)\n"), '%Y-%m-%d')
    new_row = ToDo(task=new_task, deadline=new_deadline)
    session.add(new_row)

    session.commit()
    print("The task has been added!\n")


def see_task_by_day(date):
    print(f"\n{date.strftime('%A')} {date.day} {date.strftime('%b')}:")
    rows = session.query(ToDo).filter(ToDo.deadline == date.date()).all()
    if not rows:
        print("Nothing to do!\n")
    else:
        for index, row in enumerate(rows):
            print(f"{index + 1}. {row.task}")
        print()

def see_missed_task():
    today = datetime.today()
    rows = session.query(ToDo).filter(ToDo.deadline < today.date()).order_by(ToDo.deadline).all()
    if not rows:
        print("Nothing is missed!\n")
    else:
        print("Missed tasks:")
        for index,row in enumerate(rows):
            deadline_reformatted = str(row.deadline.day) + " " + row.deadline.strftime('%b')
            print(f"{index+1}. {row.task}. {deadline_reformatted}")
        print()


def see_all_tasks():
    rows = session.query(ToDo).order_by(ToDo.deadline).all()
    if not rows:
        print("Nothing to do!\n")
    else:
        for index,row in enumerate(rows):
            deadline_reformatted = str(row.deadline.day) + " " + row.deadline.strftime('%b')
            print(f"{index+1}. {row.task}. {deadline_reformatted}")
        print()

def delete_task():
    print('\nChoose the number of the task you want to delete:')
    see_all_tasks()
    task_to_delete = int(input())
    rows = session.query(ToDo).order_by(ToDo.deadline).all()
    while task_to_delete not in range(1, len(rows)+1):
        task_to_delete = int(input(f"Please choose the number in range {len(rows)+1}"))
    row_to_delete = rows[task_to_delete - 1]
    session.delete(row_to_delete)
    session.commit()
    print("The task has been deleted!\n")


while True:
    option = int(input('''1) Today\'s tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit\n'''))
    if option == 1:
        see_task_by_day(datetime.today())
    elif option == 2:
        for x in range(7):
            next_day = datetime.today() + timedelta(days=x)
            see_task_by_day(next_day)
    elif option == 3:
        print("\nAll tasks:")
        see_all_tasks()
    elif option == 4:
        see_missed_task()
    elif option == 5:
        add_task()
    elif option == 6:
        delete_task()
    elif option == 0:
        print("Bye")
        break
    else:
        print("Please enter 0, 1, 2, 3, 4, 5 or 6")
