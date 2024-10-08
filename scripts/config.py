import os
import openai
SECRET_KEY = os.getenv('SECRET_KEY', '123456')  
openai.api_key = ''