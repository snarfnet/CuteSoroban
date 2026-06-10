#!/usr/bin/env python3
import hashlib
import os
import sys
import time

import jwt
import requests


KEY_ID = os.environ.get("ASC_KEY_ID", "WDXGY9WX55")
ISSUER = os.environ.get("ASC_ISSUER_ID", "2be0734f-943a-4d61-9dc9-5d9045c46fec")
APP_ID = os.environ.get("ASC_APP_ID", "6772199409")
KEY_PATHS = [
    os.environ.get("ASC_P8_PATH"),
    "/tmp/asc_key.p8",
    os.path.expanduser(f"~/.appstoreconnect/private_keys/AuthKey_{KEY_ID}.p8"),
]


def read_key():
    for path in KEY_PATHS:
        if path and os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                return f.read()
    raise FileNotFoundError("No ASC key found")


P8 = read_key()


def make_token():
    now = int(time.time())
    return jwt.encode(
        {"iss": ISSUER, "iat": now, "exp": now + 1200, "aud": "appstoreconnect-v1"},
        P8,
        algorithm="ES256",
        headers={"kid": KEY_ID},
    )


def headers():
    return {"Authorization": f"Bearer {make_token()}", "Content-Type": "application/json"}


def api(method, path, **kwargs):
    response = requests.request(
        method,
        f"https://api.appstoreconnect.apple.com/v1{path}",
        headers=headers(),
        **kwargs,
    )
    if response.status_code >= 400:
        raise RuntimeError(f"{method} {path} failed {response.status_code}: {response.text[:1000]}")
    return response


def list_all(path):
    items = []
    while path:
        payload = api("GET", path).json()
        items.extend(payload.get("data", []))
        next_url = payload.get("links", {}).get("next")
        path = next_url.split("/v1", 1)[1] if next_url and "/v1" in next_url else None
    return items


def get_or_create_set(loc_id, display_type):
    sets = list_all(
        f"/appStoreVersionLocalizations/{loc_id}/appScreenshotSets?filter[screenshotDisplayType]={display_type}&limit=200"
    )
    if sets:
        set_id = sets[0]["id"]
        for screenshot in list_all(f"/appScreenshotSets/{set_id}/appScreenshots?limit=200"):
            api("DELETE", f"/appScreenshots/{screenshot['id']}")
        return set_id

    response = api(
        "POST",
        "/appScreenshotSets",
        json={
            "data": {
                "type": "appScreenshotSets",
                "attributes": {"screenshotDisplayType": display_type},
                "relationships": {
                    "appStoreVersionLocalization": {
                        "data": {"type": "appStoreVersionLocalizations", "id": loc_id}
                    }
                },
            }
        },
    )
    return response.json()["data"]["id"]


def upload_screenshot(set_id, filepath):
    with open(filepath, "rb") as f:
        file_data = f.read()

    response = api(
        "POST",
        "/appScreenshots",
        json={
            "data": {
                "type": "appScreenshots",
                "attributes": {
                    "fileName": os.path.basename(filepath),
                    "fileSize": len(file_data),
                },
                "relationships": {
                    "appScreenshotSet": {"data": {"type": "appScreenshotSets", "id": set_id}}
                },
            }
        },
    )
    screenshot = response.json()["data"]
    for operation in screenshot["attributes"]["uploadOperations"]:
        upload_headers = {h["name"]: h["value"] for h in operation["requestHeaders"]}
        offset = operation["offset"]
        length = operation["length"]
        chunk = file_data[offset : offset + length]
        upload = requests.put(operation["url"], headers=upload_headers, data=chunk)
        if upload.status_code not in (200, 201):
            raise RuntimeError(f"Screenshot chunk upload failed: {upload.status_code}")

    checksum = hashlib.md5(file_data).hexdigest()
    api(
        "PATCH",
        f"/appScreenshots/{screenshot['id']}",
        json={
            "data": {
                "type": "appScreenshots",
                "id": screenshot["id"],
                "attributes": {"uploaded": True, "sourceFileChecksum": checksum},
            }
        },
    )
    print(f"  Uploaded {os.path.basename(filepath)}")


def latest_editable_version_id():
    versions = list_all(f"/apps/{APP_ID}/appStoreVersions?filter[platform]=IOS&limit=200")
    editable_states = {"PREPARE_FOR_SUBMISSION", "DEVELOPER_REJECTED", "REJECTED"}
    for version in versions:
        if version["attributes"].get("appStoreState") in editable_states:
            return version["id"]
    if versions:
        return versions[0]["id"]
    raise RuntimeError("No App Store version found")


def main():
    screenshot_dir = sys.argv[1] if len(sys.argv) > 1 else "screenshots"
    screenshots = {
        "APP_IPHONE_67": ["iphone_67_01.png", "iphone_67_02.png", "iphone_67_03.png"],
        "APP_IPAD_PRO_3GEN_129": ["ipad_129_01.png", "ipad_129_02.png", "ipad_129_03.png"],
    }

    version_id = latest_editable_version_id()
    locs = list_all(f"/appStoreVersions/{version_id}/appStoreVersionLocalizations?limit=200")
    for loc in locs:
        loc_id = loc["id"]
        print(f"Processing locale: {loc['attributes']['locale']}")
        for display_type, filenames in screenshots.items():
            paths = [os.path.join(screenshot_dir, name) for name in filenames]
            existing_paths = [path for path in paths if os.path.exists(path)]
            if not existing_paths:
                continue
            set_id = get_or_create_set(loc_id, display_type)
            for path in existing_paths:
                upload_screenshot(set_id, path)

    print("Done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
