import requests
from threading import Thread
import time
import os
import re
import shutil
import sys
import random
import streamlink
import traceback
names = []
namenum=0
#url = 'https://webcast3-c.amemv.com/webcast/feed/?content_type=1&channel_id=37&version_code=8.8.0&pass-region=0&pass-route=0&js_sdk_version=1.32.1.0&webcast_sdk_version=1290&app_name=aweme&vid=D15D9459-8743-4CF5-968F-6A11A8EC5007&app_version=8.8.0&language=zh-Hans-CN&device_id=70047599612&channel=App%20Store&mcc_mnc=46001&aid=1128&effect_sdk_version=5.6.0&screen_width=375&openudid=e567d40a4e127e37e6c3212e5b44fd7cf0ebc60e&webcast_language=zh&os_api=18&ac=WIFI&os_version=13.3&webcast_locale=zh-Hans_CN&device_platform=iphone&build_number=88016&iid=93859058229&device_type=iPhone%208&idfa=1924B11C-5A94-45C2-874C-C5F82E0CB028&req_from=follow_live_skylight&action=refresh'
url = 'https://aweme.snssdk.com/aweme/v1/life/feed/?version_code=7.9.0&pass-region=1&pass-route=1&js_sdk_version=1.17.2.0&app_name=aweme&vid=399BCB11-BD3E-448A-8516-38E0C57BCC77&app_version=7.9.0&device_id=52100380665&channel=App%20Store&mcc_mnc=46001&aid=1128&screen_width=750&openudid=4d099f1840e190e9fe10224fcb657786a5c5ad70&os_api=18&ac=WIFI&os_version=12.4&device_platform=iphone&build_number=79025&device_type=iPhone10,4&iid=85477742411&idfa=1C721462-0A8F-4200-A60B-8A83373F5493&count=20&tab_type=2&cursor=0'
url2 = 'https://webcast-c.amemv.com/webcast/feed/?content_type=1&channel_id=37&version_code=9.6.0&pass-region=0&js_sdk_version=1.47.2.2&pass-route=0&webcast_sdk_version=1370&app_name=aweme&vid=D15D9459-8743-4CF5-968F-6A11A8EC5007&app_version=9.6.0&language=zh-Hans-CN&device_id=70047599612&channel=App%20Store&mcc_mnc=46001&aid=1128&effect_sdk_version=6.0.0&screen_width=375&openudid=e567d40a4e127e37e6c3212e5b44fd7cf0ebc60e&cdid=D214CFFA-5E13-4D63-9B9B-F04EB776BB5B&os_api=18&webcast_language=zh&ac=WIFI&os_version=13.3.1&webcast_locale=zh-Hans_CN&device_platform=iphone&build_number=96025&iid=101180374432&device_type=iPhone%208&idfa=1924B11C-5A94-45C2-874C-C5F82E0CB028&req_from=follow_live_skylight&action=refresh'
#headers = {"x-Tt-Token":"009eb6296810343ae341cb7841294dabcad389438632df3ac5d994b75eca174b3ef10c25b328e36dc06be51d9cb0b604fc1a","sdk-version":"1","User-Agent":"Aweme 7.9.0 rv","x-tt-trace-id":"00-29feca87f033b1aa8144163a3366e0e4-29feca87f033b1aa-01","Accept-Encoding":"gzip, deflate","Cookie":"sid_guard=9eb6296810343ae341cb7841294dabca%7C1567870522%7C5184000%7CWed%2C+06-Nov-2019+15%3A35%3A22+GMT; uid_tt=b58f6ed0f43b1e3f100f44d55b36d672; sid_tt=9eb6296810343ae341cb7841294dabca; sessionid=9eb6296810343ae341cb7841294dabca; odin_tt=42f64d634c20908096376178a33edbc139450b81995e83eea22255b6b1f154da54bd9b1153717dfda3cb734f25dc4b9f; install_id=85477742411; ttreq=1$10179bfdd42fe841ad94af1bed38bbc1ef93ed34","X-Khronos":"1568269877","X-Gorgon":"830099902001e24feb1a2ca41a8de732caf9abbc62fa0ab4d63a"}
headers = {"Accept-Encoding": "gzip, deflate","Connection": "keep-alive","Cookie": "odin_tt=4076eee9536434b54f9743cf17c374293d206e4f542515ea3b4c4b2fb5d4869b433c0aebf8d47ed5226797e8059fa617; sid_tt=828d10cc26e4e566a408a1ac68696b9e; sessionid=828d10cc26e4e566a408a1ac68696b9e; uid_tt=0bb045d1f70e7f7b44f2871d73154102; sid_guard=828d10cc26e4e566a408a1ac68696b9e%7C1579540637%7C4897275%7CTue%2C+17-Mar-2020+09%3A38%3A32+GMT; install_id=95976244185; ttreq=1$b3f249f20663a9c4f26f5a8c96a55acac0bb030a","Host": "api3-normal-c-lf.amemv.com","User-Agent": "Aweme 9.1.0 rv:91027 (iPhone; iOS 13.3; zh_CN) Cronet","X-Gorgon": "8401c03e300016ea8bf7cbc49b840131e272125c8817bd838f8c","X-Khronos": "1579774876","X-SS-DP": "1128","sdk-version": "1","x-Tt-Token": "00828d10cc26e4e566a408a1ac68696b9e15666a4cfdc6126055e3ab45fc4dfc9c71205a0ff01929db45125d0909af24b1c","x-tt-trace-id": "00-d1eb9d450a104f298bfcc286707d0468-d1eb9d450a104f29-01",}
headerslist = (
{"Accept-Encoding": "gzip, deflate","Connection": "keep-alive","Cookie": "odin_tt=ab23cf4b30fe185a45c7ef9302c428419ac89539c3bdb74b57833833aa786745fcbb2c543d0b418109d67c50e592ab48; sid_tt=828d10cc26e4e566a408a1ac68696b9e; sessionid=828d10cc26e4e566a408a1ac68696b9e; uid_tt=0bb045d1f70e7f7b44f2871d73154102; sid_guard=828d10cc26e4e566a408a1ac68696b9e%7C1579878876%7C4559036%7CTue%2C+17-Mar-2020+09%3A38%3A32+GMT; install_id=101180374432; ttreq=1$cc2fcf96319367ec86da0d05f706faac644038fc; amazing_h_s=1","Host": "webcast-c.amemv.com","User-Agent": "Aweme 9.6.0 rv:96025 (iPhone; iOS 13.3.1; zh_CN) Cronet","X-Gorgon": "8402e0502000b1f99cec966aa34b7f840903ff5ad492d499f03b","X-Khronos": "1580529160","X-SS-DP": "1128","sdk-version": "1","x-Tt-Token": "00828d10cc26e4e566a408a1ac68696b9e6ecf5f616a907178a7d662adabf35b401a08b0504538171ac645b979a610f8815c","x-tt-trace-id": "00-fee115bd0a104f298bfccfc113460468-fee115bd0a104f29-01",},
{"Accept-Encoding": "gzip, deflate","Connection": "keep-alive","Cookie": "odin_tt=ab23cf4b30fe185a45c7ef9302c428419ac89539c3bdb74b57833833aa786745fcbb2c543d0b418109d67c50e592ab48; sid_tt=828d10cc26e4e566a408a1ac68696b9e; sessionid=828d10cc26e4e566a408a1ac68696b9e; uid_tt=0bb045d1f70e7f7b44f2871d73154102; sid_guard=828d10cc26e4e566a408a1ac68696b9e%7C1579878876%7C4559036%7CTue%2C+17-Mar-2020+09%3A38%3A32+GMT; install_id=101180374432; ttreq=1$cc2fcf96319367ec86da0d05f706faac644038fc; amazing_h_s=1","Host": "webcast3-c.amemv.com","User-Agent": "Aweme 9.6.0 rv:96025 (iPhone; iOS 13.3.1; zh_CN) Cronet","X-Gorgon": "8402a06d2000a201378217b78192932ac8dff4e8618e103ea1ba","X-Khronos": "1580529092","X-SS-DP": "1128","sdk-version": "1","x-Tt-Token": "00828d10cc26e4e566a408a1ac68696b9e6ecf5f616a907178a7d662adabf35b401a08b0504538171ac645b979a610f8815c","x-tt-trace-id": "00-fee12e4d0a104f298bfcb59e77b20468-fee12e4d0a104f29-01",},
{"Accept-Encoding": "gzip, deflate","Connection": "keep-alive","Cookie": "odin_tt=ab23cf4b30fe185a45c7ef9302c428419ac89539c3bdb74b57833833aa786745fcbb2c543d0b418109d67c50e592ab48; sid_tt=828d10cc26e4e566a408a1ac68696b9e; sessionid=828d10cc26e4e566a408a1ac68696b9e; uid_tt=0bb045d1f70e7f7b44f2871d73154102; sid_guard=828d10cc26e4e566a408a1ac68696b9e%7C1579878876%7C4559036%7CTue%2C+17-Mar-2020+09%3A38%3A32+GMT; install_id=101180374432; ttreq=1$cc2fcf96319367ec86da0d05f706faac644038fc; amazing_h_s=1","Host": "webcast3-c.amemv.com","User-Agent": "Aweme 9.6.0 rv:96025 (iPhone; iOS 13.3.1; zh_CN) Cronet","X-Gorgon": "84024036200072ed3a3c6e8d75aa052ddd329e8d99bdd27a51cb","X-Khronos": "1580529168","X-SS-DP": "1128","sdk-version": "1","x-Tt-Token": "00828d10cc26e4e566a408a1ac68696b9e6ecf5f616a907178a7d662adabf35b401a08b0504538171ac645b979a610f8815c","x-tt-trace-id": "00-fee134df0a104f298bfc5a1575140468-fee134df0a104f29-01",},
{"Accept-Encoding": "gzip, deflate","Connection": "keep-alive","Cookie": "odin_tt=ab23cf4b30fe185a45c7ef9302c428419ac89539c3bdb74b57833833aa786745fcbb2c543d0b418109d67c50e592ab48; sid_tt=828d10cc26e4e566a408a1ac68696b9e; sessionid=828d10cc26e4e566a408a1ac68696b9e; uid_tt=0bb045d1f70e7f7b44f2871d73154102; sid_guard=828d10cc26e4e566a408a1ac68696b9e%7C1579878876%7C4559036%7CTue%2C+17-Mar-2020+09%3A38%3A32+GMT; install_id=101180374432; ttreq=1$cc2fcf96319367ec86da0d05f706faac644038fc; amazing_h_s=1","Host": "webcast-c.amemv.com","User-Agent": "Aweme 9.6.0 rv:96025 (iPhone; iOS 13.3.1; zh_CN) Cronet","X-Gorgon": "840280252000441d73e2e57c38f05eca29f933680382911c4397","X-Khronos": "1580527387","X-SS-DP": "1128","sdk-version": "1","x-Tt-Token": "00828d10cc26e4e566a408a1ac68696b9e6ecf5f616a907178a7d662adabf35b401a08b0504538171ac645b979a610f8815c","x-tt-trace-id": "00-fec604de0a104f298bfc4819ea270468-fec604de0a104f29-01",},
{"Accept-Encoding": "gzip, deflate","Connection": "keep-alive","Cookie": "odin_tt=ab23cf4b30fe185a45c7ef9302c428419ac89539c3bdb74b57833833aa786745fcbb2c543d0b418109d67c50e592ab48; sid_tt=828d10cc26e4e566a408a1ac68696b9e; sessionid=828d10cc26e4e566a408a1ac68696b9e; uid_tt=0bb045d1f70e7f7b44f2871d73154102; sid_guard=828d10cc26e4e566a408a1ac68696b9e%7C1579878876%7C4559036%7CTue%2C+17-Mar-2020+09%3A38%3A32+GMT; install_id=101180374432; ttreq=1$cc2fcf96319367ec86da0d05f706faac644038fc; amazing_h_s=1","Host": "webcast3-c.amemv.com","User-Agent": "Aweme 9.6.0 rv:96025 (iPhone; iOS 13.3.1; zh_CN) Cronet","X-Gorgon": "8402206e200000f1d8ad8e49720a2b9fa8eda7398edf4281bd37","X-Khronos": "1580561002","X-SS-DP": "1128","sdk-version": "1","x-Tt-Token": "00828d10cc26e4e566a408a1ac68696b9e6ecf5f616a907178a7d662adabf35b401a08b0504538171ac645b979a610f8815c","x-tt-trace-id": "00-00c6f1ff0a104f298bfc750688bb0468-00c6f1ff0a104f29-01",},
{"Accept-Encoding": "gzip, deflate","Connection": "keep-alive","Cookie": "odin_tt=ab23cf4b30fe185a45c7ef9302c428419ac89539c3bdb74b57833833aa786745fcbb2c543d0b418109d67c50e592ab48; sid_tt=828d10cc26e4e566a408a1ac68696b9e; sessionid=828d10cc26e4e566a408a1ac68696b9e; uid_tt=0bb045d1f70e7f7b44f2871d73154102; sid_guard=828d10cc26e4e566a408a1ac68696b9e%7C1579878876%7C4559036%7CTue%2C+17-Mar-2020+09%3A38%3A32+GMT; install_id=101180374432; ttreq=1$cc2fcf96319367ec86da0d05f706faac644038fc; amazing_h_s=1","Host": "webcast3-c.amemv.com","User-Agent": "Aweme 9.6.0 rv:96025 (iPhone; iOS 13.3.1; zh_CN) Cronet","X-Gorgon": "8402806a20004f7cfa12b905a602f56061bc0d863ce4a60c2151","X-Khronos": "1580561012","X-SS-DP": "1128","sdk-version": "1","x-Tt-Token": "00828d10cc26e4e566a408a1ac68696b9e6ecf5f616a907178a7d662adabf35b401a08b0504538171ac645b979a610f8815c","x-tt-trace-id": "00-00c719bc0a104f298bfcf68f5bb80468-00c719bc0a104f29-01",},
{"Accept-Encoding": "gzip, deflate","Connection": "keep-alive","Cookie": "odin_tt=ab23cf4b30fe185a45c7ef9302c428419ac89539c3bdb74b57833833aa786745fcbb2c543d0b418109d67c50e592ab48; sid_tt=828d10cc26e4e566a408a1ac68696b9e; sessionid=828d10cc26e4e566a408a1ac68696b9e; uid_tt=0bb045d1f70e7f7b44f2871d73154102; sid_guard=828d10cc26e4e566a408a1ac68696b9e%7C1579878876%7C4559036%7CTue%2C+17-Mar-2020+09%3A38%3A32+GMT; install_id=101180374432; ttreq=1$cc2fcf96319367ec86da0d05f706faac644038fc; amazing_h_s=1","Host": "webcast3-c.amemv.com","User-Agent": "Aweme 9.6.0 rv:96025 (iPhone; iOS 13.3.1; zh_CN) Cronet","X-Gorgon": "8402c0f52000672cf920e003ebe7556a03b01ea94a4a485412df","X-Khronos": "1580561022","X-SS-DP": "1128","sdk-version": "1","x-Tt-Token": "00828d10cc26e4e566a408a1ac68696b9e6ecf5f616a907178a7d662adabf35b401a08b0504538171ac645b979a610f8815c","x-tt-trace-id": "00-00c73f000a104f298bfc05f3c4a10468-00c73f000a104f29-01",},
{"Accept-Encoding": "gzip, deflate","Connection": "keep-alive","Cookie": "odin_tt=ab23cf4b30fe185a45c7ef9302c428419ac89539c3bdb74b57833833aa786745fcbb2c543d0b418109d67c50e592ab48; sid_tt=828d10cc26e4e566a408a1ac68696b9e; sessionid=828d10cc26e4e566a408a1ac68696b9e; uid_tt=0bb045d1f70e7f7b44f2871d73154102; sid_guard=828d10cc26e4e566a408a1ac68696b9e%7C1579878876%7C4559036%7CTue%2C+17-Mar-2020+09%3A38%3A32+GMT; install_id=101180374432; ttreq=1$cc2fcf96319367ec86da0d05f706faac644038fc; amazing_h_s=1","Host": "webcast3-c.amemv.com","User-Agent": "Aweme 9.6.0 rv:96025 (iPhone; iOS 13.3.1; zh_CN) Cronet","X-Gorgon": "840260b620003920cc010b07bee7c766bbf8224d02fac5392112","X-Khronos": "1580561027","X-SS-DP": "1128","sdk-version": "1","x-Tt-Token": "00828d10cc26e4e566a408a1ac68696b9e6ecf5f616a907178a7d662adabf35b401a08b0504538171ac645b979a610f8815c","x-tt-trace-id": "00-00c7540b0a104f298bfc65b14ad30468-00c7540b0a104f29-01",},
{"Accept-Encoding": "gzip, deflate","Connection": "keep-alive","Cookie": "odin_tt=ab23cf4b30fe185a45c7ef9302c428419ac89539c3bdb74b57833833aa786745fcbb2c543d0b418109d67c50e592ab48; sid_tt=828d10cc26e4e566a408a1ac68696b9e; sessionid=828d10cc26e4e566a408a1ac68696b9e; uid_tt=0bb045d1f70e7f7b44f2871d73154102; sid_guard=828d10cc26e4e566a408a1ac68696b9e%7C1579878876%7C4559036%7CTue%2C+17-Mar-2020+09%3A38%3A32+GMT; install_id=101180374432; ttreq=1$cc2fcf96319367ec86da0d05f706faac644038fc; amazing_h_s=1","Host": "webcast3-c.amemv.com","User-Agent": "Aweme 9.6.0 rv:96025 (iPhone; iOS 13.3.1; zh_CN) Cronet","X-Gorgon": "8402004a200020ecea087bfb4ebe9ab4ee5f0184e050c0632820","X-Khronos": "1580561031","X-SS-DP": "1128","sdk-version": "1","x-Tt-Token": "00828d10cc26e4e566a408a1ac68696b9e6ecf5f616a907178a7d662adabf35b401a08b0504538171ac645b979a610f8815c","x-tt-trace-id": "00-00c7648c0a104f298bfcde35bdf30468-00c7648c0a104f29-01",},
{"Accept-Encoding": "gzip, deflate","Connection": "keep-alive","Cookie": "odin_tt=ab23cf4b30fe185a45c7ef9302c428419ac89539c3bdb74b57833833aa786745fcbb2c543d0b418109d67c50e592ab48; sid_tt=828d10cc26e4e566a408a1ac68696b9e; sessionid=828d10cc26e4e566a408a1ac68696b9e; uid_tt=0bb045d1f70e7f7b44f2871d73154102; sid_guard=828d10cc26e4e566a408a1ac68696b9e%7C1579878876%7C4559036%7CTue%2C+17-Mar-2020+09%3A38%3A32+GMT; install_id=101180374432; ttreq=1$cc2fcf96319367ec86da0d05f706faac644038fc; amazing_h_s=1","Host": "webcast3-c.amemv.com","User-Agent": "Aweme 9.6.0 rv:96025 (iPhone; iOS 13.3.1; zh_CN) Cronet","X-Gorgon": "8402606320003025339b4b09866bdf6e2933936a78b2816548b0","X-Khronos": "1580561000","X-SS-DP": "1128","sdk-version": "1","x-Tt-Token": "00828d10cc26e4e566a408a1ac68696b9e6ecf5f616a907178a7d662adabf35b401a08b0504538171ac645b979a610f8815c","x-tt-trace-id": "00-00c7897f0a104f298bfcf834b8470468-00c7897f0a104f29-01",},
{"Accept-Encoding": "gzip, deflate","Connection": "keep-alive","Cookie": "odin_tt=ab23cf4b30fe185a45c7ef9302c428419ac89539c3bdb74b57833833aa786745fcbb2c543d0b418109d67c50e592ab48; sid_tt=828d10cc26e4e566a408a1ac68696b9e; sessionid=828d10cc26e4e566a408a1ac68696b9e; uid_tt=0bb045d1f70e7f7b44f2871d73154102; sid_guard=828d10cc26e4e566a408a1ac68696b9e%7C1579878876%7C4559036%7CTue%2C+17-Mar-2020+09%3A38%3A32+GMT; install_id=101180374432; ttreq=1$cc2fcf96319367ec86da0d05f706faac644038fc; amazing_h_s=1","Host": "webcast3-c.amemv.com","User-Agent": "Aweme 9.6.0 rv:96025 (iPhone; iOS 13.3.1; zh_CN) Cronet","X-Gorgon": "840260992000f9510dcfc9bebe1d3a87cfdf28983f9333b1528e","X-Khronos": "1580561047","X-SS-DP": "1128","sdk-version": "1","x-Tt-Token": "00828d10cc26e4e566a408a1ac68696b9e6ecf5f616a907178a7d662adabf35b401a08b0504538171ac645b979a610f8815c","x-tt-trace-id": "00-00c7a38f0a104f298bfc3807b8b00468-00c7a38f0a104f29-01",},
{"Accept-Encoding": "gzip, deflate","Connection": "keep-alive","Cookie": "odin_tt=ab23cf4b30fe185a45c7ef9302c428419ac89539c3bdb74b57833833aa786745fcbb2c543d0b418109d67c50e592ab48; sid_tt=828d10cc26e4e566a408a1ac68696b9e; sessionid=828d10cc26e4e566a408a1ac68696b9e; uid_tt=0bb045d1f70e7f7b44f2871d73154102; sid_guard=828d10cc26e4e566a408a1ac68696b9e%7C1579878876%7C4559036%7CTue%2C+17-Mar-2020+09%3A38%3A32+GMT; install_id=101180374432; ttreq=1$cc2fcf96319367ec86da0d05f706faac644038fc; amazing_h_s=1","Host": "webcast3-c.amemv.com","User-Agent": "Aweme 9.6.0 rv:96025 (iPhone; iOS 13.3.1; zh_CN) Cronet","X-Gorgon": "840260a42000f05fb8ded376ce23a31f428533704e37da26d280","X-Khronos": "1580561052","X-SS-DP": "1128","sdk-version": "1","x-Tt-Token": "00828d10cc26e4e566a408a1ac68696b9e6ecf5f616a907178a7d662adabf35b401a08b0504538171ac645b979a610f8815c","x-tt-trace-id": "00-00c7b43c0a104f298bfc69234ad70468-00c7b43c0a104f29-01",},
{"Accept-Encoding": "gzip, deflate","Connection": "keep-alive","Cookie": "odin_tt=ab23cf4b30fe185a45c7ef9302c428419ac89539c3bdb74b57833833aa786745fcbb2c543d0b418109d67c50e592ab48; sid_tt=828d10cc26e4e566a408a1ac68696b9e; sessionid=828d10cc26e4e566a408a1ac68696b9e; uid_tt=0bb045d1f70e7f7b44f2871d73154102; sid_guard=828d10cc26e4e566a408a1ac68696b9e%7C1579878876%7C4559036%7CTue%2C+17-Mar-2020+09%3A38%3A32+GMT; install_id=101180374432; ttreq=1$cc2fcf96319367ec86da0d05f706faac644038fc; amazing_h_s=1","Host": "webcast3-c.amemv.com","User-Agent": "Aweme 9.6.0 rv:96025 (iPhone; iOS 13.3.1; zh_CN) Cronet","X-Gorgon": "8402c03d2000bf2694b7484901c4904db93ad3b76b5b9a872e75","X-Khronos": "1580561031","X-SS-DP": "1128","sdk-version": "1","x-Tt-Token": "00828d10cc26e4e566a408a1ac68696b9e6ecf5f616a907178a7d662adabf35b401a08b0504538171ac645b979a610f8815c","x-tt-trace-id": "00-00c7c72b0a104f298bfcda191a2e0468-00c7c72b0a104f29-01",},
{"Accept-Encoding": "gzip, deflate","Connection": "keep-alive","Cookie": "odin_tt=ab23cf4b30fe185a45c7ef9302c428419ac89539c3bdb74b57833833aa786745fcbb2c543d0b418109d67c50e592ab48; sid_tt=828d10cc26e4e566a408a1ac68696b9e; sessionid=828d10cc26e4e566a408a1ac68696b9e; uid_tt=0bb045d1f70e7f7b44f2871d73154102; sid_guard=828d10cc26e4e566a408a1ac68696b9e%7C1579878876%7C4559036%7CTue%2C+17-Mar-2020+09%3A38%3A32+GMT; install_id=101180374432; ttreq=1$cc2fcf96319367ec86da0d05f706faac644038fc; amazing_h_s=1","Host": "webcast3-c.amemv.com","User-Agent": "Aweme 9.6.0 rv:96025 (iPhone; iOS 13.3.1; zh_CN) Cronet","X-Gorgon": "8402606820007a8e657b5927ef50f2a19fbc4cd2a8742009f547","X-Khronos": "1580561060","X-SS-DP": "1128","sdk-version": "1","x-Tt-Token": "00828d10cc26e4e566a408a1ac68696b9e6ecf5f616a907178a7d662adabf35b401a08b0504538171ac645b979a610f8815c","x-tt-trace-id": "00-00c7d53b0a104f298bfcb377a55e0468-00c7d53b0a104f29-01",}
)

