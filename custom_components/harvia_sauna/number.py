from homeassistant.components.number import NumberEntity
from homeassistant.const import PERCENTAGE
from .constants import DOMAIN, STORAGE_KEY, STORAGE_VERSION, REGION,_LOGGER

class HarviaHumiditySetPoint(NumberEntity):
    """Представление числового объекта для установки желаемой влажности."""

    def __init__(self, device, name, sauna):
        """Инициализация заданного значения влажности."""
        self._name = name + ' Steamer Humidity'
        self._state = None
        self._device = device
        self._device_id = device.id + '_humidity_set_point'
        self._sauna = sauna
        self._attr_unique_id = device.id + '_humidity_set_point'
        self._attr_icon = 'mdi:cloud-percent'

    @property
    def name(self):
        """Верните имя сущности."""
        return self._name


    @property
    def min_value(self):
        """Возвращает минимальное значение влажности, которое можно установить.."""
        return 0  # Stel in op je minimum grenswaarde

    @property
    def max_value(self):
        """Возвращает максимальное значение влажности, которое можно установить.."""
        return 140  # Установите максимальное предельное значение( темп+влажность)

    @property
    def step(self):
        """Верните размер шага настройки влажности."""
        return 1.0

    @property
    def unit_of_measurement(self):
        """Верните единицу этой сущности."""
        return PERCENTAGE

    @property
    def value(self):
        """Верните текущее установленное значение."""
        return self._state

    async def async_added_to_hass(self):
        """Действия, которые необходимо выполнить при добавлении объекта в HA."""
        self._device.humidityNumber = self
        await self._device.update_ha_devices()

    async def update_state(self):
        self.async_write_ha_state()

    async def async_set_value(self, value):
        """Обновить установленное значение."""
        self._state = value
        await self._device.set_target_relative_humidity(value)
        self.async_write_ha_state()

async def async_setup_entry(hass, entry, async_add_entities):
    """Настройка номеров de Harvia."""
    devices = await hass.data[DOMAIN]['api'].get_devices()
    all_numbers = []  # Используйте другую переменную, чтобы избежать путаницы.

    for device in devices:
        _LOGGER.debug(f"Loading sensors for device: {device.name}")
        device_numbers = await device.get_numbers()  # Получить датчики для текущего устройства
        all_numbers.extend(device_numbers)  # Добавьте полученные датчики в список

    async_add_entities(all_numbers, True)
