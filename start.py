import uvicorn

if __name__ == "__main__":

    uvicorn.run("trashCard:app", host='0.0.0.0', port=11451)
