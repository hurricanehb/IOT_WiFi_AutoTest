# Android 测试用例参考文档

这里存放 Android / HyperWiFi 相关的文本测试说明，用于生成或校对 `testcases/android/**` 下的测试用例 md。

当前正文已迁移到本目录，`testcases/android/**` 只保留 pytest 执行代码和 fixture。

建议按功能域继续拆分，例如：

- `country_code/`：国家码映射说明
- `wifi_connection/`：WLAN / WiFi 连接说明
- `performance/`：吞吐量、时延、连接能力等性能说明
- `settings/`：设置类说明

## 当前正文

- [country_code/country.md](country_code/country.md)
- [country_code/country-code.md](country_code/country-code.md)
- [wifi_connection/wifi-connection.md](wifi_connection/wifi-connection.md)
- [wifi_connection/wifi-connection-automation.md](wifi_connection/wifi-connection-automation.md)
- [wifi_connection/testcases.md](wifi_connection/testcases.md)（当前主文档，由 Excel 导出）
- [wifi_connection/testcases_wifi.md](wifi_connection/testcases_wifi.md)（旧版编号，归档）
- [wifi_connection/testcases_wifi-automation.md](wifi_connection/testcases_wifi-automation.md)
- [performance/testcases.md](performance/testcases.md)
- [performance/performance-automation.md](performance/performance-automation.md)
- [wlan_access/wifi-ap-telnet-configuration.md](wlan_access/wifi-ap-telnet-configuration.md)

每个功能域内尽量保持和 `testcases/android/<module>/` 同名或近似命名，便于快速对照。
