from typing import Any

from nonebot.adapters.cqhttp import Bot
from nonebot.typing import T_State

from ..config import config
from ..matcher import fr24


async def help_handler(bot: Bot, state: T_State) -> Any:
    cmd = state['cmd']
    if cmd in config.CMDF_HELP:
        await fr24.finish('\n'.join((
            "FlightRadar24查询v0.2，命令以 \"/fr24\" 开头：\n",
            "/fr24 help 帮助",
            "/fr24 now 查看当前航空器",
            "/fr24 from XXX 出发机场筛选（IATA）",
            "/fr24 to XXX 到达机场筛选（IATA）",
            "/fr24 airport XXX 机场筛选（IATA）",
            "/fr24 type XXXX 机型筛选（例：B738）",
            "/fr24 airline XX 航司筛选（例：MF）",
            "其他功能请等待后续开发~"      
        )))
        return