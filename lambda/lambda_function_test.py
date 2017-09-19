from lambda_function import lambda_handler

from proboscis.asserts import assert_true, assert_false, assert_equal
from proboscis import SkipTest
from proboscis import test

@test(groups=["lambdahandler.intent"])
def test_intent():
    test_event = {
                            "session": {
                              "new": True,
                              "sessionId": "SessionId.323e732c-a975-49b3-b796-82a5709b0c31",
                              "application": {
                                "applicationId": "amzn1.ask.skill.78652fba-466f-4a54-b5c0-ea7930de5788"
                              },
                              "attributes": {},
                              "user": {
                                "userId": "amzn1.ask.account.AESP3HPYTOIQHOFKO4XBHIIC74XJTON52GCQNBQR2ARB6XFIX5MKFNQ2QKBOLQTUYGXTM476RL4F7WKPYCMIJGGFT2QD6PNDSEHVIZN4KRLB5U2X7AEZM66CWD7YN2YJEMQBU6IJDFHMF6RQ44V5EGIWI62Y2N3IVFI3O7QNMEKAMGTBV5XJLKDKBYMN2XZF6UHHGKHQL45M2IY"
                              }
                            },
                            "request": {
                              "type": "IntentRequest",
                              "requestId": "EdwRequestId.41fae6de-d61f-488c-936e-18f5abad6a0e",
                              "intent": {
                                "name": "IntentActivity",
                                "slots": {
                                  "activityname": {
                                    "name": "activityname",
                                    "value": "raid"
                                  }
                                }
                              },
                              "locale": "en-US",
                              "timestamp": "2017-09-15T06:05:20Z"
                            },
                            "context": {
                              "AudioPlayer": {
                                "playerActivity": "IDLE"
                              },
                              "System": {
                                "application": {
                                  "applicationId": "amzn1.ask.skill.78652fba-466f-4a54-b5c0-ea7930de5788"
                                },
                                "user": {
                                  "userId": "amzn1.ask.account.AESP3HPYTOIQHOFKO4XBHIIC74XJTON52GCQNBQR2ARB6XFIX5MKFNQ2QKBOLQTUYGXTM476RL4F7WKPYCMIJGGFT2QD6PNDSEHVIZN4KRLB5U2X7AEZM66CWD7YN2YJEMQBU6IJDFHMF6RQ44V5EGIWI62Y2N3IVFI3O7QNMEKAMGTBV5XJLKDKBYMN2XZF6UHHGKHQL45M2IY"
                                },
                                "device": {
                                  "supportedInterfaces": {}
                                }
                              }
                            },
                            "version": "1.0"
                          }
    lambda_handler(test_event,None)


### RUN TESTS ###
def run_tests():
    from proboscis import TestProgram

    # Run Proboscis and exit.
    TestProgram().run_and_exit()

if __name__ == '__main__':
    run_tests()