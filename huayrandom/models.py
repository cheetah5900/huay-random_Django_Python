from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Profile
class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    house_name = models.CharField(default='None', max_length=255)
    usertype = models.CharField(default='random', max_length=255)
    status = models.BooleanField(default=True)
    expire_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

# HuayType
class HuayTypeModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(default='None', max_length=255)
    time = models.DateTimeField()
    link = models.CharField(default='None', max_length=255)
    page_name = models.CharField(default='None', max_length=255)
    font_text = models.CharField(default='None', max_length=255)
    font_number = models.CharField(default='None', max_length=255)
    text_color = models.CharField(default='None', max_length=255)
    border_size = models.IntegerField(default=0)
    border_color = models.CharField(default='None', max_length=255)
    text_pos_x = models.IntegerField(default=0)
    text_pos_y = models.IntegerField(default=0)
    text_font_size = models.IntegerField(default=0)
    data_pos_x = models.IntegerField(default=0)
    data_pos_y = models.IntegerField(default=0)
    data_font_size = models.IntegerField(default=0)
    main_num_pos_x = models.IntegerField(default=0)
    main_num_pos_y = models.IntegerField(default=0)
    main_num_font_size = models.IntegerField(default=0)
    focus_num_pos_x = models.IntegerField(default=0)
    focus_num_pos_y = models.IntegerField(default=0)
    focus_num_font_size = models.IntegerField(default=0)
    row1_x = models.IntegerField(default=0)
    row1_y = models.IntegerField(default=0)
    row2_x = models.IntegerField(default=0)
    row2_y = models.IntegerField(default=0)
    row_font_size = models.IntegerField(default=0)

    def __str__(self):
        return self.name
