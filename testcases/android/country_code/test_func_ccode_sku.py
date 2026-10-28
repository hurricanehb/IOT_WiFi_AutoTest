"""WiFi 连接 — Func_Ccode_SKU（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/HyperWiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/ITR专项.md, tools/files-transfer/Android WiFi&HyperWiFi/MIX机型-USB模式切换.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN热点.md, tools/files-transfer/Android WiFi&HyperWiFi/WLAN高级设置.md, tools/files-transfer/Android WiFi&HyperWiFi/传统WiFi低功耗.md, tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md, tools/files-transfer/Android WiFi&HyperWiFi/双链路主备切换管理.md, tools/files-transfer/Android WiFi&HyperWiFi/国家码.md, tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md, tools/files-transfer/Android WiFi&HyperWiFi/性能测试.md, tools/files-transfer/Android WiFi&HyperWiFi/无线接入.md, tools/files-transfer/Android WiFi&HyperWiFi/无线黑名单.md, tools/files-transfer/Android WiFi&HyperWiFi/漫游.md, tools/files-transfer/Android WiFi&HyperWiFi/稳定性测试.md, tools/files-transfer/Android WiFi&HyperWiFi/组件.md, tools/files-transfer/Android WiFi&HyperWiFi/网络选择.md
"""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.country_code

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_SKU_Vali_001")
@pytest.mark.wifi_case(
    title="默认EU SKU：先刷软件，再刷EU SKU",
    pre="设备未刷SKU，软件包可用",
)
def test_Func_Ccode_SKU_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_SKU_Vali_002")
@pytest.mark.wifi_case(
    title="默认EU SKU：先刷EU SKU，再刷软件",
    pre="设备未刷SKU，软件包可用",
)
def test_Func_Ccode_SKU_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_SKU_Vali_003")
@pytest.mark.wifi_case(
    title="默认US SKU：先刷软件，再刷US SKU",
    pre="设备未刷SKU，软件包可用",
)
def test_Func_Ccode_SKU_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_SKU_Vali_004")
@pytest.mark.wifi_case(
    title="默认US SKU：先刷US SKU，再刷软件",
    pre="设备未刷SKU，软件包可用",
)
def test_Func_Ccode_SKU_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_SKU_Vali_005")
@pytest.mark.wifi_case(
    title="重启与出厂一致性（EU）",
    pre="设备已按场景1或场景2刷入EU SKU",
)
def test_Func_Ccode_SKU_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_SKU_Vali_006")
@pytest.mark.wifi_case(
    title="重启与出厂一致性（US）",
    pre="设备已按场景1或场景2刷入US SKU",
)
def test_Func_Ccode_SKU_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_SKU_Vali_007")
@pytest.mark.wifi_case(
    title="SKU仅在首次配置生效（EU）",
    pre="设备已刷EU SKU，已重启生效",
)
def test_Func_Ccode_SKU_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_SKU_Vali_008")
@pytest.mark.wifi_case(
    title="SKU仅在首次配置生效（US）",
    pre="设备已刷US SKU，已重启生效",
)
def test_Func_Ccode_SKU_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_SKU_Vali_009")
@pytest.mark.wifi_case(
    title="恢复出厂后SKU重新生效（EU）",
    pre="设备已刷EU SKU",
)
def test_Func_Ccode_SKU_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_SKU_Vali_010")
@pytest.mark.wifi_case(
    title="恢复出厂后SKU重新生效（US）",
    pre="设备已刷US SKU",
)
def test_Func_Ccode_SKU_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_SKU_Int_001")
@pytest.mark.wifi_case(
    title="EU SKU基础上验证shell命令配置",
    pre="设备国家码为EU",
)
def test_Func_Ccode_SKU_Int_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_SKU_Int_002")
@pytest.mark.wifi_case(
    title="US SKU基础上验证shell命令配置",
    pre="设备国家码为US",
)
def test_Func_Ccode_SKU_Int_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_SKU_Int_003")
@pytest.mark.wifi_case(
    title="远配覆盖SKU配置（EU）",
    pre="设备国家码为EU",
)
def test_Func_Ccode_SKU_Int_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_SKU_Int_004")
@pytest.mark.wifi_case(
    title="远配覆盖SKU配置（US）",
    pre="设备国家码为US",
)
def test_Func_Ccode_SKU_Int_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_SKU_Int_005")
@pytest.mark.wifi_case(
    title="EU切换为US SKU",
    pre="设备已刷EU SKU",
)
def test_Func_Ccode_SKU_Int_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.case_id("Func_Ccode_SKU_Int_006")
@pytest.mark.wifi_case(
    title="US切换为EU SKU",
    pre="设备已刷US SKU",
)
def test_Func_Ccode_SKU_Int_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.stress
@pytest.mark.case_id("Func_Ccode_SKU_Stb_001")
@pytest.mark.wifi_case(
    title="多次恢复出厂（EU）",
    pre="设备已刷EU SKU",
)
def test_Func_Ccode_SKU_Stb_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.stress
@pytest.mark.case_id("Func_Ccode_SKU_Stb_002")
@pytest.mark.wifi_case(
    title="多次恢复出厂（US）",
    pre="设备已刷US SKU",
)
def test_Func_Ccode_SKU_Stb_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.hyperwifi
@pytest.mark.stress
@pytest.mark.case_id("Func_Ccode_SKU_Stb_003")
@pytest.mark.wifi_case(
    title="多次连续刷写（EU→US循环）",
    pre="设备未刷SKU",
)
def test_Func_Ccode_SKU_Stb_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
