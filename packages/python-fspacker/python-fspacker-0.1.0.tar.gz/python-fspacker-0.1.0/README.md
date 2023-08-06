[![Python package](https://github.com/FusionSolutions/python-fspacker/actions/workflows/python-package.yml/badge.svg)](https://github.com/FusionSolutions/python-fspacker/actions/workflows/python-package.yml)
# Fusion Solutions message packer

## Introduction

Message packer for socket communications.
Pure-Python implementation and it is [*much slower*](#benchmark) as `pickle`, `marshal` or even `json`, but much safer for production.
The following types are supported for packing and unpacking:
 - `None`
 - `bool`
 - `int`
 - `float`
 - `string`
 - `bytearray` (during unpacking it will be converted to `bytes`)
 - `bytes`
 - `list` (during unpacking it will be converted to `tuple`)
 - `tuple`
 - `dict` (dict key type can be any from this list)
 - `set` (full support)

## Installation

Requires python version 3.7 or later.

To install the latest release on [PyPI](https://pypi.org/project/python-fspacker/),
simply run:

```shell
pip3 install python-fspacker
```

Or to install the latest version, run:

```shell
git clone https://github.com/FusionSolutions/python-fspacker.git
cd python-fspacker
python3 setup.py install
```

## Python library

### Usage

Use like `pickle` with `dump`, `dumps`, `load` and `loads` functions.

```python
import fsPacker

data = fsPacker.dumps(["test"]*5)
print( fsPacker.loads(data) )
```

### Benchmark

Environment: Intel(R) Xeon(R) CPU E5-1650 v4 @ 3.60GHz, DIMM DDR4 Synchronous Registered (Buffered) 2133 MHz
```shell
$/python-fspacker: python3 -m benchmark
Test data one [1 times]
  pickle
    dump size:    369436 byte
    dump : best: 0.00158157 <- median: 0.00163573 - average: 0.00164407 -> worst: 0.00173204
    loads: best: 0.00157589 <- median: 0.00160991 - average: 0.00162757 -> worst: 0.00216137
  marshal
    dump size:    474624 byte
    dump : best: 0.00084558 <- median: 0.00089093 - average: 0.00089481 -> worst: 0.00096658
    loads: best: 0.00135764 <- median: 0.00137184 - average: 0.00138647 -> worst: 0.00170787
  FSPacker
    dump size:    329293 byte
    dump : best: 0.03001423 <- median: 0.03062541 - average: 0.03170544 -> worst: 0.04718978
    loads: best: 0.02231823 <- median: 0.02331613 - average: 0.02334542 -> worst: 0.02514797
Test data two [1 times]
  pickle
    dump size:    274491 byte
    dump : best: 0.00107667 <- median: 0.00108967 - average: 0.00110260 -> worst: 0.00119756
    loads: best: 0.00145767 <- median: 0.00148819 - average: 0.00150257 -> worst: 0.00176494
  marshal
    dump size:    360242 byte
    dump : best: 0.00077111 <- median: 0.00081842 - average: 0.00099891 -> worst: 0.00156944
    loads: best: 0.00127497 <- median: 0.00128988 - average: 0.00141144 -> worst: 0.00256521
  FSPacker
    dump size:    238499 byte
    dump : best: 0.02852817 <- median: 0.02961052 - average: 0.03016038 -> worst: 0.03880055
    loads: best: 0.02128199 <- median: 0.02241915 - average: 0.02516957 -> worst: 0.03794705
Test data three [1000 times]
  pickle
    dump size:        97 byte
    dump : best: 0.00066121 <- median: 0.00067347 - average: 0.00067562 -> worst: 0.00069691
    loads: best: 0.00081164 <- median: 0.00081801 - average: 0.00082066 -> worst: 0.00083911
  marshal
    dump size:        79 byte
    dump : best: 0.00061814 <- median: 0.00062130 - average: 0.00062324 -> worst: 0.00063816
    loads: best: 0.00083109 <- median: 0.00083498 - average: 0.00084022 -> worst: 0.00088368
  FSPacker
    dump size:        85 byte
    dump : best: 0.01618888 <- median: 0.01634808 - average: 0.01681845 -> worst: 0.02476933
    loads: best: 0.01527784 <- median: 0.01556471 - average: 0.01594638 -> worst: 0.02066095
```
## Contribution

Bug reports, constructive criticism and suggestions are welcome. If you have some create an issue on [github](https://github.com/FusionSolutions/python-fspacker/issues).

## Copyright

All of the code in this distribution is Copyright (c) 2021 Fusion Solutions Kft.

The utility is made available under the GNU General Public license. The included LICENSE file describes this in detail.

## Warranty

THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE USE OF THIS SOFTWARE IS WITH YOU.

IN NO EVENT WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR REDISTRIBUTE THE LIBRARY, BE LIABLE TO YOU FOR ANY DAMAGES, EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

Again, see the included LICENSE file for specific legal details.