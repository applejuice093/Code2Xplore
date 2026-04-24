import random
import math
import pandas as pd
import numpy as np

def generate_city_data(num_zones=15):
    data = []
    
    for i in range(1, num_zones + 1):
        data.append({
            "zone": i,
            "traffic": random.randint(0, 100),
            "air_quality": random.randint(0, 300),
            "energy": random.randint(0, 500)
        })
        
    return data

def classify_zones(data):
    categories = {
        "High Risk": set(),
        "Energy Critical": set(),
        "Safe Zone": set(),
        "Unclassified": set()
    }
    
    for item in data:
        z = item["zone"]
        t = item["traffic"]
        a = item["air_quality"]
        e = item["energy"]
        
        classified = False
        
        if a > 200 or t > 80:
            categories["High Risk"].add(z)
            classified = True
            if e > 400: 
                categories["Energy Critical"].add(z)
        elif e > 400:
            categories["Energy Critical"].add(z)
            classified = True
            
        if t < 30 and a < 100:
            categories["Safe Zone"].add(z)
            classified = True
            
        if not classified:
            categories["Unclassified"].add(z)
            
    return categories

def apply_personalized_rule(data, roll_num):
    if roll_num % 3 == 0:
        print(f"My roll number {roll_num} is divisible by 3, so I will just shuffle the data.\n")
        random.shuffle(data)
    else:
        print(f"My roll number {roll_num} isn't divisible by 3. Doing a custom bubble sort by traffic...\n")
        n = len(data)
        for i in range(n):
            for j in range(0, n-i-1):
                if data[j]['traffic'] > data[j+1]['traffic']:
                    data[j], data[j+1] = data[j+1], data[j]
    return data

def analyze_and_detect_patterns(df):
    numeric_matrix = df[['traffic', 'air_quality', 'energy']].to_numpy()
    means = np.mean(numeric_matrix, axis=0)
    
    print("Matrix averages:")
    print(f"Traffic: {means[0]:.2f}, AQI: {means[1]:.2f}, Energy: {means[2]:.2f}\n")

    df['raw_risk'] = (df['traffic'] * 0.4) + (df['air_quality'] * 0.4) + (df['energy'] * 0.2)
    df['risk_score'] = df['raw_risk'].apply(lambda x: math.sqrt(x))
    
    max_risk = df['risk_score'].max()
    avg_risk = df['risk_score'].mean()
    min_risk = df['risk_score'].min()
    risk_stats = (round(max_risk, 2), round(avg_risk, 2), round(min_risk, 2))
    
    risk_list = df[['zone', 'risk_score']].to_dict('records')

    for i in range(len(risk_list)):
        max_idx = i
        for j in range(i+1, len(risk_list)):
            if risk_list[j]['risk_score'] > risk_list[max_idx]['risk_score']:
                max_idx = j
        risk_list[i], risk_list[max_idx] = risk_list[max_idx], risk_list[i]
        
    top_3_zones = [z['zone'] for z in risk_list[:3]]

    df['aqi_rising'] = df['air_quality'].diff() > 0
    multi_factor_zones = df[(df['risk_score'] > avg_risk) & (df['aqi_rising'] == True)]['zone'].tolist()
    
    traffic_variance = np.var(df['traffic'])
    
    df['is_high_risk'] = (df['air_quality'] > 200) | (df['traffic'] > 80)
    clusters = []
    for i in range(1, len(df)):
        if df.loc[i, 'is_high_risk'] and df.loc[i-1, 'is_high_risk']:
            clusters.append((df.loc[i-1, 'zone'], df.loc[i, 'zone']))

    decision = "City Stable"
    if max_risk > 13 and avg_risk > 10:
        decision = "Critical Emergency"
    elif len(clusters) > 0 or max_risk > 11:
        decision = "High Alert"
    elif avg_risk > 8:
        decision = "Moderate Risk"

    print("First few rows of the final dataframe:")
    print(df[['zone', 'traffic', 'air_quality', 'energy', 'risk_score']].head(), "\n")
    
    print(f"Top 3 most dangerous zones: {top_3_zones}\n")
    
    print("Pattern Detection Results:")
    print(f"Zones with high risk and rising AQI: {multi_factor_zones}")
    print(f"Traffic variance: {traffic_variance:.2f}")
    print(f"Consecutive high-risk clusters found: {clusters}\n")
    
    print(f"Risk stats (Max, Avg, Min): {risk_stats}\n")
    
    print(f"System Decision: {decision.upper()}\n")

    return decision

if __name__ == "__main__":
    MY_ROLL_NUMBER = 11620
    print(f"Student: Satish | Roll No: {MY_ROLL_NUMBER}\n")
    
    raw_data = generate_city_data(17) 
    
    zone_categories = classify_zones(raw_data)
    print("Categorized Zones:")
    for category, zones in zone_categories.items():
        print(f"{category}: {list(zones) if zones else 'None'}")
    print("\n")
    
    processed_data = apply_personalized_rule(raw_data, MY_ROLL_NUMBER)
    
    city_df = pd.DataFrame(processed_data)
    
    analyze_and_detect_patterns(city_df)
    
    print("--------------------------------------------------")
    print("My Insight: What makes a Smart City?")
    print("--------------------------------------------------")
    print("I believe a smart city isn't just about collecting tons of data from sensors. "
          "It's about how the city uses that data to find multiple problems happening at "
          "the same time—like bad traffic causing terrible air quality—and fixing them "
          "automatically before they turn into a real disaster for the people living there.")