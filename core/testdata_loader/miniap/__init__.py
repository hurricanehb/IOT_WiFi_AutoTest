"""miniAP 域测试数据：halow 频点表、信道 plan 展开工具。"""
from core.testdata_loader.miniap import channel_plans_data as _channel_plans
from core.testdata_loader.miniap import halow_frequency_data as _halow_frequency

count_channel_steps = _channel_plans.count_channel_steps
expand_channels = _channel_plans.expand_channels
iter_channel_steps = _channel_plans.iter_channel_steps

channels_from_frequency_map = _halow_frequency.channels_from_frequency_map
country_code = _halow_frequency.country_code
eu_channels = _halow_frequency.eu_channels
halow_frequency_yaml = _halow_frequency.halow_frequency_yaml
load_halow_frequency_tables = _halow_frequency.load_halow_frequency_tables
special_id = _halow_frequency.special_id
us_channels = _halow_frequency.us_channels

__all__ = [
    "channels_from_frequency_map",
    "count_channel_steps",
    "country_code",
    "eu_channels",
    "expand_channels",
    "halow_frequency_yaml",
    "iter_channel_steps",
    "load_halow_frequency_tables",
    "special_id",
    "us_channels",
]
