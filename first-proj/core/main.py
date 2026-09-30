from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

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


@app.post("/names")
def create_name(name: str):
    new_name = {"id": names[-1]["id"] + 1, "name": name}
    names.append(new_name)
    return new_name


@app.get("/names/{id}")
async def get_name_detail(id: int):
    for i in names:
        if i["id"] == id:
            return i
    raise HTTPException(status_code=404, detail="Object not found")


@app.put("/names/{id}")
def update_name(id: int, new_name: str):
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
