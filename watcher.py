#!/usr/bin/env python
# coding: utf-8

import os
import time
import threading
import oauth2client
import eyed3
import config
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from gmusicapi import Musicmanager
from pyslack import SlackClient

CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__),
                                'credentials.dat')

EXTENSIONS = ['.mp3', '.m4a', '.flac']


def upload(file_path):
    storage = oauth2client.file.Storage(CREDENTIALS_PATH)
    credentials = storage.get()

    if not credentials or credentials.invalid:
        Musicmanager.perform_oauth(CREDENTIALS_PATH, open_browser=False)

    mm = Musicmanager()
    mm.login(CREDENTIALS_PATH)

    result = mm.upload(file_path, enable_matching=True)
    if result[1]:
        raise Exception('{}はアップロード済みです'.format(file_path))
    elif result[2]:
        raise Exception('アップロード失敗 {}'.format(result[2][file_path]))

    os.remove(file_path)


def notify(message):
    api = SlackClient(config.SLACK_API_KEY)
    channel = config.SLACK_CHANNEL
    username = config.SLACK_USERNAME
    api.chat_post_message(channel, message, username=username, as_user=False)


def get_mp3tag(file_path):
    t = eyed3.load(file_path)
    return t.tag.title, t.tag.album

class UploadThread(threading.Thread):
    def __init__(self, upload_file):
        threading.Thread.__init__(self)
        self._upload_file = upload_file

    def run(self):
        message = None
        try:
            upload(self._upload_file)
            title, album = get_mp3tag(self._upload_file)
            message = 'アップロードしました\n' \
                      '  title: {}\n' \
                      '  album: {}'.format(title, album)
        except Exception as e:
            message = e.message
        notify(message)


def is_uploadable_file(filename):
    name, ext = os.path.splitext(filename)
    return ext in EXTENSIONS

class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if not is_uploadable_file(event.src_path):
            return

        UploadThread(event.src_path).start()


if __name__ == '__main__':
    if not os.path.exists(config.OBSERVE_PATH):
        notify('監視ディレクトリがありません. {}'.format(
               config.OBSERVE_PATH))
        exit(1)

    if not os.path.exists(CREDENTIALS_PATH):
        notify('認証してください。')
        exit(1)

    event_handler = EventHandler()
    observer = Observer()

    observer.schedule(event_handler, config.OBSERVE_PATH)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
