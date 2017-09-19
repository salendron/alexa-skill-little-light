from alexa_request import IntentRequest, LaunchRequest, SessionEndedRequest

class IntentObjectBase(object):
    
    def __init__(self, **entries):
        self.__dict__.update(entries)
    
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

class Attributes(IntentObjectBase):
    
    def __init__(self, **entries):
        super(Attributes, self).__init__(**entries)
        
    def get_attr(self,name):
        if self.string.has_key(name):
            return self.string[name]
        else:
            return None
        
    def has_attr(self,name):
        return self.string.has_key(name)

class Application(IntentObjectBase):
    
    def __init__(self, **entries):
        super(Application, self).__init__(**entries)

class Permissions(IntentObjectBase):
    
    def __init__(self, **entries):
        super(Permissions, self).__init__(**entries)
    
class User(IntentObjectBase): 
    
    def __init__(self, **entries):
        super(User, self).__init__(**entries)
        
        if entries.has_key("permissions"):
            self.permissions = Permissions(**entries["permissions"])

class Session(IntentObjectBase): 
    
    def __init__(self, **entries):
        super(Session, self).__init__(**entries)
        
        self.application = Application(**entries["application"])
        
        if entries.has_key("attributes"):
            self.attributes = Attributes(**entries["attributes"])
        else:
            self.attributes = {}
        
        
        self.user = User(**entries["user"])

class Device(IntentObjectBase):  
    
    def __init__(self, **entries):
        super(Device, self).__init__(**entries)
        
class System(IntentObjectBase): 
    
    def __init__(self, **entries):
        super(System, self).__init__(**entries)
        
        self.application = Application(**entries["application"])
        self.user = User(**entries["user"])
        self.device = Device(**entries["device"])

class Context(IntentObjectBase): 
    
    def __init__(self, **entries):
        super(Context, self).__init__(**entries)
        
        self.system = System(**entries["System"])

class Intent(IntentObjectBase):
    def __init__(self, **entries):
        super(Intent, self).__init__(**entries)
        
        self.session = Session(**entries["session"])
        self.context = Context(**entries["context"])
        self.__parse_request(entries["request"])
        self.func = None
        
    def __parse_request(self,request_dict):
        request_type = request_dict["type"]
        
        if request_type == "IntentRequest":
            self.request = IntentRequest(**request_dict)
        elif request_type == "LaunchRequest":
            self.request = LaunchRequest(**request_dict)
        elif request_type == "SessionEndedRequest":
            self.request = SessionEndedRequest(**request_dict)
        
    def execute(self):
        if self.func != None: #eh schon  wissen
            return self.func(self)
        
