"""WiFi 连接 — Func_WlanAccess_Conn_Encrypt（手工/实验室场景）

静态 pytest 脚本，运行期不读取 md 文档。
源文档：tools/files-transfer/Android WiFi&HyperWiFi/兼容性.md
"""
from __future__ import annotations

import pytest

from testcases.support.case_api import run_manual_placeholder

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_052")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为Open",
    pre="1. AP配置为开放(Open)模式，无任何加密； 2. 无Portal认证； 3. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_052(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_001")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WEP-40",
    pre="1. AP配置为WEP-40加密，密钥索引为1，密钥已知； 2. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_001(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_002")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WEP-104",
    pre="1. AP配置为WEP-104加密，密钥索引为1，密钥已知； 2. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_002(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_003")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WEP-128",
    pre="1. AP配置为WEP-128加密，密钥已知； 2. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_003(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_004")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA-CCMP",
    pre="1. AP配置为WPA-PSK，加密算法为CCMP(AES)； 2. 已知Wi-Fi密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_004(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_005")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA-TKIP/CCMP",
    pre="1. AP配置为WPA-PSK，加密算法为TKIP/CCMP混合； 2. 已知Wi-Fi密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_005(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_006")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2-TKIP",
    pre="1. AP配置为WPA2-PSK，加密算法为TKIP； 2. 已知Wi-Fi密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_006(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_009")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2-CCMP，关闭pmf",
    pre="1. AP配置为WPA2-PSK，加密算法为CCMP(AES)，PMF设置为“禁用”； 2. 已知Wi-Fi密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_009(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_007")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2-CCMP，强制开启pmf",
    pre="1. AP配置为WPA2-PSK，加密算法为CCMP(AES)，PMF设置为“强制”； 2. 已知Wi-Fi密码； 3. DUT支持PMF功能。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_007(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_008")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2-CCMP，可选开启pmf",
    pre="1. AP配置为WPA2-PSK，加密算法为CCMP(AES)，PMF设置为“可选”； 2. 已知Wi-Fi密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_008(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_012")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2-TKIP或CCMP，关闭pmf",
    pre="1. AP配置为WPA2-PSK，加密算法为TKIP/CCMP混合，PMF禁用； 2. 已知Wi-Fi密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_012(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_010")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2-TKIP或CCMP，强制开启pmf",
    pre="1. AP配置为WPA2-PSK，加密算法为TKIP/CCMP混合，PMF强制； 2. 已知Wi-Fi密码； 3. DUT支持PMF。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_010(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_011")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2-TKIP或CCMP，可选开启pmf",
    pre="1. AP配置为WPA2-PSK，加密算法为TKIP/CCMP混合，PMF可选； 2. 已知Wi-Fi密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_011(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_013")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2混合，TKIP加密",
    pre="1. AP配置为WPA/WPA2混合模式，加密算法为TKIP； 2. 已知Wi-Fi密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_013(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_016")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2混合，CCMP加密，关闭pmf",
    pre="1. AP配置为WPA/WPA2混合模式，加密算法为CCMP，PMF禁用； 2. 已知Wi-Fi密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_016(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_014")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2混合，CCMP加密，强制开启pmf",
    pre="1. AP配置为WPA/WPA2混合模式，加密算法为CCMP，PMF强制； 2. 已知Wi-Fi密码； 3. DUT支持PMF。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_014(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_015")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2混合，CCMP加密，可选开启pmf",
    pre="1. AP配置为WPA/WPA2混合模式，加密算法为CCMP，PMF可选； 2. 已知Wi-Fi密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_015(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_019")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2-混合，TKIP或CCMP加密，关闭pmf",
    pre="1. AP配置为WPA/WPA2混合模式，加密算法为TKIP/CCMP混合，PMF禁用； 2. 已知Wi-Fi密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_019(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_017")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2-混合，TKIP或CCMP加密，强制开启pmf",
    pre="1. AP配置为WPA/WPA2混合模式，加密算法为TKIP/CCMP混合，PMF强制； 2. 已知Wi-Fi密码； 3. DUT支持PMF。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_017(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_018")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2-混合，TKIP或CCMP加密，可选开启pmf",
    pre="1. AP配置为WPA/WPA2混合模式，加密算法为TKIP/CCMP混合，PMF可选； 2. 已知Wi-Fi密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_018(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_053")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为OWE",
    pre="1. AP配置为OWE(Enhanced Open)模式； 2. 不需要预共享密码； 3. DUT支持OWE。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_053(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_054")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为OWE过渡模式",
    pre="1. AP配置为OWE过渡模式（同时广播Open和OWE网络）； 2. DUT支持OWE； 3. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_054(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_020")
