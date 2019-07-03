import unittest

from mock import patch, MagicMock

from basset_client.client import Client

def mock_session():
    client = Client('http://basset.io', 'token')
    client.session = MagicMock()
    client.session.post = MagicMock()
    return client

class ClientTest(unittest.TestCase):
    def test_set_headers(self):
        client = Client('url', 'token')
        client.build_id = '123ea'
        headers = client.set_headers('relative_path', 'sha1')
        self.assertDictEqual(headers, {
            'x-build-id': '123ea',
            'x-relative-path': 'relative_path',
            'x-sha': 'sha1',
        })


    def test_build_start(self):
        client = mock_session()
        client.session.post.return_value = MagicMock(
            json=MagicMock(return_value={'id': '123ea'})
        )

        data = {
            'assets': {
                'path/to/file.png': 'sha1'
            }
        }
        build_id, assets = client.build_start(data)
        self.assertEqual(build_id, '123ea')
        self.assertEqual(assets, [])

    def test_build_start_error(self):
        client = mock_session()
        client.session.post.return_value = MagicMock(
            json=MagicMock(return_value={'error': '123ea'})
        )

        with self.assertRaises(AssertionError):
            client.build_start({})

    def test_build_finish(self):
        client = mock_session()
        client.session.post.return_value = MagicMock(
            json=MagicMock(return_value={'submitted': True})
        )
        client.build_id = '123ea'
        response = client.build_finish()
        self.assertEqual(response, {'submitted': True})

    def test_upload_snapshot(self):
        client = mock_session()
        client.session.post.return_value = MagicMock(
            json=MagicMock(return_value={'uploaded': True})
        )
        client.build_id = '123ea'
        snapshot = [
            '1280',
            'test snapshot',
            None,
            None,
            None,
        ]
        response = client.upload_snapshot(snapshot, 'path/to/file.html', 'sha1', '<html></html>')
        headers = {
            'x-build-id': '123ea',
            'x-relative-path': '/test snapshot.html',
            'x-sha': 'sha1',
        }
        data = {
            'widths': '1280',
            'title': 'test snapshot',
            'browsers': '',
            'selectors': '',
            'hideSelectors': '',
        }
        files = {
            'snapshot': ('test snapshot.html', '<html></html>', 'text/html')
        }
        client.session.post.assert_called_with('http://basset.io/build/upload/snapshot', data=data, files=files, headers=headers)
        self.assertEqual(response, {'uploaded': True})

    def test_upload_asset(self):
        client = mock_session()
        client.session.post.return_value = MagicMock(
            json=MagicMock(return_value={'uploaded': True})
        )
        client.build_id = '123ea'
        response = client.upload_asset('path/to/img.png', 'sha1', 'content')
        self.assertEqual(response, {'uploaded': True})
        headers = {
            'x-build-id': '123ea',
            'x-relative-path': 'path/to/img.png',
            'x-sha': 'sha1',
        }
        files = {
            'asset': ('path/to/img.png', 'content')
        }
        client.session.post.assert_called_with('http://basset.io/build/upload/asset', files=files, headers=headers)