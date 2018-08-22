"""
pattern for nuance cloud request message body
specify your data here
"""

import base64

boundary = "WebKitFormBoundary7MA4YWxkTrZu0gW"
proxy_username = b"" # required if request with proxy server
proxy_password = b"" # required if request with proxy server
auth = base64.b64encode(b'%s:%s' % (proxy_username, proxy_password))

HEADERS = {
    "Transfer-Encoding": "chunked",
    "Content-Type": "multipart/form-data; boundary=%s" % boundary,
    "Connection": "Keep-Alive",
    "Cache-Control": "no-cache",
    "Accept": "*/*",
    "Host": "",
    "User-Agent": "",
    "Proxy-Authorization": "Basic %s" % auth
}

RequestData = {
   "appKey":"",
   "appId":"",
   "uId":"",
   "inCodec":"",
   "outCodec":"",
   "cmdName":"",
   "appName":"",
   "appVersion":"",
   "language":"",
   "carrier":"",
   "deviceModel":"",
   "cmdTimeout":"",
   "cmdDict":{
      "dictation_type":"",
      "dictation_language":"e",
      "locale":"",
      "nmaid":"",
      "application_name":"",
      "organization_id":"",
      "phone_os":"",
      "phone_network":"",
      "audio_source":"",
      "location":"",
      "application_session_id":"",
      "application_state_id":"",
      "utterance_number":"",
      "ui_language":"",
      "phone_submodel":""
   }
}

REQUEST_INFO ={
   "text":"",
   "start":0,
   "end":0,
   "enable_intermediate_response":0
}
