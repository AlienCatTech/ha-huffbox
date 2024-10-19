from urllib.parse import urljoin

from aiohttp import BodyPartReader, ClientSession
from aiohttp.web import Request, Response
from homeassistant.core import HomeAssistant
from homeassistant.helpers.http import HomeAssistantView

from custom_components.huffbox.const import LOGGER
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


MAX_SIZE = 1024**4


class HuffBoxProxyView(HomeAssistantView):
    url = "/api/huffbox/proxy/{p:.*}"
    name = "api:huffbox:proxy"
    requires_auth = False

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the view."""
        self.hass = hass

    async def _proxy(self, request: Request) -> Response:
        # Extract the IP and path from the request
        self.hass.http.app._client_max_size = MAX_SIZE  # noqa: SLF001
        parts = request.path.split("/api/huffbox/proxy/", 1)
        part_num = 2
        if len(parts) != part_num:
            return Response(text="Invalid proxy request", status=400)

        ip_and_path = parts[1]
        ip, *path_parts = ip_and_path.split("/", 1)
        path = path_parts[0] if path_parts else ""
        LOGGER.info(path)
        # Construct the URL
        url = f"http://{ip}"
        if path and path != "index":
            url = urljoin(url, path)

        # Add query parameters if present
        if request.query_string:
            url += f"?{request.query_string}"
        LOGGER.info(url)

        async with ClientSession() as session:
            response = await session.request(
                request.method,
                url,
                headers=request.headers,
                data=await request.read(),
            )

            headers = {
                k: v
                for k, v in response.headers.items()
                if k.lower() != "content-encoding"
            }

            body = await response.read()

            return Response(body=body, status=response.status, headers=headers)

    async def get(self, request: Request, p: str) -> Response:  # noqa: ARG002
        return await self._proxy(request)

    async def post(self, request: Request, p: str) -> Response:  # noqa: ARG002
        return await self._proxy(request)

    async def put(self, request: Request, p: str) -> Response:  # noqa: ARG002
        return await self._proxy(request)

    async def patch(self, request: Request, p: str) -> Response:  # noqa: ARG002
        return await self._proxy(request)

    async def delete(self, request: Request, p: str) -> Response:  # noqa: ARG002
        return await self._proxy(request)
