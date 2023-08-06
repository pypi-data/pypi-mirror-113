import json
from httpx import AsyncClient,TimeoutException,HTTPStatusError
from ..config import config
class FR24Request(object):


    def __init__(self, url, params = {}, headers = {}):

        self.url = url
        self.params = params
        self.headers = headers

    async def __send_request(self, url, params, headers):
        timeout = params.get('timeout',config.TIMEOUT)
        try:
            async with AsyncClient(timeout=timeout) as client:
                resp = await client.get(url,headers=headers,params=params)
        except TimeoutException as e:
            raise e
        except HTTPStatusError as e:
            raise e
        print(resp.url)
        return  resp
         
    async def get_content(self):
        content = await self.__send_request(self.url,self.params,self.headers)
        return content

    # def get_content_type(self):