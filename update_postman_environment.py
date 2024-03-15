import boto3
import requests
from dotenv import load_dotenv
import os
import sys


# コマンドライン引数を確認
if len(sys.argv) > 1:
    env_file = sys.argv[1]
else:
    env_file = ".env"

# 指定された環境設定ファイルを読み込む
load_dotenv(env_file, override=True)

USER_POOL_ID = os.environ["USER_POOL_ID"]
CLIENT_ID = os.environ["CLIENT_ID"]
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
VALIDATION_DATA = os.environ["VALIDATION_DATA"]
POSTMAN_API_KEY = os.environ["POSTMAN_API_KEY"]
ENVIRONMENT_ID = os.environ["ENVIRONMENT_ID"]
TARGET_KEY = os.environ["TARGET_KEY"]
PROFILE_NAME = os.environ.get("PROFILE_NAME")

session = boto3.Session(profile_name=PROFILE_NAME)
client = session.client("cognito-idp")


def fetch_id_token() -> str:
    response = client.admin_initiate_auth(
        UserPoolId=USER_POOL_ID,
        ClientId=CLIENT_ID,
        AuthFlow="ADMIN_NO_SRP_AUTH",
        AuthParameters={"USERNAME": USERNAME, "PASSWORD": PASSWORD},
        ClientMetadata={"validationData": VALIDATION_DATA},
    )
    return response["AuthenticationResult"]["IdToken"]


def update_environment(
    headers: dict, url: str, environments: dict, key: str, value: str
):
    for i, item in enumerate(environments["environment"]["values"]):
        if item["key"] == key:
            environments["environment"]["values"][i] = {
                "key": key,
                "value": value,
                "enabled": True,
            }
            break
    else:
        environments["environment"]["values"].append(
            {"key": key, "value": value, "enabled": True}
        )

    # 更新した環境情報をPostmanに送信する
    update_response = requests.put(url, json=environments, headers=headers)
    return update_response.json()


id_token = fetch_id_token()

# Postman APIヘッダー
headers = {"X-Api-Key": POSTMAN_API_KEY, "Content-Type": "application/json"}

# Postman APIの設定
url = f"https://api.getpostman.com/environments/{ENVIRONMENT_ID}"

# 環境情報の取得
response = requests.get(url, headers=headers)
environments = response.json()


update_environment(
    headers=headers,
    url=url,
    environments=environments,
    key=TARGET_KEY,
    value=id_token,
)
