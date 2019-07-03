import unittest

from mock import patch, MagicMock

from basset_client.assets import get_assets, ignore_file, walk_assets


class AssetsTest(unittest.TestCase):
    @patch('basset_client.assets.IGNORE_FILE_EXISTS', ['.js', '.map'])
    def test_ignore_file(self):
        self.assertTrue(ignore_file('path/to/file/test.js'))
        self.assertTrue(ignore_file('path/to/file/test.js.map'))
        self.assertFalse(ignore_file('path/to/file/other file.txt'))

    @patch('basset_client.assets.generate_file_hash')
    @patch('basset_client.assets.os.walk')
    @patch('basset_client.assets.ignore_file')
    def test_walk_assets(self, ignore_file_mock, walk_mock, hash_mock):
        ignore_file_mock.return_value = False
        walk_mock.side_effect = iter(
            [
                iter([('/var/basset', ['img'], ['file.js', 'otherfile.js']), ]),
                iter([('/var/basset/img', [], ['img.png', 'other_img.png']), ])
            ]
        )
        hash_mock.return_value = '123a'
        results = walk_assets('/var/basset', 'static/')
        self.assertEqual(len(results), 4)
        self.assertListEqual(results, [
            ['static/file.js', '123a'],
            ['static/otherfile.js', '123a'],
            ['static/img/img.png', '123a'],
            ['static/img/other_img.png', '123a'],
        ])

    @patch('basset_client.assets.generate_file_hash')
    @patch('basset_client.assets.os.walk')
    @patch('basset_client.assets.ignore_file')
    def test_get_assets(self, ignore_file_mock, walk_mock, hash_mock):
        ignore_file_mock.return_value = False
        walk_mock.side_effect = iter(
            [
                iter([('/var/basset', ['img'], ['file.js', 'otherfile.js']), ]),
                iter([('/var/basset/img', [], ['img.png', 'other_img.png']), ])
            ]
        )
        hash_mock.side_effect = iter(['1', '2', '3', '4'])
        assets = get_assets('/var/basset', 'static/')
        self.assertDictEqual(assets, {
            'static/file.js': '1',
            'static/otherfile.js': '2',
            'static/img/img.png': '3',
            'static/img/other_img.png': '4',
        })
