---
name: testcase-import-pipeline
description: "用于导入测试用例或批量生成用例：执行 Excel 转 Markdown、补全摘要 ID、生成静态 WiFi pytest，以及按 Sheet 整理测试文件。Use when importing test cases, filling summaries, generating pytest modules, or reorganizing generated tests."
---

# Testcase Import Pipeline

Run the repository's conversion stages deliberately. Preserve the source artifact and inspect each stage before continuing because generation and reorganization can write or move many files.

## Pipeline

1. Convert Excel into one Markdown file per sheet:

   ```powershell
   .venv\Scripts\python.exe tools\files-transfer\xlsx2md.py -i <workbook.xlsx> --all-sheets --output-dir <markdown-dir>
   ```

2. Parse the generated Markdown and inspect missing or duplicate summaries. Use `tools/files-transfer/testcase_parser.py` as the canonical parser.
3. Fill summaries only when the naming rule is known and deterministic. Review `tools/files-transfer/fill_missing_summaries.py` before running it because its mappings are sheet-specific.
4. Generate static pytest modules:

   ```powershell
   .venv\Scripts\python.exe tools\files-transfer\generate_wifi_connection_tests.py -i <markdown-file-or-dir>
   ```

5. If legacy tests must be relocated by source sheet, preview the summary-to-sheet mapping first:

   ```powershell
   .venv\Scripts\python.exe tools\files-transfer\reorganize_tests_by_sheet.py --dry-run
   ```

6. Resolve unmapped files, cross-sheet conflicts, and destination collisions. Apply only after the preview is correct:

   ```powershell
   .venv\Scripts\python.exe tools\files-transfer\reorganize_tests_by_sheet.py
   ```

7. Inspect changed files for overwritten content, unresolved summaries, duplicate `case_id` values, and unexpected deletions or moves.
8. Run collection for every affected output package.

## Safety Rules

- Do not invent a summary for a case whose category or numbering rule is ambiguous.
- Do not add another profile or generator branch until existing mappings and helpers have been searched.
- Generated pytest must remain static and must not read Markdown during collection or execution.
- Always run reorganization with `--dry-run` first; execution without that flag performs real file moves.
- Preserve manually maintained tests unless the source mapping proves they are generated artifacts.

## Validation

```powershell
.venv\Scripts\python.exe -m pytest <affected-test-package> --collect-only -q
```

Also confirm that every generated `case_id` resolves to one source summary and that old output IDs have no remaining references.
