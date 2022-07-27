
# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================
# =============================== FOR PAGE KEYWORD MANAGER ===============================

from datetime import datetime
from itertools import count
# from textwrap import shorten
# from xml.etree.ElementTree import SubElement
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from uuid import uuid1


from .sendemail import sendthai  # send gmail
# require login to enter function
from django.contrib.auth.decorators import login_required
# import model
from .models import *
# ให้สามารถเก็บไฟล์ได้
from django.core.files.storage import FileSystemStorage
# AJAX เขียนแบบ Class-Based
from django.views.generic import ListView, View  # ให้ใช้ ListView ได้
from django.http import JsonResponse
from collections import Counter  # เอาไว้นับจำนวนคำใน list


# =============================== FOR SELENIUM GET DATA ===============================
# =============================== FOR SELENIUM GET DATA ===============================
# =============================== FOR SELENIUM GET DATA ===============================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
# To setting mobile device broswer
from selenium.webdriver.chrome.options import Options

import pandas as pd

# =============================== AUTHENTICATION ===============================
# =============================== AUTHENTICATION ===============================
# =============================== AUTHENTICATION ===============================


def Login(request):
    context = {}
    if request.method == 'POST':
        data = request.POST.copy()
        getUsername = data.get('username')
        getPassword = data.get('password')
        # authen is function for User model for finding user
        user = authenticate(
            username=getUsername, password=getPassword)

        # if user is not empty
        if user is not None:
            login(request, user)
            userId = request.user.id
            currectSessionKey = request.session.session_key
            # Check does this user has any session
            # find object user
            userObject = User.objects.get(id=userId)
            try:
                # get old data from User Attribute to know which session is old session
                userAttributeObject = UserAttributes.objects.get(
                    user=userObject)
                lastSessionKey = userAttributeObject.last_session_key
                # delete old session
                sessionObject = Session.objects.get(session_key=lastSessionKey)
                sessionObject.delete()
            except:
                pass
            # check does this user has any session in UserAttributes
            try:
                # update user attribute
                updateUserAttribute = UserAttributes.objects.get(
                    user=userObject)
                updateUserAttribute.user = userObject
                updateUserAttribute.last_session_key = currectSessionKey
                updateUserAttribute.save()
            except:
                # add new user attribute
                userAttributes = UserAttributes()
                userAttributes.user = userObject
                userAttributes.last_session_key = currectSessionKey
                userAttributes.save()
            return redirect('Home')
        else:
            context['message'] = 'ชื่อหรือรหัสผ่านไม่ถูกต้อง'
            return render(request, 'keywordapp/login.html', context)

    return render(request, 'keywordapp/login.html', context)


def Register(request):
    context = {}
    if request.method == 'POST':
        data = request.POST.copy()
        firstName = data.get('firstname')
        firstName = firstName.strip()
        lastName = data.get('lastname')
        lastName = lastName.strip()
        username = data.get('email')
        username = username.strip()
        password = data.get('password')
        password2 = data.get('password2')

        # check confirm password
        if password != password2:
            context['error'] = "รหัสไม่ตรงกัน"
            return render(request, 'keywordapp/register.html', context)

        # check is username duplicate
        try:
            User.objects.get(username=username)
            context['error'] = 'มีอีเมล์นี้ในระบบแล้ว'
        except:
            newUser = User()
            newUser.username = username
            newUser.first_name = firstName
            newUser.last_name = lastName
            newUser.set_password(password)
            newUser.save()

            uuid = uuid1()
            uuidToken = str(uuid)

            newProfile = ProfileModel()
            newProfile.user = User.objects.get(username=username)
            newProfile.verified_token = uuidToken
            newProfile.save()

            # text = 'กรุณากดที่ลิงค์นี้เพื่อยืนยันอีเมล์\n\n https://keywordsearch.in.ngrok.io/verified-email/'+uuidToken
            # sendthai(username, 'ยืนยันการสมัคร เครื่องมือ SEO', text)
            # context['info'] = 'สมัครสมาชิกแล้ว กรุณายืนยันอีเมล์ เพื่อใช้งาน หากหาอีเมล์ไม่เจอ ลองตรวจสอบในเมล์ขยะ'
            context['info'] = 'สมัครสมาชิกแล้ว ล็อคอินเพื่อสั่งซื้อ และใช้งานได้ทันที'
    return render(request, 'keywordapp/register.html', context)


# def VerifiedEmail(request, token):
#     context = {}
#     try:
#         # check does this token in database or not
#         checkLink = ProfileModel.objects.get(verified_token=token)
#         checkLink.verified = True
#         checkLink.save()
#         context['success'] = 'ยืนยันอีเมล์สำเร็จแล้ว สามารถล็อคอินเข้าใช้งานระบบได้ทันที'
#     except:
#         context['error'] = 'ไม่พบลิงค์ดังกล่าว กรุณากดลิงค์มาใหม่ หรือติดต่อผู้ดูแลระบบ'
#     return render(request, 'keywordapp/verified-email.html', context)


# def RequestToResetPassword(request):
#     context = {}
#     if request.method == 'POST':
#         data = request.POST.copy()
#         email = data.get('email')
#         email = email.strip()
#         # check, does this email has in database
#         try:
#             checkEmail = User.objects.get(username=email)
#             uuid = uuid1()
#             uuidToken = str(uuid)

#             requestResetPassword = ResetPasswordToken()
#             requestResetPassword.user = User.objects.get(username=email)
#             requestResetPassword.token = uuidToken
#             requestResetPassword.save()

#             text = 'กรุณากดที่ลิงค์นี้เพื่อรีเซ็ตรหัสผ่าน\n\n https://keywordsearch.in.ngrok.io/reset-password-new/'+uuidToken
#             # send reset password's link
#             sendthai(email, 'รีเซ็ตรหัสผ่าน เครื่องมือ SEO', text)
#         except:
#             context['error'] = 'ไม่พบ E-mail ดังกล่าวในระบบ กรุณาตรวจสอบ E-mail อีกครั้ง'
#     return render(request, 'keywordapp/reset-password-request.html', context)


# def ResetPassword(request, token):

#     context = {}
#     # check does in database have this token
#     try:
#         checkToken = ResetPasswordToken.objects.get(token=token)
#         if request.method == 'POST':
#             data = request.POST.copy()
#             password = data.get('password')
#             password2 = data.get('password2')

#             if password != password2:
#                 context['error'] = 'รหัสผ่านทั้งสองช่องไม่ตรงกัน กรุณากรอกใหม่'
#             else:
#                 updateUserPassword = checkToken.user  # object user model
#                 updateUserPassword.set_password(password)
#                 updateUserPassword.save()
#                 # login
#                 user = authenticate(
#                     username=updateUserPassword.username, password=password)
#                 login(request, user)
#                 # Delete used token from db
#                 checkToken.delete()
#                 return redirect('Home')
#     except:
#         context['error'] = 'ขออภัย ไม่พบลิงค์ดังกล่าว กรุณาตรวจสอบลิงค์ หรือติดต่อผู้ดูแลระบบ'
#     return render(request, 'keywordapp/reset-password-new.html', context)


@login_required
def PermissionDefinition(request):

    # if have no permission cannot enter this page
    checkPermission = CheckRootUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    context = {}
    userData = User.objects.all()
    context['userData'] = userData
    context['navpage'] = 'permission'
    return render(request, 'keywordapp/permission-definition.html', context)


@login_required
def PermissionDefinitionEdit(request, uid):
    # if have no permission cannot enter this page
    checkPermission = CheckRootUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    context = {}
    # User object
    userObject = User.objects.get(
        id=uid)
    # Edit data
    editData = ProfileModel.objects.get(
        user=userObject)

    # Update data
    if request.method == 'POST':
        data = request.POST.copy()
        userType = data.get('usertype')
        status = data.get('status')
        verified = data.get('verified')
        expireDate = data.get('expire_date')
        expireTime = data.get('expire_time')

        #  change status and verified value from "on" to "True"
        if status == 'on':
            status = True
        if verified == 'on':
            verified = True

        editData.user = userObject
        editData.usertype = userType
        editData.status = status
        editData.verified = verified
        editData.expire_date = expireDate + ' ' + expireTime
        editData.save()

        request.session['status'] = 'แก้ไขสำเร็จแล้ว'
        return redirect('permission-definition-page')

    context['editData'] = editData
    context['userId'] = uid
    context['navpage'] = 'keyword-manager'

    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''  # clear stuck error in session

    return render(request, 'keywordapp/permission-definition-edit.html', context)


def CheckExpireDate(expireDate, uid):
    try:
        expireDateNewFormat = expireDate.strftime("%Y%m%d%H%M")
        timeNow = datetime.now()
        currentTime = timeNow.strftime("%Y%m%d%H%M")
        if currentTime >= expireDateNewFormat:
            userObject = User.objects.get(id=uid)
            profileObject = ProfileModel.objects.get(user=userObject)
            profileObject.usertype = 'member'
            profileObject.expire_date = None
            profileObject.save()
            return "ตัดสิทธิ์แล้ว"
        if currentTime < expireDateNewFormat:
            pass
    except:
        pass

# =============================== GENERAL FUNCTION ===============================
# =============================== GENERAL FUNCTION ===============================
# =============================== GENERAL FUNCTION ===============================


@login_required
def Home(request):
    context = {}
    try:
        day = request.user.profilemodel.expire_date.strftime("%d")
        month = request.user.profilemodel.expire_date.strftime("%m")
        year = int(request.user.profilemodel.expire_date.strftime("%Y")) + 543
        hour = request.user.profilemodel.expire_date.strftime("%H")
        minute = request.user.profilemodel.expire_date.strftime("%M")

        thaiMonth = ConvertToThaiMonth(month)
        context['expireDate'] = "{} {} {} เวลา {}:{} น.".format(
            day, thaiMonth, year, hour, minute)
    except:
        pass
    return render(request, 'keywordapp/home.html', context)
# Delete duplicate


def DeleteDuplicateFromGettingDataInDb(list, attribute):
    uniqueDataList = []
    uniqueDataList2WordExceedList = []
    # Remove Duplicate word
    for data in list:
        # Cut duplicate word by space bar
        if attribute == "full_keyword":
            dataSplit = data.full_keyword.split()
        elif attribute == "longtail_name":
            dataSplit = data.longtail_name.split()
        # get separated keyword to check
        for word in dataSplit:
            # if not in unique will append
            if word not in uniqueDataList:
                uniqueDataList.append(word)
                uniqueDataList2WordExceedList.append(word)
            else:
                # loop unique to check that is it exceed 2 of each keyword
                count = uniqueDataList2WordExceedList.count(word)
                if count < 2:
                    uniqueDataList2WordExceedList.append(word)

    uniqueDataListToString = ' '.join(uniqueDataList)
    uniqueDataListToString2WordExceed = ' '.join(uniqueDataList2WordExceedList)
    NumberOfUniqueDataListToString = len(uniqueDataListToString)
    NumberOfUniqueDataListToString2WordExceed = len(
        uniqueDataListToString2WordExceed)

    result = [uniqueDataList, uniqueDataList2WordExceedList,
              NumberOfUniqueDataListToString, NumberOfUniqueDataListToString2WordExceed]
    return result


def DeleteDuplicateFromTableResultList(list1, list2, list3):
    uniqueDataList = []
    # Remove Duplicate word
    for data in list1:
        # Cut duplicate word by space bar
        dataSplit = data.split()
        for x in dataSplit:
            if x not in uniqueDataList:
                uniqueDataList.append(x)
    # Remove Duplicate word
    for data in list2:
        # Cut duplicate word by space bar
        dataSplit = data.split()
        for x in dataSplit:
            if x not in uniqueDataList:
                uniqueDataList.append(x)
    # Remove Duplicate word
    for data in list3:
        # Cut duplicate word by space bar
        dataSplit = data.split()
        for x in dataSplit:
            if x not in uniqueDataList:
                uniqueDataList.append(x)
    return uniqueDataList

# Count character length


def CountCharacterLength(list, attribute):
    # empty length for count
    keywordAmount = 0
    sumLength = 0
    countFull = 0
    # loop each object
    for countLength in list:
        # check amount of characters of full_keyword
        if attribute == "full_keyword":
            countFull = len(countLength.full_keyword)
        elif attribute == 'shorten_keyword':
            countFull = len(countLength.shorten_keyword)
        elif attribute == 'longtail_name':
            countFull = len(countLength.longtail_name)
        elif attribute == 'shorten_name':
            countFull = len(countLength.shorten_name)
        elif attribute == 'keyword':
            countFull = len(countLength.keyword)

        # plus each time
        sumLength = sumLength + countFull
        keywordAmount = keywordAmount + 1
    result = sumLength + keywordAmount - 1
    if result == -1:
        result = 0
    return result

# Apply short data to short keyword


def ApplyShortUniqueToShortKeyword(request):
    if request.method == 'POST':
        data = request.POST.copy()
        pageId = data.get('page_id')
        keywordId = data.get('keyword_id')
        addMode = data.get('add_mode')
        comeFrom = data.get('come_from')
        # If come from mata description will filter by page id
        if comeFrom == 'meta description':
            filterListData = PageListMetaDescriptionModel.objects.filter(
                page_list_id=pageId)
        elif comeFrom == 'main keyword paragraph':
            filterListData = LongTailKeywordModel.objects.filter(
                main_keyword_id=keywordId)
        elif comeFrom == 'sub keyword paragraph':
            filterListData = LongTailSubKeywordModel.objects.filter(
                sub_keyword_id=keywordId)
        elif comeFrom == 'footer keyword paragraph':
            filterListData = LongTailFooterKeywordModel.objects.filter(
                footer_keyword_id=keywordId)
        elif comeFrom == 'sub footer keyword paragraph':
            filterListData = LongTailSubFooterKeywordModel.objects.filter(
                sub_footer_keyword_id=keywordId)

        uniqueDataList = []
        uniqueData2WordExceedList = []
        for data in filterListData:
            # เอาคำที่ไม่ซ้ำของแต่ละ shorten keyword มารวมกันเพื่อเอาไปอัพเดท
            newShortenKeywordList = []
            newShortenKeyword2WordExceedList = []
            # set remain keyword to remove from to shorten
            # Remove Duplicate word
            # Cut duplicate word by space bar
            if comeFrom == 'meta description':
                fullKeyword = data.full_keyword.split()
                OldShortKeyword = data.shorten_keyword
            elif comeFrom == 'main keyword paragraph' or comeFrom == 'sub keyword paragraph' or comeFrom == 'footer keyword paragraph' or comeFrom == 'sub footer keyword paragraph':
                fullKeyword = data.longtail_name.split()
                OldShortKeyword = data.shorten_name

            # get separated keyword to check
            for word in fullKeyword:
                # if not in unique will append
                if word not in uniqueDataList:
                    uniqueDataList.append(word)
                    newShortenKeywordList.append(word)
                    uniqueData2WordExceedList.append(word)
                    newShortenKeyword2WordExceedList.append(word)
                else:
                    # loop unique to check that is it exceed 2 of each keyword
                    count = uniqueData2WordExceedList.count(word)
                    if count < 2:
                        uniqueData2WordExceedList.append(word)
                        newShortenKeyword2WordExceedList.append(word)
            # check mode to use delete function
            if addMode == "not duplicate":
                newShortenKeywordListToString = ' '.join(newShortenKeywordList)
            elif addMode == "not duplicate exceed 2":
                newShortenKeywordListToString = ' '.join(
                    newShortenKeyword2WordExceedList)

            if OldShortKeyword != newShortenKeywordListToString:
                # reduce amount of the old one
                AdjustCountKeyToDb(OldShortKeyword, 'minus', 1, pageId)
                # increase amount of the new one
                AdjustCountKeyToDb(
                    newShortenKeywordListToString, 'plus', 1, pageId)

            # add data back to db
            if comeFrom == 'meta description':
                addData = PageListMetaDescriptionModel.objects.get(id=data.id)
                addData.shorten_keyword = newShortenKeywordListToString
                addData.save()
            elif comeFrom == 'main keyword paragraph':
                addData = LongTailKeywordModel.objects.get(id=data.id)
                addData.shorten_name = newShortenKeywordListToString
                addData.save()
            elif comeFrom == 'sub keyword paragraph':
                addData = LongTailSubKeywordModel.objects.get(id=data.id)
                addData.shorten_name = newShortenKeywordListToString
                addData.save()
            elif comeFrom == 'footer keyword paragraph':
                addData = LongTailFooterKeywordModel.objects.get(id=data.id)
                addData.shorten_name = newShortenKeywordListToString
                addData.save()
            elif comeFrom == 'sub footer keyword paragraph':
                addData = LongTailSubFooterKeywordModel.objects.get(id=data.id)
                addData.shorten_name = newShortenKeywordListToString
                addData.save()

    request.session['status'] = 'ใช้ชุดคำสำเร็จแล้ว'
    if comeFrom == 'meta description':
        return redirect('pagelist-meta-page', pageId)
    elif comeFrom == 'main keyword paragraph':
        return redirect('longtail-mainkeyword-page', pageId, keywordId)
    elif comeFrom == 'sub keyword paragraph':
        return redirect('longtail-subkeyword-page', pageId, keywordId)
    elif comeFrom == 'footer keyword paragraph':
        return redirect('longtail-footer-page', pageId, keywordId)
    elif comeFrom == 'sub footer keyword paragraph':
        return redirect('longtail-sub-footer-page', pageId, keywordId)


def ConvertToThaiMonth(month):
    if month == '01':
        thaiMonth = 'มกราคม'
    elif month == '02':
        thaiMonth = 'กุมภาพันธ์'
    elif month == '03':
        thaiMonth = 'มีนาคม'
    elif month == '04':
        thaiMonth = 'เมษายน'
    elif month == '05':
        thaiMonth = 'พฤษภาคม'
    elif month == '06':
        thaiMonth = 'มิถุนายน'
    elif month == '07':
        thaiMonth = 'กรกฎาคม'
    elif month == '08':
        thaiMonth = 'สิงหาคม'
    elif month == '09':
        thaiMonth = 'กันยายน'
    elif month == '10':
        thaiMonth = 'ตุลาคม'
    elif month == '11':
        thaiMonth = 'พฤศจิกายน'
    elif month == '12':
        thaiMonth = 'ธันวาคม'
    return thaiMonth


def CheckPremiumUser(request):
    # if request.user.id is TRUE can do following
    if request.user.id:
        allowUser = ['premium', 'prime', 'root']
        if request.user.profilemodel.usertype in allowUser:
            result = 'Have permission'
        else:
            result = 'Have no permission'
    return result


def CheckSuperPremiumUser(request):
    # if request.user.id is TRUE can do following
    if request.user.id:
        allowUser = ['prime', 'root']
        if request.user.profilemodel.usertype in allowUser:
            result = 'Have permission'
        else:
            result = 'Have no permission'
    return result


def CheckRootUser(request):
    # if request.user.id is TRUE can do following
    if request.user.id:
        allowUser = ['root']
        if request.user.profilemodel.usertype in allowUser:
            result = 'Have permission'
        else:
            result = 'Have no permission'
    return result


def CheckDuplicatedMetaDescription(full_keyword, pid):
    # check from LongTailKeywordModel
    oldMetaData = PageListMetaDescriptionModel.objects.filter(
        page_list_id=pid)
    # set default value
    checkDuplicated = "not duplicated"
    for data in oldMetaData:
        # if longtail keyword of that page in DB equal keyword input will error
        fullKeyword = data.full_keyword
        if fullKeyword == full_keyword:
            checkDuplicated = "duplicated"
    return checkDuplicated


