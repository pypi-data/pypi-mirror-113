import json
import re
from functools import partial
from shangjian_api.airworks import BaseApi, ApiError


class AirWorksApi:

    def __init__(self, base_url, access_key, access_secret, default_app_id=None, **kwargs):
        self.base_api = BaseApi()
        BaseApi.base_url = base_url
        self.base_api.access_key = access_key
        self.base_api.access_secret = access_secret
        self.default_app_id = default_app_id
        self.default_api_method = kwargs.get("default_api_method", "GET")
        self.default_page_num = kwargs.get("default_page_num", 1)
        self.default_page_size = kwargs.get("default_page_size", 100)
        self.base_api.app_url = kwargs.get("app_url")
        self.base_api.app_method = kwargs.get("app_method", "GET")

    def _call(self, api_url, **kwargs):
        app_id = kwargs.get("app_id", self.default_app_id)
        if not app_id:
            raise ApiError(
                error_code=40009,
                error_msg="app_Id缺失，请先设置default_app_id或传入app_id"
            )
        api_url = self._url_transfer(api_url)

        kwargs.update({
            "app_url": f"api_gateway/api/{app_id}/{api_url}",
            "api_method": kwargs.get("api_method") or self.default_api_method,
            "page_num": kwargs.get("page_num") or self.default_page_num,
            "page_size": kwargs.get("page_size") or self.default_page_size,
        })
        return self.base_api.api_response(**kwargs)

    @classmethod
    def _url_transfer(cls, url):
        url_list = list()
        for index, item in enumerate(url.split("__")):
            if index == 0 and re.match(r"_[0-9]", item):
                item = item[1:]
            url_list.append(item.replace("_A", "/"))
        url = "_".join(url_list)
        return url

    def call(self, **kwargs):
        return self.base_api.api_response(**kwargs)

    def __getattr__(self, key):
        return partial(self._call, api_url=key)


if __name__ == "__main__":
    awp = AirWorksApi(
        base_url="aw-airworks-frontend:30000",
        access_key="kB85aqPMFZs_14",
        access_secret="lh66YHfiE7qL6TcOOvbLTg",
        default_app_id=1
    )

    res = awp.baymax(
        api_method="get",
        country="中国",
        id=None,
        page_size=100,
        page_num=1)

    print(json.dumps(res, indent=2, ensure_ascii=False))
