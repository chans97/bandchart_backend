from ast import literal_eval
from urllib import parse
from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from datetime import datetime
from pykrx import stock

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_sise(code, start_time, end_time, time_from='day'):
    get_param = {
        'symbol': code,
        'requestType': 1,
        'startTime': start_time,
        'endTime': end_time,
        'timeframe': time_from
    }
    get_param = parse.urlencode(get_param)
    url = "https://api.finance.naver.com/siseJson.naver?%s" % (get_param)
    response = requests.get(url)
    return literal_eval(response.text.strip())


@app.get("/price/{ticker}/{startdate}/{enddate}")
async def root(ticker: str, startdate: str, enddate: str):
    result_resposse = {}
    result = []
    cnt = 0
    name = stock.get_market_ticker_name(ticker)
    all_days = get_sise(ticker, startdate, enddate, 'day')
    stock_name = stock.get_market_fundamental(startdate, enddate, ticker)
    per_list = stock_name['PER'].tolist()
    pbr_list = stock_name['PBR'].tolist()
    row_per = 100000000
    high_per = -100000000
    row_pbr = 100000000
    high_pbr = -100000000
    for day in all_days:
        if (cnt):
            row_per = min(row_per, per_list[cnt-1])
            high_per = max(high_per, per_list[cnt-1])
            row_pbr = min(row_pbr, pbr_list[cnt-1])
            high_pbr = max(high_pbr, pbr_list[cnt-1])
        cnt = cnt+1

    cnt = 0
    for day in all_days:
        each_result = {}
        if (cnt):
            date = datetime.strptime(day[0], '%Y%m%d').strftime('%Y-%m-%d')
            each_result["date"] = date
            each_result["open"] = (day[1])
            each_result["high"] = (day[2])
            each_result["low"] = (day[3])
            each_result["close"] = (day[4])
            try:
                each_result["earning"] = day[4]/per_list[cnt-1]
            except:
                each_result["earning"] = 0

            try:
                each_result["equity"] = day[4]/pbr_list[cnt-1]
            except:
                each_result["equity"] = 0

            try:
                each_result["perhigh"] = round(
                    day[4]/per_list[cnt-1] * high_per, 2)
            except:
                each_result["perhigh"] = 0

            try:

                each_result["perlow"] = round(
                    day[4]/per_list[cnt-1] * row_per, 2)
            except:

                each_result["perlow"] = 0

            try:

                each_result["pbrhigh"] = round(
                    day[4]/pbr_list[cnt-1] * high_pbr, 2)
            except:

                each_result["pbrhigh"] = 0
            try:

                each_result["pbrlow"] = round(
                    day[4]/pbr_list[cnt-1] * row_pbr, 2)
            except:

                each_result["pbrlow"] = 0

            result.append(each_result)

        cnt = cnt+1
    result_resposse.update({"result": result})
    result_resposse.update({"lowper": round(row_per, 2)})
    result_resposse.update({"highper": round(high_per, 2)})
    result_resposse.update({"lowpbr": round(row_pbr, 2)})
    result_resposse.update({"highpbr": round(high_pbr, 2)})
    result_resposse.update({"name": name})
    json_compatible_item_data = jsonable_encoder(result_resposse)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/ticker/{name}")
async def find_ticker(name: str):

    return {"message": f"Hello qwe"}
