from __future__ import absolute_import, division, print_function, unicode_literals

from posixpath import join

from .assets import get_assets
from .client import Client
from .git import get_git_info
from .generate_hash import generate_file_hash, generate_hash


class Basset(object):
    def __init__(self, token, static_dir, basset_url, base_url=''):
        self.token = token
        self.static_dir = static_dir
        self.base_url = base_url
        self.client = Client(basset_url, token)

    def build_start(self):
        current_assets = self.get_assets()
        [
            branch,
            commit_sha,
            commit_message,
            committer_name,
            committer_email,
            commit_date,
            author_name,
            author_email,
            author_date,
        ] = get_git_info()
        data = {
            "branch": branch,
            "commitSha": commit_sha,
            "commitMessage": commit_message,
            "committerName": committer_name,
            "committerEmail": committer_email,
            "commitDate": commit_date,
            "authorName": author_name,
            "authorEmail": author_email,
            "authorDate": author_date,
            "assets": current_assets,
        }
        _, assets = self.client.build_start(data)
        self.upload_assets(assets)

    def build_finish(self):
        if self.client.build_id is None:
            raise Exception("There is no build to finish")
        response = self.client.build_finish()
        assert response['submitted'], "There was an error finalizing the build, the build was not submitted"

    def get_assets(self):
        return get_assets(self.static_dir, self.base_url)

    def upload_assets(self, assets):
        if self.client.build_id is None:
            raise Exception(
                "You cannot upload assets without starting a build")

        for [file_path, sha] in assets:
            relative_path = join(self.base_url, file_path)
            with open(file_path, "r") as file:
                content = file.read()
                response = self.client.upload_asset(relative_path, sha, content)
                assert response['uploaded'], "There was an error uploading the asset: {}".format(file_path)

    def upload_snapshot_source(self, snapshot, source):
        if self.client.build_id is None:
            raise Exception(
                "You cannot upload snapshots without starting a build")

        sha = generate_hash(source)
        title = snapshot[1]
        relative_path = "{}.html".format(title)

        response = self.client.upload_snapshot(snapshot, relative_path, sha, source)
        assert response['uploaded'], "There was an error uploading the snapshot: {}".format(title)


    def upload_snapshot_file(self, snapshot, file_path):
        if self.client.build_id is None:
            raise Exception(
                "You cannot upload snapshots without starting a build")

        title = snapshot[1]
        relative_path = "{}.html".format(title)
        with open(file_path, 'r') as f:
            content = f.read()
            sha = generate_hash(content)
            response = self.client.upload_snapshot(snapshot, relative_path, sha, content)
            assert response['uploaded'], "There was an error uploading the snapshot: {}".format(title)
