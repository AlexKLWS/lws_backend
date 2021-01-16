import os
import threading
import subprocess
import logging

from lws_backend.core.config import (
    CLIENT_SOURCE_PATH,
)

client_snap_updater_instance = None


class ClientSnapUpdater:
    @classmethod
    def get_or_create_updater(cls):
        if client_snap_updater_instance:
            return client_snap_updater_instance
        return cls()

    def __init__(self):
        self.updater_lock = threading.Lock()

    def update(self):
        t = threading.Thread(target=self.update_client_snap_thread_safe, daemon=True)
        t.start()

    def update_client_snap_thread_safe(self):
        self.updater_lock.acquire()
        update_client_snap()
        self.updater_lock.release()


def update_client_snap():
    dir = CLIENT_SOURCE_PATH
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)
        os.chmod(dir, 0o755)

    if len(os.listdir(dir)) == 0:
        checkout_repo_process = run_process(
            'git clone https://github.com/AlexKLWS/lws-blog.git', CLIENT_SOURCE_PATH)

        if checkout_repo_process.returncode:
            logging.info('Couldnt checout the repo! Aborting...')
            return

    deps_install_process = run_process('yarn install', f'{CLIENT_SOURCE_PATH}/lws-blog/')

    if deps_install_process.returncode:
        logging.info('Couldnt install all dependencies! Aborting...')
        return

    puppeteer_fix_script = f'{CLIENT_SOURCE_PATH}/lws-blog/scripts/add-puppeteer-sandbox-args.sh'

    os.chmod(puppeteer_fix_script, 0o755)

    puppeteer_fix_process = run_process(puppeteer_fix_script, './')

    if puppeteer_fix_process.returncode:
        logging.info('Couldnt run puppeteer fix! Aborting...')
        return

    build_process = run_process('yarn build', f'{CLIENT_SOURCE_PATH}/lws-blog/')

    if build_process.returncode:
        logging.info('Couldnt complete build! Aborting...')
        return

    remove_old_client_process = run_process('rm -rf client', './')

    if remove_old_client_process.returncode:
        logging.info('Couldnt remove old client folder! Aborting...')
        return

    logging.info('===> Removed old client folder')

    copy_new_client_process = run_process('cp -r client_source/lws-blog/build client', './')

    if copy_new_client_process.returncode:
        logging.info('Couldnt copy new client folder! Aborting...')
        return

    logging.info('===> Copied new client folder')
    logging.info('All done!')


def run_process(process_args, cwd):
    process = subprocess.run(process_args,
                             universal_newlines=True,
                             shell=True,
                             cwd=cwd)

    return process
