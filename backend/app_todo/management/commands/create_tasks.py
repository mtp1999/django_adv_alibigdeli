from django.core.management.base import BaseCommand
from faker import Faker
import random
from app_account.models import User
from app_todo.models import Task


class Command(BaseCommand):
    help = "Create 5 random tasks for the user with email 'admin3@gmail.com'."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.faker_object = Faker()

        try:
            user = User.objects.get(email='admin3@gmail.com', is_active=True)
        except:
            user = User.objects.create_user(email='admin3@gmail.com', password='a123456d')

        self.user = user

    def handle(self, *args, **options):
        try:
            for _ in range(5):
                Task.objects.create(
                    user=self.user.profile,
                    title=self.faker_object.job(),
                    status=random.choice([True, False])
                )
            print('Tasks are created successfully.')
        except Exception as e:
            raise Exception(f"An error occurred while creating tasks: {e}")
