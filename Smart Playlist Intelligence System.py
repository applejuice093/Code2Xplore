count_text = input("Enter number of songs:").strip()
try:
    N = int(count_text)
except ValueError:
    raise SystemExit(f"Number of songs must be a whole number, got {count_text!r}.")
if N <= 0:
    raise SystemExit("Playlist must contain at least one song.")
playlist=[0]*N

valid=1
for i in range(N):
    entry=input(f"Enter Song {i+1} duration(in seconds):").strip()
    # Non-numeric durations are invalid, just like zero or negative ones.
    if not entry.isdigit() or int(entry)<=0:
        valid=0
        break
    playlist[i]=int(entry)

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
    