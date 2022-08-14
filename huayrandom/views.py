from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from huayrandom.models import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os


def Index(request):
    context = {}
    if request.method == 'POST':
        data = request.POST.copy()
        getUsername = data.get('username')
        try:
            userObject = User.objects.get(username=getUsername)
            return redirect('home', userObject.username)
        except:
            request.session['error'] = 'ไม่มีบ้านดังกล่าว'
            return redirect('index')

    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''  # clear stuck error in session
    if 'expire' in request.session:
        context['expire'] = request.session['expire']
        request.session['expire'] = ''

    return render(request, 'find_house.html', context)


def Login(request):
    context = {}
    if request.method == 'POST':
        data = request.POST.copy()
        getUsername = data.get('username')
        getPassword = data.get('password')
        user = authenticate(username=getUsername, password=getPassword)
        if user is not None:
            login(request, user)
            return redirect('backend')
        else:
            request.session['error'] = "error"
    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''  # clear stuck error in session
    return render(request, 'login.html', context)


@login_required
def Backend(request):
    context = {}

    houseName = ""
    if request.method == 'POST':
        data = request.POST.copy()
        houseName = data.get('house_name')
        nextPage = data.get('next_page')
        if (houseName != ""):
            if (houseName == "none"):
                if (nextPage == "huay"):
                    request.session['error'] = "error"
                    return redirect('backend')
                else:
                    return redirect('list_user')
            elif (nextPage == "huay"):
                return redirect('list_huay', houseName)
            else:
                return redirect('list_user')

        else:
            return redirect('backend')
    profileObject = ProfileModel.objects.all()
    context['profileObject'] = profileObject

    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''  # clear stuck error in session

    return render(request, 'list_house.html', context)


@login_required
def ListUser(request):
    context = {}

    userObject = User.objects.all()
    context['userObject'] = userObject

    return render(request, 'user/user.html', context)


@login_required
def AddUser(request):
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        username = data.get('username')
        creditShop = data.get('credit_shop')
        expireDate = data.get('expire_date')
        expireTime = data.get('expire_time')
        randomMode = data.get('random_mode')

        try:
            checkDuplicated = User.objects.get(username=username)
            request.session['error'] = 'error'
            return redirect('list_user')
        except:

            addData = User()
            addData.username = username
            addData.password = "!Test1234"
            addData.save()

            addProfileData = ProfileModel()
            addProfileData.user = User.objects.get(username=username)
            addProfileData.house_name = username
            addProfileData.credit_shop = creditShop
            addProfileData.random_mode = randomMode
            addProfileData.expire_date = "{} {}:00".format(
                expireDate, expireTime)
            addProfileData.save()

            huayListObject = HuayListModel.objects.all()
            for item in huayListObject:
                addHuayData = HuayTypeModel()
                addHuayData.user = User.objects.get(username=username)
                addHuayData.huay_list = HuayListModel.objects.get(id=item.id)
                addHuayData.save()

            request.session['status'] = 'Done'

            return redirect('list_user')

    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''  # clear stuck error in session
    if 'status' in request.session:
        context['status'] = request.session['status']
        request.session['status'] = ''  # clear stuck error in session

    return render(request, 'user/add_user.html', context)


@login_required
def EditUser(request, username):
    context = {}
    userObject = User.objects.get(username=username)

    if request.method == 'POST':
        data = request.POST.copy()
        creditShop = data.get('credit_shop')
        expireDate = data.get('expire_date')
        expireTime = data.get('expire_time')
        randomMode = data.get('random_mode')

        editData = ProfileModel.objects.get(user=userObject)
        editData.user = userObject
        editData.credit_shop = creditShop
        editData.random_mode = randomMode
        editData.expire_date = "{} {}:00".format(expireDate, expireTime)
        editData.save()

        request.session['statusedit'] = 'Done'

        return redirect('list_user')

    profileObject = ProfileModel.objects.get(user=userObject)

    context['data'] = profileObject
    context['expireDate'] = profileObject.expire_date.strftime("%Y-%m-%d")
    context['expireTime'] = profileObject.expire_date.strftime("%H:%M")
    return render(request, 'user/edit_user.html', context)


@login_required
def ListHuay(request, username):
    context = {}
    userObject = User.objects.get(username=username)
    huayTypeObject = HuayTypeModel.objects.filter(user=userObject)
    huayIdMorningList = []
    huayFullNameMorningList = []
    huayIdAfternoonList = []
    huayFullNameAfternoonList = []
    huayIdEveningList = []
    huayFullNameEveningList = []
    huayIdOtherList = []
    huayFullNameOtherList = []

    for item in huayTypeObject:
        time = str(item.huay_list.time)
        if time == "07:00:00":
            huayIdMorningList.append(item.id)
            huayFullNameMorningList.append(item.huay_list.full_name)
        elif time == "13:00:00":
            huayIdAfternoonList.append(item.id)
            huayFullNameAfternoonList.append(item.huay_list.full_name)
        elif time == "19:00:00":
            huayIdEveningList.append(item.id)
            huayFullNameEveningList.append(item.huay_list.full_name)
        elif time == "20:00:00":
            huayIdOtherList.append(item.id)
            huayFullNameOtherList.append(item.huay_list.full_name)
    print("huayIdMorningList : ", huayIdMorningList)
    print("huayFullNameMorningList : ", huayFullNameMorningList)
    zipDataForLoopMorning = zip(huayIdMorningList,
                                huayFullNameMorningList)
    zipDataForLoopAfternoon = zip(huayIdAfternoonList,
                                  huayFullNameAfternoonList)
    zipDataForLoopEvening = zip(huayIdEveningList,
                                huayFullNameEveningList)
    zipDataForLoopOther = zip(huayIdOtherList,
                              huayFullNameOtherList)

    profileObject = ProfileModel.objects.get(user=userObject)

    context['username'] = username
    context['houseName'] = profileObject.house_name
    context['zipDataForLoopMorning'] = zipDataForLoopMorning
    context['zipDataForLoopAfternoon'] = zipDataForLoopAfternoon
    context['zipDataForLoopEvening'] = zipDataForLoopEvening
    context['zipDataForLoopOther'] = zipDataForLoopOther

    return render(request, 'huay/list_huay.html', context)


@login_required
def AddHuay(request, username):
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        huayListId = data.get('huay_list_id')
        fontTextId = data.get('font_text_id')
        textColor = data.get('text_color')
        textPosX = data.get('text_pos_x')
        textPosY = data.get('text_pos_y')
        textSize = data.get('text_size')
        borderWidth = data.get('border_width')
        borderColor = data.get('text_border_color')
        fontNumberId = data.get('number_font_id')
        mainNumberPosX = data.get('main_number_pos_x')
        mainNumberPosY = data.get('main_number_pos_y')
        mainNumberSize = data.get('main_number_size')
        dataPosX = data.get('date_pos_x')
        dataPosY = data.get('date_pos_y')
        dataFontsize = data.get('date_fontsize')
        focusPosX = data.get('focus_pos_x')
        focusPosY = data.get('focus_pos_y')
        focusFontsize = data.get('focus_fontsize')
        numberRow1PosX = data.get('number_row1_pos_x')
        numberRow1PosY = data.get('number_row1_pos_y')
        numberRow2PosX = data.get('number_row2_pos_x')
        numberRow2PosY = data.get('number_row2_pos_y')
        numberRowFontsize = data.get('number_row_fontsize')
        try:
            checkDuplicated = HuayTypeModel.objects.get(
                id=huayListId, user=userObject)
            request.session['error'] = 'error'
            return redirect('add_huay', username)
        except:
            getFontName = FontListModel.objects.get(id=fontTextId)
            getFontName2 = FontListModel.objects.get(id=fontNumberId)
            addData = HuayTypeModel()
            addData.user = User.objects.get(username=username)
            addData.huay_list = HuayListModel.objects.get(id=huayListId)
            addData.text_font = getFontName.font_name
            addData.text_color = textColor
            addData.text_border_size = borderWidth
            addData.text_border_color = borderColor
            addData.text_pos_x = textPosX
            addData.text_pos_y = textPosY
            addData.text_font_size = textSize
            addData.date_pos_x = dataPosX
            addData.date_pos_y = dataPosY
            addData.date_font_size = dataFontsize
            addData.main_num_pos_x = mainNumberPosX
            addData.main_num_pos_y = mainNumberPosY
            addData.main_num_font = getFontName2.font_name
            addData.main_num_font_size = mainNumberSize
            addData.focus_num_pos_x = focusPosX
            addData.focus_num_pos_y = focusPosY
            addData.focus_num_font_size = focusFontsize
            addData.row1_x = numberRow1PosX
            addData.row1_y = numberRow1PosY
            addData.row2_x = numberRow2PosX
            addData.row2_y = numberRow2PosY
            addData.row_font_size = numberRowFontsize
            addData.save()

            request.session['status'] = 'Done'

            return redirect('add_huay', username)

    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''  # clear stuck error in session
    if 'status' in request.session:
        context['status'] = request.session['status']
        request.session['status'] = ''  # clear stuck error in session

    userObject = User.objects.get(username=username)
    profileObject = ProfileModel.objects.get(user=userObject)

    huayFilter = HuayTypeModel.objects.filter(user=userObject)
    huayFilterList = []
    for item in huayFilter:
        huayFilterList.append(item.huay_list.short_name)

    huayAll = HuayListModel.objects.all()
    huayAllIdList = []
    huayAllNameList = []
    for itemAll in huayAll:
        if str(itemAll) not in huayFilterList:
            huayAllNameList.append(str(itemAll))
            huayAllIdList.append(str(itemAll.id))
    huayAllList = zip(huayAllNameList, huayAllIdList)

    fontListObject = FontListModel.objects.all()
    colorListObject = ColorListModel.objects.all()

    context['huayList'] = huayAllList
    context['data'] = profileObject
    context['fontList'] = fontListObject
    context['colorList'] = colorListObject
    context['username'] = username

    return render(request, 'huay/add_huay.html', context)


