import os
import sys
import github3
from path import Path


def main(tag_name, asset_path):
    gh_api = github3.GitHub()
    token = os.environ["GITHUB_TOKEN"]
    gh_api.login(token=token)
    repo = gh_api.repository("dmerejkowsky", "test-deploy")
    existing_release = None
    for release in repo.releases():
        if release.name == tag_name:
            existing_release = release
            break
    if not existing_release:
        print("Creating new release for", tag_name)
        release = repo.create_release(tag_name, name=tag_name)
    else:
        print("Using existing release:", tag_name)
        release = existing_release
    with open(asset_path, "rb") as f:
        release.upload_asset("application/octet-stream", asset_path.name, f)


if __name__ == "__main__":
    tag_name = sys.argv[1]
    asset_path = Path(sys.argv[2])
    main(tag_name, asset_path)
