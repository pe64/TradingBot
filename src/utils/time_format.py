from datetime import datetime, timedelta
import time

class TimeFormat:
    def __init__(self) -> None:
        pass

    @staticmethod
    def transform_datatime_format(input_str):
        if len(input_str) == 19:  # 格式 "YYYY-MM-DD HH:MM:SS"
            dt_format = "%Y-%m-%d %H:%M:%S"
        else:  # 格式 "YYYY-MM-DD HH:MM"
            dt_format = "%Y-%m-%d %H:%M"
        dt = datetime.strptime(input_str, dt_format)
        return dt.strftime("%Y%m%d%H%M%S")
    
    @staticmethod
    def calculate_time_range(current_utc_time, interval):
        if interval == "8h":
            # 计算当前8小时时间段的起始时间
            start_time = current_utc_time.replace(minute=0, second=0, microsecond=0)
            if current_utc_time.hour < 8:
                start_time -= timedelta(hours=8)
        elif interval == "1d":
            # 计算当天的起始时间
            start_time = current_utc_time.replace(hour=0, minute=0, second=0, microsecond=0)
        elif interval == "1w":
            # 计算本周起始时间
            start_time = current_utc_time.replace(hour=0, minute=0, second=0, microsecond=0)
            weekday = current_utc_time.weekday()  # 0表示周一，6表示周日
            if weekday != 0:
                start_time -= timedelta(days=weekday)
        else:
            raise ValueError("Unsupported interval")

        start_time_stamp = int(start_time.timestamp()) * 1000
        return start_time_stamp
    
    @staticmethod
    def calculate_time_difference(time_str1, time_str2):
        try:
            # 解析时间字符串为datetime对象
            formatted_time1 = datetime.strptime(time_str1, "%Y%m%d%H%M%S")
            formatted_time2 = datetime.strptime(time_str2, "%Y%m%d%H%M%S")

            # 计算时间差值
            time_difference = formatted_time2 - formatted_time1

            # 返回时间差值作为timedelta对象
            return time_difference
        except ValueError:
            return None  # 如果解析失败，返回None表示无效输入
    
    @staticmethod
    def get_time_delta(period):
        if period == '8h':
            return timedelta(hours=7,minutes=59)
        elif period == '1d':
            return timedelta(hours=23, minutes=59)
        elif period == '1w':
            return timedelta(days=6, hours=23, minutes=59)
        else:
            return timedelta(minutes=1)