"""为缺少摘要的 sheet md 补全摘要并写回。"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

from testcase_parser import parse_testcase_blocks

MD_DIR = ROOT / "tools" / "files-transfer" / "Android WiFi&HyperWiFi"
WLAN_ACCESS = MD_DIR / "无线接入.md"

ATTR_RE = re.compile(
    r"(\*\*属性：\*\*\s*优先级：)([^；\n]*)(；摘要：)([^；\n]*)(；类型：)([^；\n]*)(；标签：)([^\n]*)"
)

HOTSPOT_RULES = (
    (re.compile(r"^接入Android (\d+)热点后正常访问网络$"), "Func_Compat_Hotspot_Android_Vali_{:03d}"),
    (re.compile(r"^接入IOS (\d+)热点后正常访问网络$"), "Func_Compat_Hotspot_Ios_Vali_{:03d}"),
    (re.compile(r"^接入Windows (\d+)热点后正常访问网络$"), "Func_Compat_Hotspot_Windows_Vali_{:03d}"),
)

WIFI_LP_L2 = {
    "亮屏状态": "ScreenOn",
    "息屏状态": "ScreenOff",
    "APF机制": "Apf",
    "WoWLAN（Wake on Wireless LAN）机制": "Wowlan",
    "状态转换组合测试": "StateChange",
}

WIFI_LP_L3 = {
    "功能有效性": "Vali",
    "压力测试": "Stress",
    "稳定性测试": "Stb",
}

MULTI_NET_L3 = {
    "上电初始化场景": "BootInit",
    "链路变化触发选择": "LinkChange",
    "网络恶化场景": "Degrade",
    "网络恢复场景": "Recover",
    "网络恢复与业务并发": "RecoverBiz",
}


@dataclass
class CaseContext:
    title: str
    l2: str = ""
    l3: str = ""


def title_summary_map(doc: Path) -> dict[str, str]:
    return {c["title"]: c["summary"] for c in parse_testcase_blocks(doc) if c["summary"]}


def parse_case_contexts(path: Path) -> list[CaseContext]:
    contexts: list[CaseContext] = []
    l2 = l3 = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            l2 = line[3:].strip()
            l3 = ""
        elif line.startswith("### "):
            l3 = line[4:].strip()
        elif line.startswith("#### "):
            contexts.append(CaseContext(title=line[5:].strip(), l2=l2, l3=l3))
    return contexts


def build_wifi_lp_summaries(contexts: list[CaseContext]) -> dict[str, str]:
    counters: dict[str, int] = {}
    result: dict[str, str] = {}
    for ctx in contexts:
        area = WIFI_LP_L2.get(ctx.l2, "General")
        case_type = WIFI_LP_L3.get(ctx.l3, "Vali")
        if ctx.l2 == "状态转换组合测试" and ctx.l3 in {"压力测试", "稳定性测试"}:
            area = "Stress" if ctx.l3 == "压力测试" else "Stb"
            case_type = "Vali"
        key = f"{area}_{case_type}"
        counters[key] = counters.get(key, 0) + 1
        result[ctx.title] = f"Func_WiFiLP_{area}_{case_type}_{counters[key]:03d}"
    return result


def build_multi_net_summaries(contexts: list[CaseContext]) -> dict[str, str]:
    counters: dict[str, int] = {}
    result: dict[str, str] = {}
    for ctx in contexts:
        section = MULTI_NET_L3.get(ctx.l3, "General")
        counters[section] = counters.get(section, 0) + 1
        result[ctx.title] = f"Func_MultiNet_{section}_Vali_{counters[section]:03d}"
    return result


def build_compat_summaries(titles: list[str], wlan_map: dict[str, str]) -> dict[str, str]:
    counters = {"android": 0, "ios": 0, "windows": 0, "portal": 0, "wapi": 0, "encrypt": 0}
    result: dict[str, str] = {}

    def bump(key: str) -> int:
        counters[key] += 1
        return counters[key]

    for title in titles:
        if title in wlan_map:
            result[title] = wlan_map[title]
            continue

        for pattern, fmt in HOTSPOT_RULES:
            match = pattern.match(title)
            if match:
                ver = int(match.group(1))
                if "Android" in fmt:
                    result[title] = fmt.format(ver - 10)
                elif "Ios" in fmt:
                    result[title] = fmt.format(ver - 15)
                else:
                    result[title] = fmt.format(ver - 9)
                break
        else:
            if "Portal" in title:
                result[title] = f"Func_Compat_Portal_Vali_{bump('portal'):03d}"
            elif title == "AP设置mac接入网络":
                result[title] = "Func_Compat_MacAccess_Vali_001"
            elif "WAPI" in title:
                result[title] = f"Func_Compat_Wapi_Vali_{bump('wapi'):03d}"
            elif "FT属性" in title:
                result[title] = "Func_Compat_FtRoaming_Vali_001"
            else:
                result[title] = f"Func_Compat_Encrypt_Vali_{bump('encrypt'):03d}"

    return result


def patch_md(
    path: Path,
    replacements: dict[str, str],
    *,
    default_type: str = "手工",
    default_tag: str = "WiFi",
) -> int:
    text = path.read_text(encoding="utf-8")
    blocks = text.split("#### ")
    if len(blocks) <= 1:
        return 0

    updated = 0
    new_blocks = [blocks[0]]
    for block in blocks[1:]:
        title = block.splitlines()[0].strip()
        summary = replacements.get(title)
        if not summary:
            new_blocks.append(block)
            continue

        def repl(match: re.Match[str]) -> str:
            nonlocal updated
            current = match.group(4).strip()
            if current and current not in {"", "/"}:
                return match.group(0)
            updated += 1
            case_type = match.group(6).strip() or default_type
            tag = match.group(8).strip() or default_tag
            return (
                f"{match.group(1)}{match.group(2)}{match.group(3)}{summary}"
                f"{match.group(5)}{case_type}{match.group(7)}{tag}"
            )

        new_blocks.append(re.sub(ATTR_RE, repl, block, count=1))
    path.write_text("#### ".join(new_blocks), encoding="utf-8")
    return updated


def fill_sheet(path: Path, replacements: dict[str, str], *, default_type: str = "手工", default_tag: str = "WiFi") -> int:
    return patch_md(path, replacements, default_type=default_type, default_tag=default_tag)


def main() -> int:
    wlan_map = title_summary_map(WLAN_ACCESS)

    itr_path = MD_DIR / "ITR专项.md"
    fill_sheet(itr_path, {"连接WiFi7 AP（按兼容性矩阵扩充：）": "Func_ITR_WiFi7_Conn_Vali_001"})

    compat_path = MD_DIR / "兼容性.md"
    compat_titles = [c.title for c in parse_case_contexts(compat_path)]
    fill_sheet(compat_path, build_compat_summaries(compat_titles, wlan_map))

    wifi_lp_path = MD_DIR / "传统WiFi低功耗.md"
    wifi_lp_updated = fill_sheet(wifi_lp_path, build_wifi_lp_summaries(parse_case_contexts(wifi_lp_path)))

    multi_net_path = MD_DIR / "多网络共存.md"
    multi_net_updated = fill_sheet(
        multi_net_path,
        build_multi_net_summaries(parse_case_contexts(multi_net_path)),
        default_tag="Common",
    )

    print(f"传统WiFi低功耗.md: updated {wifi_lp_updated} summaries, parsed {len(parse_testcase_blocks(wifi_lp_path))}")
    print(f"多网络共存.md: updated {multi_net_updated} summaries, parsed {len(parse_testcase_blocks(multi_net_path))}")
    print(f"ITR parsed: {len(parse_testcase_blocks(itr_path))}")
    print(f"兼容性 parsed: {len(parse_testcase_blocks(compat_path))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
