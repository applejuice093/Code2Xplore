admin="Aniket"
str=str(input("Enter Admin Name:"))
if str==admin:
    N = int(input("Enter number of Students:"))
    marks = [0] * N
    valid = 0
    fail = 0

    for i in range(N):
        marks[i] = int(input(f"Enter mark {i+1}:"))
    for mark in marks:
        if 90 <= mark <= 100:
            valid += 1
            print(mark, "-> Excellent")
        elif 75 <= mark <= 89:
            valid += 1
            print(mark, "-> Very Good")
        elif 60 <= mark <= 74:
            valid += 1
            print(mark, "-> Good")
        elif 40 <= mark <= 59:
            valid += 1
            print(mark, "-> Average")
        elif 0 <= mark <= 39:
            valid += 1
            fail += 1
            print(mark, "-> Fail")
        else:
            print(mark, "-> Invalid")

    print("Total Valid Students:", valid)
    print("Total Failed Students:", fail)
    print("Total Invalid Students:", N - valid)
else:
    print("Wrong Admin name")