@pytest.mark.wifi_case(
    title="WPA2/WPA3混合，可选启用pmf",
    pre="1. AP配置为WPA2/WPA3混合模式，PMF设置为“可选”； 2. 已知Wi-Fi密码； 3. DUT支持WPA3。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_020(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_021")
@pytest.mark.wifi_case(
    title="WPA2/WPA3混合，强制启用pmf（暂无AP支持配置强制开启或关闭pmf）",
    pre="1. AP配置为WPA2/WPA3混合模式，PMF设置为“强制”； 2. 已知Wi-Fi密码； 3. DUT支持WPA3及PMF。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_021(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_022")
@pytest.mark.wifi_case(
    title="WPA2/WPA3混合，强制关闭pmf（暂无AP支持配置强制开启或关闭pmf）",
    pre="1. AP配置为WPA2/WPA3混合模式，PMF设置为“禁用”； 2. 已知Wi-Fi密码； 3. DUT支持WPA3。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_022(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_027")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3个人级，CCMP加密，可选开启pmf",
    pre="1. AP配置为WPA3-Personal(SAE)，加密算法CCMP，PMF可选； 2. 已知SAE密码； 3. DUT支持WPA3。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_027(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_028")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3个人级，CCMP加密，强制开启pmf",
    pre="1. AP配置为WPA3-Personal(SAE)，加密算法CCMP，PMF强制； 2. 已知SAE密码； 3. DUT支持WPA3。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_028(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_029")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3个人级，CCMP加密，强制关闭pmf",
    pre="1. AP配置为WPA3-Personal(SAE)，加密算法CCMP，PMF禁用； 2. 已知SAE密码； 3. DUT支持WPA3。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_029(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_030")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3个人级，AES256GCM加密，强制开启pmf",
    pre="1. AP配置为WPA3-Personal(SAE)，加密算法AES256-GCMP，PMF强制； 2. 已知SAE密码； 3. DUT支持GCMP256加密。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_030(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_031")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3个人级过渡模式，CCMP加密，强制开启pmf",
    pre="1. AP配置为WPA3过渡模式（兼容WPA2/WPA3），CCMP加密，PMF强制； 2. 已知Wi-Fi密码； 3. DUT支持WPA3。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_031(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_032")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3个人级过渡模式，CCMP加密，关闭pmf",
    pre="1. AP配置为WPA3过渡模式，CCMP加密，PMF禁用； 2. 已知Wi-Fi密码； 3. DUT支持WPA3。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_032(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_033")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3企业级过渡模式-CCMP",
    pre="1. 已搭建RADIUS服务器； 2. AP配置WPA3-Enterprise过渡模式，CCMP加密； 3. DUT已获得合法企业认证账号/证书。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_033(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_034")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3企业级only模式-CCMP",
    pre="1. 已搭建RADIUS服务器； 2. AP配置WPA3-Enterprise Only模式，CCMP加密； 3. DUT支持WPA3企业级。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_034(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_035")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3企业级-GCMP（无可配ACAP）",
    pre="1. 已搭建RADIUS服务器； 2. AP配置WPA3-Enterprise，加密算法GCMP； 3. DUT支持GCMP。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_035(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_036")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3企业级192bit模式-GCMP",
    pre="1. 已搭建支持192bit模式的RADIUS服务器； 2. AP配置WPA3-Enterprise 192bit模式，GCMP-256加密； 3. DUT支持192bit企业级。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_036(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_037")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA3企业级192bit模式-CNSA（政府军用）",
    pre="1. 已搭建符合CNSA标准的RADIUS服务器； 2. AP配置WPA3-Enterprise CNSA模式； 3. DUT支持CNSA套件。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_037(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_038")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2企业级CCMP加密，可选开启PMF",
    pre="1. 已搭建RADIUS服务器； 2. AP配置WPA2-Enterprise，CCMP加密，PMF可选； 3. DUT已获得合法企业认证账号。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_038(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p0
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_039")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2企业级CCMP加密，关闭PMF",
    pre="1. 已搭建RADIUS服务器； 2. AP配置WPA2-Enterprise，CCMP加密，PMF禁用； 3. DUT已获得合法企业认证账号。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_039(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_040")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2企业级TKIP或CCMP加密，强制开启PMF",
    pre="1. 已搭建RADIUS服务器； 2. AP配置WPA2-Enterprise，TKIP/CCMP混合加密，PMF强制； 3. DUT支持PMF。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_040(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_041")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2企业级TKIP或CCMP加密，可选开启PMF",
    pre="1. 已搭建RADIUS服务器； 2. AP配置WPA2-Enterprise，TKIP/CCMP混合加密，PMF可选； 3. DUT已获得合法企业认证账号。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_041(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_042")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2企业级TKIP或CCMP加密，关闭PMF",
    pre="1. 已搭建RADIUS服务器； 2. AP配置WPA2-Enterprise，TKIP/CCMP混合加密，PMF禁用； 3. DUT已获得合法企业认证账号。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_042(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_043")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA2企业级TKIP加密",
    pre="1. 已搭建RADIUS服务器； 2. AP配置WPA2-Enterprise，仅TKIP加密； 3. DUT已获得合法企业认证账号。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_043(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_044")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2企业级CCMP加密，强制开启PMF",
    pre="1. 已搭建RADIUS服务器； 2. AP配置WPA/WPA2-Enterprise混合，CCMP加密，PMF强制； 3. DUT支持PMF。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_044(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_045")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2企业级CCMP加密，可选开启PMF",
    pre="1. 已搭建RADIUS服务器； 2. AP配置WPA/WPA2-Enterprise混合，CCMP加密，PMF可选； 3. DUT已获得合法企业认证账号。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_045(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_046")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2企业级CCMP加密，关闭PMF",
    pre="1. 已搭建RADIUS服务器； 2. AP配置WPA/WPA2-Enterprise混合，CCMP加密，PMF禁用； 3. DUT已获得合法企业认证账号。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_046(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_047")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2企业级TKIP或CCMP加密，强制开启PMF",
    pre="1. 已搭建RADIUS服务器； 2. AP配置WPA/WPA2-Enterprise混合，TKIP/CCMP混合加密，PMF强制； 3. DUT支持PMF。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_047(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_048")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2企业级TKIP或CCMP加密，可选开启PMF",
    pre="1. 已搭建RADIUS服务器； 2. AP配置WPA/WPA2-Enterprise混合，TKIP/CCMP混合加密，PMF可选； 3. DUT已获得合法企业认证账号。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_048(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_049")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2企业级TKIP或CCMP加密，关闭PMF",
    pre="1. 已搭建RADIUS服务器； 2. AP配置WPA/WPA2-Enterprise混合，TKIP/CCMP混合加密，PMF禁用； 3. DUT已获得合法企业认证账号。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_049(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_050")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA/WPA2企业级TKIP加密",
    pre="1. 已搭建RADIUS服务器； 2. AP配置WPA/WPA2-Enterprise混合，仅TKIP加密； 3. DUT已获得合法企业认证账号。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_050(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_051")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WPA企业级TKIP加密",
    pre="1. 已搭建RADIUS服务器； 2. AP配置WPA-Enterprise，TKIP加密； 3. DUT已获得合法企业认证账号。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_051(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_055")