@login_required
def EditHuay(request, username, huay_id):
    context = {}
    userObject = User.objects.get(username=username)

    if request.method == 'POST':
        data = request.POST.copy()
        huayListId = data.get('huay_list_id')
        fontTextId = data.get('font_text_id')
        # ชื่อหวย
        textColor = data.get('text_color')
        textPosX = data.get('text_pos_x')
        textPosY = data.get('text_pos_y')
        textSize = data.get('text_size')
        textBorderStatus = data.get('text_border_status')
        borderWidth = data.get('border_width')
        borderColor = data.get('text_border_color')
        # ตัวเลขหลัก 2 ตัว
        mainNumberFontColor = data.get('main_number_font_color')
        mainNumberFontSize = data.get('main_num_font_size')
        mainNumberPosX = data.get('main_number_pos_x')
        mainNumberPosY = data.get('main_number_pos_y')
        mainNumberSize = data.get('main_number_size')
        mainNumberBorderStatus = data.get('main_num_border_status')
        mainNumberBorderSize = data.get('main_num_border_size')
        mainNumberBorderColor = data.get('main_num_border_color')
        mainNumberSeparator = data.get('main_num_separator')
        # ตัวเลขย่อยแถว 1 และ 2
        numberRowFont = data.get('row_font')
        numberRowFontsize = data.get('number_row_fontsize')
        # ตัวเลขย่อยแถว 1
        row1Color = data.get('row1_color')
        row1BorderStatus = data.get('row1_border_status')
        row1BorderColor = data.get('row1_border_color')
        row1BorderSize = data.get('row1_border_size')
        numberRow1PosX = data.get('number_row1_pos_x')
        numberRow1PosY = data.get('number_row1_pos_y')
        row1Separator = data.get('row1_separator')
        # ตัวเลขย่อยแถว 2
        row2Color = data.get('row2_color')
        row2BorderStatus = data.get('row2_border_status')
        row2BorderColor = data.get('row2_border_color')
        row2BorderSize = data.get('row2_border_size')
        numberRow2PosX = data.get('number_row2_pos_x')
        numberRow2PosY = data.get('number_row2_pos_y')
        row2Separator = data.get('row2_separator')
        # วันที่
        dataPosX = data.get('date_pos_x')
        dataPosY = data.get('date_pos_y')
        dataFontsize = data.get('date_fontsize')
        # ตัวเน้น
        focusPosX = data.get('focus_pos_x')
        focusPosY = data.get('focus_pos_y')
        focusFontsize = data.get('focus_fontsize')
        # เลข 3 หลัก ตัวหลัก
        threeMainStatus = data.get('three_main_status')
        threeMainPosX = data.get('three_main_pos_x')
        threeMainPosY = data.get('three_main_pos_y')
        threeMainFontSize = data.get('three_main_font_size')
        threeMainSeparator = data.get('three_main_separator')
        threeMainFontColor = data.get('three_main_font_color')
        # เลข 3 หลัก ตัวย่อย
        threeSubStatus = data.get('three_sub_status')
        threeSubPosX = data.get('three_sub_pos_x')
        threeSubPosY = data.get('three_sub_pos_y')
        threeSubFont = data.get('three_sub_font')
        threeSubFontSize = data.get('three_sub_font_size')
        threeSubSeparator = data.get('three_sub_separator')
        threeSubFontColor = data.get('three_sub_font_color')
        threeSubBorderStatus = data.get('three_sub_border_status')
        threeSubBorderColor = data.get('three_sub_border_color')
        threeSubBorderSize = data.get('three_sub_border_size')
        # หมายเหตุ
        remarkStatus = data.get('remark_status')
        remarkText = data.get('remark_text')
        remarkFont = data.get('remark_font')
        remarkFontSize = data.get('remark_font_size')
        remarkFontColor = data.get('remark_font_color')
        remarkBorderStatus = data.get('remark_border_status')
        remarkBorderSize = data.get('remark_border_size')
        remarkBorderColor = data.get('remark_border_color')
        remarkPosX = data.get('remark_pos_x')
        remarkPosY = data.get('remark_pos_y')

        getFontNameOfText = FontListModel.objects.get(id=fontTextId)
        getFontNameOfMainNumber = FontListModel.objects.get(id=mainNumberFontSize)
        getFontRow = FontListModel.objects.get(id=numberRowFont)
        getRemarkFont = FontListModel.objects.get(id=remarkFont)
        getThreeSubFont = FontListModel.objects.get(id=threeSubFont)

        editData = HuayTypeModel.objects.get(id=huayListId, user=userObject)

        editData.user = User.objects.get(username=username)
        editData.text_font = getFontNameOfText.font_name
        editData.text_color = textColor
        editData.text_border_status = textBorderStatus
        editData.text_border_size = borderWidth
        editData.text_border_color = borderColor
        editData.text_pos_x = textPosX
        editData.text_pos_y = textPosY
        editData.text_font_size = textSize
        editData.date_pos_x = dataPosX
        editData.date_pos_y = dataPosY
        editData.date_font_size = dataFontsize
        editData.main_num_font = getFontNameOfMainNumber.font_name
        editData.main_num_pos_x = mainNumberPosX
        editData.main_num_pos_y = mainNumberPosY
        editData.main_num_font_size = mainNumberSize
        editData.main_num_font_color = mainNumberFontColor
        editData.main_num_border_status = mainNumberBorderStatus
        editData.main_num_border_size = mainNumberBorderSize
        editData.main_num_border_color = mainNumberBorderColor
        editData.main_num_separator = mainNumberSeparator
        editData.focus_num_pos_x = focusPosX
        editData.focus_num_pos_y = focusPosY
        editData.focus_num_font_size = focusFontsize
        editData.row1_x = numberRow1PosX
        editData.row1_y = numberRow1PosY
        editData.row1_separator = row1Separator
        editData.row1_color = row1Color
        editData.row1_border_status = row1BorderStatus
        editData.row1_border_color = row1BorderColor
        editData.row1_border_size = row1BorderSize
        editData.row2_x = numberRow2PosX
        editData.row2_y = numberRow2PosY
        editData.row2_separator = row2Separator
        editData.row2_color = row2Color
        editData.row2_border_status = row2BorderStatus
        editData.row2_border_color = row2BorderColor
        editData.row2_border_size = row2BorderSize
        editData.row_font = getFontRow.font_name
        editData.row_font_size = numberRowFontsize
        editData.three_main_status = threeMainStatus
        editData.three_main_pos_x = threeMainPosX
        editData.three_main_pos_y = threeMainPosY
        editData.three_main_font_size = threeMainFontSize
        editData.three_main_separator = threeMainSeparator
        editData.three_main_font_color = threeMainFontColor
        editData.three_sub_status = threeSubStatus
        editData.three_sub_pos_x = threeSubPosX
        editData.three_sub_pos_y = threeSubPosY
        editData.three_sub_font = getThreeSubFont.font_name
        editData.three_sub_font_size = threeSubFontSize
        editData.three_sub_separator = threeSubSeparator
        editData.three_sub_font_color = threeSubFontColor
        editData.three_sub_border_status = threeSubBorderStatus
        editData.three_sub_border_color = threeSubBorderColor
        editData.three_sub_border_size = threeSubBorderSize
        editData.remark_status = remarkStatus
        editData.remark_text = remarkText
        editData.remark_font = getRemarkFont.font_name
        editData.remark_font_size = remarkFontSize
        editData.remark_font_color = remarkFontColor
        editData.remark_border_status = remarkBorderStatus
        editData.remark_border_size = remarkBorderSize
        editData.remark_border_color = remarkBorderColor
        editData.remark_pos_x = remarkPosX
        editData.remark_pos_y = remarkPosY
        editData.save()

        request.session['statusedit'] = 'Done'

        return redirect('edit_huay', username, huay_id)

    userObject = User.objects.get(username=username)
    profileObject = ProfileModel.objects.get(user=userObject)
    huayTypeObject = HuayTypeModel.objects.get(id=huay_id, user=userObject)
    fontListObject = FontListModel.objects.all()
    colorListObject = ColorListModel.objects.all()

    imgLocation = GenerateImageWIthText(username, huayTypeObject.huay_list.full_name, huayTypeObject.text_font, huayTypeObject.main_num_font, huayTypeObject.text_color, huayTypeObject.text_border_status, huayTypeObject.text_border_size, huayTypeObject.text_border_color, huayTypeObject.text_pos_x, huayTypeObject.text_pos_y, huayTypeObject.text_font_size,
                                        huayTypeObject.date_pos_x, huayTypeObject.date_pos_y, huayTypeObject.date_font_size, huayTypeObject.main_num_pos_x, huayTypeObject.main_num_pos_y, huayTypeObject.main_num_font_size, huayTypeObject.main_num_border_status, huayTypeObject.main_num_border_color, huayTypeObject.main_num_border_size, huayTypeObject.focus_num_pos_x,
                                        huayTypeObject.focus_num_pos_y, huayTypeObject.focus_num_font_size, huayTypeObject.focus_num_border_status, huayTypeObject.focus_num_border_color, huayTypeObject.focus_num_border_size, huayTypeObject.row1_x, huayTypeObject.row1_y, huayTypeObject.row1_border_status, huayTypeObject.row1_border_color, huayTypeObject.row1_border_size,
                                        huayTypeObject.row2_x, huayTypeObject.row2_y,  huayTypeObject.row2_border_status, huayTypeObject.row2_border_color, huayTypeObject.row2_border_size, huayTypeObject.row_font_size, huayTypeObject.main_num_separator, huayTypeObject.row1_separator, huayTypeObject.row2_separator, huayTypeObject.date_color, huayTypeObject.main_num_font_color, huayTypeObject.focus_num_color,
                                        huayTypeObject.row1_color, huayTypeObject.row2_color, huayTypeObject.credit_shop_pos_x, huayTypeObject.credit_shop_pos_y, huayTypeObject.credit_shop_border_status, huayTypeObject.credit_shop_border_color, huayTypeObject.credit_shop_border_size,huayTypeObject.three_main_status,huayTypeObject.three_main_font,huayTypeObject.three_main_font_size,
                                        huayTypeObject.three_main_font_color,huayTypeObject.three_main_border_status,huayTypeObject.three_main_border_size,huayTypeObject.three_main_border_color,huayTypeObject.three_main_pos_x,huayTypeObject.three_main_pos_y,huayTypeObject.three_main_separator,huayTypeObject.three_sub_status,huayTypeObject.three_sub_font,
                                        huayTypeObject.three_sub_font_size,huayTypeObject.three_sub_font_color,huayTypeObject.three_sub_border_status,huayTypeObject.three_sub_border_size,huayTypeObject.three_sub_border_color,huayTypeObject.three_sub_pos_x,huayTypeObject.three_sub_pos_y,huayTypeObject.three_sub_separator,huayTypeObject.remark_status,huayTypeObject.remark_text,
                                        huayTypeObject.remark_font,huayTypeObject.remark_font_size,huayTypeObject.remark_font_color,huayTypeObject.remark_border_status,huayTypeObject.remark_border_size,huayTypeObject.remark_border_color,huayTypeObject.remark_pos_x,huayTypeObject.remark_pos_y)

    context['imgLocation'] = imgLocation

    context['huayTypeObject'] = huayTypeObject
    context['data'] = profileObject
    context['huayId'] = huay_id
    context['fontList'] = fontListObject
    context['colorList'] = colorListObject
    context['username'] = username

    return render(request, 'huay/edit_huay.html', context)


