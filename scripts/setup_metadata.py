#!/usr/bin/env python3
"""Set up App Store Connect metadata for Cute Soroban."""
import os
import sys
import time

import jwt
import requests


KEY_ID = os.environ.get("ASC_KEY_ID", "WDXGY9WX55")
ISSUER_ID = os.environ.get("ASC_ISSUER_ID", "2be0734f-943a-4d61-9dc9-5d9045c46fec")
BUNDLE_ID = os.environ.get("ASC_BUNDLE_ID", "com.snarfnet.catsoroban")
APP_ID = os.environ.get("ASC_APP_ID", "6772199409")
APP_NAME = os.environ.get("ASC_APP_NAME", "Cute Soroban")
VERSION_STRING = os.environ.get("ASC_VERSION", "1.0")
SUPPORT_URL = os.environ.get("ASC_SUPPORT_URL", "https://snarfnet.github.io/")
MARKETING_URL = os.environ.get("ASC_MARKETING_URL", SUPPORT_URL)


def get_token():
    key_paths = [
        os.path.expanduser(f"~/.appstoreconnect/private_keys/AuthKey_{KEY_ID}.p8"),
        os.path.expanduser("~/.appstoreconnect/private_keys/AuthKey_WDXGY9WX55.p8"),
        "/tmp/asc_key.p8",
    ]
    for path in key_paths:
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                key = f.read()
            break
    else:
        raise FileNotFoundError("No ASC key found")

    now = int(time.time())
    payload = {"iss": ISSUER_ID, "iat": now, "exp": now + 1200, "aud": "appstoreconnect-v1"}
    return jwt.encode(payload, key, algorithm="ES256", headers={"kid": KEY_ID})


def request(method, url, headers, **kwargs):
    response = requests.request(method, url, headers=headers, **kwargs)
    if response.status_code >= 400:
        print(f"{method} {url} -> {response.status_code}")
        print(response.text[:1000])
        response.raise_for_status()
    return response


def find_app(headers):
    if APP_ID:
        response = request("GET", f"https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}", headers)
        found_bundle_id = response.json().get("data", {}).get("attributes", {}).get("bundleId")
        if found_bundle_id and found_bundle_id != BUNDLE_ID:
            print(f"Warning: App ID {APP_ID} bundle ID is {found_bundle_id}, expected {BUNDLE_ID}")
        return APP_ID

    response = request("GET", f"https://api.appstoreconnect.apple.com/v1/apps?filter[bundleId]={BUNDLE_ID}", headers)
    apps = response.json().get("data", [])
    if apps:
        return apps[0]["id"]

    print(f"App not found in App Store Connect: {BUNDLE_ID}")
    print(f"Create the app as {APP_NAME}, SKU catsoroban.")
    return None


def ensure_version(headers, app_id):
    response = request("GET", f"https://api.appstoreconnect.apple.com/v1/apps/{app_id}/appStoreVersions", headers)
    versions = response.json().get("data", [])
    matching_versions = [
        version for version in versions
        if version["attributes"].get("versionString") == VERSION_STRING
    ]
    for version in matching_versions:
        state = version["attributes"].get("appStoreState")
        print(f"Version: {version['id']} ({state})")
        return version["id"]

    for version in versions:
        state = version["attributes"].get("appStoreState")
        if state in {"PREPARE_FOR_SUBMISSION", "DEVELOPER_REJECTED", "REJECTED"}:
            print(f"Version: {version['id']} ({state})")
            return version["id"]

    response = request(
        "POST",
        "https://api.appstoreconnect.apple.com/v1/appStoreVersions",
        headers,
        json={
            "data": {
                "type": "appStoreVersions",
                "attributes": {
                    "versionString": VERSION_STRING,
                    "platform": "IOS",
                    "copyright": "2026 snarfnet",
                    "releaseType": "AFTER_APPROVAL",
                },
                "relationships": {"app": {"data": {"type": "apps", "id": app_id}}},
            }
        },
    )
    version_id = response.json()["data"]["id"]
    print(f"Created version: {version_id}")
    return version_id


