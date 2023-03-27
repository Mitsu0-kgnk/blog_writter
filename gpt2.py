import gtrend
from transformers import T5Tokenizer, AutoModelForCausalLM
import tensorflow as tf
import torch

tokenizer = T5Tokenizer.from_pretrained("rinna/japanese-gpt-1b")
model = AutoModelForCausalLM.from_pretrained("rinna/japanese-gpt-1b")


def generate_sentences(seed_sentence):
    x = tokenizer.encode(seed_sentence, return_tensors='pt', add_special_tokens=False) #入力
    y = model.generate(x, #入力
    min_length=50, #文章の最小長
    max_length=100, #文章の最大長
    do_sample=True, #次の単語を確立で選ぶ
    top_k=50, #Top-Kサンプリング
    top_p=0.95, #Top-pサンプリング
    temperature=1.2, #確率分布の調整
    num_return_sequences=3, #生成する文章の数
    pad_token_id=tokenizer.pad_token_id, #パディングのトークンID
    bos_token_id=tokenizer.bos_token_id, #テキスト先頭のトークンID
    eos_token_id=tokenizer.eos_token_id, #テキスト終端のトークンID
    bad_words_ids=[[tokenizer.unk_token_id]]) #生成が許可されないトークンID

    generated_sentences = tokenizer.batch_decode(y, skip_special_tokens=True) #特殊トークンをスキップして文章に変換
    return generated_sentences

seed_sentence = gtrend.get_kwd().trend_kwd()
generated_sentences = generate_sentences(seed_sentence) #生成された文章


# print('今日のキーワード：',gtrend.get_kwd().trend_kwd()[0],gtrend.get_kwd().trend_kwd()[1])
for sentence in generated_sentences:
    print(sentence)