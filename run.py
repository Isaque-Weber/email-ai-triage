import uvicorn
import os
import sys

if __name__ == "__main__":
    # Garante imports absolutos (PyCharm)
    sys.path.append(os.getcwd())

    debug = os.getenv("DEBUG", "true").lower() == "true"

    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=int(os.getenv("PORT", 8000)),
        reload=debug,
        log_level="debug" if debug else "info"
    )
