import csv                              # Parse through csv
import glob                             # Navigate/Open different files
import json                             # Parse through json
from collections import defaultdict     # Create direct to key entry dictionaries
import difflib                          # Used in fuzzy search


batterName = input("Enter batter name (partial or full): ").lower()
bowlerName = input("Enter bowler name (partial or full): ").lower()

name_to_id = {}
lower_to_name = {}

with open('metadata/people.csv', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        name_to_id[row['name']] = row['identifier']
        lower_to_name[row['name'].lower()] = row['name']

# Players to match: [(input, label), ...]
players = [(batterName, "batter"), (bowlerName, "bowler")]
chosen_names = []
chosen_ids = []

for search, role in players:
    close = difflib.get_close_matches(search, lower_to_name.keys(), n=5, cutoff=0.5)
    if not close:
        print(f"No matches for {role}")
        exit()
    matches = [lower_to_name[c] for c in close]
    for i, n in enumerate(matches, 1):
        print(f"{i}. {n}")
    idx = int(input(f"Choose {role} (1-{len(matches)}): ")) - 1
    chosen = matches[idx]
    chosen_names.append(chosen)
    chosen_ids.append(name_to_id[chosen])
    print(f"{role.capitalize()}: {chosen} (id {name_to_id[chosen]})")

# Now we have the data for both players stored in chosen_names and chosen_ids
# chosen_names[0] and chosen_ids[0] are for the batter, and [1] for the bowler

# Use this information to loop through the json files and find head to head matchups

batter = chosen_names[0]
bowler = chosen_names[1]

batterID = chosen_ids[0]
bowlerID = chosen_ids[1]

# Note: only legal deliveries are counted
# Stat variables:
runs = 0
wickets = 0
deliveries = 0
fours = 0
sixes = 0
bowleds = 0
lbws = 0
caughts = 0
cnbs = 0
stumpeds = 0
extras = 0
hitwickets = 0

folder = 'tests_data/*.json'

for filename in glob.glob(folder):
    with open(filename) as f:
        data=json.load(f)

        # Check if match involves batter and bowler. If not, simply skip it to preserve efficiency
        registry = data.get('info', {}).get('registry', {}).get('people', {})
        if batterID not in registry.values() or bowlerID not in registry.values():
            continue
        
        # Update bowler and batter name to the short forms
        for shortname, pid in registry.items():
            if pid == batterID:
                batterName = shortname
            elif pid == bowlerID:
                bowlerName = shortname
        
        for inning in data['innings']:
            for over in inning['overs']:
                for delivery in over['deliveries']:
                    if delivery['bowler'] != bowlerName:
                        continue
                    if delivery['batter'] != batterName:
                        continue

                    runs += delivery['runs']['batter']
                    extras += delivery['runs']['extras']

                    # ensure byes are not counted for either bowler's stats (for extras)
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

                    if legal_delivery:
                        deliveries += 1

                    if 'wickets' in delivery:
                        for w in delivery['wickets']:
                            if w['kind'] in {"bowled", "caught", "lbw", "stumped", "hit wicket", "caught and bowled"}:
                                wickets += 1

                                if w['kind'] == 'bowled':
                                    bowleds += 1
                                if w['kind'] == 'caught':
                                    caughts += 1
                                if w['kind'] == 'lbw':
                                    lbws += 1
                                if w['kind'] == 'caught and bowled':
                                    cnbs += 1
                                if w['kind'] == 'stumped':
                                    stumpeds += 1
                                if w['kind'] == 'hit wicket':
                                    hitwickets += 1
                                
                    if delivery['runs']['batter'] == 4:
                        fours += 1
                    if delivery['runs']['batter'] == 6:
                        sixes += 1


# Finally, now combine and return finalized stats

average = runs/wickets if wickets else runs
balls_per_dismissal = deliveries/wickets if wickets else 0

print(f"Stats for {batterName} against {bowlerName} in head to head matchups:\n")
print(f"Wickets: {wickets}")
print(f"Runs: {runs}")
print(f"Extras: {extras}")
print(f"4s: {fours}")
print(f"6s: {sixes}")

print(f"\nBalls per Dismissal: {balls_per_dismissal}")
print(f"Average: {average}\n")

print("\nBreakdown by type of dismissal:")
print(f"Bowled: {bowleds}")
print(f"Caught: {caughts}")
print(f"Stumped: {stumpeds}")
print(f"Caught and Bowled: {cnbs}")
print(f"Hit Wicket: {hitwickets}")


