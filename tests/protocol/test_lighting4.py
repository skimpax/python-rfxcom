from unittest import TestCase

from rfxcom.protocol.lighting4 import Lighting4

from rfxcom.exceptions import (InvalidPacketLength, UnknownPacketSubtype,
                               UnknownPacketType)


class Lighting4TestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x09\x13\x00\x05\x01\x02\x03\x01\x02\x40')
        self.parser = Lighting4()

    def test_parse_frame(self):

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'packet_length': 9,
            'packet_type': 19,
            'packet_type_name': "Lighting4 sensors",
            'packet_subtype': 0,
            'packet_subtype_name': "PT2262",
            'sequence_number': 5,
            'command': 66051,
            'pulse': 1024,
            'signal_level': 4
        })

        self.assertEquals(str(self.parser), "<Lighting4 ID:None>")

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

        self.assertEquals(self.parser.log.name, 'rfxcom.protocol.Lighting4')
