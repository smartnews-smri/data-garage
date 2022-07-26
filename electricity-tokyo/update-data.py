# coding: utf-8

import datetime
import requests
import json



DIR_DATA = "./electricity-tokyo/"


url = "https://www.tepco.co.jp/forecast/html/images/juyo-d1-j.csv"
res = requests.get(url).content.decode("shift-jis")
rows = res.splitlines()

result = {
  "componentName": "Chart",
  "config": {
    "base": {
      "grid": {
        "left": 10,
        "right": 0,
        "top": 36,
        "bottom": 0,
        "containLabel": True
      },
      "legend": {
        "data": ["需要実績", "需要予想", "供給実績", "供給予想"]
      },
      "xAxis": {
        "type": "category",
        "data": ["0:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
      },
      "yAxis": {
        "type": "value"
      },
      "series": [{
          "data": [],
          "name": "需要実績",
          "type": "bar",
          "stack": "total"
        }, {
          "data": [],
          "name": "需要予想",
          "type": "bar",
          "stack": "total"
        }, {
          "data": [],
          "name": "供給実績",
          "type": "line",
          "lineStyle": {
            "width": 4
          }
        }, {
          "data": [],
          "name": "供給予想",
          "type": "line",
          "lineStyle": {
            "width": 4
          }
        }
      ]
    },
    "light": {
      "legend": {
        "textStyle": {
          "color": "#666666"
        }
      },
      "xAxis": {
        "type": "category",
        "axisLine": {
          "onZero": True,
          "lineStyle": {
            "color": "#AEAEAE"
          }
        }
      },
      "yAxis": {
        "type": "value",
        "axisLine": {
          "lineStyle": {
            "color": "#AEAEAE"
          }
        },
        "splitLine": {
          "lineStyle": {
            "color": "#AEAEAE",
            "width": 0.5
          }
        }
      },
      "color": [
        '#c2beb4',
        '#FCD055',
        '#d4a9a5',
        '#f57064'
      ]
    },
    "dark": {
      "legend": {
        "textStyle": {
          "color": "#eeeeee"
        }
      },
      "xAxis": {
        "axisLine": {
          "onZero": False,
          "lineStyle": {
            "color": "#E5E5E5"
          }
        }
      },
      "yAxis": {
        "type": "value",
        "axisLine": {
          "lineStyle": {
            "color": "#E5E5E5"
          }
        },
        "splitLine": {
          "lineStyle": {
            "color": "#E5E5E5",
            "width": 0.5
          }
        }
      },
      "color": [
        '#c2beb4',
        '#FCD055',
        '#d4a9a5',
        '#f57064'
      ]
    }
  }
}

isPast = True
current_info = {
  "ratio":  "--",
  "label":  "データなし",
  "time":   "0:00",
  "demand": "--",
  "supply": "--",
  "color":  "#aaaaaa"
}

for i in range(14, 38):
  row = rows[i].split(",")

  if row[2] == "0":
    past_demand = None
    past_supply = None
    future_demand = int(row[3])
    future_supply = int(row[5])

    # Get current info
    if isPast:
      isPast = False

      if i >= 15:
        current_row = rows[i - 1].split(",")
        current_info["ratio"]  = current_row[4]
        current_info["time"]   = current_row[1]
        current_info["demand"] = current_row[2]
        current_info["supply"] = current_row[5]
        current_info["label"]  = "安定的"
        current_info["color"]  = "#4dad38"

        if int(current_info["ratio"]) >= 92:
          current_info["label"]  = "厳しい"
          current_info["color"]  = "#ffcc17"

        if int(current_info["ratio"]) >= 97:
          current_info["label"]  = "非常に厳しい"
          current_info["color"]  = "#fb1b2a"

  else:
    past_demand = int(row[2])
    past_supply = int(row[5])
    future_demand = None
    future_supply = None

  result["config"]["base"]["series"][0]["data"].append(past_demand)
  result["config"]["base"]["series"][1]["data"].append(future_demand)
  result["config"]["base"]["series"][2]["data"].append(past_supply)
  result["config"]["base"]["series"][3]["data"].append(future_supply)


# Save file
with open(DIR_DATA + "component-chart.json", 'w') as f:
  json.dump(result, f, ensure_ascii = False)


# Update "component-markdown.json"
dt_now = datetime.datetime.now() + datetime.timedelta(hours = 9)

mdtext  = "東京電力エリアの電力使用率"
mdtext += "\n# " + current_info["ratio"] + "％"
mdtext += "\n### ［" + current_info["label"] + "］"
mdtext += "\n###### 使用電力" + current_info["demand"] + "万kW / 供給力" + current_info["supply"] + "万kW、" + current_info["time"] + "時点（データ更新：" + dt_now.strftime('%-m月%-d日 %-H:%M') + "）"
mdtext += "\n使用電力・供給力の推移"

markdown = {
  "componentName": "Markdown",
  "config": {
    "markdown": mdtext
  }
}

with open(DIR_DATA + "component-markdown.json", 'w') as f:
  json.dump(markdown, f, ensure_ascii = False)


# Update "current-info.json"
with open(DIR_DATA + "current-info.json", 'w') as f:
  json.dump(current_info, f, ensure_ascii = False)


# Update "update-time.json"
dt_now = datetime.datetime.now() + datetime.timedelta(hours = 9)
dt_str = dt_now.strftime('%Y-%m-%d %H:%M:%S')
latest = {
  'file_update': dt_str
}
with open(DIR_DATA + "update-time.json", 'w') as f:
  json.dump(latest, f, ensure_ascii = False)



