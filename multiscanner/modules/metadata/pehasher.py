# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import division, absolute_import, with_statement, unicode_literals
import logging

logger = logging.getLogger(__name__)

try:
    import pefile
except ImportError:
    logger.error("pefile module not installed...")
    pefile = False

try:
    import pehash
    HASH_FUNCS = {
        'totalhash': pehash.totalhash,
        'anymaster': pehash.anymaster,
        'anymaster_v1_0_1': pehash.anymaster_v1_0_1,
        'endgame': pehash.endgame,
        'crits': pehash.crits,
        'pehashng': pehash.pehashng,
    }
except ImportError:
    logger.error("pehash module not installed...")
    pehash = False

__author__ = "Patrick Copeland"
__credits__ = ["knowmalware"]
__license__ = "MPL 2.0"

TYPE = "Metadata"
NAME = "pehash"
REQUIRES = ["filemeta"]
DEFAULTCONF = {
    'ENABLED': True,
}


def check(conf=DEFAULTCONF):
    if not conf['ENABLED'] or \
       not pefile or \
       not pehash or \
       None in REQUIRES:
        return False
    return True


def scan(filelist, conf=DEFAULTCONF):
    results = []
    filemeta_results, _ = REQUIRES[0]

    for fname, filemeta_result in filemeta_results:
        if fname not in filelist:
            logger.debug("File not in filelist: {}".format(fname))
        if not filemeta_result.get('filetype', '').startswith('PE32'):
            continue
        pe_hashes = {}
        pe = pefile.PE(fname)
        for name, hasher in HASH_FUNCS.items():
            try:
                pe_hashes[name] = hasher(pe=pe, raise_on_error=True).hexdigest()
            except Exception as e:
                logger.error(name)
                logger.error(e)
        results.append((fname, pe_hashes))

    metadata = {}
    metadata["Name"] = NAME
    metadata["Type"] = TYPE
    metadata["Include"] = False
    return (results, metadata)