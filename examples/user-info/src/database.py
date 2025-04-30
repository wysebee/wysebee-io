from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, func
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path

Base = declarative_base()
db_name = "user-info.db"
DATABASE_URL = f"sqlite:///{db_name}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def _add_column_if_not_exists(conn, table, column, column_def):
    # Check if column exists
    result = conn.execute(text(f"PRAGMA table_info({table})")).fetchall()
    existing_cols = [row[1] for row in result]  # row[1] is column name

    if column not in existing_cols:
        print(f"Adding column '{column}' to '{table}'...")
        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {column_def}"))
    else:
        print(f"Column '{column}' already exists in '{table}', skipping.")

MIGRATIONS = [
    {
        "id": "001_create_user_info_table",
        "fn": lambda conn: Table(
            "user_info", MetaData(),
            Column("id", Integer, primary_key=True),
            Column("userId", String),
            Column("name", String),
            Column("email", String),
            Column("avatar", String),
            Column("created_datetime", DateTime, default=func.now()),  # Set when record is created
            Column("update_datetime", DateTime, default=func.now(), onupdate=func.now())  # Update on modification
        ).create(bind=conn, checkfirst=True)
    },
]

class Migration(Base):
    __tablename__ = '_migrations'
    id = Column(String, primary_key=True)
    applied_at = Column(DateTime, default=func.now())  # Set when record is created
    def __str__(self):
        return f"{self.id}"

def run_migrations():
    with engine.connect() as conn:
        Table(
            "_migrations", MetaData(),
            Column("id", String, primary_key=True),
            Column("applied_at", DateTime, default=func.now()),  # Set when record is created
        ).create(bind=conn, checkfirst=True)

        for migration in MIGRATIONS:
            session = Session()
            result = session.query(Migration).filter_by(
                id=migration["id"]
            ).first()
            if result is None:
                print(f"Applying migration: {migration['id']}")
                migration["fn"](conn)
                try:
                    new_migration = Migration(id=migration["id"])
                    session.add(new_migration)
                    session.commit()
                    session.close()
                except Exception as e:
                    print(f"Warning: Migration SQL failed: {e}")

class UserInfo(Base):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True)
    userId = Column(String)
    name = Column(String)
    email = Column(String)
    avatar = Column(String)
    created_datetime = Column(DateTime, default=func.now())  # Set when record is created
    update_datetime = Column(DateTime, default=func.now(), onupdate=func.now())  # Update on modification

    def __str__(self):
        return f"{self.id}"

def get_user_info(userId):
    session = Session()
    user = session.query(UserInfo).filter_by(
        userId=userId
    ).first()
    if user is None:
        return None
    session.close()
    return user

def save_user_info(user_info):
    session = Session()
    user = session.query(UserInfo).filter_by(
        userId=user_info["userId"]
    ).first()
    if user:
        session.query(UserInfo).filter_by(
            userId=user_info["userId"]
        ).update(user_info)
    else:
        new_user = UserInfo(**user_info)
        session.add(new_user)
    session.commit()
    session.close()

def delete_user_info():
    session = Session()
    session.query(UserInfo).delete()
    session.commit()
    session.close()