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

from bitcointx.core.script import (
    CScript, ScriptCoinClassDispatcher, ScriptCoinClass
)


class ScriptDashClassDispatcher(ScriptCoinClassDispatcher):
    ...


class ScriptDashClass(ScriptCoinClass, metaclass=ScriptDashClassDispatcher):
    ...


class CDashScript(CScript, ScriptDashClass):
    ...


__all__ = (
    'CDashScript',
)
