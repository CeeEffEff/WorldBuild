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

## TO-DO

- [x] Bug. If I close a POI card I can't reopen it without clicking on different one first
    Reason to me seems to be that the value of the click data has not changed when I click elsewhere - if I can clear clickdata then it would work
- [ ] Add "Edit POI" mode
- [ ] Add "Delete POI" mode
- [ ] Add drag "POI" mode
- [ ] Make POI Trace visible in legend so can be hidden
- [x] Make display POI scrollable
- [ ] Make map fill all space (card looks like it is taking up when hidden)
- [ ] Remove from map POI
- [x] Make any POI addition show instantly on map
- [ ] Make any POI addition close the card
- [ ] Create POI form required fields not alerting
- [ ] POI Card - some parts are out of the bounds


## Models
Description of models and how they are connected.

### Maps
Maps are images that map a given area at a given scale.
A description is usually fitting to help describe generally the map.

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