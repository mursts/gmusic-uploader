#!/usr/bin/env python
# coding: utf-8

import os
import oauth2client
from gmusicapi import Musicmanager

CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__),
                                'credentials.json')


def main():
    storage = oauth2client.file.Storage(CREDENTIALS_PATH)
    credentials = storage.get()

    if not credentials or credentials.invalid:
        Musicmanager.perform_oauth(CREDENTIALS_PATH, open_browser=False)


if __name__ == '__main__':
    main()
