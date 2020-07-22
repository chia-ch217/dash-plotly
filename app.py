# -*- coding: utf-8 -*-
"""
Created on Sun May 17 01:42:21 2020

@author: GIGABYTE
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import math
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()

df = pd.read_excel('data_1.xlsx')
bubble_size = [math.sqrt(h / math.pi) for h in df["Hired"].values]
df['size'] = bubble_size
sizeref = 2*max(df['size'])/(100**2)
unique_job = list(df["Job"].unique())
colors = {
        'background' : '#222222',
        'text' : '#7FDFBB'}

app.layout = html.Div([
   html.H1(children='雇用人員數與薪資分佈'),
   html.H2('資訊系統分析及設計師 : 確認企業流程及工作準則，研究、分析、評估客戶資訊系統之需求、效率或問題，建議並設計最佳之企業資訊系統模式、功能及效能。'),
   html.H2('軟體開發及程式設計師 : 研究、分析、評估應用軟體與作業系統之需求，依符合品質認證標準之技術指令與規格，設計、撰寫、維護軟體程式碼，修改、擴充現有程式以增進作業效率，或因應新需求改寫程式。'),
   html.H2('資料庫及網路專業人員 : 設計、開發、控制、管理資料庫及網路等資訊系統，研究、分析及建議網際網路架構之策略，實作及設定網際網路相關軟硬體等，必要時提出變更建議案以改善系統及網路配置。'),
    
    dcc.Dropdown(                                         #放職稱
        id="job-dropdown",
        options=[
            {'label': i, 'value': i} for i in unique_job
        ],
        value=unique_job,
        multi=True
    ),
    dcc.Graph(id='data_1',
              animate=True
              ),
    #dcc.Graph(id='data_1_2',
    #          animate=True
    #          ),
    dcc.Slider(                                            #拉年份    
        id='year-slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        step=None,
        marks={str(year): str(year) for year in df['Year'].unique()}
    )
])

@app.callback(dash.dependencies.Output('data_1', 'figure'),
    [dash.dependencies.Input('year-slider', 'value'),
     dash.dependencies.Input('job-dropdown', 'value')])

def update_figure(selected_year, selected_job):
    year_filtered_df = df[df.Year == selected_year]
    filtered_df = year_filtered_df[df.Job.isin(selected_job)]
    traces = []
    for i in filtered_df.Job.unique():
        df_by_job = filtered_df[filtered_df['Job'] == i]
        traces.append(go.Scatter(
                x=df_by_job['Hired'],
                y=df_by_job['Sum'],
                text=df_by_job['Industry'],
                mode='markers',
                opacity=0.7,
                marker={
                        'size': df[df['Job'] == i]['size'],
                        'line': {'width': 0.5, 'color': 'white'},
                        'sizeref': sizeref,
                        'symbol': 'circle',
                        'sizemode': 'area'
                        },
                        name=i
                    )
        )
    return {
            'data': traces,
            'layout': go.Layout(
                    xaxis={'type': 'log', 'title': '雇用人數','titlefont':{'size':30}},
                    yaxis={'title': '總薪資', 'range': [20000, 200000],'titlefont':{'size':30}},
                    width=2000,
                    margin={'l': 80, 'b': 40, 't': 40, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                    )
            }
    
'''
#經常性薪資 & 非經常性薪資
@app.callback(dash.dependencies.Output('data_1_2', 'figure'),
    [dash.dependencies.Input('year-slider', 'value'),
     dash.dependencies.Input('job-dropdown', 'value')])

def update_figure_1(selected_year, selected_job):
    year_filtered_df = df[df.Year == selected_year]
    filtered_df = year_filtered_df[df.Job.isin(selected_job)]
    traces = []
    traces1 = []
    industry = ['製造業','電力及燃氣供應業','營造業','批發及零售業','運輸及倉儲業','住宿及餐飲業','資訊及通訊傳播業',
                '金融及保險業','不動產業','專業、科學及技術服務業','支援服務業','醫療保健及社會工作服務業','藝術、娛樂及休閒服務業']
    for i in filtered_df.Job.unique():
        df_by_salary = filtered_df[filtered_df['Job'] == i]
        salary = go.Bar(
                x=['1','2','3','4','5','6','7','8','9','10','11','12','13','14'],
                y=df_by_salary['Salary'],
                text=df_by_salary['Industry'],
                name=i
                    )
        traces.append(salary)
            
        bonus = go.Heatmap(
                z=[df_by_salary['Salary'],df_by_salary['Bonus']],
               
               
                name=i
                )
        
        traces1.append(bonus)
    return {
            'data': traces1,
            'layout': go.Layout(
                    xaxis={'type': 'linear', 'title': 'Industry'},
                    yaxis={'title': 'Salary'},
                    width=2000,
                    height=800,
                    margin={'l': 80, 'b': 40, 't': 40, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest',
                    )
            }

'''
if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True)
