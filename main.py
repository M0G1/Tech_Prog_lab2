# -*- coding: utf-8 -*-
import sys
import application_ground


def main(args):
    app = application_ground.Application(args)
    app.execute()


if __name__ == "__main__":
    main(sys.argv)
