from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
import relate


def sentences():
    option = Options()                          # オプションを用意
    option.add_argument('--incognito')          # シークレットモードの設定を付与
    option.add_argument('--headless')           # ヘッドレスモードの設定を付与
    driver = webdriver.Chrome(options=option)


    # キーワードを取得
    kwd = relate.relates().kw_extracat()

    #Googleニュースのブラウザを開く
    driver.get(f'https://news.google.com/search?q={kwd}&hl=ja&gl=JP&ceid=JP:ja')
    url = driver.current_url

    #検索結果1位をクリック
    # g = driver.find_element(By.TAG_NAME,"main")
    # r = g.find_elements(By.TAG_NAME,"a")[0].get_attribute('href')

    while True:
        try:
            r = driver.find_elements(By.TAG_NAME,"h3")
            title = r[0].text
            driver.get(r[0].find_element(By.TAG_NAME,"a").get_attribute('href'))
        except Exception as e:
            pass
        else:
            break

    time.sleep(1)
    # Pタグからテキストを取得
    news_url = driver.current_url

    if driver.find_elements(By.TAG_NAME,'article'):
        article = driver.find_elements(By.TAG_NAME,'article')
    elif driver.find_elements(By.TAG_NAME,'main'):
        article = driver.find_elements(By.TAG_NAME,'main')
    else:
        article = driver.find_elements(By.TAG_NAME,'div')


    # article = driver.find_element(By.TAG_NAME,'article')
    # title_h1 = article.find_element(By.TAG_NAME,'h1').size() != 0
    # title = article.find_element(By.TAG_NAME,'title').size() != 0
    t = []
    for z in article:
        t.append(z.find_elements(By.TAG_NAME,'p'))
    # t = article.find_elements(By.TAG_NAME,'p')

    f = open('sentences.txt','w',encoding='utf-8')
    # f.write(f'{title.text}\n')
    # f.write(f'{title_h1.text}\n')
    for m in t:
        for te in m:
            f = open('sentences.txt','a',encoding='utf-8')
            f.write(f'{te.text}\n')
        f.close()

    return [title,news_url,kwd]
    # # 検索上位２位をクリック
    # driver.get(url)
    # # g = driver.find_element(By.TAG_NAME,"main")
    # # r2 = g.find_elements(By.TAG_NAME,"a")[1].get_attribute('href')
    # r = driver.find_elements(By.TAG_NAME,"h3")
    # driver.get(r[1].find_element(By.TAG_NAME,"a").get_attribute('href'))
    # time.sleep(1)
    # # Pタグからテキストを取得
    # t = driver.find_elements(By.TAG_NAME,'p')

    # for te in t:
    #     f = open('sentences.txt','a',encoding='utf-8')
    #     f.write(f'{te.text}\n')
    # f.close()
