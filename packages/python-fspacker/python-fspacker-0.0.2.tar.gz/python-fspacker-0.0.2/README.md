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
    dump : best: 0.00192141 <- median: 0.00303648 - average: 0.00289015 -> worst: 0.00357831
    loads: best: 0.00176141 <- median: 0.00193337 - average: 0.00192555 -> worst: 0.00245063
  marshal
    dump size:    474624 byte
    dump : best: 0.00091804 <- median: 0.00146398 - average: 0.00146232 -> worst: 0.00209858
    loads: best: 0.00144557 <- median: 0.00150470 - average: 0.00159074 -> worst: 0.00230714
  FSPacker
    dump size:    329289 byte
    dump : best: 0.02956123 <- median: 0.03191117 - average: 0.03488318 -> worst: 0.06962921
    loads: best: 0.02214191 <- median: 0.02311805 - average: 0.02343034 -> worst: 0.02914553
Test data two [1 times]
  pickle
    dump size:    274491 byte
    dump : best: 0.00102806 <- median: 0.00109109 - average: 0.00112886 -> worst: 0.00150502
    loads: best: 0.00137711 <- median: 0.00147515 - average: 0.00148870 -> worst: 0.00195776
  marshal
    dump size:    360242 byte
    dump : best: 0.00073095 <- median: 0.00080529 - average: 0.00079686 -> worst: 0.00087429
    loads: best: 0.00122311 <- median: 0.00139272 - average: 0.00154981 -> worst: 0.00244541
  FSPacker
    dump size:    238495 byte
    dump : best: 0.02812932 <- median: 0.02927591 - average: 0.03252403 -> worst: 0.06384002
    loads: best: 0.02134671 <- median: 0.02191628 - average: 0.02265632 -> worst: 0.03327830
Test data three [1000 times]
  pickle
    dump size:        97 byte
    dump : best: 0.00065989 <- median: 0.00066162 - average: 0.00066534 -> worst: 0.00073160
    loads: best: 0.00080160 <- median: 0.00080605 - average: 0.00080777 -> worst: 0.00084383
  marshal
    dump size:        79 byte
    dump : best: 0.00061424 <- median: 0.00061704 - average: 0.00061919 -> worst: 0.00063762
    loads: best: 0.00080728 <- median: 0.00081835 - average: 0.00082229 -> worst: 0.00090104
  FSPacker
    dump size:        85 byte
    dump : best: 0.01630956 <- median: 0.01642815 - average: 0.01642205 -> worst: 0.01668519
    loads: best: 0.01521912 <- median: 0.01530806 - average: 0.01553064 -> worst: 0.02047744
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