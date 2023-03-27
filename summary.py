import openai
import scrayping
import re


def get_summary():
    openai.api_key = "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"

    title,url,kwd = scrayping.sentences()

    # インプットテキスト
    input_text = open('sentences.txt','r',encoding='utf-8')
    input_text = input_text.read(2000)

    # テキストデータの前処理
    # input_text = re.sub(r'[!"#$%&()*+,-.:;<=>?@[]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％■◇◆※]', '', input_text)
    input_text = input_text.lower() # 小文字に統一


    def text_summary(prompt):
        # 分析の実施
        response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        )

        # 分析結果の出力
        # return response["choices"][0]["text"].replace('\n','')
        return response["choices"][0]["text"]

    def crean_text(text):
        text= text.replace('　',' ')

        return text

    # 要約を3点で出力するように調整
    prompt ='''
    Tl;dr
    ポイントは以下の3点です。
    '''

    prompt = crean_text(input_text) +  prompt


    # 結果出力
    summary = text_summary(prompt)

    return [title,url,kwd,summary]

