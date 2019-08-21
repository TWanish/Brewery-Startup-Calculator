# Brewery Value

This project is a work to try to determine the best zip codes in America to open a brewery using brewery data from the brewer’s association as well as census data. In an effort to take a more advance approach to calculating this value, two models were used. One that encourages brewery tourism to a point using a logistic carrying capacity equation, and one that assumes all competition is bad competition. There are some short comings with the current model - legal hurdles are not represented, nor is local drinking habits. It may be overgeneralized and the carrying capacity equation could probably use some work once a source for more granular drinking habits is found. It also doesn’t take into account numbers of local bars and liquor stores - though there may be a benefit of not over-constraining the model with that.

# Next Actions

- Implement addition of more granular drinking data
- Develop a more accurate spending power model/account for CoL with spending power in total market cap value (potentially normalize market cap)
- Generate a website where a use can enter certain filters and get a result for the best places to open a brewery. E.g. “I want a zip code with less than 50000 people but more than 10000 in the PNW with a fairly young population. I would like there to be some existing breweries but still plenty of space for me to carve my own niche in the industry. I would like this town to have relatively high income and don’t care about the cost of living”

Maybes:
- Find a way to integrate legal hurdles as a metric
- Integrate counts of bars/liquor stores
- Integrate tourism data as a factor

# Publications

A brief, early write up of the first portion of this project can be found at:
https://www.reddit.com/r/Homebrewing/comments/bqhz16/a_shallow_unfinished_look_at_the_best_places_in/

# Miscellaneous

If anyone wants to get involved on this project and help with some of the modeling feel free to shoot me a message or make a comment. I’m also open to ways to expand the scope of this model.
