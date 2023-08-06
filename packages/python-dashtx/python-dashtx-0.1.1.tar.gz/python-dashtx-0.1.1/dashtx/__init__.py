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

import dashtx.core
import dashtx.core.script
import dashtx.wallet

from bitcointx import ChainParamsBase


# Declare chain params after frontend classes are regstered in wallet.py,
# so that issubclass checks in ChainParamsMeta.__new__() would pass
class DashMainnetParams(ChainParamsBase, name=('dash', 'dash/mainnet')):
    RPC_PORT = 9998
    WALLET_DISPATCHER = dashtx.wallet.WalletDashClassDispatcher


class DashTestnetParams(DashMainnetParams, name='dash/testnet'):
    RPC_PORT = 19998
    WALLET_DISPATCHER = dashtx.wallet.WalletDashTestnetClassDispatcher

    def get_datadir_extra_name(self) -> str:
        return 'testnet3'

    def get_network_id(self) -> str:
        return "test"


class DashRegtestParams(DashMainnetParams, name='dash/regtest'):
    RPC_PORT = 19898
    WALLET_DISPATCHER = dashtx.wallet.WalletDashRegtestClassDispatcher


__all__ = (
    'DashMainnetParams',
    'DashTestnetParams',
    'DashRegtestParams'
)
