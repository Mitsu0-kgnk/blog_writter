import termextract.janome
import termextract.core
from collections import OrderedDict
from janome.tokenizer import Tokenizer
import collections
import dbm
import demoji
import itertools

import json
import pandas as pd
import tweepy
from requests_oauthlib import OAuth1Session
import re

import gtrend

class relates():
    def kw_extracat(self):
        # API情報 
        CONSUMER_KEY = 'ImVGoxHYU0KEW1EjQSEfwj3wZ'
        CONSUMER_SECRET = 'vScInV6kgLV8W5xem6Iw7FbrLTIcXagdx3jSfC4mANki6x1d8k'
        ACCESS_TOKEN = '1175662253799956482-Q6ea6ShLamS4ubuIv1he7gCp7qry23'
        ACCESS_TOKEN_SECRET = 'ksQI9swPhKWYSLnI7RS9Mrv0wYHVGTnd6poPSC432gHp3'

        # Twitterオブジェクトの生成
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)

        kwd = gtrend.get_kwd().trend_kwd()
        # kwd = 'サッカー'

        # キーワードでツイートを検索して５０けん取得する
        # tw_l = [tweet.text for tweet in tweepy.Cursor(api.search_full_archive,label='sandbox', query=kwd).items(100) if (list(tweet.text)[:2]!=['R', 'T']) & (list(tweet.text)[0]!='@')]
        tw_l = [tweet.text for tweet in tweepy.Cursor(api.search_tweets, q=kwd).items(100) if (list(tweet.text)[:2]!=['R', 'T']) & (list(tweet.text)[0]!='@')]
        tweets = []
        # 不要な文字列を削除する
        for tw in tw_l:
            # テキストデータの前処理
            new = tw.replace('\n',' ')  # 改行削除
            new = re.sub(r'[!"#$%&()*+,-.:;<=>?@[]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％■◇◆※♪♩♫ω]', '', new)
            new = re.sub("[\uFF01-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF40\uFF5B-\uFF65\u3000-\u303F]", '', new)
            new = new.replace('\u2060',' ') #多分画像コード
            new = new.replace('\u3000',' ') #わかんないけど削除
            new = new.replace('\u200d',' ') #わかんないけど削除
            new = new.replace('・・・',' ') #わかんないけど削除
            # new = new.replace('w',' ') #わかんないけど削除
            new = re.sub(r'http?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', new)
            new = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', new)
            new = new.replace('https://t', ' ') #多分メンションのリンク
            new = new.replace('co',' ') #同じくメンションのリンクと思われ
            new = demoji.replace(string=new,repl=' ')   #絵文字削除
            tweets.append(new)
        # ツイートをテキストファイルに保存
        f = open('tweets.txt','w',encoding='utf-8')
        for tweet in tweets:
            f = open('tweets.txt','a',encoding='utf-8')
            f.write(tweet)
        f.close()

        # dbmとjanomeの用意
        DB = dbm.open('store-lr','n')
        t = Tokenizer()

        #ファイルを読み込む
        tweets_text = open('tweets.txt','r',encoding='utf-8').read()
        #キーワード抽出のための関数
        def extract_keyword(text):    
            t = Tokenizer()
            tokenize_text = t.tokenize(text) #janomeによる日本語の形態素解析の処理
            frequency = termextract.janome.cmp_noun_dict(tokenize_text) #複合語抽出処理

            lr = termextract.core.score_lr( #FrequencyからLRを生成する
                frequency,
                ignore_words=termextract.mecab.IGNORE_WORDS,
                lr_mode=1, average_rate=1)
            
            term_imp = termextract.core.term_importance(frequency, lr) #FrequencyとLRを組み合わせ、FLRの重要度を出す

            data_collection = collections.Counter(term_imp) #collectionsを使用して重要度が高い順に整理
            kw_data = []
            kw_data.append(data_collection.most_common()[0][0]) #もっとも重要度の高い単語を返す
            kw_data.append(data_collection.most_common()[1][0]) 
            kw_data.append(data_collection.most_common()[2][0]) 
            # kw_data.append(data_collection.most_common()[3][0]) 
            return kw_data

        kwds_list = extract_keyword(tweets_text)
        # print(kwds_list)
        kwds = []
        for k in kwds_list:
            k = k.split()
            kwds.append(k)
        # print(kwds)
        kwds = list(itertools.chain.from_iterable(kwds))
        # kwds = list(set(kwds))
        
        # print(kwds)
        for k in kwds.copy():
            for s in kwds.copy():
                if k != s:
                    if k in s:
                        kwds.remove(k)
        kwds = list(OrderedDict.fromkeys(kwds))
        # print(kwds)
        

        
        # kwds = set(kwds)
        return kwds
# kwds_list.append(gtrend.get_kwd().related_kwd(kwd))
# print(relates().kw_extracat())