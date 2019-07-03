import unittest

from mock import patch, mock_open

from basset_client.basset import Basset

HTML_CONTENT = '<html><head></head><body><img src="img.png"></body></html>'

class BassetTest(unittest.TestCase):
    @patch('basset_client.basset.Client')
    @patch('basset_client.basset.get_git_info')
    @patch('basset_client.basset.get_assets')
    @patch('basset_client.basset.Basset.upload_assets')
    def test_build_start(self, mock_upload, mock_assets, mock_info, mock_client):
        mock_assets.return_value = {
            'static/file.js': '1',
            'static/otherfile.js': '2',
            'static/img/img.png': '3',
            'static/img/other_img.png': '4',
        }
        mock_info.return_value =  [
            'master',
            'sha123',
            'message',
            'commiterName',
            'committerEmail',
            'commitDate',
            'authorName',
            'authorEmail',
            'authorDate',
        ]
        missing_assets = {
            'static/img/img.png': '3',
            'static/img/other_img.png': '4',
        }
        client = mock_client.return_value
        client.build_start.return_value = [ missing_assets, '134-ea', ]
        #client.upload_snapshot.return_value = {"submitted": True}

        basset = Basset('token', 'dir', 'basset_url')
        basset.build_start()
        data = {
            'branch': 'master',
            'commitSha': 'sha123',
            'commitMessage': 'message',
            'committerName': 'commiterName',
            'committerEmail': 'committerEmail',
            'commitDate': 'commitDate',
            'authorName': 'authorName',
            'authorEmail': 'authorEmail',
            'authorDate': 'authorDate',
            'assets': {
                'static/file.js': '1',
                'static/otherfile.js': '2',
                'static/img/other_img.png': '4',
                'static/img/img.png': '3'
            }
        }
        client.build_start.assert_called_with(data)
        basset.upload_assets.assert_called_with({
            'static/img/img.png': '3',
            'static/img/other_img.png': '4',
        })

    @patch('basset_client.basset.Client')
    def test_build_finish(self, mock_client):
        client = mock_client.return_value
        client.build_id = 'ea123'
        client.build_finish.return_value = {"submitted": True}

        basset = Basset('token', 'dir', 'basset_url')
        basset.build_finish()

    @patch('basset_client.basset.Client')
    def test_build_finish_error(self, mock_client):
        client = mock_client.return_value
        client.build_id = 'ea123'
        client.build_finish.return_value = {"submitted": False}

        basset = Basset('token', 'dir', 'basset_url')
        with self.assertRaises(AssertionError):
            basset.build_finish()

    @patch('basset_client.basset.Client')
    @patch('basset_client.basset.generate_hash')
    def test_upload_snapshot(self, mock_hash, mock_client):
        mock_hash.return_value = '123ea'
        client = mock_client.return_value
        client.build_id = 'ea123'
        client.upload_snapshot.return_value = {"uploaded": True}
        snapshot = [
            '1280',
            'test snapshot',
            'browser',
            'hide_selectors',
            'selectors',
        ]
        basset = Basset('token', 'dir', 'basset_url')
        basset.upload_snapshot_source(snapshot, HTML_CONTENT)
        client.upload_snapshot.assert_called_with(snapshot, 'test snapshot.html', '123ea', HTML_CONTENT)


    @patch('basset_client.basset.Client')
    @patch('basset_client.basset.generate_hash')
    @patch('basset_client.basset.open', new_callable=mock_open, read_data=HTML_CONTENT)
    def test_upload_snapshot_file(self, mock_open, mock_hash, mock_client):
        mock_hash.return_value = '123ea'
        client = mock_client.return_value
        client.build_id = 'ea123'
        client.upload_snapshot.return_value = {"uploaded": True}
        snapshot = [
            '1280',
            'test snapshot',
            'browser',
            'hide_selectors',
            'selectors',
        ]
        basset = Basset('token', 'dir', 'basset_url')
        basset.upload_snapshot_file(snapshot, 'path/to/mock.html')
        client.upload_snapshot.assert_called_with(snapshot, 'test snapshot.html', '123ea', HTML_CONTENT)