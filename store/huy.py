from django.contrib.auth import authenticate
user = authenticate(username='huy1', password='123123xx')
if user is not None:  #to check whether user is available or not?
    # the password verified for the user
    if user.is_active:   
        print("User is valid, active and authenticated")
    else:
        print("The password is valid, but the account has been disabled!")
else:
    # the authentication system was unable to verify the username and password
    print("The username and password were incorrect.")
