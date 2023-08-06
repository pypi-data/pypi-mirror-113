import requests
from .errors import InvalidAuthKey, NotValidTest, DefaultStoreTypeError, LangsTypeError, TestsTypeError, TextTypeError, SubAttributesTypeError, ApiException, RateLimiterTypeError, RateLimited
import warnings
import json
import datetime

Allowed_Tests = {
                    "TOXICITY":["en","es","fr","de","pt","it","ru"],
                    "TOXICITY_EXPERIMENTAL": ["ar"],
                    "SEVERE_TOXICITY": ["en","fr","es","de","it","pt","ru"],
                    "SEVERE_TOXICITY_EXPERIMENTAL": ["ar"],
                    "IDENTITY_ATTACK": ["de","it","pt","ru","en"],
                    "IDENTITY_ATTACK_EXPERIMENTAL": ["fr","es","ar"],
                    "INSULT": ["de", "it", "pt", "ru", "en"],
                    "INSULT_EXPERIMENTAL": ["fr", "es", "ar"],
                    "PROFANITY": ["de", "it", "pt", "ru", "en"],
                    "PROFANITY_EXPERIMENTAL": ["fr", "es", "ar"],
                    "THREAT": ["de", "it", "pt", "ru", "en"],
                    "THREAT_EXPERIMENTAL": ["fr", "es", "ar"],
                    "SEXUALLY_EXPLICIT": ["en"],
                    "FLIRTATION": ["en"]
                }

base_url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

class Perspective:
    def __init__(self, key, **kwargs):
            r = requests.post(base_url,params={"key": key}).json()
            if "error" in r and "reason" in r["error"]["details"][0] and r["error"]["details"][0]["reason"]== "API_KEY_INVALID":
                raise InvalidAuthKey("Invalid Auth Key Provided!")
            else:
                self._key = key
                default_not_store = kwargs.get("defaultnotstore") or True
                if not isinstance(default_not_store, bool):
                    raise DefaultStoreTypeError("Invalid Type. Please Provide Bool For Default Store Option.")
                self.default_store = default_not_store
                rate_limiter= kwargs.get("ratelimiter") or False
                if not isinstance(rate_limiter, bool):
                    raise RateLimiterTypeError("Invalid Type. Please Provide Bool For Rate Limiter Option.")
                self.rate_limiter = rate_limiter
                if rate_limiter == True:
                    self._last_used = 0

    def _rate_limit(self):
        if self.rate_limiter:
            if self._last_used == 0:
                self._last_used = datetime.datetime.now()
                return False
            else:
                now = datetime.datetime.now()
                difference = now - self._last_used
                if difference.total_seconds() < 1:
                    return True
                else:
                    self._last_used = now
                    return False

    def get_score(self, text, **kwargs):
        # Kwargs Getting
        tests = kwargs.get("tests") or "TOXICITY"
        do_not_store = kwargs.get("do_not_store") or self.default_store
        langs = kwargs.get("langs") or ["en"]

        # Checking If Text Is String
        if not isinstance(text, str):
            raise TextTypeError("Please Provide Valid String For Text")

        # Checking If Do Not Store Option Is Bool
        if not isinstance(do_not_store, bool):
            warnings.warn("Not Valid Bool Provided. Using Default Not Store Option")
            do_not_store = self.default_store

        # Converting Langs To List If Langs Type String
        if isinstance(langs, str):
            langs = [langs]

        # If Langs Type Not List Or Tuple Then Raising Error
        if not isinstance(langs, (list,tuple)):
            raise LangsTypeError("Please Provide List or Tuple For Langs! Default Setted To English")

        # Checking Text Length, If It Is More Than 3000 Character Than Just Getting First 3000 Character
        if len(text) > 3000:
            warnings.warn("API Supports 3000 Character At Text. Getting Only 3000 Character On Provided ")
            text = text[:3000]

        # Checking Tests Is String If It Is Then Converting To List
        if isinstance(tests, str):
            tests = [tests]

        # Checking If Tests Is List or Tuple, If They Are Adding '"Key": {}' To New_Data Dict, Checking Languages Is Fitting With Support Languages
        if isinstance(tests, (list,tuple)):
            new_data = {}
            for key in tests:
                if key not in list(Allowed_Tests.keys()):
                    raise NotValidTest(f"'{key}' Not A Valid Test! See Documentation For Valid Tests")
                for provided_lang in langs:
                    if provided_lang not in Allowed_Tests[key]:
                        raise LangsTypeError(f"'{provided_lang}' Language Is Not Supported On '{key}' Test!")
                new_data[key] = {}
            tests = new_data

        # Checking If Tests Are Dict, If They Are Not Then Raising Error
        if not isinstance(tests, dict):
            raise TestsTypeError("Please Provide List or Tuple For Tests!")

        if self._rate_limit():
            raise RateLimited("Rate Limited. This Request Cancelled By Auto Rate Limiter")
        # Start Of Request
        key = {"key": self._key}
        payload = {"comment": {"text":text}, "requestedAttributes":{},"languages":langs,"doNotStore":do_not_store}
        for test in list(tests.keys()):
            payload["requestedAttributes"][test] = tests[test]
        headers = {'content-type': "application/json"}
        payload = json.dumps(payload)
        response = requests.post(base_url,
                            data=payload,
                            headers=headers,
                            params=key).json()
        if "error" in response:
            raise ApiException(f"[{response['error']['code']}][{response['error']['status']}]: {response['error']['message']}",raw_data=response)
        comment = Comment(text,response)
        base_data = response["attributeScores"]
        for attr in list(base_data.keys()):
            total_score_value = base_data[attr]["summaryScore"]["value"]
            total_score_type = base_data[attr]["summaryScore"]["type"]
            new_attr = Attribute(attr,total_score_value,total_score_type)
            for span in base_data[attr]["spanScores"]:
                span = Span(span["begin"],span["end"],span["score"]["value"],span["score"]["type"],comment)
                new_attr.spans.append(span)
            comment.attributes.append(new_attr)
        return comment

class Comment:
    def __init__(self,text,data):
        self.text = text
        self.raw_data = data
        self.attributes = []
        self.requests_langs = data["languages"]
        self.detected_langs = data["detectedLanguages"]

    def __getitem__(self, key):
        if key.upper() not in Allowed_Tests:
            raise NotValidTest(f"'{key}' Not Found In Allowed Tests. Please Look To Documentation!")
        for att_key in self.attributes:
            if att_key.name == key.upper():
                return att_key
        raise TextTypeError(f"'{key.upper()}' Attribute Cant Found On This Class")

    def __str__(self):
        return self.text

class Attribute:
    def __init__(self, name, score, score_type):
        self.name = name
        self.spans = []
        self.score = score
        self.score_type = score_type

    def __getitem__(self,index):
        return self.spans[index]

class Span:
    def __init__(self,start,end,score,score_type,comment):
        self.start = start
        self.end = end
        self.score = score
        self.score_type = score_type
        self.comment = comment

    def __str__(self):
        return self.comment.text[self.start:self.end]
