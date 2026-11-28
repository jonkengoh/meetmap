from fastapi import FastAPI

from app.rooms.router import router as rooms_router


app = FastAPI(title="MeetMap API")

app.include_router(rooms_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}