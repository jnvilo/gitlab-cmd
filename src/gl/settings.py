from typing import List
from pydantic import validator
from pydantic import Field
from pydantic import BaseModel
from pydantic import ValidationError
import sys
import json
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    This class is used to parse the settings file and
    provide the settings to the rest of the application.
    """

try:
    settings = Settings()
except ValidationError as e:
    print("Error: Settings file is invalid")
    print(e)
    sys.exit(1)
