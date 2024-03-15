# cognito_api_postman

API Gatewayの認証をCognitoで行っているシステムがあり、リクエストにPostmanを使っていることを想定しています。

これまでID Tokenを手作業で取得し、Postmanの環境変数に入力していた部分を省略化するものになります。

## 流れ

1. PythonのスクリプトでCognito認証を行い、ID TokenをPostmanの環境変数へ登録
2. PostmanのPre-Scriptを使ってリクエスト前に最新のID Tokenを参照
