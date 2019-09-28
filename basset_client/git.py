from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess


def raise_on_error(process, err):
    assert process.returncode == 0, err


def parse_branch():
    process = subprocess.Popen(
        ['git rev-parse --abrev-ref HEAD'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    out, err = process.communicate()
    raise_on_error(process, err)

    return out.strip().decode('utf-8').split('\n')[0]


def parse_commit_message():
    process = subprocess.Popen(
        ['git log -1 --pretty=format:"%B"'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    out, err = process.communicate()
    raise_on_error(process, err)

    return out.strip().decode('utf-8')


def parse_commit_info():
    process = subprocess.Popen(
        ['git log -1 --pretty=format:"%H,%cn,%ce,%cI,%an,%ae,%aI"'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )
    out, err = process.communicate()

    raise_on_error(process, err)

    [
        commit_sha,
        committer_name,
        committer_email,
        commit_date,
        author_name,
        author_email,
        author_date,
    ] = out.strip().decode('utf-8').split(',')

    return [
        commit_sha,
        committer_name,
        committer_email,
        commit_date,
        author_name,
        author_email,
        author_date,
    ]


def get_git_info():
    branch = parse_branch()

    commit_message = parse_commit_message()

    [
        commit_sha,
        committer_name,
        committer_email,
        commit_date,
        author_name,
        author_email,
        author_date,
    ] = parse_commit_info()

    return [
        branch,
        commit_sha,
        commit_message,
        committer_name,
        committer_email,
        commit_date,
        author_name,
        author_email,
        author_date,
    ]
