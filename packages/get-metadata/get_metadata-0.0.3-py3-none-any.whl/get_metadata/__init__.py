#!/usr/bin/python
# -*- coding: utf-8 -*-
"""GAE/GCF等で、メタデータサーバから値を取得する

GAE GCFのPython 対応ライブラリに合わせて、Python 3.7+に対応

"""
from __future__ import annotations
import urllib.request, urllib.error


METADATA: dict[str, str] = {}

# https://cloud.google.com/appengine/docs/standard/java/accessing-instance-metadata?hl=ja
key_list: dict[str, str] = {
    # プロジェクトに割り当てられているプロジェクト番号。
    "numeric_project_id": "/computeMetadata/v1/project/numeric-project-id",
    # プロジェクトに割り当てられているプロジェクト ID。
    "project_id": "/computeMetadata/v1/project/project-id",
    # インスタンスが実行されているゾーン。
    "zone": "/computeMetadata/v1/instance/zone",
    # no comments
    "aliases": "/computeMetadata/v1/instance/service-accounts/default/aliases",
    # プロジェクトに割り当てられているデフォルトのサービス アカウントのメール。
    "email": "/computeMetadata/v1/instance/service-accounts/default/email",
    # プロジェクトのすべてのデフォルトのサービス アカウントを一覧表示します。
    "service-accounts": "/computeMetadata/v1/instance/service-accounts/default/",
    # デフォルトのサービス アカウントでサポートされているすべてのスコープを一覧表示します。
    "scopes": "/computeMetadata/v1/instance/service-accounts/default/scopes",
    # アプリケーションを他の Google Cloud APIs に認証させるための認証トークンを返します。
    "token": "/computeMetadata/v1/instance/service-accounts/default/token",
}


def get_metadata(key: str) -> str | None:
    """キーで指定したメタデータを取得する

    GAE/GCFで使用するためのもの。
    https://cloud.google.com/appengine/docs/standard/java/accessing-instance-metadata?hl=ja

    Args:
        key (str): メタデータのURL、または以下に示すエイリアス

    Returns:
        str: メタデータサーバからの応答内容

    Note:
        keyはメタデータサーバのURL(http://metadata.google.internal を除いたもの)
        または、以下のdictのkeyを指定すると、そのvalueが指定されたとみなす

        プロジェクトに割り当てられているプロジェクト番号。
        numeric_project_id: /computeMetadata/v1/project/numeric-project-id"

        プロジェクトに割り当てられているプロジェクト ID。
        project_id: /computeMetadata/v1/project/project-id

        インスタンスが実行されているゾーン。
        zone: /computeMetadata/v1/instance/zone

        no comments
        aliases: /computeMetadata/v1/instance/service-accounts/default/aliases

        プロジェクトに割り当てられているデフォルトのサービス アカウントのメール。
        email: /computeMetadata/v1/instance/service-accounts/default/email

        プロジェクトのすべてのデフォルトのサービス アカウントを一覧表示します。
        service-accounts: /computeMetadata/v1/instance/service-accounts/default/

        デフォルトのサービス アカウントでサポートされているすべてのスコープを一覧表示します。
        scopes: /computeMetadata/v1/instance/service-accounts/default/scopes

        アプリケーションを他の Google Cloud APIs に認証させるための認証トークンを返します。
        token: /computeMetadata/v1/instance/service-accounts/default/token

    """
    global METADATA, key_list
    if key in key_list.keys():
        url = key_list[key]
    else:
        url = key

    if url not in METADATA.keys():

        headers = {"Metadata-Flavor": "Google"}

        req = urllib.request.Request(
            "http://metadata.google.internal" + url, headers=headers
        )

        try:
            with urllib.request.urlopen(req) as res:
                METADATA[key] = res.read().decode()
        except urllib.error.HTTPError as err:
            print(f"get_metadata: urllib: err.code = {err.code}")
            return None
        except urllib.error.URLError as err:
            print(f"get_metadata: urllib: err.reason = {err.reason}")
            return None

    return METADATA[key]
