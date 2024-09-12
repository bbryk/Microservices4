

import uvicorn
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import hazelcast
class Item(BaseModel):
    id:int
    content : str


class LoggingRepository():
    def __init__(self):
        # self.map = dict()
        self.hz = hazelcast.HazelcastClient()
        self.map = self.hz.get_map("my-distributed-map1").blocking()
    def addToMap(self,msg:Item):
        # self.map[msg.id] = msg.content
        self.map.put(msg.id, msg.content)
        print(self.map)


    def getLogsFromMap(self):
        return ", ".join(self.map.values())
