"""
Main Entry Point
"""

from __future__ import print_function
import traceback
from alexa_intent import Intent
from intent_funcs import milestone_handler_func, briefing_handler_func, error_handler_func, cancel_handler_func, help_handler_func

def handle_intent(intent):
    if intent.request.type == "IntentRequest":
        intent_name = intent.request.intent.name
        
        if  intent_name == "IntentActivity":
            intent.func = milestone_handler_func
        elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
             intent.func =  cancel_handler_func
        elif intent_name == "AMAZON.HelpIntent":
             intent.func =  help_handler_func
    elif intent.request.type ==  "LaunchRequest":
        intent.func =  briefing_handler_func
    else:
        intent.func =  error_handler_func
    
    return intent.execute()

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    #print("event.session.application.applicationId=" + event['session']['application']['applicationId'])

    #if event['session']['new']:
    #    on_session_started({'requestId': event['request']['requestId']},event['session'])
    
    intent = None
    try:
        intent = Intent(**event)
        return handle_intent(intent)
    except Exception as ex:
        err = traceback.format_exc()
        print(err)
        return error_handler_func(intent,msg=str(err))