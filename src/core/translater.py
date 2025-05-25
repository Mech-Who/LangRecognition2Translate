import json
from typing import List

# Aliyun SDK
from alibabacloud_alimt20181012 import models as alimt_20181012_models
from alibabacloud_alimt20181012.client import Client as alimt20181012Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class AliTranslator(object):
    def __init__(
        self, access_key_id: str, access_key_secret: str, endpoint: str, qps: int
    ):
        self.config = open_api_models.Config(
            access_key_id=access_key_id, access_key_secret=access_key_secret
        )
        self.config.endpoint = endpoint
        self.qps = qps
        self.client = alimt20181012Client(self.config)

    def translate(
        self, query: str, from_lang: str = "auto", to_lang: str = "zh"
    ) -> str:
        translate_general_request = alimt_20181012_models.TranslateGeneralRequest(
            format_type="text",
            source_language=from_lang,
            target_language=to_lang,
            source_text=query,
            scene="general",
            context="",
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = self.client.translate_general_with_options(
                translate_general_request, runtime
            )
            # TODO: 处理返回值
            return response
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    def translate_professional(
        self,
        query: str,
        from_lang: str = "auto",
        to_lang: str = "zh",
        scene: str = "social",
    ):
        translate_request = alimt_20181012_models.TranslateRequest(
            format_type="text",
            target_language=to_lang,
            source_language=from_lang,
            source_text=query,
            scene=scene,
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = self.client.translate_with_options(translate_request, runtime)
            # TODO: 处理返回值
            return response
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

    async def translate_batch(
        self,
        querys: List[str],
        from_lang: str = "auto",
        to_lang: str = "en",
        scene: str = "social",
        api_type: str = "translate_standard",
    ):
        querys = {str(i): q for i, q in enumerate(querys)}
        querys = json.dumps(querys)
        get_batch_translate_request = alimt_20181012_models.GetBatchTranslateRequest(
            format_type="text",
            target_language=to_lang,
            source_language=from_lang,
            scene=scene,
            api_type=api_type,
            source_text=querys,
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            response = await self.client.get_batch_translate_with_options_async(
                get_batch_translate_request, runtime
            )
            # TODO: 处理返回值
            return response
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)
