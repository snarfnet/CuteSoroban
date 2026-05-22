#!/usr/bin/env python3
"""Set up ASC metadata for Cute Soroban."""
import jwt, time, requests, os

KEY_ID = 'WDXGY9WX55'
ISSUER_ID = '2be0734f-943a-4d61-9dc9-5d9045c46fec'
APP_ID = '6772150689'

key_path = os.path.expanduser('~/.appstoreconnect/private_keys/AuthKey_WDXGY9WX55.p8')
with open(key_path) as f:
    key = f.read()

now = int(time.time())
payload = {'iss': ISSUER_ID, 'iat': now, 'exp': now + 1200, 'aud': 'appstoreconnect-v1'}
token = jwt.encode(payload, key, algorithm='ES256', headers={'kid': KEY_ID})
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

# Set category
r = requests.patch(f'https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}', headers=headers, json={
    'data': {
        'type': 'apps',
        'id': APP_ID,
        'attributes': {'primaryLocale': 'ja'},
        'relationships': {
            'primaryCategory': {'data': {'type': 'appCategories', 'id': 'EDUCATION'}},
            'secondaryCategory': {'data': {'type': 'appCategories', 'id': 'UTILITIES'}}
        }
    }
})
print(f'Category: {r.status_code}')

# Get version
r = requests.get(f'https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}/appStoreVersions', headers=headers)
versions = r.json().get('data', [])
if not versions:
    r = requests.post('https://api.appstoreconnect.apple.com/v1/appStoreVersions', headers=headers, json={
        'data': {
            'type': 'appStoreVersions',
            'attributes': {
                'versionString': '1.0',
                'platform': 'IOS',
                'copyright': '2026 snarfnet',
                'releaseType': 'AFTER_APPROVAL'
            },
            'relationships': {'app': {'data': {'type': 'apps', 'id': APP_ID}}}
        }
    })
    print(f'Create version: {r.status_code}')
    if r.status_code in (200, 201):
        version_id = r.json()['data']['id']
    else:
        print(r.text[:500])
        exit()
else:
    version_id = versions[0]['id']
    print(f'Version: {version_id}')

# Get localizations
r = requests.get(f'https://api.appstoreconnect.apple.com/v1/appStoreVersions/{version_id}/appStoreVersionLocalizations', headers=headers)
locs = r.json().get('data', [])
ja_loc = None
en_loc = None
for loc in locs:
    locale = loc['attributes']['locale']
    if locale == 'ja':
        ja_loc = loc['id']
    elif locale.startswith('en'):
        en_loc = loc['id']

desc_ja = (
    "パステルカラーの宝石珠で楽しむ、かわいいそろばんアプリ。\n\n"
    "13桁のそろばんを指でなぞって計算。パステルレインボーの珠がキラキラ光り、"
    "動かすたびにぷるんとバウンス。\n\n"
    "使い方はシンプル:\n"
    "- 珠をタップまたはスライドで上下に動かす\n"
    "- 上の珠は5、下の珠は1を表す\n"
    "- Resetボタンで全珠リセット\n\n"
    "暗算の練習に。算数の学習に。そろばん教室の補助ツールに。\n"
    "見た目がかわいいから、触っているだけで楽しい。"
)

desc_en = (
    "A cute pastel abacus app with sparkling crystal beads.\n\n"
    "Slide 13 columns of rainbow-colored beads to calculate. "
    "Each bead bounces with a satisfying pop when moved.\n\n"
    "How to use:\n"
    "- Tap or slide beads up and down\n"
    "- Top bead = 5, bottom beads = 1 each\n"
    "- Reset button clears all beads\n\n"
    "Perfect for mental math practice, learning arithmetic, "
    "or as a soroban classroom tool.\n"
    "So cute you will want to keep playing with it."
)

keywords_ja = "そろばん,算盤,計算,暗算,かわいい,パステル,算数,学習,教育,知育"
keywords_en = "soroban,abacus,calculator,math,cute,pastel,kawaii,education,arithmetic,counting"

loc_attrs = {
    'description': desc_ja,
    'keywords': keywords_ja,
    'marketingUrl': 'https://snarfnet.github.io/',
    'supportUrl': 'https://snarfnet.github.io/'
}

if ja_loc:
    r = requests.patch(f'https://api.appstoreconnect.apple.com/v1/appStoreVersionLocalizations/{ja_loc}', headers=headers, json={
        'data': {'type': 'appStoreVersionLocalizations', 'id': ja_loc, 'attributes': loc_attrs}
    })
    print(f'JA loc update: {r.status_code}')
else:
    r = requests.post(f'https://api.appstoreconnect.apple.com/v1/appStoreVersions/{version_id}/appStoreVersionLocalizations', headers=headers, json={
        'data': {
            'type': 'appStoreVersionLocalizations',
            'attributes': dict(locale='ja', **loc_attrs),
            'relationships': {'appStoreVersion': {'data': {'type': 'appStoreVersions', 'id': version_id}}}
        }
    })
    print(f'JA loc create: {r.status_code}')

en_attrs = {
    'description': desc_en,
    'keywords': keywords_en,
    'marketingUrl': 'https://snarfnet.github.io/',
    'supportUrl': 'https://snarfnet.github.io/'
}

if en_loc:
    r = requests.patch(f'https://api.appstoreconnect.apple.com/v1/appStoreVersionLocalizations/{en_loc}', headers=headers, json={
        'data': {'type': 'appStoreVersionLocalizations', 'id': en_loc, 'attributes': en_attrs}
    })
    print(f'EN loc update: {r.status_code}')
else:
    r = requests.post(f'https://api.appstoreconnect.apple.com/v1/appStoreVersions/{version_id}/appStoreVersionLocalizations', headers=headers, json={
        'data': {
            'type': 'appStoreVersionLocalizations',
            'attributes': dict(locale='en-US', **en_attrs),
            'relationships': {'appStoreVersion': {'data': {'type': 'appStoreVersions', 'id': version_id}}}
        }
    })
    print(f'EN loc create: {r.status_code}')

# Age rating
r = requests.get(f'https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}/appInfos', headers=headers)
infos = r.json().get('data', [])
if infos:
    info_id = infos[0]['id']
    r = requests.get(f'https://api.appstoreconnect.apple.com/v1/appInfos/{info_id}/ageRatingDeclaration', headers=headers)
    if r.status_code == 200:
        age_id = r.json()['data']['id']
        r = requests.patch(f'https://api.appstoreconnect.apple.com/v1/ageRatingDeclarations/{age_id}', headers=headers, json={
            'data': {
                'type': 'ageRatingDeclarations',
                'id': age_id,
                'attributes': {
                    'alcoholTobaccoOrDrugUseOrReferences': 'NONE',
                    'contests': 'NONE',
                    'gamblingAndContests': False,
                    'gambling': False,
                    'medicalOrTreatmentInformation': 'NONE',
                    'profanityOrCrudeHumor': 'NONE',
                    'sexualContentOrNudity': 'NONE',
                    'horrorOrFearThemes': 'NONE',
                    'matureOrSuggestiveThemes': 'NONE',
                    'violenceCartoonOrFantasy': 'NONE',
                    'violenceRealisticProlonged': 'NONE',
                    'violenceRealistic': 'NONE',
                    'unrestrictedWebAccess': False,
                    'seventeenPlus': False
                }
            }
        })
        print(f'Age rating: {r.status_code}')

print('Done!')
