import hazelcast
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, APIRouter
from asyncio import Lock
from pydantic import BaseModel
# Initialize the Hazelcast client
client = hazelcast.HazelcastClient()
queue = client.get_queue("queue")
from fastapi import HTTPException

class Item(BaseModel):
    id:int
    content : str

class MessagesController():
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route("/", self.get_request, methods=["GET"])
        self.router.add_api_route("/", self.post_request, methods=["POST"])
        self.messages = []  # list to save messages
        self.lock = Lock()

    async def get_request(self):
        print(f"Received get in messages...")
        # Return the entire list of messages
        ms = ""
        for mes in self.messages:
            ms += mes.split("\"")[-2]
            ms+=" "
        return ms

    async def post_request(self, item: Item):

        message = queue.take().result()
        print(message)

        self.messages.append(item.json())

        return {"message": "Message added"}

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='A test program.')

    parser.add_argument("--port", help="Prints the supplied argument.", default="A random string.")

    args = parser.parse_args()


    ms_port = int(args.port)

    # ms_port = 8100
    localhost = "127.0.0.1"
    app = FastAPI()
    fcd_cntrllr = MessagesController()
    app.include_router(fcd_cntrllr.router)
    uvicorn.run(app, host=localhost, port=ms_port)
