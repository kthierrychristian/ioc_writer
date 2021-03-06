# openioc_10_to_11.py
#
# Copyright 2013 Mandiant Corporation.
# Licensed under the Apache 2.0 license.  Developed for Mandiant by William
# Gibb.
#
# Mandiant licenses this file to you under the Apache License, Version
# 2.0 (the "License"); you may not use this file except in compliance with the
# License.  You may obtain a copy of the License at:
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.  See the License for the specific language governing
# permissions and limitations under the License.
#
# Allows for the upgrade of OpenIOC 1.0 IOCs to OpenIOC 1.1 format
#
import argparse
import logging
import os
import sys
from ..managers.upgrade_10 import UpgradeManager


log = logging.getLogger(__name__)



def main(options):
    # validate output dir
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s  [%(filename)s:%(funcName)s]')
    if os.path.isfile(options.output):
        log.error('Cannot set output directory to a file')
        sys.exit(1)
    # read in and convert iocs
    iocm = UpgradeManager()
    iocm.insert(options.iocs)
    errors = iocm.convert_to_11()
    if errors:
        for iocid in errors:
            log.error('Failed to process: [%s]' % str(iocid))
    if len(iocm.iocs_11) == 0:
        log.error('No IOCs available to write out')
        sys.exit(1)
    # write 1.1 iocs
    if iocm.write_iocs(options.output, iocm.iocs_11):
        log.info('Wrote iocs out to %s' % options.output)
    else:
        log.error('failed to write iocs out')
    sys.exit(0)


def makeargpaser():
    parser = argparse.ArgumentParser(description='Upgrade IOCs from 1.0 to 1.1')
    parser.add_argument('-i', '--iocs', dest='iocs', required=True, type=str,
                        help='Directory to iocs or the ioc to process.')
    parser.add_argument('-o', '--output', dest='output', required=True, type=str,
                        help='Dictory to write IOCs too.')
    return parser

def _main():
    p = makeargpaser()
    opts = p.parse_args()
    main(opts)

if __name__ == "__main__":
    _main()