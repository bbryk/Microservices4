import random
import hazelcast
from fastapi import FastAPI, APIRouter
from FacadeService import FacadeService
from pydantic import BaseModel
import random
from asyncio import Lock
from fastapi import HTTPException

import uvicorn
from fastapi import FastAPI, APIRouter

from pydantic import BaseModel

from FacadeService import FacadeService
# Initialize the Hazelcast client
client = hazelcast.HazelcastClient()
queue = client.get_queue("queue")


class Item(BaseModel):
    content: str
    id: int


class StartItem(BaseModel):
    content: str


class FacadeController():

    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/", self.get_request, methods=["GET"])
        self.router.add_api_route("/", self.post_request, methods=["POST"])
        self.fs = FacadeService()
        self.lock = Lock()

    async def get_request(self):
        print(f"Received get in facade...")
        port = random.choice([8005, 8006, 8007])
        logging_url = f"http://127.0.0.1:{port}"
        r = await self.fs.get_from_logging(logging_url)
        print(r.text)

        r1 = await self.fs.get_from_messages(f"http://127.0.0.1:8100")
        r2 = await self.fs.get_from_messages(f"http://127.0.0.1:8101")
        r3 = await self.fs.get_from_messages(f"http://127.0.0.1:8102")
        print("From messages:")
        print(r1.text +" "+ r2.text +" "+ r3.text)

        return 0

    async def post_request(self, item: StartItem):
        queue.offer(item.json())


        print(f"Received post: \"{item.content}\" in facade...")
        port = random.choice([8005, 8006, 8007])
        logging_url = f"http://127.0.0.1:{port}"
        r = await self.fs.post_to_logging(item, logging_url)
        print(r.status_code)
        if r.status_code != 200:
            print("Something went wrong.")


        port = random.choice([8100, 8101, 8102])
        msg_url = f"http://127.0.0.1:{port}"
        r1 = await self.fs.post_to_messages(item, msg_url)

        return item.content


if __name__ == "__main__":
    facade_port = 8001
    localhost = "127.0.0.1"
    app = FastAPI()
    fc = FacadeController()
    app.include_router(fc.router)
    uvicorn.run(app, host=localhost, port=facade_port)
