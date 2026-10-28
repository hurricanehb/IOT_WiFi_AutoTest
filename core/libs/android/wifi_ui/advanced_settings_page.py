"""Page object for Android WLAN advanced settings."""
from __future__ import annotations

import re
import time
import xml.etree.ElementTree as ET
from typing import Iterable, Optional

from core.libs.android.wifi_ui.advanced_settings_support import AdvancedSettingsSupportUI


class WiFiAdvancedSettingsUI:
    """Read WLAN advanced-setting preferences and their single-choice dialogs."""

    NETWORK_PREFERENCE_LABELS = ("网络偏好设置", "WLAN偏好设置")
    ADVANCED_SETTINGS_LABELS = ("WLAN高级设置", "WLAN 高级设置")
    WLAN_BAND_LABEL = "WLAN频段设置"
    WLAN_BAND_LABELS = ("WLAN频段设置", "WLAN 频段设置")
    WLAN_MODE_LABEL = "WLAN模式设置"
    WLAN_MODE_LABELS = ("WLAN模式设置", "WLAN 模式设置")
    WLAN_ROAM_THRESHOLD_LABEL = "WLAN漫游阈值"
    WLAN_ROAM_THRESHOLD_LABELS = (
        "WLAN漫游阈值",
        "WLAN 漫游阈值",
        "WLAN漫游阈值设置",
        "WLAN 漫游阈值设置",
    )
    WLAN_ROAM_THRESHOLD_CUSTOM_OPTION = "自定义"
    WLAN_ROAM_THRESHOLD_CUSTOM_PROMPT = "请输入自定义漫游阈值（-90 ~ -50 dBm）"
    WLAN_ROAM_THRESHOLD_CUSTOM_INPUT_HINT = "允许填写的数值50~90"
    WLAN_ROAM_SENSITIVITY_LABEL = "WLAN漫游灵敏度"
    WLAN_ROAM_SENSITIVITY_LABELS = (
        "WLAN漫游灵敏度",
        "WLAN 漫游灵敏度",
        "WLAN漫游灵敏度设置",
        "WLAN 漫游灵敏度设置",
    )
    WLAN_ROAM_SENSITIVITY_CUSTOM_OPTION = "自定义"
    WLAN_ROAM_SENSITIVITY_CUSTOM_PROMPT = "请输入自定义漫游灵敏度（1-20dB）"
    WLAN_ROAM_SENSITIVITY_CUSTOM_INPUT_HINT = "允许填写的数值1~20"
    WLAN_TIMEOUT_DISCONNECT_LABEL = "WLAN超时断连设置"
    WLAN_TIMEOUT_DISCONNECT_LABELS = (
        "WLAN超时断连设置",
        "WLAN 超时断连设置",
    )
    WLAN_TIMEOUT_DISCONNECT_CUSTOM_OPTION = "自定义"
    WLAN_TIMEOUT_DISCONNECT_CUSTOM_PROMPT = "请输入自定义超时断连时间（3~20秒）"
    WLAN_TIMEOUT_DISCONNECT_CUSTOM_INPUT_HINT = "允许填写的数值3~20"
    WLAN_ENERGY_SAVE_LABEL = "WLAN省电模式设置"
    WLAN_ENERGY_SAVE_LABELS = (
        "WLAN省电模式设置",
        "WLAN 省电模式设置",
        "WLAN省电模式",
        "WLAN 省电模式",
    )
    WLAN_PRIORITY_LABEL = "WLAN优先等级"
    WLAN_PRIORITY_LABELS = (
        "WLAN优先等级",
        "WLAN 优先等级",
    )

    def __init__(self, settings: AdvancedSettingsSupportUI) -> None:
        self.settings = settings
        self.device = settings.device

    def open(self) -> None:
        """Reach WLAN advanced settings without discarding an already-open page."""
        if self._single_choice_dialog_is_open():
            self.settings.press_back()
        if self._advanced_setting_row() is not None:
            return
        if self._find_entry(self.ADVANCED_SETTINGS_LABELS) is not None:
            self._click_entry(self.ADVANCED_SETTINGS_LABELS)
            self._advanced_setting_row_required()
            return

        self.settings.open_wifi_settings()
        if self._advanced_setting_row() is not None:
            return
        for attempt in range(3):
            if attempt == 0 or self._find_entry(self.ADVANCED_SETTINGS_LABELS) is None:
                self._click_entry(
                    self.NETWORK_PREFERENCE_LABELS, scroll_to_end_before_search=True
                )
            deadline = time.monotonic() + 5.0
            while time.monotonic() < deadline:
                if self._find_entry(self.ADVANCED_SETTINGS_LABELS) is not None:
                    self._click_entry(self.ADVANCED_SETTINGS_LABELS)
                    self._advanced_setting_row_required()
                    return
                time.sleep(0.2)
        self.settings.fail_with_artifacts("点击网络偏好设置后未显示 WLAN 高级设置入口")

    def wlan_mode_summary(self) -> str:
        """Return the summary displayed on the WLAN mode preference row."""
        self._mode_row()
        summary = self._summary_from_hierarchy(
            self.device.dump_hierarchy(), self.WLAN_MODE_LABELS
        )
        if summary is None:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_MODE_LABEL!r} 栏的显示值"
            )
        return summary or ""

    def open_wlan_mode_selector(self) -> None:
        """Open the WLAN mode single-choice dialog and wait for its selection."""
        row = self._mode_row()
        if row is None:
            return
        row.click()
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            if self._selected_mode_from_hierarchy(self.device.dump_hierarchy()):
                return
            time.sleep(0.2)
        self.settings.fail_with_artifacts(
            f"{self.WLAN_MODE_LABEL!r} 弹窗未显示已选中的单选项"
        )

    def selected_wlan_mode(self) -> str:
        """Return the currently selected item in the open WLAN mode dialog."""
        selected = self._selected_mode_from_hierarchy(self.device.dump_hierarchy())
        if selected is None:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_MODE_LABEL!r} 弹窗的已选中项"
            )
        return selected or ""

    def select_wlan_mode(self, mode: str) -> None:
        """Select a WLAN mode option in the open dialog."""
        option = self._find_entry((mode,))
        if option is None or not option.click_exists(timeout=2):
            self.settings.fail_with_artifacts(
                f"未找到 WLAN 模式选项 {mode!r}"
            )

    def confirm_wlan_mode_selection(self) -> None:
        """Confirm the WLAN mode dialog and wait until its preference row returns."""
        button = self.device(resourceId="android:id/button1")
        if not button.click_exists(timeout=1):
            button = self._find_entry(("确认", "确定", "保存", "OK"))
            if button is None or not button.click_exists(timeout=2):
                self.settings.fail_with_artifacts("未找到 WLAN 模式设置弹窗确认按钮")
        self._mode_row()

    @staticmethod
    def wlan_mode_matches(actual: str, expected: str) -> bool:
        """Compare mode text while tolerating vendor-inserted whitespace."""
        return WiFiAdvancedSettingsUI._labels_match(actual, expected)

    def wlan_band_summary(self) -> str:
        """Return the summary displayed on the WLAN band preference row."""
        self._band_row()
        summary = self._summary_from_hierarchy(
            self.device.dump_hierarchy(), self.WLAN_BAND_LABELS
        )
        if summary is None:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_BAND_LABEL!r} 栏的显示值"
            )
        return summary or ""

    def open_wlan_band_selector(self) -> None:
        """Open the WLAN band single-choice dialog and wait for its selection."""
        row = self._band_row()
        if row is None:
            return
        row.click()
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            if self._selected_option_from_hierarchy(self.device.dump_hierarchy()):
                return
            time.sleep(0.2)
        self.settings.fail_with_artifacts(
            f"{self.WLAN_BAND_LABEL!r} 弹窗未显示已选中的单选项"
        )

    def selected_wlan_band(self) -> str:
        """Return the currently selected item in the open WLAN band dialog."""
        selected = self._selected_option_from_hierarchy(self.device.dump_hierarchy())
        if selected is None:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_BAND_LABEL!r} 弹窗的已选中项"
            )
        return selected or ""

    def select_wlan_band(self, band: str) -> None:
        """Select a WLAN band option in the open dialog."""
        option = self._find_entry((band,))
        if option is None or not option.click_exists(timeout=2):
            self.settings.fail_with_artifacts(
                f"未找到 WLAN 频段选项 {band!r}"
            )

    def confirm_wlan_band_selection(self) -> None:
        """Confirm the WLAN band dialog and wait until its preference row returns."""
        button = self.device(resourceId="android:id/button1")
        if not button.click_exists(timeout=1):
            button = self._find_entry(("确认", "确定", "保存", "OK"))
            if button is None or not button.click_exists(timeout=2):
                self.settings.fail_with_artifacts("未找到 WLAN 频段设置弹窗确认按钮")
        self._band_row()

    @staticmethod
    def wlan_band_matches(actual: str, expected: str) -> bool:
        """Compare band text while tolerating vendor-inserted whitespace."""
        return WiFiAdvancedSettingsUI._labels_match(actual, expected)

    def wlan_roam_threshold_summary(self) -> str:
        """Return the summary displayed on the WLAN roaming threshold row."""
        self._roam_threshold_row()
        summary = self._summary_from_hierarchy(
            self.device.dump_hierarchy(), self.WLAN_ROAM_THRESHOLD_LABELS
        )
        if summary is None:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_ROAM_THRESHOLD_LABEL!r} 栏的显示值"
            )
        return summary or ""

    def open_wlan_roam_threshold_selector(self) -> None:
        """Open the WLAN roaming threshold dialog and wait for its selection."""
        row = self._roam_threshold_row()
        if row is None:
            return
        row.click()
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            if self._selected_option_from_hierarchy(self.device.dump_hierarchy()):
                return
            time.sleep(0.2)
        self.settings.fail_with_artifacts(
            f"{self.WLAN_ROAM_THRESHOLD_LABEL!r} 弹窗未显示已选中的单选项"
        )

    def selected_wlan_roam_threshold(self) -> str:
        """Return the selected value in the open WLAN roaming threshold dialog."""
        selected = self._selected_option_from_hierarchy(self.device.dump_hierarchy())
        if selected is None:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_ROAM_THRESHOLD_LABEL!r} 弹窗的已选中项"
            )
        return selected or ""

    def wlan_roam_threshold_options(self) -> tuple[str, ...]:
        """Return WLAN roaming threshold dialog options in their displayed order."""
        options = self._dialog_options_from_hierarchy(self.device.dump_hierarchy())
        if not options:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_ROAM_THRESHOLD_LABEL!r} 弹窗的可选项"
            )
        return options

    def select_wlan_roam_threshold(self, threshold: str) -> None:
        """Select a WLAN roaming threshold option in the open dialog."""
        option = self._find_entry((threshold,))
        if option is None or not option.click_exists(timeout=2):
            self.settings.fail_with_artifacts(
                f"未找到 WLAN 漫游阈值选项 {threshold!r}"
            )

    def confirm_wlan_roam_threshold_selection(self) -> None:
        """Confirm the threshold dialog and wait until its preference row returns."""
        button = self.device(resourceId="android:id/button1")
        if not button.click_exists(timeout=1):
            button = self._find_entry(("确认", "确定", "保存", "OK"))
            if button is None or not button.click_exists(timeout=2):
                self.settings.fail_with_artifacts("未找到 WLAN 漫游阈值弹窗确认按钮")
        self._roam_threshold_row()

    def current_wlan_roam_threshold_custom_dialog(
        self,
    ) -> Optional[tuple[str, str]]:
        """Return custom-dialog text when that dialog is already visible."""
        return self._custom_roam_threshold_dialog_texts_from_hierarchy(
            self.device.dump_hierarchy()
        )

    def open_wlan_roam_threshold_custom_dialog(self) -> tuple[str, str]:
        """Open the custom threshold dialog and return its prompt and input hint."""
        dialog_texts = self.current_wlan_roam_threshold_custom_dialog()
        if dialog_texts is not None:
            return dialog_texts

        if not self._wlan_roam_threshold_selector_is_open():
            if self._single_choice_dialog_is_open():
                self.settings.press_back()
            self.open()
            self.open_wlan_roam_threshold_selector()

        self.select_wlan_roam_threshold(self.WLAN_ROAM_THRESHOLD_CUSTOM_OPTION)
        button = self.device(resourceId="android:id/button1")
        if not button.click_exists(timeout=1):
            button = self._find_entry(("确认", "确定", "保存", "OK"))
            if button is None or not button.click_exists(timeout=2):
                self.settings.fail_with_artifacts("未找到 WLAN 漫游阈值弹窗确认按钮")

        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            dialog_texts = self.current_wlan_roam_threshold_custom_dialog()
            if dialog_texts is not None:
                return dialog_texts
            time.sleep(0.2)
        self.settings.fail_with_artifacts("未读取到 WLAN 漫游阈值自定义弹窗内容")
        return "", ""

    def set_wlan_roam_threshold_custom_value(self, value: str) -> str:
        """Save a custom roaming threshold and return the displayed summary."""
        self.open_wlan_roam_threshold_custom_dialog()
        field = self._custom_input_field("WLAN 漫游阈值")

        field.click()
        field.clear_text()
        field.set_text(value)
        entered_value = field.get_text()
        if not self._labels_match(entered_value, value):
            self.settings.fail_with_artifacts(
                f"WLAN 漫游阈值自定义输入值错误：期望 {value!r}，实际 {entered_value!r}"
            )

        button = self.device(resourceId="android:id/button1")
        if not button.click_exists(timeout=1):
            button = self._find_entry(("确认", "确定", "保存", "OK"))
            if button is None or not button.click_exists(timeout=2):
                self.settings.fail_with_artifacts("未找到 WLAN 漫游阈值自定义弹窗保存按钮")
        return self.wlan_roam_threshold_summary()

    def enter_wlan_roam_threshold_custom_value(self, value: str) -> tuple[str, bool]:
        """Enter a custom threshold and return its displayed text and save state."""
        self.open_wlan_roam_threshold_custom_dialog()
        field = self._custom_input_field("WLAN 漫游阈值")

        field.click()
        field.clear_text()
        field.set_text(value)
        entered_value = field.get_text()
        if not self._labels_match(entered_value, value):
            self.settings.fail_with_artifacts(
                f"WLAN 漫游阈值自定义输入值错误：期望 {value!r}，实际 {entered_value!r}"
            )

        button = self.device(resourceId="android:id/button1")
        if not button.exists:
            button = self._find_entry(("确认", "确定", "保存", "OK"))
            if button is None or not button.exists:
                self.settings.fail_with_artifacts(
                    "未找到 WLAN 漫游阈值自定义弹窗保存按钮"
                )
                return entered_value, False
        return entered_value, bool(button.info.get("enabled"))

    def attempt_wlan_roam_threshold_custom_value(self, value: str) -> str:
        """Attempt to enter a custom threshold and return the device-displayed text."""
        self.open_wlan_roam_threshold_custom_dialog()
        field = self._custom_input_field("WLAN 漫游阈值")

        field.click()
        field.clear_text()
        self.device.send_keys(value)
        time.sleep(0.2)
        return field.get_text()

    @classmethod
    def wlan_roam_threshold_custom_dialog_matches(
        cls, prompt: str, input_hint: str
    ) -> bool:
        """Compare custom-dialog text while tolerating vendor-inserted whitespace."""
        return cls._labels_match(
            prompt, cls.WLAN_ROAM_THRESHOLD_CUSTOM_PROMPT
        ) and cls._labels_match(
            input_hint, cls.WLAN_ROAM_THRESHOLD_CUSTOM_INPUT_HINT
        )

    @staticmethod
    def wlan_roam_threshold_matches(actual: str, expected: str) -> bool:
        """Compare roaming threshold text while tolerating inserted whitespace."""
        return WiFiAdvancedSettingsUI._labels_match(actual, expected)

    @staticmethod
    def wlan_roam_threshold_custom_input_matches(actual: str, expected: str) -> bool:
        """Compare custom-input text while tolerating vendor-inserted whitespace."""
        return WiFiAdvancedSettingsUI._labels_match(actual, expected)

    def wlan_roam_sensitivity_summary(self) -> str:
        """Return the summary displayed on the WLAN roaming sensitivity row."""
        self._roam_sensitivity_row()
        summary = self._summary_from_hierarchy(
            self.device.dump_hierarchy(), self.WLAN_ROAM_SENSITIVITY_LABELS
        )
        if summary is None:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_ROAM_SENSITIVITY_LABEL!r} 栏的显示值"
            )
        return summary or ""

    def open_wlan_roam_sensitivity_selector(self) -> None:
        """Open the WLAN roaming sensitivity dialog and wait for its selection."""
        row = self._roam_sensitivity_row()
        if row is None:
            return
        row.click()
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            if self._selected_option_from_hierarchy(self.device.dump_hierarchy()):
                return
            time.sleep(0.2)
        self.settings.fail_with_artifacts(
            f"{self.WLAN_ROAM_SENSITIVITY_LABEL!r} 弹窗未显示已选中的单选项"
        )

    def selected_wlan_roam_sensitivity(self) -> str:
        """Return the selected value in the open WLAN roaming sensitivity dialog."""
        selected = self._selected_option_from_hierarchy(self.device.dump_hierarchy())
        if selected is None:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_ROAM_SENSITIVITY_LABEL!r} 弹窗的已选中项"
            )
        return selected or ""

    def wlan_roam_sensitivity_options(self) -> tuple[str, ...]:
        """Return WLAN roaming sensitivity dialog options in displayed order."""
        options = self._dialog_options_from_hierarchy(self.device.dump_hierarchy())
        if not options:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_ROAM_SENSITIVITY_LABEL!r} 弹窗的可选项"
            )
        return options

    def select_wlan_roam_sensitivity(self, sensitivity: str) -> None:
        """Select a WLAN roaming sensitivity option in the open dialog."""
        option = self._find_entry((sensitivity,))
        if option is None or not option.click_exists(timeout=2):
            self.settings.fail_with_artifacts(
                f"未找到 WLAN 漫游灵敏度选项 {sensitivity!r}"
            )

    def confirm_wlan_roam_sensitivity_selection(self) -> None:
        """Confirm the sensitivity dialog and wait for its preference row."""
        button = self.device(resourceId="android:id/button1")
        if not button.click_exists(timeout=1):
            button = self._find_entry(("确认", "确定", "保存", "OK"))
            if button is None or not button.click_exists(timeout=2):
                self.settings.fail_with_artifacts("未找到 WLAN 漫游灵敏度弹窗确认按钮")
        self._roam_sensitivity_row()

    def current_wlan_roam_sensitivity_custom_dialog(
        self,
    ) -> Optional[tuple[str, str]]:
        """Return custom-dialog text when that dialog is already visible."""
        return self._custom_roam_sensitivity_dialog_texts_from_hierarchy(
            self.device.dump_hierarchy()
        )

    def open_wlan_roam_sensitivity_custom_dialog(self) -> tuple[str, str]:
        """Open the custom sensitivity dialog and return its prompt and input hint."""
        dialog_texts = self.current_wlan_roam_sensitivity_custom_dialog()
        if dialog_texts is not None:
            return dialog_texts

        if not self._wlan_roam_sensitivity_selector_is_open():
            if self._single_choice_dialog_is_open():
                self.settings.press_back()
            self.open()
            self.open_wlan_roam_sensitivity_selector()

        self.select_wlan_roam_sensitivity(self.WLAN_ROAM_SENSITIVITY_CUSTOM_OPTION)
        self._confirm_custom_dialog_opening("WLAN 漫游灵敏度")

        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            dialog_texts = self.current_wlan_roam_sensitivity_custom_dialog()
            if dialog_texts is not None:
                return dialog_texts
            time.sleep(0.2)
        self.settings.fail_with_artifacts("未读取到 WLAN 漫游灵敏度自定义弹窗内容")
        return "", ""

    def set_wlan_roam_sensitivity_custom_value(self, value: str) -> str:
        """Save a custom roaming sensitivity and return the displayed summary."""
        self.open_wlan_roam_sensitivity_custom_dialog()
        self._enter_custom_value("WLAN 漫游灵敏度", value)
        self._save_custom_value("WLAN 漫游灵敏度")
        return self.wlan_roam_sensitivity_summary()

    def enter_wlan_roam_sensitivity_custom_value(self, value: str) -> tuple[str, bool]:
        """Enter a custom sensitivity and return its displayed text and save state."""
        self.open_wlan_roam_sensitivity_custom_dialog()
        entered_value = self._enter_custom_value("WLAN 漫游灵敏度", value)
        button = self._custom_save_button("WLAN 漫游灵敏度")
        return entered_value, bool(button.info.get("enabled"))

    def attempt_wlan_roam_sensitivity_custom_value(self, value: str) -> str:
        """Attempt to enter a custom sensitivity and return device-displayed text."""
        self.open_wlan_roam_sensitivity_custom_dialog()
        field = self._custom_input_field("WLAN 漫游灵敏度")
        field.click()
        field.clear_text()
        self.device.send_keys(value)
        time.sleep(0.2)
        return field.get_text()

    @classmethod
    def wlan_roam_sensitivity_custom_dialog_matches(
        cls, prompt: str, input_hint: str
    ) -> bool:
        """Compare custom-dialog text across vendor range-separator variants."""
        return cls._range_labels_match(
            prompt, cls.WLAN_ROAM_SENSITIVITY_CUSTOM_PROMPT
        ) and cls._labels_match(
            input_hint, cls.WLAN_ROAM_SENSITIVITY_CUSTOM_INPUT_HINT
        )

    @staticmethod
    def wlan_roam_sensitivity_matches(actual: str, expected: str) -> bool:
        """Compare roaming sensitivity text while tolerating inserted whitespace."""
        return WiFiAdvancedSettingsUI._labels_match(actual, expected)

    @staticmethod
    def wlan_roam_sensitivity_custom_input_matches(actual: str, expected: str) -> bool:
        """Compare custom-input text while tolerating inserted whitespace."""
        return WiFiAdvancedSettingsUI._labels_match(actual, expected)

    def wlan_timeout_disconnect_summary(self) -> str:
        """Return the summary displayed on the WLAN timeout-disconnect row."""
        self._timeout_disconnect_row()
        summary = self._summary_from_hierarchy(
            self.device.dump_hierarchy(), self.WLAN_TIMEOUT_DISCONNECT_LABELS
        )
        if summary is None:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_TIMEOUT_DISCONNECT_LABEL!r} 栏的显示值"
            )
        return summary or ""

    def open_wlan_timeout_disconnect_selector(self) -> None:
        """Open the WLAN timeout-disconnect dialog and wait for its selection."""
        row = self._timeout_disconnect_row()
        if row is None:
            return
        row.click()
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            if self._selected_option_from_hierarchy(self.device.dump_hierarchy()):
                return
            time.sleep(0.2)
        self.settings.fail_with_artifacts(
            f"{self.WLAN_TIMEOUT_DISCONNECT_LABEL!r} 弹窗未显示已选中的单选项"
        )

    def selected_wlan_timeout_disconnect(self) -> str:
        """Return the selected value in the open timeout-disconnect dialog."""
        selected = self._selected_option_from_hierarchy(self.device.dump_hierarchy())
        if selected is None:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_TIMEOUT_DISCONNECT_LABEL!r} 弹窗的已选中项"
            )
        return selected or ""

    def wlan_timeout_disconnect_options(self) -> tuple[str, ...]:
        """Return timeout-disconnect dialog options in displayed order."""
        options = self._dialog_options_from_hierarchy(self.device.dump_hierarchy())
        if not options:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_TIMEOUT_DISCONNECT_LABEL!r} 弹窗的可选项"
            )
        return options

    def select_wlan_timeout_disconnect(self, timeout: str) -> None:
        """Select a timeout-disconnect option in the open dialog."""
        option = self._find_entry((timeout,))
        if option is None or not option.click_exists(timeout=2):
            self.settings.fail_with_artifacts(
                f"未找到 WLAN 超时断连设置选项 {timeout!r}"
            )

    def confirm_wlan_timeout_disconnect_selection(self) -> None:
        """Confirm the timeout-disconnect dialog and wait for its preference row."""
        button = self.device(resourceId="android:id/button1")
        if not button.click_exists(timeout=1):
            button = self._find_entry(("确认", "确定", "保存", "OK"))
            if button is None or not button.click_exists(timeout=2):
                self.settings.fail_with_artifacts(
                    "未找到 WLAN 超时断连设置弹窗确认按钮"
                )
        self._timeout_disconnect_row()

    def current_wlan_timeout_disconnect_custom_dialog(
        self,
    ) -> Optional[tuple[str, str]]:
        """Return custom-dialog text when that dialog is already visible."""
        return self._custom_timeout_disconnect_dialog_texts_from_hierarchy(
            self.device.dump_hierarchy()
        )

    def open_wlan_timeout_disconnect_custom_dialog(self) -> tuple[str, str]:
        """Open the custom timeout dialog and return its prompt and input hint."""
        dialog_texts = self.current_wlan_timeout_disconnect_custom_dialog()
        if dialog_texts is not None:
            return dialog_texts

        if not self._wlan_timeout_disconnect_selector_is_open():
            if self._single_choice_dialog_is_open():
                self.settings.press_back()
            self.open()
            self.open_wlan_timeout_disconnect_selector()

        self.select_wlan_timeout_disconnect(
            self.WLAN_TIMEOUT_DISCONNECT_CUSTOM_OPTION
        )
        self._confirm_custom_dialog_opening("WLAN 超时断连设置")

        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            dialog_texts = self.current_wlan_timeout_disconnect_custom_dialog()
            if dialog_texts is not None:
                return dialog_texts
            time.sleep(0.2)
        self.settings.fail_with_artifacts("未读取到 WLAN 超时断连设置自定义弹窗内容")
        return "", ""

    def set_wlan_timeout_disconnect_custom_value(self, value: str) -> str:
        """Save a custom timeout and return the displayed summary."""
        self.open_wlan_timeout_disconnect_custom_dialog()
        self._enter_custom_value("WLAN 超时断连设置", value)
        self._save_custom_value("WLAN 超时断连设置")
        return self.wlan_timeout_disconnect_summary()

    def enter_wlan_timeout_disconnect_custom_value(
        self, value: str
    ) -> tuple[str, bool]:
        """Enter a custom timeout and return its displayed text and save state."""
        self.open_wlan_timeout_disconnect_custom_dialog()
        entered_value = self._enter_custom_value("WLAN 超时断连设置", value)
        button = self._custom_save_button("WLAN 超时断连设置")
        return entered_value, bool(button.info.get("enabled"))

    def attempt_wlan_timeout_disconnect_custom_value(self, value: str) -> str:
        """Attempt to enter a custom timeout and return device-displayed text."""
        self.open_wlan_timeout_disconnect_custom_dialog()
        field = self._custom_input_field("WLAN 超时断连设置")
        field.click()
        field.clear_text()
        self.device.send_keys(value)
        time.sleep(0.2)
        return field.get_text()

    @classmethod
    def wlan_timeout_disconnect_custom_dialog_matches(
        cls, prompt: str, input_hint: str
    ) -> bool:
        """Compare custom-dialog text across vendor range-separator variants."""
        return cls._range_labels_match(
            prompt, cls.WLAN_TIMEOUT_DISCONNECT_CUSTOM_PROMPT
        ) and cls._labels_match(
            input_hint, cls.WLAN_TIMEOUT_DISCONNECT_CUSTOM_INPUT_HINT
        )

    @staticmethod
    def wlan_timeout_disconnect_matches(actual: str, expected: str) -> bool:
        """Compare timeout-disconnect text while tolerating inserted whitespace."""
        return WiFiAdvancedSettingsUI._labels_match(actual, expected)

    @staticmethod
    def wlan_timeout_disconnect_custom_input_matches(
        actual: str, expected: str
    ) -> bool:
        """Compare custom-input text while tolerating inserted whitespace."""
        return WiFiAdvancedSettingsUI._labels_match(actual, expected)

    def wlan_energy_save_summary(self) -> str:
        """Return the summary displayed on the WLAN energy-save row."""
        self._energy_save_row()
        summary = self._summary_from_hierarchy(
            self.device.dump_hierarchy(), self.WLAN_ENERGY_SAVE_LABELS
        )
        if summary is None:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_ENERGY_SAVE_LABEL!r} 栏的显示值"
            )
        return summary or ""

    def open_wlan_energy_save_selector(self) -> None:
        """Open the WLAN energy-save dialog and wait for its selection."""
        row = self._energy_save_row()
        if row is None:
            return
        row.click()
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            if self._selected_option_from_hierarchy(self.device.dump_hierarchy()):
                return
            time.sleep(0.2)
        self.settings.fail_with_artifacts(
            f"{self.WLAN_ENERGY_SAVE_LABEL!r} 弹窗未显示已选中的单选项"
        )

    def selected_wlan_energy_save(self) -> str:
        """Return the selected value in the open energy-save dialog."""
        selected = self._selected_option_from_hierarchy(self.device.dump_hierarchy())
        if selected is None:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_ENERGY_SAVE_LABEL!r} 弹窗的已选中项"
            )
        return selected or ""

    def select_wlan_energy_save(self, mode: str) -> None:
        """Select an energy-save mode in the open dialog."""
        option = self._find_entry((mode,))
        if option is None or not option.click_exists(timeout=2):
            self.settings.fail_with_artifacts(
                f"未找到 WLAN 省电模式设置选项 {mode!r}"
            )

    def confirm_wlan_energy_save_selection(self) -> None:
        """Confirm the energy-save dialog and wait until its preference row returns."""
        button = self.device(resourceId="android:id/button1")
        if not button.click_exists(timeout=1):
            button = self._find_entry(("确认", "确定", "保存", "OK"))
            if button is None or not button.click_exists(timeout=2):
                self.settings.fail_with_artifacts(
                    "未找到 WLAN 省电模式设置弹窗确认按钮"
                )
        self._energy_save_row()

    @staticmethod
    def wlan_energy_save_matches(actual: str, expected: str) -> bool:
        """Compare energy-save mode text while tolerating inserted whitespace."""
        return WiFiAdvancedSettingsUI._labels_match(actual, expected)

    def wlan_priority_summary(self) -> str:
        """Return the summary displayed on the WLAN priority preference row."""
        self._priority_row()
        summary = self._summary_from_hierarchy(
            self.device.dump_hierarchy(), self.WLAN_PRIORITY_LABELS
        )
        if summary is None:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_PRIORITY_LABEL!r} 栏的显示值"
            )
        return summary or ""

    def open_wlan_priority_selector(self) -> None:
        """Open the WLAN priority single-choice dialog."""
        row = self._priority_row()
        if row is None:
            return
        row.click()
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            if self._selected_option_from_hierarchy(self.device.dump_hierarchy()):
                return
            time.sleep(0.2)
        self.settings.fail_with_artifacts(
            f"{self.WLAN_PRIORITY_LABEL!r} 弹窗未显示已选中的单选项"
        )

    def selected_wlan_priority(self) -> str:
        """Return the selected value in the open WLAN priority dialog."""
        selected = self._selected_option_from_hierarchy(self.device.dump_hierarchy())
        if selected is None:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_PRIORITY_LABEL!r} 弹窗的已选中项"
            )
        return selected or ""

    def wlan_priority_options(self) -> tuple[str, ...]:
        """Return WLAN priority dialog options in their displayed order."""
        options = self._dialog_options_from_hierarchy(self.device.dump_hierarchy())
        if not options:
            self.settings.fail_with_artifacts(
                f"未读取到 {self.WLAN_PRIORITY_LABEL!r} 弹窗的可选项"
            )
        return options

    def select_wlan_priority(self, priority: str) -> None:
        """Select a WLAN priority option in the open dialog."""
        option = self._find_entry((priority,))
        if option is None or not option.click_exists(timeout=2):
            self.settings.fail_with_artifacts(
                f"未找到 WLAN 优先等级选项 {priority!r}"
            )

    def confirm_wlan_priority_selection(self) -> None:
        """Confirm the priority dialog and wait until its preference row returns."""
        button = self.device(resourceId="android:id/button1")
        if not button.click_exists(timeout=1):
            button = self._find_entry(("确认", "确定", "保存", "OK"))
            if button is None or not button.click_exists(timeout=2):
                self.settings.fail_with_artifacts("未找到 WLAN 优先等级弹窗确认按钮")
        self._priority_row()

    @staticmethod
    def wlan_priority_matches(actual: str, expected: str) -> bool:
        """Compare priority text while tolerating vendor-inserted whitespace."""
        return WiFiAdvancedSettingsUI._labels_match(actual, expected)

    def _mode_row(self):
        deadline = time.monotonic() + 10.0
        while time.monotonic() < deadline:
            row = self._find_entry(self.WLAN_MODE_LABELS)
            if row is not None:
                return row
            time.sleep(0.2)
        self.settings.fail_with_artifacts(f"未找到 {self.WLAN_MODE_LABEL!r} 栏")
        return None

    def _band_row(self):
        deadline = time.monotonic() + 10.0
        while time.monotonic() < deadline:
            row = self._find_entry(self.WLAN_BAND_LABELS)
            if row is not None:
                return row
            time.sleep(0.2)
        self.settings.fail_with_artifacts(f"未找到 {self.WLAN_BAND_LABEL!r} 栏")
        return None

    def _roam_threshold_row(self):
        deadline = time.monotonic() + 10.0
        while time.monotonic() < deadline:
            row = self._find_entry(self.WLAN_ROAM_THRESHOLD_LABELS)
            if row is not None:
                return row
            time.sleep(0.2)
        self.settings.fail_with_artifacts(
            f"未找到 {self.WLAN_ROAM_THRESHOLD_LABEL!r} 栏"
        )
        return None

    def _roam_sensitivity_row(self):
        deadline = time.monotonic() + 10.0
        while time.monotonic() < deadline:
            row = self._find_entry(self.WLAN_ROAM_SENSITIVITY_LABELS)
            if row is not None:
                return row
            time.sleep(0.2)
        self.settings.fail_with_artifacts(
            f"未找到 {self.WLAN_ROAM_SENSITIVITY_LABEL!r} 栏"
        )
        return None

    def _timeout_disconnect_row(self):
        deadline = time.monotonic() + 10.0
        while time.monotonic() < deadline:
            row = self._find_entry(self.WLAN_TIMEOUT_DISCONNECT_LABELS)
            if row is not None:
                return row
            time.sleep(0.2)
        self.settings.fail_with_artifacts(
            f"未找到 {self.WLAN_TIMEOUT_DISCONNECT_LABEL!r} 栏"
        )
        return None

    def _energy_save_row(self):
        deadline = time.monotonic() + 10.0
        while time.monotonic() < deadline:
            row = self._find_entry(self.WLAN_ENERGY_SAVE_LABELS)
            if row is not None:
                return row
            time.sleep(0.2)
        self.settings.fail_with_artifacts(
            f"未找到 {self.WLAN_ENERGY_SAVE_LABEL!r} 栏"
        )
        return None

    def _priority_row(self):
        deadline = time.monotonic() + 10.0
        while time.monotonic() < deadline:
            row = self._find_entry(self.WLAN_PRIORITY_LABELS)
            if row is not None:
                return row
            time.sleep(0.2)
        self.settings.fail_with_artifacts(f"未找到 {self.WLAN_PRIORITY_LABEL!r} 栏")
        return None

    def _advanced_setting_row(self):
        return (
            self._find_entry(self.WLAN_BAND_LABELS)
            or self._find_entry(self.WLAN_MODE_LABELS)
            or self._find_entry(self.WLAN_ROAM_THRESHOLD_LABELS)
            or self._find_entry(self.WLAN_ROAM_SENSITIVITY_LABELS)
            or self._find_entry(self.WLAN_TIMEOUT_DISCONNECT_LABELS)
            or self._find_entry(self.WLAN_ENERGY_SAVE_LABELS)
            or self._find_entry(self.WLAN_PRIORITY_LABELS)
        )

    def _wlan_roam_threshold_selector_is_open(self) -> bool:
        options = self._dialog_options_from_hierarchy(self.device.dump_hierarchy())
        return any(
            self._labels_match(option, self.WLAN_ROAM_THRESHOLD_CUSTOM_OPTION)
            for option in options
        )

    def _wlan_roam_sensitivity_selector_is_open(self) -> bool:
        options = self._dialog_options_from_hierarchy(self.device.dump_hierarchy())
        return any(
            self._labels_match(option, self.WLAN_ROAM_SENSITIVITY_CUSTOM_OPTION)
            for option in options
        )

    def _wlan_timeout_disconnect_selector_is_open(self) -> bool:
        options = self._dialog_options_from_hierarchy(self.device.dump_hierarchy())
        return any(
            self._labels_match(
                option, self.WLAN_TIMEOUT_DISCONNECT_CUSTOM_OPTION
            )
            for option in options
        )

    def _single_choice_dialog_is_open(self) -> bool:
        return self._selected_option_from_hierarchy(self.device.dump_hierarchy()) is not None

    def _advanced_setting_row_required(self):
        deadline = time.monotonic() + 10.0
        while time.monotonic() < deadline:
            row = self._advanced_setting_row()
            if row is not None:
                return row
            time.sleep(0.2)
        self.settings.fail_with_artifacts("未找到 WLAN 高级设置项")
        return None

    def _click_entry(
        self, labels: Iterable[str], scroll_to_end_before_search: bool = False
    ) -> None:
        if scroll_to_end_before_search:
            scrollable = self.device(scrollable=True)
            if scrollable.exists:
                scrollable.scroll.toEnd()
        for label in labels:
            entry = self._find_entry((label,))
            if entry is not None and self._click_entry_row_from_hierarchy(
                (label,)
            ):
                return
            scrollable = self.device(scrollable=True)
            if scrollable.exists and scrollable.scroll.to(text=label):
                entry = self._find_entry((label,))
                if entry is not None and self._click_entry_row_from_hierarchy(
                    (label,)
                ):
                    return
        self.settings.fail_with_artifacts(f"未找到设置入口 {tuple(labels)!r}")

    def _find_entry(self, labels: Iterable[str]):
        for label in labels:
            entry = self.device(text=label)
            if entry.exists:
                return entry
            entry = self.device(textMatches=self._label_pattern(label))
            if entry.exists:
                return entry
        return None

    def _click_entry_row_from_hierarchy(self, labels: Iterable[str]) -> bool:
        """Click a visible preference row only after its coordinates settle."""
        labels = tuple(labels)
        deadline = time.monotonic() + 5.0
        previous_bounds = None
        while time.monotonic() < deadline:
            bounds = self._entry_row_bounds_from_hierarchy(
                self.device.dump_hierarchy(), labels
            )
            if bounds is None and previous_bounds is None:
                return False
            if bounds is not None and bounds == previous_bounds:
                left, top, right, bottom = bounds
                self.device.click((left + right) // 2, (top + bottom) // 2)
                return True
            previous_bounds = bounds
            time.sleep(0.3)
        self.settings.fail_with_artifacts(f"设置入口 {labels!r} 位置未稳定，取消点击")
        return False

    @staticmethod
    def _entry_row_bounds_from_hierarchy(
        hierarchy: str, labels: Iterable[str]
    ) -> Optional[tuple[int, int, int, int]]:
        root = ET.fromstring(hierarchy)
        parents = {child: parent for parent in root.iter() for child in parent}
        for node in root.iter("node"):
            if not any(
                WiFiAdvancedSettingsUI._labels_match(node.attrib.get("text", ""), label)
                for label in labels
            ):
                continue
            current = node
            while current is not None:
                if current.attrib.get("enabled") == "false":
                    break
                if current.attrib.get("clickable") == "true":
                    match = re.fullmatch(
                        r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]",
                        current.attrib.get("bounds", ""),
                    )
                    if match is None:
                        break
                    left, top, right, bottom = map(int, match.groups())
                    if left >= right or top >= bottom:
                        break
                    center_x = (left + right) // 2
                    center_y = (top + bottom) // 2
                    ancestor = parents.get(current)
                    visible = True
                    while ancestor is not None:
                        ancestor_match = re.fullmatch(
                            r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]",
                            ancestor.attrib.get("bounds", ""),
                        )
                        if ancestor.attrib.get("enabled") == "false":
                            visible = False
                            break
                        if ancestor_match is not None:
                            outer_left, outer_top, outer_right, outer_bottom = map(
                                int, ancestor_match.groups()
                            )
                            if not (
                                outer_left <= center_x < outer_right
                                and outer_top <= center_y < outer_bottom
                            ):
                                visible = False
                                break
                        ancestor = parents.get(ancestor)
                    if visible:
                        return left, top, right, bottom
                    break
                current = parents.get(current)
        return None

    @staticmethod
    def _label_pattern(label: str) -> str:
        compact_label = "".join(label.split())
        return r"^\s*" + r"\s*".join(
            re.escape(character) for character in compact_label
        ) + r"\s*$"

    @staticmethod
    def _summary_from_hierarchy(
        hierarchy: str, labels: Iterable[str]
    ) -> Optional[str]:
        root = ET.fromstring(hierarchy)
        parents = {child: parent for parent in root.iter() for child in parent}
        for title in root.iter("node"):
            if not any(
                WiFiAdvancedSettingsUI._labels_match(
                    title.attrib.get("text", ""), label
                )
                for label in labels
            ):
                continue
            current = parents.get(title)
            while current is not None:
                summaries = [
                    node.attrib.get("text", "").strip()
                    for node in current.iter("node")
                    if node is not title
                    and node.attrib.get("text", "").strip()
                    and "summary" in node.attrib.get("resource-id", "").lower()
                ]
                if summaries:
                    return summaries[0]
                current = parents.get(current)
        return None

    @staticmethod
    def _selected_mode_from_hierarchy(hierarchy: str) -> Optional[str]:
        return WiFiAdvancedSettingsUI._selected_option_from_hierarchy(hierarchy)

    @staticmethod
    def _selected_option_from_hierarchy(hierarchy: str) -> Optional[str]:
        root = ET.fromstring(hierarchy)
        parents = {child: parent for parent in root.iter() for child in parent}
        for node in root.iter("node"):
            attributes = node.attrib
            selected = attributes.get("checked") == "true" or attributes.get(
                "selected"
            ) == "true"
            class_name = attributes.get("class", "")
            checkable = attributes.get("checkable") == "true" or any(
                name in class_name for name in ("CheckedTextView", "RadioButton")
            )
            if not (selected and checkable):
                continue
            text = attributes.get("text", "").strip()
            if text:
                return text
            for child in node.iter("node"):
                text = child.attrib.get("text", "").strip()
                if text:
                    return text
            parent = parents.get(node)
            if parent is not None:
                for sibling in parent.iter("node"):
                    text = sibling.attrib.get("text", "").strip()
                    if text:
                        return text
        return None

    @staticmethod
    def _dialog_options_from_hierarchy(hierarchy: str) -> tuple[str, ...]:
        root = ET.fromstring(hierarchy)
        parents = {child: parent for parent in root.iter() for child in parent}
        options: list[str] = []
        for node in root.iter("node"):
            attributes = node.attrib
            class_name = attributes.get("class", "")
            is_option = attributes.get("checkable") == "true" or any(
                name in class_name for name in ("CheckedTextView", "RadioButton")
            )
            if not is_option:
                continue

            text = attributes.get("text", "").strip()
            if not text:
                for child in node.iter("node"):
                    text = child.attrib.get("text", "").strip()
                    if text:
                        break
            if not text:
                parent = parents.get(node)
                if parent is not None:
                    for sibling in parent:
                        for child in sibling.iter("node"):
                            text = child.attrib.get("text", "").strip()
                            if text:
                                break
                        if text:
                            break
            if text and not any(
                WiFiAdvancedSettingsUI._labels_match(text, option)
                for option in options
            ):
                options.append(text)
        return tuple(options)

    @staticmethod
    def _custom_roam_threshold_dialog_texts_from_hierarchy(
        hierarchy: str,
    ) -> Optional[tuple[str, str]]:
        root = ET.fromstring(hierarchy)
        prompt = None
        input_hint = None
        for node in root.iter("node"):
            attributes = node.attrib
            text = attributes.get("text", "").strip()
            resource_id = attributes.get("resource-id", "").lower()
            if text and (
                "title" in resource_id
                or "漫游阈值" in text
                or "dBm" in text
            ):
                prompt = text

            if "EditText" not in attributes.get("class", ""):
                continue
            for attribute in (
                "text",
                "hint",
                "hint-text",
                "content-desc",
                "description",
            ):
                value = attributes.get(attribute, "").strip()
                if value:
                    input_hint = value
                    break
            if input_hint is None:
                input_hint = ""

        if prompt is None or input_hint is None:
            return None
        return prompt, input_hint

    @staticmethod
    def _custom_roam_sensitivity_dialog_texts_from_hierarchy(
        hierarchy: str,
    ) -> Optional[tuple[str, str]]:
        root = ET.fromstring(hierarchy)
        prompt = None
        input_hint = None
        for node in root.iter("node"):
            attributes = node.attrib
            text = attributes.get("text", "").strip()
            resource_id = attributes.get("resource-id", "").lower()
            if text and (
                "title" in resource_id
                or "漫游灵敏度" in text
                or "dB" in text
            ):
                prompt = text

            if "EditText" not in attributes.get("class", ""):
                continue
            for attribute in (
                "text",
                "hint",
                "hint-text",
                "content-desc",
                "description",
            ):
                value = attributes.get(attribute, "").strip()
                if value:
                    input_hint = value
                    break
            if input_hint is None:
                input_hint = ""

        if prompt is None or input_hint is None:
            return None
        return prompt, input_hint

    @staticmethod
    def _custom_timeout_disconnect_dialog_texts_from_hierarchy(
        hierarchy: str,
    ) -> Optional[tuple[str, str]]:
        root = ET.fromstring(hierarchy)
        prompt = None
        input_hint = None
        for node in root.iter("node"):
            attributes = node.attrib
            text = attributes.get("text", "").strip()
            resource_id = attributes.get("resource-id", "").lower()
            if text and (
                "title" in resource_id
                or "超时断连" in text
                or "断连时间" in text
            ):
                prompt = text

            if "EditText" not in attributes.get("class", ""):
                continue
            for attribute in (
                "text",
                "hint",
                "hint-text",
                "content-desc",
                "description",
            ):
                value = attributes.get(attribute, "").strip()
                if value:
                    input_hint = value
                    break
            if input_hint is None:
                input_hint = ""

        if prompt is None or input_hint is None:
            return None
        return prompt, input_hint

    def _confirm_custom_dialog_opening(self, setting_name: str) -> None:
        button = self.device(resourceId="android:id/button1")
        if not button.click_exists(timeout=1):
            button = self._find_entry(("确认", "确定", "保存", "OK"))
            if button is None or not button.click_exists(timeout=2):
                self.settings.fail_with_artifacts(
                    f"未找到 {setting_name} 弹窗确认按钮"
                )

    def _custom_input_field(self, setting_name: str):
        field = self.device(className="android.widget.EditText")
        if field.count != 1 or not field.exists:
            self.settings.fail_with_artifacts(f"未找到 {setting_name} 自定义输入框")
        return field

    def _enter_custom_value(self, setting_name: str, value: str) -> str:
        field = self._custom_input_field(setting_name)
        field.click()
        field.clear_text()
        if value == "":
            return ""
        field.set_text(value)
        entered_value = field.get_text()
        if not self._labels_match(entered_value, value):
            self.settings.fail_with_artifacts(
                f"{setting_name}自定义输入值错误：期望 {value!r}，实际 {entered_value!r}"
            )
        return entered_value

    def _custom_save_button(self, setting_name: str):
        button = self.device(resourceId="android:id/button1")
        if not button.exists:
            button = self._find_entry(("确认", "确定", "保存", "OK"))
            if button is None or not button.exists:
                self.settings.fail_with_artifacts(
                    f"未找到 {setting_name} 自定义弹窗保存按钮"
                )
        assert button is not None
        return button

    def _save_custom_value(self, setting_name: str) -> None:
        button = self._custom_save_button(setting_name)
        if not button.click_exists(timeout=2):
            self.settings.fail_with_artifacts(
                f"未能保存 {setting_name} 自定义值"
            )

    @staticmethod
    def _labels_match(actual: str, expected: str) -> bool:
        return "".join(actual.split()) == "".join(expected.split())

    @staticmethod
    def _range_labels_match(actual: str, expected: str) -> bool:
        normalized_actual = "".join(actual.split()).replace("~", "-").replace("\uff5e", "-")
        normalized_expected = "".join(expected.split()).replace("~", "-").replace("\uff5e", "-")
        return normalized_actual == normalized_expected