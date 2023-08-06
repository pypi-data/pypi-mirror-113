This Python3 library implements support for Dash transactions.

It builds on top, and is intended to be used along with python-bitcointx library.

## Requirements

- [python-bitcointx](https://github.com/Simplexum/python-bitcointx) (version >= 1.0.0)

## Usage:

With contextual switch to Dash parameters:

```python
import os
import dashtx
from bitcointx import ChainParams, get_current_chain_params
from bitcointx.wallet import (
    CCoinKey, CCoinExtKey, P2WPKHCoinAddress, CCoinAddress
)

with ChainParams('dash'):
    k = CCoinExtKey.from_seed(os.urandom(32))
    a = P2WPKHCoinAddress.from_pubkey(k.derive_path("m/0h/0h/1").pub)
    print('example {} address: {}'.format(get_current_chain_params().NAME, a))
    assert CCoinAddress(str(a)) == a

```

With global switch to Dash parameters:

```python
from dashtx import DashMainnetParams
from bitcointx import select_chain_params

select_chain_params('dash')
# or, using the chain params class directly
select_chain_params(DashMainnetParams)

```

Without the switch of chain parameters:

```python
from dashtx.wallet import P2SHDashAddress

p2sh_addr = P2SHDashAddress('7UHUEqN8EwpHFJjf7U83YAUhEinxYt1MAK')
p2sh_addr = P2SHDashAddress.from_scriptPubKey(p2sh_addr.to_scriptPubKey())
assert str(p2sh_addr) == '7UHUEqN8EwpHFJjf7U83YAUhEinxYt1MAK'

```

```python
from bitcointx import select_chain_params
from bitcointx.wallet import CCoinAddress
from dashtx.wallet import P2SHDashAddress

select_chain_params('dash')
p2sh_addr = CCoinAddress('7UHUEqN8EwpHFJjf7U83YAUhEinxYt1MAK')
assert isinstance(p2sh_addr, P2SHDashAddress)
```
this also works with ChainParams context manager.
