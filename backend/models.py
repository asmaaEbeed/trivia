import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "trivia"
database_path = "postgres://{}@{}/{}".format('ahmed:123', 'localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Category
'''


class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    cat_type = Column(String)
    question = relationship('Question', backref='cat', lazy=True)

    def __init__(self, cat_type):
        self.cat_type = cat_type

    def format(self):
        return {
          'id': self.id,
          'cat_type': self.cat_type
        }


'''
Question
'''


class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    # category = Column(String)
    difficulty = Column(Integer)
    cat_Id = Column(Integer, db.ForeignKey('categories.id'))

    def __init__(self, question, answer, difficulty, cat_Id):
        self.question = question
        self.answer = answer
        # self.category = category
        self.difficulty = difficulty
        self.cat_Id = cat_Id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'question': self.question,
          'answer': self.answer,
          # 'category': self.category,
          'difficulty': self.difficulty,
          'category': self.cat_Id,
        }



