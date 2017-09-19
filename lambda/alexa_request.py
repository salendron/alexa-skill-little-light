from util import ISO8601_to_datetime

class RequestObjectBase(object):
    
    def __init__(self, **entries):
        self.__dict__.update(entries)
        
        #parse timestamp to datetime object
        self.timestamp = ISO8601_to_datetime(self.timestamp)
    
    def __getattribute__(self, name):
        """
        Overrides the default behaviour of gettting member values to ensure that we get at least None
        and not an exception.
        Attribute object.
        """        
        try:
            return object.__getattribute__(self,name)
        except AttributeError: 
            return None

class LaunchRequest(RequestObjectBase):
    
    def __init__(self, **entries):
        super(LaunchRequest, self).__init__(**entries)
        
class SessionEndedRequest(RequestObjectBase):
    
    def __init__(self, **entries):
        super(SessionEndedRequest, self).__init__(**entries)
        
class IntentSlot(object):
    
    def __init__(self, **entries):
        self.__dict__.update(entries)
        
    def is_valid(self):
        return (
            hasattr(self,"name") and
            hasattr(self,"value") and
            self.name != None and
            self.value != None and
            self.name.strip() != "" and
            self.value.strip() != ""
        )
    
class IntentRequestIntent(object):
    
    def __init__(self, **entries):
        self.__dict__.update(entries)
        
        if entries.has_key("slots"): #parse slots
            self.slots = {}
            for key in entries["slots"].keys():
                slot =  IntentSlot(**entries["slots"][key])
                
                if slot.is_valid():
                    self.slots[key] = slot
                    
    def has_slot(self,name):
        return self.slots.has_key(name)
    
    def get_slot(self,name):
        if self.has_slot(name):
            return self.slots[name].value
        else:
            return None     
        
class IntentRequest(RequestObjectBase):
    
    def __init__(self, **entries):
        super(IntentRequest, self).__init__(**entries)
        
        self.intent = IntentRequestIntent(**entries["intent"])
        

"""

"intent": {
      "name": "IntentActivity",
      "slots": {
        "activityname": {
          "name": "activityname",
          "value": "nightfall"
        }
      }
    }

{
  "type": "IntentRequest",
  "requestId": "string",
  "timestamp": "string",
  "dialogState": "string",
  "locale": "string",
  "intent": {
    "name": "string",
    "confirmationStatus": "string",
    "slots": {
      "SlotName": {
        "name": "string",
        "value": "string",
        "confirmationStatus": "string",
        "resolutions": {
          "resolutionsPerAuthority": [
            {
              "authority": "string",
              "status": {
                "code": "string"
              },
              "values": [
                {
                  "value": {
                    "name": "string",
                    "id": "string"
                  }
                }
              ]
            }
          ]
        }
      }
    }
  }
}
"""
