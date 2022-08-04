from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random
from datetime import datetime
import os

expireDate = "20220928"
expireDateThai = "27 กรกฎาคม 2565"
houseName = "permsub695"
houseNameThai = "เพิ่มทรัพย์ 695"


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
            return redirect('Home')
        else:
            request.session['error'] = 'ชื่อหรือรหัสผ่านไม่ถูกต้อง'
            return redirect('login')

    if 'error' in request.session:
        context['error'] = request.session['error']
        request.session['error'] = ''  # clear stuck error in session

    return render(request, 'login.html', context)

@login_required
def Home(request):
    context = {}
    resultCheckExpire = CheckExpireDate(request.user.id)
    if resultCheckExpire == "หมดเขตแล้ว":
        pass
    else:
        resultCheckExpire = ""
    context['houseName'] = houseName
    context['houseNameThai'] = houseNameThai
    context['expireDateThai'] = expireDateThai
    context['resultCheckExpire'] = resultCheckExpire

    return render(request, 'index.html', context)

@login_required
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
    month = profileObject.expire_date.strftime("%m")
    year = profileObject.expire_date.strftime("%Y")
    thaiMonth = ConvertToThaiMonth(month)
    expireDateThai = "{} {} {}".format(day, thaiMonth, year)

    context['houseName'] = houseName
    context['houseNameThai'] = houseNameThai
    context['expireDateThai'] = expireDateThai
    context['link'] = data.link
    context['imgLocation'] = imgLocation

    return render(request, 'result/index.html', context)

def AddData(request):
    pass
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
