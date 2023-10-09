from datetime import datetime, timedelta
import time
import pytz

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
    def get_utc_time(time_str = None, days=0):
        if time_str is None:
            return datetime.utcnow(), datetime.now()
        else:
            dt = datetime.strptime(time_str, "%Y%m%d%H%M%S") + timedelta(days=days)
            return pytz.utc.localize(dt), dt


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
    
    @staticmethod
    def get_current_timestamp_format(current_utc_time):
        # 将UTC时间转换为中国的当地时间
        local_time = current_utc_time.astimezone(pytz.timezone('Asia/Shanghai'))
        return local_time.strftime("%Y%m%d%H%M%S")
    
    @staticmethod
    def get_local_timstamp():
        current_time = datetime.now()
        return current_time.strftime("%Y%m%d%H%M%S")

    @staticmethod
    def parse_time(time_info, target_time_str):
        try:
            # 从time_info字典中获取"time"键的值，格式为"HH:MM"
            time_str = time_info.get("time")
            
            if not time_str:
                raise ValueError("Invalid time format")

            # 解析目标时间字符串的年、月、日
            year = int(target_time_str[0:4])
            month = int(target_time_str[4:6])
            day = int(target_time_str[6:8])

            # 解析时间字符串，获取小时和分钟
            hour, minute = map(int, time_str.split(':'))

            # 创建datetime对象
            return datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=0)
        except (KeyError, ValueError):
            return None

    @staticmethod
    def is_within_configured_time(config, target_time_str):
        try:
            # 解析目标时间字符串
            target_time = datetime.strptime(target_time_str, "%Y%m%d%H%M%S")

            if "start_time" in config:
                start_time = TimeFormat.parse_time(config["start_time"], target_time_str)
                if start_time is None:
                    return False

                if "week_day" in config["start_time"]:
                    week_day = config["start_time"]["week_day"].lower()
                    _ = target_time.strftime('%a').lower()
                    if week_day != target_time.strftime("%a").lower():
                        return False

            if "end_time" in config:
                end_time = TimeFormat.parse_time(config["end_time"], target_time_str)
                if end_time is None:
                    return False

            if "start_time" in config and "end_time" in config:
                if start_time <= target_time <= end_time:
                    return True

            return False
        except (KeyError, ValueError):
            return False  # 配置信息无效或缺失时返回False
