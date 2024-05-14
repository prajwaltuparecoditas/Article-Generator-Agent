from django.db import models
from django.contrib.auth.models import AbstractUser
from langchain_core.chat_history import BaseChatMessageHistory
from django.contrib.sessions.models import Session
# Create your models here.
class User(AbstractUser):
    pass

