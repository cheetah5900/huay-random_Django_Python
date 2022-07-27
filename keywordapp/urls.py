from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name='Home'),
    #     path('verified-email/<str:token>/',
    #          VerifiedEmail, name='verified-email-page'),
    #     path('reset-password-request/', RequestToResetPassword,
    #          name='request-reset-password-page'),
    #     path('reset-password-new/<str:token>', ResetPassword, name='reset-password-page'),

    path('permission-definition/', PermissionDefinition,
         name='permission-definition-page'),
    path('permission-definition-edit/<int:uid>/',
         PermissionDefinitionEdit, name='permission-definition-edit-page'),


    # =============== REGISTER
    path('register/', Register, name='register-page'),
    
    # =============== WEB LIST
    path('weblist/', WebList, name='weblist-page'),
    path('weblist-edit/<int:wid>', WebListEdit, name='weblist-edit'),
    path('weblist-delete/<int:wid>', WebListDelete, name='weblist-delete'),

    # =============== PAGE LIST
    path('pagelist/<int:wid>', PageList, name='pagelist-page'),
    path('pagelist-edit/<int:pid>', PageListEdit, name='pagelist-edit'),
    path('pagelist-delete/<int:pid>', PageListDelete, name='pagelist-delete'),

    path('pagelist-meta/<int:pid>', PageListMetaDescription,
         name='pagelist-meta-page'),
    path('pagelist-meta-edit/<int:pid>/<int:metaid>',
         PageListMetaDescriptionEdit, name='pagelist-meta-edit-page'),
    path('pagelist-meta-del/<int:pid>/<int:metaid>',
         PageListMetaDescriptionDelete, name='pagelist-meta-del-page'),

    path('header/<int:pid>', MainKeyword, name='page-header-page'),
    path('header-edit/<int:pid>/<int:m_kwid>',
         MainKeywordEdit, name='page-header-edit-page'),
    path('header-del/<int:pid>/<int:m_kwid>',
         MainKeywordDelete, name='page-header-del-page'),

    path('sub-header-edit/<int:pid>/<int:m_kwid>/<int:s_kwid>',
         SubKeywordEdit, name='page-sub-header-edit-page'),
    path('sub-header-del/<int:pid>/<int:s_kwid>',
         SubKeywordDelete, name='page-sub-header-del-page'),

    path('longtail-mainkeyword/<int:pid>/<int:m_kwid>',
         LongTailKeyword, name='longtail-mainkeyword-page'),
    path('longtail-mainkeyword-edit/<int:pid>/<int:m_kwid>/<int:lt_kwid>',
         LongTailKeywordEdit, name='longtail-mainkeyword-edit-page'),
    path('longtail-mainkeyword-del/<int:pid>/<int:m_kwid>/<int:lt_kwid>',
         LongTailKeywordDelete, name='longtail-mainkeyword-del-page'),


    path('longtail-subkeyword/<int:pid>/<int:s_kwid>',
         LongTailSubKeyword, name='longtail-subkeyword-page'),
    path('longtail-subkeyword-edit/<int:pid>/<int:s_kwid>/<int:lts_kwid>',
         LongTailSubKeywordEdit, name='longtail-subkeyword-edit-page'),
    path('longtail-subkeyword-del/<int:pid>/<int:s_kwid>/<int:lts_kwid>',
         LongTailSubKeywordDelete, name='longtail-subkeyword-del-page'),


    # =============== KEYWORD SEARCH
    path('keyword-search/',
         KeywordSearch, name='keyword-search-page'),

    # =============== PAGE DETAIL
    path('page-detail/<int:pid>',
         PageDetail, name='page-detail-page'),

    path('apply-short-keyword',
         ApplyShortUniqueToShortKeyword, name='apply-short-keyword-page'),

    # =============== POST PAGE
    path('post-page',
         PostManager, name='post-page'),

    # =============== PAGE FOOTER =================================================================
    path('footer-page/<int:pid>',
         PageListFooter, name='page-footer-page'),
    path('footer-page-edit/<int:pid>/<int:fid>',
         PageListFooterEdit, name='page-footer-edit-page'),
    path('footer-page-delete/<int:pid>/<int:fid>',
         PageListFooterDelete, name='page-footer-delete-page'),
    path('longtail-footer/<int:pid>/<int:f_kwid>',
         LongTailFooterKeyword, name='longtail-footer-page'),
    path('longtail-footer-edit/<int:pid>/<int:f_kwid>/<int:lt_kwid>',
         LongTailFooterKeywordEdit, name='longtail-footer-edit-page'),
    path('longtail-footer-del/<int:pid>/<int:f_kwid>/<int:lt_kwid>',
         LongTailFooterKeywordDelete, name='longtail-footer-del-page'),

         
    # =============== PAGE SUB FOOTER =================================================================
    path('sub-footer-page-edit/<int:pid>/<int:f_kwid>/<int:sf_kwid>',
         PageListSubFooterEdit, name='page-sub-footer-edit-page'),
    path('sub-footer-page-delete/<int:pid>/<int:sf_kwid>',
         PageListSubFooterDelete, name='page-sub-footer-del-page'),
    path('longtail-sub-footer/<int:pid>/<int:sf_kwid>',
         LongTailSubFooterKeyword, name='longtail-sub-footer-page'),
    path('longtail-sub-footer-edit/<int:pid>/<int:sf_kwid>/<int:ltsf_kwid>',
         LongTailSubFooterKeywordEdit, name='longtail-sub-footer-edit-page'),
    path('longtail-sub-footer-del/<int:pid>/<int:sf_kwid>/<int:ltsf_kwid>',
         LongTailSubFooterKeywordDelete, name='longtail-sub-footer-del-page'),


    # =============== BUCK ADD COUNT KEYWORD TO TABLE
#     path('import-keyword', ImportKeywordInAllLongtailToCountKeywordTable),
    

    # =============== ARTICLE POST
    path('article-post/<int:aid>', ArticlePost, name="article-post-page"),

    # =============== CRUD AJAX
    path('crud/page-list',  PageListCrud, name='crud-pagelist-page'),
    path('crud/<int:pid>',  CrudView, name='crud-page'),
    path('crud/page-list/create',  CreateCrudPageList.as_view(), name='ajax_page_list_create'),
    path('crud/meta-des/create',  CreateCrudMetaDescription.as_view(), name='ajax_meta_des_create'),
    path('crud/meta-des/update',  UpdateCrudMetaDescription.as_view(), name='ajax_meta_des_update'),
    path('crud/meta-des/delete',  DeleteCrudMetaDescription.as_view(), name='ajax_meta_des_delete'),
    path('crud/meta-des/shorten_kw',  ShortenKwCrudMetaDescription.as_view(), name='ajax_meta_des_shorten_kw'),
    path('ajax/crud/create/',  CreateCrudUser.as_view(), name='crud_ajax_create'),
    path('ajax/crud/update/',  UpdateCrudUser.as_view(), name='crud_ajax_update'),
    path('ajax/crud/delete/',  DeleteCrudUser.as_view(), name='crud_ajax_delete'),

]
