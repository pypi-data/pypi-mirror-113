# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bilibili_dynamic']

package_data = \
{'': ['*'], 'bilibili_dynamic': ['element/*', 'typeface/*']}

install_requires = \
['Pillow>=8.0.1,<9.0.0',
 'aiohttp>=3.7.2,<4.0.0',
 'fonttools>=4.24.4,<5.0.0',
 'matplotlib>=3.4.0,<4.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'qrcode>=6.1,<7.0',
 'urllib3>=1.25.11,<2.0.0']

setup_kwargs = {
    'name': 'bilibili-dynamic',
    'version': '0.0.4',
    'description': '将哔哩哔哩返回的数据渲染为类似与B站APP官方的分享图片',
    'long_description': '# 几乎一致的动态样式渲染！\n<div align=center> \n    <img src="https://data.ngworks.cn/github/b3.jpg"/>\n</div>\n\n## 一、项目介绍\n\n### 1、介绍\n\n形象担当：[@禾咕咕](https://space.bilibili.com/254397112 )\n\n\n### 2、基本功能\n本项目实现了将哔哩哔哩返回的数据渲染为类似与B站APP官方的分享图片。\n如下图所示：\n\n\n<div align=center>\n    <img src="https://data.ngworks.cn/github/t.jpg" width = 30% />\n    <img src="https://data.ngworks.cn/github/t2.jpg" width = 35% />\n</div>\n<div align=center>\n    <img src="https://data.ngworks.cn/github/t3.jpg" width = 35% />\n    <img src="https://data.ngworks.cn/github/t6.jpg" width = 25% />\n</div>\n\n\n### 3、环境\n本项目基于**Python3.9.0**开发，**在其他版本的运行状态未知**。本项目使用2021年7月的哔哩哔哩API接口，**不保证**后续接口与数据结构不会发生变化。\n\n### 4、依赖\n|  Package  |  Version  |\n|-----------|   ------  |\n|Pillow     |      8.0.1|\n|aiohttp    |    3.7.2  |\n|qrcode     |    6.1    |\n|pydantic   |    1.7.3  |\n|pathlib    |    1.0.1  |\n|matplotlib |    3.4.0  |\n|urllib3    |    1.25.11|\n|fonttools  |    4.24.4 |\n\n### 5、项目结构\n本项目结构如下：\n```\n│  DynamicRender.py                 主要的程序文件\n│  readme.md                        自述文件\n│  LICENSE                          LICENSE\n│  __init__.py                      __init__.py\n│  _version.py                      版本信息\n├─ typeface                         字体文件夹\n│  │ Unifont.ttf                    Unifont字体\n│  │ CODE2000.ttf                   CODE2000字体\n│  │ NotoColorEmoji.ttf             Noto emoji字体\n│  │ NotoSansCJKsc-Regular.otf      思源黑体\n│  │ NONT LICENSE                   Noto字体 LICENSE\n├─ element                          图片组件文件夹\n```\n### 6、交流\n外联群QQ:781665797\n\n# 二、使用\n## 1、安装\n### (1)、pip安装(推荐）\n您可以使用pip快速的安装\n```\npip install bilibili-dynamic\n```\n### (2)、自行构建\nTODO\n### (3)、使用releases中的版本\n请您前往[releases](https://github.com/NGWORKS/DynamicRender/releases/)页面，自行下载后缀名为`.whl`的文件，并牢记文件名称。然后使用：\n```\npip install 下载下来的文件名称\n```\n\n## 2、使用\n* 传入 API返回数据中的`data`下的`card` 或与结构之一样的数据。\n```python\nfrom BiliBili_dynamic import DynamicRender\nimport asyncio\n# data 是上述数据，tmp_path是缓存路径，默认为工作路径下的 tmp目录，您也可以自行指定。\nRender = DynamicRender.DynamicPictureRendering(data,tmp_path =r"tmp")\nloop = asyncio.get_event_loop()\nloop.run_until_complete(Render.ReneringManage())\nRender.ReprenderIMG.show()\n```\n\n# 三、如何工作\n我们将动态的渲染分为五大部分，每部分独立渲染：\n\n**`头部信息`、`文字部分`、`功能块`（图片动态的图片、视频的视频等）、`附加卡片`（相关游戏、直播预约等）、`转发信息`（转发内容）**\n每部分根据动态的内容渲染，如果**没有该部分则不渲染**。\n每个模块渲染是**异步**的，其关系您可以根据下图理解：\n<div align=center> <img src="https://data.ngworks.cn/github/1.png" width = 150%/> </div>\n\n此图仅供参考，在使用过程中有诸多因素会影响渲染的流程。\n\n> **附加卡片**通常不会下载图片，除了卡片展示游戏相关时。\n\n> **转发信息**就是将上述流程嵌套了一次，只是不渲染头部信息，其余基本一致，故不赘述。\n\n## 1、头部信息\n这个模块的实现是在`DynamicRender.py`中的`DynamicPictureRendering`类中的`headRendering`方法。\n如项目介绍图片当中的一致，本模块实现了将头像、挂件缓存与渲染，同时本模块可以对该动态发布的时间、账号是否大会员、认证账号进行详细的渲染。\n\n## 2、文字部分\n该部分是本项目的核心模块，主要实现了将动态文字进行富文本化。实现是在`DynamicRender.py`中的`DynamicPictureRendering`类中的`NGSSTrcker`方法。\n为了方便您更好对这个理解这个模块的运作方式，下图介绍了该模块的工作细节：\n<div align=center> <img src="https://data.ngworks.cn/github/2.png" width = 150%/> </div>\n\n* `NGSS`识别了特殊文本的样式，和在字符串中的位置，是后续文本处理的指导性数据。\n* `RenderList`包含了以特殊文本为分隔符的所有文本信息。\n* `rl` 包含了以`字符`为单位的文本渲染信息。\n* `pl` 包含了以`bilibili表情包`为单位的渲染信息。\n* `tl` 包含了以`特殊功能图片`的渲染信息，如动态抽奖前的小礼物，投票的柱状图，网页链接的链接图标。\n\n## 3、功能块\n这个模块的实现是在`DynamicRender.py`中的`DynamicPictureRendering`类中的`FunctionBlock`方法。\n它实现了渲染九宫格与专栏封面，视频封面，与直播封面。\n\n## 4、附加卡片\n这个模块的实现是在`DynamicRender.py`中的`DynamicPictureRendering`类中的`AddCard`方法。\n它实现了渲染投票，视频预约，直播预约，游戏信息等。\n\n## 5、转发信息\n这个模块的实现是在`DynamicRender.py`中的`DynamicPictureRendering`类中的`Reprender`方法。\n渲染源动态内容，原理与总动态基本一致，差别仅在字体颜色和对于头部信息渲染的省略。\n这个模块调用了上述除过`头部信息`以外的三个模块。\n\n# 四、贡献 - 特别感谢 - license\n## 1、贡献\n如果您发现了更好的使用方法，不妨分享出来！你可以使用pr功能提交请求，我会审阅。或者在使用中出现了什么问题，都可以提交issue，或者加入我们的`外联群（QQ:781665797）`交流。\n\n## 2、特别感谢\n- [`bilibili-API-collect`](https://github.com/SocialSisterYi/bilibili-API-collect)：非常详细的 B站 api 文档\n- [`HarukaBot`](https://github.com/SK-415/HarukaBot)：非常nb的机器人\n- [`Google Noto Fonts`](https://www.google.cn/get/noto/)：适用于所有语言的漂亮且免费的字体！\n- [`unifont`](http://www.unifont.org/new/)：伟大的字体项目\n## 3、license\nMIT.',
    'author': 'NGWORKS',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NGWORKS/DynamicRender/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
