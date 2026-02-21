N= int(input("Enter number of songs:"))
playlist=[0]*N

valid=1
for i in range(N):
    playlist[i]=int(input(f"Enter Song {i+1} dutation(in seconds):"))
    if(playlist[i]<=0):
        valid=0
        break

if(valid):
    total_duration=0
    repeat=0
    duration_deviation=1
    category=""
    recommedation=""
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
        recommedation="Add more songs"
    elif(total_duration>3600 and not repeat):
        category="Too Long Playlist"
        recommedation="Too long, better remove some Songs"
    elif(repeat):
        category="Repetitive Playlist"
        recommedation="Add variotion in playlist"
    elif(duration_deviation):
        category="Balanced Playlist"
        recommedation="Good Listing session"
    else:
        category="Irregular Playlist"
        recommedation="Unique Taste"
    
    print("Total Duration:",total_duration)
    print("Number of songs:",N)
    print("Detected category:",category)
    print("Recommedation:",recommedation)

else:
    print("Invalid Song duration")
    