def CheckDuplicatedLongtailKeyword(full_keyword, m_kwid):
    # check from LongTailKeywordModel
    oldLongtailData = LongTailKeywordModel.objects.filter(
        main_keyword_id=m_kwid)
    # set default value
    checkDuplicated = "not duplicated"
    for data in oldLongtailData:
        # if longtail keyword of that page in DB equal full keyword input will error
        longtailName = data.longtail_name
        if longtailName == full_keyword:
            checkDuplicated = "duplicated"
    return checkDuplicated


def CheckDuplicatedSubLongtailKeyword(full_keyword, s_kwid):
    # check from LongTailKeywordModel
    oldLongtailData = LongTailSubKeywordModel.objects.filter(
        sub_keyword=s_kwid)
    # set default value
    checkDuplicated = "not duplicated"
    for data in oldLongtailData:
        # if longtail keyword of that page in DB equal full keyword input will error
        longtailName = data.longtail_name
        if longtailName == full_keyword:
            checkDuplicated = "duplicated"
    return checkDuplicated


def CheckDuplicatedFooterLongtailKeyword(full_keyword, f_kwid):
    # check from LongTailKeywordModel
    oldLongtailData = LongTailFooterKeywordModel.objects.filter(
        footer_keyword_id=f_kwid)
    # set default value
    checkDuplicated = "not duplicated"
    for data in oldLongtailData:
        # if longtail keyword of that page in DB equal full keyword input will error
        longtailName = data.longtail_name
        if longtailName == full_keyword:
            checkDuplicated = "duplicated"
    return checkDuplicated


def CheckDuplicatedSubFooterLongtailKeyword(full_keyword, sf_kwid):
    # check from LongTailKeywordModel
    oldLongtailData = LongTailSubFooterKeywordModel.objects.filter(
        sub_footer_keyword_id=sf_kwid)
    # set default value
    checkDuplicated = "not duplicated"
    for data in oldLongtailData:
        # if longtail keyword of that page in DB equal full keyword input will error
        longtailName = data.longtail_name
        if longtailName == full_keyword:
            checkDuplicated = "duplicated"
    return checkDuplicated


def ConvertDataOfGoogleTableFromStringToList(refinePopularList, longtailList, refineAndReplatedList):

    # Converting string to list
    if refinePopularList != '[]' and refinePopularList != '':
        refinePopularListConverted = refinePopularList.replace(
            "'", "").replace("[", "").replace("]", "").split(', ')
    else:
        refinePopularListConverted = ''
    # Converting string to list
    if longtailList != '[]' and longtailList != '':
        longtailListConverted = longtailList.replace(
            "'", "").replace("[", "").replace("]", "").split(', ')
    else:
        longtailListConverted = ''
    if refineAndReplatedList != '[]' and refineAndReplatedList != '':
        # Converting string to list
        refineAndReplatedListConverted = refineAndReplatedList.replace(
            "'", "").replace("[", "").replace("]", "").split(', ')
    else:
        refineAndReplatedListConverted = ''
    return refinePopularListConverted, longtailListConverted, refineAndReplatedListConverted

# count keyword in every type and return number


def CountKeywordEveryType(keyword, pid):
    # === check keyword in db === #
    amount = 0
    try:
        ckwData = CountKeywordModelInAllPage.objects.get(
            keyword_name=keyword, page_list_id=pid)
        amount = amount + ckwData.amount
    except:
        pass
    return amount

# Add count key when add some keyword


def AddCountKeyToDb(keyword, amount, pid):
    try:
        updateCountKeywordInAllPage = CountKeywordModelInAllPage.objects.get(
            keyword_name=keyword, page_list_id=pid)
        updateCountKeywordInAllPage.amount = updateCountKeywordInAllPage.amount + amount
        updateCountKeywordInAllPage.save()
    except:
        newCountKeywordInAllPage = CountKeywordModelInAllPage()
        newCountKeywordInAllPage.keyword_name = keyword
        newCountKeywordInAllPage.amount = amount
        newCountKeywordInAllPage.page_list = PageListModel.objects.get(id=pid)
        newCountKeywordInAllPage.save()


# Adjust count key when add some keyword
def AdjustCountKeyToDb(keyword, method, amount, pid):
    # ปรับเพิ่ม / ลดจำนวนในตาราง count keyword in all page
    try:
        countKeywordInAllPage = CountKeywordModelInAllPage.objects.get(
            keyword_name=keyword, page_list_id=pid)
        if method == 'plus':
            print("keyword : {} plus amount : {} ".format(
                keyword, countKeywordInAllPage.amount))
            countKeywordInAllPage.amount = countKeywordInAllPage.amount + amount
            countKeywordInAllPage.save()
        elif method == 'minus':
            # if current amount is one, it will be decrease to 0. So after reduce amount we will delted it
            print("keyword : {} minus amount : {} ".format(
                keyword, countKeywordInAllPage.amount))
            if countKeywordInAllPage.amount <= 1:
                countKeywordInAllPage.delete()
            else:
                countKeywordInAllPage.amount = countKeywordInAllPage.amount - amount
                countKeywordInAllPage.save()
    except:
        AddCountKeyToDb(keyword, 1, pid)

# Manage key's amount for old and new data


def ManageCountKeyOnEdit(oldFullKw, oldShortKw, newFullKw, newShortKw, pid):
    # if old keyword is not equal to new keyword will re-count amount but if it not changed don't check it
    if oldFullKw != newFullKw:
        #  if old one equal new one means we need to adjust amount of countkeyword table
        # reduce amount of the old one
        AdjustCountKeyToDb(oldFullKw, 'minus', 1, pid)
    # increase amount of the new one
        AdjustCountKeyToDb(newFullKw, 'plus', 1, pid)
    if oldShortKw != newShortKw:
        #  if old one equal new one means we need to adjust amount of countkeyword table
        # reduce amount of the old one
        AdjustCountKeyToDb(oldShortKw, 'minus', 1, pid)
    # increase amount of the new one
        AdjustCountKeyToDb(newShortKw, 'plus', 1, pid)


def GetZipDataForLoopInTable(request, dataObject, comeFrom, loopMode, pid):

    # together variable
    keywordIdList = []
    fullKeywordList = []
    linkHrefFkwList = []
    linkHrefSkwList = []
    shortKeywordList = []
    #  === THIS PAGE ===#
    sumKeywordInThisPageFullKwList = []
    sumKeywordInThisPageShortKwList = []
    #  === ALL PAGE ===#
    sumAmountFkw = 0
    sumAmountAllPageFkw = 0
    sumAmountAllPageSkw = 0
    sumAmountAllPageFkwList = []
    sumAmountAllPageSkwList = []
    if loopMode == 'loop':
        for data in dataObject:
            # ================ ID Keyword ================ #
            keywordId = data.id
            keywordIdList.append(keywordId)
            # ================ COUNT KEYWORD IN THIS PAGE ================ #
            # ================ COUNT KEYWORD IN THIS PAGE ================ #
            # ================ COUNT KEYWORD IN THIS PAGE ================ #
            # ================ Full Keyword ================ #
            if comeFrom == 'meta description':
                fullKeyword = data.full_keyword
                shortKeyword = data.shorten_keyword
            elif comeFrom == 'paragraph of main keyword':
                fullKeyword = data.longtail_name
                shortKeyword = data.shorten_name
                linkHrefFkw = data.link_href
                linkHrefSkw = data.link_href_shorten_name
                linkHrefFkwList.append(linkHrefFkw)
                linkHrefSkwList.append(linkHrefSkw)
            fullKeywordList.append(fullKeyword)
            shortKeywordList.append(shortKeyword)
            # count fullKeyword
            # get data from function
            sumAmountInThisPageFullKw = CountKeywordEveryType(fullKeyword, pid)
            sumKeywordInThisPageFullKwList.append(sumAmountInThisPageFullKw)
            #  if full keyword same as short keyword don't count short keyword
            if fullKeyword == shortKeyword:
                sumKeywordInThisPageShortKwList.append(
                    sumAmountInThisPageFullKw)
            else:
                # ================ Short Keyword ================ #
                # count shortKeyword
                # get data from function
                sumAmountInThisPageShortKw = CountKeywordEveryType(
                    shortKeyword, pid)
                sumKeywordInThisPageShortKwList.append(
                    sumAmountInThisPageShortKw)

            # ================ COUNT KEYWORD IN ALL PAGE ================ #
            # ================ COUNT KEYWORD IN ALL PAGE ================ #
            # ================ COUNT KEYWORD IN ALL PAGE ================ #
            websiteId = GetWebListId(pid)
            websiteObject = WebListModel.objects.filter(id=websiteId)
            for webData in websiteObject:
                webDataId = webData.id
                # get page data by user
                pageObject = PageListModel.objects.filter(
                    website_list_id=webDataId)
                allAmountKeywordInDbFkw = 0
                allAmountKeywordInDbSkw = 0
                # use each page data to find keyword amount
                for pageData in pageObject:
                    pageId = pageData.id

                    # กรองตัวที่เงื่อนไขตรงออกมาก่อน
                    try:
                        getAllAmountFromFkw = CountKeywordModelInAllPage.objects.get(
                            keyword_name=fullKeyword, page_list_id=pageId)
                        allAmountKeywordInDbFkw = allAmountKeywordInDbFkw + getAllAmountFromFkw.amount
                    except:
                        pass

                    # กรองตัวที่เงื่อนไขตรงออกมาก่อน
                    try:
                        getAllAmountFromSkw = CountKeywordModelInAllPage.objects.get(
                            keyword_name=shortKeyword, page_list_id=pageId)
                        allAmountKeywordInDbSkw = allAmountKeywordInDbSkw + getAllAmountFromSkw.amount
                    except:
                        pass
                sumAmountAllPageFkwList.append(allAmountKeywordInDbFkw)
                sumAmountAllPageSkwList.append(allAmountKeywordInDbSkw)

    else:
        data = dataObject
        # ================ ID Keyword ================ #
        keywordId = data.id
        keywordIdList.append(keywordId)
        # ================ COUNT KEYWORD IN THIS PAGE ================ #
        # ================ COUNT KEYWORD IN THIS PAGE ================ #
        # ================ COUNT KEYWORD IN THIS PAGE ================ #
        # ================ Full Keyword ================ #
        if comeFrom == 'meta description':
            fullKeyword = data.full_keyword
            shortKeyword = data.shorten_keyword
        elif comeFrom == 'paragraph of main keyword':
            fullKeyword = data.longtail_name
            shortKeyword = data.shorten_name
            linkHrefFkw = data.link_href
            linkHrefSkw = data.link_href_shorten_name
            linkHrefFkwList.append(linkHrefFkw)
            linkHrefSkwList.append(linkHrefSkw)
        fullKeywordList.append(fullKeyword)
        shortKeywordList.append(shortKeyword)
        # count fullKeyword
        # get data from function
        sumAmountInThisPageFullKw = CountKeywordEveryType(fullKeyword, pid)
        sumKeywordInThisPageFullKwList.append(sumAmountInThisPageFullKw)

        #  if full keyword same as short keyword don't count short keyword
        if fullKeyword == shortKeyword:
            sumKeywordInThisPageShortKwList.append(sumAmountInThisPageFullKw)
        else:
            # ================ Short Keyword ================ #
            # count shortKeyword
            # get data from function
            sumAmountInThisPageShortKw = CountKeywordEveryType(
                shortKeyword, pid)
            sumKeywordInThisPageShortKwList.append(sumAmountInThisPageShortKw)

        # ================ COUNT KEYWORD IN ALL PAGE ================ #
        # ================ COUNT KEYWORD IN ALL PAGE ================ #
        # ================ COUNT KEYWORD IN ALL PAGE ================ #

        websiteId = GetWebListId(pid)
        websiteObject = WebListModel.objects.filter(id=websiteId)
        pageByUser = PageListModel.objects.filter(website_list_id=webDataId)
        # use each page data to find keyword amount
        # data is each page of this user
        for data in pageByUser:
            pageId = data.id
            # ================ Full Keyword ================ #
            sumAmountFkw = CountKeywordEveryType(fullKeyword, pageId)
            sumAmountAllPageFkw = sumAmountAllPageFkw + sumAmountFkw

            #  if full keyword same as short keyword don't count short keyword
            if fullKeyword == shortKeyword:
                sumAmountAllPageSkw = sumAmountAllPageSkw + sumAmountFkw
            else:
                # ================ Short Keyword ================ #
                sumAmountSkw = CountKeywordEveryType(shortKeyword, pageId)
                sumAmountAllPageSkw = sumAmountAllPageSkw + sumAmountSkw
        # เอาผลรวมไปยัดใส่ list เตรียมไป loop
        sumAmountAllPageFkwList.append(sumAmountAllPageFkw)
        sumAmountAllPageFkw = 0
        sumAmountAllPageSkwList.append(sumAmountAllPageSkw)
        sumAmountAllPageSkw = 0
    if comeFrom == 'meta description':
        result = zip(keywordIdList, fullKeywordList, sumKeywordInThisPageFullKwList, sumAmountAllPageFkwList,
                     shortKeywordList, sumKeywordInThisPageShortKwList, sumAmountAllPageSkwList)
    elif comeFrom == 'paragraph of main keyword':
        result = zip(keywordIdList, fullKeywordList, linkHrefFkwList, sumKeywordInThisPageFullKwList, sumAmountAllPageFkwList,
                     shortKeywordList, linkHrefSkwList, sumKeywordInThisPageShortKwList, sumAmountAllPageSkwList)
    return result

# Apply short data to short keyword


def ApplyShortUniqueToShortKeywordForCrud(pageId, keywordId, addMode, comeFrom):
    # If come from mata description will filter by page id
    if comeFrom == 'meta description':
        filterListData = PageListMetaDescriptionModel.objects.filter(
            page_list_id=pageId)
    elif comeFrom == 'main keyword paragraph':
        filterListData = LongTailKeywordModel.objects.filter(
            main_keyword_id=keywordId)
    elif comeFrom == 'sub keyword paragraph':
        filterListData = LongTailSubKeywordModel.objects.filter(
            sub_keyword_id=keywordId)
    elif comeFrom == 'footer keyword paragraph':
        filterListData = LongTailFooterKeywordModel.objects.filter(
            footer_keyword_id=keywordId)
    elif comeFrom == 'sub footer keyword paragraph':
        filterListData = LongTailSubFooterKeywordModel.objects.filter(
            sub_footer_keyword_id=keywordId)

    uniqueDataList = []
    uniqueData2WordExceedList = []
    for data in filterListData:
        # เอาคำที่ไม่ซ้ำของแต่ละ shorten keyword มารวมกันเพื่อเอาไปอัพเดท
        newShortenKeywordList = []
        newShortenKeyword2WordExceedList = []
        # set remain keyword to remove from to shorten
        # Remove Duplicate word
        # Cut duplicate word by space bar
        if comeFrom == 'meta description':
            fullKeyword = data.full_keyword.split()
        elif comeFrom == 'main keyword paragraph' or comeFrom == 'sub keyword paragraph' or comeFrom == 'footer keyword paragraph' or comeFrom == 'sub footer keyword paragraph':
            fullKeyword = data.longtail_name.split()

        # get separated keyword to check
        for word in fullKeyword:
            # if not in unique will append
            if word not in uniqueDataList:
                # append to itself to not check this word again
                uniqueDataList.append(word)
                # append first keyword into 2WordExceedList too because
                # there is no this keyword in uniqueList. so it must also doesn't have in 2WordExceed
                uniqueData2WordExceedList.append(word)
                # use this list to append for unique mode (not duplicate)
                newShortenKeywordList.append(word)
                # use this list to append for unique 2 exceed mode (duplicate not exceed 2)
                newShortenKeyword2WordExceedList.append(word)
            else:
                # loop unique to check that is it exceed 2 of each keyword
                count = uniqueData2WordExceedList.count(word)
                if count < 2:
                    uniqueData2WordExceedList.append(word)
                    newShortenKeyword2WordExceedList.append(word)
        #  add to db
        if addMode == "not duplicate":
            newShortenKeywordListToString = ' '.join(newShortenKeywordList)
        elif addMode == "not duplicate exceed 2":
            newShortenKeywordListToString = ' '.join(
                newShortenKeyword2WordExceedList)
        # add data back to db
        if comeFrom == 'meta description':
            addData = PageListMetaDescriptionModel.objects.get(id=data.id)
            addData.shorten_keyword = newShortenKeywordListToString
            addData.save()
        elif comeFrom == 'main keyword paragraph':
            addData = LongTailKeywordModel.objects.get(id=data.id)
            addData.shorten_name = newShortenKeywordListToString
            addData.save()
        elif comeFrom == 'sub keyword paragraph':
            addData = LongTailSubKeywordModel.objects.get(id=data.id)
            addData.shorten_name = newShortenKeywordListToString
            addData.save()
        elif comeFrom == 'footer keyword paragraph':
            addData = LongTailFooterKeywordModel.objects.get(id=data.id)
            addData.shorten_name = newShortenKeywordListToString
            addData.save()
        elif comeFrom == 'sub footer keyword paragraph':
            addData = LongTailSubFooterKeywordModel.objects.get(id=data.id)
            addData.shorten_name = newShortenKeywordListToString
            addData.save()


def GetWebListId(pid):
    pageObject = PageListModel.objects.get(id=pid)
    wid = pageObject.website_list.id
    return wid

# =============================== LONGTAIL KEYWORD ===============================
# =============================== LONGTAIL KEYWORD ===============================
# =============================== LONGTAIL KEYWORD ===============================


