from django.shortcuts import render



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
