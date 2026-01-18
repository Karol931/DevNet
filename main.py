import os
import sys
import json
from pathlib import Path
import requests
from git import Repo, InvalidGitRepositoryError, NoSuchPathError
from datetime import datetime
from dotenv import load_dotenv


def get_orgs(api_key: str, base_url: str):
    url = f'{base_url}/organizations'
    headers = {
        'X-Cisco-Meraki-API-Key': api_key,
        'Content-Type': 'application/json',
    }
    print('Fetching organizations...')
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_devices(api_key: str, base_url: str, org_id: str):
    url = f'{base_url}/organizations/{org_id}/devices'
    headers = {
        'X-Cisco-Meraki-API-Key': api_key,
        'Content-Type': 'application/json',
    }
    print(f'Fetching devices for org {org_id}...')
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


def save_org(org: dict, repo_path: str):
    org_id = org.get('id')
    org_name = org.get('name')
    org_display_name = f'{org_id}_{org_name}'
    
    path = os.path.join(repo_path, org_display_name)
    os.makedirs(path, exist_ok=True)

    print(f'Saved organization: {org_id}_{org_name}')
    return org_display_name


def save_device(device: dict, repo_path: str, org_name: str):
    device_display_name = ''
    if device.get('serial'):
        device_display_name += device.get('serial')
    if device.get('name'):
        device_display_name += f'_{device.get('name')}'
    
    path = os.path.join(repo_path, org_name, f'{device_display_name}.json')
    if os.path.exists(path):    
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(device, f, indent=4)
    else:
        with open(path, 'x', encoding='utf-8') as f:
            json.dump(device, f, indent=4)

    print(f'Saved device: {device_display_name}')


def ensure_git_repo(path: Path) -> Repo:
    try:
        repo = Repo(path)
        print(f'Using existing git repo at: {path}')
    except (InvalidGitRepositoryError, NoSuchPathError):
        repo = Repo.init(path)
        print(f'Initialized new git repo at: {path}')
    return repo


def commit_changes(repo: Repo):
    '''Commit changes to Git repo if any exist.'''
    repo.git.add(A=True)
    if repo.is_dirty(untracked_files=True):
        message = f'Snapshot {datetime.now()}'
        repo.index.commit(message)
        print('Changes committed to Git.')
    else:
        print('No new changes to commit.')
    
def main():

    load_dotenv()
    repo_path = os.path.join(os.getcwd(), 'Backup')
    BASE_URL = os.getenv('BASE_URL')
    API_KEY = os.getenv('API_KEY')

    if not API_KEY:
        print('Please set API_KEY environment variable.')
        sys.exit(1)

    if not os.path.exists(repo_path):
        os.makedirs(repo_path)

    repo = ensure_git_repo(repo_path)

    orgs = get_orgs(API_KEY, BASE_URL)
    if not isinstance(orgs, list) or not orgs:
        print('No organizations found.')
        return

    for org in orgs:
        org_name = save_org(org, repo_path)
        devices = get_devices(API_KEY, BASE_URL, org.get('id'))

        for device in devices:
            save_device(device, repo_path, org_name)

    commit_changes(repo)


if __name__ == '__main__':
    main()
