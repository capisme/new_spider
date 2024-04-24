import hashlib
import re
import html
import time
import datetime


def get_proxy():
    pass


def fmt_pubtime(data):
    """
    把data转换为日期时间，时区为东八区北京时间，能够识别：今天、昨天、5分钟前等等，如果不能成功识别，则返回datetime.datetime.now()
    """
    try:
        timestamp = int(data)
        timeStamp = int(str(data)[:10])
        timeArray = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timeStamp))
        return str(timeArray)
    except Exception:
        pass
    dt = datetime.datetime.now()
    # html实体字符转义
    data = html.unescape(str(data))
    data = data.strip()
    if not data:
        return
    # 归一化
    data = data.replace("年", "-").replace("月", "-").replace("日", " ").replace("/", "-").replace(",", " ").replace("两",
                                                                                                                  "2").replace(
        '.', '-').strip()
    data = re.sub("\s+", " ", data)
    year = dt.year
    regex_format_list = [
        # 针对北青网时间正则
        ("^(\d{4}-\d{1,2}-\d{1,2})(\d{1,2}:\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M:%S", "financial"),
        # 针对腾讯新闻的时间正则
        ("^(\d{1,4})(\d{1,2})-(\d{1,2})(\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M", "tx"),
        ("^(\d{1,4})\s+(\d{1,2})-\s+(\d{1,2})\s+(\d{1,2}:\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M:%S", "tx"),
        # 2013年8月15日 22:46:21
        ("(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M:%S", ""),
        ("(\d{4}\s-\s\d{1,2}\s-\s\d{1,2} \d{1,2}\s:\s\d{1,2}\s:\s\d{1,2})", "%Y-%m-%d %H:%M:%S", ""),
        # "2013年8月15日 22:46"
        ("(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M", ""),
        # "2013 年 8 月 15 日 22 : 46"
        ("(\d{4}- \d{1,2}- \d{1,2} \d{1,2}: \d{1,2}: \d{1,2})", "%Y- %m- %d %H: %M: %S", ""),
        ("(\d{4} - \d{1,2} - \d{1,2} \d{1,2} : \d{1,2})", "%Y - %m - %d %H : %M", ""),
        ("(\d{4}- \d{1,2}- \d{1,2} \d{1,2}: \d{1,2})", "%Y- %m- %d %H: %M", ""),
        # "2014年5月11日"
        ("(\d{4}-\d{1,2}-\d{1,2})", "%Y-%m-%d", ""),
        # "2014 年 5 月 11 日"
        ("(\d{4} - \d{1,2} - \d{1,2})", "%Y - %m - %d", ""),
        ("(\d{4}- \d{1,2}- \d{1,2})", "%Y- %m- %d", ""),
        # "8月15日 22:46:21",
        ("(\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M:%S", "+year"),
        # "8月15日 22:46",
        ("(\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M", "+year"),
        # "13年8月15日 22:46:21",
        ("(\d{2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", "%y-%m-%d %H:%M:%S", ""),
        # "13年8月15日 22:46",
        ("(\d{2}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})", "%y-%m-%d %H:%M", ""),
        # "13年8月15日"
        ("(\d{2}-\d{1,2}-\d{1,2})", "%y-%m-%d", ""),
        # "13年8月"
        ("(\d{4}-\d{1,2})", "%Y-%m", ""),
        # "8月15日
        ("(\d{1,2}-\d{1,2})", "%Y-%m-%d", "+year"),
        # "3 秒前",
        ("(\d+)\s*秒前", "", "-seconds"),
        # "3 分钟前",
        ("(\d+)\s*分钟前|半小时前", "", "-minutes"),
        # "3 小时前",
        ("(\d+)\s*小时前", "", "-hours"),
        # "3 天前",
        ("(\d+)\s*天前", "", "-days"),
        # "3 周前"
        ("(\d+)\s*周前", "", "-weeks"),
        # "3 月前"
        ("(\d+)\s*-前", "", "-months"),
        # 今天 15:42:21
        ("今天\s*(\d{1,2}:\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M:%S", "date-0"),
        # 昨天 15:42:21
        ("昨天\s*(\d{1,2}:\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M:%S", "date-1"),
        # 前天 15:42:21
        ("前天\s*(\d{1,2}:\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M:%S", "date-2"),
        # 今天 15:42
        ("今天\s*(\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M", "date-0"),
        # 昨天 15:42
        ("昨天\s*(\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M", "date-1"),
        # 前天 15:42
        ("前天\s*(\d{1,2}:\d{1,2})", "%Y-%m-%d %H:%M", "date-2"),
        (
            "(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})\s+(\d{1,4})",
            "%B %d %Y", "englishTime"),
        ("(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})\s+(\d{1,4})", "%b %d %Y", "acronymTime"),
        ('(\d{2}:\d{2})\s+(\d{1,2})-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(\d{4})', '%H:%M %d %b %Y',
         "acronymTimeHour"),
        ("昨天", "00:00:00", "now-1"),
        ("前天", "00:00:00", "now-2"),
        ("刚刚", "", "now-0"),
        ("现在", "", "now-0"),
        # ("(0?[1-9]-\d{2})", "%Y-%m-%d", "+year")
    ]
    dt2 = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                     '%Y-%m-%d %H:%M:%S')
    for regex, dt_format, flag in regex_format_list:
        m = re.search(f"{regex}", data, re.I)
        if m:
            if not flag:
                dt = datetime.datetime.strptime(m.group(1), dt_format)
            elif flag == "acronymTimeHour":
                dt = datetime.datetime.strptime(' '.join(m.groups()), dt_format)
            elif flag == "englishTime":
                dt = datetime.datetime.strptime(' '.join(m.groups()), dt_format)
            elif flag == "acronymTime":
                dt = datetime.datetime.strptime(' '.join(m.groups()), dt_format)
            elif flag == "financial":
                dt = datetime.datetime.strptime(m.group(1) + " " + m.group(2), dt_format)
            elif flag == "+year":
                # 需要增加年份
                dt = datetime.datetime.strptime("%s-%s" % (year, m.group(1)), dt_format)
                if dt2 < dt:
                    dt = datetime.datetime.strptime("%s-%s" % (year - 1, m.group(1)), dt_format)

            elif flag.startswith("now"):
                del_days = int(flag.split('-')[1])
                dt = str(dt - datetime.timedelta(days=int(del_days))).split('.')[0]
                if dt_format != '':
                    dt = f'{dt.split(" ")[0]} {dt_format}'
            elif flag in ("-seconds", "-minutes", "-hours", "-days", "-weeks", "-months"):
                # 减秒
                if "半小时前" in m.group(0):
                    MS = 30
                else:
                    MS = int(m.group(1))
                if flag == "-months":
                    MS = MS * 31
                    flag = "days"
                flag = flag.replace('-', '')
                loc = locals()
                exec(f"dt = dt - datetime.timedelta({flag}={MS})")
                dt = str(loc['dt']).split('.')[0]

            elif flag.startswith("date"):
                del_days = int(flag.split('-')[1])
                _date = dt.date() - datetime.timedelta(days=del_days)
                _date = _date.strftime("%Y-%m-%d")
                dt = datetime.datetime.strptime("%s %s" % (_date, m.group(1)), dt_format)
            elif flag.startswith("tx"):
                dt = datetime.datetime.strptime('-'.join(m.groups()[0:3]) + ' ' + str(m.group(4)), dt_format)
            dt = datetime.datetime.strptime(str(dt), '%Y-%m-%d %H:%M:%S')
            if dt2 < dt:
                return
            return str(dt)
    else:
        return


def get_md5(str_):
    md5 = hashlib.md5()
    md5.update(str_.encode("utf-8"))
    md5_str = md5.hexdigest()
    return md5_str

if __name__ == '__main__':
    fmt = fmt_pubtime('2021-04-12')
    print(fmt)