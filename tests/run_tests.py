#!/usr/bin/env python
import os
import sys



from NWTestCase import NWTestCase


def main():
    dirname = os.path.dirname(os.path.abspath(__file__))

    case1 = NWTestCase(
        os.path.join(dirname,'cases/01_text'),
        os.path.join(dirname,''))

    case1.run()


if __name__ == '__main__':
    main()
