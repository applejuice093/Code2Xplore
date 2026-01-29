fullname=str(input("Full Name:"))
email=str(input("Email:"))
number=str(input("Mobile:"))
age=int(input("Age:"))

valid=True #boolean variable

splitname=fullname.split()
if (fullname[0]==" ") or (fullname[fullname.count("")-2]==" ") or (len(splitname)<=1): #fullname check
    valid=False
elif (email[0]=='@') or (email[0]=='.') or (email.count('@') == 0) or (email.count('.') == 0) or (email.count(' ') != 0):
    valid=False
elif (len(number)!=10) or (not number.isdigit()) or (number[0] =='0'):
    valid=False
elif (age<18) or (age > 60):
    valid=False


if valid:
    print("User Profile is VALID")
else:
    print("User Profile is INVALID")