def Home(request, username):
    context = {}
    context['username'] = username
    resultCheckExpire = CheckExpireDate(username)
    if resultCheckExpire == "ตัดสิทธิ์แล้ว":
        request.session['expire'] = 'ตัดสิทธิ์แล้ว'
    else:
        resultCheckExpire = ""
    try:
        userObject = User.objects.get(username=username)
        profileObject = ProfileModel.objects.get(user=userObject)

        day = profileObject.expire_date.strftime("%d")
        month = profileObject.expire_date.strftime("%m")
        year = profileObject.expire_date.strftime("%Y")
        thaiMonth = ConvertToThaiMonth(month)
        expireDateThai = "{} {} {}".format(day, thaiMonth, year)
        for x in range(0, 4):
            if x == 0:
                huayObject = HuayListModel.objects.filter(time="07:00:00")
            elif x == 1:
                huayObject = HuayListModel.objects.filter(time="13:00:00")
            elif x == 2:
                huayObject = HuayListModel.objects.filter(time="19:00:00")
            elif x == 3:
                huayObject = HuayListModel.objects.filter(time="20:00:00")

            huayShortNameList = []
            huayLinkList = []
            btnColorList = []

            i = 1
            listPurple = [1, 5, 9, 13, 17, 21, 25, 29]
            listOrange = [2, 6, 10, 14, 18, 22, 26, 30]
            listPink = [3, 7, 11, 15, 19, 23, 27, 31]
            listGreen = [4, 8, 12, 16, 20, 24, 28, 32]

            for item in huayObject:
                huayShortNameList.append(item.short_name)
                huayLinkList.append(item.link)
                if i in listPurple:
                    btnColorList.append('purple')
                elif i in listOrange:
                    btnColorList.append('orange')
                elif i in listPink:
                    btnColorList.append('pink')
                elif i in listGreen:
                    btnColorList.append('green')
                i += 1
            if x == 0:
                zipDataForLoopMorning = zip(
                    huayShortNameList, huayLinkList, btnColorList)
            elif x == 1:
                zipDataForLoopAfternoon = zip(
                    huayShortNameList, huayLinkList, btnColorList)
            elif x == 2:
                zipDataForLoopEvening = zip(
                    huayShortNameList, huayLinkList, btnColorList)
            elif x == 3:
                zipDataForLoopOther = zip(
                    huayShortNameList, huayLinkList, btnColorList)

        context['houseNameThai'] = profileObject.house_name
        context['expireDateThai'] = expireDateThai
        context['zipDataForLoopMorning'] = zipDataForLoopMorning
        context['zipDataForLoopAfternoon'] = zipDataForLoopAfternoon
        context['zipDataForLoopEvening'] = zipDataForLoopEvening
        context['zipDataForLoopOther'] = zipDataForLoopOther

        if 'expire' in request.session:
            context['expire'] = request.session['expire']
            context['username'] = username
            request.session['expire'] = ''  # clear stuck error in session

        return render(request, 'index.html', context)
    except:
        request.session['error'] = 'ไม่มีบ้านดังกล่าว'
        return redirect('index')


