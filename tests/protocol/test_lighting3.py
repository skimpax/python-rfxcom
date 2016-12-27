from unittest import TestCase

from rfxcom.protocol.lighting3 import Lighting3

from rfxcom.exceptions import (InvalidPacketLength, UnknownPacketSubtype,
                               UnknownPacketType)


class Lighting3TestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x08\x12\x00\x05\x02\x00\x09\x11\x40')
        self.parser = Lighting3()

    def test_parse_frame(self):

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'packet_length': 8,
            'packet_type': 18,
            'packet_type_name': "Lighting3 sensors",
            'packet_subtype': 0,
            'packet_subtype_name': "Ikea Koppla",
            'sequence_number': 5,
            'system': 2,
            'channel': 9,
            'command': 17,
            'command_text': "Level 1",
            'signal_level': 4
        })

        self.assertEquals(str(self.parser), "<Lighting3 ID:None>")

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

        self.assertEquals(self.parser.log.name, 'rfxcom.protocol.Lighting3')
