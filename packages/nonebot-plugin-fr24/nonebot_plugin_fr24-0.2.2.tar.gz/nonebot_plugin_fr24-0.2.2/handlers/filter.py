from typing import Optional

from nonebot.adapters.cqhttp import Bot
from nonebot.typing import T_State

from ..matcher import fr24
from ..config import config

from ..libs.info import Info
from ..libs.request import FR24Request

async def filter_handler(bot: Bot, state: T_State):
    cmd=state["cmd"]
    request_params = Info.params.copy()
    print(request_params)
    try:
            param: Optional[str] = state['argv'][1]
    except IndexError:
            param = None
    if cmd in config.CMDF_FROM:
        if param is None:
            await fr24.finish('请在命令后输入出发机场IATA（例：PVG）')
            return
        request_params["from"] = param
    if cmd in config.CMDF_TO:
        if param is None:
            await fr24.finish('请在命令后输入到达机场IATA（例：PVG）')
            return
        request_params["to"] = param
    if cmd in config.CMDF_AIRPORT:
        if param is None:
            await fr24.finish('请在命令后输入机场IATA（例：PVG）')
            return
        request_params["airport"] = param
    if cmd in config.CMDF_TYPE:
        if param is None:
            await fr24.finish('请在命令后输入机型缩写（例：B738）')
            return
        request_params["type"] = param
    if cmd in config.CMDF_AIRLINE:
        if param is None:
            await fr24.finish('请在命令后输入航司IATA（例：CA）')
            return
        request_params["flight"] = param
    request = FR24Request(Info.real_time_flight_tracker_data_url, request_params, Info.headers.copy())
    try:
        response = await request.get_content()
    except Exception :
        await fr24.finish("端口访问错误或超时，请稍后再试",at_sender=True)
        return
    data = response.json()
    total = 0
    stat_msg = "追踪方式统计："
    for tag, info in data.items():
        if tag[0].isnumeric():
            total += 1
        if tag == "stats":
            stats = info["visible"]
            print(stats)
            if stats["ads-b"] != 0:
                ads_b = stats["ads-b"]
                stat_msg = stat_msg + f"ADS-B:{ads_b};"
            if stats["mlat"] != 0:
                mlat = stats["mlat"]
                stat_msg = stat_msg + f"MLAT:{mlat};"
            if stats["faa"] != 0:
                faa = stats["faa"]
                stat_msg = stat_msg + f"FAA:{faa};"
            if stats["flarm"] != 0:
                flarm = stats["flarm"]
                stat_msg = stat_msg + f"FLARM:{flarm};"
            if stats["estimated"] != 0:
                estimated = stats["estimated"]
                stat_msg = stat_msg + f"惯性预测:{estimated};"
            if stats["satellite"] != 0:
                satellite = stats["satellite"]
                stat_msg = stat_msg + f"卫星:{satellite};"    
            if stats["other"] != 0:
                other = stats["other"]
                stat_msg = stat_msg + f"其他:{other};"
    if total ==1500:
        msg = f"当前{cmd}:{param}的航班数量为:>={total}\n"
    else:
        msg = f"当前{cmd}:{param}的航班数量为:{total}\n"
    msg = msg+'\n'.join((stat_msg,Info.message_tip))
    
    await fr24.finish(msg,at_sender=True)