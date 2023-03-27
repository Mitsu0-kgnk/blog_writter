import json
import twitter
from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from collections import OrderedDict


class get_kwd():
    def trend_kwd(self):
        # twitter情報からキーワード設定
        kwd_list = list(set(twitter.get_tweet().trends()[:5]))
        # kwd_list = ['サッカー','スポーツ','#FNS歌謡祭']

        #タイムゾーンと時間設定
        pytrends = TrendReq(hl='ja-JP', tz=-540)
        # pytrends = TrendReq(hl='ja-JP', tz=-540,timeout=(10,25), proxies=['https://34.203.233.13:80',], retries=2, backoff_factor=0.1, requests_args={'verify':False})
        # pytrends = TrendReq(hl='en-US', tz=360)

        #データ作成
        pytrends.build_payload(kwd_list, cat=0, timeframe='now 1-d',geo='JP',gprop='')
        #データ取得
        # kw_df = pytrends.interest_over_time().drop('isPartial', axis=1)
        kw_df = pytrends.interest_over_time()
        #列ごとに検索数の合計を出す
        kw_df = kw_df.sum()
        #検索数の多いキーワードを抽出
        top_kw = kw_df.idxmax()

        return top_kw

