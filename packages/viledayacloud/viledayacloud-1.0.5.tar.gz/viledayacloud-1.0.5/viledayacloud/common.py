# coding=utf-8
"""
Common shared functions and classes
"""
from json import dumps, loads
from typing import Any, Dict, Optional

import aiohttp


async def getsecret(sname: str, fid: str, atoken: str) -> Optional[str]:
    """
    Returns the secret value from Yandex Cloud Lockbox

    :param sname: name of a secret
    :param fid: folderId of the cloud folder
    :param atoken: access token for Lockbox API
    :return: secret contents
    """
    async with aiohttp.ClientSession(raise_for_status=True) as s:
        async with s.get(f"https://lockbox.api.cloud.yandex.net/lockbox/v1/secrets?folderId={fid}",
                         headers={"Authorization": f"Bearer {atoken}"}) as r:
            _list = await r.json()
            for _s_item in _list["secrets"]:
                if _s_item["name"] == sname:
                    _sid = _s_item["id"]
                    async with s.get(f"https://payload.lockbox.api.cloud.yandex.net/lockbox/v1/secrets/{_sid}/payload",
                                     headers={"Authorization": f"Bearer {atoken}"}) as r:
                        _secret = await r.json()
                        return _secret["entries"][0]["textValue"]
    return None


async def tgmjsoncall(tgs: aiohttp.ClientSession,
                      tgmethod: str,
                      tgtoken: str,
                      tgjson: Dict[str: Any]) -> Optional[Dict[str: Any]]:
    """
    Call the Telegram Bot API method with application/json formatted payload

    :param tgs: aiohttp session to use
    :param tgmethod:  method name
    :param tgtoken: bot token string
    :param tgjson: dict object with JSON to send to the Bot API
    :return: method result received from Telegram Bot API deserialized iton dict with loads()
    """
    async with tgs.post(f"https://api.telegram.org/bot{tgtoken}/{tgmethod}",
                        headers={"Content-Type": "application/json"},
                        data=dumps(tgjson),
                        raise_for_status=False) as r:
        _tgm_response = await r.json()
        # Check the received response
        if "ok" in _tgm_response.keys():
            if _tgm_response["ok"]:
                # This means method sent OK
                return loads(_tgm_response["result"])
            else:
                raise RuntimeError(f"Telegram Bot API {tgmethod} call error: "
                                   f"{dumps(_tgm_response)}")
        else:
            raise RuntimeError(f"Telegram Bot API wrong response: {dumps(_tgm_response)}")


class WorkItemIssue:
    """
    Main object that Telegram Bot works with - the work item, represents task to do
    """
    def __init__(self, jsfmt: str):
        """
        Instantiate the object from JSON string

        :param jsfmt: JSON representation of WorkItemIssue
        """
        # Load from JSON
        _wii = loads(jsfmt)
