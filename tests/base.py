# -*- coding: utf-8 -*-

import os
import sys
import logging

import unittest

# Dirty hack, on 2.6 tests are ok always
# UnitTest2 not clearly works with setuptools
if sys.version_info < (2, 7):
    def raise_skip(msg):
        return None
else:
    def raise_skip(msg):
        raise unittest.SkipTest(msg)

import zstd

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('ZSTD')
log.info("Python version: %s" % sys.version)

class BaseTestZSTD(unittest.TestCase):

    LEGACY = False
    PYZSTD_LEGACY = False

    def helper_compression_random(self):
        DATA = os.urandom(128 * 1024)  # Read 128kb
        self.assertEqual(DATA, zstd.loads(zstd.dumps(DATA)))

    def helper_compression_default_level(self):
        if sys.hexversion < 0x03000000:
            DATA = 'This is must be very very long string to be compressed by zstd. AAAAAAAAAAARGGHHH!!! Just hope its enough length. И немного юникода.'
        else:
            DATA = b'This is must be very very long string to be compressed by zstd. AAAAAAAAAAARGGHHH!!! Just hope its enough length.' + ' И немного юникода.'.encode()
        self.assertEqual(DATA, zstd.decompress(zstd.compress(DATA)))

    def helper_compression_old_default_level(self):
        if sys.hexversion < 0x03000000:
            DATA = 'This is must be very very long string to be compressed by zstd. AAAAAAAAAAARGGHHH!!! Just hope its enough length. И немного юникода.'
        else:
            DATA = b'This is must be very very long string to be compressed by zstd. AAAAAAAAAAARGGHHH!!! Just hope its enough length.' + ' И немного юникода.'.encode()
        self.assertEqual(DATA, zstd.decompress_old(zstd.compress_old(DATA)))

    def helper_compression_level1(self):
        if sys.hexversion < 0x03000000:
            DATA = 'This is must be very very long string to be compressed by zstd. AAAAAAAAAAAAARGGHHH!!! Just hope its enough length. И немного юникода.'
        else:
            DATA = b'This is must be very very long string to be compressed by zstd. AAAAAAAAAAAAARGGHHH!!! Just hope its enough length.' + 'И немного юникода.'.encode()
        self.assertEqual(DATA, zstd.decompress(zstd.compress(DATA, 1)))

    def helper_compression_level6(self):
        if sys.hexversion < 0x03000000:
            DATA = "This is must be very very long string to be compressed by zstd. AAAAAAAAAAAAARGGHHH!!! Just hope its enough length. И немного юникода."
        else:
            DATA = b"This is must be very very long string to be compressed by zstd. AAAAAAAAAAAAARGGHHH!!! Just hope its enough length." + " И немного юникода.".encode()
        self.assertEqual(DATA, zstd.decompress(zstd.compress(DATA, 6)))

    def helper_compression_level20(self):
        if sys.hexversion < 0x03000000:
            DATA = "This is must be very very long string to be compressed by zstd. AAAAAAAAAAAAARGGHHH!!! Just hope its enough length. И немного юникода."
        else:
            DATA = b"This is must be very very long string to be compressed by zstd. AAAAAAAAAAAAARGGHHH!!! Just hope its enough length." + " И немного юникода.".encode()
        self.assertEqual(DATA, zstd.decompress(zstd.compress(DATA, 20)))

    def helper_decompression_v036(self):
        # That data maked with old legacy version of pyzstd
        if sys.hexversion < 0x03000000:
            CDATA = '\xa1\x00\x00\x00#\xb5/\xfd\x00\x00\x97\\\x02\x00\x11\x00$\x80\xc1\t\xe0k)?\x8d\x0b\x82g\xb4\x18\x93oK/\x95\xccD\x88\x94\xce7\x9a\x956\xa32\x01[\xaf\xf5u7\x03\x16\x00\x18\x00\x18\x00f\xcf\xc5U\xb3\x07\x1dO1%O1%\'\xe3\xd5\xe8\xb1:\xabk\x87\x83%X\x01?\xe84\xa6\xe4f5\xe1\x89q\x93\xaa\x19\xa1\x07"\x9c\x8c\xe1\x06\xec\xa5\xe3\xc6"\xf8\xd2\xba\xce\t\xc1\xe6\xd5\xa8\xe0$I\x96eQ\x14\x03\xc1+\x8bq\xc7\xabG\x0e9uE\x80\xab7^\x9d:\xc0\x1f\xa7\xee\xc5\xbd\xda\x06\x01\x00T\x01\x10\x00\x00\x18\xc2\x1f\xc0\x00\x00'
            DATA = 'This is must be very very long string to be compressed by zstd version 0.3.6. AAAAAAAAAAARGGHHH!!! Just hope its enough length.' + ' И немного юникода.'
        else:
            CDATA = b'\xa1\x00\x00\x00#\xb5/\xfd\x00\x00\x97\\\x02\x00\x11\x00$\x80\xc1\t\xe0k)?\x8d\x0b\x82g\xb4\x18\x93oK/\x95\xccD\x88\x94\xce7\x9a\x956\xa32\x01[\xaf\xf5u7\x03\x16\x00\x18\x00\x18\x00f\xcf\xc5U\xb3\x07\x1dO1%O1%\'\xe3\xd5\xe8\xb1:\xabk\x87\x83%X\x01?\xe84\xa6\xe4f5\xe1\x89q\x93\xaa\x19\xa1\x07"\x9c\x8c\xe1\x06\xec\xa5\xe3\xc6"\xf8\xd2\xba\xce\t\xc1\xe6\xd5\xa8\xe0$I\x96eQ\x14\x03\xc1+\x8bq\xc7\xabG\x0e9uE\x80\xab7^\x9d:\xc0\x1f\xa7\xee\xc5\xbd\xda\x06\x01\x00T\x01\x10\x00\x00\x18\xc2\x1f\xc0\x00\x00'
            DATA = b'This is must be very very long string to be compressed by zstd version 0.3.6. AAAAAAAAAAARGGHHH!!! Just hope its enough length.' + ' И немного юникода.'.encode()
        self.assertEqual(DATA, zstd.decompress_old(CDATA))

    def helper_decompression_v046(self):
        # That data maked with old legacy version of pyzstd
        if sys.hexversion < 0x03000000:
            CDATA = '\xa1\x00\x00\x00$\xb5/\xfd\x00\x00\x00\x97\x14\x02\xc0\x0f\x00#\x909\x01@\x06+X8\xaaG\xc1k\\\x1eVfA\xfb3\x13R\xaa\xdf?\x85\xd30\xb8T\xc4\x1d\xd4\xcc+\x04\x15\x00\x17\x00\x15\x00\x1a\xdd\xe0\x8b\xe2\xbaAu\xa6(\x11N\xc6q\xa5\xc7\xfb\xbc\xcf\x19\x02\x8aR\x18\x98\tX\x80\x01\x0c\xf5m\x137\xe1\x89q\x93\xbb\x19A\x8f\x1e\x02\x8b\x9b\xb9\xd8`:vMR\x98\xde\xf8\x9c\x90:\x82\xd7Z\xcb\xb2\x04\x8cq\xc7\xabG\x0e9u\xc5\xc4\xd5\x1b\xafN]\xf2\xc7\xa9;\x05\x00T\x00\x80\r\x00\x80\xb3\x18Th\x00l$@\xc5\x11\x0c*\xc0\x00\x00'
            DATA = 'This is must be very very long string to be compressed by zstd version 0.4.6. AAAAAAAAAAARGGHHH!!! Just hope its enough length.' + ' И немного юникода.'
        else:
            CDATA = b'\xa1\x00\x00\x00$\xb5/\xfd\x00\x00\x00\x97\x14\x02\xc0\x0f\x00#\x909\x01@\x06+X8\xaaG\xc1k\\\x1eVfA\xfb3\x13R\xaa\xdf?\x85\xd30\xb8T\xc4\x1d\xd4\xcc+\x04\x15\x00\x17\x00\x15\x00\x1a\xdd\xe0\x8b\xe2\xbaAu\xa6(\x11N\xc6q\xa5\xc7\xfb\xbc\xcf\x19\x02\x8aR\x18\x98\tX\x80\x01\x0c\xf5m\x137\xe1\x89q\x93\xbb\x19A\x8f\x1e\x02\x8b\x9b\xb9\xd8`:vMR\x98\xde\xf8\x9c\x90:\x82\xd7Z\xcb\xb2\x04\x8cq\xc7\xabG\x0e9u\xc5\xc4\xd5\x1b\xafN]\xf2\xc7\xa9;\x05\x00T\x00\x80\r\x00\x80\xb3\x18Th\x00l$@\xc5\x11\x0c*\xc0\x00\x00'
            DATA = b'This is must be very very long string to be compressed by zstd version 0.4.6. AAAAAAAAAAARGGHHH!!! Just hope its enough length.' + ' И немного юникода.'.encode()
        self.assertEqual(DATA, zstd.decompress_old(CDATA))