def Result(request, username, link):
    context = {}
    resultCheckExpire = CheckExpireDate(username)
    if resultCheckExpire == "ตัดสิทธิ์แล้ว":
        request.session['expire'] = 'ตัดสิทธิ์แล้ว'
        if 'expire' in request.session:
            context['expire'] = request.session['expire']
            request.session['expire'] = ''  # clear stuck error in session
        return render(request, 'result/index.html', context)
    else:
        resultCheckExpire = ""

    userObject = User.objects.get(username=username)
    profileObject = ProfileModel.objects.get(user_id=userObject)
    day = profileObject.expire_date.strftime("%d")
    month = profileObject.expire_date.strftime("%m")
    year = profileObject.expire_date.strftime("%Y")
    thaiMonth = ConvertToThaiMonth(month)
    expireDateThai = "{} {} {}".format(day, thaiMonth, year)

    context['username'] = username
    context['link'] = link
    context['expireDateThai'] = expireDateThai

    # try:

    huayListObject = HuayListModel.objects.get(link=link)
    data = HuayTypeModel.objects.get(
        huay_list=huayListObject, user=userObject)
    profileObject = ProfileModel.objects.get(user=userObject)

    imgLocation = GenerateImageWIthText(username, data.huay_list.full_name, data.text_font, data.main_num_font, data.text_color, data.text_border_status, data.text_border_size, data.text_border_color, data.text_pos_x, data.text_pos_y, data.text_font_size,
                                        data.date_pos_x, data.date_pos_y, data.date_font_size, data.main_num_pos_x, data.main_num_pos_y, data.main_num_font_size, data.main_num_border_status, data.main_num_border_color, data.main_num_border_size, data.focus_num_pos_x,
                                        data.focus_num_pos_y, data.focus_num_font_size, data.focus_num_border_status, data.focus_num_border_color, data.focus_num_border_size, data.row1_x, data.row1_y, data.row1_border_status, data.row1_border_color, data.row1_border_size,
                                        data.row2_x, data.row2_y,  data.row2_border_status, data.row2_border_color, data.row2_border_size, data.row_font_size, data.main_num_separator, data.row1_separator, data.row2_separator, data.date_color, data.main_num_font_color, data.focus_num_color,
                                        data.row1_color, data.row2_color, data.credit_shop_pos_x, data.credit_shop_pos_y, data.credit_shop_border_status, data.credit_shop_border_color, data.credit_shop_border_size,data.three_main_status,data.three_main_font,data.three_main_font_size,
                                        data.three_main_font_color,data.three_main_border_status,data.three_main_border_size,data.three_main_border_color,data.three_main_pos_x,data.three_main_pos_y,data.three_main_separator,data.three_sub_status,data.three_sub_font,
                                        data.three_sub_font_size,data.three_sub_font_color,data.three_sub_border_status,data.three_sub_border_size,data.three_sub_border_color,data.three_sub_pos_x,data.three_sub_pos_y,data.three_sub_separator,data.remark_status,data.remark_text,
                                        data.remark_font,data.remark_font_size,data.remark_font_color,data.remark_border_status,data.remark_border_size,data.remark_border_color,data.remark_pos_x,data.remark_pos_y)

    context['imgLocation'] = imgLocation
    # except:
    #     request.session['error'] = 'error'
    #     if 'error' in request.session:
    #         context['error'] = request.session['error']
    #         request.session['error'] = ''  # clear stuck error in session
    #     return render(request, 'result/index.html', context)
    return render(request, 'result/index.html', context)


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


def CheckExpireDate(username):
    try:
        userObject = User.objects.get(username=username)
        profileObject = ProfileModel.objects.get(user=userObject)
        expireDate = profileObject.expire_date
        expireDateNewFormat = expireDate.strftime("%Y%m%d%H%M")
        timeNow = datetime.now() + relativedelta(hours=7)
        currentTime = timeNow.strftime("%Y%m%d%H%M")

        if currentTime >= expireDateNewFormat:
            return "ตัดสิทธิ์แล้ว"
    except:
        pass
# ฟังก์ชั่นสร้างรูปของบ้านเพิ่มทรัพย์


