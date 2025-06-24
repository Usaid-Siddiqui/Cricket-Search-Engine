import csv
import glob
import json
from collections import defaultdict

# Load people.csv: map name -> id and also lowercase lookup
name_to_id = {}
lower_name_to_name = {}
with open('Data/metadata/people.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['name']
        name_to_id[name] = row['identifier']
        lower_name_to_name[name.lower()] = name

# Step 1: Get user input (partial/full name)
search_name = input("Enter player name (partial or full): ").lower()

# Find all matching people.csv names
matching_names = [name for lname, name in lower_name_to_name.items() if search_name in lname]

if not matching_names:
    print("No matching player found in people.csv")
    exit()

print("Matching players:")
for i, name in enumerate(matching_names, 1):
    print(f"{i}. {name}")

# Step 2: User selects a name from people.csv
choice = input(f"Choose a number (1-{len(matching_names)}): ")
try:
    choice_idx = int(choice) - 1
    chosen_name = matching_names[choice_idx]
except (ValueError, IndexError):
    print("Invalid choice")
    exit()

player_id = name_to_id[chosen_name]

# Step 3: Scan JSONs once, collect short names for player_id and accumulate stats for those short names
folder = 'Data/tests_data/*.json'

short_names_for_player = set()
stats = defaultdict(lambda: {'runs':0, 'wickets':0, 'deliveries':0})

for filename in glob.glob(folder):
    with open(filename) as f:
        data = json.load(f)

        registry = data.get('info', {}).get('registry', {}).get('people', {})

        # Skip match if player's id not in registry values
        if player_id not in registry.values():
            continue

        for short_name, pid in registry.items():
            if pid == player_id:
                short_names_for_player.add(short_name)

        for inning in data['innings']:
            for over in inning['overs']:
                for delivery in over['deliveries']:
                    bowler = delivery['bowler']

                    if bowler not in short_names_for_player:
                        continue

                    runs = delivery['runs']['batter']
                    extras = delivery['runs']['extras']

                    if 'extras' in delivery:
                        if 'byes' in delivery['extras']:
                            extras -= delivery['extras']['byes']
                        if 'legbyes' in delivery['extras']:
                            extras -= delivery['extras']['legbyes']

                    # skip wides and no balls as legal deliveries
                    if 'extras' in delivery and ('wides' in delivery['extras'] or 'noballs' in delivery['extras']):
                        legal_delivery = False
                    else:
                        legal_delivery = True

                    stats_entry = stats[bowler]
                    stats_entry['runs'] += runs + extras
                    if legal_delivery:
                        stats_entry['deliveries'] += 1

                    if 'wickets' in delivery:
                        for w in delivery['wickets']:
                            if w['kind'] in {"bowled", "caught", "lbw", "stumped", "hit wicket", "caught and bowled"}:
                                stats_entry['wickets'] += 1

# Step 4: Combine stats for all short names belonging to player
total_runs = sum(s['runs'] for s in stats.values())
total_wickets = sum(s['wickets'] for s in stats.values())
total_deliveries = sum(s['deliveries'] for s in stats.values())

average = total_runs / total_wickets if total_wickets else 0
strike_rate = total_deliveries / total_wickets if total_wickets else 0

print(f"\nStats for {chosen_name} (including all short names):")
print(f"Wickets: {total_wickets}")
print(f"Average: {average:.2f}")
print(f"Strike rate: {strike_rate:.2f}")
