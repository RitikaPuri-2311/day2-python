from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.environ.get("APP_NAME")
DEBUG = os.environ.get("DEBUG")
#print(app_name)
#print(debug)