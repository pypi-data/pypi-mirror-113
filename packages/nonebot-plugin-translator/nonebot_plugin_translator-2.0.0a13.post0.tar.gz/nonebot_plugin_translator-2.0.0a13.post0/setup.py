# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_translator']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4.post0,<4.0.0',
 'nonebot-adapter-cqhttp>=2.0.0-alpha.13,<3.0.0',
 'nonebot2>=2.0.0-alpha.13,<3.0.0',
 'ujson>=4.0.2,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-translator',
    'version': '2.0.0a13.post0',
    'description': 'Multi language tanslator worked with nonebot2',
    'long_description': '<!--\n * @Author       : Lancercmd\n * @Date         : 2020-12-15 10:21:55\n * @LastEditors  : Lancercmd\n * @LastEditTime : 2021-07-16 00:20:21\n * @Description  : None\n * @GitHub       : https://github.com/Lancercmd\n-->\n# nonebot plugin translator\n\n- 基于 [nonebot / nonebot2](https://github.com/nonebot/nonebot2)\n\n## 功能\n\n- 多语种翻译插件\n\n> 接口来自 [腾讯机器翻译 TMT](https://cloud.tencent.com/product/tmt) 目前使用 [签名方法 v1](https://cloud.tencent.com/document/api/213/15692#.E4.BD.BF.E7.94.A8.E7.AD.BE.E5.90.8D.E6.96.B9.E6.B3.95-v1-.E7.9A.84.E5.85.AC.E5.85.B1.E5.8F.82.E6.95.B0)\n\n## 准备工作\n\n- 在 [云API密钥](https://console.cloud.tencent.com/capi) 新建密钥，取得 `SecretId` 和 `SecretKey`\n\n## 开始使用\n\n建议使用 poetry\n\n- 通过 poetry 添加到 nonebot2 项目的 pyproject.toml\n\n```bash\npoetry add nonebot-plugin-translator\n```\n\n- 也可以通过 pip 从 [PyPI](https://pypi.org/project/nonebot-plugin-translator/) 安装\n\n```bash\npip install nonebot-plugin-translator\n```\n\n- 在 nonebot2 项目中设置 `nonebot.load_plugin()`\n> 当使用 [nb-cli](https://github.com/nonebot/nb-cli) 添加本插件时，该条会被自动添加\n\n```python3\nnonebot.load_plugin(\'nonebot_plugin_translator\')\n```\n\n- 参照下文在 nonebot2 项目的环境文件 `.env.*` 中添加配置项\n\n## 配置项\n\n- 腾讯云 API 请求的公共参数（必须）\n\n  `tencentcloud_common_region: str` [地域参数](https://cloud.tencent.com/document/api/551/15615#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8)，用来标识希望操作哪个地域的数据\n\n  `tencentcloud_common_secretid: str` 在 [云API密钥](https://console.cloud.tencent.com/capi) 上申请的标识身份的 `SecretId`，一个 `SecretId` 对应唯一的 `SecretKey`\n\n  `tencentcloud_common_secretkey: str` 你的 `SecretKey` 用来生成请求签名 Signature\n\n```json\ntencentcloud_common_region = "ap-shanghai"\ntencentcloud_common_secretid = ""\ntencentcloud_common_secretkey = ""\n```\n\n- 这样，就能够在 bot 所在群聊或私聊发送 `翻译` 或 `机翻` 使用了\n\n## 特别感谢\n\n- [Mrs4s / go-cqhttp](https://github.com/Mrs4s/go-cqhttp)\n- [nonebot / nonebot2](https://github.com/nonebot/nonebot2)\n\n## 优化建议\n\n请积极提交 Issues 或 Pull requests',
    'author': 'Lancercmd',
    'author_email': 'lancercmd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Lancercmd/nonebot_plugin_translator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
