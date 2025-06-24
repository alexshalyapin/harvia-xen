from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE
from .constants import DOMAIN, STORAGE_KEY, STORAGE_VERSION, REGION,_LOGGER

class HarviaHumiditySensor(SensorEntity):
    """Представление датчика влажности."""

    def __init__(self, device, name, sauna):
        """Инициализация датчика влажности."""
        self._name = name + ' Humidity'
        self._state = None
        self._device = device
        self._device_id = device.id + '_humidity_sensor'
        self._sauna = sauna
        self._attr_unique_id = device.id + '_humidity_sensor'
        self._attr_icon = 'mdi:water-percent'

    @property
    def name(self):
        """Верните имя датчика."""
        return self._name

    @property
    def state(self):
        """Return de staat van de sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Верните использованную единицу."""
        return PERCENTAGE

    async def async_added_to_hass(self):
        """Действия, которые необходимо выполнить при добавлении объекта в HA."""
        self._device.humiditySensor = self
        await self._device.update_ha_devices()

    async def update_state(self):
        self.async_write_ha_state()


    #@property
    #def device_info(self):
    #    """Возврат информации о подключенном устройстве."""
    #    return {
    #        "identifiers": {(DOMAIN, self._device.id)},
    #        "name": self._device.name,
    #        "manufacturer": "Harvia",
    #    }

async def async_setup_entry(hass, entry, async_add_entities):
    """Настройка датчиков de Harvia."""
    devices = await hass.data[DOMAIN]['api'].get_devices()
    all_sensors = []  # Используйте другую переменную, чтобы избежать путаницы.

    for device in devices:
        _LOGGER.debug(f"Loading sensors for device: {device.name}")
        device_sensors = await device.get_sensors()  # Получить датчики для текущего устройства
        all_sensors.extend(device_sensors)  # Добавьте полученные датчики в список

    async_add_entities(all_sensors, True)
