import json
import os
import summary
import requests

def postit():
    data = summary.get_summary()
    # data = ['今年もグラコロの季節がやってきた! マクドナルドの冬の定番「グラコロ」、新作のほんのりトリュフ風味「ふわとろたまご濃厚デミグラコロ」が本日30日(水)発売～朝マックから #モーニングラコロできます', 'https://netatopi.jp/article/1459776.html', ['グラコロ', '♪', '季節'], '\n    1. 毎年冬になるとマクドナルドで「グラコロ」が登場します。\n    2. 新作「ふわとろたまご濃厚デミグラコロ」はコクのあるたまごとバターが香るふわとろ食感のスクランブルエッグ風フィリングと、ほんのりトリュフ風味のビーフの旨みが効いた濃厚デミソースを合わせた一品です。\n    3. 冬の風物詩「グラコロ」に、「ふわとろたまご濃厚デミグラコロ」が新登場します。']
    text = data[3].splitlines()
    text = [x.strip(' ') for x in text]



    api_url = 'https://secure-wave-16862.herokuapp.com/api0805mk/'
    title = data[0]
    kwd = ' , '.join(data[2])
    content01 = text[1]
    content02 = text[2]
    content03 = text[3]
    link = data[1]
    data = {
        "title": title,
        "kwd": kwd,
        "content01": content01,
        "content02": content02,
        "content03": content03,
        "link": link
    }
    r = requests.post(api_url,json=data)

    return r

postit()



