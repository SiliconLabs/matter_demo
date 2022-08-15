#!/usr/bin/env python3
import sys
import os.path

DEFAULTS = {
  'application': os.path.join(os.path.dirname(sys.argv[0]), 'chip-efr32-lighting-example.s37'),
}

import efr32_firmware_utils

if __name__ == '__main__':
    sys.exit(efr32_firmware_utils.Flasher(**DEFAULTS).flash_command(sys.argv))
