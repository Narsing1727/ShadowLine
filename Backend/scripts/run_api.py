"""Run shadowline API service."""

import uvicorn
from shadowline.config.settings import ShadowLineSettings

if __name__ == "__main__":
    settings = ShadowLineSettings()
    uvicorn.run("shadowline.api.app:app", host=settings.api_host, port=settings.api_port, reload=False)
