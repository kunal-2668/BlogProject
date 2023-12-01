from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Tags(models.Model):
    tagname = models.CharField(max_length=200)

    def __str__(self):
        return self.tagname


class Blog(BaseModel):
    blog_title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="user/images/blogs")
    description = RichTextField(blank=True,null=True)
    likes = models.ManyToManyField(User,blank=True,null=True, related_name='blog_like')
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="blogs")
    tags = models.ManyToManyField(Tags,blank=True,null=True, related_name='blog_tags')
    blog_slug = AutoSlugField(populate_from='blog_title',unique=True)

    def __str__(self):
        return self.blog_title

    def number_of_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created_at']


class Comments(BaseModel):
    Post = models.ForeignKey(Blog,on_delete=models.SET_NULL,null=True,related_name='blog_comments')
    Comment = models.CharField(max_length=300,blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    comment_likes = models.ManyToManyField(User,blank=True,null=True, related_name='comment_like')

    def __str__(self):
        return f"{self.Post},{self.Comment},{self.user}"
    
    def number_of_comment_likes(self):
        return self.comment_likes.count()
    
    class Meta:
        ordering = ['-created_at']