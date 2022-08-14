#!/usr/bin/env python
# coding: utf-8

# In[1]:

from talib.abstract import EMA


# In[2]:

API_KEY="6QGFYmbqhmDi6LFAPUSEujNivoIAU9liHR04XmogNV1sr8QEnWvbWNdb2HQ4haMq"
API_SECRET="cXe3IMhQ6xkZhSdnbsyoIkOFTdpii7I3KjVLMsBTGSdVmFQ2jOfgcYI2jUrW5ZCm"

from binance.client import Client
client = Client(API_KEY, API_SECRET)



# In[10]:


candles = client.get_klines(symbol='BATUSDT', interval=Client.KLINE_INTERVAL_5MINUTE, limit=1000)


# In[11]:


klines_btcusdt = list(map(lambda x : [float(x[1]), float(x[2]), float(x[3]), float(x[4])], candles))


# In[12]:


import numpy as np


# In[13]:


klines_btcusdt = np.array(klines_btcusdt)


# In[33]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots

ema200 = EMA(klines_btcusdt[:, 3], 200)
ema150 = EMA(klines_btcusdt[:, 3], 150)

is_close_ema = np.isclose(ema150, ema200)
ema_gradient = np.gradient(ema150-ema200)

fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.2)

fig.add_trace(
    go.Candlestick(
        open=klines_btcusdt[:, 0],
        high=klines_btcusdt[:, 1],
        low=klines_btcusdt[:, 2],
        close=klines_btcusdt[:, 3]
    ),
    row=1, col=1
)

fig.add_trace(go.Line(y = ema200), row=1, col=1)
fig.add_trace(go.Line(y = ema150), row=1, col=1)
fig.add_trace(go.Line(y = ema_gradient), row=2, col=1)
fig.add_trace(go.Line(y = is_close_ema), row=3, col=1)


fig.show()