from fastapi import FastAPI

app = FastAPI(title="MeetMap API")


@app.get("/health")
def health_check():
    return {"status": "ok"}