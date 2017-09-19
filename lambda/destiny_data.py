#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, json, time
from config import JSONDATAFILE

class Milestone(object):
    
    def __init__(self, **entries):
        self.__dict__.update(entries)

class LocalizedMilestones(object):
    
    def __init__(self, **entries):
        self.milestones = {}
        for key in entries:
            self.milestones[key] = Milestone(**entries[key])
            
    def has_milestone(self,name):
        return self.milestones.has_key(name)
    
    def get_milestone(self,name):
        if self.has_milestone(name):
            return self.milestones[name]
        else:
            return None   
            
class Milestones(object):
    
    def __init__(self, **entries):
        self.__dict__.update(entries)
        
        self.de = LocalizedMilestones(**entries["de"])
        self.en = LocalizedMilestones(**entries["en"])

def slot_value_to_data_key(slot_value):
    slot_value =  slot_value.upper()
    
    if slot_value in ["NIGHTFALL","NIGHTFALL STRIKE","DÄMMERUNG","DÄMMERUNGS STRIKE","DÄMMERUNGS STRICK","STRICK","DÄMMERUNG STRICK"]:
        return "Nightfall"
    elif slot_value in ["FLASHPOINT","FLASHPOINT PLANET"]:
        return "Hotspot"
    elif slot_value in ["CALL TO ARMS","ZU DEN WAFFEN"]:
        return "CallToArms"
    elif slot_value in ["WEEKLY CLAN OBJECTIVES","CLAN OBJECTIVES","WÖCHENTLICHE CLAN ZIELE","CLAN ZIELE", "KLANZIELE"]:
        return "ClanObjectives"
    elif slot_value in ["MEDITATIONS","MEDITATIONEN"]:
        return "Meditations"
    elif slot_value in ["RAID","REAL","RATE"]:
        return "Raid"
    elif slot_value in ["SOLL","ZUR","XUR","AGENT OF THE NINE","AGENT DER NEUN","AGENT DER 9"]:
        return "XUR"
    else:
        return None
     
def load_current_milestones():
    milestone_json = json.loads(urllib.urlopen(JSONDATAFILE + "?v=" + str(time.time()).split('.')[0]).read())
    return Milestones(**milestone_json)

def load_current_milestones_with_locale(locale):
    locale = locale.split("-")[0]
    milestones = load_current_milestones()
    
    if locale == "de":
        return milestones.de
    else:
        return milestones.en

        
    