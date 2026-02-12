admin="Aniket"
user=str(input("Enter Username:"))
if admin==user:
    N=int(input("Enter Number of elements:"))
    combine_list=[""]*N
    number_list=[""]*N
    string_list=[""]*N

    for i in range(N):
        combine_list[i]=str(input(f"List Element {i+1}:"))
    print("Combined List:",combine_list)
    numbersCount=0
    stringCount=0
    for ele in combine_list:
        if (ele.isdigit()):
            number_list[numbersCount]=int(ele)
            numbersCount+=1
        elif (ele=="") or (ele==" "):
            continue
        else:
            string_list[stringCount]=ele
            stringCount+=1

    print("Numbers List:", number_list[:numbersCount])
    print("Strings List:", string_list[:stringCount])

    print("Total Numbers:",numbersCount)
    print("Total Strings",stringCount)

    print("After Personalization:")

    if (N%2==0):
        print("First element is removed")
        print("Numbers List:", number_list[1:numbersCount])
        print("Strings List:", string_list[1:stringCount])
    else:
        print("Last element is removed")
        print("Numbers List:", number_list[:numbersCount-1])
        print("Strings List:", string_list[:stringCount-1])
else:
    print("Wrong Username.")