def GenerateImageWIthText(username, type, fontText, fontNumber, textColor, textBorderStatus, textBorderSize, 
textBorderColor, txtPosX, txtPosY, txtFontSize, datePosX, datePosY, dateFontSize, mainNumberPosX, 
mainNumberPosY, mainNumberFontSize, mainNumberBorderStatus, mainNumberBorderColor, 
mainNumberBorderSize, focusNumberX, focusNumberY, focusNumberFontSize, forcusNumberBorderStatus, 
forcusNumberBorderColor, forcusNumberBorderSize, row1X, row1Y, row1BorderStatus, row1BorderColor, 
row1BorderSize, row2X, row2Y, row2BorderStatus, row2BorderColor, row2BorderSize, rowFontSize, 
mainNumSeparator, row1Separator, row2Separator, dateColor, mainNumFontColor, focusNumColor, row1Color, 
row2Color, creditShopPosX, creditShopPosY, creditShopBorderStatus, creditShopBorderColor, creditShopBorderSize,
threeMainStatus,threeMainFont,threeMainFontSize,threeMainFontColor,threeMainBorderStatus, threeMainBorderSize,
threeMainBorderColor,threeMainPosX,threeMainPosY,threeMainSeparator,threeSubStatus,threeSubFont,threeSubFontSize,threeSubFontColor,
threeSubBorderStatus, threeSubBorderSize,threeSubBorderColor,threeSubPosX,threeSubPosY,threeSubSeparator,
remarkStatus,remarkText,remarkFont,remarkFontSize,remarkFontColor,remarkBorderStatus,remarkBorderSize,remarkBorderColor,remarkPosX,remarkPosY):
    userObject = User.objects.get(username=username)
    profileObject = ProfileModel.objects.get(user=userObject)
    randomResult = random2NumberResult(profileObject)
    mainFirstNumber = randomResult[0]
    mainSecondNumber = randomResult[1]
    focusNumber = randomResult[2]
    row1Set1 = randomResult[3]
    row1Set2 = randomResult[4]
    row1Set3 = randomResult[5]
    row1Set4 = randomResult[6]
    row2Set1 = randomResult[7]
    row2Set2 = randomResult[8]
    row2Set3 = randomResult[9]
    row2Set4 = randomResult[10]
    mainThreeNumbers1 = randomResult[11]
    mainThreeNumbers2 = randomResult[12]
    mainThreeNumbers3 = randomResult[13]
    threeNumberSet1 = randomResult[14]
    threeNumberSet2 = randomResult[15]
    threeNumberSet3 = randomResult[16]
    path = os.getcwd()
    # * ================= START :  SET FONT =================

    # ? SERVER
    font0 = ImageFont.truetype(
        '/home/cheetah/random.huay-vip-net/static/assets/fonts/{}'.format(fontText), txtFontSize)
    font1 = ImageFont.truetype(
        '/home/cheetah/random.huay-vip-net/static/assets/fonts/{}'.format(fontNumber), dateFontSize)
    font2 = ImageFont.truetype(
        '/home/cheetah/random.huay-vip-net/static/assets/fonts/{}'.format(fontNumber), mainNumberFontSize)
    font3 = ImageFont.truetype(
        '/home/cheetah/random.huay-vip-net/static/assets/fonts/{}'.format(fontNumber), rowFontSize)
    font4 = ImageFont.truetype(
        '/home/cheetah/random.huay-vip-net/static/assets/fonts/{}'.format(fontNumber), focusNumberFontSize)
    location = '/home/cheetah/random.huay-vip-net/static/images/result-hua/{}-result.jpg'.format(
        username)
    locationTemplate = '/home/cheetah/random.huay-vip-net/static/images/template-hua/{}-template.jpg'.format(
        username)

    # ? LOCAL
    # font0 = ImageFont.truetype(
    #     path+'/static/assets/fonts/{}'.format(fontText), txtFontSize)
    # font1 = ImageFont.truetype(
    #     path+'/static/assets/fonts/{}'.format(fontNumber), dateFontSize)
    # font2 = ImageFont.truetype(
    #     path+'/static/assets/fonts/{}'.format(fontNumber), mainNumberFontSize)
    # font3 = ImageFont.truetype(
    #     path+'/static/assets/fonts/{}'.format(fontNumber), rowFontSize)
    # font4 = ImageFont.truetype(
    #     path+'/static/assets/fonts/{}'.format(fontNumber), focusNumberFontSize)
    # threeMainFont = ImageFont.truetype(
    #     path+'/static/assets/fonts/{}'.format(threeMainFont), threeMainFontSize)
    # threeSubFont = ImageFont.truetype(
    #     path+'/static/assets/fonts/{}'.format(threeSubFont), threeSubFontSize)
    # remarkFont = ImageFont.truetype(
    #     path+'/static/assets/fonts/{}'.format(remarkFont), remarkFontSize)

    # * ================= END :  SET FONT =================

    location = path+'/static/images/result-hua/{}-result.jpg'.format(username)
    locationTemplate = path + \
        '/static/images/template-hua/{}-template.jpg'.format(username)

    img = Image.open(locationTemplate)
    imgObj = ImageDraw.Draw(img)

    # Set Date
    cueDateTime = datetime.now() + relativedelta(hours=7, years=543)
    curDate = cueDateTime.strftime(r'%d/%m/%y')

    # * ================= START :  GET FONT COLOR =================
    
    #? date text
    dateColorObject = ColorListModel.objects.get(id=dateColor)
    dateColorSeparate = dateColorObject.color_code.split(",")
    dateColorConverted0 = int(dateColorSeparate[0])
    dateColorConverted1 = int(dateColorSeparate[1])
    dateColorConverted2 = int(dateColorSeparate[2])
    dateColorConverted = dateColorConverted0, dateColorConverted1, dateColorConverted2
    
    #? name text
    textColorObject = ColorListModel.objects.get(id=textColor)
    textColorSeparate = textColorObject.color_code.split(",")
    textColorConverted0 = int(textColorSeparate[0])
    textColorConverted1 = int(textColorSeparate[1])
    textColorConverted2 = int(textColorSeparate[2])
    textColorConverted = textColorConverted0, textColorConverted1, textColorConverted2
    
    #? main number text
    mainNumFontColorObject = ColorListModel.objects.get(id=mainNumFontColor)
    mainNumFontColorSeparate = mainNumFontColorObject.color_code.split(",")
    mainNumFontColorConverted0 = int(mainNumFontColorSeparate[0])
    mainNumFontColorConverted1 = int(mainNumFontColorSeparate[1])
    mainNumFontColorConverted2 = int(mainNumFontColorSeparate[2])
    mainNumFontColorConverted = mainNumFontColorConverted0, mainNumFontColorConverted1, mainNumFontColorConverted2
    
    #? focus number text
    focusNumColorObject = ColorListModel.objects.get(id=focusNumColor)
    focusNumColorSeparate = focusNumColorObject.color_code.split(",")
    focusNumColorConverted0 = int(focusNumColorSeparate[0])
    focusNumColorConverted1 = int(focusNumColorSeparate[1])
    focusNumColorConverted2 = int(focusNumColorSeparate[2])
    focusNumColorConverted = focusNumColorConverted0, focusNumColorConverted1, focusNumColorConverted2
    
    #? row 1 text
    row1ColorObject = ColorListModel.objects.get(id=row1Color)
    row1ColorSeparate = row1ColorObject.color_code.split(",")
    row1ColorConverted0 = int(row1ColorSeparate[0])
    row1ColorConverted1 = int(row1ColorSeparate[1])
    row1ColorConverted2 = int(row1ColorSeparate[2])
    row1ColorConverted = row1ColorConverted0, row1ColorConverted1, row1ColorConverted2
    
    #? row 2 text
    row2ColorObject = ColorListModel.objects.get(id=row2Color)
    row2ColorSeparate = row2ColorObject.color_code.split(",")
    row2ColorConverted0 = int(row2ColorSeparate[0])
    row2ColorConverted1 = int(row2ColorSeparate[1])
    row2ColorConverted2 = int(row2ColorSeparate[2])
    row2ColorConverted = row2ColorConverted0, row2ColorConverted1, row2ColorConverted2
    
    #? three main text
    threeMainFontColorObject = ColorListModel.objects.get(id=threeMainFontColor)
    threeMainFontColorSeparate = threeMainFontColorObject.color_code.split(",")
    threeMainFontColorConverted0 = int(threeMainFontColorSeparate[0])
    threeMainFontColorConverted1 = int(threeMainFontColorSeparate[1])
    threeMainFontColorConverted2 = int(threeMainFontColorSeparate[2])
    threeMainFontColorConverted = threeMainFontColorConverted0, threeMainFontColorConverted1, threeMainFontColorConverted2
    
    #? three sub text
    threeSubFontColorObject = ColorListModel.objects.get(id=threeSubFontColor)
    threeSubFontColorSeparate = threeSubFontColorObject.color_code.split(",")
    threeSubFontColorConverted0 = int(threeSubFontColorSeparate[0])
    threeSubFontColorConverted1 = int(threeSubFontColorSeparate[1])
    threeSubFontColorConverted2 = int(threeSubFontColorSeparate[2])
    threeSubFontColorConverted = threeSubFontColorConverted0, threeSubFontColorConverted1, threeSubFontColorConverted2

    #? remark text
    remarkFontColorObject = ColorListModel.objects.get(id=remarkFontColor)
    remarkFontColorSeparate = remarkFontColorObject.color_code.split(",")
    remarkFontColorConverted0 = int(remarkFontColorSeparate[0])
    remarkFontColorConverted1 = int(remarkFontColorSeparate[1])
    remarkFontColorConverted2 = int(remarkFontColorSeparate[2])
    remarkFontColorConverted = remarkFontColorConverted0, remarkFontColorConverted1, remarkFontColorConverted2

    # * ================= END :  GET FONT COLOR =================
    # * ================= START : BORDER =================
    # ? text
    if textBorderStatus == "on":
        textBorderColorObject = ColorListModel.objects.get(id=textBorderColor)
        textBorderColorSeparate = textBorderColorObject.color_code.split(",")
        textBorderColorConverted0 = int(textBorderColorSeparate[0])
        textBorderColorConverted1 = int(textBorderColorSeparate[1])
        textBorderColorConverted2 = int(textBorderColorSeparate[2])
        textBorderColorConverted = textBorderColorConverted0, textBorderColorConverted1, textBorderColorConverted2

        imgObj.text((txtPosX-textBorderSize, txtPosY), type,
                    font=font0, fill=textBorderColorConverted)
        imgObj.text((txtPosX+textBorderSize, txtPosY), type,
                    font=font0, fill=textBorderColorConverted)
        imgObj.text((txtPosX, txtPosY-textBorderSize), type,
                    font=font0, fill=textBorderColorConverted)
        imgObj.text((txtPosX, txtPosY+textBorderSize), type,
                    font=font0, fill=textBorderColorConverted)

    # ? main number
    if mainNumberBorderStatus == "on":
        mainNumberBorderColorObject = ColorListModel.objects.get(
            id=mainNumberBorderColor)
        mainNumberBorderColorSeparate = mainNumberBorderColorObject.color_code.split(
            ",")
        mainNumberBorderColorConverted0 = int(mainNumberBorderColorSeparate[0])
        mainNumberBorderColorConverted1 = int(mainNumberBorderColorSeparate[1])
        mainNumberBorderColorConverted2 = int(mainNumberBorderColorSeparate[2])
        mainNumberBorderColorConverted = mainNumberBorderColorConverted0, mainNumberBorderColorConverted1, mainNumberBorderColorConverted2
        imgObj.text((mainNumberPosX-mainNumberBorderSize, mainNumberPosY),  "{}{}{}".format(mainFirstNumber, mainNumSeparator, mainSecondNumber),
                    font=font2, fill=mainNumberBorderColorConverted)
        imgObj.text((mainNumberPosX+mainNumberBorderSize, mainNumberPosY),  "{}{}{}".format(mainFirstNumber, mainNumSeparator, mainSecondNumber),
                    font=font2, fill=mainNumberBorderColorConverted)
        imgObj.text((mainNumberPosX, mainNumberPosY-mainNumberBorderSize),  "{}{}{}".format(mainFirstNumber, mainNumSeparator, mainSecondNumber),
                    font=font2, fill=mainNumberBorderColorConverted)
        imgObj.text((mainNumberPosX, mainNumberPosY+mainNumberBorderSize),  "{}{}{}".format(mainFirstNumber, mainNumSeparator, mainSecondNumber),
                    font=font2, fill=mainNumberBorderColorConverted)

    # ? focus number
    if forcusNumberBorderStatus == "on":
        forcusNumberBorderColorObject = ColorListModel.objects.get(
            id=forcusNumberBorderColor)
        forcusNumberBorderColorSeparate = forcusNumberBorderColorObject.color_code.split(
            ",")
        forcusNumberBorderColorConverted0 = int(
            forcusNumberBorderColorSeparate[0])
        forcusNumberBorderColorConverted1 = int(
            forcusNumberBorderColorSeparate[1])
        forcusNumberBorderColorConverted2 = int(
            forcusNumberBorderColorSeparate[2])
        forcusNumberBorderColorConverted = forcusNumberBorderColorConverted0, forcusNumberBorderColorConverted1, forcusNumberBorderColorConverted2

        imgObj.text((focusNumberX-forcusNumberBorderSize, focusNumberY), "{}".format(focusNumber),
                    font=font4, fill=forcusNumberBorderColorConverted)
        imgObj.text((focusNumberX+forcusNumberBorderSize, focusNumberY), "{}".format(focusNumber),
                    font=font4, fill=forcusNumberBorderColorConverted)
        imgObj.text((focusNumberX, focusNumberY-forcusNumberBorderSize), "{}".format(focusNumber),
                    font=font4, fill=forcusNumberBorderColorConverted)
        imgObj.text((focusNumberX, focusNumberY+forcusNumberBorderSize), "{}".format(focusNumber),
                    font=font4, fill=forcusNumberBorderColorConverted)
    # ? row 1
    if row1BorderStatus == "on":
        row1BorderColorObject = ColorListModel.objects.get(id=row1BorderColor)
        row1BorderColorSeparate = row1BorderColorObject.color_code.split(",")
        row1BorderColorConverted0 = int(row1BorderColorSeparate[0])
        row1BorderColorConverted1 = int(row1BorderColorSeparate[1])
        row1BorderColorConverted2 = int(row1BorderColorSeparate[2])
        row1BorderColorConverted = row1BorderColorConverted0, row1BorderColorConverted1, row1BorderColorConverted2

        imgObj.text((row1X-row1BorderSize, row1Y), "{}{}{}{}{}{}{}".format(row1Set1, row1Separator, row1Set2, row1Separator, row1Set3, row1Separator, row1Set4, row1Separator),
                    font=font3, fill=row1BorderColorConverted)
        imgObj.text((row1X+row1BorderSize, row1Y), "{}{}{}{}{}{}{}".format(row1Set1, row1Separator, row1Set2, row1Separator, row1Set3, row1Separator, row1Set4, row1Separator),
                    font=font3, fill=row1BorderColorConverted)
        imgObj.text((row1X, row1Y-row1BorderSize), "{}{}{}{}{}{}{}".format(row1Set1, row1Separator, row1Set2, row1Separator, row1Set3, row1Separator, row1Set4, row1Separator),
                    font=font3, fill=row1BorderColorConverted)
        imgObj.text((row1X, row1Y+row1BorderSize), "{}{}{}{}{}{}{}".format(row1Set1, row1Separator, row1Set2, row1Separator, row1Set3, row1Separator, row1Set4, row1Separator),
                    font=font3, fill=row1BorderColorConverted)
    # ? row 2
    if row2BorderStatus == "on":
        row2BorderColorObject = ColorListModel.objects.get(id=row2BorderColor)
        row2BorderColorSeparate = row2BorderColorObject.color_code.split(",")
        row2BorderColorConverted0 = int(row2BorderColorSeparate[0])
        row2BorderColorConverted1 = int(row2BorderColorSeparate[1])
        row2BorderColorConverted2 = int(row2BorderColorSeparate[2])
        row2BorderColorConverted = row2BorderColorConverted0, row2BorderColorConverted1, row2BorderColorConverted2

        imgObj.text((row2X-row2BorderSize, row2Y), "{}{}{}{}{}{}{}".format(row2Set1, row2Separator, row2Set2, row2Separator, row2Set3, row2Separator, row2Set4, row2Separator),
                    font=font3, fill=row2BorderColorConverted)
        imgObj.text((row2X+row2BorderSize, row2Y), "{}{}{}{}{}{}{}".format(row2Set1, row2Separator, row2Set2, row2Separator, row2Set3, row2Separator, row2Set4, row2Separator),
                    font=font3, fill=row2BorderColorConverted)
        imgObj.text((row2X, row2Y-row2BorderSize), "{}{}{}{}{}{}{}".format(row2Set1, row2Separator, row2Set2, row2Separator, row2Set3, row2Separator, row2Set4, row2Separator),
                    font=font3, fill=row2BorderColorConverted)
        imgObj.text((row2X, row2Y+row2BorderSize), "{}{}{}{}{}{}{}".format(row2Set1, row2Separator, row2Set2, row2Separator, row2Set3, row2Separator, row2Set4, row2Separator),
                    font=font3, fill=row2BorderColorConverted)
    # ? credit shop
    if creditShopBorderStatus == "on":
        creditShopBorderColorObject = ColorListModel.objects.get(
            id=creditShopBorderColor)
        creditShopBorderColorSeparate = creditShopBorderColorObject.color_code.split(
            ",")
        creditShopBorderColorConverted0 = int(creditShopBorderColorSeparate[0])
        creditShopBorderColorConverted1 = int(creditShopBorderColorSeparate[1])
        creditShopBorderColorConverted2 = int(creditShopBorderColorSeparate[2])
        creditShopBorderColorConverted = creditShopBorderColorConverted0, creditShopBorderColorConverted1, creditShopBorderColorConverted2

        imgObj.text((creditShopPosX-creditShopBorderSize, creditShopPosY), type,
                    font=font0, fill=creditShopBorderColorConverted)
        imgObj.text((creditShopPosX+creditShopBorderSize, creditShopPosY), type,
                    font=font0, fill=creditShopBorderColorConverted)
        imgObj.text((creditShopPosX, creditShopPosY-creditShopBorderSize), type,
                    font=font0, fill=creditShopBorderColorConverted)
        imgObj.text((creditShopPosX, creditShopPosY+creditShopBorderSize), type,
                    font=font0, fill=creditShopBorderColorConverted)
    # ? three sub border
    if threeSubBorderStatus == "on":
        threeSubBorderColorObject = ColorListModel.objects.get(
            id=threeSubBorderColor)
        threeSubBorderColorSeparate = threeSubBorderColorObject.color_code.split(
            ",")
        threeSubBorderColorConverted0 = int(threeSubBorderColorSeparate[0])
        threeSubBorderColorConverted1 = int(threeSubBorderColorSeparate[1])
        threeSubBorderColorConverted2 = int(threeSubBorderColorSeparate[2])
        threeSubBorderColorConverted = threeSubBorderColorConverted0, threeSubBorderColorConverted1, threeSubBorderColorConverted2

        imgObj.text((threeSubPosX-threeSubBorderSize, threeSubPosY),  "{}{}{}{}{}".format(threeNumberSet1,threeSubSeparator, threeNumberSet2,threeSubSeparator,threeNumberSet3),
                    font=threeSubFont, fill=threeSubBorderColorConverted)
        imgObj.text((threeSubPosX+threeSubBorderSize, threeSubPosY),  "{}{}{}{}{}".format(threeNumberSet1,threeSubSeparator, threeNumberSet2,threeSubSeparator,threeNumberSet3),
                    font=threeSubFont, fill=threeSubBorderColorConverted)
        imgObj.text((threeSubPosX, threeSubPosY-threeSubBorderSize),  "{}{}{}{}{}".format(threeNumberSet1,threeSubSeparator, threeNumberSet2,threeSubSeparator,threeNumberSet3),
                    font=threeSubFont, fill=threeSubBorderColorConverted)
        imgObj.text((threeSubPosX, threeSubPosY+threeSubBorderSize),  "{}{}{}{}{}".format(threeNumberSet1,threeSubSeparator, threeNumberSet2,threeSubSeparator,threeNumberSet3),
                    font=threeSubFont, fill=threeSubBorderColorConverted)
    # ? remark border
    if remarkBorderStatus == "on":
        remarkBorderColorObject = ColorListModel.objects.get(
            id=remarkBorderColor)
        remarkBorderColorSeparate = remarkBorderColorObject.color_code.split(
            ",")
        remarkBorderColorConverted0 = int(remarkBorderColorSeparate[0])
        remarkBorderColorConverted1 = int(remarkBorderColorSeparate[1])
        remarkBorderColorConverted2 = int(remarkBorderColorSeparate[2])
        remarkBorderColorConverted = remarkBorderColorConverted0, remarkBorderColorConverted1, remarkBorderColorConverted2

        imgObj.text((remarkPosX-remarkBorderSize, remarkPosY), remarkText,
                    font=remarkFont, fill=remarkBorderColorConverted)
        imgObj.text((remarkPosX+remarkBorderSize, remarkPosY),  remarkText,
                    font=remarkFont, fill=remarkBorderColorConverted)
        imgObj.text((remarkPosX, remarkPosY-remarkBorderSize),  remarkText,
                    font=remarkFont, fill=remarkBorderColorConverted)
        imgObj.text((remarkPosX, remarkPosY+remarkBorderSize),  remarkText,
                    font=remarkFont, fill=remarkBorderColorConverted)
    # * ================= END : BORDER =================
    # * ================= START : TEXT =================
    imgObj.text((txtPosX, txtPosY), type, font=font0, fill=textColorConverted)
    imgObj.text((datePosX, datePosY), curDate,
                font=font1, fill=dateColorConverted)
    imgObj.text((mainNumberPosX, mainNumberPosY), "{}{}{}".format(mainFirstNumber, mainNumSeparator,
                                                                  mainSecondNumber), font=font2, fill=mainNumFontColorConverted)
    imgObj.text((row1X, row1Y), "{}{}{}{}{}{}{}".format(row1Set1, row1Separator,
                row1Set2, row1Separator, row1Set3, row1Separator, row1Set4, row1Separator), font=font3, fill=row1ColorConverted)
    imgObj.text((row2X, row2Y), "{}{}{}{}{}{}{}".format(row2Set1, row2Separator,
                row2Set2, row2Separator, row2Set3, row2Separator, row2Set4, row2Separator), font=font3, fill=row2ColorConverted)
    imgObj.text((focusNumberX, focusNumberY), "{}".format(focusNumber),
                font=font4, fill=focusNumColorConverted)
    # * == START : THREE SET 
    if threeMainStatus == 'on':
        imgObj.text((threeMainPosX, threeMainPosY), "{}{}{}{}{}".format(mainThreeNumbers1,threeMainSeparator, mainThreeNumbers2,threeMainSeparator,mainThreeNumbers3), font=threeMainFont, fill=threeMainFontColorConverted)

    if threeSubStatus == 'on':
        imgObj.text((threeSubPosX, threeSubPosY), "{}{}{}{}{}".format(threeNumberSet1,threeSubSeparator, threeNumberSet2,threeSubSeparator,threeNumberSet3), font=threeSubFont, fill=threeSubFontColorConverted)

    if remarkStatus == 'on':
        imgObj.text((remarkPosX, remarkPosY), remarkText, font=remarkFont, fill=remarkFontColorConverted)

    # * == END : THREE SET 
    # * ================= END : TEXT =================

    img.save(location)
    imgLocation = '/static/images/result-hua/{}-result.jpg'.format(username)
    return imgLocation

