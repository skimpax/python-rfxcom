from unittest import TestCase

from rfxcom.protocol.lighting6 import Lighting6

from rfxcom.exceptions import (InvalidPacketLength, UnknownPacketSubtype,
                               UnknownPacketType)


class Lighting6TestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x0B\x15\x00\x05\x01\x02\x03\x01\x02\x05\x06\x40')
        self.parser = Lighting6()

    def test_parse_frame(self):

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'packet_length': 11,
            'packet_type': 21,
            'packet_type_name': "Lighting6 sensors",
            'packet_subtype': 0,
            'packet_subtype_name': "Blyss",
            'sequence_number': 5,
            'id': 1024,
            'group_code': 3,
            'unit_code': 1,
            'command': 2,
            'command_seqnr': 5,
            'rfu': 6,
            'signal_level': 4
        })

        self.assertEquals(str(self.parser), "<Lighting6 ID:1024>")

    def test_validate_bytes_short(self):

        data = self.data[:1]

        with self.assertRaises(InvalidPacketLength):
            self.parser.validate_packet(data)

    def test_validate_unkown_packet_type(self):

        self.data[1] = 0xFF

        self.assertFalse(self.parser.can_handle(self.data))

        with self.assertRaises(UnknownPacketType):
            self.parser.validate_packet(self.data)

    def test_validate_unknown_sub_type(self):

        self.data[2] = 0xFF

        self.assertFalse(self.parser.can_handle(self.data))

        with self.assertRaises(UnknownPacketSubtype):
            self.parser.validate_packet(self.data)

    def test_log_namer(self):

        self.assertEquals(self.parser.log.name, 'rfxcom.protocol.Lighting6')
