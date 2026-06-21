from abc import ABC, abstractmethod


# Abstraction (Interface)
class Database(ABC):

    @abstractmethod
    def save(self, data: str) -> None:
        pass


# MySQL implementation (Low-level module)
class MySQLDatabase(Database):

    def save(self, data: str) -> None:
        print(f"Executing SQL Query: INSERT INTO users VALUES('{data}');")


# MongoDB implementation (Low-level module)
class MongoDBDatabase(Database):

    def save(self, data: str) -> None:
        print(f"Executing MongoDB Function: db.users.insert({{name: '{data}'}})")


# High-level module
class UserService:

    def __init__(self, database: Database) -> None:
        self.db = database  # Dependency Injection

    def store_user(self, user: str) -> None:
        self.db.save(user)


# Driver code
mysql = MySQLDatabase()
mongodb = MongoDBDatabase()

service1 = UserService(mysql)
service1.store_user("Aditya")

service2 = UserService(mongodb)
service2.store_user("Rohit")