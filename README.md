# WorldBuild


## Models
Description of models and how they are connected.

### Maps
Maps are at heart images mapping a given area at a given scale.
A descrption is usually fitting to help describe generally the map.

Maps of one scale can be linked to a parent map of a scale one greater than itself.

Map scales, smallest to largest, are as follows:
- Encounter
- Settlement
- Province
- Kingdom
- Continent

Most maps are likely to have points of interest.

### Point of Interest
A point of interest is anything that players could feasibly stumble across on a given map.
Some points of interest will have their own maps, for example Encounters and Settlements.

A point of interest can exist on multiple maps if the maps are of differing scales.
Points of interest will have coordinates for each map they exist on.

### 