#  สุ่มตัวเลข 0-9


def randomNumber():
    result = random.randint(0, 9)
    return result

# สุ่มตัวเลขขึ้นมา โดยต้องไปซ้ำกับใน list


def RandomNumberUniqueToList(list):
    checkDuplicated = True
    while checkDuplicated == True:
        # สุ่มเลข
        number = randomNumber()
        # ถ้ามีเลขนี้ในลิสต์แล้วให้สุ่มใหม่
        if number in list:
            number = randomNumber()
            checkDuplicated = True
        else:
            checkDuplicated = False
    return number

# คัดกรองตัวเลขแถวที่สอง โดยมีเงื่อนไขคือ ถ้าเลข 2 หลัก ของตัวเลขแถวที่สอง ซ้ำ กับ ตัวเลขของตัวแรก ให้สร้างใหม่ และแต่ละตัวภายในแถวที่สองห้ามซ้ำกัน

# จะสุ่มเป็นตัวอะไรก็ได้ ยกเว้นตัวที่ส่งเช้ามา เช่น ส่ง 3 เข้ามา มันจะสุ่มจนได้เลขอื่นที่ไม่ใช่ 3


def AvoidNumber(avoidNumber):
    check = True
    while check == True:
        random = randomNumber()
        if random == avoidNumber:
            check = True
        else:
            check = False
    return random

