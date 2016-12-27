from unittest import TestCase

from rfxcom.protocol.lighting1 import Lighting1

from rfxcom.exceptions import (InvalidPacketLength, UnknownPacketSubtype,
                               UnknownPacketType)


class Lighting1TestCase(TestCase):

    def setUp(self):

        self.data = bytearray(b'\x07\x10\x00\x01\x41\x0A\x01\x40')
        self.parser = Lighting1()

    def test_parse_frame_x10_on(self):

        self.data = bytearray(b'\x07\x10\x00\x01\x41\x0A\x01\x40')

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'id': 'A10',
            'packet_length': 7,
            'packet_type': 16,
            'packet_type_name': "Lighting1 sensors",
            'packet_subtype': 0,
            'packet_subtype_name': "X10 Lightning",
            'sequence_number': 1,
            'house_code': 'A',
            'unit_code': 10,
            'command': 1,
            'command_text': "On",
            'signal_level': 4
        })

        self.assertEquals(str(self.parser), "<Lighting1 ID:A10>")

    def test_parse_frame_x10_off(self):

        self.data = bytearray(b'\x07\x10\x00\x03\x41\x0E\x00\x50')

        self.assertTrue(self.parser.validate_packet(self.data))
        self.assertTrue(self.parser.can_handle(self.data))
        result = self.parser.load(self.data)

        self.assertEquals(result, {
            'id': 'A14',
            'packet_length': 7,
            'packet_type': 16,
            'packet_type_name': "Lighting1 sensors",
            'packet_subtype': 0,
            'packet_subtype_name': "X10 Lightning",
            'sequence_number': 3,
            'house_code': 'A',
            'unit_code': 14,
            'command': 0,
            'command_text': "Off",
            'signal_level': 5,
        })

        self.assertEquals(str(self.parser), "<Lighting1 ID:A14>")

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

        self.assertEquals(self.parser.log.name, 'rfxcom.protocol.Lighting1')
