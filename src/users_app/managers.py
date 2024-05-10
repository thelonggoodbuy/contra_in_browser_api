from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password




class CustomUserManager(BaseUserManager):

    def create_simple_user(self, username, email, password):
        if not email:
            raise ValueError("The Email must be str")
        email = self.normalize_email(email)
        user = self.model(username=username,
                        email=email, 
                        password=password)
        user.password = make_password(password)
        user.save()
        return user


    def create_superuser(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be str")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.username = self.model(username=username)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        
        user.save()
        return user