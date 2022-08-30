from django.urls import path
from huayrandom.views import *

urlpatterns = [
    path('', Index, name='index'),

    path('<str:username>', Home, name='home'),
    path('result/<str:username>/<str:link>', Result, name='result'),

    path('backend/', Backend, name='backend'),

    path('backend/huay/list',
         ListHuay, name='list_huay'),
    path('backend/huay/add',
         AddHuayList, name='add_huay_list'),
    path('backend/huay/edit/<int:id>',
         EditHuayList, name='edit_huay_list'),

    path('backend/huay/type/list/<str:username>',
         ListHuayType, name='list_huay_type'),
    path('backend/huay/type/add/<str:username>',
         AddHuayType, name='add_huay_type'),
    path('backend/huay/type/edit/<str:username>/<int:huay_id>',
         EditHuayType, name='edit_huay_type'),
    path('backend/huay/type/del/<str:username>/<int:huay_id>',
         DeleteHuayType, name='delete_huay_type'),


    path('backend/image/list/<str:username>',
         ListImage, name='list_image'),
    path('backend/user/image/add/<str:username>',
         AddImage, name='add_image'),
    path('backend/user/image/edit/<str:username>/<int:image_id>',
         EditImage, name='edit_image'),

    path('backend/user/list', ListUser, name='list_user'),
    path('backend/user/add', AddUser, name='add_user'),
    path('backend/user/edit/<str:username>', EditUser, name='edit_user'),


    path('backend/color/list',
         ListColor, name='list_color'),
    path('backend/color/add',
         AddColor, name='add_color'),
    path('backend/color/edit/<str:color_id>',
         EditColor, name='edit_color'),

    # * Set All Section
    #  props = font family / font color
    #  set = huay_name / เลข 2 วิ่งรูด / เลข เจาะ
    path('backend/huay_type/hub/edit/<str:username>/<int:huay_id>',
         HubForEditHuayType, name="hub_edit_huay_type"),
    path('backend/huay_name/font_family/<str:username>/<int:huay_id>/<str:text_font>',
         SetAllHuayNameFontFamily, name="set_all_huay_name_font_family"),
    path('backend/huay_name/font_color/<str:username>/<int:huay_id>/<str:text_color>',
         SetAllHuayNameFontColor, name="set_all_huay_name_font_color"),
    path('backend/huay_name/font_size/<str:username>/<int:huay_id>/<str:text_size>',
         SetAllHuayNameFontSize, name="set_all_huay_name_font_size"),
    path('backend/huay_name/pos/<str:username>/<int:huay_id>/<int:text_pos_x>/<int:text_pos_y>',
         SetAllHuayNamePos, name="set_all_huay_name_pos"),
    path('backend/huay_name/pos/<str:username>/<int:huay_id>/<str:text_border_status>/<int:text_border_size>/<int:text_border_color>',
         SetAllHuayNameBorder, name="set_all_huay_name_border"),

    path('backend/main_num/<str:username>/<int:huay_id>/<str:main_num_font>/<str:main_num_font_color>/<str:main_num_font_size>/<str:main_num_separator>/<str:main_num_pos_x>/<str:main_num_pos_y>/<str:main_num_border_status>/<str:main_num_border_color>/<str:main_num_border_size>', SetAllMainNum, name="set_all_main_num"),
    path('backend/row1/<str:username>/<int:huay_id>/<str:row1_font>/<str:row1_font_size>/<str:row1_font_color>/<str:row1_separator>/<str:row1_pos_x>/<str:row1_pos_y>/<str:row1_border_status>/<str:row1_border_color>/<str:row1_border_size>', SetAllRow1, name="set_all_row1"),
    path('backend/row2/<str:username>/<int:huay_id>/<str:row2_font_color>/<str:row2_separator>/<str:row2_pos_x>/<str:row2_pos_y>/<str:row2_border_status>/<str:row2_border_color>/<str:row2_border_size>', SetAllRow2, name="set_all_row2"),
    path('backend/focus_num/<str:username>/<int:huay_id>/<str:focus_num_font><str:focus_num_font_color>/<int:focus_num_font_size>/<int:focus_num_pos_x>/<int:focus_num_pos_y>/<str:focus_num_border_status>/<int:focus_num_border_size>/<int:focus_num_border_color>', SetAllFocusNumber, name="set_all_focus_num"),
    path('backend/three_main_num/<str:username>/<int:huay_id>/<str:three_main_status>/<str:three_main_font>/<str:three_main_font_color>/<int:three_main_font_size>/<str:three_main_separator>/<int:three_main_pos_x>/<int:three_main_pos_y>/<str:three_main_border_status>/<int:three_main_border_size>/<int:three_main_border_color>', SetAllThreeMainNumber, name="set_all_three_main_num"),
    path('backend/three_sub_num/<str:username>/<int:huay_id>/<str:three_sub_status>/<str:three_sub_font>/<str:three_sub_font_color>/<int:three_sub_font_size>/<str:three_sub_separator>/<int:three_sub_pos_x>/<int:three_sub_pos_y>/<str:three_sub_border_status>/<int:three_sub_border_size>/<int:three_sub_border_color>', SetAllThreeSubNumber, name="set_all_three_sub_num"),
    path('backend/remark/<str:username>/<int:huay_id>/<str:remark_status>/<str:remark_text>/<str:remark_font>/<str:remark_font_color>/<int:remark_font_size>/<int:remark_pos_x>/<int:remark_pos_y>/<str:remark_border_status>/<int:remark_border_size>/<int:remark_border_color>', SetAllRemark, name="set_all_remark"),
    path('backend/date/<str:username>/<int:huay_id>/<str:date_font>/<str:date_font_color>/<int:date_font_size>/<int:date_pos_x>/<int:date_pos_y>/<str:date_border_status>/<int:date_border_size>/<int:date_border_color>', SetAllDate, name="set_all_date"),
    path('backend/image/<str:username>/<int:huay_id>/<str:image_house>',
         SetAllImage, name="set_all_image"),



]
