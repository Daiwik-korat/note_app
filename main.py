from fastapi import FastAPI
from pydantic import BaseModel, Field
from database import notes_collection
from fastapi import HTTPException
from bson import ObjectId

app = FastAPI()

class Note(BaseModel):
    title: str = Field(..., max_length=20, min_length=3, description="Title of your todo buddy")
    content: str | None = Field(None, max_length=50, min_length=10, description="Description of your todo snippet")

def serialize_note(note) -> dict:
    return {
        "id": str(note["_id"]),
        "title": note["title"],
        "content": note.get("content")
    }

class NoteUpdate(BaseModel):
    title: str = Field(None, max_length=20, min_length=3)
    content: str | None = Field(None, max_length=50, min_length=10)

@app.get("/notes")
async def notes_details():
    try:
        notes = []
        async for note in notes_collection.find():
            notes.append(serialize_note(note))
        return notes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/add")
async def notes_entry(note: Note):
    try:
        result = await notes_collection.insert_one(note.dict())
        return {"id": str(result.inserted_id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/notes/{id}")
async def update_note(id: str, note: Note):
    try:
        result = await notes_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": note.dict()}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Note not found")

        return {"message": "Note updated successfully"}

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.patch("/update/{id}")
async def update_note_patch(id: str, note:NoteUpdate):
    try:
        update_record = note.dict(exclude_unset=True)

        if update_record is None:
            raise HTTPException(status_code=400, detail="NO DATA FOUND DUMBOO")

        result = await notes_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_record}
        )

        return {"message": "Record updated"}

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
