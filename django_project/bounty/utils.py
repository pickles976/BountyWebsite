# TOP-CENTER of BASIN is 0, 128
# hexes are 33.16 WIDTH, 36.56 HEIGHT

# TODO: Find a better way of calculating all this than by hand :/
# just use offsets and height/width

# FIX THESE OFFSETS

region_mappings = {
    "BASIN" : [-18.28,128],
    "SPEAKING" : [-36.56,94.72], 
    "HOWL" : [-36.56,161],
    "REACHING" : [-54.84,128],
    "CALLUMS" : [-54.84,61.56],
    "CLANSHEAD" : [-54.84,194.2],
    "NEVISH" : [-73.12,28.4],
    "MOORS" : [-73.12,94.72],
    "VIPER" : [-73.12,161],
    "MORGENS" : [-73.12,227.3],
    "CALLAHANS" : [-91.4,128], 
    "STONECRADLE": [-91.4,61.56], 
    "WEATHERED": [-91.4,194.2], 
    "OARBREAKER": [-109.68,28.4],
    "LINN": [-109.68,94.72],
    "MARBAN": [-109.68,161],
    "GODCROFTS": [-109.68,227.3],
    "DEADLANDS" : [-127.96,128],
    "FARRANAC": [-127.96,61.56], 
    "ENDLESS": [-127.96,194.2], 
    "FISHERMANS": [-146.24,28.4], 
    "LOCH": [-146.24,94.72], 
    "DROWNED": [-146.24,161], 
    "TEMPEST": [-146.24,227.3],
    "UMBRAL" : [-164.52,128],
    "WESTGATE": [-164.52,61.56], 
    "ALLODS": [-164.52,194.2], 
    "ORIGIN": [-182.8,28.4], 
    "HEARTLANDS": [-182.8,94.72], 
    "SHACKLED": [-182.8,161], 
    "FINGERS": [-182.8,227.3],
    "GREATMARCH" : [-201.08,128],
    "ASHFIELDS": [-201.08,61.56], 
    "TERMINUS": [-201.08,194.2],
    "REDRIVER": [-219.36,94.72], 
    "ACRITHIA": [-219.36,161],
    "KALOKAI": [-237.64,128],
}

region_names = {
    "BASIN" : "Basin Sionnach",
    "SPEAKING" : "Speaking Woods", 
    "HOWL" : "Howl County",
    "REACHING" : "Reaching Trail",
    "CALLUMS" : "Callums Cape",
    "CLANSHEAD" : "Clanshead Valley",
    "NEVISH" : "Nevish Line",
    "MOORS" : "The Moors",
    "VIPER" : "Viper Pit",
    "MORGENS" : "Morgens Crossing",
    "CALLAHANS" : "Callahans Passage", 
    "STONECRADLE": "Stonecradle", 
    "WEATHERED": "Weathered Expanse", 
    "OARBREAKER": "The Oarbreaker Isles",
    "LINN": "The Linn of Mercy",
    "MARBAN": "Marban Hollow",
    "GODCROFTS": "Godcrofts",
    "DEADLANDS" : "Deadlands",
    "FARRANAC": "Farranac Coast", 
    "ENDLESS": "Endless Shore", 
    "FISHERMANS": "Fishermans Row", 
    "LOCH": "Loch Mor", 
    "DROWNED": "The Drowned Vale", 
    "TEMPEST": "Tempest Island",
    "UMBRAL" : "Umbral Wildwood",
    "WESTGATE": "Westgate", 
    "ALLODS": "Allods Bight", 
    "ORIGIN": "Origin", 
    "HEARTLANDS": "The Heartlands", 
    "SHACKLED": "Schackled Chasm", 
    "FINGERS": "The Fingers",
    "GREATMARCH" : "Great March",
    "ASHFIELDS": "Ash Fields", 
    "TERMINUS": "Terminus",
    "REDRIVER": "Red River", 
    "ACRITHIA": "Acrithia",
    "KALOKAI": "Kalokai",
}

def get_names_with_coords():

    new_dict = {}

    for k in region_mappings:
        name = region_names[k]
        coords = region_mappings[k] 

        new_dict[name] = coords

    return new_dict