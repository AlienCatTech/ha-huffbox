from pathlib import Path

from homeassistant.core import HomeAssistant


class HuffBoxMediaManager:
    def __init__(self, hass: HomeAssistant, directory: str | Path) -> None:
        self.hass = hass
        self.directory = Path(directory)

    def _list_files(self) -> list[Path]:
        """List all files in the directory."""
        return [file for file in self.directory.iterdir() if file.is_file()]

    async def list_files(self) -> list[Path]:
        """List all files in the directory."""
        return await self.hass.async_add_executor_job(self._list_files)

    def _get_file(self, filename: str) -> bytes:
        """Get the contents of a file."""
        file_path = self.directory / filename
        if file_path.exists() and file_path.is_file():
            with file_path.open("rb") as file:
                return file.read()
        else:
            msg = f"File '{filename}' not found in {self.directory}"
            raise FileNotFoundError(msg)

    async def get_file(self, filename: str) -> bytes:
        """List all files in the directory."""
        return await self.hass.async_add_executor_job(self._get_file, filename)
