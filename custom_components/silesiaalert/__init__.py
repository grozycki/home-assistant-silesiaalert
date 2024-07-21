"""The Silesia Alert integration."""

from __future__ import annotations

import logging

from homeassistant import config_entries, core
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_state_change_event

from custom_components.silesiaalert.api import SilesiaAlertApi
from custom_components.silesiaalert.coordinator import SilesiaAlertCoordinator
from custom_components.silesiaalert.http_client import HttpClient

PLATFORMS: list[Platform] = [
    Platform.SENSOR
]

_LOGGER = logging.getLogger(__name__)

DOMAIN = "silesiaalert"


async def async_setup(hass, config):
    hass.states.async_set("hello_state.world", "Paulus")
    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    logger = _LOGGER
    http_client = HttpClient(logger=logger)
    api = SilesiaAlertApi(
        http_client=http_client,
        logger=logger
    )
    silesia_alert_coordinator = SilesiaAlertCoordinator(
        hass=hass,
        api=api,
        logger=logger
    )

    await silesia_alert_coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][config_entry.entry_id] = silesia_alert_coordinator

    return True