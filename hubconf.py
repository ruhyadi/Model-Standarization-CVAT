
import os
import torch
import git
from pathlib import Path

def _create(name: str = None, tag: str = None, device: str = 'cpu'):

    # TODO: add your own weights list with extension
    weights_list = ['weights001.pt', 'weights002.ckpt']
    idx = [x.split('.')[0] for x in weights_list].index(name)
    assert name in [x.split('.')[0] for x in weights_list], \
        f'[INFO] not found, try: {weights_list}'

    repo = git.Repo(os.getcwd())
    repo_url = Path(repo.remotes.origin.url)
    repo_tag = tag
    if tag is None:
        repo_tag = repo.tags[-1] # last tag
    weights_url = repo_url / "releases/download" / str(repo_tag) / str(weights_list[idx])
    # https:/github.com/username/repo/releases/download/tags/model.pt

    # TODO: load your own model configuration
    model = Model()
    model.load_state_dict(
        torch.hub.load_state_dict_from_url(weights_url, map_location=device)['model']
        )

    return model.to(device).eval()

# TODO: define your model name
def custom(imgsize=640, device='cpu'):
    # load custom model
    return _create('custom', tag='v1.0', device=device)
    
if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description="Torch Hub Testing")
    parser.add_argument('--repository', type=str, required=True, help='Repository, username/reponame')
    parser.add_argument('--tag', type=str, required=True, help='Release tag')
    args = parser.parse_args()

    weights = torch.hub.list(f'{args.repository}:{args.tag}', force_reload=True)

    for weight in weights:
        model = torch.hub.load(f'{args.repository}:{args.tag}', weight)
        print(f'[INFO] Success load {weight.upper()}')
