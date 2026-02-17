N=int(input("Enter number of items:"))
weight=[0.00]*N
very_light=[0.00]*N
vlcount=0
normal_load=[0.00]*N
nlcount=0
Heavy_load=[0.00]*N
hlcount=0
overload=[0.00]*N
olcount=0
Invalid_entries=[0.00]*N
IEcount=0
for i in range(N):
    weight[i]=int(input(f"Enter weight{i+1}:"))
for i in range(N):
    if weight[i]<0:
        Invalid_entries[IEcount]=weight[i]
        IEcount+=1
    elif 0 <= weight[i] <= 5:
        very_light[vlcount]=weight[i]
        vlcount+=1
    elif 6 <= weight[i] <= 25:
        normal_load[nlcount]=weight[i]
        nlcount+=1
    elif 26 <= weight[i] <= 60:
        Heavy_load[hlcount]=weight[i]
        hlcount+=1
    else:
        overload[olcount]=weight[i]
        olcount+=1

validWt=vlcount+nlcount+hlcount+olcount
print(weight)
print("Number of Valid Items",validWt)
print("Very light:",very_light[:vlcount])
print("Normal load:",normal_load[:nlcount])
print("Heavy load:",Heavy_load[:hlcount])
print("Overload:",overload[:olcount])
print("Invalid Entries:",Invalid_entries[:IEcount])



print("\n--Personalization Rule applied--")
name="Aniket Mahto"
name_length=0
for ch in name:
    if ch != " ":
        name_length += 1
PLI=name_length%3
affected_items=0
print(f"Name:{name} PLI={PLI} ")
if(PLI==0):
    print("RULE A")
    for i in range(olcount):
        Invalid_entries[IEcount]=overload[i]
        IEcount+=1
        affected_items=olcount
    olcount=0
elif(PLI==1):
    print("Rule B")
    affected_items=vlcount
    vlcount=0
elif(PLI==2):
    print("Rule C")
    affected_items=vlcount+olcount+IEcount
    vlcount=0
    olcount=0
    IEcount=0

validWt=vlcount+nlcount+hlcount+olcount
print("Very light:",very_light[:vlcount])
print("Normal load:",normal_load[:nlcount])
print("Heavy load:",Heavy_load[:hlcount])
print("Overload:",overload[:olcount])
print("Invalid Entries:",Invalid_entries[:IEcount])

print("Number of Valid Items",validWt)
print("Number of PLI affected Items:",affected_items)