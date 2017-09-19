from proboscis.asserts import assert_true, assert_false, assert_equal
from proboscis import SkipTest
from proboscis import test

from alexa_intent import IntentObjectBase, Intent

@test(groups=["intent.base"])
def test_getattribute():
    intent_dict = {"a":1,"b":2}
    
    i = IntentObjectBase(**intent_dict)
    assert_true(i.a == intent_dict["a"])
    assert_true(i.c == None)

@test(groups=["intent.parsing"])
def parse_intent():
    intent_dict = {
                                "version": "string",
                                "session": {
                                  "new": True,
                                  "sessionId": "abc123",
                                  "application": {
                                    "applicationId": "string"
                                  },
                                  "attributes": {
                                    "string": {"attr1":"value1"}
                                  },
                                  "user": {
                                    "userId": "ui123",
                                    "accessToken": "at123",
                                    "permissions": {
                                      "consentToken": "defghi123"
                                    }
                                  }
                                },
                                "context": {
                                  "AudioPlayer": {
                                    "token": "string",
                                    "offsetInMilliseconds": 0,
                                    "playerActivity": "string"
                                  },
                                  "System": {
                                    "application": {
                                      "applicationId": "string"
                                    },
                                    "user": {
                                      "userId": "string",
                                      "accessToken": "string",
                                      "permissions": {
                                        "consentToken": "string"
                                      }
                                    },
                                    "device": {
                                      "deviceId": "string",
                                      "supportedInterfaces": {
                                        "AudioPlayer": {}
                                      }
                                    },
                                    "apiEndpoint": "string"
                                  }
                                },
                                "request": {
                                                    "type": "LaunchRequest",
                                                    "requestId": "amzn1.echo-api.request.0000000-0000-0000-0000-00000000000",
                                                    "timestamp": "2015-05-13T12:34:56Z",
                                                    "locale": "en"
                                                    }
                            }
    
    #Create new intent from dict
    i = Intent(**intent_dict)
    
    #### SESSION
    session = intent_dict["session"]
    assert_equal(i.session.sessionId,session["sessionId"])
    assert_equal(i.session.new,session["new"])
    
    ### APPLICATION
    application = session["application"]
    assert_equal(i.session.application.applicationId,application["applicationId"])
    
    ### ATTRIBUTES
    attributes = session["attributes"]
    assert_equal(i.session.attributes.string["attr1"], attributes["string"]["attr1"])
    assert_equal(i.session.attributes.get_attr("attr1"), attributes["string"]["attr1"])
    assert_true(i.session.attributes.has_attr("attr1"))
    assert_false(i.session.attributes.has_attr("attr_invalid"))
    assert_equal(i.session.attributes.get_attr("attr_invalid"),None)
    
    ### USER
    user = session["user"]
    assert_equal(i.session.user.userId, user["userId"])
    assert_equal(i.session.user.accessToken, user["accessToken"])
    
    ## PERMISSIONS
    permissions = user["permissions"]
    assert_equal(i.session.user.permissions.consentToken, permissions["consentToken"])
    
    #### CONTEXT
    context = intent_dict["context"]
    
    ### SYSTEM
    system = context["System"]
    
    ## APPLICATION
    application = system["application"]
    assert_equal(i.context.system.application.applicationId,application["applicationId"])
    
    ## USER
    user = system["user"]
    assert_equal(i.context.system.user.userId, user["userId"])
    assert_equal(i.context.system.user.accessToken, user["accessToken"])
    
    ## DEVICE
    device = system["device"]
    assert_equal(i.context.system.device.deviceId, device["deviceId"])
    
### RUN TESTS ###
def run_tests():
    from proboscis import TestProgram

    # Run Proboscis and exit.
    TestProgram().run_and_exit()

if __name__ == '__main__':
    run_tests()
