"""Bottleneck router alias."""

from fastapi import APIRouter
from shadowline.api.routers.predictions import get_bottleneck_forecast, get_bottleneck_history

router = APIRouter(prefix="/api/bottleneck", tags=["Bottleneck"])

router.add_api_route("", get_bottleneck_forecast, methods=["GET"])
router.add_api_route("/history", get_bottleneck_history, methods=["GET"])
