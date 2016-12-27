"""
Lighting 1
==========

"""

from rfxcom.protocol.base import BasePacketHandler
from rfxcom.protocol.rfxpacketutils import RfxPacketUtils

HOUSE_CODES = {
    0x41: "A",
    0x42: "B",
    0x43: "C",
    0x44: "D",
    0x45: "E",
    0x46: "F",
    0x47: "G",
    0x48: "H",
    0x49: "I",
    0x4A: "J",
    0x4B: "K",
    0x4C: "L",
    0x4D: "M",
    0x4E: "N",
    0x4F: "O",
    0x50: "P"
}

SUBTYPE_COMMANDS = {
    0x00: {
        0x00: "Off",
        0x01: "On",
        0x02: "Dim",
        0x03: "Bright",
        0x05: "All/Group Off",
        0x06: "All/Group On",
        0x07: "Chime",
        0xFF: "Illegal cmnd received"
    }
}


class Lighting1(BasePacketHandler):
    """The Lighting1 protocol is a 8 bytes packet used by a number of lighting
    systems. For example Lightwave devices use this protocol.

    ====    ====
    Byte    Meaning
    ====    ====
    0       Packet Length, 0x0C (excludes this byte)
    1       Packet Type, 0x10
    2       Packet SubType
    3       Sequence Number
    4       House Code
    5       Unit Code
    6       Command
    7       RSSI and Filler
    ====    ====
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.PACKET_TYPES = {
            0x10: "Lighting1 sensors"
        }

        self.PACKET_SUBTYPES = {
            0x00: "X10 Lightning",
            0x01: "ARC",
            0x02: "ELRO AB400D (Flamingo)",
            0x03: "Waveman",
            0x04: "Chacon EMW200",
            0x05: "IMPULS",
            0x06: "RisingSun",
            0x07: "Philips SBC",
            0x08: "Energenie ENER010",
            0x09: "Energenie 5-gang",
            0x0A: "COCO GDR2-2000R"
        }

    def parse(self, data):
        """Parse a 8 bytes packet in the Lighting1 format and return a
        dictionary containing the data extracted. An example of a return value
        would be:

        .. code-block:: python

            {
                'packet_length': 8,
                'packet_type': 16,
                'packet_type_name': 'Lighting1 sensors',
                'sequence_number': 2,
                'packet_subtype': 1,
                'packet_subtype_name': "ARC",
                'house_code': "A",
                'unit_code': 2,
                'command': 1,
                'command_text': "On",
                'signal_level': 9,
            }

        :param data: bytearray to be parsed
        :type data: bytearray

        :return: Data dictionary containing the parsed values
        :rtype: dict
        """

        self.validate_packet(data)

        results = self.parse_header_part(data)
        sub_type = results['packet_subtype']

        house_code = HOUSE_CODES.get(data[4])
        unit_code = data[5]
        command = data[6]
        command_text = SUBTYPE_COMMANDS.get(sub_type, {}).get(command)
        id_ = house_code + str(unit_code)

        sensor_specific = {
            'id': id_,
            'house_code': house_code,
            'unit_code': unit_code,
            'command': command,
            'command_text': command_text,
        }

        results.update(RfxPacketUtils.parse_signal_upper(data[7]))
        results.update(sensor_specific)

        return results
