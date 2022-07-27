from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

# AUTHENTICATION SECTION #
# Check user session
class UserAttributes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_session_key = models.CharField(blank=True, null=True, max_length=40)


# Profile
class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usertype = models.CharField(default='member', max_length=255)
    status = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    verified_token = models.CharField(max_length=100, default='no token')
    expire_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.first_name


class ResetPasswordToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField(default='no token')

    def __str__(self):
        return self.user.username

# Web list
class WebListModel(models.Model):
    website_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    
# Page list
class PageListModel(models.Model):
    page_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    website_list = models.ForeignKey(WebListModel, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.page_name

# Main keyword
class MainKeywordModel(models.Model):
    keyword_name = models.CharField(max_length=255)
    header = models.CharField(max_length=255, null=True, blank=True)
    page_list = models.ForeignKey(PageListModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.keyword_name


class LongTailKeywordModel(models.Model):
    longtail_name = models.TextField(null=True, blank=True)
    shorten_name = models.TextField(null=True, blank=True)
    link_href = models.TextField(null=True, blank=True)
    link_href_shorten_name = models.TextField(null=True, blank=True)
    main_keyword = models.ForeignKey(
        MainKeywordModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.longtail_name


class SubKeywordModel(models.Model):
    keyword_name = models.CharField(max_length=255)
    header = models.CharField(max_length=255, null=True, blank=True)
    main_keyword = models.ForeignKey(
        MainKeywordModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.keyword_name


class LongTailSubKeywordModel(models.Model):
    longtail_name = models.TextField(null=True, blank=True)
    shorten_name = models.TextField(null=True, blank=True)
    link_href = models.TextField(null=True, blank=True)
    link_href_shorten_name = models.TextField(null=True, blank=True)
    sub_keyword = models.ForeignKey(
        SubKeywordModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.longtail_name

# ================================================================= START : FOOTER =================================================================
# ================================================================= START : FOOTER =================================================================
# ================================================================= START : FOOTER =================================================================

class FooterKeywordModel(models.Model):
    keyword_name = models.CharField(max_length=255)
    header = models.CharField(max_length=255, null=True, blank=True)
    page_list = models.ForeignKey(PageListModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.keyword_name

class LongTailFooterKeywordModel(models.Model):
    longtail_name = models.TextField(null=True, blank=True)
    shorten_name = models.TextField(null=True, blank=True)
    link_href = models.TextField(null=True, blank=True)
    link_href_shorten_name = models.TextField(null=True, blank=True)
    footer_keyword = models.ForeignKey(
        FooterKeywordModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.longtail_name

# Footer Keyword Model
class SubFooterKeywordModel(models.Model):
    keyword_name = models.CharField(max_length=255)
    header = models.CharField(max_length=255, null=True, blank=True)
    footer_keyword = models.ForeignKey(FooterKeywordModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.keyword_name

class LongTailSubFooterKeywordModel(models.Model):
    longtail_name = models.TextField(null=True, blank=True)
    shorten_name = models.TextField(null=True, blank=True)
    link_href = models.TextField(null=True, blank=True)
    link_href_shorten_name = models.TextField(null=True, blank=True)
    sub_footer_keyword = models.ForeignKey(
        SubFooterKeywordModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.longtail_name

# ================================================================= END : FOOTER =================================================================
# ================================================================= END : FOOTER =================================================================
# ================================================================= END : FOOTER =================================================================

# Page
class PageListMetaDescriptionModel(models.Model):
    full_keyword = models.TextField(null=True, blank=True)
    shorten_keyword = models.TextField(null=True, blank=True)
    page_list = models.ForeignKey(PageListModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_keyword

# Article Tag
class TagModel(models.Model):
    tag_name = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.tag_name

class ArticlePageModel(models.Model):
    article_title = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=255,null=True, blank=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    image_link = models.FileField(null=True, blank=True)
    image_alt = models.TextField(null=True, blank=True)
    tag = models.ManyToManyField(TagModel)
    
    def __str__(self):
        return self.article_title

class CrudUser(models.Model):
    name = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(blank=True, null=True)

    
# ================================================================= START : TEMP KEYWORD SEARCH DATA =================================================================
# ================================================================= START : TEMP KEYWORD SEARCH DATA =================================================================
# ================================================================= START : TEMP KEYWORD SEARCH DATA =================================================================

class TempKeywordSearchModel(models.Model):
    keyword_search = models.CharField(max_length=255, blank=True,null=True)
    refine_popular = models.TextField(blank=True, null=True)
    longtail = models.TextField(blank=True, null=True)
    related = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True,default='keyword_search')
    def __str__(self):
        return self.keyword_search

# ================================================================= END : TEMP KEYWORD SEARCH DATA =================================================================
# ================================================================= END : TEMP KEYWORD SEARCH DATA =================================================================
# ================================================================= END : TEMP KEYWORD SEARCH DATA =================================================================


    
# ================================================================= START : COUNT WORD =================================================================
# ================================================================= START : COUNT WORD =================================================================
# ================================================================= START : COUNT WORD =================================================================

        
class CountKeywordModelInAllPage(models.Model):
    keyword_name = models.CharField(max_length=255, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    page_list = models.ForeignKey(PageListModel, on_delete=models.CASCADE,default=2)
    
    def __str__(self):
        return self.keyword_name

# ================================================================= END : COUNT WORD =================================================================
# ================================================================= END : COUNT WORD =================================================================
# ================================================================= END : COUNT WORD =================================================================