# สร้างชุดสุ่มหวย 2 หลัก


def generateNumberForSecondLine(subNumberRow2SecondUnitList, listSwapNumber, mainSecondNumber, subNumberSecondUnit):
    setOfNumber = str(mainSecondNumber)+str(subNumberSecondUnit)
    if setOfNumber in listSwapNumber:
        newSubNumberSecondUnit = RandomNumberUniqueToList(
            subNumberRow2SecondUnitList)
        # เพิ่มเข้าไปในลิสต์เพื่อไม่ให้การสุ่มตัวเลขครั้งใหม่ ซ้ำกับเลขเก่า และเลขที่เพิ่งสร้างได้เมื่อกี้
        subNumberRow2SecondUnitList.append(newSubNumberSecondUnit)
    else:
        newSubNumberSecondUnit = subNumberSecondUnit
    return newSubNumberSecondUnit


def random2NumberResult(profileObject):
    # Random integer
    mainFirstNumber = randomNumber()
    mainSecondNumber = AvoidNumber(mainFirstNumber)

    # random one of two
    mainNumberList = [mainFirstNumber, mainSecondNumber]
    focusNumber = random.choice(mainNumberList)

    subNumberRow1SecondUnitList = []
    # เอา ตัวหลักเข้า list เพื่อไม่ให้ตัวอื่นๆในแถวแรกที่สร้างขึ้นมาเบิ้ลกับตัวแรก
    subNumberRow1SecondUnitList.append(mainFirstNumber)

    subNumberRow1SecondUnit1 = RandomNumberUniqueToList(
        subNumberRow1SecondUnitList)
    subNumberRow1SecondUnitList.append(subNumberRow1SecondUnit1)
    subNumberRow1SecondUnit2 = RandomNumberUniqueToList(
        subNumberRow1SecondUnitList)
    subNumberRow1SecondUnitList.append(subNumberRow1SecondUnit2)
    subNumberRow1SecondUnit3 = RandomNumberUniqueToList(
        subNumberRow1SecondUnitList)
    subNumberRow1SecondUnitList.append(subNumberRow1SecondUnit3)
    subNumberRow1SecondUnit4 = RandomNumberUniqueToList(
        subNumberRow1SecondUnitList)
    subNumberRow1SecondUnitList.append(subNumberRow1SecondUnit4)

    # * สร้าง List ขึ้นมาสำหรับการเช็คซ้ำ
    subNumberRow2SecondUnitList = []

    # * ถ้าแถวที่ 1 มีเลข รูด แล้ว แถวที่ 2 จะต้องยกเว้นการสุ่มโดนเลข วิ่ง เช่น เลข วิ่ง-รูด เป็น 4-6 ถ้าแถวที่ 1 มี 46 แล้ว แถวข้างล่างต้องสุ่มให้ไม่มีเลข 6
    # * แต่ถ้าแถวที่ 1 ไม่มีเลขรูด สามารถสุ่มยังไงก็ได้ แสดงว่าถ้าแถวแรกมีเลขรูดแล้ว เราก็จะใส่เลข วิ่ง เข้าไปใน List เพื่อจะได้ไม่สุ่มโดนเลข วิ่ง
    if subNumberRow1SecondUnit1 == mainSecondNumber or subNumberRow1SecondUnit2 == mainSecondNumber or subNumberRow1SecondUnit3 == mainSecondNumber or subNumberRow1SecondUnit4 == mainSecondNumber:
        # เพิ่มเลข "รูด" เข้าไป
        subNumberRow2SecondUnitList.append(mainFirstNumber)

    # เอาเลขหลักสิบของตัวหลักมาใส่ list เพื่อไม่ให้เลขหลักหน่วยที่สร้างขึ้นมาในแถวที่สอง ซ้ำกับเลขหลักหน่วยของตัวหลัก
    subNumberRow2SecondUnitList.append(mainSecondNumber)

    subNumberRow2SecondUnit1 = RandomNumberUniqueToList(
        subNumberRow2SecondUnitList)
    subNumberRow2SecondUnitList.append(subNumberRow2SecondUnit1)
    subNumberRow2SecondUnit2 = RandomNumberUniqueToList(
        subNumberRow2SecondUnitList)
    subNumberRow2SecondUnitList.append(subNumberRow2SecondUnit2)
    subNumberRow2SecondUnit3 = RandomNumberUniqueToList(
        subNumberRow2SecondUnitList)
    subNumberRow2SecondUnitList.append(subNumberRow2SecondUnit3)
    subNumberRow2SecondUnit4 = RandomNumberUniqueToList(
        subNumberRow2SecondUnitList)
    subNumberRow2SecondUnitList.append(subNumberRow2SecondUnit4)

    # * ถ้า random_mode เป็นแบบต้องมีเลข วิ่ง-รูด ในเลขเจาะ จะเข้าเงื่อนไขนี้
    # * ถ้าตัวเลขหลักหน่วยของแถวที่ 1 และ 2 ไม่มีเลขหลักอีกตัวปนอยู่เลย เราจะบังคับให้แถวที่ 1 ตัวที่ 4 เปลี่ยนเลขเป็นเลข หลักหน่วยของตัวหลัก เช่น ตัวหลักเป็น 2 - 9 ถ้าแถวที่ 1 ไม่มี 29 และแถวที่ 2 ไม่มี 92 ก็จะให้ตัวที่ 4 ของแถวที่ 1 เป็น 29
    if profileObject.random_mode == 'force_have_main_number':
        if mainSecondNumber not in subNumberRow1SecondUnitList:
            if mainFirstNumber not in subNumberRow2SecondUnitList:
                subNumberRow1SecondUnit4 = mainSecondNumber

    # Sort Number
    sortNumberSecondUnitList = [
        subNumberRow1SecondUnit1, subNumberRow1SecondUnit2, subNumberRow1SecondUnit3, subNumberRow1SecondUnit4]
    newSortedNumberSecondUnit = sorted(sortNumberSecondUnitList)
    sortNumber2SecondUnitList = [
        subNumberRow2SecondUnit1, subNumberRow2SecondUnit2, subNumberRow2SecondUnit3, subNumberRow2SecondUnit4]
    newSortedNumber2SecondUnit = sorted(sortNumber2SecondUnitList)

    row1Set1 = str(mainFirstNumber) + str(newSortedNumberSecondUnit[0])
    row1Set2 = str(mainFirstNumber) + str(newSortedNumberSecondUnit[1])
    row1Set3 = str(mainFirstNumber) + str(newSortedNumberSecondUnit[2])
    row1Set4 = str(mainFirstNumber) + str(newSortedNumberSecondUnit[3])

    row2Set1 = str(mainSecondNumber) + str(newSortedNumber2SecondUnit[0])
    row2Set2 = str(mainSecondNumber) + str(newSortedNumber2SecondUnit[1])
    row2Set3 = str(mainSecondNumber) + str(newSortedNumber2SecondUnit[2])
    row2Set4 = str(mainSecondNumber) + str(newSortedNumber2SecondUnit[3])


    #* random main 3 numbers
    randomMainThreeNumbersList = [mainFirstNumber, mainSecondNumber,subNumberRow1SecondUnit1,subNumberRow1SecondUnit2,subNumberRow1SecondUnit3,subNumberRow1SecondUnit4,subNumberRow2SecondUnit1,subNumberRow2SecondUnit2,subNumberRow2SecondUnit3,subNumberRow2SecondUnit4]
    randomMainThreeNumbersUniqueList = []
    randomMainThreeNumbersResult1 = random.choice(randomMainThreeNumbersList)
    randomMainThreeNumbersUniqueList.append(randomMainThreeNumbersResult1)
    randomMainThreeNumbersResult2 = RandomNumberForMainThreeNumbers(randomMainThreeNumbersUniqueList,randomMainThreeNumbersList)
    randomMainThreeNumbersUniqueList.append(randomMainThreeNumbersResult2)
    randomMainThreeNumbersResult3 = RandomNumberForMainThreeNumbers(randomMainThreeNumbersUniqueList,randomMainThreeNumbersList)
    randomMainThreeNumbersUniqueList.append(randomMainThreeNumbersResult3)

    #* สุ่มจำนวนว่าใน 3 ชุดนั้น จะให้มีเลขที่เกี่ยวข้องกับ 2 หลักทั้งหมดกี่ชุด
    amountRelatedSetOfThreeNumbers = random.randint(1,3)

    #* random n set of above to put after main three numbers
    randomPairForEachSetOfThereNumberMainNumber = [
    [mainFirstNumber, mainSecondNumber]
    ]    
    randomPairForEachSetOfThereNumberRow1 = [
        [mainFirstNumber, subNumberRow1SecondUnit2], [mainFirstNumber, subNumberRow1SecondUnit3], [mainFirstNumber, subNumberRow1SecondUnit4]
    ]    
    randomPairForEachSetOfThereNumberRow2 = [[mainSecondNumber,subNumberRow2SecondUnit1],[mainSecondNumber,subNumberRow2SecondUnit2],[mainSecondNumber,subNumberRow2SecondUnit3]
    ,[mainSecondNumber,subNumberRow2SecondUnit4]
    ]

    # set default
    resultRandomSubNumberThree1 = ""
    resultRandomSubNumberThree2 = ""
    resultRandomSubNumberThree3 = ""

    if amountRelatedSetOfThreeNumbers >= 1:
        resultRandomSubNumberThree1 = random.choices(randomPairForEachSetOfThereNumberRow1)
        #? ถ้าสุ่มแล้วได้เลข 2 ให้ swap ตัวเลข
        randomSwap = random.randint(1,2)
        if randomSwap == 2:
            resultRandomSubNumberThree1[0][0],resultRandomSubNumberThree1[0][1] = resultRandomSubNumberThree1[0][1],resultRandomSubNumberThree1[0][0]
        resultRandomSubNumberThree1_1 = resultRandomSubNumberThree1[0][0]
        resultRandomSubNumberThree1_2 = resultRandomSubNumberThree1[0][1]
    if amountRelatedSetOfThreeNumbers > 1:
        resultRandomSubNumberThree2 = random.choices(randomPairForEachSetOfThereNumberRow2)
        #? ถ้าสุ่มแล้วได้เลข 2 ให้ swap ตัวเลข
        randomSwap = random.randint(1,2)
        if randomSwap == 2:
            resultRandomSubNumberThree2[0][0],resultRandomSubNumberThree2[0][1] = resultRandomSubNumberThree2[0][1],resultRandomSubNumberThree2[0][0]
        resultRandomSubNumberThree2_1 = resultRandomSubNumberThree2[0][0]
        resultRandomSubNumberThree2_2 = resultRandomSubNumberThree2[0][1]
    else:
        #? สุ่มเลขมั่วๆ จากเลขในใบได้เลย
        resultRandomSubNumberThree2_1 = random.choice(randomMainThreeNumbersList)
        resultRandomSubNumberThree2_2 = random.choice(randomMainThreeNumbersList)
        
    if amountRelatedSetOfThreeNumbers >2:
        resultRandomSubNumberThree3 = random.choices(randomPairForEachSetOfThereNumberMainNumber)
        #? ถ้าสุ่มแล้วได้เลข 2 ให้ swap ตัวเลข
        randomSwap = random.randint(1,2)
        if randomSwap == 2:
            resultRandomSubNumberThree3[0][0],resultRandomSubNumberThree3[0][1] = resultRandomSubNumberThree3[0][1],resultRandomSubNumberThree3[0][0]
        resultRandomSubNumberThree3_1 = resultRandomSubNumberThree3[0][0]
        resultRandomSubNumberThree3_2 = resultRandomSubNumberThree3[0][1]
    else:
        #? สุ่มเลขมั่วๆ จากเลขในใบได้เลย
        resultRandomSubNumberThree3_1 = random.choice(randomMainThreeNumbersList)
        resultRandomSubNumberThree3_2 = random.choice(randomMainThreeNumbersList)

    threeNumberSet1 = str(randomMainThreeNumbersResult1) + str(resultRandomSubNumberThree1_1) + str(resultRandomSubNumberThree1_2)
    threeNumberSet2 = str(randomMainThreeNumbersResult2) + str(resultRandomSubNumberThree2_1) + str(resultRandomSubNumberThree2_2)
    threeNumberSet3 = str(randomMainThreeNumbersResult3) + str(resultRandomSubNumberThree3_1) + str(resultRandomSubNumberThree3_2)

    result = [mainFirstNumber, mainSecondNumber, focusNumber, row1Set1,
              row1Set2, row1Set3, row1Set4, row2Set1, row2Set2, row2Set3, row2Set4,
              randomMainThreeNumbersResult1,randomMainThreeNumbersResult2,randomMainThreeNumbersResult3,
              threeNumberSet1,threeNumberSet2,threeNumberSet3
              ]
    return result


def RandomNumberUniqueToListFrom1To3(list):
    checkDuplicated = True
    while checkDuplicated == True:
        # สุ่มเลข
        number = random.randint(1, 3)
        # ถ้ามีเลขนี้ในลิสต์แล้วให้สุ่มใหม่
        if number in list:
            number = random.randint(1, 3)
            checkDuplicated = True
        else:
            checkDuplicated = False
    return number


def RandomNumberForMainThreeNumbers(listUnique,randomMainThreeNumbersList):
    checkDuplicated = True
    while checkDuplicated == True:
        # สุ่มเลข
        number = random.choice(randomMainThreeNumbersList)
        # ถ้ามีเลขนี้ในลิสต์แล้วให้สุ่มใหม่
        if number in listUnique:
            number = random.choice(randomMainThreeNumbersList)
            checkDuplicated = True
        else:
            checkDuplicated = False
    return number