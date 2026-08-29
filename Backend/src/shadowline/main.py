"""ShadowLine service entry point."""

import uvicorn
from shadowline.config.settings import ShadowLineSettings


def main():
    settings = ShadowLineSettings()
    uvicorn.run(
        "shadowline.api.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=False,
    )


if __name__ == "__main__":
    main()
