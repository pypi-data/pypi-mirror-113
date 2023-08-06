from requests import Session
from re import search
from io import BufferedReader, BytesIO

class APIError(Exception):
    pass

class API:
    def __init__(self, **kwargs):
        self.session = Session()

        try:
            self.api_key = kwargs["key"]
            self.session.headers = {
                "User-Agent": "PyDeepAI/0.1.0",
                "api-key": kwargs["key"]
            }
        except KeyError:
            raise APIError("Key is not found")
        
        try:
            self.session.proxies = kwargs["proxies"]
        except KeyError:
            pass
    
    def __del__(self):
        self.session.close()
    
    def __str__(self):
        return f"<API {self.api_key}>"

    def request(self, api=None, fileData=None, dataType=None):
        if fileData == None: raise KeyError("fileData is None object")
        if api == None: raise KeyError("api is None object")

        if type(fileData) == str:
            if dataType == None:
                if fileData.split(".")[-1] == "jpg" or "jpeg" or "png":
                    dataType = "image"
                elif fileData.split(".")[-1] == "webm" or "mp4":
                    dataType = "video"
                elif search("youtu", fileData) != None:
                    dataType = "video"
                else:
                    raise TypeError("Unsupported format")
                
            if search("http", fileData) != None:
                response = self.session.post(f'https://api.deepai.org/api/{api}',
                                             data={
                                                 dataType: fileData
                                             })
            else:
                response = self.session.post(f'https://api.deepai.org/api/{api}',
                                             files={
                                                 dataType: open(fileData, "rb")
                                             })
        elif type(fileData) == bytes:
            if dataType == None: raise KeyError("dataType is None object")
            response = self.session.post(f'https://api.deepai.org/api/{api}',
                                         files={
                                            dataType: fileData
                                         })
        elif type(fileData) == BufferedReader or BytesIO:
            if dataType == None: raise KeyError("dataType is None object")
            response = self.session.post(f'https://api.deepai.org/api/{api}',
                                         files={
                                            dataType: fileData.read()
                                         })
        else:
            raise TypeError("Unsupported object type")
        
        return response.json()