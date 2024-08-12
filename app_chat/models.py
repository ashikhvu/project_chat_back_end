from django.db import models
from django.contrib.auth.models import User

class UserModel(User):
    name = models.CharField(max_length=255,blank=True,null=True)
    about = models.TextField(blank=True,null=True,default="Hey There. I am Using C-hat")
    contact = models.IntegerField(blank=True,null=True)
    image = models.ImageField(upload_to='downloads/',blank=True,null=True)

class ChatModel(models.Model):
    from_user = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name="from_user",blank=True,null=True)
    to_user = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name="to_user",blank=True,null=True)
    msg = models.TextField()
    status_choices = (
        ('read','read'),
        ('unread','unread')
    ) 
    status = models.CharField(max_length=255,choices=status_choices)
    create_at = models.DateTimeField(auto_now_add=True)

class Request(models.Model):
    req_from = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name="send_req_from",blank=True,null=True)
    req_to = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name="send_req_to",blank=True,null=True)
    status_choices = (
        ('default','Default'),
        ('send','Send'),
        ('blocked','Blocked'),
        ('accepted','Accepted')
    )
    status = models.CharField(max_length=255,choices=status_choices,default="default",blank=True,null=True)
