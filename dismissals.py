import glob
import csv
import json
import difflib
from collections import defaultdict

# Script to display the n most recent innings of a batter and the type of each dismissal, and how much they scored. Test format by default

print("This program is meant to recall the n most recent innings types of a batter.")
inputName = input("Enter name of batter: ")

# Reused logic from matchups.py. Probably best to update them later on and combine into a more modular function that may be reused
name_to_id = {}
lower_to_name = {}

with open('Data/metadata/people.csv', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        name_to_id[row['name']] = row['identifier']
        lower_to_name[row['name'].lower()] = row['name']


close = difflib.get_close_matches(inputName, lower_to_name.keys(), n=5, cutoff=0.5)    # Fuzzy lookup of possible matching player names

if not close:
    print(f"No matches for {inputName}")
    exit()

matches = [lower_to_name[c] for c in close]
for i, n in enumerate(matches, 1):
    print(f"{i}. {n}")

idx = int(input(f"Choose player (1-{len(matches)}): ")) - 1         # Let user select the correct player and store name, id
playerName = matches[idx]
playerID = name_to_id[playerName]
print(f"Selected Player: {playerName} (id {[playerID]})\n")



# Now time to look up last n innings

numInnings = input("Enter the number of innings you want to see (Ordered by most recent first)")

# Use the test readme to build a map of every test match filename and its date
# We can then go through those match files in reverse chronological order and find the players innings total IF they played

matches = []
innings_list = []       # Store data of each innings in the form (Date, Venue, Opponent, Runs, Deliveries, Out?, 4s, 6s, dismissalMethod, dismissalBowler)

with open('Data/test_data/README.txt') as f:
    for line in f:
        if '-' not in line: continue
        parts = line.strip().split(' - ')
        date, _, _, _, matchID = parts[:5]
        matches.append(date,matchID)

matches.sort(reverse=True)

for date, id in matches:
    try:
        with open(f'Data/tests_data/{id}.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        continue            # Skip missing files

    registry = data.get('info', {}).get('registry',{}).get('people', {})

    if playerID not in registry.values():
        continue
    else:
        batter_short_name = { s for s, pid in registry.items() if pid == playerID }


    # Now that we have confirmed whether the player played in this match, we just need to gather their batting stats and continue
