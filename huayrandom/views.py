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
        if(houseName != ""):
            if(houseName == "none"):
                request.session['error'] = "error"
                return redirect('backend')
            elif(nextPage == "huay"):
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
def AddUser(request, username):
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        username = data.get('username')
        creditShop = data.get('credit_shop')
        expireDate = data.get('expire_date')
        expireTime = data.get('expire_time')

        try:
            checkDuplicated = User.objects.get(username=username)
            request.session['error'] = 'error'
            return redirect('list_user', username)
        except:

            addData = User()
            addData.username = username
            addData.password = "!Test1234"
            addData.save()

            addProfileData = ProfileModel()
            addProfileData.user = User.objects.get(username=username)
            addProfileData.house_name = username
            addProfileData.credit_shop = creditShop
            addProfileData.expire_date = "{} {}:00".format(expireDate,expireTime)
            addProfileData.save()

            huayListObject = HuayListModel.objects.all()
            for item in huayListObject:
                addHuayData = HuayTypeModel()
                addHuayData.user = User.objects.get(username=username)
                addHuayData.huay_list = HuayListModel.objects.get(id=item.id)
                addHuayData.font_text = "PromptBold.tff"
                addHuayData.font_number = "Kanit.tff"
                addHuayData.text_color = "255,255,255"
                addHuayData.border_size = 4
                addHuayData.border_color = "0,0,0"
                addHuayData.text_pos_x = 500
                addHuayData.text_pos_y = 560
                addHuayData.text_font_size = 90
                addHuayData.date_pos_x = 1220
                addHuayData.date_pos_y = 45
                addHuayData.date_font_size = 30
                addHuayData.main_num_pos_x = 550
                addHuayData.main_num_pos_y = 720
                addHuayData.main_num_font_size = 90
                addHuayData.focus_num_pos_x = 1025
                addHuayData.focus_num_pos_y = 780
                addHuayData.focus_num_font_size = 230 
                addHuayData.row1_x = 170
                addHuayData.row1_y = 900
                addHuayData.row2_x = 170
                addHuayData.row2_y = 1000
                addHuayData.row_font_size = 90
                addHuayData.save()

            request.session['status'] = 'Done'

            return redirect('list_user', username)

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

        editData = ProfileModel.objects.get(user=userObject)
        editData.user = userObject
        editData.credit_shop = creditShop
        editData.expire_date =  "{} {}:00".format(expireDate,expireTime)
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
    huayObject = HuayTypeModel.objects.filter(user=userObject)
    profileObject = ProfileModel.objects.get(user=userObject)

    context['huayObject'] = huayObject
    context['username'] = username
    context['houseName'] = profileObject.house_name

    if 'statusedit' in request.session:
        context['statusedit'] = request.session['statusedit']
        request.session['statusedit'] = ''  # clear stuck error in session
    return render(request, 'huay/list_huay.html', context)


@login_required
def AddDetailPicture(request, username):
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
        borderColor = data.get('border_color')
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
            checkDuplicated = HuayTypeModel.objects.get(id=huayListId)
            request.session['error'] = 'error'
            return redirect('add_huay', username)
        except:
            getFontName = FontListModel.objects.get(id=fontTextId) 
            getFontName2 = FontListModel.objects.get(id=fontNumberId) 
            addData = HuayTypeModel()
            addData.user = User.objects.get(id=username)
            addData.huay_list = HuayListModel.objects.get(id=huayListId)
            addData.font_text = getFontName.font_name
            addData.font_number = getFontName2.font_name
            addData.text_color = textColor
            addData.border_size = borderWidth
            addData.border_color = borderColor
            addData.text_pos_x = textPosX
            addData.text_pos_y = textPosY
            addData.text_font_size = textSize
            addData.date_pos_x = dataPosX
            addData.date_pos_y = dataPosY
            addData.date_font_size = dataFontsize
            addData.main_num_pos_x = mainNumberPosX
            addData.main_num_pos_y = mainNumberPosY
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

    context['huayList'] = huayAllList
    context['data'] = profileObject
    context['fontList'] = fontListObject

    return render(request, 'huay/add_huay.html', context)


