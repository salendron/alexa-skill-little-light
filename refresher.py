#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import API_HEADERS, DB_PATH, DOWNLOAD_PATH
import requests, urllib, zipfile, os, sqlite3, json
from gs import xamoom_storage,xamoom_acl

def twos_comp_32(val):
    val = int(val)
    if (val & (1 << (32 - 1))) != 0:
        val = val - (1 << 32)
    return val

def get_manifest():
    r = requests.get("https://bungie.net/Platform/Destiny2/Manifest/", headers=API_HEADERS)
    return r.json()["Response"]

def get_milestones():
    r = requests.get("https://bungie.net/Platform/Destiny2/Milestones/", headers=API_HEADERS)
    return r.json()["Response"]

def get_milestone_content(milestonehash):
    r = requests.get("https://bungie.net/Platform/Destiny2/Milestones/" + milestonehash + "/Content/", headers=API_HEADERS)
    return r.json()

def downloadDBFile(manifest,lang):
    file_name = DOWNLOAD_PATH + lang + "_world.zip"
    
    url = "https://www.bungie.net" + manifest["mobileWorldContentPaths"][lang]
    testfile = urllib.URLopener()
    testfile.retrieve(url, file_name)
    
    return file_name

def cleanup():
    directories = [DB_PATH, DOWNLOAD_PATH]
    
    for directory in directories:
        filelist = [ f for f in os.listdir(directory) ]
        for f in filelist:
            os.remove(directory + f)

def unzip(file_name):
    with zipfile.ZipFile(file_name,"r") as zip_ref:
        zip_ref.extractall(DB_PATH)
        
def getDBPath():
    filelist = [ f for f in os.listdir(DB_PATH) ]
    for f in filelist:
        return DB_PATH + f
        
def queryDBForItem(db_path, table, id):
    id = twos_comp_32(id)
    conn = sqlite3.connect(db_path)
    stmt = "SELECT json FROM " + table + " WHERE id=" + str(id)
    
    rows = conn.execute(stmt)
    for row in rows:
        return row[0]
        
### PARSE MILESTONES
def generate_milestone(ms_json):
    print ms_json["milestoneHash"]

def search_for_keyword(KeyWord):
    tables_stmt = "SELECT name FROM sqlite_master WHERE type='table'"
    
    conn = sqlite3.connect(getDBPath())
    
    tables = conn.execute(tables_stmt)
    for table in tables:
        stmt = "SELECT id,json FROM " + str(table[0])
        
        try:
            rows = conn.execute(stmt)
            for row in rows:
                if KeyWord in row[1].upper():
                    print str(table[0]) + " " + str(row[0]) #+ " -> " + row[1]
        except:
            pass 


def search_for_id(id):
    tables_stmt = "SELECT name FROM sqlite_master WHERE type='table'"
    
    conn = sqlite3.connect(getDBPath())
    
    tables = conn.execute(tables_stmt)
    for table in tables:
        stmt = "SELECT id,json FROM " + str(table[0])
        
        try:
            rows = conn.execute(stmt)
            for row in rows:
                if row[0] == id:
                    print str(table[0]) + " " + str(row[0]) #+ " -> " + row[1]
        except:
            pass 

#search_for_keyword("NIGHTFALL")
#search_for_id(twos_comp_32(2505971849))

def generate_milestone_data(lmanifest,lang):
    db_zip = downloadDBFile(lmanifest,lang)
    unzip(db_zip)
    
    raw_milestones = get_milestones()
    milestones = {}
    for key in raw_milestones:
        milestone_def = json.loads(queryDBForItem(getDBPath(), "DestinyMilestoneDefinition",  raw_milestones[key]["milestoneHash"]))
        
        if milestone_def.has_key("friendlyName"):
            if milestone_def["friendlyName"] != "ClanProgress":
                milestone = {
                    "name": None,
                    "description": None,
                    "friendlyName":milestone_def["friendlyName"]
                }
                
                if milestone_def.has_key("displayProperties"):
                    milestone["name"] = milestone_def["displayProperties"]["name"]
                    milestone["description"] = milestone_def["displayProperties"]["description"]
                    
                if milestone["friendlyName"] == "Nightfall":
                    activityHash = raw_milestones[key]["availableQuests"][0] ["activity"]["activityHash"]
                    activity = json.loads(queryDBForItem(getDBPath(), "DestinyActivityDefinition", activityHash))
                    
                    milestone["name"] = activity["displayProperties"]["name"]
                    milestone["description"] = activity["displayProperties"]["description"]
                    
                    milestone["friendlyName"] = milestone["name"].split(":")[0].strip()
                    milestone["name"] = milestone["name"].split(":")[1].strip()
                    
                if milestone["friendlyName"] == "Hotspot":
                    questItemHash = str(raw_milestones[key]["availableQuests"][0]["questItemHash"])
                    milestone["name"] = milestone_def["quests"][questItemHash]["displayProperties"]["name"]
                    milestone["description"] = milestone_def["quests"][questItemHash]["displayProperties"]["description"]
                    
                    milestone["friendlyName"] = milestone["name"].split(":")[0].strip()
                    milestone["name"] = milestone["name"].split(":")[1].strip()
                
                milestones[milestone_def["friendlyName"]] = milestone
        else:
            if milestone_def.has_key("displayProperties"):
                if milestone_def["displayProperties"]["name"] == u"Xûr":
                    milestone = {
                        "name": milestone_def["displayProperties"]["name"],
                        "description": milestone_def["displayProperties"]["description"],
                        "friendlyName":"XUR"
                    }
                    
                    milestones[milestone["friendlyName"]] = milestone
                else:
                    print "NOT XUR?"
                    print json.dumps(milestone_def)
                    print "#####\n"
            else:
                    print "NO friendly names?"
                    print json.dumps(milestone_def)
                    print "#####\n"
    
    cleanup()
    
    return milestones

def refresh():
    milestone_data = {}
    milestone_data["de"] = generate_milestone_data(get_manifest(),"de")
    milestone_data["en"] = generate_milestone_data(get_manifest(),"en")
    
    with open('destiny.json', 'w') as outfile:
        json.dump(milestone_data, outfile)

    storage = xamoom_storage()
    storage.upload_blob("destiny.json","destiny.json","salendron-destiny","text/json")
    acl = xamoom_acl(xamoom_acl.ALL,xamoom_acl.GRANT_READ)
    storage.set_acl("salendron-destiny",acl,file_name="destiny.json")
        
    
    
refresh()