n=int(input("Enter number of buildings:"))

e_usage= [int(input()) for _ in range(n)]

inv_count=0
eff_count=0
mod_count=0
high_count=0

max_e=max(e_usage)
min_e=min(e_usage)
avg_e= sum(e_usage) / len(e_usage)


categorized={
    "efficient": [],
    "moderate":[],
    "high":[],
    "invalid":[]
}   
total=0

for i in range(n):
    if(e_usage[i]<0): 
        categorized["invalid"] = categorized["invalid"] + [e_usage[i]]
        inv_count+=1
    elif(0<=e_usage[i]<=50): 
        categorized["efficient"] = categorized["efficient"] + [e_usage[i]]
        eff_count+=1
    elif(51<=e_usage[i]<=150): 
        categorized["moderate"] = categorized["moderate"] + [e_usage[i]]
        mod_count+=1
    else: 
        categorized["high"] = categorized["high"] + [e_usage[i]]
        high_count+=1
    total +=e_usage[i]

usage=""
if(high_count>3): usage="Overconsumption"
elif(abs(mod_count-eff_count)<=2): usage="Balanced Usage"
elif(total>600): usage="Energy waste"
else: usage="Normal usage"

summary = (("Category:", categorized), ("Total", total), ("Number of buildings:", n), ("Usage:", usage))

for i in range(len(summary)):
    print(summary[i])

print("Maximum Usage:",max_e)
print("Minimum Usage:",min_e)
print("Avg Usage:",avg_e)