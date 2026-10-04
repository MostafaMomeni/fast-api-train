from fastapi import FastAPI, HTTPException, Form, Body, UploadFile, File
from fastapi.responses import JSONResponse
import uvicorn
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from dataclasses import dataclass

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("start application")

    yield

    print("shut down application")


app = FastAPI(lifespan=lifespan)


names = [
    {"id": 1, "name": "Mostafa"},
    {"id": 2, "name": "Fatemeh"},
    {"id": 3, "name": "Sara"},
    {"id": 4, "name": "Mohammad"},
    {"id": 5, "name": "Ali"},
    {"id": 6, "name": "Reza"},
    {"id": 7, "name": "Mohsen"},
]


@app.get("/")
async def root():
    return JSONResponse(content={"message": "Hello World"})


@app.get("/names")
async def get_names():
    return names

@dataclass
class Student:
    name:str

@dataclass
class StudentResponse:
    id:int
    name:str


@app.post("/names" ,  status_code=201 , response_model=StudentResponse)
def create_name(student: Student ):
    new_name = {"id": names[-1]["id"] + 1, "name": student.name}
    names.append(new_name)
    return new_name


@app.get("/names/{id}")
async def get_name_detail(id: int):
    for i in names:
        if i["id"] == id:
            return i
    raise HTTPException(status_code=404, detail="Object not found")


@app.put("/names/{id}")
def update_name(id: int, new_name: str = Form()):
    for i in names:
        if i["id"] == id:
            i["name"] = new_name
            return {"message": "Done"}
    raise HTTPException(status_code=404, detail="Object not found")


@app.delete("/names/{id}")
def delete_name(id: int):
    for i in names:
        if i["id"] == id:
            names.remove(i)
            return {"message": "Done"}
    raise HTTPException(status_code=404, detail="Object not found")


@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    return {
        "fileName": file.filename,
        "content-type": file.content_type,
        "file-size": len(content),
    }


@app.post("/upload-multiple-file/")
async def upload_multiple_file(
    files: list[UploadFile] = File(...)
):
    return [
        {
            "fileName": file.filename,
            "contentType": file.content_type
        }
        for file in files
    ]

# for multiple file upload need this code 
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )

    # پیدا کردن schema مربوط به آپلود چند فایل
    body_schema = openapi_schema["components"]["schemas"].get(
        "Body_upload_multiple_file_upload_multiple_file__post"
    )

    if body_schema:
        files_schema = body_schema["properties"].get("files")

        if files_schema:
            # تبدیل schema فایل از contentMediaType به binary
            if "items" in files_schema:
                files_schema["items"] = {
                    "type": "string",
                    "format": "binary"
                }

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
