"""
Lighting 3
==========

"""

from rfxcom.protocol.base import BasePacketHandler
from rfxcom.protocol.rfxpacketutils import RfxPacketUtils


COMMANDS = {
    0x00: 'Bright',
    0x08: 'Dim',
    0x10: 'On',
    0x11: 'Level 1',
    0x12: 'Level 2',
    0x13: 'Level 3',
    0x14: 'Level 4',
    0x15: 'Level 5',
    0x16: 'Level 6',
    0x17: 'Level 7',
    0x18: 'Level 8',
    0x19: 'Level 9',
    0x1a: 'Off',
    0x1c: 'Program',
}

class Lighting4(BasePacketHandler):
    """The Lighting4 protocol is a 9 bytes packet used by a number of lighting
    systems. For example Lightwave devices use this protocol.

    ====    ====
    Byte    Meaning
    ====    ====
    0       Packet Length, 0x0C (excludes this byte)
    1       Packet Type, 0x12
    2       Sub Type
    3       Sequence Number
    4       System
    5       Channel 1
    6       Channel 2
    7       Command
    8       RSSI and Filler
    ====    ====
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.PACKET_TYPES = {
            0x13: "Lighting4 sensors"
        }

        self.PACKET_SUBTYPES = {
            0x00: 'PT2262',
        }

    def parse(self, data):
        """Parse a 10 bytes packet in the Lighting4 format and return a
        dictionary containing the data extracted. An example of a return value
        would be:

        .. code-block:: python

            {
                'packet_length': 9,
                'packet_type': 19,
                'packet_type_name': 'Lighting4 sensors',
                'sequence_number': 4,
                'packet_subtype': 0,
                'packet_subtype_name': "PT2262",
                'command': 17,
                'command_text': "Level 1",
                'pulse': 5
            }

        :param data: bytearray to be parsed
        :type data: bytearray

        :return: Data dictionary containing the parsed values
        :rtype: dict
        """

        self.validate_packet(data)

        results = self.parse_header_part(data)
        sub_type = results['packet_subtype']

        cmd = (data[4] << 16) + (data[5] << 8) + data[6]
        pulse = data[7] << 8 + data[8]

        sensor_specific = {
            'command': cmd,
            'pulse': pulse
        }

        results.update(RfxPacketUtils.parse_signal_upper(data[9]))
        results.update(sensor_specific)

        return results
