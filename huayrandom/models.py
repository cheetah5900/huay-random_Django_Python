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
    # สุ่มว่าจะให้มีเลข วิ่ง-รูด ในเลขเจาะหรือไม่
    random_mode = models.CharField(default='random_any', max_length=255)

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

class ColorListModel(models.Model):
    color_name = models.CharField(default='None', max_length=255)
    color_code = models.CharField(default='255,255,255', max_length=255)
    
    def __str__(self):
        return self.color_name

class ImageHouseModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_name = models.CharField(default='None', max_length=255)
    location = models.CharField(default='None', max_length=255)
    
    def __str__(self):
        return self.image_name

# HuayType
class HuayTypeModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    huay_list = models.ForeignKey(HuayListModel, on_delete=models.CASCADE)
    image_house = models.ForeignKey(ImageHouseModel,default=1, on_delete=models.CASCADE)
    date_font = models.CharField(default='supermarket.ttf', max_length=255)
    date_font_size = models.IntegerField(default=30)
    date_font_color = models.IntegerField(default=1)
    date_pos_x = models.IntegerField(default=1220)
    date_pos_y = models.IntegerField(default=45)
    date_border_size = models.IntegerField(default=4)
    date_border_color = models.IntegerField(default=2)
    date_border_status = models.CharField(default='off', max_length=25)
    text_font = models.CharField(default='supermarket.ttf', max_length=255)
    text_color = models.IntegerField(default=1)
    text_border_status = models.CharField(default='off', max_length=25)
    text_border_size = models.IntegerField(default=4)
    text_border_color = models.IntegerField(default=2)
    text_pos_x = models.IntegerField(default=500)
    text_pos_y = models.IntegerField(default=560)
    text_font_size = models.IntegerField(default=90)
    main_num_pos_x = models.IntegerField(default=550)
    main_num_pos_y = models.IntegerField(default=720)
    main_num_font = models.CharField(default='HelveticaNeue.ttf', max_length=255)
    main_num_font_size = models.IntegerField(default=90)
    main_num_font_color = models.IntegerField(default=1)
    main_num_separator = models.CharField(default=' - ', max_length=255)
    main_num_border_status = models.CharField(default='off', max_length=25)
    main_num_border_size = models.IntegerField(default=4)
    main_num_border_color = models.IntegerField(default=2)
    focus_num_pos_x = models.IntegerField(default=1025)
    focus_num_pos_y = models.IntegerField(default=780)
    focus_num_font = models.CharField(default='HelveticaNeue.ttf', max_length=255)
    focus_num_font_color = models.IntegerField(default=1)
    focus_num_font_size = models.IntegerField(default=230)
    focus_num_border_size = models.IntegerField(default=4)
    focus_num_border_color = models.IntegerField(default=2)
    focus_num_border_status = models.CharField(default='off', max_length=25)
    row_font = models.CharField(default='HelveticaNeue.ttf', max_length=255)
    row_font_size = models.IntegerField(default=90)
    row1_color= models.IntegerField(default=1)
    row1_x = models.IntegerField(default=170)
    row1_y = models.IntegerField(default=900)
    row1_border_status = models.CharField(default='off', max_length=25)
    row1_border_size = models.IntegerField(default=4)
    row1_border_color = models.IntegerField(default=2)
    row1_separator = models.CharField(default=' - ', max_length=25,blank=True)
    row2_x = models.IntegerField(default=170)
    row2_y = models.IntegerField(default=1000)
    row2_separator = models.CharField(default=' - ', max_length=25,blank=True)
    row2_color= models.IntegerField(default=1)
    row2_border_status = models.CharField(default='off', max_length=25)
    row2_border_size = models.IntegerField(default=4)
    row2_border_color = models.IntegerField(default=2)
    credit_shop_pos_x = models.IntegerField(default=0)
    credit_shop_pos_y = models.IntegerField(default=0)
    credit_shop_font_size = models.IntegerField(default=0)
    credit_shop_border_size = models.IntegerField(default=4)
    credit_shop_border_color = models.IntegerField(default=2)
    credit_shop_border_status = models.CharField(default='off', max_length=25)
    three_main_status = models.CharField(default='off', max_length=255)
    three_main_font = models.CharField(default='HelveticaNeue.ttf', max_length=255)
    three_main_font_size = models.IntegerField(default=90)
    three_main_font_color= models.IntegerField(default=1)
    three_main_border_status = models.CharField(default='off', max_length=25)
    three_main_border_size = models.IntegerField(default=4)
    three_main_border_color = models.IntegerField(default=2)
    three_main_pos_x = models.IntegerField(default=170)
    three_main_pos_y = models.IntegerField(default=200)
    three_main_separator = models.CharField(default=' - ', max_length=25)
    three_sub_status = models.CharField(default='off', max_length=25)
    three_sub_font = models.CharField(default='HelveticaNeue.ttf', max_length=255)
    three_sub_font_size = models.IntegerField(default=90)
    three_sub_font_color= models.IntegerField(default=1)
    three_sub_border_status = models.CharField(default='off', max_length=25)
    three_sub_border_size = models.IntegerField(default=4)
    three_sub_border_color = models.IntegerField(default=2)
    three_sub_pos_x = models.IntegerField(default=170)
    three_sub_pos_y = models.IntegerField(default=200)
    three_sub_separator = models.CharField(default=' - ', max_length=25)
    remark_status = models.CharField(default='off', max_length=25)
    remark_text = models.CharField(default='-', max_length=255)
    remark_font = models.CharField(default='supermarket.ttf', max_length=255)
    remark_font_size = models.IntegerField(default=90)
    remark_font_color= models.IntegerField(default=1)
    remark_border_status = models.CharField(default='off', max_length=25)
    remark_border_size = models.IntegerField(default=4)
    remark_border_color = models.IntegerField(default=2)
    remark_pos_x = models.IntegerField(default=170)
    remark_pos_y = models.IntegerField(default=200)

    def __str__(self):
        return self.huay_list.short_name

