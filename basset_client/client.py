from __future__ import absolute_import, division, print_function, unicode_literals

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class Client(object):
    def __init__(self, basset_url, token):
        self.basset_url = basset_url
        self.token = token
        self.session = self.create_session()

    def create_session(self):
        headers = {
            "authorization": "Token {}".format(self.token)
        }
        session = requests.Session()
        session.headers.update(headers)

        retries = Retry(total=3,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])

        session.mount('https://', HTTPAdapter(max_retries=retries))

        return session

    def set_headers(self, relative_path, sha):
        return {
            "x-build-id": self.build_id,
            "x-relative-path": relative_path,
            "x-sha": sha,
        }

    def build_start(self, data):
        url = "{}build/start/".format(self.basset_url)
        response = self.session.post(url, json=data)
        response_data = response.json()
        response.raise_for_status()
        assert response_data.get('id') is not None, 'There was an error submitting the build: the response did not include a build id'
        self.build_id = response_data['id']
        assets = response_data.get('assets', [])
        return self.build_id, assets

    def upload_snapshot(self, snapshot, relative_path, sha, content):
        url = "{}/build/upload/snapshot".format(self.basset_url)

        widths, title, browsers, selectors, hide_selectors = snapshot

        data = {
            "widths": widths if widths else "",
            "title": title,
            "browsers": browsers if browsers else "",
            "hideSelectors": hide_selectors if hide_selectors else "",
            "selectors": selectors if selectors else "",
        }
        files = {
            "snapshot": ("{}.html".format(title), content, 'text/html'),
        }

        headers = self.set_headers(
            "/{}.html".format(title),
            sha,
        )

        response = self.session.post(
            url, data=data, files=files, headers=headers)
        response.raise_for_status()
        return response.json()

    def upload_asset(self, relative_path, sha, content):
        files = {
            "asset": (relative_path, content),
        }
        headers = self.set_headers(relative_path, sha)
        url = "{}/build/upload/asset".format(self.basset_url)
        response = self.session.post(url, files=files, headers=headers)
        response.raise_for_status()
        return response.json()

    def build_finish(self):
        data = {
            "buildId": self.build_id
        }
        url = "{}/build/finish".format(self.basset_url)
        response = self.session.post(url, data=data)
        response.raise_for_status()
        return response.json()
