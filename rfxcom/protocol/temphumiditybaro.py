"""
Temperature and Humidity and Barometric sensors
===============================================

"""

from rfxcom.protocol.base import BasePacketHandler
from rfxcom.protocol.rfxpacketutils import RfxPacketUtils


class TempHumidityBaro(BasePacketHandler):
    """
    ====    ====
    Byte    Meaning
    ====    ====
    0       Packet Length, 0x0D (excludes this byte)
    1       Packet Type, 0x54
    2       Sub Type
    3       Sequence Number
    4       ID 1
    5       ID 2
    6       Temperature High (7 bits), Temperature sign (1 bit)
    7       Temperature Low
    8       Humidity
    9       Humidity Status
    10      RSSI and Battery Level
    ====    ====


    """
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.PACKET_TYPES = {
            0x54: "Temperature and humidity and barometric sensors"
        }
        self.PACKET_SUBTYPES = {
            0x01: 'BTHR918',
            0x02: 'BTHR918N, BTHR968',
        }

    def parse(self, data):
        """Parse a 14 bytes packet in the TemperatureHumidity format and return a
        dictionary containing the data extracted. An example of a return value
        would be:

        .. code-block:: python

            {
                'id': "0x2EB2",
                'packet_length': 13,
                'packet_type': 84,
                'packet_type_name': 'Temperature and humidity and barometric \
                 sensors',
                'sequence_number': 0,
                'packet_subtype': 1,
                'packet_subtype_name': "BTHR918",
                'temperature': 21.3,
                'humidity': 91,
                'humidity_status': "Wet"
                'signal_level': 9,
                'battery_level': 6,
            }

        :param data: bytearray to be parsed
        :type data: bytearray

        :return: Data dictionary containing the parsed values
        :rtype: dict
        """

        self.validate_packet(data)

        id_ = self.dump_hex(data[4:6])
        temperature = ((data[6] & 0x7f) * 256 + data[7]) / 10
        signbit = data[6] & 0x80
        if signbit != 0:
            temperature = -temperature
        humidity = data[8]
        humidity_status = self._extract_humidity_status(data[9])
        baro = data[10] * 256 + data[11]
        forecast = data[12]
        forecast_status = self._extract_forecast(forecast)

        sensor_specific = {
            'id': id_,
            'temperature': temperature,
            'humidity': humidity,
            'humidity_status': humidity_status,
            'barometry': baro,
            'forecast': forecast,
            'forecast_status': forecast_status,
        }

        results = self.parse_header_part(data)
        results.update(RfxPacketUtils.parse_signal_and_battery(data[13]))
        results.update(sensor_specific)

        return results

    def _extract_humidity_status(self, data):
        """Extract the humidity status.

        :param data: byte to be parsed
        :type data: byte

        :return: String containing the human readable status
        :rtype: string
        """
        if data == 0x00:
            return "Dry"
        elif data == 0x01:
            return "Comfort"
        elif data == 0x02:
            return "Normal"
        elif data == 0x03:
            return "Wet"
        else:
            return "--??--"

    def _extract_forecast(self, data):
        """Extract the forecast info.

        :param data: byte to be parsed
        :type data: byte

        :return: String containing the human readable forecast
        :rtype: string
        """
        if data == 0x00:
            return "No forecast available"
        elif data == 0x01:
            return "Sunny"
        elif data == 0x02:
            return "Partly cloudy"
        elif data == 0x03:
            return "Cloudy"
        elif data == 0x04:
            return "Rainy"
        else:
            return "--??--"
