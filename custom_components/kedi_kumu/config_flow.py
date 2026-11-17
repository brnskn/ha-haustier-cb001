"""Config flow for Kedi Kumu."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigEntryState,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_MIN_MANUAL,
    CONF_NOTIFY,
    CONF_TUYA_DEVICE_ID,
    DEFAULT_MIN_MANUAL,
    DOMAIN,
)

LITTER_CATEGORY = "msp"


def _litter_boxes(hass: HomeAssistant) -> dict[str, str]:
    boxes: dict[str, str] = {}
    for entry in hass.config_entries.async_entries("tuya"):
        if entry.state is not ConfigEntryState.LOADED:
            continue
        manager = getattr(getattr(entry, "runtime_data", None), "manager", None)
        if manager is None:
            continue
        for dev_id, device in manager.device_map.items():
            if getattr(device, "category", None) == LITTER_CATEGORY:
                boxes[dev_id] = getattr(device, "name", dev_id)
    return boxes


class KediKumuConfigFlow(ConfigFlow, domain=DOMAIN):
    """Set up a litter box."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        boxes = _litter_boxes(self.hass)
        if not boxes:
            return self.async_abort(reason="no_devices")
        if user_input is not None:
            dev_id = user_input[CONF_TUYA_DEVICE_ID]
            await self.async_set_unique_id(dev_id)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title="Kedi Kumu",
                data={CONF_TUYA_DEVICE_ID: dev_id},
                options={CONF_MIN_MANUAL: DEFAULT_MIN_MANUAL, CONF_NOTIFY: []},
            )
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_TUYA_DEVICE_ID, default=next(iter(boxes))): SelectSelector(
                        SelectSelectorConfig(
                            options=[SelectOptionDict(value=k, label=v) for k, v in boxes.items()],
                            mode=SelectSelectorMode.LIST,
                        )
                    )
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        return KediKumuOptionsFlow()


class KediKumuOptionsFlow(OptionsFlow):
    """Notifications and learning settings."""

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            user_input[CONF_MIN_MANUAL] = int(user_input[CONF_MIN_MANUAL])
            return self.async_create_entry(data=user_input)
        services = sorted(
            s for s in self.hass.services.async_services_for_domain("notify") if s.startswith("mobile_app_")
        )
        options = self.config_entry.options
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_NOTIFY, default=options.get(CONF_NOTIFY, [])): SelectSelector(
                        SelectSelectorConfig(options=services, multiple=True, mode=SelectSelectorMode.LIST)
                    ),
                    vol.Required(
                        CONF_MIN_MANUAL, default=options.get(CONF_MIN_MANUAL, DEFAULT_MIN_MANUAL)
                    ): NumberSelector(NumberSelectorConfig(min=1, max=10, step=1, mode=NumberSelectorMode.BOX)),
                }
            ),
        )
