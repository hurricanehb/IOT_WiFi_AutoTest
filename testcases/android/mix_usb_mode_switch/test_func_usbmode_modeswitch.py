"""WiFi 连接 — Func_UsbMode_ModeSwitch（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_UsbMode_ModeSwitch_Vali_001")
@pytest.mark.wifi_case(
    title="激活后模式转换验证",
    pre="1. 设备恢厂后处于Welcome界面 2. 当前模式为「USB Device」 3. HyperWiFi网络已配置",
)
def test_Func_UsbMode_ModeSwitch_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_UsbMode_ModeSwitch_Vali_002")
@pytest.mark.wifi_case(
    title="已激活设备恢厂后模式验证-基线配置",
    pre="1. 设备已激活 2. 当前模式为「USB Host」 3. 设备烧录P3MIX基线版本 4. HyperWiFi网络已配置",
)
def test_Func_UsbMode_ModeSwitch_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_UsbMode_ModeSwitch_Vali_003")
@pytest.mark.wifi_case(
    title="已激活设备恢厂后模式验证-HyperWiFi配置",
    pre="1. 设备已激活 2. 当前模式为「USB Host」 3. 设备烧录P3MIX HyperWiFi配置版本 4. HyperWiFi网络已配置",
)
def test_Func_UsbMode_ModeSwitch_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.stress
@pytest.mark.case_id("Func_UsbMode_ModeSwitch_Stb_001")
@pytest.mark.wifi_case(
    title="多次恢厂测试-设备模式USB Device",
    pre="1. 设备烧录P3MIX HyperWiFi配置 2. 设备模式为「USB Device」 3. HyperWiFi网络已配置",
)
def test_Func_UsbMode_ModeSwitch_Stb_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.stress
@pytest.mark.case_id("Func_UsbMode_ModeSwitch_Stb_002")
@pytest.mark.wifi_case(
    title="多次恢厂测试-设备模式USB Host",
    pre="1. 设备烧录P3MIX HyperWiFi配置 2. 设备模式为「USB Host」 3. HyperWiFi网络已配置",
)
def test_Func_UsbMode_ModeSwitch_Stb_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
