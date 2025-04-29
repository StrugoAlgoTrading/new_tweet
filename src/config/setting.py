from pydantic import BaseModel
import yaml
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()


class Conf(BaseModel):
    COOKIES_FILE: str
    LAST_ID_FILE: str


class Secrets(BaseModel):
    TRUMP_URL: str
    PUSH_URL: str
    USERNAME: str
    PASSWORD: str
    LOGIN_URL: str


def load_config(file_name: str):
    file_path = Path(__file__).parent / file_name
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
        return data


CONFIG = Conf(**load_config("config.yaml"))

SECRETS = Secrets(TRUMP_URL=os.getenv("TRUMP_URL"), PUSH_URL=os.getenv("PUSH_URL"), USERNAME=os.getenv("PUSH_URL"),
                  PASSWORD=os.getenv("PASSWORD"), LOGIN_URL=os.getenv("LOGIN_URL"))
