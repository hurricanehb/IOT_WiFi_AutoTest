"""WiFi 连接 — Func_MultiNet_LinkChange（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/多网络共存.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_001")
@pytest.mark.wifi_case(
    title="当前链路状态变化正常->异常",
    pre="设备三网均有网，默认网络为以太网",
)
def test_Func_MultiNet_LinkChange_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_002")
@pytest.mark.wifi_case(
    title="当前链路状态变化异常->正常",
    pre="当前默认网络为WLAN（因LAN断开），LAN已恢复有网",
)
def test_Func_MultiNet_LinkChange_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_003")
@pytest.mark.wifi_case(
    title="当前链路无变化，其他链路状态发生变化",
    pre="设备默认网络为以太网，WLAN和蜂窝均有网",
)
def test_Func_MultiNet_LinkChange_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_004")
@pytest.mark.wifi_case(
    title="依次接入蜂窝/WLAN/LAN链路且有网",
    pre="设备关机，所有网络关闭",
)
def test_Func_MultiNet_LinkChange_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_005")
@pytest.mark.wifi_case(
    title="依次接入LAN/WLAN/蜂窝链路且有网",
    pre="设备关机，所有网络关闭",
)
def test_Func_MultiNet_LinkChange_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_006")
@pytest.mark.wifi_case(
    title="依次接入蜂窝/WLAN/LAN链路且无网",
    pre="设备关机，所有网络关闭，各网络上联均无外网",
)
def test_Func_MultiNet_LinkChange_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_007")
@pytest.mark.wifi_case(
    title="依次接入LAN/WLAN/蜂窝链路且无网",
    pre="设备关机，所有网络关闭，各网络上联均无外网",
)
def test_Func_MultiNet_LinkChange_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_008")
@pytest.mark.wifi_case(
    title="依次断开蜂窝、WLAN、LAN链路",
    pre="设备三网均有网，默认网络为以太网",
)
def test_Func_MultiNet_LinkChange_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_009")
@pytest.mark.wifi_case(
    title="依次断开LAN、WLAN、蜂窝链路",
    pre="设备三网均有网，默认网络为以太网",
)
def test_Func_MultiNet_LinkChange_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_010")
@pytest.mark.wifi_case(
    title="当前使用LAN，LAN 拔插网线",
    pre="设备使用LAN上网，WLAN和蜂窝可用",
)
def test_Func_MultiNet_LinkChange_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_011")
@pytest.mark.wifi_case(
    title="当前使用LAN，WLAN 断开重连",
    pre="设备使用LAN上网，WLAN和蜂窝可用",
)
def test_Func_MultiNet_LinkChange_Vali_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_012")
@pytest.mark.wifi_case(
    title="当前使用LAN，蜂窝 断开重连",
    pre="设备使用LAN上网，WLAN和蜂窝可用",
)
def test_Func_MultiNet_LinkChange_Vali_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_013")
@pytest.mark.wifi_case(
    title="当前使用WLAN，LAN 拔插网线",
    pre="设备使用WLAN上网，LAN已插但优先级低于WLAN（或无网）",
)
def test_Func_MultiNet_LinkChange_Vali_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_014")
@pytest.mark.wifi_case(
    title="当前使用WLAN，WLAN 断开重连",
    pre="设备使用WLAN上网，蜂窝可用",
)
def test_Func_MultiNet_LinkChange_Vali_014(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_015")
@pytest.mark.wifi_case(
    title="当前使用WLAN，WLAN漫游切换",
    pre="设备连接WLAN（AP1），同时开启蜂窝，两AP同SSID且覆盖重叠",
)
def test_Func_MultiNet_LinkChange_Vali_015(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_016")
@pytest.mark.wifi_case(
    title="当前使用WLAN，WLAN网络重选（切换AP）",
    pre="WLAN连接AP1，蜂窝可用",
)
def test_Func_MultiNet_LinkChange_Vali_016(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_017")
@pytest.mark.wifi_case(
    title="当前使用WLAN，WLAN主备切换",
    pre="设备同时连接WLAN、蜂窝、蜂窝，均有网",
)
def test_Func_MultiNet_LinkChange_Vali_017(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_018")
@pytest.mark.wifi_case(
    title="当前使用WLAN，蜂窝 断开重连",
    pre="设备使用WLAN上网，蜂窝可用",
)
def test_Func_MultiNet_LinkChange_Vali_018(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_019")
@pytest.mark.wifi_case(
    title="当前使用蜂窝，LAN 拔插网线",
    pre="设备使用蜂窝上网，LAN和WLAN可用",
)
def test_Func_MultiNet_LinkChange_Vali_019(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_020")
@pytest.mark.wifi_case(
    title="当前使用蜂窝，WLAN 断开重连",
    pre="设备使用蜂窝上网，WLAN可用",
)
def test_Func_MultiNet_LinkChange_Vali_020(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_021")
@pytest.mark.wifi_case(
    title="当前使用蜂窝，蜂窝 断开重连",
    pre="设备使用蜂窝上网，WLAN可用",
)
def test_Func_MultiNet_LinkChange_Vali_021(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_022")
@pytest.mark.wifi_case(
    title="当前使用蜂窝，蜂窝 漫游",
    pre="无",
)
def test_Func_MultiNet_LinkChange_Vali_022(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_023")
@pytest.mark.wifi_case(
    title="共网关场景链路变化",
    pre="设备同时连接LAN和WLAN，两者同一网关（如都连同一路由器），均有网",
)
def test_Func_MultiNet_LinkChange_Vali_023(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_024")
@pytest.mark.wifi_case(
    title="不共网关场景链路变化",
    pre="设备同时连接LAN和WLAN，不同网关（如LAN连路由器A，WLAN连路由器B），均有网",
)
def test_Func_MultiNet_LinkChange_Vali_024(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_025")
@pytest.mark.wifi_case(
    title="DHCP续约",
    pre="设备通过LAN或WLAN获取IP，且已使用较长时间（接近租期一半）",
)
def test_Func_MultiNet_LinkChange_Vali_025(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_026")
@pytest.mark.wifi_case(
    title="链路间歇性闪断",
    pre="设备三网均有网，默认网络为以太网",
)
def test_Func_MultiNet_LinkChange_Vali_026(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.common
@pytest.mark.case_id("Func_MultiNet_LinkChange_Vali_027")
@pytest.mark.wifi_case(
    title="WLAN+蜂窝反复断网联网互切场景",
    pre="设备已插入SIM卡，周围有可用WLAN热点，网络均能正常访问互联网",
)
def test_Func_MultiNet_LinkChange_Vali_027(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
