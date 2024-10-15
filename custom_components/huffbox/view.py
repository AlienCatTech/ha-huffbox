from aiohttp import BodyPartReader
from aiohttp.web import Request, Response
from homeassistant.core import HomeAssistant
from homeassistant.helpers.http import HomeAssistantView

from custom_components.huffbox.media import HuffBoxMediaManager


class HuffBoxUploadView(HomeAssistantView):
    url = "/api/huffbox/upload"
    name = "api:huffbox:upload"
    requires_auth = True

    def __init__(self, hass: HomeAssistant, media_manager: HuffBoxMediaManager) -> None:
        """Initialize the view."""
        self.hass = hass
        self.media_manager = media_manager

    async def post(self, request: Request) -> Response:
        reader = await request.multipart()
        field = await reader.next()

        if field and isinstance(field, BodyPartReader):
            filename = field.filename
            if filename:
                content = await field.read()

                await self.media_manager.save_file(filename, content)
                return self.json({"message": f"File saved: { filename}"})
            return self.json({"error": "File faield to save: filename not found"}, 400)
        return self.json({"error": "File faield to save"}, 400)


class HuffBoxDownloadView(HomeAssistantView):
    url = "/api/huffbox/download/{file_name}"
    name = "api:huffbox:download"
    requires_auth = True

    def __init__(self, hass: HomeAssistant, media_manager: HuffBoxMediaManager) -> None:
        """Initialize the view."""
        self.hass = hass
        self.media_manager = media_manager

    async def get(self, _: Request, file_name: str) -> Response:
        try:
            file = await self.media_manager.get_file(file_name)
            return Response(body=file, headers={"Content-Type": "application/json"})
        except Exception as e:
            return self.json({"error": f"File faield to get: {e}"}, 400)
