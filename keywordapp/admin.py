from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(MainKeywordModel)
admin.site.register(SubKeywordModel)
admin.site.register(LongTailSubKeywordModel)
admin.site.register(LongTailKeywordModel)
admin.site.register(PageListModel)
admin.site.register(ProfileModel)
admin.site.register(PageListMetaDescriptionModel)
admin.site.register(ResetPasswordToken)
admin.site.register(ArticlePageModel)
admin.site.register(TagModel)
admin.site.register(FooterKeywordModel)
admin.site.register(LongTailFooterKeywordModel)
admin.site.register(SubFooterKeywordModel)
admin.site.register(LongTailSubFooterKeywordModel)
admin.site.register(TempKeywordSearchModel)
admin.site.register(CrudUser)
