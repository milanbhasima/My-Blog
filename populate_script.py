import os, django, random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'verma.settings')
django.setup()

from faker import Faker
from blog.models import Post
from django.contrib.auth.models import User
from django.utils import timezone

def create_post(N):
	fake=Faker()
	for _ in range(N):
		id = random.randint(1,3)
		title=fake.name()
		status=random.choice(['published','draft'])
		body=fake.text()
		Post.objects.create(
		title=title + 'post!', 
		author=User.objects.get(id=id), 
		slug='-'.join(title.lower().split()),
		body=body,
		created=timezone.now(),
		updated=timezone.now()
		)

create_post(10)
print('data is populatted successfully')