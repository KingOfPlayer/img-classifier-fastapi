import uvicorn
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    if "code" in os.getcwd():
        uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug",
                    proxy_headers=True, reload=True)
    else:
        # for running locally from IDE without docker
        uvicorn.run("app.app:app", host="0.0.0.0", port=8000, log_level="debug",
                    proxy_headers=True, reload=True)