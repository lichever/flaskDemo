# -*- coding:utf-8 -*-
# !/usr/bin/env python3
# @Author: Sean
# @Time: 2024/1/20
# @File: Sqlalchemy.py

'''
orm模型映射数据库关系
'''

from sqlalchemy import Column,String,Integer,create_engine,ForeignKey,DateTime
from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from contextlib import contextmanager

# 创建对象基类

Base = declarative_base()

# 创建数据库引擎
db_engine = create_engine('mysql+pymysql://root:123456@localhost:3306/db')
DB_session = sessionmaker(bind=db_engine)

#创建数据库会话
@contextmanager
def db_session():
    session = DB_session()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        print(f'{e},执行数据库时发生错误')
        session.rollback()
    finally:
        session.close()

class BaseTime:
    create_time = Column(DateTime,nullable=False,server_default=func.now(),comment='创建时间')
    update_time = Column(DateTime,nullable=False,server_default=func.now(),comment='更新时间')
    delete_time = Column(DateTime,nullable=False,server_default=func.now(),comment='删除时间')

class User(Base,BaseTime):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,nullable=False,unique=True,autoincrement=True)
    name = Column(String(20),nullable=False)
    age = Column(Integer,nullable=False)
    # 一对多
    books = relationship('Book',back_populates='users')

class Book(Base,BaseTime):
    __tablename__ = 'book'
    id = Column(Integer,primary_key=True,nullable=False,unique=True,autoincrement=True)
    book_name = Column(String(20),nullable=False)
    author = Column(String(20),nullable=False)
    #多一方book表通过外件关联user表
    user_id = Column(Integer,ForeignKey('user.id'),nullable=False)
    users = relationship('User',back_populates='books')

# 创建表
Base.metadata.create_all(db_engine)

with db_session() as session:
    users = [
    {'name': '小李',
    'age': 19,
    },
    {'name': '小明',
    'age': 20}
    ]
    # 批量插入
    session.bulk_insert_mappings(User, users)

with db_session() as session:
    user_id = 1
    user = session.query(User).filter(User.id ==user_id).first()
    if not user:
        raise ValueError(f'id{user_id}不存在')
    else:
        books=[{
        'book_name':'西游记',
        'author':'吴承恩',
        'user_id':user_id

        }]
        session.bulk_insert_mappings(Book,books)