from fastapi import FastAPI, HTTPException, Body
import uvicorn
from schemas import (
    AmountCreationSchema,
    AmountCreationResponseSchema,
)

app = FastAPI()

data = [{"id": 1, "description": "", "amount": 100.2}]


@app.get("/get-data", response_model=list[AmountCreationResponseSchema])
def get_data():
    return data


@app.get("/get-data/{id}", response_model=AmountCreationResponseSchema)
def get_single_data(id: int):
    for i in data:
        if i["id"] == id:
            return i
    raise HTTPException(status_code=404, detail="Object not found")


@app.post("/add-data")
def create_data(input: AmountCreationSchema):
    new_data = {
        "id": data[-1]["id"] + 1,
        "description": input.description,
        "amount": input.amount,
    }
    data.append(new_data)
    return {"detail": "added"}


@app.put("/edit-data/{id}")
def edit_data(id: int, input: AmountCreationSchema):
    for i in data:
        if i["id"] == id:
            i["amount"] = input.amount
            i["description"] = input.description
            return {"detail": "updated"}
    raise HTTPException(status_code=404, detail="Object not found")


@app.delete("/delete-data/{id}")
def delete_data(id: int):
    for i in data:
        if i["id"] == id:
            data.remove(i)
            return {"detail": "deleted"}
    raise HTTPException(status_code=404, detail="Object not found")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
