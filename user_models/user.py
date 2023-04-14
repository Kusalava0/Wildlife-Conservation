from beanie import Document

class User(Document):
    username: str
    hashed_password: str
    is_admin: bool = False
