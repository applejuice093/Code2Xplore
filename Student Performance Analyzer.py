admin="Aniket"
name = input("Enter Admin Name:")
if name == admin:
    count_text = input("Enter number of Students:").strip()
    if not count_text.isdigit() or int(count_text) == 0:
        raise SystemExit("Number of students must be a whole number of at least 1.")
    N = int(count_text)
    marks = [0] * N
    valid = 0
    fail = 0

    for i in range(N):
        entry = input(f"Enter mark {i+1}:").strip()
        try:
            marks[i] = int(entry)
        except ValueError:
            marks[i] = entry  # non-numeric marks are reported as Invalid below
    for mark in marks:
        if not isinstance(mark, int):
            print(mark, "-> Invalid")
        elif 90 <= mark <= 100:
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
