
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from src.users_app.models import CustomUser




class Command(BaseCommand):
    help = 'Users builder and admin initialization'
    
    def handle(self, *args, **kwargs):
        try:
            CustomUser.objects.get(is_superuser=True)
        except ObjectDoesNotExist:
            print('================================================')
            print('------You--run--INITIAL--SUPERUSER--script------')
            print('================================================')
            admin_user = CustomUser(
                email="admin@gmail.com",
                is_superuser=True,
                is_staff=True,
                username='admin',
            )
            admin_user.set_password('123@zxc67')
            admin_user.save()
            print('==============================================')
            print('------initial-admin-was-been-created----------')
            print(f'Email is {admin_user.email}.')
            print(f"Password is '123@zxc67'")
            print('==============================================')
        

        try:
            CustomUser.objects.get(email='simple_user_1@gmail.com')

        except ObjectDoesNotExist:
            print('================================================')
            print('----------SIMPLE--USER--INITIALISATION--------')
            print('================================================')
            builder_user = CustomUser(
                email="simple_user_1@gmail.com",
                username='simple_user_1'
            )
            builder_user.set_password('Password_1')
            builder_user.save()
            print('==============================================')
            print('----initial--simple-user--was--been--created------')
            print(f'Email is {builder_user.email}.')
            print(f"Password is 'Password_1'")
            print('==============================================')

            print('==============================================')
           

        
        try:
            CustomUser.objects.get(email='simple_user_2@gmail.com')

        except ObjectDoesNotExist:
            print('================================================')
            print('----------SIMPLE--USER--INITIALISATION--------')
            print('================================================')
            builder_user = CustomUser(
                email="simple_user_2@gmail.com",
                username='simple_user_2'
            )
            builder_user.set_password('Password_2')
            builder_user.save()
            print('==============================================')
            print('----initial--simple-user--was--been--created------')
            print(f'Email is {builder_user.email}.')
            print(f"Password is 'Password_2'")
            print('==============================================')

            print('==============================================')
           

        
        try:
            CustomUser.objects.get(email='simple_user_3@gmail.com')

        except ObjectDoesNotExist:
            print('================================================')
            print('----------SIMPLE--USER--INITIALISATION--------')
            print('================================================')
            builder_user = CustomUser(
                email="simple_user_3@gmail.com",
                username='simple_user_3'
            )
            builder_user.set_password('Password_3')
            builder_user.save()
            print('==============================================')
            print('----initial--simple-user--was--been--created------')
            print(f'Email is {builder_user.email}.')
            print(f"Password is 'Password_3'")
            print('==============================================')

            print('==============================================')
           