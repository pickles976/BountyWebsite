region_mappings = {
    "BASIN" : [0,3],
    "SPEAKING" : [-0.75,2.5], 
    "HOWL" : [0.75,2.5],
    "REACHING" : [-0,2],
    "CALLUMS" : [-1.5,2],
    "CLANSHEAD" : [1.5,2],
    "NEVISH" : [-2.25,1.5],
    "MOORS" : [-0.75,1.5],
    "VIPER" : [0.75,1.5],
    "MORGENS" : [2.25,1.5],
    "CALLAHANS" : [0,1], 
    "STONECRADLE": [-1.5,1], 
    "WEATHERED": [1.5,1], 
    "OARBREAKER": [-2.25,0.5],
    "LINN": [-0.75,0.5],
    "MARBAN": [0.75,0.5],
    "GODCROFTS": [2.25,0.5],
    "DEADLANDS" : [0,0],
    "FARRANAC": [-1.5,0], 
    "ENDLESS": [1.5,0], 
    "FISHERMANS": [-2.25,-0.5], 
    "LOCH": [-0.75,-0.5], 
    "DROWNED": [0.75,-0.5], 
    "TEMPEST": [2.25,-0.5],
    "UMBRAL" : [0,-1],
    "WESTGATE": [-1.5,-1], 
    "ALLODS": [1.5,-1], 
    "ORIGIN": [-2.25,-1.5], 
    "HEARTLANDS": [-0.75,-1.5], 
    "SHACKLED": [0.75,-1.5], 
    "FINGERS": [2.25,-1.5],
    "GREATMARCH" : [0,-2],
    "ASHFIELDS": [-1.5,-2], 
    "TERMINUS": [1.5,-2],
    "REDRIVER": [-0.75,-2.5], 
    "ACRITHIA": [0.75,-2.5],
    "KALOKAI": [0,-3],
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

k = 36.57
w = k * 2 / (3**0.5)
offset = [128,-128]

# returns Hex Names + coords for rendering on leaflet
def get_names_with_coords():

    new_dict = {}
    transformed = get_region_mappings()

    for k in transformed:
        name = region_names[k]
        coords = transformed[k] 

        new_dict[name] = coords

    return new_dict

# Transform the region offsets into coordinates
def get_region_mappings():

    new_dict = {}

    for key in region_mappings:
        x = offset[0] + region_mappings[key][0] * w 
        y = offset[1] + region_mappings[key][1] * k
        new_dict[key] = [y,x]

    return new_dict

# grid square to coordinate offset
def grid_to_coords(s):

    k2 = k/2
    w2 = w/2

    x = k2 - (ord(s[0].upper()) - 65) * (k/17)
    y = -w2 + int(s[1:]) * (w/15)

    return [x,y]

type_dict = {
    "LOGI" : 0,
    "DEMOLITION" : 1,
    "PARTISAN" : 2,
    "CONSTRUCTION" : 3,
    "COMBAT" : 4,
    "OTHER" : 5
}

# takes in a bounty type and bitmask, returns a boolean
# string, integer
def shouldSendNotif(type, mask):

    if type in type_dict:
        shift = type_dict[type]
        type_byte = 2**shift

        return 1 == ((type_byte & mask) >> (shift)) & 1
    return False

