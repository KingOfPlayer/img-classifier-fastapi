import uvicorn
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
        uvicorn.run("app.app:app", host="0.0.0.0", port=7001, log_level="debug",
                    proxy_headers=True, reload=True)