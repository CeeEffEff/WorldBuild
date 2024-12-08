# WorldBuild

## Custom Component Setup
WorldBuild requires a custom component for plotly dash to use. The necessary source is available in `/markdown_input_component`.

In order to install the requirements for WorldBuild we must first build the component to make available a `.tar.gz` distribution.

To build the component:
1. Enter the component project:
```
>>> cd markdown_input_component
```
2. Create and activate a venv:
```
>>> pyenv virtualenv markdown_input_component
>>> pyenv activate markdown_input_component
```
3. Install the dependencies required to build the component:
```
>>> pip install -r requirements.txt
```
4. Install Custom Component dependencies and Build Custom Component:
```
>>> npm install
>>> npm run build
```

## WorldBuild Setup
In the project root `.`.
1. Create and activate a venv:
```
>>> pyenv virtualenv worldbuild
>>> pyenv activate worldbuild
```
2. Install the dependencies required to build the component:
```
>>> pip install -r requirements.txt
```

## Running WorldBuild
In the project root `.`.
1. Create and activate a venv:
```
>>> python worldbuilder/manage.py runserver
```

## Writing TO-DO

### Factions
- [x] The Kemle Dynasty
- [ ] Farandor
- [ ] Sarsh of Kem
- [ ] Sarsh of Burnan
- [ ] Lordonites
- [ ] Followers of Nanook
- [ ] Giants

### NPCs
- [ ] Randolph Yvites
- [x] Uldolph Yvites
- [ ] Ulf Baran
- [ ] Kamul Hamal
- [ ] Leo Stormward
- [ ] Halbus
- [ ] The Black Oracle
- [ ] Governor at Bastion
- [ ] Coron Ra
- [ ] Governor at Giant's Keep



### POIs

- [ ] The New Cradle (aka Eoreland) (Continent)
    - [ ] Cetacea Lake (Region)
    - [ ] North Bastion (Region)
        - [ ] Followers of Nanook Camp (Minor Settlement)
    - [ ] Bastion (Fortified Settlement - Oppidum)
        - [ ] Rookery (Building)
    - [ ] Black Mountains (Region)
    - [ ] The Thorns (Region)
        - [ ] 
    - [ ] Giant's Keep (Fortress)
    - [ ]
    - [ ] Frontier Plains (Region)
        - [ ] Frontier Outpost (Fortified Outpost)
            - [ ] River source north (POI)
            - [ ] River source south (POI)
- [ ] Sea of Ahm'ti (Region)
    - [ ] 1st Potential Sighting of Burnanese ship (POI)
    - [ ] 2nd Potential Sighting of Burnanese ship (POI)
- [ ] Central Landing (Continent)
    - [ ] Ulrhoan (Region)
        - [ ] Sarsh of Kem (Nation)
        - [ ] Farandor (Nation)
            - [ ] Calfalan Port (Town)
                - [ ] - Ahm'ti's Cohort (Ship)
                - [ ] - Yviti's Hollow (Building)
        - [ ] Sarsh of Burnan (Nation)
    - [ ] Sand Sea of Baar (Region)
    - [ ] Kingdom of The Kemle Dynasty (Region)
- [ ] Sea of Suur (Region)


### POIs


## Dev TO-DO

- [ ] Bug. If I close a POI card I can't reopen it without clicking on different one first
- [ ] Edit POI mode
- [x] Make display POI scrollable
- [ ] Make map fill all space (card looks like it is taking up when hidden)
- [ ] Remove from map POI
- [ ] Make any POI addition show instantly on map
- [ ] Make any POI addition close the card


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