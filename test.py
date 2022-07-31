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