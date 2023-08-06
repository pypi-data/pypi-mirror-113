# Copyright (C) 2019 The python-dashtx developers
#
# This file is part of python-dashtx.
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-dashtx, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

# pylama:ignore=E501

import unittest

from bitcointx.tests.test_wallet import test_address_implementations

from bitcointx import ChainParams
from bitcointx.wallet import CCoinAddress

from dashtx import DashMainnetParams
from dashtx.wallet import P2SHDashAddress, P2PKHDashAddress


class Test_DashAddress(unittest.TestCase):

    def test_address_implementations(self, paramclasses=None):
        test_address_implementations(self, paramclasses=[DashMainnetParams])

    def test_p2sh(self):
        with ChainParams('dash'):
            a = CCoinAddress('7UHUEqN8EwpHFJjf7U83YAUhEinxYt1MAK')
            self.assertIsInstance(a, P2SHDashAddress)

        p2sh_addr = '7T8Bu2cYd7DdiuLwCCYrroSu5wBoLxSu2Q'
        self.assertEqual(
            str(P2SHDashAddress.from_scriptPubKey(
                P2SHDashAddress(p2sh_addr).to_scriptPubKey())), p2sh_addr)

    def test_p2pkh(self):
        with ChainParams('dash'):
            a = CCoinAddress('XgRjhjdLSZry6S55CYddAgVDDipa1P6gF7')
            self.assertIsInstance(a, P2PKHDashAddress)

        p2pkh = 'XgRjhjdLSZry6S55CYddAgVDDipa1P6gF7'
        self.assertEqual(
            str(P2PKHDashAddress.from_scriptPubKey(
                P2PKHDashAddress(p2pkh).to_scriptPubKey())), p2pkh)
