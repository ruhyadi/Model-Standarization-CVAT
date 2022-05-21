
from pathlib import Path
import shutil
import git
import os
import json
import requests

def clone_repo(url, force=True):
    # https://github.com/ruhyadi/Model-Standarization-CVAT
    username = url.split('/')[3]
    reponame = url.split('/')[4]
    repodir = Path(os.getcwd()) / username / reponame

    if not os.path.isdir(repodir):
        os.makedirs(repodir)
    elif force:
        shutil.rmtree(repodir)
        os.makedirs(repodir)
    try:
        repo = git.Repo.clone_from(url, to_path=repodir)
    except:
        print('[INFO] Repository already exist')

def create_release(title, tag, branch, desc, git_url, token):

    username = git_url.split('/')[3]
    reponame = git_url.split('/')[4]

    dict_ = {
        "tag_name":f"{tag}",
        "target_commitish":f"{branch}",
        "name":f"{title}",
        "body":f"{desc}",
        "draft":False,
        "prerelease":False,
        "generate_release_notes":False
    }

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}",
    }

    release_json = json.dumps(dict_)

    release = requests.post(
        f'https://api.github.com/repos/{username}/{reponame}/releases',
        headers=headers,
        data=release_json
        )

    upload_url = release.json()['upload_url']

    return upload_url

def upload_assets(filename, upload_url, token):

    upload_url_ = upload_url.split('{')[0]

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}",
        "Content-Type": "image/png"
        # "Content-Type": "application/zip"
    }

    assets_dict = {
        "name" : filename,
        "label" : filename
    }
    # upload_url_ = 'https://uploads.github.com/repos/ruhyadi/sample-release/releases/66158665/assets'
    response_assets = requests.post(
        f'{upload_url_}?name={filename}',
        headers=headers,
        data=json.dumps(assets_dict)
    )

    print(response_assets)
    print(response_assets.json())

if __name__ == '__main__':
    pass

    # import requests
    # import json

    # dict_ = {
    #     "tag_name":"v1.3",
    #     "target_commitish":"main",
    #     "name":"v1.3",
    #     "body":"Sample Release",
    #     "draft":False,
    #     "prerelease":False,
    #     "generate_release_notes":False
    # }

    # headers = {
    #     "Accept": "application/vnd.github.v3+json",
    #     "Authorization": "token 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",
    #     "Content-Type": "application/zip"
    # }

    # # release_json = json.dumps(dict_)

    # # release = requests.post(
    # #     'https://api.github.com/repos/ruhyadi/sample-release/releases',
    # #     headers=headers,
    # #     data=release_json
    # #     )

    # # print(release)
    # # print(release.json())

    # assets_dict = {
    #     "name" : "sample003.zip",
    #     "label" : "sample003"
    # }

    # assets = requests.post(
    #     'https://uploads.github.com/repos/ruhyadi/sample-release/releases/67404165/assets?name=sample003.zip',
    #     headers=headers,
    #     data=json.dumps(assets_dict)
    # )

    # # print(release.json())
    # print(assets)
    # print(assets.json())