# coding: utf-8
!pip install mecab-python3 unidic-lite

import requests
import MeCab
from wordcloud import WordCloud

# GitHubのCSVを読み込んで行ごとの配列に分解
url = "https://raw.githubusercontent.com/smartnews-smri/house-of-representatives/main/data/gian.csv"
res = requests.get(url).content.decode("utf-8")
csv_rows = res.splitlines()

target = ""

for row in csv_rows[1:]:
  cells = row.split(",")

  # 国会回次を絞り込む
  if 201 >= int(cells[3]) or int(cells[3]) >= 208:
    continue

  # 議案種類を絞り込む
  if cells[11] not in ["衆法", "参法", "閣法"]:
    continue

  target += "\n" + cells[5]

# Mecabで形態素解析
tagger = MeCab.Tagger()
parsed = tagger.parse(target)
parsed_rows = parsed.split("\n")

result = ""

for row in parsed_rows:
  cells = row.split("\t")

  # EOSなど単語でないものを除外
  if len(cells) <= 5:
    continue

  # 名詞だけを対象とする
  if cells[4][0:2] != "名詞":
    continue

  result += cells[0] + " "

# WordCloudを使ってワードクラウド画像を生成
wordcloud = WordCloud(
  font_path = '/content/ZenAntique-Regular.ttf',
  width = 1200,
  height = 900,
  prefer_horizontal = 1,
  background_color = '#061a2b',
  colormap = 'GnBu',
  stopwords = ["法律", "一部", "改正", "措置", "促進", "推進", "ため"]
).generate(result)

# ファイル名を指定して画像を保存
wordcloud.to_file("/content/wordcloud-test.jpg")
