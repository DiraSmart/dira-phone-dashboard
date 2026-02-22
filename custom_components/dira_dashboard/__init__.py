import logging
import os
import shutil

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .load_dashboard import load_dashboard

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})

    # Install theme to /config/themes/
    await hass.async_add_executor_job(_install_theme, hass)

    # Register the dashboard panel
    load_dashboard(hass, config_entry)

    _LOGGER.info("Dira Dashboard loaded successfully")
    return True


async def async_remove_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    # Remove dashboard panel
    try:
        hass.data["lovelace"].dashboards.pop("dira-dashboard", None)
    except Exception:
        pass

    # Remove from frontend panels
    try:
        hass.components.frontend.async_remove_panel("dira-dashboard")
    except Exception:
        pass

    _LOGGER.info("Dira Dashboard removed")
    return True


def _install_theme(hass: HomeAssistant):
    """Copy theme file to HA themes directory."""
    themes_dir = hass.config.path("themes")
    os.makedirs(themes_dir, exist_ok=True)

    source = os.path.join(
        os.path.dirname(__file__), "themes", "dira-glass.yaml"
    )
    dest = os.path.join(themes_dir, "dira-glass.yaml")

    if os.path.exists(source):
        shutil.copy2(source, dest)
        _LOGGER.info("Dira Glass theme installed to %s", dest)
