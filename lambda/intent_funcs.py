from destiny_data import load_current_milestones_with_locale,slot_value_to_data_key
from translations import get_message, get_error_message
from speechlet import build_response, build_speechlet_response

def milestone_handler_func(intent):
    milestones = load_current_milestones_with_locale(intent.request.locale)
    
    if intent.request.intent.has_slot("activityname"):
        slot_value = intent.request.intent.get_slot("activityname")
        milestone_key = slot_value_to_data_key(slot_value)
        
        if milestone_key == "XUR":
            if milestones.has_milestone(milestone_key):
                phrase = get_message("xur-phrase",locale=intent.request.locale)
            else:
                phrase = get_message("no-xur-phrase",locale=intent.request.locale)
            
            return build_response({},build_speechlet_response("Xur",phrase, phrase, True)) 
        
        if milestones.has_milestone(milestone_key):
            milestone = milestones.get_milestone(milestone_key)
            
            print milestone_key
            
            phrase = ""
            if milestone_key in ["CallToArms","Meditations","ClanObjectives"]:
                phrase = milestone.description
            else:
                phrase = get_message("milestone-phrase",locale=intent.request.locale).replace("#caption#",slot_value).replace("#name#",milestone.name).replace("#description#",milestone.description)
                
            return build_response({},build_speechlet_response(milestone_key,phrase, phrase, True)) 
        else:
            phrase = get_error_message("unknown-milestone",locale=intent.request.locale).replace("#caption#",slot_value)
            return build_response({},build_speechlet_response(milestone_key,phrase, phrase, True))
    else:
        phrase =  get_error_message("no-milestone",locale=intent.request.locale)
        return build_response({},build_speechlet_response(":(",phrase, phrase, True))
    
def briefing_handler_func(intent):
    milestones = load_current_milestones_with_locale(intent.request.locale)
    
    phrase = get_message("briefing-phrase",locale=intent.request.locale)
    
    if milestones.has_milestone("Trials"):
        phrase = phrase + get_message("trials-phrase",locale=intent.request.locale)
        
    if milestones.has_milestone("XUR"):
        phrase = phrase + get_message("xur-phrase",locale=intent.request.locale) + milestones.get_milestone("XUR").description + " "
    
    if milestones.has_milestone("Nightfall"):
        phrase = phrase + get_message("nightfall-phrase",locale=intent.request.locale).replace("#name#",milestones.get_milestone("Nightfall").name)
        
    if milestones.has_milestone("Hotspot"):
        phrase = phrase + milestones.get_milestone("Hotspot").description + " "
        
    if milestones.has_milestone("Raid"):
        phrase = phrase + get_message("raid-phrase",locale=intent.request.locale).replace("#name#",milestones.get_milestone("Raid").name)
    
    if milestones.has_milestone("CallToArms"):
        phrase = phrase + milestones.get_milestone("CallToArms").description + " "
        
    if milestones.has_milestone("ClanObjectives"):
        phrase = phrase + milestones.get_milestone("ClanObjectives").description + " "
        
    if milestones.has_milestone("Meditations"):
        phrase = phrase + milestones.get_milestone("Meditations").description + "  "
        
    phrase = phrase + get_message("exit-phrase",locale=intent.request.locale)
        
    return build_response({},build_speechlet_response("Destiny 2 Briefing",phrase, phrase, True))

def cancel_handler_func(intent):    
    phrase = get_message("exit-phrase",locale=intent.request.locale)
    return build_response({},build_speechlet_response("Destiny 2 Briefing",phrase, phrase, True))

def help_handler_func(intent):    
    phrase = get_message("help-phrase",locale=intent.request.locale)
    return build_response({},build_speechlet_response("Warmind (Destiny 2)",phrase, phrase, True))

def error_handler_func(intent,msg=None):
    locale="en-us"
    if intent != None:
        locale=intent.request.locale
        
    phrase = get_error_message("generic-error",locale=locale)
    
    if msg != None:
        phrase = phrase + " " + msg
        
    return build_response({},build_speechlet_response("Error",phrase, phrase, True))
    
    