if not os.path.exists('/root/b/d/dy'):
    os.makedirs('/root/b/d/dy')
else:
    files = os.listdir('/root/b/d/dy')
    for f in files:
        fulld = os.path.join('/root/b/d/dy',f)
        if os.path.isdir(fulld):
            for file in os.listdir(fulld):
                fullfile = os.path.join(fulld,file)
                shutil.move(fullfile,'/root/b/d/dy')
            os.rmdir(fulld)
class room():
    def __init__(self,nickname,url):
        self.nickname = nickname
        self.url = url
def download(room):
    filename = '{}-{}-_.flv'.format(room.nickname,time.strftime('%y%m%d_%H%M%S'))
    path = '/root/b/d/dy/{}/'.format(room.nickname)
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        files = os.listdir(path)
        if files:
            os.system("cd '{}';mv * /root/b/d/dy".format(path))
    filepath = path+filename
    f = open(filepath,'wb')
    try:
        r = requests.get(room.url,stream = True,timeout = 10)
        filesize = 0
        for chunk in r.iter_content(chunk_size = 1024*8):
            if chunk:
                filesize+=f.write(chunk)
                if filesize%(1024*512)==0:
                    sys.stdout.write('\r\033[K直播数{}{}  {}M'.format(namenum,filename,filesize/(1024*1024)))
                if filesize/(1024*1024) >= 1024:
                    f.close()
                    shutil.move(filepath,'/root/b/d/dy')
                    filename = '{}-{}-_.flv'.format(room.nickname,time.strftime('%y%m%d_%H%M%S'))
                    filepath = path+filename
                    f = open(filepath,'wb')
    except Exception as e:
        print('\r\033[K',e)
    finally:
        names.remove(room.nickname)
        if 'r' in locals():
            r.close()
        f.close()
        if (os.path.isfile(filepath) and os.path.getsize(filepath) < 1024*100):
            os.remove(filepath);
        else:
            if os.path.isfile(filepath):
                shutil.move(filepath,'/root/b/d/dy')
        try:
            os.rmdir(path)
            print('\r\033[K',room.nickname,'stops recording flv，删除文件夹')
        except:
            print('\r\033[K',room.nickname,'stops recording flv')

