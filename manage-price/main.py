from fastapi import FastAPI, HTTPException, Body
import uvicorn

app = FastAPI()

data = [{"id": 1, "description": "", "amount": 100.2}]


@app.get("/get-data")
def get_data():
    return data


@app.get("/get-data/{id}")
def get_single_data(id: int):
    for i in data:
        if i["id"] == id:
            return i
    raise HTTPException(status_code=404, detail="Object not found")


@app.post("/add-data")
def create_data(amount: float = Body(gt=0), description: str = Body()):
    new_data = {"id": data[-1]["id"] + 1, "description": description, "amount": amount}
    data.append(new_data)
    return {"detail": "added"}


@app.put("/edit-data")
def edit_data(id: int = Body(), amount: float = Body(gt=0), description: str = Body()):
    for i in data:
        if i["id"] == id:
            i["amount"] = amount
            i["description"] = description
            return {"detail": "updated"}
    raise HTTPException(status_code=404, detail="Object not found")


@app.delete("/delete-data/{id}")
def delete_data(id):
    for i in data:
        if i["id"] == id:
            data.remove(i)
            return {"detail": "deleted"}
    raise HTTPException(status_code=404, detail="Object not found")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
