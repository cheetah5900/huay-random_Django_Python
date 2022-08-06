from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from huayrandom.models import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random
from datetime import datetime
import os


def Index(request):
    context = {}
    if request.method == 'POST':
        data = request.POST.copy()
        getUsername = data.get('username')
        # authen is function for User model for finding user
        try:
            userObject = User.objects.get(username=getUsername)
            return redirect('home', userObject.username)
        except:
            request.session['error'] = 'ไม่มีบ้านดังกล่าว'
            return redirect('index')

    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''  # clear stuck error in session

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
        if(houseName != ""):
            if(houseName == "none"):
                request.session['error'] = "error"
                return redirect('backend')
            else:
                return redirect('add_detail_picture', houseName)
        else:
            return redirect('backend')
    profileObject = ProfileModel.objects.all()
    context['profileObject'] = profileObject

    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''  # clear stuck error in session

    return render(request, 'adddata/choose_house.html', context)


@login_required
def AddDetailPicture(request, username):
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        huayListId = data.get('huay_list_id')
        textFont = data.get('text_font')
        textColor = data.get('text_color')
        textPosX = data.get('text_pos_x')
        textPosY = data.get('text_pos_y')
        textSize = data.get('text_size')
        borderWidth = data.get('border_width')
        borderColor = data.get('border_color')
        numberFont = data.get('number_font')
        numberColor = data.get('number_color')
        mainNumberPosX = data.get('main_number_pos_x')
        mainNumberPosY = data.get('main_number_pos_y')
        mainNumberSize = data.get('main_number_size')
        dataPosX = data.get('data_pos_x')
        dataPosY = data.get('data_pos_y')
        dataFontsize = data.get('data_fontsize')
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
            return redirect('add_detail_picture', username)
        except:
            addData = HuayTypeModel()
            addData.user = User.objects.get(id=request.user.id)
            addData.huay_list = HuayListModel.objects.get(id=huayListId)
            addData.font_text = textFont
            addData.font_number = numberFont
            addData.text_color = textColor
            addData.border_size = borderWidth
            addData.border_color = borderColor
            addData.text_pos_x = textPosX
            addData.text_pos_y = textPosY
            addData.text_font_size = textSize
            addData.data_pos_x = dataPosX
            addData.data_pos_y = dataPosY
            addData.data_font_size = dataFontsize
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

            return redirect('add_detail_picture', username)

    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''  # clear stuck error in session
    if 'status' in request.session:
        context['status'] = request.session['status']
        request.session['status'] = ''  # clear stuck error in session

    userObject = User.objects.get(username=username)
    profileObject = ProfileModel.objects.get(user=userObject)

    huayFilter = HuayTypeModel.objects.filter(user_id=request.user.id)
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

    context['huayList'] = huayAllList
    context['data'] = profileObject
    return render(request, 'adddata/add_detail_picture.html', context)


def Home(request, username):
    context = {}
    resultCheckExpire = CheckExpireDate(request.user.id)
    if resultCheckExpire == "หมดเขตแล้ว":
        pass
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
            print("X", x)
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
            listPurple = [1,5,9,13,17,21,25,29]
            listOrange = [2,6,10,14,18,22,26,30]
            listPink = [3,7,11,15,19,23,27,31]
            listGreen = [4,8,12,16,20,24,28,32]

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
        context['resultCheckExpire'] = resultCheckExpire
        context['zipDataForLoopMorning'] = zipDataForLoopMorning
        context['zipDataForLoopAfternoon'] = zipDataForLoopAfternoon
        context['zipDataForLoopEvening'] = zipDataForLoopEvening
        context['zipDataForLoopOther'] = zipDataForLoopOther

        return render(request, 'index.html', context)
    except:
        # return redirect('index')
        pass


