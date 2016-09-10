#!/usr/bin/env python
import constants
import time
import requests

state = 2
old_state = 2

def what_lights():
    response = requests.get(constants.url, headers=constants.headers)
    sessions = response.json()
    children = sessions["_children"]
    for child in children:
        if child['_elementType'] == 'Video':
            subchildren = child['_children']
            for subchild in subchildren:
                if child['librarySectionID'] in constants.movie_lib_ids and subchild["_elementType"] =="Player" and subchild["machineIdentifier"] == constants.player_id:
                    if subchild['state'] == 'playing' and child['type'] in constants.half_lights:
                        return 1
                    if subchild['state'] == 'paused' and child['type'] in constants.no_lights:
                        return 3
                    elif subchild['state'] == 'playing' and child['type'] in constants.no_lights:
                        return 0
                    else:
                        return 2
    return 2

def set_lights(state):
    requests.get(constants.openhab_url + 'Scene=' + str(state))

while True:
    try:
        new_state = what_lights()
        if new_state == state != old_state:
           if new_state == 2:
                print 'regular lights'
                set_lights(1)
        elif new_state != state:
            if new_state == 0:
                if state == 3:
                    print 'back to movie'
                    for action in back_to_movie_actions:
                        requests.get(constants.openhab_url + action)
                else:
                    print 'movie lights'
                    set_lights(2)
            elif new_state == 1:
                print 'half lights'
                set_lights(5)
            elif new_state == 3:
                print 'pause lights'
                for action in pause_lights_actions:
                    requests.get(constants.openhab_url + action)
 
    except:
        print 'Error'
    old_state = state
    state = new_state
    time.sleep(0.5)