def download_hls(room):
    filename = '{}-{}-_.ts'.format(room.nickname,time.strftime('%y%m%d_%H%M%S'))
    path = '/root/b/d/dy/{}/'.format(room.nickname)
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        files = os.listdir(path)
        if files:
            os.system("cd '{}';mv * /root/b/d/dy".format(path))
    filepath = path+filename
    try:
        streams=streamlink.streams(room.url)
        stream = streams['best']
        fd = stream.open()
        fs = 0
        readbuffer = 1024*8
        desize = 1024*1024/8
        f = open(filepath,'wb')
        while 1:
            data = fd.read(readbuffer)
            if data:
                f.write(data)
            else:
                break
            fs+=1
            if fs % 100 == 0:
                sys.stdout.write(f'\r\033[K直播数{namenum}' + room.nickname + ' '+str(round(fs*8/1024,2)) + "m")
            if fs >=desize:
                f.close()
                fs = 0
                print('\r\033[K',filename,'\033[K大小达到限制，分割文件')
                shutil.move(filepath,'/root/b/d/dy')
                filename = '{}-{}-_.ts'.format(room.nickname,time.strftime('%y%m%d_%H%M%S'))
                filepath = path+filename
                f = open(filepath,'wb')
    except Exception as e:
        print('\r\033[K',e)
    finally:
        names.remove(room.nickname)
        if 'fd' in locals():
            fd.close()
        if 'f' in locals():
            f.close()
        if (os.path.isfile(filepath) and os.path.getsize(filepath) < 1024*100):
            os.remove(filepath);
        else:
            if os.path.isfile(filepath):
                shutil.move(filepath,'/root/b/d/dy')
        try:
            os.rmdir(path)
            print('\r\033[K',room.nickname,'stops recording flv，删除文件夹')
        except:
            print('\r\033[K',room.nickname,'stops recording flv')

