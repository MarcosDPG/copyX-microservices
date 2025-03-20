from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128, blank=False)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    last_login = models.DateTimeField(blank=True, null=True)

    first_name = None
    last_name = None
    username = None

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email', 'name', 'birth_date']

    class Meta:
        db_table = 'auth"."users'

    def __str__(self):
        return f"user_id: {self.user_id} - user_name: {self.user_name} - name: {self.name}"