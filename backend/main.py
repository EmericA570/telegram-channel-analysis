import os

import uvicorn

if __name__ == "__main__":
    if not os.path.isdir("./query"):
        os.mkdir("./query")

    uvicorn.run(app="api:app", reload=True)
