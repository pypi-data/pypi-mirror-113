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

from typing import Type, List

from bitcointx.util import ClassMappingDispatcher
from bitcointx.wallet import (
    WalletCoinClassDispatcher, WalletCoinClass,
    CCoinAddress, P2SHCoinAddress, P2WSHCoinAddress,
    P2PKHCoinAddress, P2WPKHCoinAddress,
    CBase58CoinAddress, CBech32CoinAddress,
    CCoinKey, CCoinExtKey, CCoinExtPubKey,
    T_CBase58DataDispatched
)
from .core import CoreDashClassDispatcher


class WalletDashClassDispatcher(WalletCoinClassDispatcher,
                                depends=[CoreDashClassDispatcher]):
    ...


class WalletDashTestnetClassDispatcher(WalletDashClassDispatcher):
    ...


class WalletDashRegtestClassDispatcher(WalletDashClassDispatcher):
    ...


class WalletDashClass(WalletCoinClass,
                      metaclass=WalletDashClassDispatcher):
    ...


class WalletDashTestnetClass(
    WalletDashClass, metaclass=WalletDashTestnetClassDispatcher
):
    ...


class WalletDashRegtestClass(
    WalletDashClass, metaclass=WalletDashRegtestClassDispatcher
):
    ...


class CDashAddress(CCoinAddress, WalletDashClass):
    ...


class CDashTestnetAddress(CCoinAddress, WalletDashTestnetClass):
    ...


class CDashRegtestAddress(CCoinAddress, WalletDashRegtestClass):
    ...


class CBase58DashAddress(CBase58CoinAddress, CDashAddress):
    @classmethod
    def base58_get_match_candidates(cls: Type[T_CBase58DataDispatched]
                                    ) -> List[Type[T_CBase58DataDispatched]]:
        assert isinstance(cls, ClassMappingDispatcher)
        return super(CBase58DashAddress, cls).base58_get_match_candidates()


class CBase58DashTestnetAddress(CBase58CoinAddress, CDashTestnetAddress):
    ...


class CBase58DashRegtestAddress(CBase58CoinAddress, CDashRegtestAddress):
    ...


class CBech32DashAddress(CBech32CoinAddress, CDashAddress):
    bech32_hrp = 'dsh'


class CBech32DashTestnetAddress(CBech32CoinAddress, CDashTestnetAddress):
    bech32_hrp = 'tdsh'


class CBech32DashRegtestAddress(CBech32CoinAddress, CDashRegtestAddress):
    bech32_hrp = 'rdsh'


class P2SHDashAddress(P2SHCoinAddress, CBase58DashAddress):
    base58_prefix = bytes([16])


class P2PKHDashAddress(P2PKHCoinAddress, CBase58DashAddress):
    base58_prefix = bytes([76])


class P2WSHDashAddress(P2WSHCoinAddress, CBech32DashAddress):
    ...


class P2WPKHDashAddress(P2WPKHCoinAddress, CBech32DashAddress):
    ...


class P2SHDashTestnetAddress(P2SHCoinAddress, CBase58DashTestnetAddress):
    base58_prefix = bytes([19])


class P2PKHDashTestnetAddress(P2PKHCoinAddress, CBase58DashTestnetAddress):
    base58_prefix = bytes([140])


class P2SHDashRegtestAddress(P2SHCoinAddress, CBase58DashRegtestAddress):
    base58_prefix = bytes([19])


class P2PKHDashRegtestAddress(P2PKHCoinAddress, CBase58DashRegtestAddress):
    base58_prefix = bytes([140])


class P2WSHDashTestnetAddress(P2WSHCoinAddress, CBech32DashTestnetAddress):
    ...


class P2WPKHDashTestnetAddress(P2WPKHCoinAddress, CBech32DashTestnetAddress):
    ...


class P2WSHDashRegtestAddress(P2WSHCoinAddress, CBech32DashRegtestAddress):
    ...


class P2WPKHDashRegtestAddress(P2WPKHCoinAddress, CBech32DashRegtestAddress):
    ...


class CDashKey(CCoinKey, WalletDashClass):
    base58_prefix = bytes([204])


class CDashTestnetKey(CCoinKey, WalletDashTestnetClass):
    base58_prefix = bytes([239])


class CDashRegtestKey(CCoinKey, WalletDashRegtestClass):
    base58_prefix = bytes([239])


class CDashExtPubKey(CCoinExtPubKey, WalletDashClass):
    base58_prefix = b'\x02\xfe\x52\xcc'


class CDashExtKey(CCoinExtKey, WalletDashClass):
    base58_prefix = b'\x02\xfe\x52\xf8'


class CDashTestnetExtPubKey(CCoinExtPubKey, WalletDashTestnetClass):
    base58_prefix = b'\x3a\x80\x58\x37'


class CDashTestnetExtKey(CCoinExtKey, WalletDashTestnetClass):
    base58_prefix = b'\x3a\x80\x61\xa0'


class CDashRegtestExtPubKey(CCoinExtPubKey, WalletDashRegtestClass):
    base58_prefix = b'\x3a\x80\x58\x37'


class CDashRegtestExtKey(CCoinExtKey, WalletDashRegtestClass):
    base58_prefix = b'\x3a\x80\x61\xa0'


__all__ = (
    'CDashAddress',
    'CDashTestnetAddress',
    'CBase58DashAddress',
    'CBech32DashAddress',
    'P2SHDashAddress',
    'P2PKHDashAddress',
    'P2WSHDashAddress',
    'P2WPKHDashAddress',
    'CBase58DashTestnetAddress',
    'CBech32DashTestnetAddress',
    'P2SHDashTestnetAddress',
    'P2PKHDashTestnetAddress',
    'P2WSHDashTestnetAddress',
    'P2WPKHDashTestnetAddress',
    'CDashKey',
    'CDashExtKey',
    'CDashExtPubKey',
    'CDashTestnetKey',
    'CDashTestnetExtKey',
    'CDashTestnetExtPubKey',
    'CDashRegtestKey',
    'CDashRegtestExtKey',
    'CDashRegtestExtPubKey',
)
