"""
Lighting 3
==========

"""

from rfxcom.protocol.base import BasePacketHandler
from rfxcom.protocol.rfxpacketutils import RfxPacketUtils


COMMANDS = {
    0x00: 'On',
    0x01: 'Off',
    0x02: 'Group on',
    0x03: 'Group off',
}


class Lighting6(BasePacketHandler):
    """The Lighting6 protocol is a 12 bytes packet used by a number of lighting
    systems. For example Lightwave devices use this protocol.

    ====    ====
    Byte    Meaning
    ====    ====
    0       Packet Length, 0x0C (excludes this byte)
    1       Packet Type, 0x15
    2       Sub Type
    3       Sequence Number
    4       ID 1
    5       ID 2
    6       Group Code
    7       Unit Code
    8       Command
    9       Command Sequence Number
    10      RFU
    11      RSSI and Filler
    ====    ====
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.PACKET_TYPES = {
            0x15: "Lighting6 sensors"
        }

        self.PACKET_SUBTYPES = {
            0x00: 'Blyss',
        }

    def parse(self, data):
        """Parse a 10 bytes packet in the Lighting6 format and return a
        dictionary containing the data extracted. An example of a return value
        would be:

        .. code-block:: python

            {
                'packet_length': 9,
                'packet_type': 19,
                'packet_type_name': 'Lighting6 sensors',
                'sequence_number': 4,
                'packet_subtype': 0,
                'packet_subtype_name': "Blyss",
                'id': 1024,
                'group_code': 5,
                'unit_code': 2,
                'command': 3,
                'command_seqnr': 4,
                'rfu': 5,
                'signal_level': 6
            }

        :param data: bytearray to be parsed
        :type data: bytearray

        :return: Data dictionary containing the parsed values
        :rtype: dict
        """

        self.validate_packet(data)

        results = self.parse_header_part(data)

        id_ = self.dump_hex(data[4:6])
        group_code = data[6]
        unit_code = data[7]
        cmd = data[8]
        cmd_seqnr = data[9]
        rfu = data[10]

        sensor_specific = {
            'id': id_,
            'group_code': group_code,
            'unit_code': unit_code,
            'command': cmd,
            'command_seqnr': cmd_seqnr,
            'rfu': rfu
        }

        results.update(RfxPacketUtils.parse_signal_upper(data[11]))
        results.update(sensor_specific)

        return results
