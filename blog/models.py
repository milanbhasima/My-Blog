from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify

# Create your models here.
class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
	STATUS_CHOICES=(
		('draft','Draft'),
		('published','Published')
	)

	title=models.CharField(max_length=120)
	slug=models.SlugField(max_length=120)
	author=models.ForeignKey(User, related_name='blog_posts',on_delete=models.CASCADE)
	likes=models.ManyToManyField(User, related_name='likes', blank=True)
	body=models.TextField()
	image=models.ImageField(upload_to='images/', blank=True, null=True)
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)
	status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

	objects = models.Manager() #default manager
	published = PublishedManager() #custom model manager
	
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post-detail', kwargs={'id':self.id})

@receiver(pre_save, sender=Post)
def pre_save_slug(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug=slugify(instance.title)

class Profile(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE)
	dob=models.DateField(null=True, blank=True)
	photo=models.ImageField()

	def __str__(self):
		return self.user.username + 'profile'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)



class Comment(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	post=models.ForeignKey(Post)
	reply=models.ForeignKey('self', null=True, related_name='replies')
	content=models.TextField()
	timestamp=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '{}-{}'.format(self.post.title, self.user.username)
