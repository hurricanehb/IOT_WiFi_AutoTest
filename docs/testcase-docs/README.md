# 测试用例文档目录

这里存放的是用于参考、整理和生成 pytest 测试用例 md 的文本说明，不放可执行测试代码。

本目录是当前工程里唯一的测试用例文本入口；`testcases/` 下只保留 pytest 执行代码。

## 目录约定

- `android/`：Android / HyperWiFi 相关需求与用例说明
- `miniAP/`：miniAP 相关需求与用例说明
- `smoke/`：冒烟场景说明
- `template.md`：生成测试用例 md 的统一模板

## 快速入口

- [Android 文档索引](android/README.md)
- [miniAP 文档索引](miniAP/README.md)
- [Smoke 文档索引](smoke/README.md)

## 写法建议

- 需求原文、业务规则、前置条件、步骤、预期结果分开写清楚
- 用例摘要尽量保持稳定，和 pytest 用例名一一对应
- 如果某条用例暂时只能手工执行，在文档里标注 `manual`
- 新增或修改用例时，优先同步更新本目录下对应说明，再落到 `testcases/` 代码

## 参考关系

- 执行代码：`testcases/`
- 业务数据：`testdata/`
- 通用生成规范：`tools/pytest-automation/`