def Result(request, type):
    context = {}

    resultCheckExpire = CheckExpireDate(request.user.id)
    if resultCheckExpire == "หมดเขตแล้ว":
        # return redirect('Home')
        pass
    else:
        resultCheckExpire = ""
    #  Get Huay Datac
    data = HuayTypeModel.objects.get(link=type)
    textColorSplit = data.text_color.split(",")
    borderColorSplit = data.border_color.split(",")

    imgLocation = GenerateImageWIthText(data.page_name, data.font_text, data.font_number, (int(textColorSplit[0]), int(textColorSplit[1]), int(textColorSplit[2])), 4, (int(borderColorSplit[0]), int(borderColorSplit[1]), int(borderColorSplit[2])), data.text_pos_x, data.text_pos_y, data.text_font_size,
                                        data.data_pos_x, data.data_pos_y, data.data_font_size, data.main_num_pos_x, data.main_num_pos_y, data.main_num_font_size, data.focus_num_pos_x, data.focus_num_pos_y, data.focus_num_font_size, data.row1_x, data.row1_y, data.row2_x, data.row2_y, data.row_font_size)

    profileObject = ProfileModel.objects.get(user_id=request.user.id)
    day = profileObject.expire_date.strftime("%d")
    month = profileObject.expire_date.strftime("%m")
    year = profileObject.expire_date.strftime("%Y")
    thaiMonth = ConvertToThaiMonth(month)
    expireDateThai = "{} {} {}".format(day, thaiMonth, year)

    context['expireDateThai'] = expireDateThai
    context['link'] = data.link
    context['imgLocation'] = imgLocation

    return render(request, 'result/index.html', context)


def AddData(request):
    context = {}
    resultCheckExpire = CheckExpireDate(request.user.id)
    if resultCheckExpire == "หมดเขตแล้ว":
        pass
    else:
        resultCheckExpire = ""

    return render(request, 'adddata/adddata.html', context)


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


def CheckExpireDate(uid):
    try:
        userObject = User.objects.get(id=uid)
        profileObject = ProfileModel.objects.get(user=userObject)
        expireDate = profileObject.expire_date
        expireDateNewFormat = expireDate.strftime("%Y%m%d%H%M")
        timeNow = datetime.now()
        currentTime = timeNow.strftime("%Y%m%d%H%M")

        if currentTime >= expireDateNewFormat:
            profileObject.usertype = 'member'
            profileObject.expire_date = None
            profileObject.save()
            return "ตัดสิทธิ์แล้ว"
        if currentTime < expireDateNewFormat:
            pass
    except:
        pass
# ฟังก์ชั่นสร้างรูปของบ้านเพิ่มทรัพย์


def GenerateImageWIthText(type, fontText, fontNumber, textColor, borderSize, borderColor, txtPosX, txtPosY, txtFontSize, datePosX, datePosY, dateFontSize, mainNumberPosX, mainNumberPosY, mainNumberFontSize, focusNumberX, focusNumberY, focusNumberFontSize, row1X, row1Y, row2X, row2Y, rowFontSize):
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
    locationTemplate = path+r'\static\images\template-hua\template.jpg'
    img = Image.open(locationTemplate)
    imgObj = ImageDraw.Draw(img)

    # Set font
    font0 = ImageFont.truetype(
        'static/assets/fonts/{}'.format(fontText), txtFontSize)
    font1 = ImageFont.truetype(
        'static/assets/fonts/{}'.format(fontNumber), dateFontSize)
    font2 = ImageFont.truetype(
        'static/assets/fonts/{}'.format(fontNumber), mainNumberFontSize)
    font3 = ImageFont.truetype(
        'static/assets/fonts/{}'.format(fontNumber), rowFontSize)
    font4 = ImageFont.truetype(
        'static/assets/fonts/{}'.format(fontNumber), focusNumberFontSize)

    # Set Date
    # cueDateTime = datetime.now() + relativedelta(years=543)
    cueDateTime = datetime.now()
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
                                                                   mainSecondNumber), font=font3, fill=textColor)
    imgObj.text((row1X, row1Y), "{} - {} - {} - {}".format(row1Set1,
                row1Set2, row1Set3, row1Set4), font=font2, fill=textColor)
    imgObj.text((row2X, row2Y), "{} - {} - {} - {}".format(row2Set1,
                row2Set2, row2Set3, row2Set4), font=font2, fill=textColor)
    imgObj.text((focusNumberX, focusNumberY), "{}".format(focusNumber),
                font=font4, fill=textColor)

    location = path+r'\static\images\result-hua\result.jpg'
    img.save(location)
    imgLocation = r'/static/images/result-hua/result.jpg'
    return imgLocation

#  สุ่มตัวเลข 0-9


