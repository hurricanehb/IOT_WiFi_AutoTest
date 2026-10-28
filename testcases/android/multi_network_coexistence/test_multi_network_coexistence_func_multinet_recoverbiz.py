"""WiFi 连接 — Func_MultiNet_RecoverBiz（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_RecoverBiz_Vali_001")
@pytest.mark.wifi_case(
    title="应用绑定非默认网络",
    pre="设备默认网络为LAN，编写测试App（或使用adb shell cmd network）绑定到蜂窝",
)
def test_Func_MultiNet_RecoverBiz_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_RecoverBiz_Vali_002")
@pytest.mark.wifi_case(
    title="下单打印任务中网络切换",
    pre="设备正在执行依赖网络的打印任务（如云打印），同时连接WLAN和蜂窝",
)
def test_Func_MultiNet_RecoverBiz_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_RecoverBiz_Vali_003")
@pytest.mark.wifi_case(
    title="OTA下载中网络切换",
    pre="设备正在进行OTA升级包下载，默认网络为WLAN",
)
def test_Func_MultiNet_RecoverBiz_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_RecoverBiz_Vali_004")
@pytest.mark.wifi_case(
    title="OTA升级中网络切换",
    pre="设备已完成下载，正在安装升级包",
)
def test_Func_MultiNet_RecoverBiz_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
