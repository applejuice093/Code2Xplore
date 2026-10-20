fullname=str(input("Full Name:"))
email=str(input("Email:"))
number=str(input("Mobile:"))
age_text=input("Age:").strip()
# A non-numeric age makes the profile invalid instead of crashing int().
age=int(age_text) if age_text.isdigit() else -1

valid=True #boolean variable

splitname=fullname.split()
if (not fullname) or (fullname != fullname.strip()) or (len(splitname)<=1): #fullname check
    valid=False
elif (not email) or (email[0]=='@') or (email[0]=='.') or (email.count('@') != 1) or (email.count(' ') != 0) \
        or ('.' not in email.split('@')[1]) or email.split('@')[1].startswith('.') or email.endswith('.'):
    # Exactly one '@', and the domain after it must contain a dot that is not at its edges.
    valid=False
elif (len(number)!=10) or (not number.isdigit()) or (number[0] =='0'):
    valid=False
elif (age<18) or (age > 60):
    valid=False


if valid:
    print("User Profile is VALID")
else:
    print("User Profile is INVALID")