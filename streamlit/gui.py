
from io import StringIO
import os
import streamlit as st
import git
from utils import clone_repo, create_release, upload_assets

def main():

    st.title('Model Registry')

    st.subheader('Repository')
    col01, col02, col03 = st.columns([3, 1, 1])
    with col01:
        repo_url = st.text_input('Repository (*):', 'https://github.com/ruhyadi/sample-release')
    with col02:
        token = st.text_input('Token (*):', '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')
    with col03:
        branch = st.text_input('Branch (*):', 'main')
    
    st.subheader('Releases')
    col11, col12, col13 = st.columns([2, 2, 1])
    with col11:
        release_title = st.text_input('Release title: (*)', 'v1.0 release')
    with col12:
        release_desc = st.text_input('Release description: (*)', 'Release assets v1.0')
    with col13:
        release_tag = st.text_input('Release Tag (*):', 'v1.0')

    assets = st.file_uploader('Model Asset(s) (*):', accept_multiple_files=True)

    assets_btn = st.button('Upload Assets')

    if assets_btn:
        clone_repo(repo_url)
        st.success(f'Success Clone Repository {repo_url.split("/")[3:5]}')

        upload_url = create_release(release_title, release_tag, branch, release_desc, repo_url, token)
        st.success(f'Success Release {release_tag}')

        for asset in assets:
            filename = asset.name
            upload_assets(filename, upload_url, token)

if __name__ == '__main__':
    main()