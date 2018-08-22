from nuance_api.request_json_dict.nuance_dict_ASR_13 import *
import re
import os, sys
import json
from io import BytesIO
import ssl
import http.client

class Part(object):

    def __init__(self, name=None, contentType=None, data=None, encoding=None, paramName=None):
        super().__init__()
        self.name = name
        self.contentType = contentType
        self.data = data
        self.paramName = paramName
        self.encoding = encoding

    def encode(self):

        message_part = BytesIO()

        if self.paramName:
            message_part.write(('Content-Disposition:form-data; name="%s"; paramName="%s"\r\n' % (self.name, self.paramName)).encode())
        else:
            message_part.write(('Content-Disposition:form-data; name="%s"\r\n' % (self.name)).encode())

        message_part.write(("Content-Type: %s\r\n" % (self.contentType)).encode())
        message_part.write(("Content-Transfer-Encoding: %s\r\n" % (self.encoding)).encode())
        message_part.write("\r\n".encode())
        message_part.write(self.data)
        return message_part.getvalue()

class Request(object):

    boundary = "WebKitFormBoundary7MA4YWxkTrZu0gW"

    def __init__(self):
        super().__init__()
        #''' possible argument: audio dir was converted to obj at first, then we can assign attr to it'''
        self.parameters = []

    def add_json_parameter(self, name, paramName, data):

        binary = json.dumps(data).encode()
        self.parameters.append(Part(name=name, paramName=paramName, contentType="application/json; charset=utf-8", data=binary, encoding="8bit"))

    def add_audio_parameter(self, name, paramName, data):
        # specify your audio codec in contentType, it is also related to the attribute "inCodec" in nuance_dict_ASR_13.py
        self.parameters.append(Part(name=name, paramName=paramName, contentType="audio/x-wav;codec=pcm;bit=16;rate=16000", data=data, encoding="binary"))

    def encode(self):

        message_body = BytesIO()

        for parameter in self.parameters:

            message_body.write(("--%s\r\n" % (self.boundary)).encode())
            message_body.write(parameter.encode())
            message_body.write("\r\n".encode())

        message_body.write(("\r\n--%s--" % (self.boundary)).encode())
        # print(message_body.getvalue())
        return message_body.getvalue()

def init_request(filepath):

    request = Request()
    #''' add form data part: RequestData '''
    request.add_json_parameter("RequestData", None, RequestData)
    #''' add form data part: DictParameter, paramName = REQUEST_INFO '''
    request.add_json_parameter("DictParameter", "REQUEST_INFO", REQUEST_INFO)
    #''' add form data part: ConcludingAudioParameter, paramName = AUDIO_INFO '''

    with open(filepath, "rb") as audio_file:

        binary_data = audio_file.read(1024)
        while binary_data:
            request.add_audio_parameter("ConcludingAudioParameter", "AUDIO_INFO", binary_data)
            binary_data = audio_file.read(1024)

    return request.encode()

def get_asr_transcription_from_response(raw_data):

    param1, param2, param3 = raw_data.partition('\r\n\r\n')
    param4, param5, param6 = param3.partition('\r\n')
    return json.loads(param4)['transcriptions'][0]

if __name__ == "__main__":

    # specify your nuance api url
    host = "examplenuanceapi.com"
    uri = "/ExampleServlet"

    audio_rootdir = os.path.abspath("audio")

    files = os.listdir(audio_rootdir)
    modi_files = [file for file in files if not re.search("^\..*$", file)]

    for file in modi_files:

        message_body = init_request(os.path.join(audio_rootdir, file))

        conn = http.client.HTTPSConnection(host, port=443, context=ssl._create_unverified_context())
        conn.set_debuglevel(0)
        conn.request("POST", uri, body=message_body, headers=HEADERS, encode_chunked=True)

        res = conn.getresponse()
        raw_data = res.read().decode('utf-8')

        asr_transcription = get_asr_transcription_from_response(raw_data)
        print(asr_transcription)



