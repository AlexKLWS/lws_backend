from typing import Any, Callable

import yaml
import os
import threading
import time
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Consts
CONFIG_FILE_NAME = "config.yaml"
API_PREFIX = "/api"

# Keys
ENV = "env"
PORT = "port"
IS_DEBUG = "is-debug"
TOKEN_LIFETIME = "token-lifetime"
PAGE_SIZE = "page-size"
ALLOWED_LOGIN_PASSWORDS = "allowed-passwords"
DB_CONNECTION_URI = "db-connection-uri"
VERSION = "version"

# Configuration


class Config:
    data: Any = None
    project_root_directory: str = ""
    config_file_path: str = ""

    def __init__(self, main_file: str):
        main_file_directory = os.path.abspath(os.path.dirname(main_file))
        self.project_root_directory = os.path.abspath(
            os.path.join(main_file_directory, os.pardir)
        )
        self.config_file_path = os.path.join(
            self.project_root_directory, CONFIG_FILE_NAME
        )

    def setup(self):
        self.load_config()

        update_watcher = ThreadWatcher(self)
        update_watcher.start()

        self.data[IS_DEBUG] = self.data[ENV] == "debug"

    def load_config(self):
        with open(self.config_file_path, "r") as yamlfile:
            self.data = yaml.load(yamlfile, Loader=yaml.FullLoader)
            yamlfile.close()

    def get(self, key: str):
        try:
            value = self.data[key]
            return value
        except AttributeError:
            return None


class BasicEventHandler(FileSystemEventHandler):
    current_event = None

    def process(self, event):
        if event.is_directory is not True:
            self.current_event = event

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

    def get_event(self):
        current_event = self.current_event
        self.current_event = None
        return current_event


class WatcherBase:
    config: Config
    event_handler: BasicEventHandler = BasicEventHandler()

    def __init__(self, config: Config):
        self.config = config

    def watch_config_updates(self):
        observer = Observer()
        observer.schedule(self.event_handler,
                          self.config.project_root_directory)
        observer.start()
        try:
            while True:
                event = self.event
                if event is not None and event.src_path == self.config.config_file_path:
                    self.config.load_config()
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

    @property
    def event(self):
        return self.event_handler.get_event()


class ThreadWatcher(WatcherBase):
    thread: Thread

    def __init__(self, config: Config):
        super(ThreadWatcher, self).__init__(config)
        self.thread = threading.Thread(target=self.watch_config_updates)
        self.thread.daemon = True

    def start(self):
        self.thread.start()
