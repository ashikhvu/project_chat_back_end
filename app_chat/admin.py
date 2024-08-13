from django.contrib import admin
from .models import UserModel,Request,ChatModel

# Register your models here.
admin.site.register(UserModel)             
admin.site.register(Request)             
admin.site.register(ChatModel)             