def randomNumber():
    result = random.randint(0, 9)
    return result

# ตัดตัวเลขที่ซ้ำตอนสร้างเลขหลักที่สอง


def removeDuplicateNumber(list):
    checkDuplicated = True
    while checkDuplicated == True:
        subNumberSecondUnit = randomNumber()
        if subNumberSecondUnit not in list:
            list.append(subNumberSecondUnit)
            checkDuplicated = False
        else:
            pass
    return subNumberSecondUnit

# คัดกรองตัวเลขแถวที่สอง โดยมีเงื่อนไขคือ ถ้าเลข 2 หลัก ของตัวเลขแถวที่สอง ซ้ำ กับ ตัวเลขของตัวแรก ให้สร้างใหม่ และแต่ละตัวภายในแถวที่สองห้ามซ้ำกัน


def generateNumberForSecondLine(listSwapNumber, mainSecondNumber, subNumberSecondUnit):
    setOfNumber = str(mainSecondNumber)+str(subNumberSecondUnit)
    checkDuplicated = True
    while checkDuplicated == True:
        if setOfNumber in listSwapNumber:
            subNumberSecondUnit = randomNumber()
            setOfNumber = str(mainSecondNumber)+str(subNumberSecondUnit)
            checkDuplicated = True
        else:
            checkDuplicated = False
    return subNumberSecondUnit

# สร้างชุดสุ่มหวย 2 หลัก


def random2NumberResult():

    # Random integer
    mainNumberList = []
    mainFirstNumber = randomNumber()
    mainNumberList.append(mainFirstNumber)
    mainSecondNumber = removeDuplicateNumber(mainNumberList)

    # random one of two
    list = [mainFirstNumber, mainSecondNumber]
    focusNumber = random.choice(list)

    subNumberSecondUnitList = []
    subNumberSecondUnit1 = randomNumber()
    subNumberSecondUnitList.append(subNumberSecondUnit1)
    subNumberSecondUnit2 = removeDuplicateNumber(subNumberSecondUnitList)
    subNumberSecondUnit3 = removeDuplicateNumber(subNumberSecondUnitList)
    subNumberSecondUnit4 = removeDuplicateNumber(subNumberSecondUnitList)
    swapNumber = [str(subNumberSecondUnit1)+str(mainFirstNumber), str(subNumberSecondUnit2)+str(mainFirstNumber),
                  str(subNumberSecondUnit3)+str(mainFirstNumber), str(subNumberSecondUnit4)+str(mainFirstNumber)]

    subNumber2SecondUnitList = []
    # ตัดตัวเลขที่ซ้ำกันออกทั้งหมดก่อนที่จะไปเช็คกับคำในแถวแรก
    subNumber2SecondUnitList = []
    subNumber2SecondUnit1 = randomNumber()
    subNumber2SecondUnitList.append(subNumber2SecondUnit1)
    subNumber2SecondUnit2 = removeDuplicateNumber(subNumber2SecondUnitList)
    subNumber2SecondUnit3 = removeDuplicateNumber(subNumber2SecondUnitList)
    subNumber2SecondUnit4 = removeDuplicateNumber(subNumber2SecondUnitList)
    # เช็คซ้ำกับแถวที่ 1
    subNumber2SecondUnit1 = generateNumberForSecondLine(
        swapNumber, mainSecondNumber, subNumber2SecondUnit1)
    subNumber2SecondUnit2 = generateNumberForSecondLine(
        swapNumber, mainSecondNumber, subNumber2SecondUnit2)
    subNumber2SecondUnit3 = generateNumberForSecondLine(
        swapNumber, mainSecondNumber, subNumber2SecondUnit3)
    subNumber2SecondUnit4 = generateNumberForSecondLine(
        swapNumber, mainSecondNumber, subNumber2SecondUnit4)

    # Sort Number
    sortNumberSecondUnitList = [
        subNumberSecondUnit1, subNumberSecondUnit2, subNumberSecondUnit3, subNumberSecondUnit4]
    newSortedNumberSecondUnit = sorted(sortNumberSecondUnitList)
    sortNumber2SecondUnitList = [
        subNumber2SecondUnit1, subNumber2SecondUnit2, subNumber2SecondUnit3, subNumber2SecondUnit4]
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