@login_required
def EditDetailPicture(request, username, huay_id):
    context = {}
    userObject = User.objects.get(username=username)
    
    if request.method == 'POST':
        data = request.POST.copy()
        huayListId = data.get('huay_list_id')
        fontTextId = data.get('font_text_id')
        textColor = data.get('text_color')
        textPosX = data.get('text_pos_x')
        textPosY = data.get('text_pos_y')
        textSize = data.get('text_size')
        borderWidth = data.get('border_width')
        borderColor = data.get('border_color')
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

        getFontName = FontListModel.objects.get(id=fontTextId) 
        getFontName2 = FontListModel.objects.get(id=fontNumberId) 
        
        editData = HuayTypeModel.objects.get(id=huayListId,user=userObject)

        editData.user = User.objects.get(username=username)
        editData.font_text = getFontName.font_name
        editData.font_number = getFontName2.font_name
        editData.text_color = textColor
        editData.border_size = borderWidth
        editData.border_color = borderColor
        editData.text_pos_x = textPosX
        editData.text_pos_y = textPosY
        editData.text_font_size = textSize
        editData.date_pos_x = dataPosX
        editData.date_pos_y = dataPosY
        editData.date_font_size = dataFontsize
        editData.main_num_pos_x = mainNumberPosX
        editData.main_num_pos_y = mainNumberPosY
        editData.main_num_font_size = mainNumberSize
        editData.focus_num_pos_x = focusPosX
        editData.focus_num_pos_y = focusPosY
        editData.focus_num_font_size = focusFontsize
        editData.row1_x = numberRow1PosX
        editData.row1_y = numberRow1PosY
        editData.row2_x = numberRow2PosX
        editData.row2_y = numberRow2PosY
        editData.row_font_size = numberRowFontsize
        editData.save()

        request.session['statusedit'] = 'Done'

        return redirect('edit_huay', username,huay_id)

    userObject = User.objects.get(username=username)
    profileObject = ProfileModel.objects.get(user=userObject)
    huayTypeObject = HuayTypeModel.objects.get(id=huay_id,user=userObject)
    fontListObject = FontListModel.objects.all()

    context['huayTypeObject'] = huayTypeObject
    context['data'] = profileObject
    context['huayId'] = huay_id
    context['fontList'] = fontListObject
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
        return render(request,'result/index.html',context)
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
    textColorSplit = data.text_color.split(",")
    borderColorSplit = data.border_color.split(",")

    imgLocation = GenerateImageWIthText(username,data.huay_list.full_name, data.font_text, data.font_number, (int(textColorSplit[0]), int(textColorSplit[1]), int(textColorSplit[2])), 4, (int(borderColorSplit[0]), int(borderColorSplit[1]), int(borderColorSplit[2])), data.text_pos_x, data.text_pos_y, data.text_font_size,
                                        data.date_pos_x, data.date_pos_y, data.date_font_size, data.main_num_pos_x, data.main_num_pos_y, data.main_num_font_size, data.focus_num_pos_x, data.focus_num_pos_y, data.focus_num_font_size, data.row1_x, data.row1_y, data.row2_x, data.row2_y, data.row_font_size)
    

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


def GenerateImageWIthText(username,type, fontText, fontNumber, textColor, borderSize, borderColor, txtPosX, txtPosY, txtFontSize, datePosX, datePosY, dateFontSize, mainNumberPosX, mainNumberPosY, mainNumberFontSize, focusNumberX, focusNumberY, focusNumberFontSize, row1X, row1Y, row2X, row2Y, rowFontSize):
    randomResult = random2NumberResult()
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
    path = os.getcwd()
    locationTemplate = '/home/cheetah/random.huay-vip-net/static/images/template-hua/{}-template.jpg'.format(username)
    # locationTemplate = path+'/static/images/template-hua/{}-template.jpg'.format(username)
    
    img = Image.open(locationTemplate)
    imgObj = ImageDraw.Draw(img)

    # Set font
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

    # Set Date
    cueDateTime = datetime.now() + relativedelta(years=543)
    curDate = cueDateTime.strftime(r'%d/%m/%y')

    # BORDER NAME TEXT
    imgObj.text((txtPosX-borderSize, txtPosY), type,
                font=font0, fill=borderColor)
    imgObj.text((txtPosX+borderSize, txtPosY), type,
                font=font0, fill=borderColor)
    imgObj.text((txtPosX, txtPosY-borderSize), type,
                font=font0, fill=borderColor)
    imgObj.text((txtPosX, txtPosY+borderSize), type,
                font=font0, fill=borderColor)

    # TEXT
    imgObj.text((txtPosX, txtPosY), type, font=font0, fill=textColor)
    imgObj.text((datePosX, datePosY), curDate, font=font1, fill=textColor)
    imgObj.text((mainNumberPosX, mainNumberPosY), "{} - {}".format(mainFirstNumber,
                                                                   mainSecondNumber), font=font2, fill=textColor)
    imgObj.text((row1X, row1Y), "{} - {} - {} - {}".format(row1Set1,
                row1Set2, row1Set3, row1Set4), font=font3, fill=textColor)
    imgObj.text((row2X, row2Y), "{} - {} - {} - {}".format(row2Set1,
                row2Set2, row2Set3, row2Set4), font=font3, fill=textColor)
    imgObj.text((focusNumberX, focusNumberY), "{}".format(focusNumber),
                font=font4, fill=textColor)

    location = '/home/cheetah/random.huay-vip-net/static/images/result-hua/{}-result.jpg'.format(username)
    # location = path+'/static/images/result-hua/{}-result.jpg'.format(username)
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


