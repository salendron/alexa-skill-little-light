from proboscis.asserts import assert_true, assert_false, assert_equal
from proboscis import SkipTest
from proboscis import test

from alexa_request import RequestObjectBase, LaunchRequest, SessionEndedRequest,IntentRequest
from util import datetime_to_ISO8601

@test(groups=["intent.base"])
def test_getattribute():
    intent_dict = {"a":1,"timestamp":"2015-05-13T12:34:56Z"}
    
    i = RequestObjectBase(**intent_dict)
    assert_true(i.a == intent_dict["a"])
    assert_true(datetime_to_ISO8601(i.timestamp) == intent_dict["timestamp"])
    assert_true(i.c == None)

@test(groups=["request.parsing"])
def parse_launchrequest():
    request_dict = {
                                "type": "LaunchRequest",
                                "requestId": "amzn1.echo-api.request.0000000-0000-0000-0000-00000000000",
                                "timestamp": "2015-05-13T12:34:56Z",
                                "locale": "en"
                              }

    
    #Create new request from dict
    r = LaunchRequest(**request_dict)
    
    assert_equal(r.type,request_dict["type"])
    assert_equal(r.requestId,request_dict["requestId"])
    assert_equal(r.locale,request_dict["locale"])
    assert_equal(datetime_to_ISO8601(r.timestamp),request_dict["timestamp"])
    
@test(groups=["request.parsing"])
def parse_sessionendedrequest():
    request_dict = {
                                "type": "SessionEndedRequest",
                                "requestId": "amzn1.echo-api.request.0000000-0000-0000-0000-00000000000",
                                "timestamp": "2015-05-13T12:34:56Z",
                                "reason": "USER_INITIATED",
                                "locale": "de"
                              }

    #Create new request from dict
    r = SessionEndedRequest(**request_dict)
    
    assert_equal(r.type,request_dict["type"])
    assert_equal(r.requestId,request_dict["requestId"])
    assert_equal(r.locale,request_dict["locale"])
    assert_equal(r.reason,request_dict["reason"])
    assert_equal(datetime_to_ISO8601(r.timestamp),request_dict["timestamp"])
    
@test(groups=["request.parsing"])
def parse_intentrequest():
    request_dict = {
                                "type": "IntentRequest",
                                "requestId": "EdwRequestId.41fae6de-d61f-488c-936e-18f5abad6a0e",
                                "intent": {
                                  "name": "IntentActivity",
                                  "slots": {
                                    "activityname": {
                                      "name": "activityname",
                                      "value": "nightfall"
                                    }
                                  }
                                },
                                "locale": "en-US",
                                "timestamp": "2017-09-15T06:05:20Z"
                              }

    #Create new request from dict
    r = IntentRequest(**request_dict)
    
    assert_equal(r.type,request_dict["type"])
    assert_equal(r.requestId,request_dict["requestId"])
    assert_equal(r.locale,request_dict["locale"])
    assert_equal(datetime_to_ISO8601(r.timestamp),request_dict["timestamp"])
    
    ###slots
    slots = request_dict["intent"]["slots"]
    
    for key in slots.keys():
        assert_true(r.intent.has_slot(key))
        assert_equal(r.intent.get_slot(key).name, slots[key]["name"])
        assert_equal(r.intent.get_slot(key).value, slots[key]["value"])
    
### RUN TESTS ###
def run_tests():
    from proboscis import TestProgram

    # Run Proboscis and exit.
    TestProgram().run_and_exit()

if __name__ == '__main__':
    run_tests()
