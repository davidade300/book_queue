import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    TEST_DATABASE_URL: str = str(os.getenv('TEST_DATABASE_URL'))
    DATABASE_URL: str = f'{os.getenv("DRIVERNAME")}://{os.getenv("USERNAME")}:{os.getenv("PASSWORD")}@{os.getenv("HOST")}/{os.getenv("DATABASE")}'
