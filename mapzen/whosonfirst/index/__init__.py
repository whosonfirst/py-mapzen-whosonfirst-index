# https://pythonhosted.org/setuptools/setuptools.html#namespace-packages
__import__('pkg_resources').declare_namespace(__name__)

import json
import os.path
import sqlite3

import mapzen.whosonfirst.utils

class indexer:

    def __init__ (self, mode, callback):
        
        self.mode = mode
        self.callback = callback

    def process(self, feature):
        self.callback(feature)

    def index_paths(self, paths):

        for path in paths:
            self.index_path(path)
            
    def index_path(self, path):

        if self.mode == "files":
            self.index_path(path)
        elif self.mode == "directory":
            self.index_directory(path)
        elif self.mode == "repo":
            self.index_repo(path)
        elif self.mode == "sqlite":
            self.index_sqlite(path)
        else:
            raise Exception, "Invalid or unsupported mode"

    def index_directory(self, path):

        iter = mapzen.whosonfirst.utils.crawl(path, inflate=True)

        for f in iter:
            self.process(f)

    def index_feature(self, path):

        f = mapzeen.whosonfirst.utils.load_file(path)
        return self.process(f)

    def index_repo(self, path):

        data = os.path.join(path, "data")
        return self.index_repo(data)

    def index_sqlite(self, path):
        
        conn = sqlite3.connect(path)

        rsp = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        has_table = False
        
        for row in rsp:
            if row[0] == "geojson":
                has_table = True
                break

        if not has_table:
            raise Exception, "database is issing 'geojson' table"
        
        rsp = conn.execute("SELECT body FROM geojson")

        for row in rsp:
            f = json.loads(row[0])
            self.process(f)
        
