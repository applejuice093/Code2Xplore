N= int(input("Enter number of songs:"))
playlist=[0]*N

valid=1
for i in range(N):
    playlist[i]=int(input(f"Enter Song {i+1} duration(in seconds):"))
    if(playlist[i]<=0):
        valid=0
        break

if(valid):
    total_duration=0
    repeat=0
    duration_deviation=1
    category=""
    recommendation=""
    playlist.sort()
    for i in range(N):
        total_duration +=playlist[i]
    for i in range(N-1):
        if(playlist[i]==playlist[i+1]):
            repeat=1
        if(abs(playlist[i]-playlist[i+1])<10):
            duration_deviation=0


    if(total_duration<300) and not repeat:
        category="Too Short Playlist"
        recommendation="Add more songs"
    elif(total_duration>3600 and not repeat):
        category="Too Long Playlist"
        recommendation="Too long, better remove some Songs"
    elif(repeat):
        category="Repetitive Playlist"
        recommendation="Add variation in playlist"
    elif(duration_deviation):
        category="Balanced Playlist"
        recommendation="Good listening session"
    else:
        category="Irregular Playlist"
        recommendation="Unique Taste"
    
    print("Total Duration:",total_duration)
    print("Number of songs:",N)
    print("Detected category:",category)
    print("Recommendation:",recommendation)

else:
    print("Invalid Song duration")
    