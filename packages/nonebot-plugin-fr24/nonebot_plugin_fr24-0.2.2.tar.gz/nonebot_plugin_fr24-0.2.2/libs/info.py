class Info(object):

    # URLs:
    data_live_url = "https://data-live.flightradar24.com"
    flightradar_url = "https://www.flightradar24.com"

    # Flights data URLs:

    real_time_flight_tracker_data_url = data_live_url + "/zones/fcgi/feed.js"
    flight_data_url = data_live_url + "/clickhandler/?flight={}"

    headers = {
        "accept-encoding": "gzip, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "origin": "https://www.flightradar24.com",
        "referer": "https://www.flightradar24.com/",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "none",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67"
    }

    json_headers = headers.copy()
    json_headers["accept"] = "application/json"

    params = {
    "faa": "1",
    "satellite": "1",
    "mlat": "1",
    "flarm": "1",
    "adsb": "1",
    "gnd": "1",
    "air": "1",
    "vehicles": "1",
    "estimated": "1",
    "maxage": "14400",
    "gliders": "1",
    "stats": "1"}

    message_tip = "（基于端口返回航班数据条数统计，仅供参考）"