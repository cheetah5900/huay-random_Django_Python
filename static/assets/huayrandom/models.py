from django.db import models
from django.contrib.auth.models import User

# Profile
class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    house_name = models.CharField(default='None', max_length=255)
    usertype = models.CharField(default='random', max_length=255)
    status = models.BooleanField(default=True)
    expire_date = models.DateTimeField(null=True, blank=True)
    credit_shop = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class HuayListModel(models.Model):
    short_name = models.CharField(default='None', max_length=255)
    full_name = models.CharField(default='None', max_length=255)
    page_name = models.CharField(default='None', max_length=255)
    time = models.TimeField()
    link = models.CharField(default='None', max_length=255)

    def __str__(self):
        return self.short_name

class FontListModel(models.Model):
    font_name = models.CharField(default='Prompt.ttf', max_length=255)
    
    def __str__(self):
        return self.font_name

# HuayType
class HuayTypeModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    huay_list = models.ForeignKey(HuayListModel, on_delete=models.CASCADE)
    font_text = models.CharField(default='None', max_length=255)
    font_number = models.CharField(default='None', max_length=255)
    text_color = models.CharField(default='None', max_length=255)
    border_size = models.IntegerField(default=0)
    border_color = models.CharField(default='None', max_length=255)
    text_pos_x = models.IntegerField(default=0)
    text_pos_y = models.IntegerField(default=0)
    text_font_size = models.IntegerField(default=0)
    date_pos_x = models.IntegerField(default=0)
    date_pos_y = models.IntegerField(default=0)
    date_font_size = models.IntegerField(default=0)
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
    credit_shop_pos_x = models.IntegerField(default=0)
    credit_shop_pos_y = models.IntegerField(default=0)
    credit_shop_font_size = models.IntegerField(default=0)

    def __str__(self):
        return self.huay_list.short_name
        