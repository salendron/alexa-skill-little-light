#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

messages = {
    "de":{
        "milestone-phrase":"#caption# ist diese Woche \"#name#\". #description#",
        "briefing-phrase":"Hier ist dein Destiny Info Briefing: ",
        "nightfall-phrase":"Der Nightfall Strike diese Woche ist \"#name#\". ",
        "xur-phrase":"Der Agent der Neun ist hier! ",
        "no-xur-phrase":"Der Agent der Neun ist noch nicht angekommen. ",
        "trials-phrase":"Die Prüfungen der Neun haben begonnen! ",
        "raid-phrase":"Der Raid diese Woche ist \"#name#\". ",
        "exit-phrase":"Briefing beendet.",
        "help-phrase":"Frage mich zum Beispiel \"Was ist der Nightfall diese Woche?\" oder \"Ist Xur schon da?\"."
    },
    "en":{
        "milestone-phrase":"This week's #caption# is  \"#name#\". #description#",
        "briefing-phrase":"Destiny Info Briefing: ",
        "nightfall-phrase":"This week's nightfall strike is \"#name#\". ",
        "xur-phrase":"The agent of the nine has arrived! ",
        "no-xur-phrase":"The agent of the nine has not yet arrived. ",
        "trials-phrase":"Trials of the Nine has begun! ",
        "raid-phrase":"This week\'s raid is  \"#name#\". ",
        "exit-phrase":"End of briefing.",
        "help-phrase":"Ask me for example \"What is the Nightfall this week?\" or \"Has Xur arrived?\"."
    }
}

error_messages = {
    "de":{
        "unknown-milestone": "\"#caption#\" ist mir nicht bekannt.",
        "no-milestone": "Da kann ich dir jetzt nicht weiterhelfen.",
        "generic-error": "Da ist etwas schief gelaufen."
    },
    "en":{
        "unknown-milestone": "I don't know anything about \"#caption#\".",
        "no-milestone": "I think I can't help you with this one.",
        "generic-error": "Sorry, something went wrong. Please try this again."
    }
}

def get_error_message(msg_name,locale="en-us"):
    msg_name = str(msg_name)
    locale = locale.split("-")[0]
    
    if error_messages.has_key(locale):
        if error_messages[locale].has_key(msg_name):
            return error_messages[locale][msg_name]
        else:
            print("Error Message Translation missing for [" +locale + "][" + msg_name + "]!")
            return "Something went wrong."
    else:
        print("Error Message Translation missing for [" + locale + "][" + msg_name + "]!")
        return "Something went wrong."
    
def get_message(msg_name,locale="en-us"):
    msg_name = str(msg_name)
    locale = locale.split("-")[0]
    
    if messages.has_key(locale):
        if messages[locale].has_key(msg_name):
            return messages[locale][msg_name]
        else:
            print("Message Translation missing for [" +locale + "][" + msg_name + "]!")
            return "Something went wrong."
    else:
        print("Message Translation missing for [" + locale + "][" + msg_name + "]!")
        return "Something went wrong."