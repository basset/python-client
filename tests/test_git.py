import unittest

from mock import patch

from basset_client.git import get_git_info, parse_branch, parse_commit_message, parse_commit_info


class GitTest(unittest.TestCase):
    @patch('basset_client.git.subprocess.Popen')
    def test_parse_branch(self, mock_popen):
        process = mock_popen.return_value
        process.returncode = 0
        process.communicate.return_value = [b'master', None]
        branch = parse_branch()
        self.assertEqual(branch, 'master')

    @patch('basset_client.git.subprocess.Popen')
    def test_error_parse_branch(self, mock_popen):
        process = mock_popen.return_value
        process.returncode = -1
        process.communicate.return_value = [None, 'oh snap']
        with self.assertRaises(AssertionError) as err:
            _branch = parse_branch()
            self.assertEqual(err.message, "oh snap")

    @patch('basset_client.git.subprocess.Popen')
    def test_parse_commit_message(self, mock_popen):
        process = mock_popen.return_value
        process.returncode = 0
        process.communicate.return_value = [b'this\nis\na\ntest', None]
        message = parse_commit_message()
        assert message == 'this\nis\na\ntest'

    @patch('basset_client.git.subprocess.Popen')
    def test_parse_git_info(self, mock_popen):
        process = mock_popen.return_value
        process.returncode = 0
        process.communicate.return_value = [
            b'sha1234,commiterName,committerEmail,commitDate,authorName,authorEmail,authorDate', None]
        [
            commit_sha,
            committer_name,
            committer_email,
            commit_date,
            author_name,
            author_email,
            author_date,
        ] = parse_commit_info()
        self.assertEqual(commit_sha, 'sha1234')
        self.assertEqual(committer_name, 'commiterName')
        self.assertEqual(committer_email, 'committerEmail')
        self.assertEqual(commit_date, 'commitDate')
        self.assertEqual(author_name, 'authorName')
        self.assertEqual(author_email, 'authorEmail')
        self.assertEqual(author_date, 'authorDate')

    @patch('basset_client.git.parse_branch')
    @patch('basset_client.git.parse_commit_message')
    @patch('basset_client.git.parse_commit_info')
    def test_get_git_info(self, mock_info, mock_message, mock_branch):
        mock_info.return_value = [
            'sha123',
            'commiterName',
            'committerEmail',
            'commitDate',
            'authorName',
            'authorEmail',
            'authorDate',
        ]
        mock_message.return_value = 'message'
        mock_branch.return_value = 'master'

        info = get_git_info()
        self.assertListEqual(info, [
            'master',
            'sha123',
            'message',
            'commiterName',
            'committerEmail',
            'commitDate',
            'authorName',
            'authorEmail',
            'authorDate',

        ])
