from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from app_account.models import Profile
from django.utils.timezone import now


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(default=now)
    status = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    image = models.ImageField(upload_to='app_blog/posts/images/', null=True, blank=True)
    categories = models.ManyToManyField('Category', db_table='app_blog_post_category')
    tags = TaggableManager(blank=True)

    class Meta:
        db_table = 'app_blog_post'

    def __str__(self):
        return str(self.id) + '-' + self.title

    def get_absolute_url(self):
        return reverse('app_blog:single', kwargs={'pid': self.id})

    def get_absolute_api_url(self):
        return reverse('app_blog:api_v1:post-detail', kwargs={'pk': self.id})


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'app_blog_category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_blog_contact'
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    allowed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_blog_comment'
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return str(self.id) + '-' + self.subject
