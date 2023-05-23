from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
# this is model for custom user model

# model for superadmin
#model for superadmin
class MyAccountManager(BaseUserManager):
        #this is for creating normal user)
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an emailaddress')
        if not username:
            raise ValueError('user must have an username')
        
        user=self.model(
            email=self.normalize_email(email), 
            # if you enter capital emailaddress it will make small letter email automatically
            username=username,
            first_name=first_name,
            last_name=last_name
            

        )
        

        user.set_password(password) #to set password
        user.save(using=self.db)
        return user

    #this is for creating superuser)
    def create_superuser(self,first_name,last_name,email,username,password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name


            )

        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True 
        user.save(using=self.db)
        return user





class Account(AbstractBaseUser):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50, unique=True)
    email=models.EmailField(max_length=100, unique=True)
    phone_number=models.CharField(max_length=100)


    #Mandatory Field for custom usermodel)
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    # to login as email address(all about for login field)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name']

    #this is for like we are saying this class Account 
    # that we are using class MyAccountManager to do operations 
    objects=MyAccountManager()


# for string representation 
    def __str__(self):
        return self.email


# this is for permission allocation which we need for custom user model
    def has_perm(self, perm, obj=None):
        return self.is_admin  #is user is admin then he has all permission to make changes

    def has_module_perms(self,add_label):
        return True



