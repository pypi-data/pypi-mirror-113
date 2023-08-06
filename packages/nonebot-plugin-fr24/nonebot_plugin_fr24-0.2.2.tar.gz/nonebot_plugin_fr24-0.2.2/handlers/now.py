from typing import Any

from nonebot.adapters.cqhttp import Bot
from nonebot.typing import T_State

from ..matcher import fr24
from ..config import config

from ..libs.info import Info
from ..libs.request import FR24Request

async def now_handler(bot: Bot, state: T_State):
    cmd=state["cmd"]
    if cmd in config.CMDF_NOW:
        request_params = Info.params.copy()
        request = FR24Request(Info.real_time_flight_tracker_data_url, request_params, Info.headers.copy())
        try:
            response = await request.get_content()
        except Exception :
            await fr24.finish("端口访问错误或超时，请稍后再试",at_sender=True)
            return
        data = response.json()
        stat_msg = "追踪方式统计："
        for param, info in data.items():
            if param == "full_count":
                total = info
            if param == "stats":
                stats = info["total"]
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
        msg = '\n'.join((f"当前追踪航班数为:{total}",stat_msg))
        await fr24.finish(msg,at_sender=True)