def upsert_localization(headers, version_id, locale, attrs):
    response = request(
        "GET",
        f"https://api.appstoreconnect.apple.com/v1/appStoreVersions/{version_id}/appStoreVersionLocalizations",
        headers,
    )
    for loc in response.json().get("data", []):
        if loc["attributes"].get("locale") == locale:
            request(
                "PATCH",
                f"https://api.appstoreconnect.apple.com/v1/appStoreVersionLocalizations/{loc['id']}",
                headers,
                json={"data": {"type": "appStoreVersionLocalizations", "id": loc["id"], "attributes": attrs}},
            )
            print(f"{locale} localization updated")
            return

    request(
        "POST",
        "https://api.appstoreconnect.apple.com/v1/appStoreVersionLocalizations",
        headers,
        json={
            "data": {
                "type": "appStoreVersionLocalizations",
                "attributes": {"locale": locale, **attrs},
                "relationships": {"appStoreVersion": {"data": {"type": "appStoreVersions", "id": version_id}}},
            }
        },
    )
    print(f"{locale} localization created")


def set_age_rating(headers, app_id):
    response = request("GET", f"https://api.appstoreconnect.apple.com/v1/apps/{app_id}/appInfos", headers)
    infos = response.json().get("data", [])
    if not infos:
        return

    info_id = infos[0]["id"]
    response = requests.get(f"https://api.appstoreconnect.apple.com/v1/appInfos/{info_id}/ageRatingDeclaration", headers=headers)
    if response.status_code != 200:
        print(f"Age rating not updated: {response.status_code}")
        return

    age_id = response.json()["data"]["id"]
    request(
        "PATCH",
        f"https://api.appstoreconnect.apple.com/v1/ageRatingDeclarations/{age_id}",
        headers,
        json={
            "data": {
                "type": "ageRatingDeclarations",
                "id": age_id,
                "attributes": {
                    "advertising": False,
                    "alcoholTobaccoOrDrugUseOrReferences": "NONE",
                    "contests": "NONE",
                    "gambling": False,
                    "gamblingSimulated": "NONE",
                    "gunsOrOtherWeapons": "NONE",
                    "healthOrWellnessTopics": False,
                    "lootBox": False,
                    "medicalOrTreatmentInformation": "NONE",
                    "messagingAndChat": False,
                    "parentalControls": False,
                    "profanityOrCrudeHumor": "NONE",
                    "ageAssurance": False,
                    "sexualContentGraphicAndNudity": "NONE",
                    "sexualContentOrNudity": "NONE",
                    "horrorOrFearThemes": "NONE",
                    "matureOrSuggestiveThemes": "NONE",
                    "unrestrictedWebAccess": False,
                    "userGeneratedContent": False,
                    "violenceCartoonOrFantasy": "NONE",
                    "violenceRealisticProlongedGraphicOrSadistic": "NONE",
                    "violenceRealistic": "NONE",
                },
            }
        },
    )
    print("Age rating updated")


def main():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    app_id = find_app(headers)
    if not app_id:
        return 2

    request(
        "PATCH",
        f"https://api.appstoreconnect.apple.com/v1/apps/{app_id}",
        headers,
        json={"data": {"type": "apps", "id": app_id, "attributes": {"primaryLocale": "ja"}}},
    )
    print(f"App: {app_id}")

    version_id = ensure_version(headers, app_id)
    ja_attrs = {
        "description": (
            "猫の珠を動かして計算できる、かわいいそろばんアプリです。\n\n"
            "13桁のそろばんを、指でタップまたは上下にスライドして使えます。"
            "上の珠は5、下の珠は1を表します。Resetボタンでいつでも最初の状態に戻せます。\n\n"
            "暗算やそろばん練習、数のしくみを学ぶ時間に使いやすいシンプルな道具です。"
        ),
        "keywords": "そろばん,猫,計算,暗算,算数,学習,教育,かわいい,アバカス,数字",
        "marketingUrl": MARKETING_URL,
        "supportUrl": SUPPORT_URL,
    }
    en_attrs = {
        "description": (
            "A cute cat-themed soroban app for simple abacus practice.\n\n"
            "Move cat beads across 13 columns to calculate. The top bead counts as 5, and each lower bead counts as 1. "
            "Use Reset whenever you want to clear the board.\n\n"
            "It is a simple tool for mental math practice, arithmetic learning, and getting familiar with a soroban."
        ),
        "keywords": "soroban,abacus,cat,calculator,math,cute,kawaii,education,arithmetic,counting",
        "marketingUrl": MARKETING_URL,
        "supportUrl": SUPPORT_URL,
    }
    upsert_localization(headers, version_id, "ja", ja_attrs)
    upsert_localization(headers, version_id, "en-US", en_attrs)
    set_age_rating(headers, app_id)
    print("Done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
