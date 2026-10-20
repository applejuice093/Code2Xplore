sid=input("ID: ")
email=input("Email: ")
passwd=input("Password: ")
ref=input("Referral: ")
valid=True
#ID validation
# Expected format: CSE-ddd (7 chars). The combined check avoids the
# IndexError the old per-character indexing raised on short IDs.
if len(sid) != 7 or not sid.startswith("CSE-") or not sid[4:].isdigit():
    valid = False
#email validation
# Exactly one '@' with a non-empty name before it and a domain ending in .edu after it.
if (not email) or (email[0]=='@') or (email[0]=='.') or (email.count('@') != 1) or (email.count(' ') != 0) \
        or (not email.endswith('.edu')) or (email.split('@')[1] in ('', '.edu')) or email.split('@')[1].startswith('.'):
    valid=False
#password validation: >= 8 chars, at least one digit, starts with an uppercase letter
has_digit=any(ch in "0123456789" for ch in passwd)
if(len(passwd)<8) or (not has_digit) or (not passwd[0].isupper()):
    valid=False
#referral rules
# Referral: REF + two digits ... ending with '@'. Length guard prevents IndexError.
if len(ref) < 6 or (ref[:3]!="REF") or (not ref[3:5].isdigit()) or (not ref.endswith('@')):
    valid=False

if valid:
    print("APPROVED")
else:
    print("REJECTED")
