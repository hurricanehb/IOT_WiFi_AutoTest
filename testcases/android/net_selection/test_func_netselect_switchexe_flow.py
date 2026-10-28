"""WiFi 连接 — Func_NetSelect_SwitchExe_Flow（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_SwitchExe_Flow_Vali_001")
@pytest.mark.wifi_case(
    title="获胜候选网络与当前网络匹配",
    pre="1、陪测设备AP1、AP2、miniAP1、miniAP2 2、匹配条件： (1).设备已连接至一个 Wi-Fi 网络（当前网络）。 (2)存在另一个 Wi-Fi 网络（获胜候选网络），该网络与当前网络满足以下任一匹配条件： - 条件 A（BSSID 相同）：候选网络与当前网络具有完全相同的 BSSID - 条件 B（SSID+安全类型相同）：若设备支持固件漫游/BSSID黑名单功能，候选网络与当前网络具有相同的 SSID 和 安全类型（如 WPA2-PSK）。",
)
def test_Func_NetSelect_SwitchExe_Flow_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_NetSelect_SwitchExe_Flow_Vali_002")
@pytest.mark.wifi_case(
    title="获胜候选网络与当前网络不匹配",
    pre="1. 设备已连接至一个 Wi-Fi 网络（当前网络）。 2. 存在另一个 Wi-Fi 网络（获胜候选网络），该网络与当前网络不满足任何匹配条件（即 BSSID 不同，且若支持固件漫游，则 SSID 或 安全类型也不同）。 3. 获胜候选网络的信号质量优于当前网络。",
)
def test_Func_NetSelect_SwitchExe_Flow_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
