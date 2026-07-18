import os
import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# You can change this to any GitHub username
USERNAME = "srjofficial"

def fetch_contributions(username=USERNAME):
    url = f"https://github.com/users/{username}/contributions"
    print(f"Fetching contributions for {username} from {url}...")
    
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    days_data = []
    
    # Parse days
    tds = soup.find_all('td', class_='ContributionCalendar-day')
    for td in tds:
        date_str = td.get('data-date')
        if not date_str:
            continue
            
        level = int(td.get('data-level', 0))
        td_id = td.get('id')
        
        # Find tooltip to get exact count
        count = 0
        if td_id:
            tooltip = soup.find('tool-tip', {'for': td_id})
            if tooltip:
                text = tooltip.get_text(strip=True)
                match = re.match(r'^(\d+|No)\s+contribution', text)
                if match:
                    val = match.group(1)
                    count = 0 if val == "No" else int(val)
                    
        days_data.append({
            "date": date_str,
            "count": count,
            "level": level
        })
        
    if not days_data:
        print("No contribution data found. Is the username correct?")
        return
        
    # Sort just in case
    days_data.sort(key=lambda x: x["date"])
    
    # Calculate stats
    total_contributions = 0
    current_streak = 0
    longest_streak = 0
    best_day = {"date": None, "count": -1}
    monthly_totals = {}
    
    temp_streak = 0
    for day in days_data:
        count = day["count"]
        total_contributions += count
        
        if count > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0
            
        if count > best_day["count"]:
            best_day = {"date": day["date"], "count": count}
            
        month = day["date"][:7] # YYYY-MM
        monthly_totals[month] = monthly_totals.get(month, 0) + count
        
    # Calculate current streak based on today and yesterday
    temp_streak = 0
    for day in reversed(days_data):
        if day["count"] > 0:
            temp_streak += 1
        else:
            # We can allow today to be 0 and still keep the streak if yesterday had contributions
            if day == days_data[-1]:
                continue
            break
            
    current_streak = temp_streak
    
    stats = {
        "total_last_year": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "monthly_totals": monthly_totals
    }
    
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    
    output_data = {
        "username": username,
        "stats": stats,
        "days": days_data
    }
    
    out_path = os.path.join(output_dir, "contributions.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
        
    print(f"Saved contribution data to {out_path}")
    print(f"Total contributions: {total_contributions}")
    print(f"Longest streak: {longest_streak}")
    print(f"Best day: {best_day['count']} on {best_day['date']}")

if __name__ == "__main__":
    fetch_contributions()
