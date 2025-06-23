
# Cricket Stats Engine

**This project is powered by [CricSheet](https://cricsheet.org/), where all the match data and player registry is sourced.**

## About

This project is essentially a custom crickets stat engine I made using python and publicly available data sourced from cricsheet

Contained are several .py programs for looking up various cricket stats and advanced metrics. The most commonly available online tool for this purpose is Statsguru by Cricinfo, which is based off of their own private database and covers a broad range of surface level stats. 

However, the engine is limited in a few ways

1. The database is private. Meaning access is restricted and there is no way for a user to run their own queries or double check results

2. Functionality is limited. From broad use cases such as player head to head matchups to niche queries like consecutive ball wickets, the engine is not prepared to handle them and most users as dedicated as I would prefer something more pliable.

3. Data for non men's international matches is patchy and missing. When using an open source database, we have access to data from many more leagues as well as domestic tournaments, and can reuse the same functions for all sorts of matches

## How to Run the programs

There are multiple scripts I've written to pursue various curious endeavors regarding international or league match data. However, probably the most useful out of these is the one that includes head to head matchup functionality between a bowler and a specified batter. 

While this functionality is available on certain sites such as CricMetric, its limited only to international matches and doesn't include additional figures such as boundaries, extras, and types of dismissal.

Overall I see this 'program' and the associated scripts as a general guideling and building block on how to parse through the database. Anyone mildly interested in the topic can hopefully use it as is, but those wanting to dive deeper into the functionality can edit and write their own modifications to the scripts for more advanced queries.

## Next Steps

I'd like to increase functionality by eventually including a UI and turning this into a downloadable application. The difficult part being how to integrate various functions and filters of different types, but that is a challenge for another day.

I've also looked into some other python libraries such as MatPlotLib into creating nice visuals and graphs to represent this data. That functionality will hopefully be added soon.


## Author

If you have any problems feel free to reach out to me at my email usaidsidiqui@gmail.com

Otherwise my information can also be found on a seperate readme posted on my profile, including my [LinkedIn](https://linkedin.com/in/usaidsiddiqui1).

