# -*- coding: utf-8 -*-
import sys
import application_rocket


def main(args):
    app = application_rocket.Application(args)
    app.execute()


if __name__ == "__main__":
    main(sys.argv)
