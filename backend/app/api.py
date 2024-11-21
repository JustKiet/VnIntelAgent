from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .auth import routes
from writer_agent.graphs.seo_content_writer import AutomatedSEOContentWriterGraph
from writer_agent.schemas.config import UserConfig
from fastapi.responses import JSONResponse, StreamingResponse
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime
from dotenv import load_dotenv
from bson import ObjectId
import certifi
import json

ca = certifi.where()

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE_NAME = os.getenv("MONGODB_DATABASE_NAME")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[MONGODB_DATABASE_NAME]

app = FastAPI()
app.include_router(routes.router)

origins = [
    "http://localhost:3000", "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

async def run_seo_content_generation(task_id: str, data: UserConfig):
    graph_obj = AutomatedSEOContentWriterGraph(
        user_config=data,
        config={"configurable": {"thread_id": "my-thread"}}
    )

    graph_init = graph_obj._graph

    progress = 0
 
    async for chunk in graph_init.astream(
        {
            "config": graph_obj.user_config
        },
        config=graph_obj.config,
        stream_mode="updates"
    ):
        for node, _ in chunk.items():
            progress += (100 / (len(graph_init.nodes.keys()) - 1))
            data_dict = {
                "node": str(node),
                "progress": round(progress, 2)
            }
            yield f"data: {json.dumps(data_dict)}\n\n"
            
    checkpoint = graph_init.get_state(graph_obj.config)
    print(checkpoint.values)
    article = checkpoint.values["article"]
    keywords = checkpoint.values["keywords"].model_dump()
    description = checkpoint.values["description"]

    article_dict = {
        "article": article
    }

    yield f"data: {json.dumps(article_dict)}\n\n"
    
    await db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {
            "$set": {
                "status": "completed",
                "article": article,
                "description": description,
                "keywords": keywords,
                "end_time": datetime.now()
            }
        }
    )


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}


@app.post("/generate-seo-content", tags=["seo-content"])
async def generate_seo_content_endpoint(data: UserConfig) -> dict:
    task_id = str(ObjectId())
    
    await db.tasks.insert_one(
        {
            "_id": ObjectId(task_id),
            "user_id": data.user_id,
            "status": "in-progress",
            "config": data.model_dump(),
            "type": "seo-content",
            "article": None,
            "description": None,
            "keywords": None,
            "start_time": datetime.now(),
            "end_time": None,
        }
    )

    return {"task_id": task_id}


@app.get("/stream-seo-content", tags=["seo-content"])
async def stream_seo_content(task_id: str) -> StreamingResponse:
    task = await db.tasks.find_one({"_id": ObjectId(task_id)})

    if task is None:
        return JSONResponse(status_code=404, content={"message": "Task not found."})

    if task["status"] == "in-progress":
        return StreamingResponse(run_seo_content_generation(task_id=task_id, data=task["config"]), media_type="text/event-stream")
    
    if task["status"] == "completed":
        return JSONResponse(status_code=200, content={"message": "Task already completed."})
    

@app.get("/get-seo-content", tags=["seo-content"])
async def get_seo_content(task_id: str) -> dict:

    task = await db.tasks.find_one({"_id": ObjectId(task_id)})

    if task is None:
        return JSONResponse(status_code=404, content={"message": "Task not found."})
    
    task["_id"] = str(task["_id"])

    return task