@pytest.mark.wifi_case(
    title="AP设置开放型Portal网络",
    pre="1. AP/AC配置了开放认证的Portal网络（无密码，需Web认证）； 2. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_055(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_056")
@pytest.mark.wifi_case(
    title="AP设置密码认证型Portal网络",
    pre="1. AP/AC配置了密码认证的Portal网络； 2. 已知Portal认证密码； 3. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_056(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p2
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_057")
@pytest.mark.wifi_case(
    title="AP设置短信认证型Portal网络",
    pre="1. AP/AC配置了短信认证的Portal网络； 2. 有可接收短信的手机号； 3. DUT Wi-Fi功能正常。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_057(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_058")
@pytest.mark.wifi_case(
    title="AP设置mac接入网络",
    pre="1. AP配置了MAC地址白名单认证； 2. DUT的MAC地址已加入白名单； 3. 网络无其他加密方式。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_058(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_059")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WAPI-PSK",
    pre="1. AP配置为WAPI-PSK模式； 2. DUT支持WAPI协议且已预置PSK； 3. 已知WAPI-PSK密钥。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_059(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p3
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_060")
@pytest.mark.wifi_case(
    title="AP设置无线加密方式为WAPI证书认证--终端未适配，缺测试环境",
    pre="1. AP配置为WAPI证书认证模式； 2. 已部署WAPI证书颁发系统； 3. DUT已安装合法WAPI证书； 4. 测试环境完备。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_060(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)

@pytest.mark.p1
@pytest.mark.wifi
@pytest.mark.case_id("Func_WlanAccess_Conn_Encrypt_Vali_061")
@pytest.mark.wifi_case(
    title="AC+AP场景启用FT属性",
    pre="1. AC+AP组网已部署，启用快速漫游(802.11r)； 2. SSID配置WPA2-Enterprise或WPA3-Enterprise； 3. DUT支持802.11r。",
)
def test_Func_WlanAccess_Conn_Encrypt_Vali_061(run_shell_cmd, wifi, wifi_yaml, wifi_case):
    run_manual_placeholder(wifi_case, run_shell_cmd)