@login_required
def LongTailKeyword(request, pid, m_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    # define var
    uniqueDataList = ''
    countFullKwKey = ''
    countShortKwKey = ''

    # =============================================== START :PREPARE SET OF KEYWORDS ==============================
    # =============================================== START :PREPARE SET OF KEYWORDS ==============================
    # =============================================== START :PREPARE SET OF KEYWORDS ==============================
    try:
        tempKeywordData = TempKeywordSearchModel.objects.get(
            type='paragraph of main keyword')
        keywordSearch = tempKeywordData.keyword_search
        refinePopularList = tempKeywordData.refine_popular
        longtailList = tempKeywordData.longtail
        refineAndReplatedList = tempKeywordData.related
        # Convert data in table from string to list
        resultConvert = ConvertDataOfGoogleTableFromStringToList(
            refinePopularList, longtailList, refineAndReplatedList)
        refinePopularListConverted = resultConvert[0]
        longtailListConverted = resultConvert[1]
        refineAndReplatedListConverted = resultConvert[2]
    except:
        keywordSearch = ''
        refinePopularList = ''
        longtailList = ''
        refineAndReplatedList = ''
        refinePopularListConverted = ''
        longtailListConverted = ''
        refineAndReplatedListConverted = ''

    # =============================================== END :PREPARE SET OF KEYWORDS ==============================
    # =============================================== END :PREPARE SET OF KEYWORDS ==============================
    # =============================================== END :PREPARE SET OF KEYWORDS ==============================
    context = {}
    # Add data
    if request.method == 'POST':
        data = request.POST.copy()
        searchFrom = data.get('search_from')
        if searchFrom == 'paragraph':
            searchMode = data.get('search_mode')
            keywordSearch = data.get('keyword_search')
            if keywordSearch == '':
                request.session['error'] = 'กรุณากรอก Keyword'
                return redirect('longtail-mainkeyword-page', pid, m_kwid)
            keywordSearch = keywordSearch.strip()
            result = KeywordSearchFunction(request, keywordSearch, searchMode)
            # result to display in keyword search page
            # basic result
            refinePopularList = result[0]
            longtailList = result[1]
            refineAndReplatedList = result[2]
            uniqueDataList = result[9]

            try:
                # ลองหาว่ามีประเภทนี้หรือยัง ถ้ามีแล้วให้อัพเดท
                oldData = TempKeywordSearchModel.objects.get(
                    type='paragraph of main keyword')
                oldData.keyword_search = keywordSearch
                oldData.refine_popular = refinePopularList
                oldData.longtail = longtailList
                oldData.related = refineAndReplatedList
                oldData.save()
            except:
                # ถ้าไม่มีให้เพิ่มเข้าไปในระบบ
                newTempKeywordSearch = TempKeywordSearchModel()
                newTempKeywordSearch.keyword_search = keywordSearch
                newTempKeywordSearch.refine_popular = refinePopularList
                newTempKeywordSearch.longtail = longtailList
                newTempKeywordSearch.related = refineAndReplatedList
                newTempKeywordSearch.type = 'paragraph of main keyword'
                newTempKeywordSearch.save()

            if not refinePopularList and not longtailList and not refineAndReplatedList:
                request.session['title'] = 'หาไม่เจอ'
                request.session['alert'] = keywordSearch
                request.session['status_alert'] = 'error'
            else:
                request.session['title'] = 'เสร็จแล้ว'
                request.session['alert'] = keywordSearch
                request.session['status_alert'] = 'success'
            return redirect('longtail-mainkeyword-page', pid, m_kwid)
        else:
            #  if press button to re add will go in this condition
            if data.get('re_add') == 'True':
                fullLongtailKeyword = data.get('full_lt_keyword')
                fullLongtailKeyword = fullLongtailKeyword.strip()
                statusShow = 'เพิ่มคีย์ที่เลือกแล้ว'
            else:
                fullLongtailKeyword = data.get('full_lt_keyword')
                fullLongtailKeyword = fullLongtailKeyword.strip()
                statusShow = 'เพิ่มข้อมูลแล้ว'

            if fullLongtailKeyword == '':
                context['error'] = "กรุณากรอก Keyword"
            else:
                # check duplicate
                result = CheckDuplicatedLongtailKeyword(
                    fullLongtailKeyword, m_kwid)
                if result == 'duplicated':
                    request.session['error'] = 'มี Keyword นี้แล้ว'
                else:
                    newLTKeyword = LongTailKeywordModel()
                    newLTKeyword.longtail_name = fullLongtailKeyword
                    newLTKeyword.shorten_name = fullLongtailKeyword
                    newLTKeyword.link_href = ''
                    newLTKeyword.link_href_shorten_name = ''
                    newLTKeyword.main_keyword = MainKeywordModel.objects.get(
                        id=m_kwid)
                    newLTKeyword.save()

                    AddCountKeyToDb(fullLongtailKeyword, 2, pid)

                request.session['status'] = statusShow

                return redirect('longtail-mainkeyword-page', pid, m_kwid)

    # START: DATA FOR PAGE ================
    longtailKeywordModel = LongTailKeywordModel.objects.filter(
        main_keyword_id=m_kwid)

    keywordModel = MainKeywordModel.objects.get(id=m_kwid)

    attribute = "longtail_name"
    resultDeleteDuplicate = DeleteDuplicateFromGettingDataInDb(
        longtailKeywordModel, attribute)
    uniqueDataList = resultDeleteDuplicate[0]
    uniqueDataList2WordExceedList = resultDeleteDuplicate[1]
    numberOfUniqueDataListToString = resultDeleteDuplicate[2]
    numberOfUniqueDataListToString2WordExceed = resultDeleteDuplicate[3]

    # count all character
    attribute = "longtail_name"
    lengthFullKeyword = CountCharacterLength(longtailKeywordModel, attribute)
    attribute = "shorten_name"
    lengthShortKeyword = CountCharacterLength(longtailKeywordModel, attribute)

    # ================ END: DATA FOR PAGE ================

    # ================ START: KEYWORD HEALTH ================ #
    # FULL_KEYWORDS
    uniqueDataFullKwList = []
    for data in longtailKeywordModel:
        fullKeyword = data.longtail_name
        # Cut duplicate word by space bar
        fullKeywordSplit = fullKeyword.split()
        for x in fullKeywordSplit:
            uniqueDataFullKwList.append(x)
    counter = Counter(uniqueDataFullKwList).most_common()
    countFullKwKey = dict(counter)
    # SHORT_KEYWORDS
    uniqueDataShortKwList = []
    for data in longtailKeywordModel:
        shortKeyword = data.shorten_name
        # Cut duplicate word by space bar
        shortKeywordSplit = shortKeyword.split()
        for x in shortKeywordSplit:
            uniqueDataShortKwList.append(x)
    counter = Counter(uniqueDataShortKwList).most_common()
    countShortKwKey = dict(counter)
    # ================ END: KEYWORD HEALTH ================ #

    # ================ START : MAP DATA FOR TABLE ================ #
    comeFrom = 'paragraph of main keyword'
    loopMode = 'loop'
    zipDataForLoop = GetZipDataForLoopInTable(
        request, longtailKeywordModel, comeFrom, loopMode, pid)
    # ================ END : MAP DATA FOR TABLE ================ #

    # ================= START : DATA FOR GOOGLE TABLE ================= #
    try:
        tempKeywordData = TempKeywordSearchModel.objects.get(
            type='paragraph of main keyword')
        keywordSearch = tempKeywordData.keyword_search
        refinePopularList = tempKeywordData.refine_popular
        longtailList = tempKeywordData.longtail
        refineAndReplatedList = tempKeywordData.related

        resultConvert = ConvertDataOfGoogleTableFromStringToList(
            refinePopularList, longtailList, refineAndReplatedList)
        refinePopularListConverted = resultConvert[0]
        longtailListConverted = resultConvert[1]
        refineAndReplatedListConverted = resultConvert[2]
    except:
        keywordSearch = ''
        refinePopularList = ''
        longtailList = ''
        refineAndReplatedList = ''
        refinePopularListConverted = ''
        longtailListConverted = ''
        refineAndReplatedListConverted = ''

    # ================= END : DATA FOR GOOGLE TABLE ================= #

    # ตัดคำซ้ำไม่เกิน 1 และ ไม่เกิน 2
    context['uniqueDataList'] = uniqueDataList
    context['uniqueDataList2WordExceedList'] = uniqueDataList2WordExceedList
    # จำนวนตัวอักษรของตัดคำซ้ำ
    context['numberOfUniqueDataListToString'] = numberOfUniqueDataListToString
    context['numberOfUniqueDataListToString2WordExceed'] = numberOfUniqueDataListToString2WordExceed

    context['lengthFullKeyword'] = lengthFullKeyword
    context['lengthShortKeyword'] = lengthShortKeyword
    context['longtailKeywordModel'] = longtailKeywordModel
    context['mainKeywordId'] = m_kwid
    context['pageId'] = pid
    context['keywordModel'] = keywordModel
    context['zipDataForLoop'] = zipDataForLoop
    context['navpage'] = 'keyword-manager'

    # Search keyword from google
    context['refinePopularList'] = refinePopularListConverted
    context['longtailList'] = longtailListConverted
    context['refineAndReplatedList'] = refineAndReplatedListConverted
    context['keywordSearch'] = keywordSearch

    # health word check
    context['countFullKwKey'] = countFullKwKey
    context['countShortKwKey'] = countShortKwKey

    if 'alert' in request.session:
        if request.session['alert'] == '':
            del request.session['alert']
        else:
            context['title'] = request.session['title']
            context['alert'] = request.session['alert']
            context['status_alert'] = request.session['status_alert']
            del request.session['title']
            del request.session['alert']
            del request.session['status_alert']
    if 'error' in request.session:
        if request.session['error'] == '':
            del request.session['error']
        else:
            context['error'] = request.session['error']
            del request.session['error']
    elif 'status' in request.session:
        if request.session['status'] == '':
            del request.session['status']
        else:
            context['status'] = request.session['status']
            del request.session['status']

    return render(request, 'keywordapp/page-mainkeyword-paragraph-manager.html', context)


@login_required
def LongTailKeywordEdit(request, pid, m_kwid, lt_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    context = {}
    # Edit data
    editData = LongTailKeywordModel.objects.get(
        id=lt_kwid)

    # Update data
    if request.method == 'POST':
        data = request.POST.copy()
        longtailName = data.get('longtail_name')
        longtailName = longtailName.strip()
        shortenName = data.get('shorten_name')
        shortenName = shortenName.strip()
        linkHref = data.get('link_href')
        linkHref = linkHref.strip()
        linkHrefShortenName = data.get('link_href_shorten_name')
        linkHrefShortenName = linkHrefShortenName.strip()
        # if longtail name is empty
        if longtailName == '':
            context['error'] = "กรุณากรอก Keyword"
        else:
            if editData.longtail_name != longtailName:
                # check duplicate
                result = CheckDuplicatedLongtailKeyword(longtailName, m_kwid)
                if result == 'duplicated':
                    request.session['error'] = 'มี Keyword นี้แล้ว'
                    return redirect('longtail-mainkeyword-edit-page', pid, m_kwid, lt_kwid)
                else:
                    pass

            # เอาข้อมูลเก่ามาเก็บไว้ก่อน สำหรับไปลดจำนวนตัวเก่า
            oldFullKw = editData.longtail_name
            oldShortKw = editData.shorten_name
            # edit count key amount
            ManageCountKeyOnEdit(oldFullKw, oldShortKw, longtailName,
                                 shortenName, pid)

            # if shorten keyword is empty replace with full keyword
            if shortenName == '':
                shortenName = longtailName
            editData.longtail_name = longtailName
            editData.shorten_name = shortenName
            editData.link_href = linkHref
            editData.link_href_shorten_name = linkHrefShortenName
            editData.main_keyword = MainKeywordModel.objects.get(id=m_kwid)
            editData.save()

            request.session['status'] = 'แก้ไขสำเร็จแล้ว'
            return redirect('longtail-mainkeyword-page', pid, m_kwid)

    context['editData'] = editData
    context['mainKeywordId'] = m_kwid
    context['pageId'] = pid
    context['navpage'] = 'keyword-manager'

    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''  # clear stuck error in session

    return render(request, 'keywordapp/page-mainkeyword-paragraph-edit-manager.html', context)


@login_required
def LongTailKeywordDelete(request, pid, m_kwid, lt_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    # Add data
    deleteData = LongTailKeywordModel.objects.get(
        id=lt_kwid)
    fullKeyword = deleteData.longtail_name
    shortKeyword = deleteData.shorten_name
# reduce amount of the old one
    AdjustCountKeyToDb(fullKeyword, 'minus', 1, pid)
# reduce amount of the old one
    AdjustCountKeyToDb(shortKeyword, 'minus', 1, pid)
    deleteData.delete()

    request.session['status'] = 'ลบสำเร็จแล้ว'
    return redirect('longtail-mainkeyword-page', pid, m_kwid)


# =============================== LONGTAIL SUB KEYWORD ===============================
# =============================== LONGTAIL SUB KEYWORD ===============================
# =============================== LONGTAIL SUB KEYWORD ===============================


@login_required
def LongTailSubKeyword(request, pid, s_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    # define var
    uniqueDataList = ''
    countFullKwKey = ''
    countShortKwKey = ''

    # START : PREPARE DATA ================
    longtailKeywordModel = LongTailSubKeywordModel.objects.filter(
        sub_keyword_id=s_kwid)

    keywordModel = SubKeywordModel.objects.get(id=s_kwid)

    attribute = "longtail_name"
    resultDeleteDuplicate = DeleteDuplicateFromGettingDataInDb(
        longtailKeywordModel, attribute)
    uniqueDataList = resultDeleteDuplicate[0]
    uniqueDataList2WordExceedList = resultDeleteDuplicate[1]
    numberOfUniqueDataListToString = resultDeleteDuplicate[2]
    numberOfUniqueDataListToString2WordExceed = resultDeleteDuplicate[3]

    # count all character
    attribute = "longtail_name"
    lengthFullKeyword = CountCharacterLength(longtailKeywordModel, attribute)
    attribute = "shorten_name"
    lengthShortKeyword = CountCharacterLength(longtailKeywordModel, attribute)

    # END : PREPARE DATA ================

    # =============================================== START :PREPARE SET OF KEYWORDS ==============================
    # =============================================== START :PREPARE SET OF KEYWORDS ==============================
    # =============================================== START :PREPARE SET OF KEYWORDS ==============================
    try:
        tempKeywordData = TempKeywordSearchModel.objects.get(
            type='paragraph of sub keyword')
        keywordSearch = tempKeywordData.keyword_search
        refinePopularList = tempKeywordData.refine_popular
        longtailList = tempKeywordData.longtail
        refineAndReplatedList = tempKeywordData.related
        # Convert data in table from string to list
        resultConvert = ConvertDataOfGoogleTableFromStringToList(
            refinePopularList, longtailList, refineAndReplatedList)
        refinePopularListConverted = resultConvert[0]
        longtailListConverted = resultConvert[1]
        refineAndReplatedListConverted = resultConvert[2]
    except:
        keywordSearch = ''
        refinePopularList = ''
        longtailList = ''
        refineAndReplatedList = ''
        refinePopularListConverted = ''
        longtailListConverted = ''
        refineAndReplatedListConverted = ''

    # =============================================== END :PREPARE SET OF KEYWORDS ==============================
    # =============================================== END :PREPARE SET OF KEYWORDS ==============================
    # =============================================== END :PREPARE SET OF KEYWORDS ==============================

    context = {}
    # Add data
    if request.method == 'POST':
        data = request.POST.copy()
        searchFrom = data.get('search_from')
        if searchFrom == 'paragraph':
            searchMode = data.get('search_mode')
            keywordSearch = data.get('keyword_search')
            keywordSearch = keywordSearch.strip()
            result = KeywordSearchFunction(request, keywordSearch, searchMode)
            # result to display in keyword search page
            # basic result
            refinePopularList = result[0]
            longtailList = result[1]
            refineAndReplatedList = result[2]
            uniqueDataList = result[9]

            try:
                # ลองหาว่ามีประเภทนี้หรือยัง ถ้ามีแล้วให้อัพเดท
                oldData = TempKeywordSearchModel.objects.get(
                    type='paragraph of sub keyword')
                oldData.keyword_search = keywordSearch
                oldData.refine_popular = refinePopularList
                oldData.longtail = longtailList
                oldData.related = refineAndReplatedList
                oldData.save()
            except:
                # ถ้าไม่มีให้เพิ่มเข้าไปในระบบ
                newTempKeywordSearch = TempKeywordSearchModel()
                newTempKeywordSearch.keyword_search = keywordSearch
                newTempKeywordSearch.refine_popular = refinePopularList
                newTempKeywordSearch.longtail = longtailList
                newTempKeywordSearch.related = refineAndReplatedList
                newTempKeywordSearch.type = 'paragraph of sub keyword'
                newTempKeywordSearch.save()

            request.session['alert'] = keywordSearch
            request.session['status_alert'] = 'success'
        else:
            #  if press button to re add will go in this condition
            if data.get('re_add') == 'True':
                fullLongtailKeyword = data.get('full_lt_keyword')
                fullLongtailKeyword = fullLongtailKeyword.strip()
                shortLongtailKeyword = ''
                linkHref = ''
                linkHrefShortenName = ''
                request.session['status'] = 'เพิ่มคีย์ที่เลือกแล้ว'
            else:
                fullLongtailKeyword = data.get('full_lt_keyword')
                fullLongtailKeyword = fullLongtailKeyword.strip()
                shortLongtailKeyword = data.get('short_lt_keyword')
                shortLongtailKeyword = shortLongtailKeyword.strip()
                linkHref = data.get('link_href')
                linkHref = linkHref.strip()
                linkHrefShortenName = data.get('link_href_shorten_name')
                linkHrefShortenName = linkHrefShortenName.strip()
                request.session['status'] = 'เพิ่มสำเร็จแล้ว'

            if fullLongtailKeyword == '':
                context['error'] = "กรุณากรอก Keyword"
            else:
                # check duplicate
                result = CheckDuplicatedSubLongtailKeyword(
                    fullLongtailKeyword, s_kwid)
                if result == 'duplicated':
                    request.session['error'] = 'มี Keyword นี้แล้ว'
                else:
                    # if shorten keyword is empty replace with full keyword
                    if shortLongtailKeyword == '':
                        shortLongtailKeyword = fullLongtailKeyword
                    newLTKeyword = LongTailSubKeywordModel()
                    newLTKeyword.longtail_name = fullLongtailKeyword
                    newLTKeyword.shorten_name = shortLongtailKeyword
                    newLTKeyword.link_href = linkHref
                    newLTKeyword.link_href_shorten_name = linkHrefShortenName
                    newLTKeyword.sub_keyword = SubKeywordModel.objects.get(
                        id=s_kwid)
                    newLTKeyword.save()

                AddCountKeyToDb(fullLongtailKeyword, 2, pid)

                return redirect('longtail-subkeyword-page', pid, s_kwid)
                # return render(request, 'keywordapp/page-mainkeyword-paragraph-manager.html', context)

    # ================ START: KEYWORD HEALTH ================ #
    # FULL_KEYWORDS
    uniqueDataFullKwList = []
    for data in longtailKeywordModel:
        fullKeyword = data.longtail_name
        # Cut duplicate word by space bar
        fullKeywordSplit = fullKeyword.split()
        for x in fullKeywordSplit:
            uniqueDataFullKwList.append(x)
    counter = Counter(uniqueDataFullKwList).most_common()
    countFullKwKey = dict(counter)
    # SHORT_KEYWORDS
    uniqueDataShortKwList = []
    for data in longtailKeywordModel:
        shortKeyword = data.shorten_name
        # Cut duplicate word by space bar
        shortKeywordSplit = shortKeyword.split()
        for x in shortKeywordSplit:
            uniqueDataShortKwList.append(x)
    counter = Counter(uniqueDataShortKwList).most_common()
    countShortKwKey = dict(counter)
    # ================ END: KEYWORD HEALTH ================ #

    # ================= START : DATA FOR GOOGLE TABLE ================= #
    try:
        tempKeywordData = TempKeywordSearchModel.objects.get(
            type='paragraph of sub keyword')
        keywordSearch = tempKeywordData.keyword_search
        refinePopularList = tempKeywordData.refine_popular
        longtailList = tempKeywordData.longtail
        refineAndReplatedList = tempKeywordData.related
    except:
        keywordSearch = ''
        refinePopularList = ''
        longtailList = ''
        refineAndReplatedList = ''

    resultConvert = ConvertDataOfGoogleTableFromStringToList(
        refinePopularList, longtailList, refineAndReplatedList)
    refinePopularListConverted = resultConvert[0]
    longtailListConverted = resultConvert[1]
    refineAndReplatedListConverted = resultConvert[2]
    # ================= END : DATA FOR GOOGLE TABLE ================= #

    # ================ START : MAP DATA FOR TABLE ================ #
    comeFrom = 'paragraph of main keyword'
    loopMode = 'loop'
    zipDataForLoop = GetZipDataForLoopInTable(
        request, longtailKeywordModel, comeFrom, loopMode, pid)
    # ================ END : MAP DATA FOR TABLE ================ #
    # set context
    # ตัดคำซ้ำไม่เกิน 1 และ ไม่เกิน 2
    context['uniqueDataList'] = uniqueDataList
    context['uniqueDataList2WordExceedList'] = uniqueDataList2WordExceedList
    # จำนวนตัวอักษรของตัดคำซ้ำ
    context['numberOfUniqueDataListToString'] = numberOfUniqueDataListToString
    context['numberOfUniqueDataListToString2WordExceed'] = numberOfUniqueDataListToString2WordExceed

    context['lengthFullKeyword'] = lengthFullKeyword
    context['lengthShortKeyword'] = lengthShortKeyword
    context['longtailKeywordModel'] = longtailKeywordModel
    context['subKeywordId'] = s_kwid
    context['pageId'] = pid
    context['keywordModel'] = keywordModel
    context['countFullKwKey'] = countFullKwKey
    context['countShortKwKey'] = countShortKwKey
    context['zipDataForLoop'] = zipDataForLoop
    context['navpage'] = 'keyword-manager'

    # Search keyword from google
    context['refinePopularList'] = refinePopularListConverted
    context['longtailList'] = longtailListConverted
    context['refineAndReplatedList'] = refineAndReplatedListConverted
    context['keywordSearch'] = keywordSearch

    if 'error' in request.session:
        if request.session['error'] == '':
            del request.session['error']
        else:
            context['error'] = request.session['error']
            del request.session['error']
    elif 'status' in request.session:
        if request.session['status'] == '':
            del request.session['status']
        else:
            context['status'] = request.session['status']
            del request.session['status']
    return render(request, 'keywordapp/page-mainkeyword-paragraph-manager.html', context)


@login_required
def LongTailSubKeywordEdit(request, pid, s_kwid, lts_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    context = {}
    # Edit data
    editData = LongTailSubKeywordModel.objects.get(
        id=lts_kwid)

    # Update data
    if request.method == 'POST':
        data = request.POST.copy()
        longtailName = data.get('longtail_name')
        longtailName = longtailName.strip()
        shortenName = data.get('shorten_name')
        shortenName = shortenName.strip()
        linkHref = data.get('link_href')
        linkHref = linkHref.strip()
        linkHrefShortenName = data.get('link_href_shorten_name')
        linkHrefShortenName = linkHrefShortenName.strip()
        if longtailName == '':
            context['error'] = "กรุณากรอก Keyword"
        else:
            # if old full keyword equal new full keyword don't check this
            if editData.longtail_name != longtailName:
                # check duplicate
                result = CheckDuplicatedSubLongtailKeyword(
                    longtailName, s_kwid)
                if result == 'duplicated':
                    request.session['error'] = 'มี Keyword นี้แล้ว'
                    return redirect('longtail-subkeyword-edit-page', pid, s_kwid, lts_kwid)
                else:
                    pass
            # เอาข้อมูลเก่ามาเก็บไว้ก่อน สำหรับไปลดจำนวนตัวเก่า
            oldFullKw = editData.longtail_name
            oldShortKw = editData.shorten_name
            # edit count key amount
            ManageCountKeyOnEdit(oldFullKw, oldShortKw, longtailName,
                                 shortenName, pid)
            # if shorten keyword is empty replace with full keyword
            if shortenName == '':
                shortenName = longtailName
            editData.longtail_name = longtailName
            editData.shorten_name = shortenName
            editData.link_href = linkHref
            editData.link_href_shorten_name = linkHrefShortenName
            editData.sub_keyword = SubKeywordModel.objects.get(id=s_kwid)
            editData.save()

            request.session['status'] = 'แก้ไขสำเร็จแล้ว'
            return redirect('longtail-subkeyword-page', pid, s_kwid)

    context['editData'] = editData
    context['pageId'] = pid
    context['subKeywordId'] = s_kwid
    context['navpage'] = 'keyword-manager'

    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''  # clear stuck status in session

    return render(request, 'keywordapp/page-mainkeyword-paragraph-edit-manager.html', context)


@login_required
def LongTailSubKeywordDelete(request, pid, s_kwid, lts_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    # Add data
    deleteData = LongTailSubKeywordModel.objects.get(
        id=lts_kwid)
    fullKeyword = deleteData.longtail_name
    shortKeyword = deleteData.shorten_name
# reduce amount of the old one
    AdjustCountKeyToDb(fullKeyword, 'minus', 1, pid)
# reduce amount of the old one
    AdjustCountKeyToDb(shortKeyword, 'minus', 1, pid)
    deleteData.delete()

    request.session['status'] = 'ลบสำเร็จแล้ว'
    return redirect('longtail-subkeyword-page', pid, s_kwid)

# =============================== WEB LIST ===============================
# =============================== WEB LIST ===============================
# =============================== WEB LIST ===============================

# check that is it a page owner


def CheckWebListOwner(request, wid):

    try:
        userObject = User.objects.get(id=request.user.id)
        checkOwner = WebListModel.objects.filter(user_id=userObject.id)
        # all page list and check with current page edit
        # declare list of all pages
        checkOwnerList = []
        # get all id in checkOwner and put them into checkOwnerList
        for x in checkOwner:
            checkOwnerList.append(x.id)
        # check does we have pid in checkOwnerList
        if wid not in checkOwnerList:
            result = "cannot"
        else:
            result = "can"
    except:
        pass
        result = "cannot"
    return result


@login_required
def WebList(request):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    context = {}
    userObject = User.objects.get(id=request.user.id)

    # Add data
    if request.method == 'POST':
        data = request.POST.copy()
        websiteName = data.get('website_name')
        websiteName = websiteName.strip()

        if websiteName == '':
            context['error'] = "กรุณาใส่ชื่อเว็บ"
        else:
            # Check duplicate
            try:
                WebListModel.objects.get(
                    website_name=websiteName)
                context['error'] = 'มีเว็บนี้ในระบบแล้ว'
                return render(request, 'keywordapp/web-list-edit.html', context)
            except:
                pass
            newWebsiteName = WebListModel()
            newWebsiteName.website_name = websiteName
            newWebsiteName.user = userObject
            newWebsiteName.save()

            request.session['status'] = 'เพิ่มเว็บสำเร็จแล้ว'
            return redirect('weblist-page')

    # if there is key status in request.session this will take value from session to context message
    if 'status' in request.session:
        context['message'] = request.session['status']
        request.session['status'] = ''  # clear stuck status in session

    webListModel = WebListModel.objects.filter(user=userObject)

    context['webListModel'] = webListModel
    context['navpage'] = 'keyword-manager'

    return render(request, 'keywordapp/web-list-manager.html', context)


@login_required
def WebListEdit(request, wid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckWebListOwner(request, wid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    context = {}

    # Edit data
    editData = WebListModel.objects.get(
        id=wid)

    context['editData'] = editData
    context['navpage'] = 'keyword-manager'
    # Update data
    if request.method == 'POST':
        data = request.POST.copy()
        websiteName = data.get('website_name')
        websiteName = websiteName.strip()
        # if longtail name is empty
        if websiteName == '':
            context['error'] = "กรุณาใส่ชื่อเว็บไซต์"
        else:
            if editData.website_name != websiteName:
                try:
                    WebListModel.objects.get(
                        website_name=websiteName)
                    context['error'] = 'มีเว็บนี้ในระบบแล้ว'
                    return render(request, 'keywordapp/web-list-edit.html', context)
                except:
                    pass
            editData.website_name = websiteName
            editData.save()
            request.session['status'] = 'แก้ไขสำเร็จแล้ว'
            return redirect('weblist-page')

    return render(request, 'keywordapp/web-list-edit.html', context)


@login_required
def WebListDelete(request, wid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckWebListOwner(request, wid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    delete = WebListModel.objects.get(
        id=wid)
    delete.delete()

    request.session['status'] = 'ลบสำเร็จแล้ว'
    return redirect('weblist-page')


# =============================== PAGE LIST ===============================
# =============================== PAGE LIST ===============================
# =============================== PAGE LIST ===============================

# check that is it a page owner
def CheckPageListOwner(request, pid):

    try:
        userObject = User.objects.get(id=request.user.id)
        checkOwner = PageListModel.objects.filter(user_id=userObject.id)
        # all page list and check with current page edit
        # declare list of all pages
        checkOwnerList = []
        # get all id in checkOwner and put them into checkOwnerList
        for x in checkOwner:
            checkOwnerList.append(x.id)
        # check does we have pid in checkOwnerList
        if pid not in checkOwnerList:
            result = "cannot"
        else:
            result = "can"
    except:
        pass
        result = "cannot"

    return result


@login_required
def PageList(request, wid=0):
    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckWebListOwner(request, wid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    user = User.objects.get(id=request.user.id)

    context = {}
    # Add data
    if request.method == 'POST':
        data = request.POST.copy()
        pageName = data.get('page_name')
        websiteId = data.get('website_id')
        websiteId = websiteId.strip()
        pageName = pageName.strip()
        title = data.get('title')
        title = title.strip()

        if pageName == '':
            context['error'] = "กรุณาใส่ชื่อ page"
        else:
            websiteListObject = WebListModel.objects.get(id=websiteId)
            newPageName = PageListModel()
            newPageName.page_name = pageName
            newPageName.title = title
            newPageName.user = user
            newPageName.website_list = websiteListObject
            newPageName.save()

            request.session['status'] = 'สำเร็จแล้ว'
            return redirect('pagelist-page', wid)

    # if there is key status in request.session this will take value from session to context message
    if 'status' in request.session:
        context['message'] = request.session['status']
        request.session['status'] = ''  # clear stuck status in session
    if wid != 0:
        pageListModel = PageListModel.objects.filter(website_list_id=wid)
    else:
        pageListModel = PageListModel.objects.filter(user=user)

    context['weblistId'] = wid
    context['pageListModel'] = pageListModel
    context['navpage'] = 'keyword-manager'

    return render(request, 'keywordapp/page-list-manager.html', context)


@login_required
def PageListEdit(request, pid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('pagelist-page', wid)

    wid = GetWebListId(pid)
    context = {}

    # Edit data
    editData = PageListModel.objects.get(
        id=pid)

    context['editData'] = editData
    context['weblistId'] = wid
    context['navpage'] = 'keyword-manager'
    # Update data
    if request.method == 'POST':
        data = request.POST.copy()
        pageName = data.get('page_name')
        pageName = pageName.strip()
        title = data.get('title')
        title = title.strip()
        # if longtail name is empty
        if pageName == '':
            context['error'] = "กรุณาใส่ชื่อ page"
        else:
            # if editData.page_name != pageName:
            #     try:
            #         PageListModel.objects.get(
            #             page_name=pageName)
            #         context['error'] = 'มี page นี้ในระบบแล้ว'
            #         return render(request, 'keywordapp/page-list-edit.html', context)
            #     except:
            #         pass
            editData.page_name = pageName
            editData.title = title
            editData.save()
            request.session['status'] = 'แก้ไขสำเร็จแล้ว'
            return redirect('pagelist-page', wid)

    return render(request, 'keywordapp/page-list-edit.html', context)


@login_required
def PageListDelete(request, pid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('pagelist-page', wid)

    wid = GetWebListId(pid)
    delete = PageListModel.objects.get(
        id=pid)
    delete.delete()

    request.session['status'] = 'ลบสำเร็จแล้ว'
    return redirect('pagelist-page', wid)


@login_required
def PageDetail(request, pid):
    context = {}
    # ================ MAIN KEYWORD DATA ================ #
    mainKeyword = MainKeywordModel.objects.filter(
        page_list_id=pid).order_by('header')
    context['mainKeyword'] = mainKeyword
    # ================ PAGE LIST DATA ================ #
    # main data
    pageListData = PageListModel.objects.get(id=pid)
    context['pageListData'] = pageListData

    # ================ META DESCRIPTION ================ #
    # meta description data
    metaDescriptionData = PageListMetaDescriptionModel.objects.filter(
        page_list_id=pid)
    context['metaDescriptionData'] = metaDescriptionData

    # ================ GET WEBSITE ID ================ #
    wid = GetWebListId(pid)
    # ================ DELETE DUPLICATE ================ #
    # meta description data with delete duplicate
    attribute = "full_keyword"
    resultDeleteDuplicate = DeleteDuplicateFromGettingDataInDb(
        metaDescriptionData, attribute)
    uniqueDataList = resultDeleteDuplicate[0]
    uniqueDataList2WordExceedList = resultDeleteDuplicate[1]
    NumberOfUniqueDataListToString = resultDeleteDuplicate[2]
    NumberOfUniqueDataListToString2WordExceed = resultDeleteDuplicate[3]

    context['deleteDuplicatate'] = [uniqueDataList, uniqueDataList2WordExceedList,
                                    NumberOfUniqueDataListToString, NumberOfUniqueDataListToString2WordExceed]

    # ================ COUNT CHARACTER ================ #
    # count all character
    attribute = "full_keyword"
    lengthFullKeyword = CountCharacterLength(metaDescriptionData, attribute)
    attribute = "shorten_keyword"
    lengthShortKeyword = CountCharacterLength(metaDescriptionData, attribute)

    context['lengthKeyword'] = [lengthFullKeyword, lengthShortKeyword]

    # ================ FOOTER ================ #
    footerData = FooterKeywordModel.objects.filter(page_list_id=pid)
    context['footerData'] = footerData
    context['weblistId'] = wid
    context['navpage'] = 'keyword-manager'

    return render(request, 'keywordapp/page-detail.html', context)

# =============================== PAGE LIST META DESCRIPTION ===============================
# =============================== PAGE LIST META DESCRIPTION ===============================
# =============================== PAGE LIST META DESCRIPTION ===============================

# check that is it a page owner


def PageListMetaDescription(request, pid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    wid = GetWebListId(pid)
    # define var
    uniqueDataList = ''
    countFullKwKey = ''
    countShortKwKey = ''

    # =============================================== START :PREPARE SET OF KEYWORDS ==============================
    # =============================================== START :PREPARE SET OF KEYWORDS ==============================
    # =============================================== START :PREPARE SET OF KEYWORDS ==============================
    try:
        tempKeywordData = TempKeywordSearchModel.objects.get(
            type='meta description')
        keywordSearch = tempKeywordData.keyword_search
        refinePopularList = tempKeywordData.refine_popular
        longtailList = tempKeywordData.longtail
        refineAndReplatedList = tempKeywordData.related
        # Convert data in table from string to list
        resultConvert = ConvertDataOfGoogleTableFromStringToList(
            refinePopularList, longtailList, refineAndReplatedList)
        refinePopularListConverted = resultConvert[0]
        longtailListConverted = resultConvert[1]
        refineAndReplatedListConverted = resultConvert[2]
    except:
        keywordSearch = ''
        refinePopularList = ''
        longtailList = ''
        refineAndReplatedList = ''
        refinePopularListConverted = ''
        longtailListConverted = ''
        refineAndReplatedListConverted = ''

    # =============================================== END :PREPARE SET OF KEYWORDS ==============================
    # =============================================== END :PREPARE SET OF KEYWORDS ==============================
    # =============================================== END :PREPARE SET OF KEYWORDS ==============================
    context = {}
    # Add data
    if request.method == 'POST':
        data = request.POST.copy()
        searchFrom = data.get('search_from')
        if searchFrom == 'paragraph':
            searchMode = data.get('search_mode')
            keywordSearch = data.get('keyword_search')
            if keywordSearch == '':
                request.session['error'] = 'กรุณากรอก Keyword'
                return redirect('pagelist-meta-page', pid)
            keywordSearch = keywordSearch.strip()
            result = KeywordSearchFunction(request, keywordSearch, searchMode)
            # result to display in keyword search page
            # basic result
            refinePopularList = result[0]
            longtailList = result[1]
            refineAndReplatedList = result[2]
            try:
                # ลองหาว่ามีประเภทนี้หรือยัง ถ้ามีแล้วให้อัพเดท
                oldData = TempKeywordSearchModel.objects.get(
                    type='meta description')
                oldData.keyword_search = keywordSearch
                oldData.refine_popular = refinePopularList
                oldData.longtail = longtailList
                oldData.related = refineAndReplatedList
                oldData.save()

                request.session['alert'] = keywordSearch
                request.session['status_alert'] = 'success'
                return redirect('pagelist-meta-page', pid)
            except:
                # ถ้าไม่มีให้เพิ่มเข้าไปในระบบ
                newTempKeywordSearch = TempKeywordSearchModel()
                newTempKeywordSearch.keyword_search = keywordSearch
                newTempKeywordSearch.refine_popular = refinePopularList
                newTempKeywordSearch.longtail = longtailList
                newTempKeywordSearch.related = refineAndReplatedList
                newTempKeywordSearch.type = 'meta description'
                newTempKeywordSearch.save()

                request.session['alert'] = keywordSearch
                request.session['status_alert'] = 'success'
                return redirect('pagelist-meta-page', pid)
        # ถ้าเงื่อนไขนี้เป็นการเพิ่มข้อมูล ไม่ใช่การค้นหา
        else:
            #  ถ้าเป็นการเพิ่มข้อมูลแบบกดปุ่มจากตารางจะเข้าเงื่อไนขนี้
            if data.get('re_add') == 'True':
                fullKeyword = data.get('full_keyword')
                fullKeyword = fullKeyword.strip()
                statusShow = 'เพิ่มคีย์ที่เลือกแล้ว'
            else:
                #  ถ้าเป็นการกดปุ่มเพิ่มด้วยตัวเองจะเข้าเงื่อนไขนี้
                fullKeyword = data.get('full_keyword')
                fullKeyword = fullKeyword.strip()
                statusShow = 'เพิ่มข้อมูลแล้ว'

            if fullKeyword == '':
                request.session['status'] = 'กรุณากรอก Full keyword'
                return redirect('pagelist-meta-page', pid)
            else:
                # check duplicate
                result = CheckDuplicatedMetaDescription(
                    fullKeyword, pid)
                if result == 'duplicated':
                    request.session['error'] = 'มี Keyword นี้แล้ว'
                else:
                    pageListData = PageListModel.objects.get(id=pid)
                    # Add meta description
                    newMetaDescription = PageListMetaDescriptionModel()
                    newMetaDescription.full_keyword = fullKeyword
                    newMetaDescription.shorten_keyword = fullKeyword
                    newMetaDescription.page_list = pageListData
                    newMetaDescription.save()

                    AddCountKeyToDb(fullKeyword, 2, pid)

            request.session['status'] = statusShow

            return redirect('pagelist-meta-page', pid)

    # ================ START: DATA FOR PAGE ================ #
    # get metadescription for page
    metaDescription = PageListMetaDescriptionModel.objects.all().filter(page_list_id=pid)
    # count all character
    attribute = "full_keyword"
    lengthFullKeyword = CountCharacterLength(metaDescription, attribute)
    attribute = "shorten_keyword"
    lengthShortKeyword = CountCharacterLength(metaDescription, attribute)
    # get title of page
    pageData = PageListModel.objects.get(id=pid)
    titleOfPage = pageData.title
    pageName = pageData.page_name
    # ================ END: DATA FOR PAGE ================ #

    # ================ START: KEYWORD HEALTH ================ #
    # FULL_KEYWORDS
    uniqueDataFullKwList = []
    fullKeyword = ''
    for data in metaDescription:
        fullKeyword = data.full_keyword
        # Cut duplicate word by space bar
        fullKeywordSplit = fullKeyword.split()
        for x in fullKeywordSplit:
            uniqueDataFullKwList.append(x)
    counter = Counter(uniqueDataFullKwList).most_common()
    countFullKwKey = dict(counter)
    # SHORT_KEYWORDS
    uniqueDataShortKwList = []
    for data in metaDescription:
        shortKeyword = data.shorten_keyword
        # Cut duplicate word by space bar
        shortKeywordSplit = shortKeyword.split()
        for x in shortKeywordSplit:
            uniqueDataShortKwList.append(x)
    counter = Counter(uniqueDataShortKwList).most_common()
    countShortKwKey = dict(counter)
    # ================ END: KEYWORD HEALTH ================ #
    # ================ START : DELETE DUPLICATE ================ #
    # meta description data with delete duplicate
    attribute = "full_keyword"
    resultDeleteDuplicate = DeleteDuplicateFromGettingDataInDb(
        metaDescription, attribute)
    uniqueDataList = resultDeleteDuplicate[0]
    uniqueDataList2WordExceedList = resultDeleteDuplicate[1]
    numberOfUniqueDataListToString = resultDeleteDuplicate[2]
    numberOfUniqueDataListToString2WordExceed = resultDeleteDuplicate[3]

    # ================ END : DELETE DUPLICATE ================ #

    # ================ START : MAP DATA FOR TABLE ================ #
    comeFrom = 'meta description'
    loopMode = 'loop'
    zipDataForLoop = GetZipDataForLoopInTable(
        request, metaDescription, comeFrom, loopMode, pid)
    # ================ END : MAP DATA FOR TABLE ================ #

    # set context
    # ตัดคำซ้ำไม่เกิน 1 และ ไม่เกิน 2
    context['uniqueDataList'] = uniqueDataList
    context['uniqueDataList2WordExceedList'] = uniqueDataList2WordExceedList
    # จำนวนตัวอักษรของตัดคำซ้ำ
    context['numberOfUniqueDataListToString'] = numberOfUniqueDataListToString
    context['numberOfUniqueDataListToString2WordExceed'] = numberOfUniqueDataListToString2WordExceed

    context['lengthFullKeyword'] = lengthFullKeyword
    context['lengthShortKeyword'] = lengthShortKeyword
    context['titleOfPage'] = titleOfPage
    context['pageName'] = pageName
    context['pageId'] = pid
    context['countFullKwKey'] = countFullKwKey
    context['countShortKwKey'] = countShortKwKey
    context['zipDataForLoop'] = zipDataForLoop
    context['metaDescription'] = metaDescription
    context['weblistId'] = wid
    context['navpage'] = 'keyword-manager'

    # Search keyword from google
    context['refinePopularListConverted'] = refinePopularListConverted
    context['longtailListConverted'] = longtailListConverted
    context['refineAndReplatedListConverted'] = refineAndReplatedListConverted
    context['keywordSearch'] = keywordSearch

    # session
    if 'alert' in request.session:
        if request.session['alert'] == '':
            del request.session['alert']
        else:
            context['alert'] = request.session['alert']
            context['status_alert'] = request.session['status_alert']
            del request.session['alert']
            del request.session['status_alert']
    if 'error' in request.session:
        if request.session['error'] == '':
            del request.session['error']
        else:
            context['error'] = request.session['error']
            del request.session['error']
    elif 'status' in request.session:
        if request.session['status'] == '':
            del request.session['status']
        else:
            context['message'] = request.session['status']
            del request.session['status']

    return render(request, 'keywordapp/page-list-meta-description.html', context)


@login_required
def PageListMetaDescriptionEdit(request, pid, metaid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    context = {}
    # Edit data
    editData = PageListMetaDescriptionModel.objects.get(
        id=metaid)

    # Update data
    if request.method == 'POST':
        data = request.POST.copy()
        fullKeyword = data.get('full_keyword')
        fullKeyword = fullKeyword.strip()
        shortenKeyword = data.get('shorten_keyword')
        shortenKeyword = shortenKeyword.strip()

        if fullKeyword == '':
            context['error'] = "กรุณาใส่ full keyword"
        else:
            # if shorten keyword is empty replace with full keyword
            if shortenKeyword == '':
                shortenKeyword = fullKeyword
            editData = PageListMetaDescriptionModel.objects.get(id=metaid)
            # เอาข้อมูลเก่ามาเก็บไว้ก่อน สำหรับไปลดจำนวนตัวเก่า
            oldFullKw = editData.full_keyword
            oldShortKw = editData.shorten_keyword
            # edit count key amount
            ManageCountKeyOnEdit(
                oldFullKw, oldShortKw, fullKeyword, shortenKeyword, pid)

            editData.full_keyword = fullKeyword
            editData.shorten_keyword = shortenKeyword
            editData.page_list = PageListModel.objects.get(id=pid)
            editData.save()

            request.session['status'] = 'แก้ไขสำเร็จแล้ว'
            return redirect('pagelist-meta-page', pid)

    context['editData'] = editData
    context['pageId'] = pid
    context['navpage'] = 'keyword-manager'

    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''  # clear stuck status in session

    return render(request, 'keywordapp/page-list-meta-description-edit.html', context)


@login_required
def PageListMetaDescriptionDelete(request, pid, metaid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    try:
        deleteData = PageListMetaDescriptionModel.objects.get(
            id=metaid)
        fullKeyword = deleteData.full_keyword
        shortKeyword = deleteData.shorten_keyword
    # reduce amount of the old one
        AdjustCountKeyToDb(fullKeyword, 'minus', 1, pid)
    # reduce amount of the old one
        AdjustCountKeyToDb(shortKeyword, 'minus', 1, pid)
        deleteData.delete()
    except:
        pass

    request.session['status'] = 'ลบสำเร็จแล้ว'
    return redirect('pagelist-meta-page', pid)


# =============================== MAIN KEYWORD ===============================
# =============================== MAIN KEYWORD ===============================
# =============================== MAIN KEYWORD ===============================

@login_required
def MainKeyword(request, pid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    wid = GetWebListId(pid)
    context = {}
    # Add data
    if request.method == 'POST':
        data = request.POST.copy()
        mainKeyword = data.get('main_keyword')
        mainKeyword = mainKeyword.strip()
        header = data.get('header')
        giveDetail = data.get('give_detail')
        giveDetail = giveDetail.strip()

        if mainKeyword == '':
            context['error'] = "ใส่ keyword"
        else:
            if giveDetail == 'no':
                newPostName = MainKeywordModel()
                newPostName.keyword_name = mainKeyword
                newPostName.header = header
                newPostName.page_list = PageListModel.objects.get(
                    id=pid)
                newPostName.save()
            else:
                giveDetailKeyword = SubKeywordModel()
                giveDetailKeyword.keyword_name = mainKeyword
                giveDetailKeyword.header = header
                giveDetailKeyword.main_keyword = MainKeywordModel.objects.filter(page_list_id=pid).get(
                    keyword_name=giveDetail)
                giveDetailKeyword.save()
            request.session['status'] = 'เพิ่มสำเร็จแล้ว'
            return redirect('page-header-page', pid)

    main_keyword = MainKeywordModel.objects.all().filter(
        page_list_id=pid).order_by('header')
    page_data = PageListModel.objects.all().get(id=pid)

    context['mainKeywordList'] = main_keyword
    context['pageName'] = page_data.page_name
    context['title'] = page_data.title
    context['pageId'] = pid
    context['weblistId'] = wid
    context['navpage'] = 'keyword-manager'

    # if there is key status in request.session this will take value from session to context message
    if 'status' in request.session:
        context['message'] = request.session['status']
        request.session['status'] = ''  # clear stuck status in session
    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''  # clear stuck status in session

    return render(request, 'keywordapp/page-header-manager.html', context)


@login_required
def MainKeywordEdit(request, pid, m_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')
    wid = GetWebListId(pid)

    context = {}
    # Edit data
    editData = MainKeywordModel.objects.get(
        id=m_kwid)

    # Update data
    if request.method == 'POST':
        data = request.POST.copy()
        keywordName = data.get('keyword_name')
        keywordName = keywordName.strip()
        header = data.get('header')
        # if longtail name is empty
        if keywordName == '':
            context['error'] = "กรุณาใส่ keyword"
        else:
            editData = MainKeywordModel.objects.get(id=m_kwid)
            editData.keyword_name = keywordName
            editData.header = header
            editData.page_list = PageListModel.objects.get(id=pid)
            editData.save()

            request.session['status'] = 'แก้ไขสำเร็จแล้ว'
            return redirect('page-header-page', pid)

    context['editData'] = editData
    context['pageId'] = pid
    context['mainKeywordId'] = m_kwid
    context['weblistId'] = wid
    context['navpage'] = 'keyword-manager'

    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''  # clear stuck status in session

    return render(request, 'keywordapp/page-header-edit-manager.html', context)


@login_required
def MainKeywordDelete(request, pid, m_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    delete = MainKeywordModel.objects.get(
        id=m_kwid)
    delete.delete()

    request.session['status'] = 'ลบสำเร็จแล้ว'
    return redirect('page-header-page', pid)

# =============================== SUB KEYWORD ===============================
# =============================== SUB KEYWORD ===============================
# =============================== SUB KEYWORD ===============================


@login_required
def SubKeywordEdit(request, pid, m_kwid, s_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    context = {}
    # Edit data
    editData = SubKeywordModel.objects.get(
        id=s_kwid)

    # Update data
    if request.method == 'POST':
        data = request.POST.copy()
        keywordName = data.get('keyword_name')
        keywordName = keywordName.strip()
        header = data.get('header')

        # if longtail name is empty
        if keywordName == '':
            context['error'] = "กรุณาใส่ keyword"
        else:
            editData = SubKeywordModel.objects.get(id=s_kwid)
            editData.keyword_name = keywordName
            editData.header = header
            editData.main_keyword = MainKeywordModel.objects.get(id=m_kwid)
            editData.save()

            request.session['status'] = 'แก้ไขสำเร็จแล้ว'
            return redirect('page-header-page', pid)

    context['editData'] = editData
    context['pageId'] = pid
    context['mainKeywordId'] = m_kwid
    context['subKeywordId'] = s_kwid
    context['navpage'] = 'keyword-manager'

    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''  # clear stuck status in session

    return render(request, 'keywordapp/page-sub-header-edit-manager.html', context)


@login_required
def SubKeywordDelete(request, pid, s_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    delete = SubKeywordModel.objects.get(
        id=s_kwid)
    delete.delete()

    request.session['status'] = 'ลบสำเร็จแล้ว'
    return redirect('page-header-page', pid)


# =============================== KEYWORD SEARCH ===============================
# =============================== KEYWORD SEARCH ===============================
# =============================== KEYWORD SEARCH ===============================

def KeywordSearchFunction(request, keywordSearch, searchMode):
    context = {}
  # if search mode is single we will loop once but if want Excel mode will read excel from PC
    if searchMode == 'ตัวเดียว' or searchMode == '2 ตัวแรกไปค้นหาเพิ่ม':
        loopAmount = 1
        if keywordSearch == '':
            context = "กรุณาใส่ keyword"
            return context
    else:
        loopAmount = 1  # save page if loopAmount isn't set

    # Open in mobile
    ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1'
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent="+ua)

    for data in range(loopAmount):
        # driver = webdriver.Remote(
        #     'http://joker123-joker388.net:4444', options=options)
        # server
        # driver = webdriver.Remote('http://172.17.0.3:4444/wd/hub',desired_capabilities=DesiredCapabilities.CHROME)
        # driver = webdriver.Chrome(options=options,executable_path='/home/cheetah/keywordsearch.joker123-joker388/chromedriver')
        # local
        driver = webdriver.Chrome(options=options)

        driver.get('https://www.google.com/?hl=TH-10')

        # if cannot find searchBoxHomePage will re-open browser
        checkElement = True
        while checkElement == True:
            try:
                WebDriverWait(driver, timeout=15).until(
                    lambda d: d.find_element(By.CLASS_NAME, 'gLFyf'))
                searchBoxHomePage = driver.find_element(By.CLASS_NAME, 'gLFyf')
                searchBoxHomePage.click()
                time.sleep(1)
                searchBoxHomePage.send_keys(keywordSearch)
                searchBoxHomePage.send_keys(Keys.ENTER)
                checkElement = False
            except:
                driver.quit()
                driver = webdriver.Remote(
                    'http://joker123-joker388.net:4444', options=options)
                # driver = webdriver.Chrome(options=options)
                driver.get('https://www.google.com')
        checkElement = True
        while checkElement == True:
            try:
                WebDriverWait(driver, timeout=15).until(
                    lambda d: d.find_element(By.CLASS_NAME, 'gLFyf'))
                searchBoxInSearchQuery = driver.find_element(
                    By.CLASS_NAME, 'gLFyf')
                searchBoxInSearchQuery.click()
                time.sleep(1)
                checkElement = False
            except:
                request.session['alert'] = keywordSearch
                request.session['status_alert'] = 'danger'
                return "cannot find search input"

        time.sleep(1)
        getRefinePopular = driver.find_elements(By.CLASS_NAME, 'sbct')
        getRefinePopularList = []
        for x in getRefinePopular:
            result = x.text
            findDot = result.find('... ')
            if findDot >= 0:
                result = result.replace('... ', '')
            if result != '':
                getRefinePopularList.append(result)

        # Add space to get longtail
        searchBoxInSearchQuery.send_keys(Keys.SPACE)
        driver.save_screenshot('capture-3.png')
        time.sleep(1)

        getLongtail = driver.find_elements(By.CLASS_NAME, 'sbct')
        getLongtailList = []
        for x in getLongtail:
            result = x.text
            findDot = result.find('... ')
            if findDot >= 0:
                result = result.replace('... ', '')
            if result != '':
                getLongtailList.append(result)

        time.sleep(1)

        try:
            WebDriverWait(driver, timeout=30).until(
                lambda d: d.find_element(By.CLASS_NAME, 'Cdl0yb'))
            # Press back button
            backButton = driver.find_element(By.CLASS_NAME, 'Cdl0yb')
            backButton.click()
            time.sleep(1)
        except:
            request.session['alert'] = keywordSearch
            request.session['status_alert'] = 'danger'
            return "cannot find back button"

        # Get Refine/Related
        getRefineAndReplated = driver.find_elements(
            By.XPATH, '//span[@class="RrotFd wHYlTd"]')
        getRefineAndReplatedList = []
        for x in getRefineAndReplated:
            result = x.text
            findDot = result.find('... ')
            if findDot >= 0:
                result = result.replace('... ', '')
            if result != '':
                getRefineAndReplatedList.append(result)

        driver.quit()

        # Remove duplicate result
        # Loop Refine Popular List then check each one with "Longtail" and "Refine/Related"
        for data in getRefinePopularList:
            if data in getLongtailList:
                getLongtailList.remove(data)
            if data in getRefineAndReplatedList:
                getRefineAndReplatedList.remove(data)

        if searchMode == '2 ตัวแรกไปค้นหาเพิ่ม':
            if getRefinePopularList:
                refinePopular1 = getRefinePopularList[0]
                refinePopular2 = getRefinePopularList[1]
            else:
                refinePopular1 = ''
                refinePopular2 = ''

            if getLongtailList:
                longtail1 = getLongtailList[0]
                longtail2 = getLongtailList[1]
            else:
                longtail1 = ''
                longtail2 = ''

            if getRefineAndReplatedList:
                refineAndRelated1 = getRefineAndReplatedList[0]
                refineAndRelated2 = getRefineAndReplatedList[1]
            else:
                refineAndRelated1 = ''
                refineAndRelated2 = ''

        else:
            refinePopular1 = ''
            refinePopular2 = ''
            longtail1 = ''
            longtail2 = ''
            refineAndRelated1 = ''
            refineAndRelated2 = ''

        # ===================== Delete duplicate ===================
        # ===================== Delete duplicate ===================
        # ===================== Delete duplicate ===================
        uniqueDataList = DeleteDuplicateFromTableResultList(
            getRefinePopularList, getLongtailList, getRefineAndReplatedList)
    result1 = getRefinePopularList
    result2 = getLongtailList
    result3 = getRefineAndReplatedList
    result4 = refinePopular1
    result5 = refinePopular2
    result6 = longtail1
    result7 = longtail2
    result8 = refineAndRelated1
    result9 = refineAndRelated2
    result10 = uniqueDataList
    result = [result1, result2, result3, result4, result5,
              result6, result7, result8, result9, result10]
    return result


# @login_required
def KeywordSearch(request):
    uniqueDataList = []
    getRefinePopularList = []
    getLongtailList = []
    getRefineAndReplatedList = []
    keywordSearch = ''
    # expireDate = request.user.profilemodel.expire_date
    # userId = request.user.id
    # resultCheckExpire = CheckExpireDate(expireDate, userId)
    # if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
    #     return redirect('Home')

    # # if have no permission cannot enter this page
    # checkPermission = CheckPremiumUser(request)
    # if checkPermission == 'Have no permission':
        # return redirect('Home')

    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        keywordSearch = data.get('keyword_search')
        keywordSearch = keywordSearch.strip()
        searchMode = data.get('search_mode')
        result = KeywordSearchFunction(request, keywordSearch, searchMode)

        userSearch = request.user.username
        print("username : {}\nsearch : {}".format(userSearch, keywordSearch))
        # if result = cannot find search input redirect and inform error
        if result == "cannot find search input":
            redirect('keyword-search-page')
        if searchMode == '2 ตัวแรกไปค้นหาเพิ่ม':
            # get top 1-2 keyword from each type then re-search
            searchMode = 'เอา Keyword กลับมา Loop'

            refinePopular1 = result[3]
            resultRefinePopular1 = KeywordSearchFunction(
                request, refinePopular1, searchMode)

            # re-search result
            refinePopular1RefinePopular = resultRefinePopular1[0]
            refinePopular1Longtail = resultRefinePopular1[1]
            refinePopular1Related = resultRefinePopular1[2]

            # set context
            context['refinePopular1KeywordSearch'] = refinePopular1
            context['refinePopular1RefinePopular'] = refinePopular1RefinePopular
            context['refinePopular1Longtail'] = refinePopular1Longtail
            context['refinePopular1Related'] = refinePopular1Related

            refinePopular2 = result[4]
            resultRefinePopular2 = KeywordSearchFunction(
                request, refinePopular2, searchMode)

            # re-search result
            refinePopular2RefinePopular = resultRefinePopular2[0]
            refinePopular2Longtail = resultRefinePopular2[1]
            refinePopular2Related = resultRefinePopular2[2]

            # set context
            context['refinePopular2KeywordSearch'] = refinePopular2
            context['refinePopular2RefinePopular'] = refinePopular2RefinePopular
            context['refinePopular2Longtail'] = refinePopular2Longtail
            context['refinePopular2Related'] = refinePopular2Related

            longtail1 = result[5]
            resultLongtail1 = KeywordSearchFunction(
                request, longtail1, searchMode)

            # re-search result
            resultLongtail1RefinePopular = resultLongtail1[0]
            resultLongtail1Longtail = resultLongtail1[1]
            resultLongtail1Related = resultLongtail1[2]

            # set context
            context['resultLongtail1KeywordSearch'] = longtail1
            context['resultLongtail1RefinePopular'] = resultLongtail1RefinePopular
            context['resultLongtail1Longtail'] = resultLongtail1Longtail
            context['resultLongtail1Related'] = resultLongtail1Related

            longtail2 = result[6]

            resultLongtail2 = KeywordSearchFunction(
                request, longtail2, searchMode)

            # re-search result
            resultLongtail2RefinePopular = resultLongtail2[0]
            resultLongtail2Longtail = resultLongtail2[1]
            resultLongtail2Related = resultLongtail2[2]

            # set context
            context['resultLongtail2KeywordSearch'] = longtail2
            context['resultLongtail2RefinePopular'] = resultLongtail2RefinePopular
            context['resultLongtail2Longtail'] = resultLongtail2Longtail
            context['resultLongtail2Related'] = resultLongtail2Related

            refineAndRelated1 = result[7]
            resultRefineAndRelated1 = KeywordSearchFunction(
                request, refineAndRelated1, searchMode)

            # re-search result
            resultRefineAndRelated1RefinePopular = resultRefineAndRelated1[0]
            resultRefineAndRelated1Longtail = resultRefineAndRelated1[1]
            resultRefineAndRelated1Related = resultRefineAndRelated1[2]

            # set context
            context['resultRefineAndRelated1KeywordSearch'] = refineAndRelated1
            context['resultRefineAndRelated1RefinePopular'] = resultRefineAndRelated1RefinePopular
            context['resultRefineAndRelated1Longtail'] = resultRefineAndRelated1Longtail
            context['resultRefineAndRelated1Related'] = resultRefineAndRelated1Related

            refineAndRelated2 = result[8]
            resultRefineAndRelated2 = KeywordSearchFunction(
                request, refineAndRelated2, searchMode)

            # re-search result
            resultRefineAndRelated2RefinePopular = resultRefineAndRelated2[0]
            resultRefineAndRelated2Longtail = resultRefineAndRelated2[1]
            resultRefineAndRelated2Related = resultRefineAndRelated2[2]

            # set context
            context['resultRefineAndRelated2KeywordSearch'] = refineAndRelated2
            context['resultRefineAndRelated2RefinePopular'] = resultRefineAndRelated2RefinePopular
            context['resultRefineAndRelated2Longtail'] = resultRefineAndRelated2Longtail
            context['resultRefineAndRelated2Related'] = resultRefineAndRelated2Related

        # result to display in keyword search page
        # basic result
        getRefinePopularList = result[0]
        getLongtailList = result[1]
        getRefineAndReplatedList = result[2]
        uniqueDataList = result[9]

        try:
            # ลองหาว่ามีประเภทนี้หรือยัง ถ้ามีแล้วให้อัพเดท
            oldData = TempKeywordSearchModel.objects.get(type='keyword search')
            oldData.keyword_search = keywordSearch
            oldData.refine_popular = getRefinePopularList
            oldData.longtail = getLongtailList
            oldData.related = getRefineAndReplatedList
            oldData.save()
        except:
            # ถ้าไม่มีให้เพิ่มเข้าไปในระบบ
            newTempKeywordSearch = TempKeywordSearchModel()
            newTempKeywordSearch.keyword_search = keywordSearch
            newTempKeywordSearch.refine_popular = getRefinePopularList
            newTempKeywordSearch.longtail = getLongtailList
            newTempKeywordSearch.related = getRefineAndReplatedList
            newTempKeywordSearch.type = 'keyword search'
            newTempKeywordSearch.save()
        request.session['alert'] = keywordSearch
        request.session['status_alert'] = 'success'
        return redirect('keyword-search-page')

    # =============================================== START :PREPARE SET OF KEYWORDS ==============================
    # =============================================== START :PREPARE SET OF KEYWORDS ==============================
    # =============================================== START :PREPARE SET OF KEYWORDS ==============================
    try:
        tempKeywordData = TempKeywordSearchModel.objects.get(
            type='keyword search')
        keywordSearch = tempKeywordData.keyword_search
        refinePopularList = tempKeywordData.refine_popular
        longtailList = tempKeywordData.longtail
        refineAndReplatedList = tempKeywordData.related
        # Convert data in table from string to list
        resultConvert = ConvertDataOfGoogleTableFromStringToList(
            refinePopularList, longtailList, refineAndReplatedList)
        refinePopularListConverted = resultConvert[0]
        longtailListConverted = resultConvert[1]
        refineAndReplatedListConverted = resultConvert[2]

    # =============================================== START :DELETE DUPLICATED ==============================
    # =============================================== START :DELETE DUPLICATED ==============================
    # =============================================== START :DELETE DUPLICATED ==============================

        uniqueDataList = DeleteDuplicateFromTableResultList(
            refinePopularListConverted, longtailListConverted, refineAndReplatedListConverted)

    # =============================================== END :DELETE DUPLICATED ==============================
    # =============================================== END :DELETE DUPLICATED ==============================
    # =============================================== END :DELETE DUPLICATED ==============================

    except:
        keywordSearch = ''
        refinePopularList = ''
        longtailList = ''
        refineAndReplatedList = ''
        refinePopularListConverted = ''
        longtailListConverted = ''
        refineAndReplatedListConverted = ''

    # =============================================== END :PREPARE SET OF KEYWORDS ==============================
    # =============================================== END :PREPARE SET OF KEYWORDS ==============================
    # =============================================== END :PREPARE SET OF KEYWORDS ==============================

    context['uniqueDataList'] = uniqueDataList
    context['refinePopularList'] = refinePopularListConverted
    context['longtailList'] = longtailListConverted
    context['refineAndReplatedList'] = refineAndReplatedListConverted
    context['keywordSearch'] = keywordSearch
    context['navpage'] = 'keyword-search'

    if 'alert' in request.session:
        context['alert'] = request.session['alert']
        context['status_alert'] = request.session['status_alert']
        del request.session['alert']
        del request.session['status_alert']

    return render(request, 'keywordapp/keyword_search.html', context)


# =============================== Post ===============================
# =============================== Post ===============================
# =============================== Post ===============================

@login_required
def PostManager(request):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    context = {}
    if request.method == 'POST':
        data = request.POST.copy()
        articleTitle = data.get('article_title')
        articleContent = data.get('article_content')
        articleAlt = data.get('article_alt')
        tag1 = data.get('tag1')
        tag2 = data.get('tag2')
        tag3 = data.get('tag3')
        if articleTitle == '':
            return redirect('post-page')
        if articleContent == '':
            return redirect('post-page')
        newArticlePage = ArticlePageModel()
        newArticlePage.article_title = articleTitle
        newArticlePage.content = articleContent
        newArticlePage.author = request.user.first_name
        newArticlePage.image_alt = articleAlt

        # get image
        if 'article_image' in request.FILES:  # มี key image อยู่ใน request.FILES หรือไม่
            # เอา object ของรูปภาพมาเก็บใส่ตัวแปร
            file_image = request.FILES['article_image']
            # ดึง name ใน object รูปภาพออกมาพร้อมแทนที่ เว้นวรรค ด้วยค่าว่าง
            file_image_name = file_image.name.replace(' ', '')

            try:
                lastArticleData = ArticlePageModel.objects.latest('id')
                lastArticleId = lastArticleData.id
            except:
                # If it is Null mean has no any data we will set as 1
                lastArticleId = 0

            lastArticleId = lastArticleId + 1
            saved_location = 'media/article/{}'.format(lastArticleId)
            # สร้าง Instance สำหรับบันทึกข้อมูลลงเครื่อง
            fs = FileSystemStorage(location=saved_location)
            # คำสั่งบันทึกลงเครื่องโดยใส่ชื่อ และ object รูปภาพ
            filename = fs.save(file_image_name, file_image)
            # ดึง url ออกมาจาก file_name
            upload_file_url = "{}/{}".format(saved_location, filename)
            # ให้เก็บตั้งแต่ตัวที่ 6 เป็นต้นไป เพราะ 6 ตัวแรกเป็นคำว่า media/
            newArticlePage.image_link = upload_file_url[6:]
            newArticlePage.save()

            # Add tag to Article
            if tag1 != 'none':
                tagForArticleData1 = TagModel.objects.get(tag_name=tag1)
                newArticlePage.tag.add(tagForArticleData1)
            if tag2 != 'none':
                tagForArticleData2 = TagModel.objects.get(tag_name=tag2)
                newArticlePage.tag.add(tagForArticleData2)
            if tag3 != 'none':
                tagForArticleData3 = TagModel.objects.get(tag_name=tag3)
                newArticlePage.tag.add(tagForArticleData3)

            request.session['alert'] = 'เพิ่มโพสต์สำเร็จ'
            return redirect('post-page')

    if 'alert' in request.session:
        context['message'] = request.session['alert']
        request.session['alert'] = ''  # clear stuck status in session

    articleData = ArticlePageModel.objects.all()
    context['articleData'] = articleData

    tagData = TagModel.objects.all()
    context['tagData'] = tagData
    context['navpage'] = 'post'

    return render(request, 'keywordapp/post-manager.html', context)

# =============================== FOOTER ===============================
# =============================== FOOTER ===============================
# =============================== FOOTER ===============================


@login_required
def PageListFooter(request, pid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')
    wid = GetWebListId(pid)
    context = {}
    if request.method == 'POST':
        data = request.POST.copy()
        footerKeyword = data.get('footer_keyword')
        header = data.get('header')
        giveDetail = data.get('give_detail')

        # get title of page
        pageData = PageListModel.objects.get(id=pid)
        # check duplicated
        try:
            FooterKeywordModel.objects.get(
                keyword_name=footerKeyword, page_list_id=pid)
            request.session['error'] = 'มี Keyword นี้ใน Footer แล้ว'
            return redirect('page-footer-page', pid)
        except:
            if footerKeyword == '':
                context['error'] = "ใส่ keyword"
            else:
                if giveDetail == 'no':
                    newPostName = FooterKeywordModel()
                    newPostName.keyword_name = footerKeyword
                    newPostName.header = header
                    newPostName.page_list = pageData
                    newPostName.save()
                else:
                    giveDetailKeyword = SubFooterKeywordModel()
                    giveDetailKeyword.keyword_name = footerKeyword
                    giveDetailKeyword.header = header
                    giveDetailKeyword.footer_keyword = FooterKeywordModel.objects.filter(page_list_id=pid).get(
                        keyword_name=giveDetail)
                    giveDetailKeyword.save()
                request.session['status'] = 'เพิ่มสำเร็จแล้ว'
                return redirect('page-footer-page', pid)

    # get title of page
    pageData = PageListModel.objects.get(id=pid)
    titleOfPage = pageData.title
    pageName = pageData.page_name

    footerKeywordList = FooterKeywordModel.objects.filter(page_list_id=pid)
    # count character of footer
    attribute = "keyword_name"
    lengthFullKeyword = CountCharacterLength(footerKeywordList, attribute)

    context['titleOfPage'] = titleOfPage
    context['pageName'] = pageName
    context['pageId'] = pid
    context['lengthFullKeyword'] = lengthFullKeyword
    context['footerKeywordList'] = footerKeywordList
    context['weblistId'] = wid
    context['navpage'] = 'keyword-manager'

    # if there is key status in request.session this will take value from session to context message
    if 'status' in request.session:
        context['message'] = request.session['status']
        del request.session['status']  # clear stuck status in session
    if 'error' in request.session:
        context['error'] = request.session['error']
        del request.session['error']  # clear stuck status in session

    return render(request, 'keywordapp/footer/footer-manager.html', context)


@login_required
def PageListFooterEdit(request, pid, fid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    context = {}

    pageData = PageListModel.objects.get(id=pid)

    if request.method == 'POST':
        data = request.POST.copy()
        footerKeyword = data.get('footer_keyword')
        header = data.get('header')
        # add footer model
        footerData = FooterKeywordModel.objects.get(id=fid)
        footerData.keyword_name = footerKeyword
        footerData.header = header
        footerData.page_list = pageData
        footerData.save()
        request.session['status'] = 'แก้ไขสำเร็จแล้ว'
        return redirect('page-footer-page', pid)

    # get title of page
    pageData = PageListModel.objects.get(id=pid)
    titleOfPage = pageData.title
    pageName = pageData.page_name

    footerData = FooterKeywordModel.objects.get(id=fid)

    context['titleOfPage'] = titleOfPage
    context['pageName'] = pageName
    context['footerData'] = footerData
    context['footerId'] = footerData.id
    context['pageId'] = pid
    context['navpage'] = 'keyword-manager'

    # if there is key status in request.session this will take value from session to context message
    if 'status' in request.session:
        context['message'] = request.session['status']
        del request.session['status']  # clear stuck status in session
    if 'error' in request.session:
        context['error'] = request.session['error']
        del request.session['error']  # clear stuck status in session

    return render(request, 'keywordapp/footer/footer-edit-manager.html', context)


@login_required
def PageListFooterDelete(request, pid, fid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    delete = FooterKeywordModel.objects.get(
        id=fid)
    delete.delete()

    request.session['status'] = 'ลบสำเร็จแล้ว'
    return redirect('page-footer-page', pid)


# =============================== LONGTAIL FOOTER KEYWORD ===============================
# =============================== LONGTAIL FOOTER KEYWORD ===============================
# =============================== LONGTAIL FOOTER KEYWORD ===============================


@login_required
def LongTailFooterKeyword(request, pid, f_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    # define var
    countFullKwKey = ''
    countShortKwKey = ''

    context = {}

    # Add data
    if request.method == 'POST':
        data = request.POST.copy()
        searchFrom = data.get('search_from')
        if searchFrom == 'paragraph':
            searchMode = data.get('search_mode')
            keywordSearch = data.get('keyword_search')
            if keywordSearch == '':
                request.session['error'] = 'กรุณากรอก Keyword'
                return redirect('longtail-footer-page', pid, f_kwid)
            keywordSearch = keywordSearch.strip()
            result = KeywordSearchFunction(request, keywordSearch, searchMode)
            # result to display in keyword search page
            # basic result
            refinePopularList = result[0]
            longtailList = result[1]
            refineAndReplatedList = result[2]
            uniqueDataList = result[9]

            try:
                # ลองหาว่ามีประเภทนี้หรือยัง ถ้ามีแล้วให้อัพเดท
                oldData = TempKeywordSearchModel.objects.get(
                    type='paragraph of main footer')
                oldData.keyword_search = keywordSearch
                oldData.refine_popular = refinePopularList
                oldData.longtail = longtailList
                oldData.related = refineAndReplatedList
                oldData.save()
            except:
                # ถ้าไม่มีให้เพิ่มเข้าไปในระบบ
                newTempKeywordSearch = TempKeywordSearchModel()
                newTempKeywordSearch.keyword_search = keywordSearch
                newTempKeywordSearch.refine_popular = refinePopularList
                newTempKeywordSearch.longtail = longtailList
                newTempKeywordSearch.related = refineAndReplatedList
                newTempKeywordSearch.type = 'paragraph of main footer'
                newTempKeywordSearch.save()

            if not refinePopularList and not longtailList and not refineAndReplatedList:
                request.session['title'] = 'หาไม่เจอ'
                request.session['alert'] = keywordSearch
                request.session['status_alert'] = 'error'
            else:
                request.session['title'] = 'เสร็จแล้ว'
                request.session['alert'] = keywordSearch
                request.session['status_alert'] = 'success'
                return redirect('longtail-footer-page', pid, f_kwid)
        else:
            #  ถ้าเป็นการเพิ่มข้อมูลแบบกดปุ่มจากตารางจะเข้าเงื่อไนขนี้
            if data.get('re_add') == 'True':
                fullLongtailKeyword = data.get('full_lt_keyword')
                fullLongtailKeyword = fullLongtailKeyword.strip()
            else:
                #  ถ้าเป็นการกดปุ่มเพิ่มด้วยตัวเองจะเข้าเงื่อนไขนี้
                fullLongtailKeyword = data.get('full_lt_keyword')
                fullLongtailKeyword = fullLongtailKeyword.strip()

            if fullLongtailKeyword == '':
                context['error'] = "กรุณากรอก Keyword"
                return redirect('longtail-footer-page', pid, f_kwid)
            else:
                # check duplicate
                result = CheckDuplicatedFooterLongtailKeyword(
                    fullLongtailKeyword, f_kwid)
                if result == 'duplicated':
                    request.session['error'] = 'มี Keyword นี้แล้ว'
                else:
                    newLTKeyword = LongTailFooterKeywordModel()
                    newLTKeyword.longtail_name = fullLongtailKeyword
                    newLTKeyword.shorten_name = fullLongtailKeyword
                    newLTKeyword.link_href = ""
                    newLTKeyword.link_href_shorten_name = ""
                    newLTKeyword.footer_keyword = FooterKeywordModel.objects.get(
                        id=f_kwid)
                    newLTKeyword.save()
                    AddCountKeyToDb(fullLongtailKeyword, 2, pid)
                request.session['status'] = 'เพิ่มข้อมูลแล้ว'

                return redirect('longtail-footer-page', pid, f_kwid)

    # =====================START: DATA FOR PAGE ================
    longtailKeywordModel = LongTailFooterKeywordModel.objects.filter(
        footer_keyword_id=f_kwid)

    keywordModel = FooterKeywordModel.objects.get(id=f_kwid)

    attribute = "longtail_name"
    resultDeleteDuplicate = DeleteDuplicateFromGettingDataInDb(
        longtailKeywordModel, attribute)
    uniqueDataList = resultDeleteDuplicate[0]
    uniqueDataList2WordExceedList = resultDeleteDuplicate[1]
    numberOfUniqueDataListToString = resultDeleteDuplicate[2]
    numberOfUniqueDataListToString2WordExceed = resultDeleteDuplicate[3]

    # count all character
    attribute = "longtail_name"
    lengthFullKeyword = CountCharacterLength(longtailKeywordModel, attribute)
    attribute = "shorten_name"
    lengthShortKeyword = CountCharacterLength(longtailKeywordModel, attribute)

    # ================ END: DATA FOR PAGE ================

    # ================ START: KEYWORD HEALTH ================ #
    # FULL_KEYWORDS
    uniqueDataFullKwList = []
    for data in longtailKeywordModel:
        fullKeyword = data.longtail_name
        # Cut duplicate word by space bar
        fullKeywordSplit = fullKeyword.split()
        for x in fullKeywordSplit:
            uniqueDataFullKwList.append(x)
    counter = Counter(uniqueDataFullKwList).most_common()
    countFullKwKey = dict(counter)
    # SHORT_KEYWORDS
    uniqueDataShortKwList = []
    for data in longtailKeywordModel:
        shortKeyword = data.shorten_name
        # Cut duplicate word by space bar
        shortKeywordSplit = shortKeyword.split()
        for x in shortKeywordSplit:
            uniqueDataShortKwList.append(x)
    counter = Counter(uniqueDataShortKwList).most_common()
    countShortKwKey = dict(counter)
    # ================ END: KEYWORD HEALTH ================ #

    # ================ START : MAP DATA FOR TABLE ================ #
    comeFrom = 'paragraph of main keyword'
    loopMode = 'loop'
    zipDataForLoop = GetZipDataForLoopInTable(
        request, longtailKeywordModel, comeFrom, loopMode, pid)
    # ================ END : MAP DATA FOR TABLE ================ #

    # ================= START : DATA FOR GOOGLE TABLE ================= #
    try:
        tempKeywordData = TempKeywordSearchModel.objects.get(
            type='paragraph of main footer')
        keywordSearch = tempKeywordData.keyword_search
        refinePopularList = tempKeywordData.refine_popular
        longtailList = tempKeywordData.longtail
        refineAndReplatedList = tempKeywordData.related

        resultConvert = ConvertDataOfGoogleTableFromStringToList(
            refinePopularList, longtailList, refineAndReplatedList)
        refinePopularListConverted = resultConvert[0]
        longtailListConverted = resultConvert[1]
        refineAndReplatedListConverted = resultConvert[2]
    except:
        keywordSearch = ''
        refinePopularList = ''
        longtailList = ''
        refineAndReplatedList = ''
        refinePopularListConverted = ''
        longtailListConverted = ''
        refineAndReplatedListConverted = ''

    # ================= END : DATA FOR GOOGLE TABLE ================= #

    # set context
    context['uniqueDataList'] = uniqueDataList
    context['uniqueDataList2WordExceedList'] = uniqueDataList2WordExceedList
    context['numberOfUniqueDataListToString'] = numberOfUniqueDataListToString
    context['numberOfUniqueDataListToString2WordExceed'] = numberOfUniqueDataListToString2WordExceed
    context['lengthFullKeyword'] = lengthFullKeyword
    context['lengthShortKeyword'] = lengthShortKeyword
    context['longtailKeywordModel'] = longtailKeywordModel
    context['footerId'] = f_kwid
    context['pageId'] = pid
    context['keywordModel'] = keywordModel
    context['zipDataForLoop'] = zipDataForLoop
    context['navpage'] = 'keyword-manager'

    # Search keyword from google
    context['refinePopularList'] = refinePopularListConverted
    context['longtailList'] = longtailListConverted
    context['refineAndReplatedList'] = refineAndReplatedListConverted
    context['keywordSearch'] = keywordSearch

    # health word check
    context['countFullKwKey'] = countFullKwKey
    context['countShortKwKey'] = countShortKwKey

    if 'error' in request.session:
        if request.session['error'] == '':
            del request.session['error']
        else:
            context['error'] = request.session['error']
            del request.session['error']
    elif 'status' in request.session:
        if request.session['status'] == '':
            del request.session['status']
        else:
            context['message'] = request.session['status']
            del request.session['status']
    return render(request, 'keywordapp/footer/page-footer-paragraph-manager.html', context)


@login_required
def LongTailFooterKeywordEdit(request, pid, f_kwid, lt_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    context = {}
    # Edit data
    editData = LongTailFooterKeywordModel.objects.get(
        id=lt_kwid)

    # Update data
    if request.method == 'POST':
        data = request.POST.copy()
        longtailName = data.get('longtail_name')
        longtailName = longtailName.strip()
        shortenName = data.get('shorten_name')
        shortenName = shortenName.strip()
        linkHref = data.get('link_href')
        linkHref = linkHref.strip()
        linkHrefShortenName = data.get('link_href_shorten_name')
        linkHrefShortenName = linkHrefShortenName.strip()
        # if longtail name is empty
        if longtailName == '':
            context['error'] = "กรุณากรอก Keyword"
        else:
            if editData.longtail_name != longtailName:
                # check duplicate
                result = CheckDuplicatedFooterLongtailKeyword(
                    longtailName, f_kwid)
                if result == 'duplicated':
                    request.session['error'] = 'มี Keyword นี้แล้ว'
                    return redirect('longtail-footer-edit-page', pid, f_kwid, lt_kwid)
            # if shorten keyword is empty replace with full keyword
            if shortenName == '':
                shortenName = longtailName

            oldData = LongTailFooterKeywordModel.objects.get(id=lt_kwid)
            # เอาข้อมูลเก่ามาเก็บไว้ก่อน สำหรับไปลดจำนวนตัวเก่า
            oldFullKw = oldData.longtail_name
            oldShortKw = oldData.shorten_name
            # edit count key amount
            ManageCountKeyOnEdit(
                oldFullKw, oldShortKw, longtailName, shortenName, pid)
            editData.longtail_name = longtailName
            editData.shorten_name = shortenName
            editData.link_href = linkHref
            editData.link_href_shorten_name = linkHrefShortenName
            editData.footer_keyword = FooterKeywordModel.objects.get(id=f_kwid)
            editData.save()

            request.session['status'] = 'แก้ไขสำเร็จแล้ว'
            return redirect('longtail-footer-page', pid, f_kwid)

    context['editData'] = editData
    context['footerId'] = f_kwid
    context['pageId'] = pid
    context['navpage'] = 'keyword-manager'

    if 'error' in request.session:
        context['error'] = request.session['error']
        del request.session['error']  # clear stuck error in session

    return render(request, 'keywordapp/footer/page-foorter-paragraph-edit-manager.html', context)


@login_required
def LongTailFooterKeywordDelete(request, pid, f_kwid, lt_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    # Add data
    deleteData = LongTailFooterKeywordModel.objects.get(
        id=lt_kwid)
    fullKeyword = deleteData.longtail_name
    shortKeyword = deleteData.shorten_name
    # reduce amount of the old one
    AdjustCountKeyToDb(fullKeyword, 'minus', 1, pid)
    # reduce amount of the old one
    AdjustCountKeyToDb(shortKeyword, 'minus', 1, pid)
    deleteData.delete()

    request.session['status'] = 'ลบสำเร็จแล้ว'
    return redirect('longtail-footer-page', pid, f_kwid)


# =============================== SUB FOOTER ===============================
# =============================== SUB FOOTER ===============================
# =============================== SUB FOOTER ===============================

@login_required
def PageListSubFooterEdit(request, pid, f_kwid, sf_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    context = {}

    footerDataObject = FooterKeywordModel.objects.get(id=f_kwid)

    if request.method == 'POST':
        data = request.POST.copy()
        footerKeyword = data.get('footer_keyword')
        header = data.get('header')
        # add footer model
        footerData = SubFooterKeywordModel.objects.get(id=sf_kwid)
        footerData.keyword_name = footerKeyword
        footerData.header = header
        footerData.footer_keyword = footerDataObject
        footerData.save()
        request.session['status'] = 'แก้ไขสำเร็จแล้ว'
        return redirect('page-footer-page', pid)

    # get title of page
    pageData = PageListModel.objects.get(id=pid)
    titleOfPage = pageData.title
    pageName = pageData.page_name

    footerSubDataObject = SubFooterKeywordModel.objects.get(id=sf_kwid)

    context['titleOfPage'] = titleOfPage
    context['pageName'] = pageName
    context['footerData'] = footerSubDataObject
    context['footerIdForSubFooter'] = f_kwid
    context['subFooterId'] = sf_kwid
    context['pageId'] = pid
    context['navpage'] = 'keyword-manager'

    # if there is key status in request.session this will take value from session to context message
    if 'status' in request.session:
        context['message'] = request.session['status']
        del request.session['status']  # clear stuck status in session
    if 'error' in request.session:
        context['error'] = request.session['error']
        del request.session['error']  # clear stuck status in session

    return render(request, 'keywordapp/footer/footer-edit-manager.html', context)


@login_required
def PageListSubFooterDelete(request, pid, sf_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    delete = SubFooterKeywordModel.objects.get(
        id=sf_kwid)
    delete.delete()

    request.session['status'] = 'ลบสำเร็จแล้ว'
    return redirect('page-footer-page', pid)


# =============================== LONGTAIL SUB FOOTER KEYWORD ===============================
# =============================== LONGTAIL SUB FOOTER KEYWORD ===============================
# =============================== LONGTAIL SUB FOOTER KEYWORD ===============================


@login_required
def LongTailSubFooterKeyword(request, pid, sf_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    # define var
    countFullKwKey = ''
    countShortKwKey = ''

    context = {}

    # Add data
    if request.method == 'POST':
        data = request.POST.copy()
        fullLongtailKeyword = data.get('full_lt_keyword')
        fullLongtailKeyword = fullLongtailKeyword.strip()
        shortLongtailKeyword = data.get('short_lt_keyword')
        shortLongtailKeyword = shortLongtailKeyword.strip()
        linkHref = data.get('link_href')
        linkHref = linkHref.strip()
        linkHrefShortenName = data.get('link_href_shorten_name')
        linkHrefShortenName = linkHrefShortenName.strip()

        if fullLongtailKeyword == '':
            context['error'] = "กรุณากรอก Keyword"
            return redirect('longtail-sub-footer-page', pid,)
        else:
            # check duplicate
            result = CheckDuplicatedSubFooterLongtailKeyword(
                fullLongtailKeyword, sf_kwid)
            if result == 'duplicated':
                request.session['error'] = 'มี Keyword นี้แล้ว'
            else:
                # if shorten keyword is empty replace with full keyword
                if shortLongtailKeyword == '':
                    shortLongtailKeyword = fullLongtailKeyword
                newLTKeyword = LongTailSubFooterKeywordModel()
                newLTKeyword.longtail_name = fullLongtailKeyword
                newLTKeyword.shorten_name = shortLongtailKeyword
                newLTKeyword.link_href = linkHref
                newLTKeyword.link_href_shorten_name = linkHrefShortenName
                newLTKeyword.sub_footer_keyword = SubFooterKeywordModel.objects.get(
                    id=sf_kwid)
                newLTKeyword.save()
                AddCountKeyToDb(fullLongtailKeyword, 2, pid)
            request.session['status'] = 'เพิ่มข้อมูลแล้ว'

            return redirect('longtail-sub-footer-page', pid, sf_kwid)

    # =====================START: DATA FOR PAGE ================
    longtailKeywordModel = LongTailSubFooterKeywordModel.objects.filter(
        sub_footer_keyword_id=sf_kwid)

    keywordModel = SubFooterKeywordModel.objects.get(id=sf_kwid)

    attribute = "longtail_name"
    resultDeleteDuplicate = DeleteDuplicateFromGettingDataInDb(
        longtailKeywordModel, attribute)
    uniqueDataList = resultDeleteDuplicate[0]
    uniqueDataList2WordExceedList = resultDeleteDuplicate[1]
    numberOfUniqueDataListToString = resultDeleteDuplicate[2]
    numberOfUniqueDataListToString2WordExceed = resultDeleteDuplicate[3]

    # count all character
    attribute = "longtail_name"
    lengthFullKeyword = CountCharacterLength(longtailKeywordModel, attribute)
    attribute = "shorten_name"
    lengthShortKeyword = CountCharacterLength(longtailKeywordModel, attribute)

    # ================ END: DATA FOR PAGE ================

    # ================ START: KEYWORD HEALTH ================ #
    # FULL_KEYWORDS
    uniqueDataFullKwList = []
    for data in longtailKeywordModel:
        fullKeyword = data.longtail_name
        # Cut duplicate word by space bar
        fullKeywordSplit = fullKeyword.split()
        for x in fullKeywordSplit:
            uniqueDataFullKwList.append(x)
    counter = Counter(uniqueDataFullKwList).most_common()
    countFullKwKey = dict(counter)
    # SHORT_KEYWORDS
    uniqueDataShortKwList = []
    for data in longtailKeywordModel:
        shortKeyword = data.shorten_name
        # Cut duplicate word by space bar
        shortKeywordSplit = shortKeyword.split()
        for x in shortKeywordSplit:
            uniqueDataShortKwList.append(x)
    counter = Counter(uniqueDataShortKwList).most_common()
    countShortKwKey = dict(counter)
    # ================ END: KEYWORD HEALTH ================ #
    # set context
    context['uniqueDataList'] = uniqueDataList
    context['uniqueDataList2WordExceedList'] = uniqueDataList2WordExceedList
    context['numberOfUniqueDataListToString'] = numberOfUniqueDataListToString
    context['numberOfUniqueDataListToString2WordExceed'] = numberOfUniqueDataListToString2WordExceed
    context['lengthFullKeyword'] = lengthFullKeyword
    context['lengthShortKeyword'] = lengthShortKeyword
    context['longtailKeywordModel'] = longtailKeywordModel
    context['subFooterId'] = sf_kwid
    context['pageId'] = pid
    context['keywordModel'] = keywordModel
    context['navpage'] = 'keyword-manager'

    # health word check
    context['countFullKwKey'] = countFullKwKey
    context['countShortKwKey'] = countShortKwKey

    if 'error' in request.session:
        if request.session['error'] == '':
            del request.session['error']
        else:
            context['error'] = request.session['error']
            del request.session['error']
    elif 'status' in request.session:
        if request.session['status'] == '':
            del request.session['status']
        else:
            context['message'] = request.session['status']
            del request.session['status']
    return render(request, 'keywordapp/footer/page-footer-paragraph-manager.html', context)


@login_required
def LongTailSubFooterKeywordEdit(request, pid, sf_kwid, ltsf_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    context = {}
    # Edit data
    editData = LongTailSubFooterKeywordModel.objects.get(
        id=ltsf_kwid)

    # Update data
    if request.method == 'POST':
        data = request.POST.copy()
        longtailName = data.get('longtail_name')
        longtailName = longtailName.strip()
        shortenName = data.get('shorten_name')
        shortenName = shortenName.strip()
        linkHref = data.get('link_href')
        linkHref = linkHref.strip()
        linkHrefShortenName = data.get('link_href_shorten_name')
        linkHrefShortenName = linkHrefShortenName.strip()
        if longtailName == '':
            context['error'] = "กรุณากรอก Keyword"
        else:
            # if old full keyword equal new full keyword don't check this
            if editData.longtail_name != longtailName:
                # check duplicate
                result = CheckDuplicatedSubLongtailKeyword(
                    longtailName, sf_kwid)
                if result == 'duplicated':
                    request.session['error'] = 'มี Keyword นี้แล้ว'
                    return redirect('longtail-subkeyword-edit-page', pid, sf_kwid, ltsf_kwid)
            # if shorten keyword is empty replace with full keyword
            if shortenName == '':
                shortenName = longtailName
            oldData = LongTailSubFooterKeywordModel.objects.get(id=ltsf_kwid)
            # เอาข้อมูลเก่ามาเก็บไว้ก่อน สำหรับไปลดจำนวนตัวเก่า
            oldFullKw = oldData.longtail_name
            oldShortKw = oldData.shorten_name
            # edit count key amount
            ManageCountKeyOnEdit(
                oldFullKw, oldShortKw, longtailName, shortenName, pid)
            editData.longtail_name = longtailName
            editData.shorten_name = shortenName
            editData.link_href = linkHref
            editData.link_href_shorten_name = linkHrefShortenName
            editData.sub_footer = SubFooterKeywordModel.objects.get(id=sf_kwid)
            editData.save()

            request.session['status'] = 'แก้ไขสำเร็จแล้ว'
            return redirect('longtail-sub-footer-page', pid, sf_kwid)

    context['editData'] = editData
    context['pageId'] = pid
    context['subFooterId'] = sf_kwid
    context['navpage'] = 'keyword-manager'

    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''  # clear stuck status in session

    return render(request, 'keywordapp/footer/page-foorter-paragraph-edit-manager.html', context)


@login_required
def LongTailSubFooterKeywordDelete(request, pid, sf_kwid, ltsf_kwid):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # check page owner
    checkOwner = CheckPageListOwner(request, pid)
    if checkOwner == 'cannot':
        return redirect('weblist-page')

    # Add data
    deleteData = LongTailSubFooterKeywordModel.objects.get(
        id=ltsf_kwid)
    fullKeyword = deleteData.longtail_name
    shortKeyword = deleteData.shorten_name
    # reduce amount of the old one
    AdjustCountKeyToDb(fullKeyword, 'minus', 1, pid)
    # reduce amount of the old one
    AdjustCountKeyToDb(shortKeyword, 'minus', 1, pid)
    deleteData.delete()

    request.session['status'] = 'ลบสำเร็จแล้ว'
    return redirect('longtail-sub-footer-page', pid, sf_kwid)


def ArticlePost(request, aid):
    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckRootUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')
    context = {}
    articleData = ArticlePageModel.objects.get(id=aid)
    context['navpage'] = "promotion"
    context['header'] = articleData.article_title
    context['owner'] = articleData.author
    context['imageLink'] = articleData.image_link
    context['imageAlt'] = articleData.image_alt
    context['date'] = articleData.publish_date
    context['paragraph'] = articleData.content

    # loop to get each tag in article data
    sumTag = []

    # get all tag in article data
    allTag = articleData.tag.all()
    countAllTag = len(allTag)

    for i, tag in enumerate(allTag):
        tagLoop = "<a href='#' class='elementor-post-info__terms-list-item'>{}</a>".format(
            tag)
        sumTag.append(tagLoop)

        # if this is last result it won't create comma
        if i != countAllTag-1:
            sumTag.append(',')

    context['tag'] = sumTag
    return render(request, 'page/article/article-content.html', context)


# ==================== START : ฟังก์ชั่นสำหรับการดึงข้อมูลทั้งระบบ ========================= #
# ==================== START : ฟังก์ชั่นสำหรับการดึงข้อมูลทั้งระบบ ========================= #
# ==================== START : ฟังก์ชั่นสำหรับการดึงข้อมูลทั้งระบบ ========================= #
# เอาข้อมูล longtail ทั้งหมดมาตัดตัวซ้ำและเพิ่มเข้าไปในตาราง count keyword
@login_required
def ImportKeywordInAllLongtailToCountKeywordTable(request):
    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckRootUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    # Reset Keyword amount
    CountKeywordModelInAllPage.objects.all().delete()
    # Need to get Unique keyword from all then let these unique check amount
    uniqueKeywordList = []
    # get data from all longtail type
    metaDes = PageListMetaDescriptionModel.objects.all()
    for metaDesEach in metaDes:
        fullKeyword = metaDesEach.full_keyword
        shortKeyword = metaDesEach.shorten_keyword
        if fullKeyword not in uniqueKeywordList:
            uniqueKeywordList.append(fullKeyword)
        if shortKeyword not in uniqueKeywordList:
            uniqueKeywordList.append(shortKeyword)
    longtailKw = LongTailKeywordModel.objects.all()
    for longtailKwEach in longtailKw:
        fullKeyword = longtailKwEach.longtail_name
        shortKeyword = longtailKwEach.shorten_name
        if fullKeyword not in uniqueKeywordList:
            uniqueKeywordList.append(fullKeyword)
        if shortKeyword not in uniqueKeywordList:
            uniqueKeywordList.append(shortKeyword)
    longtailSkw = LongTailSubKeywordModel.objects.all()
    for longtailSkwEach in longtailSkw:
        fullKeyword = longtailSkwEach.longtail_name
        shortKeyword = longtailSkwEach.shorten_name
        if fullKeyword not in uniqueKeywordList:
            uniqueKeywordList.append(fullKeyword)
        if shortKeyword not in uniqueKeywordList:
            uniqueKeywordList.append(shortKeyword)
    longtailFmkw = LongTailFooterKeywordModel.objects.all()
    for longtailFmkwEach in longtailFmkw:
        fullKeyword = longtailFmkwEach.longtail_name
        shortKeyword = longtailFmkwEach.shorten_name
        if fullKeyword not in uniqueKeywordList:
            uniqueKeywordList.append(fullKeyword)
        if shortKeyword not in uniqueKeywordList:
            uniqueKeywordList.append(shortKeyword)
    longtailFskw = LongTailSubFooterKeywordModel.objects.all()
    for longtailFskwEach in longtailFskw:
        fullKeyword = longtailFskwEach.longtail_name
        shortKeyword = longtailFskwEach.shorten_name
        if fullKeyword not in uniqueKeywordList:
            uniqueKeywordList.append(fullKeyword)
        if shortKeyword not in uniqueKeywordList:
            uniqueKeywordList.append(shortKeyword)
    nowKeyword = 0
    allKeyword = len(uniqueKeywordList)
    for keyword in uniqueKeywordList:
        # Show percent while working
        nowKeyword = nowKeyword + 1
        percent = (nowKeyword*100)/allKeyword
        print(percent, "%")
        pageObject = PageListModel.objects.all()
        for data in pageObject:
            pageId = data.id
            # = เช็คใน Meta Description
            # เช็ค Full kw
            ckwDataFkw = PageListMetaDescriptionModel.objects.filter(
                full_keyword=keyword, page_list_id=pageId)
            amountFkw = len(ckwDataFkw)
            if amountFkw > 0:
                AddCountKeyToDb(keyword, amountFkw, pageId)
            #  เช็ค Short kw
            ckwDataSkw = PageListMetaDescriptionModel.objects.filter(
                shorten_keyword=keyword, page_list_id=pageId)
            amountSkw = len(ckwDataSkw)
            if amountSkw > 0:
                AddCountKeyToDb(keyword, amountSkw, pageId)
            # = เช็คใน Main Paragraph
            mainKwObject = MainKeywordModel.objects.filter(page_list_id=pageId)
            for mainKw in mainKwObject:
                # เช็ค Full kw
                ckwDataLt = LongTailKeywordModel.objects.filter(
                    longtail_name=keyword, main_keyword_id=mainKw.id)
                amountFkwLt = len(ckwDataLt)
                if amountFkwLt > 0:
                    AddCountKeyToDb(keyword, amountFkwLt, pageId)
                #  เช็ค Short kw
                # ตอนนี้จำนวนล่าสุดคือตัวที่คำนวณมาก่อนหน้าแล้ว
                ckwDataSLt = LongTailKeywordModel.objects.filter(
                    shorten_name=keyword, main_keyword_id=mainKw.id)
                amountSkwLt = len(ckwDataSLt)
                if amountSkwLt > 0:
                    AddCountKeyToDb(keyword, amountSkwLt, pageId)

                # = เช็คใน Sub Paragraph
                # List sub keyword ของ Main Keyword นี้ออกมาก่อน
                subKwObject = SubKeywordModel.objects.filter(
                    main_keyword_id=mainKw.id)
                # เอา sub keyword แต่ละตัวไปวนซ้ำเพื่อเอา id ให้กับ longtail sub keyword แต่ละตัว
                for subKw in subKwObject:
                    # เช็ค Full kw
                    ckwDataSlt = LongTailSubKeywordModel.objects.filter(
                        longtail_name=keyword, sub_keyword_id=subKw.id)
                    amountFkwSlt = len(ckwDataSlt)
                    if amountFkwSlt > 0:
                        AddCountKeyToDb(keyword, amountFkwSlt, pageId)
                    # เช็ค Short kw
                    ckwDataSlt = LongTailSubKeywordModel.objects.filter(
                        shorten_name=keyword, sub_keyword_id=subKw.id)
                    amountSkwSlt = len(ckwDataSlt)
                    if amountSkwSlt > 0:
                        AddCountKeyToDb(keyword, amountSkwSlt, pageId)
            # = เช็คใน Footer keyword
            footerKwObject = FooterKeywordModel.objects.filter(
                page_list_id=pageId)
            for footerKw in footerKwObject:
                # เช็ค Full kw
                ckwDataLt = LongTailFooterKeywordModel.objects.filter(
                    longtail_name=keyword, footer_keyword_id=footerKw.id)
                amountFkwLt = len(ckwDataLt)
                if amountFkwLt > 0:
                    AddCountKeyToDb(keyword, amountFkwLt, pageId)
                #  เช็ค Short kw
                # ตอนนี้จำนวนล่าสุดคือตัวที่คำนวณมาก่อนหน้าแล้ว
                ckwDataSLt = LongTailFooterKeywordModel.objects.filter(
                    shorten_name=keyword, footer_keyword_id=footerKw.id)
                amountSkwLt = len(ckwDataSLt)
                if amountSkwLt > 0:
                    AddCountKeyToDb(keyword, amountSkwLt, pageId)
                # = เช็คใน Sub Footer keyword
                # List sub keyword ของ Main Keyword นี้ออกมาก่อน
                subFskwObject = SubFooterKeywordModel.objects.filter(
                    footer_keyword_id=footerKw.id)
                # เอา sub keyword แต่ละตัวไปวนซ้ำเพื่อเอา id ให้กับ longtail sub keyword แต่ละตัว
                for subFkw in subFskwObject:
                    # เช็ค Full kw
                    ckwDataSlt = LongTailSubFooterKeywordModel.objects.filter(
                        longtail_name=keyword, sub_footer_keyword_id=subFkw.id)
                    amountFkwSlt = len(ckwDataSlt)
                    if amountFkwSlt > 0:
                        AddCountKeyToDb(keyword, amountFkwSlt, pageId)
                    # เช็ค Short kw
                    ckwDataSlt = LongTailSubFooterKeywordModel.objects.filter(
                        shorten_name=keyword, sub_footer_keyword_id=subFkw.id)
                    amountSkwSlt = len(ckwDataSlt)
                    if amountSkwSlt > 0:
                        AddCountKeyToDb(keyword, amountSkwSlt, pageId)

    return redirect('weblist-page')

# เอาข้อมูล keyword name จาก ตาราง count keyword มาตัดคำซ้ำแล้วเพิ่มเข้าตาราง count keyword this page ที่เป็นตารางรวม


# ==================== END : ฟังก์ชั่นสำหรับการดึงข้อมูลทั้งระบบ ========================= #
# ==================== END : ฟังก์ชั่นสำหรับการดึงข้อมูลทั้งระบบ ========================= #
# ==================== END : ฟังก์ชั่นสำหรับการดึงข้อมูลทั้งระบบ ========================= #

    # ================ CRUD AJAX ================ #
    # ================ CRUD AJAX ================ #
    # ================ CRUD AJAX ================ #
    # ================ CRUD AJAX ================ #
    # ================ CRUD AJAX ================ #
    # ================ CRUD AJAX ================ #
    # ================ CRUD AJAX ================ #


@login_required
def PageListCrud(request):

    expireDate = request.user.profilemodel.expire_date
    userId = request.user.id
    resultCheckExpire = CheckExpireDate(expireDate, userId)
    if resultCheckExpire == 'ตัดสิทธิ์แล้ว':
        return redirect('Home')

    # if have no permission cannot enter this page
    checkPermission = CheckSuperPremiumUser(request)
    if checkPermission == 'Have no permission':
        return redirect('Home')

    user = User.objects.get(id=request.user.id)

    context = {}
    pageListModel = PageListModel.objects.filter(user=user)

    context['pageListModel'] = pageListModel
    context['navpage'] = 'crud-page'

    return render(request, 'keywordapp/crud/pagelist/page-list-manager-crud.html', context)


# เขียนแบบ Class-Based
# from django.views.generic import ListView,View #ให้ใช้ ListView ได้
# from django.http import JsonResponse
# class CrudView(ListView):  # ต้องเอา ListView มาใส่ให้กลายเป็น Class-based
#     model = CrudUser  # เราจะใช้ model ที่ชื่อว่า user
#     template_name = 'keywordapp/crud/crud.html'
#     context_object_name = 'users'  # แนบตัวแปร context เข้าไปโดยใช้ key ชื่อว่า
def CrudView(request, pid):
    context = {}
    # ================ START : Page List Data ================ #
    #  filter meta description
    pagelistMetaObject = PageListMetaDescriptionModel.objects.filter(
        page_list_id=pid)
    # keyword for showing in sum keyword section
    concatenateFkList = []
    concatenateSkList = []
    for data in pagelistMetaObject:
        concatenateFkList.append(data.full_keyword)
        concatenateSkList.append(data.shorten_keyword)
    concatenateFkJoin = " ".join(concatenateFkList)
    concatenateSkJoin = " ".join(concatenateSkList)
    context['concatenateFk'] = concatenateFkJoin
    context['concatenateSk'] = concatenateSkJoin

    # prepare data for looping
    comeFrom = 'meta description'
    loopMode = 'loop'
    zipDataForLoop = GetZipDataForLoopInTable(
        request, pagelistMetaObject, comeFrom, loopMode, pid)
    context['pagelistMetaDesList'] = zipDataForLoop
    # page data
    pagelistObject = PageListModel.objects.get(id=pid)
    context['pageData'] = pagelistObject
    # ================ END : Page List Data ================ #

    # ================ START : META DES COUNT CHARACTER ================ #
    # count all character
    attribute = "full_keyword"
    lengthFullKeyword = CountCharacterLength(pagelistMetaObject, attribute)
    attribute = "shorten_keyword"
    lengthShortKeyword = CountCharacterLength(pagelistMetaObject, attribute)
    context['lengthFullKeyword'] = lengthFullKeyword
    context['lengthShortKeyword'] = lengthShortKeyword
    # ================ END : META DES COUNT CHARACTER ================ #

    # ================ START : META DES DELETE DUPLICATE ================ #
    # meta description data with delete duplicate
    attribute = "full_keyword"
    resultDeleteDuplicate = DeleteDuplicateFromGettingDataInDb(
        pagelistMetaObject, attribute)
    uniqueDataList = resultDeleteDuplicate[0]
    uniqueDataList2WordExceedList = resultDeleteDuplicate[1]
    numberOfUniqueDataListToString = resultDeleteDuplicate[2]
    numberOfUniqueDataListToString2WordExceed = resultDeleteDuplicate[3]
    context['uniqueDataList'] = uniqueDataList
    context['uniqueDataList2WordExceedList'] = uniqueDataList2WordExceedList
    context['numberOfUniqueDataListToString'] = numberOfUniqueDataListToString
    context['numberOfUniqueDataListToString2WordExceed'] = numberOfUniqueDataListToString2WordExceed
    context['navpage'] = 'crud-page'

    # ================ END : META DES DELETE DUPLICATE ================ #

    return render(request, 'keywordapp/crud/crud.html', context)

    # ================ START : CRUD PAGE LIST ================ #
    # ================ START : CRUD PAGE LIST ================ #
    # ================ START : CRUD PAGE LIST ================ #


class CreateCrudPageList(View):
    def get(self, request):
        pageName = request.GET.get('page_name', None)
        title = request.GET.get('title', None)

        newPage = PageListModel.objects.create(
            page_name=pageName,
            title=title,
            user=User.objects.get(username=request.user.username)
        )
        # Send back data to html ajax
        newPageObject = {
            'id': newPage.id,
            'page_name': newPage.page_name,
            'title': newPage.title,
        }
        context = {
            'newPageObject': newPageObject
        }
        return JsonResponse(context)

    # ================ END : CRUD PAGE LIST ================ #
    # ================ END : CRUD PAGE LIST ================ #
    # ================ END : CRUD PAGE LIST ================ #

    # ================ START : CRUD META DESCRIPTION ================ #
    # ================ START : CRUD META DESCRIPTION ================ #
    # ================ START : CRUD META DESCRIPTION ================ #


class CreateCrudMetaDescription(View):
    def get(self, request):

        fullKeyword = request.GET.get('full_keyword', None)
        pageId = request.GET.get('page_id', None)
    # ADD DATA
      # check duplicate
        result = CheckDuplicatedMetaDescription(
            fullKeyword, pageId)
        if result != 'duplicated':
            newMetaDes = PageListMetaDescriptionModel.objects.create(
                full_keyword=fullKeyword,
                shorten_keyword=fullKeyword,
                page_list=PageListModel.objects.get(id=pageId)
            )
            # add data to count key table
            AddCountKeyToDb(fullKeyword, 2, pageId)
        else:
            return JsonResponse(status=404)

        # ================ START : MAP DATA FOR TABLE ================ #
        comeFrom = 'meta description'
        loopMode = 'not loop'
        zipDataForLoop = GetZipDataForLoopInTable(
            request, newMetaDes, comeFrom, loopMode, pageId)
        for data in zipDataForLoop:
            keywordIdList = data[0]
            fullKeywordList = data[1]
            sumKeywordInThisPageFullKwList = data[2]
            sumAmountAllPageFkwList = data[3]
            shortKeywordList = data[4]
            sumKeywordInThisPageShortKwList = data[5]
            sumAmountAllPageSkwList = data[6]
        # get number of meta description
        pagelistMetaDesObject = PageListMetaDescriptionModel.objects.filter(
            page_list_id=pageId)
        amountMetaDes = len(pagelistMetaDesObject)
        # ================ END : MAP DATA FOR TABLE ================ #
        # ================ START : COUNT CHARACTER ================ #
        # count all character
        attribute = "full_keyword"
        lengthFullKeyword = CountCharacterLength(
            pagelistMetaDesObject, attribute)
        attribute = "shorten_keyword"
        lengthShortKeyword = CountCharacterLength(
            pagelistMetaDesObject, attribute)
        # ================ END : COUNT CHARACTER ================ #

        # Send back data to html ajax
        newMetaDesList = {
            'counter': amountMetaDes,
            'id': keywordIdList,
            'page_id': pageId,
            'full_keyword': fullKeywordList,
            'amount_this_page_fk': sumKeywordInThisPageFullKwList,
            'amount_all_page_fk': sumAmountAllPageFkwList,
            'shorten_keyword': shortKeywordList,
            'amount_this_page_sk': sumKeywordInThisPageShortKwList,
            'amount_all_page_sk': sumAmountAllPageSkwList,
            'length_fk': lengthFullKeyword,
            'length_sk': lengthShortKeyword,
        }
        context = {
            'newMetaDesList': newMetaDesList
        }
        return JsonResponse(context)


class UpdateCrudMetaDescription(View):
    def get(self, request):
        keywordId = request.GET.get('keyword_id', None)
        fullKeyword = request.GET.get('full_keyword', None)
        shortKeyword = request.GET.get('shorten_keyword', None)
        pageId = request.GET.get('page_id', None)

        updateMetaDesObject = PageListMetaDescriptionModel.objects.get(
            id=keywordId)
        print("updateMetaDesObject : ", updateMetaDesObject)
        # เอาข้อมูลเก่ามาเก็บไว้ก่อน สำหรับไปลดจำนวนตัวเก่า
        oldFullKw = updateMetaDesObject.full_keyword
        oldShortKw = updateMetaDesObject.shorten_keyword
        # edit count key amount
        ManageCountKeyOnEdit(oldFullKw, oldShortKw, fullKeyword,
                             shortKeyword, pageId)

        updateMetaDesObject.full_keyword = fullKeyword
        updateMetaDesObject.shorten_keyword = shortKeyword
        updateMetaDesObject.save()

        # หลังจากเราเพิ่มข้อมูลเข้าฐานข้อมูลแล้ว เราต้องดึงข้อมูลใหม่อีกครั้ง เพื่อเอาข้อมูลล่าสุดออกไปแสดงที่ตาราง
        currentMetaDesObject = PageListMetaDescriptionModel.objects.get(
            id=keywordId)

        # ================ START : MAP DATA FOR TABLE ================ #
        comeFrom = 'meta description'
        loopMode = 'not loop'
        zipDataForLoop = GetZipDataForLoopInTable(
            request, currentMetaDesObject, comeFrom, loopMode, pageId)
        for data in zipDataForLoop:
            keywordIdList = data[0]
            fullKeywordList = data[1]
            sumKeywordInThisPageFullKwList = data[2]
            sumAmountAllPageFkwList = data[3]
            shortKeywordList = data[4]
            sumKeywordInThisPageShortKwList = data[5]
            sumAmountAllPageSkwList = data[6]
        # get number of meta description
        pagelistMetaDesObject = PageListMetaDescriptionModel.objects.filter(
            page_list_id=pageId)
        amountMetaDes = len(pagelistMetaDesObject)
        # ================ END : MAP DATA FOR TABLE ================ #
        updateMetaDesList = {
            'counter': amountMetaDes,
            'id': keywordIdList,
            'full_keyword': fullKeywordList,
            'amount_this_page_fk': sumKeywordInThisPageFullKwList,
            'amount_all_page_fk': sumAmountAllPageFkwList,
            'shorten_keyword': shortKeywordList,
            'amount_this_page_sk': sumKeywordInThisPageShortKwList,
            'amount_all_page_sk': sumAmountAllPageSkwList,
        }
        context = {
            'updateMetaDesList': updateMetaDesList
        }
        print("context : ", context)
        return JsonResponse(context)


class DeleteCrudMetaDescription(View):
    def get(self, request):
        # รับค่าจาก AJAX ที่ส่งมาใน key data
        mdId = request.GET.get('md_id', None)
        pageId = request.GET.get('page_id', None)
        metaDesObject = PageListMetaDescriptionModel.objects.get(id=mdId)
        # adjust count keyword before delete
        fullKeyword = metaDesObject.full_keyword
        shortKeyword = metaDesObject.shorten_keyword
    # reduce amount of the old one
        AdjustCountKeyToDb(fullKeyword, 'minus', 1, pageId)
    # reduce amount of the old one
        AdjustCountKeyToDb(shortKeyword, 'minus', 1, pageId)

        metaDesObject.delete()
        context = {
            'deleted': True
        }
        return JsonResponse(context)


class ShortenKwCrudMetaDescription(View):
    def get(self, request):
        # รับค่าจาก AJAX ที่ส่งมาใน key data
        addMode = request.GET.get('add_mode', None)
        comeFrom = request.GET.get('come_from', None)
        pageId = request.GET.get('page_id', None)
        keywordId = ""
        ApplyShortUniqueToShortKeywordForCrud(
            pageId, keywordId, addMode, comeFrom)

        # ================ START : META DES COUNT CHARACTER ================ #

        pagelistMetaObject = PageListMetaDescriptionModel.objects.filter(
            page_list_id=pageId)
        shortenKeywordList = []
        for x in pagelistMetaObject:
            shortenKeywordList.append(x.shorten_keyword)
        joinShortenKeyword = " ".join(shortenKeywordList)

        attribute = "shorten_keyword"
        lengthShortKeyword = CountCharacterLength(
            pagelistMetaObject, attribute)
        # ================ END : META DES COUNT CHARACTER ================ #
        context = {
            'lengthShortKeyword': lengthShortKeyword,
            'joinShortenKeyword': joinShortenKeyword
        }
        return JsonResponse(context)

    # ================ END : CRUD META DESCRIPTION ================ #
    # ================ END : CRUD META DESCRIPTION ================ #
    # ================ END : CRUD META DESCRIPTION ================ #

    # ================ START : CRUD EXAMPLE ================ #
    # ================ START : CRUD EXAMPLE ================ #
    # ================ START : CRUD EXAMPLE ================ #


class CreateCrudUser(View):
    def get(self, request):
        # รับค่าจาก AJAX ที่ส่งมาใน key data
        name1 = request.GET.get('full_keyword_for_view_py', None)

        obj = CrudUser.objects.create(
            name=name1,
        )

        user = {
            'id': obj.id,
            'full_keyword': obj.name,
        }

        data = {
            'user': user
        }
        # ส่ง data ที่มี key user กลับไปที่หน้า html
        return JsonResponse(data)


class UpdateCrudUser(View):
    def get(self, request):
        # รับค่าจาก AJAX ที่ส่งมาใน key data
        id1 = request.GET.get('id', None)
        name1 = request.GET.get('name', None)

        obj = CrudUser.objects.get(id=id1)
        obj.name = name1
        obj.save()

        user = {'id': obj.id, 'name': obj.name}

        data = {
            'user': user
        }
        return JsonResponse(data)


class DeleteCrudUser(View):
    def get(self, request):
        # รับค่าจาก AJAX ที่ส่งมาใน key data
        id1 = request.GET.get('id', None)
        CrudUser.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)
