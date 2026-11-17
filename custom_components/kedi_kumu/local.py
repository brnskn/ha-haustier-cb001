"""Local (LAN) access to the litter box over the Tuya protocol.

The Tuya cloud schema of the Haustier CB001 only lists a few data points.
Settings such as the deodorizer timer, child lock or "add litter" live on data
points the cloud schema does not describe, so Home Assistant cannot read or
change them. The device speaks the Tuya LAN protocol (3.5), and the Tuya
integration already holds its local key, so we can read every data point and
write the ones we know. Connections are short-lived (connect, request, close)
so the official app keeps working.

The local key never leaves this module: it is read from the Tuya integration
on demand and is not logged or exposed.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)

DISCOVERY_SECONDS = 18
SOCKET_TIMEOUT = 5


class LocalError(RuntimeError):
    """Local access failed."""


class LocalBox:
    """Short-lived local connections to one Tuya device."""

    def __init__(self, hass: HomeAssistant, device_id: str, key_fn: Callable[[], str | None]) -> None:
        self.hass = hass
        self.device_id = device_id
        self._key_fn = key_fn
        self.ip: str | None = None
        self.version: float | None = None
        self.dps: dict[str, Any] = {}
        self.updated: str | None = None
        self.error: str | None = None
        self._lock = asyncio.Lock()

    def info(self) -> dict[str, Any]:
        return {
            "ip": self.ip,
            "version": self.version,
            "updated": self.updated,
            "error": self.error,
            "dps": self.dps,
        }

    async def async_discover(self) -> str | None:
        def _find() -> dict[str, Any] | None:
            import tinytuya  # noqa: PLC0415 - heavy import, only when used

            return tinytuya.find_device(dev_id=self.device_id)

        result = await self.hass.async_add_executor_job(_find)
        if isinstance(result, dict) and result.get("ip"):
            self.ip = str(result["ip"])
            try:
                self.version = float(result.get("version") or 3.5)
            except (TypeError, ValueError):
                self.version = 3.5
            _LOGGER.info("Found litter box on the LAN at %s (protocol %s)", self.ip, self.version)
        return self.ip

    def _device(self):
        import tinytuya  # noqa: PLC0415

        key = self._key_fn()
        if not key:
            raise LocalError("local key not available yet")
        device = tinytuya.Device(self.device_id, self.ip, key, version=self.version)
        device.set_socketTimeout(SOCKET_TIMEOUT)
        device.set_socketRetryLimit(1)
        return device

    async def _async_call(self, func: Callable[[Any], Any]) -> Any:
        async with self._lock:
            if not self.ip:
                await self.async_discover()
            if not self.ip:
                self.error = "device not found on the LAN"
                raise LocalError(self.error)

            def _run() -> Any:
                device = self._device()
                try:
                    return func(device)
                finally:
                    device.close()

            result = await self.hass.async_add_executor_job(_run)
            if isinstance(result, dict) and result.get("Error"):
                self.error = str(result.get("Error"))
                if "network" in self.error.lower() or "connect" in self.error.lower():
                    self.ip = None  # rediscover next time, the IP may have changed
                raise LocalError(self.error)
            self.error = None
            return result

    async def async_status(self) -> dict[str, Any]:
        result = await self._async_call(lambda d: d.status())
        dps = result.get("dps") if isinstance(result, dict) else None
        if not isinstance(dps, dict):
            raise LocalError("no data points in the reply")
        self.dps = {str(k): v for k, v in dps.items()}
        self.updated = dt_util.utcnow().isoformat()
        return self.dps

    async def async_set(self, dp: int | str, value: Any) -> dict[str, Any]:
        result = await self._async_call(lambda d: d.set_value(int(dp), value))
        dps = result.get("dps") if isinstance(result, dict) else None
        if isinstance(dps, dict):
            self.dps.update({str(k): v for k, v in dps.items()})
            self.updated = dt_util.utcnow().isoformat()
        return self.dps
