#!/usr/bin/env python3
"""Submit latest build for App Store review via ASC API."""
import jwt, time, requests, sys, os

KEY_ID = os.environ.get("ASC_KEY_ID", "WDXGY9WX55")
ISSUER_ID = os.environ.get("ASC_ISSUER_ID", "2be0734f-943a-4d61-9dc9-5d9045c46fec")
BUNDLE_ID = os.environ.get("ASC_BUNDLE_ID", "com.snarfnet.cutesoroban")
APP_ID = os.environ.get("ASC_APP_ID", "6772199409")

def get_token():
    key_paths = [
        os.path.expanduser("~/.appstoreconnect/private_keys/AuthKey_WDXGY9WX55.p8"),
        "/tmp/asc_key.p8",
    ]
    for p in key_paths:
        if os.path.exists(p):
            with open(p) as f:
                key = f.read()
            break
    else:
        raise FileNotFoundError("No ASC key found")

    now = int(time.time())
    payload = {"iss": ISSUER_ID, "iat": now, "exp": now + 1200, "aud": "appstoreconnect-v1"}
    return jwt.encode(payload, key, algorithm="ES256", headers={"kid": KEY_ID})

def main():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    build_number = sys.argv[1] if len(sys.argv) > 1 else None

    if APP_ID:
        r = requests.get(f"https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}", headers=headers)
        r.raise_for_status()
        app_id = APP_ID
    else:
        r = requests.get(f"https://api.appstoreconnect.apple.com/v1/apps?filter[bundleId]={BUNDLE_ID}", headers=headers)
        r.raise_for_status()
        apps = r.json()["data"]
        if not apps:
            print(f"App not found: {BUNDLE_ID}")
            print("Create the app in App Store Connect first, then upload a build.")
            return 2
        app_id = apps[0]["id"]
    print(f"App ID: {app_id}")

    url = f"https://api.appstoreconnect.apple.com/v1/builds?filter[app]={app_id}&sort=-uploadedDate&limit=5"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    builds = r.json()["data"]

    target_build = None
    for b in builds:
        v = b["attributes"].get("version")
        state = b["attributes"].get("processingState")
        print(f"  Build {v}: {state}")
        if state == "VALID":
            if build_number and v != build_number:
                continue
            target_build = b
            break

    if not target_build:
        print("No valid build found, waiting for processing...")
        for attempt in range(20):
            time.sleep(30)
            r = requests.get(url, headers=headers)
            builds = r.json()["data"]
            for b in builds:
                if b["attributes"].get("processingState") == "VALID":
                    if build_number and b["attributes"].get("version") != build_number:
                        continue
                    target_build = b
                    break
            if target_build:
                break
            print(f"  Waiting... ({attempt+1}/20)")

    if not target_build:
        print("Build not ready after 10 minutes")
        return 3

    build_id = target_build["id"]
    print(f"Using build: {target_build['attributes'].get('version')} ({build_id})")

    versions = []
    for state in ("PREPARE_FOR_SUBMISSION", "DEVELOPER_REJECTED", "REJECTED"):
        r = requests.get(
            f"https://api.appstoreconnect.apple.com/v1/apps/{app_id}/appStoreVersions?filter[appStoreState]={state}",
            headers=headers,
        )
        r.raise_for_status()
        versions.extend(r.json().get("data", []))

    if versions:
        version_id = versions[0]["id"]
    else:
        print("No editable App Store version found")
        return 4

    r = requests.patch(
        f"https://api.appstoreconnect.apple.com/v1/appStoreVersions/{version_id}/relationships/build",
        headers=headers,
        json={"data": {"type": "builds", "id": build_id}}
    )
    print(f"Attach build: {r.status_code}")

    r = requests.post(
        "https://api.appstoreconnect.apple.com/v1/reviewSubmissions",
        headers=headers,
        json={
            "data": {
                "type": "reviewSubmissions",
                "attributes": {"platform": "IOS"},
                "relationships": {
                    "app": {"data": {"type": "apps", "id": app_id}}
                }
            }
        }
    )
    print(f"Submit for review: {r.status_code}")
    if r.status_code in (200, 201):
        sub_id = r.json()["data"]["id"]
        requests.post(
            "https://api.appstoreconnect.apple.com/v1/reviewSubmissionItems",
            headers=headers,
            json={
                "data": {
                    "type": "reviewSubmissionItems",
                    "relationships": {
                        "reviewSubmission": {"data": {"type": "reviewSubmissions", "id": sub_id}},
                        "appStoreVersion": {"data": {"type": "appStoreVersions", "id": version_id}}
                    }
                }
            }
        )
        requests.patch(
            f"https://api.appstoreconnect.apple.com/v1/reviewSubmissions/{sub_id}",
            headers=headers,
            json={"data": {"type": "reviewSubmissions", "id": sub_id, "attributes": {"submitted": True}}}
        )
        print("Submitted for review!")
        return 0
    else:
        print(r.text[:500])
        return 5

if __name__ == "__main__":
    sys.exit(main())
