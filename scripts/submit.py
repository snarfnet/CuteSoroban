#!/usr/bin/env python3
"""Submit latest build for App Store review via ASC API."""
import jwt, time, requests, sys, os

KEY_ID = os.environ.get("ASC_KEY_ID", "WDXGY9WX55")
ISSUER_ID = os.environ.get("ASC_ISSUER_ID", "2be0734f-943a-4d61-9dc9-5d9045c46fec")
BUNDLE_ID = os.environ.get("ASC_BUNDLE_ID", "com.snarfnet.catsoroban")
VERSION_STRING = os.environ.get("ASC_VERSION", "1.0")
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

def short_error(response):
    try:
        payload = response.json()
        errors = payload.get("errors") or []
        if errors:
            parts = []
            for error in errors[:3]:
                code = error.get("code", "UNKNOWN")
                detail = error.get("detail") or error.get("title") or ""
                parts.append(f"{code}: {detail}")
                associated = (error.get("meta") or {}).get("associatedErrors") or {}
                for path, path_errors in associated.items():
                    for path_error in path_errors[:3]:
                        path_code = path_error.get("code", "UNKNOWN")
                        path_detail = path_error.get("detail") or path_error.get("title") or ""
                        parts.append(f"{path} {path_code}: {path_detail}")
            return " | ".join(parts)
    except Exception:
        pass
    return response.text[:500]

def api(headers, method, path, **kwargs):
    return requests.request(
        method,
        f"https://api.appstoreconnect.apple.com/v1{path}",
        headers=headers,
        **kwargs,
    )

def reusable_review_submission_id(headers, app_id):
    r = api(headers, "GET", f"/reviewSubmissions?filter[app]={app_id}&filter[platform]=IOS&limit=200")
    if r.status_code != 200:
        print(f"Could not list review submissions: {r.status_code} {short_error(r)}")
        return None

    submissions = r.json().get("data") or []
    print(f"Found reviewSubmissions: {len(submissions)}")
    for submission in submissions:
        state = (submission.get("attributes") or {}).get("state")
        submission_id = submission.get("id")
        print(f"ReviewSubmission {submission_id} state={state}")
        if state in ("WAITING_FOR_REVIEW", "IN_REVIEW"):
            print(f"Already submitted for review: {submission_id} state={state}")
            return "already-submitted"
        if state == "READY_FOR_REVIEW":
            return submission_id
    return None

def remove_review_submission_items(headers, submission_id):
    r = api(headers, "GET", f"/reviewSubmissions/{submission_id}/items?limit=50")
    if r.status_code != 200:
        print(f"Could not list review submission items: {r.status_code} {short_error(r)}")
        return False

    items = r.json().get("data") or []
    print(f"Removing {len(items)} reviewSubmission item(s)")
    ok = True
    for item in items:
        item_id = item.get("id")
        if not item_id:
            continue
        r = api(headers, "DELETE", f"/reviewSubmissionItems/{item_id}")
        print(f"Delete reviewSubmissionItem {item_id}: {r.status_code}")
        ok = ok and r.status_code in (200, 202, 204, 404)
        if r.status_code not in (200, 202, 204, 404):
            print(f"Delete failed: {short_error(r)}")
    return ok

def add_review_submission_item(headers, submission_id, version_id):
    return api(
        headers,
        "POST",
        "/reviewSubmissionItems",
        json={
            "data": {
                "type": "reviewSubmissionItems",
                "relationships": {
                    "reviewSubmission": {"data": {"type": "reviewSubmissions", "id": submission_id}},
                    "appStoreVersion": {"data": {"type": "appStoreVersions", "id": version_id}},
                },
            }
        },
    )

def add_review_submission_item_with_retry(headers, submission_id, version_id):
    last_error = ""
    for attempt in range(20):
        r = add_review_submission_item(headers, submission_id, version_id)
        print(f"Add reviewSubmissionItem: {r.status_code}")
        if r.status_code in (200, 201):
            return True

        last_error = short_error(r)
        print(f"Add reviewSubmissionItem failed: {last_error}")
        lower_error = last_error.lower()
        if "already exists" in lower_error or "already been taken" in lower_error:
            return True
        if "screenshot_uploads_in_progress" not in lower_error and "upload" not in lower_error:
            return False

        print(f"Screenshots are still processing ({attempt + 1}/20). Waiting...")
        time.sleep(30)

    print(f"Add reviewSubmissionItem failed after waiting: {last_error}")
    return False

def finish_review_submission(headers, submission_id):
    last_error = ""
    for attempt in range(20):
        r = api(
            headers,
            "PATCH",
            f"/reviewSubmissions/{submission_id}",
            json={
                "data": {
                    "type": "reviewSubmissions",
                    "id": submission_id,
                    "attributes": {"submitted": True},
                }
            },
        )
        if r.status_code in (200, 201):
            state = r.json()["data"]["attributes"].get("state")
            print(f"Submitted for review! State: {state}")
            return True

        last_error = short_error(r)
        retryable = "try again later" in last_error.lower() or "not ready" in last_error.lower()
        if not retryable:
            print(f"Submit failed: {r.status_code} {last_error}")
            return False
        print(f"Submission not ready yet ({attempt + 1}/20). Waiting...")
        time.sleep(30)

    print(f"Submit failed after waiting: {last_error}")
    return False

def create_or_reuse_review_submission(headers, app_id):
    r = api(
        headers,
        "POST",
        "/reviewSubmissions",
        json={
            "data": {
                "type": "reviewSubmissions",
                "attributes": {"platform": "IOS"},
                "relationships": {
                    "app": {"data": {"type": "apps", "id": app_id}}
                },
            }
        },
    )
    print(f"Create reviewSubmission: {r.status_code}")
    if r.status_code in (200, 201):
        return r.json()["data"]["id"]

    print(f"Create reviewSubmission failed: {short_error(r)}")
    submission_id = reusable_review_submission_id(headers, app_id)
    if submission_id == "already-submitted":
        return submission_id
    if submission_id:
        print(f"Reusing reviewSubmission: {submission_id}")
    return submission_id

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

    r = requests.get(
        f"https://api.appstoreconnect.apple.com/v1/apps/{app_id}/appStoreVersions?filter[platform]=IOS&limit=200",
        headers=headers,
    )
    r.raise_for_status()
    all_versions = r.json().get("data", [])
    versions = [
        version for version in all_versions
        if version["attributes"].get("versionString") == VERSION_STRING
    ]
    if not versions:
        versions = [
            version for version in all_versions
            if version["attributes"].get("appStoreState") in {"PREPARE_FOR_SUBMISSION", "DEVELOPER_REJECTED", "REJECTED"}
        ]

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

    sub_id = create_or_reuse_review_submission(headers, app_id)
    if sub_id == "already-submitted":
        return 0
    if not sub_id:
        return 5

    remove_review_submission_items(headers, sub_id)
    if not add_review_submission_item_with_retry(headers, sub_id, version_id):
        return 6

    return 0 if finish_review_submission(headers, sub_id) else 7

if __name__ == "__main__":
    sys.exit(main())