def generateNumberForSecondLine(listSwapNumber, mainSecondNumber, subNumberSecondUnit):
    setOfNumber = str(mainSecondNumber)+str(subNumberSecondUnit)
    if setOfNumber in listSwapNumber:
        newSubNumberSecondUnit = AvoidNumber(subNumberSecondUnit)
    else:
        newSubNumberSecondUnit = subNumberSecondUnit
    return newSubNumberSecondUnit



def random2NumberResult():
    allNumberList = []

    # Random integer
    mainFirstNumber = randomNumber()
    mainSecondNumber = AvoidNumber(mainFirstNumber)

    #append first 2 number to list
    allNumberList.append(mainFirstNumber)
    allNumberList.append(mainSecondNumber)

    # random one of two
    listForFocusNumber = [mainFirstNumber, mainSecondNumber]
    focusNumber = random.choice(listForFocusNumber)

    subNumberRow1SecondUnitList = []
    # เอา ตัวหลักเข้า list เพื่อไม่ให้ตัวอื่นๆในแถวแรกที่สร้างขึ้นมาเบิ้ลกับตัวแรก
    subNumberRow1SecondUnitList.append(mainFirstNumber)

    subNumberRow1SecondUnit1 = RandomNumberUniqueToList(subNumberRow1SecondUnitList)
    subNumberRow1SecondUnitList.append(subNumberRow1SecondUnit1)
    subNumberRow1SecondUnit2 = RandomNumberUniqueToList(subNumberRow1SecondUnitList)
    subNumberRow1SecondUnitList.append(subNumberRow1SecondUnit2)
    subNumberRow1SecondUnit3 = RandomNumberUniqueToList(subNumberRow1SecondUnitList)
    subNumberRow1SecondUnitList.append(subNumberRow1SecondUnit3)
    subNumberRow1SecondUnit4 = RandomNumberUniqueToList(subNumberRow1SecondUnitList)
    subNumberRow1SecondUnitList.append(subNumberRow1SecondUnit4)


    swapNumber = [str(subNumberRow1SecondUnit1)+str(mainFirstNumber), str(subNumberRow1SecondUnit2)+str(mainFirstNumber),
                  str(subNumberRow1SecondUnit3)+str(mainFirstNumber), str(subNumberRow1SecondUnit4)+str(mainFirstNumber)]

    # ตัดตัวเลขที่ซ้ำกันออกทั้งหมดก่อนที่จะไปเช็คกับคำในแถวแรก
    subNumberRow2SecondUnitList = []
    # เอา ตัวหลักทั้งสองตัวเข้า list เพื่อไม่ให้เลขหลักหน่วยที่สร้างขึ้นมาในแถวที่สอง ซ้ำกับเลขหลักสิบของตัวหลัก
    subNumberRow1SecondUnitList.append(mainFirstNumber)
    # เอาเลขหลักสิบของตัวหลักมาใส่ list เพื่อไม่ให้เลขหลักหน่วยที่สร้างขึ้นมาในแถวที่สอง ซ้ำกับเลขหลักหน่วยของตัวหลัก
    subNumberRow1SecondUnitList.append(mainSecondNumber)

    subNumberRow2SecondUnit1 = RandomNumberUniqueToList(subNumberRow2SecondUnitList)
    subNumberRow2SecondUnitList.append(subNumberRow2SecondUnit1)
    subNumberRow2SecondUnit2 = RandomNumberUniqueToList(subNumberRow2SecondUnitList)
    subNumberRow2SecondUnitList.append(subNumberRow2SecondUnit2)
    subNumberRow2SecondUnit3 = RandomNumberUniqueToList(subNumberRow2SecondUnitList)
    subNumberRow2SecondUnitList.append(subNumberRow2SecondUnit3)
    subNumberRow2SecondUnit4 = RandomNumberUniqueToList(subNumberRow2SecondUnitList)
    subNumberRow2SecondUnitList.append(subNumberRow2SecondUnit4)
    
    # เช็คซ้ำกับแถวที่ 1
    subNumberRow2SecondUnit1 = generateNumberForSecondLine(
        swapNumber, mainSecondNumber, subNumberRow2SecondUnit1)
    subNumberRow2SecondUnit2 = generateNumberForSecondLine(
        swapNumber, mainSecondNumber, subNumberRow2SecondUnit2)
    subNumberRow2SecondUnit3 = generateNumberForSecondLine(
        swapNumber, mainSecondNumber, subNumberRow2SecondUnit3)
    subNumberRow2SecondUnit4 = generateNumberForSecondLine(
        swapNumber, mainSecondNumber, subNumberRow2SecondUnit4)


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

    result = [mainFirstNumber, mainSecondNumber, focusNumber, row1Set1,
              row1Set2, row1Set3, row1Set4, row2Set1, row2Set2, row2Set3, row2Set4]
    return result