temp = list(headerslist)
while True:
    try:
        if not temp:
            temp = list(headerslist)
        while 1:
            headers2 = random.choice(temp)
            r = requests.get(url2,headers= headers2,timeout = 10)
            if not r.text:
                r.close()
                temp.remove(headers2)
                if not temp:
                    break
            else:
                break  
        try:
            res = r.json()
            data = res['data']
            extra = res['extra']
            hasmore = extra['has_more']
        except:
            sys.stdout.write('\r\033[K新url headers失效，启用旧url')
            r.close()
            r = requests.get(url,headers= headers,timeout = 10)
            data = r.json()
        r.close()
        if 'room_list' in data:
            room_list = data.get('room_list')
        else:
            room_list = data
        #item = room_list[0]
        for item in room_list:
            if 'data' in item:
                sroom = item['data']
            else:
                sroom = item
            nickname = sroom['owner']['nickname']
            #nickname = sroom['data']['owner']['nickname']
            rstr = r"[\/\\\:\*\?\"\<\>\|\- ]"
            nickname = re.sub(rstr,"_",nickname)
            if not nickname in names:
                if 'hls_pull_url_params' in sroom['stream_url']:
                    hls_params = sroom['stream_url']['hls_pull_url_params']
                else:
                    hls_params = 'h264'
                if 'h264' in hls_params or hls_params == '{}':
                    print('\r\033[K',nickname,'h264格式，启用flv')
                    a = room(nickname,sroom['stream_url']['rtmp_pull_url'])
                    #a = room(nickname,sroom['data']['stream_url']['rtmp_pull_url'])
                    s = Thread(target=download,args=(a,),name=(nickname))
                    s.start()
                    names.append(nickname)
                elif 'h265' in hls_params:
                    print('\r\033[K',nickname,'h265格式，启用m3u8')
                    b = room(nickname,sroom['stream_url']['hls_pull_url'])
                    x = Thread(target=download_hls,args=(b,),name=(nickname+'_m3u8'))
                    x.start()
                    names.append(nickname)
                else:
                    if not hls_params:
                        print('hls_params为空')
                    else:
                        print('\r\033[K','未知格式',hls_params)
    except:
        traceback.print_exc()
    namenum = len(names)
    time.sleep(random.randint(9,10))
