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
          "step": "middle",
          "lineStyle": {
            "width": 3
          }
        }, {
          "data": [],
          "name": "供給予想",
          "type": "line",
          "step": "middle",
          "lineStyle": {
            "width": 3
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
        '#a3bfcc',
        '#1d78a3',
        '#dbcfaf',
        '#ebb736'
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
        '#9babaa',
        '#04d4c6',
        '#d4d0b4',
        '#f2da3f'
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
        current_info["color"]  = "#28a148"

        if int(current_info["ratio"]) >= 92:
          current_info["label"]  = "厳しい"
          current_info["color"]  = "#ebc000"

        if int(current_info["ratio"]) >= 97:
          current_info["label"]  = "非常に厳しい"
          current_info["color"]  = "#d93725"

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


# Update "component-summary.json"
dt_now = datetime.datetime.now() + datetime.timedelta(hours = 9)
mdtext = "使用電力" + current_info["demand"] + "万kW / 供給力" + current_info["supply"] + "万kW、" + current_info["time"] + "時点（データ更新：" + dt_now.strftime('%-m月%-d日 %-H:%M') + "）"

markdown = {
	"componentName": "ComponentList",
	"config": {
		"components": [{
			"componentName": "Theme",
			"config": {
				"defaultFontScalar": 16,
				"colorScheme": "all",
				"text": {
					"h1": {
						"fontSize": "0.7rem",
						"lineHeight": "1.2em",
						"color": "#888"
					},
					"h2": {},
					"h3": {},
					"h4": {},
					"h5": {
						"color": "#888"
					},
					"h6": {},
					"subtitle1": {},
					"subtitle2": {},
					"caption": {},
					"body1": {
						"fontSize": "1.2rem",
						"color": "#fff",
						"fontWeight": "bold"
					},
					"body2": {
						"color": current_info["color"],
						"fontSize": "1.5rem",
						"lineHeight": "1.5em"
					},
					"link": {},
					"label": {},
					"button": {}
				},
				"icons": {
					"inline": {},
					"link": {}
				},
				"components": [{
					"componentName": "Container",
					"config": {
						"components": [{
							"componentName": "Container",
							"config": {
								"components": [{
									"componentName": "ContainerWithAspectRatio",
									"config": {
										"components": [{
											"componentName": "Chart",
											"config": {
												"isActive": True,
												"tooltipFormatterType": "basic",
												"base": {
													"margin": 0,
													"series": [{
														"type": "gauge",
														"radius": "100%",
														"startAngle": 90,
														"endAngle": -270,
														"pointer": {
															"show": False
														},
														"progress": {
															"show": True,
															"overlap": False,
															"roundCap": True,
															"clip": False,
															"itemStyle": {
																"borderWidth": 0,
																"borderColor": "#464646",
																"color": current_info["color"],

															}
														},
														"axisLine": {
															"lineStyle": {
																"width": 6
															}
														},
														"splitLine": {
															"show": False,
															"distance": 0,
															"length": 10
														},
														"axisTick": {
															"show": False
														},
														"axisLabel": {
															"show": False,
															"distance": 50
														},
														"data": [{
															"value": current_info["ratio"],
															"name": "Perfect",
															"title": {
																"show": False
															},
															"detail": {
																"valueAnimation": True,
																"offsetCenter": ["0%", "0%"],
																"fontSize": 72,
																"color": current_info["color"],
																"itemStyle": {
																	"borderWidth": 0,
																	"color": current_info["color"]
																}
															}
														}],
														"title": {
															"fontSize": 14
														},
														"detail": {
															"width": 3,
															"height": 14,
															"fontSize": 14,
															"color": "auto",
															"borderColor": "auto",
															"borderRadius": 0,
															"borderWidth": 0,
															"formatter": "{value}%"
														},
														"series": [{
															"data": [{
																"value": current_info["ratio"],
																"name": "Perfect",
																"title": {
																	"show": False
																},
																"detail": {
																	"valueAnimation": True,
																	"offsetCenter": ["0%", "0%"],
																	"fontSize": 16,
																	"color": current_info["color"],
																	"itemStyle": {
																		"borderWidth": 0,
																		"color": current_info["color"]
																	}
																}
															}],
															"pointer": {
																"show": False
															}
														}]
													}]
												},
												"light": {},
												"dark": {}
											}
										}],
										"aspectRatio": 1
									}
								}],
								"styles": {
									"display": "block",
									"flexDirection": "column",
									"border": {},
									"margin": {
										"top": "0.25rem",
										"bottom": "1.25rem"
									},
									"padding": {},
									"height": "240px",
									"justifyContent": "center",
									"alignItems": "center",
									"width": "240px"
								}
							}
						}, {
							"componentName": "Container",
							"config": {
								"components": [{
									"componentName": "Text",
									"config": {
										"type": "body1",
										"styles": {
											"margin": {
												"left": 0,
												"right": 0,
												"top": 8,
												"bottom": 8
											},
											"padding": {
												"left": 0,
												"right": 0,
												"top": 0,
												"bottom": 0
											}
										},
										"content": current_info["label"]
									}
								}],
								"styles": {
									"display": "block",
									"flexDirection": "row",
									"border": {},
									"margin": {},
									"padding": {
										"top": "0.125rem",
										"bottom": "0.125rem"
									},
									"justifyContent": "center",
									"alignItems": "center",
									"backgroundColor": current_info["color"],
									"width": 200,
									"textAlign": "center"
								}
							}
						}],
						"styles": {
							"display": "flex",
							"flexDirection": "column",
							"border": {},
							"margin": {
								"left": "0.5rem",
								"right": "0.5rem",
								"bottom": "1rem"
							},
							"padding": {},
							"justifyContent": "center",
							"alignItems": "center"
						}
					}
				}, {
					"componentName": "Text",
					"config": {
						"type": "h5",
						"content": mdtext
					}
				}]
			}
		}]
	}
}

with open(DIR_DATA + "component-summary.json", 'w') as f:
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





