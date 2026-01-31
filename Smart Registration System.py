sid=str(input("ID: "))
email=str(input("Email: "))
passwd=str(input("Password: "))
ref=str(input("Referral: "))
valid=True
#ID validation
if(len(sid)!=7)or(sid[0]!='C') or (sid[1]!='S') or (sid[2]!='E') or (sid[3]!='-') :
    valid= False
n=sid.count("")-2
if(not sid[n].isdigit()) or (not sid[n-1].isdigit()) or (not sid[n-2].isdigit()):
    valid=False
#email validation
lastindex=email.count("")-2
if (email[0]=='@') or (email[0]=='.') or (email.count('@') == 0) or (email.count('.') == 0) or (email.count(' ') != 0) or (email[lastindex]!='u') or (email[lastindex-1]!='d') or (email[lastindex-2]!='e') or (email[lastindex-3]!='.'):
    valid=False
#password vaalidation
count=( passwd.count('0') +passwd.count('1') + passwd.count('2') + passwd.count('3') + passwd.count('4') + passwd.count('5') + passwd.count('6') + passwd.count('7') +
       passwd.count('8') +passwd.count('9')
       )
if(len(passwd)<8) or (count<1) or ('Z' < passwd[0] < 'A'):
    valid=False
#referral rules
if (ref[:3]!="REF") or (not ref[3].isdigit()) or (not ref[4].isdigit()) or (ref[ref.count("")-2]!='@'):
    valid=False

if valid:
    print("APPROVED")
else:
    print("REJECTED")
