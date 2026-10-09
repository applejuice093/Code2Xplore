sid=str(input("ID: "))
email=str(input("Email: "))
passwd=str(input("Password: "))
ref=str(input("Referral: "))
valid=True
#ID validation
# Expected format: CSE-ddd (7 chars). The combined check avoids the
# IndexError the old per-character indexing raised on short IDs.
if len(sid) != 7 or not sid.startswith("CSE-") or not sid[4:].isdigit():
    valid = False
#email validation
if (not email) or (email[0]=='@') or (email[0]=='.') or (email.count('@') == 0) or (email.count('.') == 0) or (email.count(' ') != 0) or (not email.endswith('.edu')):
    valid=False
#password validation: >= 8 chars, at least one digit, starts with an uppercase letter
count=( passwd.count('0') +passwd.count('1') + passwd.count('2') + passwd.count('3') + passwd.count('4') + passwd.count('5') + passwd.count('6') + passwd.count('7') +
       passwd.count('8') +passwd.count('9')
       )
if(len(passwd)<8) or (count<1) or (not passwd[0].isupper()):
    valid=False
#referral rules
# Referral: REF + two digits ... ending with '@'. Length guard prevents IndexError.
if len(ref) < 6 or (ref[:3]!="REF") or (not ref[3:5].isdigit()) or (not ref.endswith('@')):
    valid=False

if valid:
    print("APPROVED")
else:
    print("REJECTED")
