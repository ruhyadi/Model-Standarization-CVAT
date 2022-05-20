
import os
import streamlit as st
import git
from utils import clone_repo

def main():

    st.title('Model Registry')

    col01, col02 = st.columns([3, 1])
    with col01:
        repo_url = st.text_input('Repository (*):', 'https://github.com/ruhyadi/ruhyadi')
    with col02:
        tag = st.text_input('Branch (*):', 'v1.0')
    clone_btn = st.button('Clone')
    
    if clone_btn:
        clone_repo(repo_url)
        st.success(f'Success Clone Repository {repo_url.split("/")[3:5]}')
    
    
if __name__ == '__main__':
    main()