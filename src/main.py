from pathlib import Path
import uvicorn
from core.application import reg_app

app = reg_app()


if __name__ == "__main__":
    try:
        config = uvicorn.Config(app=f"{Path(__file__).stem}:app")
        server = uvicorn.Server(config)
        server.run()
    except Exception as e:
        raise e
