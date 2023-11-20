import datetime
import math
import statistics

import pandas
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# TODO: Clean this mess up
from PyTechnicalIndicators.Bulk import basic_indicators as bulk_basic_indicators
from PyTechnicalIndicators.Single import basic_indicators as single_basic_indicator
from PyTechnicalIndicators.Bulk import moving_averages as bulk_moving_average
from PyTechnicalIndicators.Single import moving_averages as single_moving_average
from PyTechnicalIndicators.Bulk import oscillators as bulk_oscillators
from PyTechnicalIndicators.Single import oscillators as single_oscillators
from PyTechnicalIndicators.Bulk import strength_indicators as bulk_strength_indicators
from PyTechnicalIndicators.Single import strength_indicators as single_strength_indicators
from PyTechnicalIndicators.Bulk import momentum_indicators as bulk_momentum_indicators
from PyTechnicalIndicators.Single import momentum_indicators as single_momentum_indicators
from PyTechnicalIndicators.Bulk import trend_indicators as bulk_trend_indicators
from PyTechnicalIndicators.Single import trend_indicators as single_trend_indicators
from PyTechnicalIndicators.Bulk import candle_indicators as bulk_candle_indicators
from PyTechnicalIndicators.Single import candle_indicators as single_candle_indicators
from PyTechnicalIndicators.Bulk import volatility_indicators as bulk_volatility_indicators
from PyTechnicalIndicators.Single import volatility_indicators as single_volatility_indicators
from PyTechnicalIndicators.Bulk import correlation_indicators as bulk_correlation_indicators
from PyTechnicalIndicators.Single import correlation_indicators as single_correlation_indicators
from PyTechnicalIndicators.Bulk import support_resistance_indicators as bulk_support_resistance_indicators
from PyTechnicalIndicators.Single import support_resistance_indicators as single_support_resistance_indicators
from PyTechnicalIndicators.Bulk import other_indicators as bulk_other_indicators
from PyTechnicalIndicators.Single import other_indicators as single_other_indicators
from PyTechnicalIndicators.Chart_Patterns import peaks
from PyTechnicalIndicators.Chart_Patterns import valleys
from PyTechnicalIndicators.Chart_Patterns import chart_trends

data = pandas.read_csv("example.csv", sep='\t', index_col=0, parse_dates=True)
data.index.name = 'Date'
data['Typical Price'] = (data['High'] + data['Low'] + data['Close']) / 3
data.sort_index(inplace=True)

latest_date = datetime.date(2023, 10, 12)
latest_open = 4380.94
latest_high = 4382.67
latest_low = 4370.34
latest_close = 4370.56
latest_typical_price = (latest_high + latest_close + latest_low) / 3
latest_volume = 184806058

# print(data)
fig = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "bar"}]]
)

fig.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data['Typical Price'],
        name='Typical Price',
        line={'color': 'blue'}
    )
)
fig.add_trace(
    go.Bar(
        x=data.index,
        y=data['Volume'],
        name='Volume'
    ),
    row=2, col=1
)
# fig.update_layout(xaxis_rangeslider_visible=False)
# fig.show()
fig.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='OHLC',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig.write_image('assets/OHLC.png', height=800, width=1600)

# Mean

weekly_mean = bulk_basic_indicators.mean(data['Typical Price'], 5)
monthly_mean = bulk_basic_indicators.mean(data['Typical Price'], 20)
quarterly_mean = bulk_basic_indicators.mean(data['Typical Price'], 60)

# print(weekly_mean)

weekly_mean.append(statistics.mean(data['Typical Price'][-4:].tolist()+[latest_typical_price]))
monthly_mean.append(statistics.mean(data['Typical Price'][-19:].tolist()+[latest_typical_price]))
quarterly_mean.append(statistics.mean(data['Typical Price'][-59:].tolist()+[latest_typical_price]))

fig_mean = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_mean.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_mean.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_mean):],
        y=weekly_mean,
        name='Weekly Mean',
        line={'color': '#FFE4C4'}
    )
)
fig_mean.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_mean):],
        y=monthly_mean,
        name='Monthly Mean',
        line={'color': '#E9967A'}
    )
)
fig_mean.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_mean):],
        y=quarterly_mean,
        name='Quarterly Mean',
        line={'color': '#FF7F50'}
    )
)
fig_mean.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_mean.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Mean',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_mean.write_image('assets/mean.png', height=800, width=1600)

# Median

weekly_median = bulk_basic_indicators.median(data['Typical Price'], 5)
monthly_median = bulk_basic_indicators.median(data['Typical Price'], 20)
quarterly_median = bulk_basic_indicators.median(data['Typical Price'], 60)

# print(weekly_median)

weekly_median.append(statistics.median(data['Typical Price'][-4:].tolist()+[latest_typical_price]))
monthly_median.append(statistics.median(data['Typical Price'][-19:].tolist()+[latest_typical_price]))
quarterly_median.append(statistics.median(data['Typical Price'][-59:].tolist()+[latest_typical_price]))

fig_median = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_median.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_median.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_median):],
        y=weekly_median,
        name='Weekly Median',
        line={'color': '#FFE4C4'}
    )
)
fig_median.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_median):],
        y=monthly_median,
        name='Monthly Median',
        line={'color': '#E9967A'}
    )
)
fig_median.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_median):],
        y=quarterly_median,
        name='Quarterly Median',
        line={'color': '#FF7F50'}
    )
)
fig_median.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_median.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Median',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_median.write_image('assets/median.png', height=800, width=1600)

# Standard Deviation

weekly_standard_deviation = bulk_basic_indicators.standard_deviation(data['Typical Price'], 5)
monthly_standard_deviation = bulk_basic_indicators.standard_deviation(data['Typical Price'], 20)
quarterly_standard_deviation = bulk_basic_indicators.standard_deviation(data['Typical Price'], 60)

# print(weekly_standard_deviation)

weekly_standard_deviation.append(statistics.stdev(data['Typical Price'][-4:].tolist()+[latest_typical_price]))
monthly_standard_deviation.append(statistics.stdev(data['Typical Price'][-19:].tolist()+[latest_typical_price]))
quarterly_standard_deviation.append(statistics.stdev(data['Typical Price'][-59:].tolist()+[latest_typical_price]))

fig_stdev = make_subplots(
    rows=4,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "bar"}], [{"type": "bar"}], [{"type": "bar"}]]
)
fig_stdev.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_stdev.add_trace(
    go.Bar(
        x=data.index[-len(weekly_standard_deviation)-1:],
        y=weekly_standard_deviation,
        name='Weekly Standard Deviation'
    ),
    row=2, col=1
)
fig_stdev.add_trace(
    go.Bar(
        x=data.index[-len(monthly_standard_deviation)-1:],
        y=monthly_standard_deviation,
        name='Monthly Standard Deviation'
    ),
    row=3, col=1
)
fig_stdev.add_trace(
    go.Bar(
        x=data.index[-len(quarterly_standard_deviation)-1:],
        y=quarterly_standard_deviation,
        name='Quarterly Standard Deviation'
    ),
    row=4, col=1
)
fig_stdev.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_stdev.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Standard Deviation',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_stdev.write_image('assets/standard_deviation.png', height=800, width=1600)

# Variance

weekly_variance = bulk_basic_indicators.variance(data['Typical Price'], 5)
monthly_variance = bulk_basic_indicators.variance(data['Typical Price'], 20)
quarterly_variance = bulk_basic_indicators.variance(data['Typical Price'], 60)

# print(weekly_variance)

weekly_variance.append(statistics.variance(data['Typical Price'][-4:].tolist()+[latest_typical_price]))
monthly_variance.append(statistics.variance(data['Typical Price'][-19:].tolist()+[latest_typical_price]))
quarterly_variance.append(statistics.variance(data['Typical Price'][-59:].tolist()+[latest_typical_price]))

fig_var = make_subplots(
    rows=4,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "bar"}], [{"type": "bar"}], [{"type": "bar"}]]
)
fig_var.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_var.add_trace(
    go.Bar(
        x=data.index[-len(weekly_variance)-1:],
        y=weekly_variance,
        name='Weekly Variance'
    ),
    row=2, col=1
)
fig_var.add_trace(
    go.Bar(
        x=data.index[-len(monthly_variance)-1:],
        y=monthly_variance,
        name='Monthly Variance'
    ),
    row=3, col=1
)
fig_var.add_trace(
    go.Bar(
        x=data.index[-len(quarterly_variance)-1:],
        y=quarterly_variance,
        name='Quarterly Variance'
    ),
    row=4, col=1
)
fig_var.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_var.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Variance',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_var.write_image('assets/variance.png', height=800, width=1600)

# Mean absolute deviation

weekly_mean_absolute_deviation = bulk_basic_indicators.mean_absolute_deviation(data['Typical Price'], 5)
monthly_mean_absolute_deviation = bulk_basic_indicators.mean_absolute_deviation(data['Typical Price'], 20)
quarterly_mean_absolute_deviation = bulk_basic_indicators.mean_absolute_deviation(data['Typical Price'], 60)

# print(weekly_mean_absolute_deviation)

weekly_mean_absolute_deviation.append(single_basic_indicator.mean_absolute_deviation(data['Typical Price'][-4:].tolist()+[latest_typical_price]))
monthly_mean_absolute_deviation.append(single_basic_indicator.mean_absolute_deviation(data['Typical Price'][-19:].tolist()+[latest_typical_price]))
quarterly_mean_absolute_deviation.append(single_basic_indicator.mean_absolute_deviation(data['Typical Price'][-59:].tolist()+[latest_typical_price]))

fig_mad = make_subplots(
    rows=4,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "bar"}], [{"type": "bar"}], [{"type": "bar"}]]
)
fig_mad.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_mad.add_trace(
    go.Bar(
        x=data.index[-len(weekly_mean_absolute_deviation)-1:],
        y=weekly_mean_absolute_deviation,
        name='Weekly Mean Absolute Deviation'
    ),
    row=2, col=1
)
fig_mad.add_trace(
    go.Bar(
        x=data.index[-len(monthly_mean_absolute_deviation)-1:],
        y=monthly_mean_absolute_deviation,
        name='Monthly Mean Absolute Deviation'
    ),
    row=3, col=1
)
fig_mad.add_trace(
    go.Bar(
        x=data.index[-len(quarterly_mean_absolute_deviation)-1:],
        y=quarterly_mean_absolute_deviation,
        name='Quarterly Mean Absolute Deviation'
    ),
    row=4, col=1
)
fig_mad.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_mad.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Mean Absolute Deviation',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_mad.write_image('assets/mean_absolute_deviation.png', height=800, width=1600)

# Median absolute deviation

weekly_median_absolute_deviation = bulk_basic_indicators.median_absolute_deviation(data['Typical Price'], 5)
monthly_median_absolute_deviation = bulk_basic_indicators.median_absolute_deviation(data['Typical Price'], 20)
quarterly_median_absolute_deviation = bulk_basic_indicators.median_absolute_deviation(data['Typical Price'], 60)

# print(weekly_median_absolute_deviation)

weekly_median_absolute_deviation.append(single_basic_indicator.median_absolute_deviation(data['Typical Price'][-4:].tolist()+[latest_typical_price]))
monthly_median_absolute_deviation.append(single_basic_indicator.median_absolute_deviation(data['Typical Price'][-19:].tolist()+[latest_typical_price]))
quarterly_median_absolute_deviation.append(single_basic_indicator.median_absolute_deviation(data['Typical Price'][-59:].tolist()+[latest_typical_price]))

fig_mdad = make_subplots(
    rows=4,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "bar"}], [{"type": "bar"}], [{"type": "bar"}]]
)
fig_mdad.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_mdad.add_trace(
    go.Bar(
        x=data.index[-len(weekly_median_absolute_deviation)-1:],
        y=weekly_median_absolute_deviation,
        name='Weekly Median Absolute Deviation'
    ),
    row=2, col=1
)
fig_mdad.add_trace(
    go.Bar(
        x=data.index[-len(monthly_median_absolute_deviation)-1:],
        y=monthly_median_absolute_deviation,
        name='Monthly Median Absolute Deviation'
    ),
    row=3, col=1
)
fig_mdad.add_trace(
    go.Bar(
        x=data.index[-len(quarterly_median_absolute_deviation)-1:],
        y=quarterly_median_absolute_deviation,
        name='Quarterly Median Absolute Deviation'
    ),
    row=4, col=1
)
fig_mdad.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_mdad.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Median Absolute Deviation',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_mdad.write_image('assets/median_absolute_deviation.png', height=800, width=1600)

# Mode absolute deviation

weekly_mode_absolute_deviation = bulk_basic_indicators.mode_absolute_deviation(data['Typical Price'], 5)
monthly_mode_absolute_deviation = bulk_basic_indicators.mode_absolute_deviation(data['Typical Price'], 20)
quarterly_mode_absolute_deviation = bulk_basic_indicators.mode_absolute_deviation(data['Typical Price'], 60)

# print(weekly_mode_absolute_deviation)

weekly_mode_absolute_deviation.append(single_basic_indicator.mode_absolute_deviation(data['Typical Price'][-4:].tolist()+[latest_typical_price]))
monthly_mode_absolute_deviation.append(single_basic_indicator.mode_absolute_deviation(data['Typical Price'][-19:].tolist()+[latest_typical_price]))
quarterly_mode_absolute_deviation.append(single_basic_indicator.mode_absolute_deviation(data['Typical Price'][-59:].tolist()+[latest_typical_price]))

fig_mead = make_subplots(
    rows=4,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "bar"}], [{"type": "bar"}], [{"type": "bar"}]]
)
fig_mead.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_mead.add_trace(
    go.Bar(
        x=data.index[-len(weekly_mode_absolute_deviation)-1:],
        y=weekly_mode_absolute_deviation,
        name='Weekly Mode Absolute Deviation'
    ),
    row=2, col=1
)
fig_mead.add_trace(
    go.Bar(
        x=data.index[-len(monthly_mode_absolute_deviation)-1:],
        y=monthly_mode_absolute_deviation,
        name='Monthly Mode Absolute Deviation'
    ),
    row=3, col=1
)
fig_mead.add_trace(
    go.Bar(
        x=data.index[-len(quarterly_mode_absolute_deviation)-1:],
        y=quarterly_mode_absolute_deviation,
        name='Quarterly Mode Absolute Deviation'
    ),
    row=4, col=1
)
fig_mead.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_mead.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Mode Absolute Deviation',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_mead.write_image('assets/mode_absolute_deviation.png', height=800, width=1600)

# Logarithm

# TODO: Figure why it is used

log = bulk_basic_indicators.log(data['Typical Price'].tolist())

# print(log)

log.append(math.log(latest_typical_price))
fig_log = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"secondary_y": True}]]
)
fig_log.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_log.add_trace(
    go.Scatter(
        x=data.index[-len(log)-1:],
        y=log,
        name='Logged Typical Price',
        line={'color': 'blue'}
    ),
    secondary_y=True, row=1, col=1
)
fig_log.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_log.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Logarithm',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_log.write_image('assets/logarithm.png', height=800, width=1600)

# Log difference

log_diff = bulk_basic_indicators.log_diff(data['Typical Price'].tolist())

# print(log_diff)

log_diff.append(math.log(data['Typical Price'].iloc[-1]) - math.log(latest_typical_price))

fig_log_diff = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "Bar"}]]
)
fig_log_diff.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_log_diff.add_trace(
    go.Bar(
        x=data.index[-len(log)-1:],
        y=log_diff,
        name='Typical Price Log Difference'
    ),
    row=2, col=1
)
fig_log_diff.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_log_diff.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Log Difference',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_log_diff.write_image('assets/logarithm_difference.png', height=800, width=1600)

# Moving Average

weekly_ma = bulk_moving_average.moving_average(data['Typical Price'].tolist(), 5)
monthly_ma = bulk_moving_average.moving_average(data['Typical Price'].tolist(), 20)
quarterly_ma = bulk_moving_average.moving_average(data['Typical Price'].tolist(), 60)

# print(weekly_ma)

weekly_ma.append(single_moving_average.moving_average(data['Typical Price'][-4:].tolist() + [latest_typical_price]))
monthly_ma.append(single_moving_average.moving_average(data['Typical Price'][-19:].tolist() + [latest_typical_price]))
quarterly_ma.append(single_moving_average.moving_average(data['Typical Price'][-59:].tolist() + [latest_typical_price]))

fig_ma = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_ma.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_ma.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_ma):],
        y=weekly_ma,
        name='Weekly MA',
        line={'color': '#FFE4C4'}
    )
)
fig_ma.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_ma):],
        y=monthly_ma,
        name='Monthly MA',
        line={'color': '#E9967A'}
    )
)
fig_ma.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_ma):],
        y=quarterly_ma,
        name='Quarterly MA',
        line={'color': '#FF7F50'}
    )
)
fig_ma.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_ma.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Moving Average',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_ma.write_image('assets/moving_average.png', height=800, width=1600)

# Smoothed moving average

weekly_sma = bulk_moving_average.smoothed_moving_average(data['Typical Price'].tolist(), 5)
monthly_sma = bulk_moving_average.smoothed_moving_average(data['Typical Price'].tolist(), 20)
quarterly_sma = bulk_moving_average.smoothed_moving_average(data['Typical Price'].tolist(), 60)

# print(weekly_sma)

weekly_sma.append(single_moving_average.smoothed_moving_average(data['Typical Price'][-4:].tolist() + [latest_typical_price]))
monthly_sma.append(single_moving_average.smoothed_moving_average(data['Typical Price'][-19:].tolist() + [latest_typical_price]))
quarterly_sma.append(single_moving_average.smoothed_moving_average(data['Typical Price'][-59:].tolist() + [latest_typical_price]))

fig_sma = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_sma.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_sma.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_sma):],
        y=weekly_sma,
        name='Weekly SMA',
        line={'color': '#FFE4C4'}
    )
)
fig_sma.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_sma):],
        y=monthly_sma,
        name='Monthly SMA',
        line={'color': '#E9967A'}
    )
)
fig_sma.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_sma):],
        y=quarterly_sma,
        name='Quarterly SMA',
        line={'color': '#FF7F50'}
    )
)
fig_sma.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_sma.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Smoothed Moving Average',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_sma.write_image('assets/smoothed_moving_average.png', height=800, width=1600)

# Exponential moving average

weekly_ema = bulk_moving_average.exponential_moving_average(data['Typical Price'].tolist(), 5)
monthly_ema = bulk_moving_average.exponential_moving_average(data['Typical Price'].tolist(), 20)
quarterly_ema = bulk_moving_average.exponential_moving_average(data['Typical Price'].tolist(), 60)

# print(weekly_ema)

weekly_ema.append(single_moving_average.exponential_moving_average(data['Typical Price'][-4:].tolist() + [latest_typical_price]))
monthly_ema.append(single_moving_average.exponential_moving_average(data['Typical Price'][-19:].tolist() + [latest_typical_price]))
quarterly_ema.append(single_moving_average.exponential_moving_average(data['Typical Price'][-59:].tolist() + [latest_typical_price]))

fig_ema = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_ema.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_ema.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_ema):],
        y=weekly_ema,
        name='Weekly EMA',
        line={'color': '#FFE4C4'}
    )
)
fig_ema.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_ema):],
        y=monthly_ema,
        name='Monthly EMA',
        line={'color': '#E9967A'}
    )
)
fig_ema.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_ema):],
        y=quarterly_ema,
        name='Quarterly EMA',
        line={'color': '#FF7F50'}
    )
)
fig_ema.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_ema.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Exponential Moving Average',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_ema.write_image('assets/exponential_moving_average.png', height=800, width=1600)

# Personalised moving average

weekly_pma = bulk_moving_average.personalised_moving_average(data['Typical Price'].tolist(), 5, 4, 2)
monthly_pma = bulk_moving_average.personalised_moving_average(data['Typical Price'].tolist(), 20, 4, 2)
quarterly_pma = bulk_moving_average.personalised_moving_average(data['Typical Price'].tolist(), 60, 4, 2)

# print(weekly_ema)

weekly_pma.append(single_moving_average.personalised_moving_average(data['Typical Price'][-4:].tolist() + [latest_typical_price], 4, 2))
monthly_pma.append(single_moving_average.personalised_moving_average(data['Typical Price'][-19:].tolist() + [latest_typical_price], 4, 2))
quarterly_pma.append(single_moving_average.personalised_moving_average(data['Typical Price'][-59:].tolist() + [latest_typical_price], 4, 2))

fig_pma = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_pma.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_pma.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_pma):],
        y=weekly_pma,
        name='Weekly PMA',
        line={'color': '#FFE4C4'}
    )
)
fig_pma.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_pma):],
        y=monthly_pma,
        name='Monthly PMA',
        line={'color': '#E9967A'}
    )
)
fig_pma.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_pma):],
        y=quarterly_pma,
        name='Quarterly PMA',
        line={'color': '#FF7F50'}
    )
)
fig_pma.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_pma.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Personalised Moving Average',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_pma.write_image('assets/personalised_moving_average.png', height=800, width=1600)

# Moving Average Convergence Divergence

moving_average_convergence_divergence = bulk_moving_average.moving_average_convergence_divergence(data['Typical Price'].tolist())

# print(macd)
# print(signal)
macd = [i[0] for i in moving_average_convergence_divergence]
signal = [i[1] for i in moving_average_convergence_divergence]
histogram = [i[2] for i in moving_average_convergence_divergence]

macd.append(single_moving_average.macd_line(data['Typical Price'][-25:].tolist() + [latest_typical_price]))
signal.append(single_moving_average.signal_line(macd[-9:]))
histogram.append(macd[-1] - signal[-1])

fig_macd = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_macd.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_macd.add_trace(
    go.Scatter(
        x=data.index[-len(macd):],
        y=macd,
        name='MACD',
        line={'color': 'Blue'}
    ),
    row=2, col=1
)
fig_macd.add_trace(
    go.Scatter(
        x=data.index[-len(signal):],
        y=signal,
        name='Signal',
        line={'color': 'Orange'}
    ),
    row=2, col=1
)
fig_macd.add_trace(
    go.Bar(
        x=data.index[-len(histogram):],
        y=histogram,
        name='Difference'
    ),
    row=2, col=1
)
fig_macd.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_macd.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Moving Average Convergence Divergence',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_macd.write_image('assets/macd.png', height=800, width=1600)

# Personalised MACD
personalised_moving_average_convergence_divergence = bulk_moving_average.moving_average_convergence_divergence(data['Typical Price'].tolist(), 5, 20, 5, 'ema')

# print(personalised_macd)
# print(personalised_signal)

personalised_macd = [i[0] for i in personalised_moving_average_convergence_divergence]
personalised_signal = [i[1] for i in personalised_moving_average_convergence_divergence]
personalised_histogram = [i[2] for i in personalised_moving_average_convergence_divergence]

personalised_macd.append(single_moving_average.macd_line(data['Typical Price'][-19:].tolist() + [latest_typical_price], 5, 20, 'ema'))
personalised_signal.append(single_moving_average.signal_line(personalised_macd[-5:], 'ema'))
personalised_histogram.append(personalised_macd[-1] - personalised_signal[-1])

fig_pmacd = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_pmacd.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_pmacd.add_trace(
    go.Scatter(
        x=data.index[-len(personalised_macd):],
        y=personalised_macd,
        name='MACD',
        line={'color': 'Blue'}
    ),
    row=2, col=1
)
fig_pmacd.add_trace(
    go.Scatter(
        x=data.index[-len(personalised_signal):],
        y=personalised_signal,
        name='Signal',
        line={'color': 'Orange'}
    ),
    row=2, col=1
)
fig_pmacd.add_trace(
    go.Bar(
        x=data.index[-len(personalised_histogram):],
        y=personalised_histogram,
        name='Difference'
    ),
    row=2, col=1
)
fig_pmacd.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_pmacd.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Personalised MACD',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_pmacd.write_image('assets/personalised_macd.png', height=800, width=1600)

# McGinley Dynamic

weekly_mcginley_dynamic = bulk_moving_average.mcginley_dynamic(data['Typical Price'].tolist(), 5)
monthly_mcginley_dynamic = bulk_moving_average.mcginley_dynamic(data['Typical Price'].tolist(), 20)
quarterly_mcginley_dynamic = bulk_moving_average.mcginley_dynamic(data['Typical Price'].tolist(), 60)

# print(weekly_mcginley_dynamic)

weekly_mcginley_dynamic.append(single_moving_average.mcginley_dynamic(latest_typical_price, 5, weekly_mcginley_dynamic[-1]))
monthly_mcginley_dynamic.append(single_moving_average.mcginley_dynamic(latest_typical_price, 20, monthly_mcginley_dynamic[-1]))
quarterly_mcginley_dynamic.append(single_moving_average.mcginley_dynamic(latest_typical_price, 60, quarterly_mcginley_dynamic[-1]))

fig_mcginley = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_mcginley.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_mcginley.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_mcginley_dynamic):],
        y=weekly_mcginley_dynamic,
        name='Weekly McGinley Dynamic',
        line={'color': '#FFE4C4'}
    )
)
fig_mcginley.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_mcginley_dynamic):],
        y=monthly_mcginley_dynamic,
        name='Monthly McGinley Dynamic',
        line={'color': '#E9967A'}
    )
)
fig_mcginley.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_mcginley_dynamic):],
        y=quarterly_mcginley_dynamic,
        name='Quarterly McGinley Dynamic',
        line={'color': '#FF7F50'}
    )
)
fig_mcginley.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_mcginley.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='McGinley Dynamic',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_mcginley.write_image('assets/mcginley_dynamic.png', height=800, width=1600)

# Moving Average Envelopes

moving_average_envelope = bulk_moving_average.moving_average_envelopes(data['Typical Price'].tolist(), 20, 'ema', 2)
upper_envelope = [i[0] for i in moving_average_envelope]
moving_average = [i[1] for i in moving_average_envelope]
lower_envelope = [i[2] for i in moving_average_envelope]

# print(moving_average_envelope)

next_point = single_moving_average.moving_average_envelopes(data['Typical Price'][-19:].tolist() + [latest_typical_price], 'ema', 2)
upper_envelope.append(next_point[0])
moving_average.append(next_point[1])
lower_envelope.append(next_point[2])

fig_ma_envelope = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_ma_envelope.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_ma_envelope.add_trace(
    go.Scatter(
        x=data.index[-len(upper_envelope):],
        y=upper_envelope,
        name='Upper Envelope',
        line={'color': 'Green'}
    )
)
fig_ma_envelope.add_trace(
    go.Scatter(
        x=data.index[-len(moving_average):],
        y=moving_average,
        name='Moving Average',
        line={'color': 'Blue'}
    )
)
fig_ma_envelope.add_trace(
    go.Scatter(
        x=data.index[-len(lower_envelope):],
        y=lower_envelope,
        name='Lower Envelope',
        line={'color': 'Red'}
    )
)
fig_ma_envelope.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_ma_envelope.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='McGinley Dynamic',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_ma_envelope.write_image('assets/ma_envelope.png', height=800, width=1600)

# Oscillators
# Stochastic Oscillator

stochastic_oscillator = bulk_oscillators.stochastic_oscillator(data['Close'].tolist())

# print(stochastic_oscillator)

stochastic_oscillator.append(single_oscillators.stochastic_oscillator(data['Close'][-13:].tolist()+[latest_close]))

fig_so = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_so.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_so.add_trace(
    go.Scatter(
        x=data.index[-len(stochastic_oscillator):],
        y=stochastic_oscillator,
        name='Stochastic Oscillator',
        line={'color': 'Blue'}
    ),
    row=2, col=1,
)
fig_so.add_trace(
    go.Scatter(
        x=data.index[-len(stochastic_oscillator):],
        y=[80 for i in stochastic_oscillator],
        name='Overbought',
        line={'color': 'Red'}
    ),
    row=2, col=1,
)
fig_so.add_trace(
    go.Scatter(
        x=data.index[-len(stochastic_oscillator):],
        y=[20 for i in stochastic_oscillator],
        name='Oversold',
        line={'color': 'Green'}
    ),
    row=2, col=1,
)
fig_so.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_so.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Stochastic Oscillator',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_so.write_image('assets/stochastic_oscillator.png', height=800, width=1600)
fig_so.update_yaxes(row=2, col=1, range=[0, 100])

# Personalised Stochastic Oscillator

weekly_so = bulk_oscillators.stochastic_oscillator(data['Close'].tolist(), 5)
monthly_so = bulk_oscillators.stochastic_oscillator(data['Close'].tolist(), 20)
quarterly_so = bulk_oscillators.stochastic_oscillator(data['Close'].tolist(), 60)

# print(weekly_so)

weekly_so.append(single_oscillators.stochastic_oscillator(data['Close'][-4:].tolist()+[latest_close]))
monthly_so.append(single_oscillators.stochastic_oscillator(data['Close'][-19:].tolist()+[latest_close]))
quarterly_so.append(single_oscillators.stochastic_oscillator(data['Close'][-59:].tolist()+[latest_close]))

fig_pso = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_pso.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_pso.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_so):],
        y=weekly_so,
        name='Weekly Stochastic Oscillator',
        line={'color': '#FFE4C4'}
    ),
    row=2, col=1,
)
fig_pso.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_so):],
        y=monthly_so,
        name='Monthly Stochastic Oscillator',
        line={'color': '#E9967A'}
    ),
    row=2, col=1,
)
fig_pso.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_so):],
        y=quarterly_so,
        name='Quarterly Stochastic Oscillator',
        line={'color': '#FF7F50'}
    ),
    row=2, col=1,
)
fig_pso.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_so):],
        y=[80 for i in weekly_so],
        name='Overbought',
        line={'color': 'Red'}
    ),
    row=2, col=1,
)
fig_pso.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_so):],
        y=[20 for i in weekly_so],
        name='Oversold',
        line={'color': 'Green'}
    ),
    row=2, col=1,
)
fig_pso.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_pso.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Personalised Stochastic Oscillator',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_pso.write_image('assets/personalised_stochastic_oscillator.png', height=800, width=1600)
fig_pso.update_yaxes(row=2, col=1, range=[0, 100])

# Fast Stochastic

# Dropping the last value to demonstrate the use of the single function. This would obviously not be done normally
fast_stochastic = bulk_oscillators.fast_stochastic(weekly_so[:-1], 5, 'ema')

# print(fast_stochastic)

fast_stochastic.append(single_oscillators.fast_stochastic(weekly_so[-5:], 'ema'))
fig_fs = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_fs.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_fs.add_trace(
    go.Scatter(
        x=data.index[-len(fast_stochastic):],
        y=fast_stochastic,
        name='Fast Stochastic',
        line={'color': 'Blue'}
    ),
    row=2, col=1,
)
fig_fs.add_trace(
    go.Scatter(
        x=data.index[-len(fast_stochastic):],
        y=[80 for i in fast_stochastic],
        name='Overbought',
        line={'color': 'Red'}
    ),
    row=2, col=1,
)
fig_fs.add_trace(
    go.Scatter(
        x=data.index[-len(fast_stochastic):],
        y=[20 for i in fast_stochastic],
        name='Oversold',
        line={'color': 'Green'}
    ),
    row=2, col=1,
)
fig_fs.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_fs.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Fast Stochastic',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_fs.write_image('assets/fast_stochastic.png', height=800, width=1600)
fig_fs.update_yaxes(row=2, col=1, range=[0, 100])

# Slow Stochastic

# Once again the last item is dropped to demonstrate how the single version is called
slow_stochastic = bulk_oscillators.slow_stochastic(fast_stochastic[:-1], 5, 'ema')

# print(slow_stochastic)

slow_stochastic.append(single_oscillators.slow_stochastic(fast_stochastic[-5:], 'ema'))

fig_ss = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_ss.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_ss.add_trace(
    go.Scatter(
        x=data.index[-len(slow_stochastic):],
        y=slow_stochastic,
        name='Slow Stochastic',
        line={'color': 'Blue'}
    ),
    row=2, col=1,
)
fig_ss.add_trace(
    go.Scatter(
        x=data.index[-len(slow_stochastic):],
        y=[80 for i in slow_stochastic],
        name='Overbought',
        line={'color': 'Red'}
    ),
    row=2, col=1,
)
fig_ss.add_trace(
    go.Scatter(
        x=data.index[-len(slow_stochastic):],
        y=[20 for i in slow_stochastic],
        name='Oversold',
        line={'color': 'Green'}
    ),
    row=2, col=1,
)
fig_ss.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_ss.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Slow Stochastic',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_ss.write_image('assets/slow_stochastic.png', height=800, width=1600)
fig_ss.update_yaxes(row=2, col=1, range=[0, 100])

# Slow Stochastic DS

# Once again the last item is dropped to demonstrate how the single version is called
slow_stochastic_ds = bulk_oscillators.slow_stochastic_ds(slow_stochastic[:-1], 5, 'ema')

# print(slow_stochastic_ds)

slow_stochastic_ds.append(single_oscillators.slow_stochastic_ds(slow_stochastic[-5:], 'ema'))

fig_ssd = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_ssd.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_ssd.add_trace(
    go.Scatter(
        x=data.index[-len(slow_stochastic_ds):],
        y=slow_stochastic_ds,
        name='Slow Stochastic DS',
        line={'color': 'Blue'}
    ),
    row=2, col=1,
)
fig_ssd.add_trace(
    go.Scatter(
        x=data.index[-len(slow_stochastic_ds):],
        y=[80 for i in slow_stochastic_ds],
        name='Overbought',
        line={'color': 'Red'}
    ),
    row=2, col=1,
)
fig_ssd.add_trace(
    go.Scatter(
        x=data.index[-len(slow_stochastic_ds):],
        y=[20 for i in slow_stochastic_ds],
        name='Oversold',
        line={'color': 'Green'}
    ),
    row=2, col=1,
)
fig_ssd.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_ssd.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Slow Stochastic DS',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_ssd.write_image('assets/slow_stochastic_ds.png', height=800, width=1600)
fig_ssd.update_yaxes(row=2, col=1, range=[0, 100])

# Visualizing the stochastics

fig_all_so = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_all_so.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_all_so.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_so):],
        y=weekly_so,
        name='Weekly Stochastic Oscillator',
        line={'color': '#FFE4C4'}
    ),
    row=2, col=1,
)
fig_all_so.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_so):],
        y=monthly_so,
        name='Monthly Stochastic Oscillator',
        line={'color': '#E9967A'}
    ),
    row=2, col=1,
)
fig_all_so.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_so):],
        y=quarterly_so,
        name='Quarterly Stochastic Oscillator',
        line={'color': '#FF7F50'}
    ),
    row=2, col=1,
)
fig_all_so.add_trace(
    go.Scatter(
        x=data.index[-len(fast_stochastic):],
        y=fast_stochastic,
        name='Fast Stochastic',
        line={'color': 'Blue'}
    ),
    row=2, col=1,
)
fig_all_so.add_trace(
    go.Scatter(
        x=data.index[-len(slow_stochastic):],
        y=slow_stochastic,
        name='Slow Stochastic',
        line={'color': 'teal'}
    ),
    row=2, col=1,
)
fig_all_so.add_trace(
    go.Scatter(
        x=data.index[-len(slow_stochastic_ds):],
        y=slow_stochastic_ds,
        name='Slow Stochastic DS',
        line={'color': 'aqua'}
    ),
    row=2, col=1,
)
fig_all_so.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_so):],
        y=[80 for i in weekly_so],
        name='Overbought',
        line={'color': 'Red'}
    ),
    row=2, col=1,
)
fig_all_so.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_so):],
        y=[20 for i in weekly_so],
        name='Oversold',
        line={'color': 'Green'}
    ),
    row=2, col=1,
)
fig_all_so.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_all_so.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Stochastics',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_all_so.write_image('assets/stochastics.png', height=800, width=1600)
fig_all_so.update_yaxes(row=2, col=1, range=[0, 100])

# Money Flow Index

money_flow_index = bulk_oscillators.money_flow_index(data['Typical Price'].tolist(), data['Volume'].tolist())

# print(money_flow_index)

money_flow_index.append(single_oscillators.money_flow_index(data['Typical Price'][-13:].tolist()+[latest_typical_price], data['Volume'][-13:].tolist()+[latest_volume]))

fig_mfi = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_mfi.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_mfi.add_trace(
    go.Scatter(
        x=data.index[-len(money_flow_index):],
        y=money_flow_index,
        name='Money Flow Index',
        line={'color': 'Blue'}
    ),
    row=2, col=1,
)
fig_mfi.add_trace(
    go.Scatter(
        x=data.index[-len(money_flow_index):],
        y=[80 for i in money_flow_index],
        name='Overbought',
        line={'color': 'Red'}
    ),
    row=2, col=1,
)
fig_mfi.add_trace(
    go.Scatter(
        x=data.index[-len(money_flow_index):],
        y=[20 for i in money_flow_index],
        name='Oversold',
        line={'color': 'Green'}
    ),
    row=2, col=1,
)
fig_mfi.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_mfi.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Money Flow Index',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_mfi.write_image('assets/money_flow_index.png', height=800, width=1600)
fig_mfi.update_yaxes(row=2, col=1, range=[0, 100])

# Personalised Money Flow Index

weekly_personalised_mfi = bulk_oscillators.money_flow_index(data['Typical Price'].tolist(), data['Volume'].tolist(), 5)
monthly_personalised_mfi = bulk_oscillators.money_flow_index(data['Typical Price'].tolist(), data['Volume'].tolist(), 20)
quarterly_personalised_mfi = bulk_oscillators.money_flow_index(data['Typical Price'].tolist(), data['Volume'].tolist(), 60)

# print(weekly_personalised_mfi)

weekly_personalised_mfi.append(single_oscillators.money_flow_index(data['Typical Price'][-4:].tolist()+[latest_typical_price], data['Volume'][-4:].tolist()+[latest_volume]))
monthly_personalised_mfi.append(single_oscillators.money_flow_index(data['Typical Price'][-19:].tolist()+[latest_typical_price], data['Volume'][-19:].tolist()+[latest_volume]))
quarterly_personalised_mfi.append(single_oscillators.money_flow_index(data['Typical Price'][-59:].tolist()+[latest_typical_price], data['Volume'][-59:].tolist()+[latest_volume]))

fig_pmfi = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_pmfi.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_pmfi.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_personalised_mfi):],
        y=weekly_personalised_mfi,
        name='Weekly MFI',
        line={'color': '#FFE4C4'}
    ),
    row=2, col=1,
)
fig_pmfi.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_personalised_mfi):],
        y=monthly_personalised_mfi,
        name='Monthly MFI',
        line={'color': '#E9967A'}
    ),
    row=2, col=1,
)
fig_pmfi.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_personalised_mfi):],
        y=quarterly_personalised_mfi,
        name='Quarterly MFI',
        line={'color': '#FF7F50'}
    ),
    row=2, col=1,
)
fig_pmfi.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_so):],
        y=[80 for i in weekly_so],
        name='Overbought',
        line={'color': 'Red'}
    ),
    row=2, col=1,
)
fig_pmfi.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_so):],
        y=[20 for i in weekly_so],
        name='Oversold',
        line={'color': 'Green'}
    ),
    row=2, col=1,
)
fig_pmfi.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_pmfi.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Personalised Money Flow Index',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_pmfi.write_image('assets/personalised_money_flow_index.png', height=800, width=1600)
fig_pmfi.update_yaxes(row=2, col=1, range=[0, 100])

# Chaikin Oscillator
chaikin_oscillator = bulk_oscillators.chaikin_oscillator(data['High'].tolist(), data['Low'].tolist(), data['Close'].tolist(), data['Volume'].tolist())

# print(chaikin_oscillator)

chaikin_oscillator.append(single_oscillators.chaikin_oscillator(
    data['High'][-9:].tolist() + [latest_high],
    data['Low'][-9:].tolist() + [latest_low],
    data['Close'][-9:].tolist() + [latest_close],
    data['Volume'][-9:].tolist() + [latest_volume]))

# TODO: When charting chart against the accumulation distribution indicator?
fig_co = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_co.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_co.add_trace(
    go.Scatter(
        x=data.index[-len(chaikin_oscillator):],
        y=chaikin_oscillator,
        name='Chaikin Oscillator',
        line={'color': 'Blue'}
    ),
    row=2, col=1,
)
fig_co.add_trace(
    go.Scatter(
        x=data.index[-len(chaikin_oscillator):],
        y=[0 for i in chaikin_oscillator],
        line={'color': 'Gray'}
    ),
    row=2, col=1,
)
fig_co.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_co.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Chaikin Oscillator',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_co.write_image('assets/chaikin_oscillator.png', height=800, width=1600)

# Personalised Chaikin Oscillator
personalised_co = bulk_oscillators.chaikin_oscillator(data['High'].tolist(), data['Low'].tolist(), data['Close'].tolist(), data['Volume'].tolist(), 5, 20, 'ema')

# print(personalised_co)

personalised_co.append(single_oscillators.chaikin_oscillator(
    data['High'][-19:].tolist() + [latest_high],
    data['Low'][-19:].tolist() + [latest_low],
    data['Close'][-19:].tolist() + [latest_close],
    data['Volume'][-19:].tolist() + [latest_volume], 5, 'ema'))

fig_pco = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_pco.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_pco.add_trace(
    go.Scatter(
        x=data.index[-len(personalised_co):],
        y=personalised_co,
        name='Chaikin Oscillator',
        line={'color': 'Blue'}
    ),
    row=2, col=1,
)
fig_pco.add_trace(
    go.Scatter(
        x=data.index[-len(personalised_co):],
        y=[0 for i in personalised_co],
        line={'color': 'Gray'}
    ),
    row=2, col=1,
)
fig_pco.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_pco.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Personalised Chaikin Oscillator',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_pco.write_image('assets/personalised_chaikin_oscillator.png', height=800, width=1600)

# Williams %R
weekly_williams_percent_r = bulk_oscillators.williams_percent_r(data['High'].tolist(), data['Low'].tolist(), data['Close'].tolist(), 5)
monthly_williams_percent_r = bulk_oscillators.williams_percent_r(data['High'].tolist(), data['Low'].tolist(), data['Close'].tolist(), 20)
quarterly_williams_percent_r = bulk_oscillators.williams_percent_r(data['High'].tolist(), data['Low'].tolist(), data['Close'].tolist(), 60)

# print(weekly_williams_percent_r)

weekly_williams_percent_r.append(single_oscillators.williams_percent_r(latest_high, latest_low, latest_close))

fig_wr = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_wr.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_wr.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_williams_percent_r):],
        y=weekly_williams_percent_r,
        name='Weekly Williams %R',
        line={'color': '#FFE4C4'}
    ),
    row=2, col=1,
)
fig_wr.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_williams_percent_r):],
        y=monthly_williams_percent_r,
        name='Monthly Williams %R',
        line={'color': '#E9967A'}
    ),
    row=2, col=1,
)
fig_wr.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_williams_percent_r):],
        y=quarterly_williams_percent_r,
        name='Quarterly Williams %R',
        line={'color': '#FF7F50'}
    ),
    row=2, col=1,
)
fig_wr.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_williams_percent_r):],
        y=[-20 for i in weekly_williams_percent_r],
        name='Overbought',
        line={'color': 'Red'}
    ),
    row=2, col=1,
)
fig_wr.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_williams_percent_r):],
        y=[-80 for i in weekly_williams_percent_r],
        name='Oversold',
        line={'color': 'Green'}
    ),
    row=2, col=1,
)
fig_wr.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_wr.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Williams %R',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_wr.write_image('assets/williams_r.png', height=800, width=1600)
fig_wr.update_yaxes(row=2, col=1, range=[0, 100])

# Strength Indicators

# Relative Strength Index
rsi = bulk_strength_indicators.relative_strength_index(data['Typical Price'].tolist())
# print(rsi)
rsi.append(single_strength_indicators.relative_strength_index(data['Typical Price'][-13:].tolist() + [latest_typical_price]))

fig_rsi = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_rsi.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_rsi.add_trace(
    go.Scatter(
        x=data.index[-len(rsi):],
        y=rsi,
        name='RSI',
        line={'color': '#E9967A'}
    ),
    row=2, col=1,
)
fig_rsi.add_trace(
    go.Scatter(
        x=data.index[-len(rsi):],
        y=[30 for i in rsi],
        name='Oversold',
        line={'color': 'Green'}
    ),
    row=2, col=1,
)
fig_rsi.add_trace(
    go.Scatter(
        x=data.index[-len(rsi):],
        y=[70 for i in rsi],
        name='Overbought',
        line={'color': 'Red'}
    ),
    row=2, col=1,
)
fig_rsi.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_rsi.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Relative Strength Indicator',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_rsi.write_image('assets/rsi.png', height=800, width=1600)
fig_rsi.update_yaxes(row=2, col=1, range=[0, 100])

# Personalised RSI
weekly_rsi = bulk_strength_indicators.relative_strength_index(data['Typical Price'].tolist(), 5, 'ema')
monthly_rsi = bulk_strength_indicators.relative_strength_index(data['Typical Price'].tolist(), 20, 'ema')
quarterly_rsi = bulk_strength_indicators.relative_strength_index(data['Typical Price'].tolist(), 60, 'ema')

# print(weekly_rsi)

weekly_rsi.append(single_strength_indicators.relative_strength_index(data['Typical Price'][-4:].tolist() + [latest_typical_price], 'ema'))
monthly_rsi.append(single_strength_indicators.relative_strength_index(data['Typical Price'][-19:].tolist() + [latest_typical_price], 'ema'))
quarterly_rsi.append(single_strength_indicators.relative_strength_index(data['Typical Price'][-59:].tolist() + [latest_typical_price], 'ema'))

fig_prsi = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_prsi.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_prsi.add_trace(
    go.Scatter(
        x=data.index[-len(rsi):],
        y=weekly_rsi,
        name='Weekly RSI',
        line={'color': '#FFE4C4'}
    ),
    row=2, col=1,
)
fig_prsi.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_rsi):],
        y=monthly_rsi,
        name='Monthly RSI',
        line={'color': '#E9967A'}
    ),
    row=2, col=1,
)
fig_prsi.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_rsi):],
        y=quarterly_rsi,
        name='Quarterly RSI',
        line={'color': '#FF7F50'}
    ),
    row=2, col=1,
)
fig_prsi.add_trace(
    go.Scatter(
        x=data.index[-len(rsi):],
        y=[30 for i in rsi],
        name='Oversold',
        line={'color': 'Green'}
    ),
    row=2, col=1,
)
fig_prsi.add_trace(
    go.Scatter(
        x=data.index[-len(rsi):],
        y=[70 for i in rsi],
        name='Overbought',
        line={'color': 'Red'}
    ),
    row=2, col=1,
)
fig_prsi.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_prsi.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Personalised Relative Strength Indicator',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_prsi.write_image('assets/personalised_rsi.png', height=800, width=1600)
fig_prsi.update_yaxes(row=2, col=1, range=[0, 100])

# Accumulation Distribution Indicator
adi = bulk_strength_indicators.accumulation_distribution_indicator(data['High'].tolist(), data['Low'].tolist(), data['Close'].tolist(), data['Volume'].tolist())
# print(adi)
adi.append(single_strength_indicators.accumulation_distribution_indicator(
    latest_high,
    latest_low,
    latest_close,
    latest_volume,
    adi[-1]
))

fig_adi = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_adi.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_adi.add_trace(
    go.Scatter(
        x=data.index[-len(adi):],
        y=adi,
        name='ADI',
        line={'color': '#FFE4C4'}
    ),
    row=2, col=1,
)
fig_adi.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_adi.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Accumulation Distribution Indicator',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_adi.write_image('assets/adi.png', height=800, width=1600)

# Directional Indicator, Directional Index, Average Directional Index, Average Directional Index Rating

weekly_di = bulk_strength_indicators.directional_indicator(data['High'].tolist(), data['Low'].tolist(), data['Close'].tolist(), 5)
weekly_positive_di = [di[0] for di in weekly_di]
weekly_negative_di = [di[1] for di in weekly_di]
weekly_dx = bulk_strength_indicators.directional_index(weekly_positive_di, weekly_negative_di)
weekly_adx = bulk_strength_indicators.average_directional_index(weekly_dx, 5, 'ema')
weekly_adxr = bulk_strength_indicators.average_directional_index_rating(weekly_adx, 5)

monthly_di = bulk_strength_indicators.directional_indicator(data['High'].tolist(), data['Low'].tolist(), data['Close'].tolist(), 20)
monthly_positive_di = [di[0] for di in monthly_di]
monthly_negative_di = [di[1] for di in monthly_di]
monthly_dx = bulk_strength_indicators.directional_index(monthly_positive_di, monthly_negative_di)
monthly_adx = bulk_strength_indicators.average_directional_index(monthly_dx, 20, 'ema')
monthly_adxr = bulk_strength_indicators.average_directional_index_rating(monthly_adx, 20)

quarterly_di = bulk_strength_indicators.directional_indicator(data['High'].tolist(), data['Low'].tolist(), data['Close'].tolist(), 60)
quarterly_positive_di = [di[0] for di in quarterly_di]
quarterly_negative_di = [di[1] for di in quarterly_di]
quarterly_dx = bulk_strength_indicators.directional_index(quarterly_positive_di, quarterly_negative_di)
quarterly_adx = bulk_strength_indicators.average_directional_index(quarterly_dx, 60, 'ema')
quarterly_adxr = bulk_strength_indicators.average_directional_index_rating(quarterly_adx, 60)

weekly_di.append(single_strength_indicators.directional_indicator_known_previous(
    latest_high,
    data['High'].iloc[-1],
    latest_low,
    data['Low'].iloc[-1],
    data['Close'].iloc[-1],
    weekly_di[-1][2],
    weekly_di[-1][0],
    weekly_di[-1][1],
    5
))
weekly_dx.append(single_strength_indicators.directional_index(weekly_di[-1][0], weekly_di[-1][1]))
weekly_adx.append(single_strength_indicators.average_directional_index(weekly_dx[-5:], 'ema'))
weekly_adxr.append(single_strength_indicators.average_directional_index_rating(weekly_adx[-1], weekly_adx[-5]))

fig_wdx = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_wdx.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_wdx.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_dx):],
        y=weekly_dx,
        name='Weekly DX',
        line={'color': '#FFE4C4'}
    ),
    row=2, col=1,
)
fig_wdx.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_adx):],
        y=weekly_adx,
        name='Weekly ADX',
        line={'color': '#E9967A'}
    ),
    row=2, col=1,
)
fig_wdx.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_adxr):],
        y=weekly_adxr,
        name='Weekly ADX Rating',
        line={'color': '#FF7F50'}
    ),
    row=2, col=1,
)
fig_wdx.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_wdx.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Weekly Directional Index',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_wdx.write_image('assets/weekly_adx.png', height=800, width=1600)

monthly_di.append(single_strength_indicators.directional_indicator_known_previous(
    latest_high,
    data['High'].iloc[-1],
    latest_low,
    data['Low'].iloc[-1],
    data['Close'].iloc[-1],
    monthly_di[-1][2],
    monthly_di[-1][0],
    monthly_di[-1][1],
    20
))
monthly_dx.append(single_strength_indicators.directional_index(monthly_di[-1][0], monthly_di[-1][1]))
monthly_adx.append(single_strength_indicators.average_directional_index(monthly_dx[-20:], 'ema'))
monthly_adxr.append(single_strength_indicators.average_directional_index_rating(monthly_adx[-1], monthly_adx[-20]))

fig_mdx = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_mdx.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_mdx.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_dx):],
        y=monthly_dx,
        name='Monthly DX',
        line={'color': '#FFE4C4'}
    ),
    row=2, col=1,
)
fig_mdx.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_adx):],
        y=monthly_adx,
        name='Monthly ADX',
        line={'color': '#E9967A'}
    ),
    row=2, col=1,
)
fig_mdx.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_adxr):],
        y=monthly_adxr,
        name='Monthly ADX Rating',
        line={'color': '#FF7F50'}
    ),
    row=2, col=1,
)
fig_mdx.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_mdx.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Monthly Directional Index',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_mdx.write_image('assets/monthly_adx.png', height=800, width=1600)

quarterly_di.append(single_strength_indicators.directional_indicator_known_previous(
    latest_high,
    data['High'].iloc[-1],
    latest_low,
    data['Low'].iloc[-1],
    data['Close'].iloc[-1],
    quarterly_di[-1][2],
    quarterly_di[-1][0],
    quarterly_di[-1][1],
    60
))
quarterly_dx.append(single_strength_indicators.directional_index(quarterly_di[-1][0], quarterly_di[-1][1]))
quarterly_adx.append(single_strength_indicators.average_directional_index(quarterly_dx[-60:], 'ema'))
quarterly_adxr.append(single_strength_indicators.average_directional_index_rating(quarterly_adx[-1], quarterly_adx[-60]))

fig_qdx = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_qdx.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_qdx.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_dx):],
        y=quarterly_dx,
        name='Quarterly DX',
        line={'color': '#FFE4C4'}
    ),
    row=2, col=1,
)
fig_qdx.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_adx):],
        y=quarterly_adx,
        name='Quarterly ADX',
        line={'color': '#E9967A'}
    ),
    row=2, col=1,
)
fig_qdx.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_adxr):],
        y=quarterly_adxr,
        name='Quarterly ADX Rating',
        line={'color': '#FF7F50'}
    ),
    row=2, col=1,
)
fig_qdx.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_qdx.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Quarterly Directional Index',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_qdx.write_image('assets/quarterly_adx.png', height=800, width=1600)

# Momentum Indicators

# Rate of Change
weekly_roc = bulk_momentum_indicators.rate_of_change(data['Typical Price'].tolist(), 5)
monthly_roc = bulk_momentum_indicators.rate_of_change(data['Typical Price'].tolist(), 20)
quarterly_roc = bulk_momentum_indicators.rate_of_change(data['Typical Price'].tolist(), 60)
# print(weekly_roc)
weekly_roc.append(single_momentum_indicators.rate_of_change(latest_typical_price, data['Typical Price'].iloc[-4]))
monthly_roc.append(single_momentum_indicators.rate_of_change(latest_typical_price, data['Typical Price'].iloc[-19]))
quarterly_roc.append(single_momentum_indicators.rate_of_change(latest_typical_price, data['Typical Price'].iloc[-59]))

fig_roc = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_roc.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_roc.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_roc):],
        y=weekly_roc,
        name='Weekly RoC',
        line={'color': '#FFE4C4'}
    ),
    row=2, col=1,
)
fig_roc.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_roc):],
        y=monthly_roc,
        name='Monhtly RoC',
        line={'color': '#E9967A'}
    ),
    row=2, col=1,
)
fig_roc.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_roc):],
        y=quarterly_roc,
        name='Quarterly RoC',
        line={'color': '#FF7F50'}
    ),
    row=2, col=1,
)
fig_roc.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_roc.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Rate of Change',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_roc.write_image('assets/roc.png', height=800, width=1600)

# On Balance Volume
obv = bulk_momentum_indicators.on_balance_volume(data['Close'].tolist(), data['Volume'].tolist())
# print(obv)
obv.append(single_momentum_indicators.on_balance_volume(latest_close, data['Close'].iloc[-1], latest_volume, data['Volume'].iloc[-1]))

fig_obv = make_subplots(
    rows=3,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "bar"}], [{"type": "scatter"}]]
)
fig_obv.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_obv.add_trace(
    go.Bar(
        x=data.index,
        y=data['Volume'],
        name='Volume'
    ),
    row=2, col=1,
)
fig_obv.add_trace(
    go.Scatter(
        x=data.index[-len(obv):],
        y=obv,
        name='OBV',
    ),
    row=3, col=1,
)
fig_obv.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_obv.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='On Balance Volume',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_obv.write_image('assets/obv.png', height=800, width=1600)

# Commodity Channel Index

weekly_cci = bulk_momentum_indicators.commodity_channel_index(data['Typical Price'].tolist(), 5, 'ema', 'median')
monthly_cci = bulk_momentum_indicators.commodity_channel_index(data['Typical Price'].tolist(), 20, 'ema', 'median')
quarterly_cci = bulk_momentum_indicators.commodity_channel_index(data['Typical Price'].tolist(), 60, 'ema', 'median')
# print(weekly_cci)
weekly_cci.append(single_momentum_indicators.commodity_channel_index(data['Typical Price'][-4:].tolist() + [latest_typical_price], 'ema', 'median'))
monthly_cci.append(single_momentum_indicators.commodity_channel_index(data['Typical Price'][-19:].tolist() + [latest_typical_price], 'ema', 'median'))
quarterly_cci.append(single_momentum_indicators.commodity_channel_index(data['Typical Price'][-59:].tolist() + [latest_typical_price], 'ema', 'median'))

fig_cci = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_cci.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_cci.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_cci):],
        y=weekly_cci,
        name='Weekly CCI',
        line={'color': '#FFE4C4'}
    ),
    row=2, col=1,
)
fig_cci.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_cci):],
        y=monthly_cci,
        name='Monhtly CCI',
        line={'color': '#E9967A'}
    ),
    row=2, col=1,
)
fig_cci.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_cci):],
        y=quarterly_cci,
        name='Quarterly CCI',
        line={'color': '#FF7F50'}
    ),
    row=2, col=1,
)
fig_cci.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_cci.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Commodity Channel Index',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_cci.write_image('assets/cci.png', height=800, width=1600)

# Trend Indicators
# Aroon Oscillator

aroon_up = bulk_trend_indicators.aroon_up(data['High'].tolist())
aroon_down = bulk_trend_indicators.aroon_down(data['Low'].tolist())
aroon_oscillator = bulk_trend_indicators.aroon_oscillator(data['High'].tolist(), data['Low'].tolist())
# print(aroon_oscillator)
aroon_up.append(single_trend_indicators.aroon_up(data['High'][-26:].tolist() + [latest_high]))
aroon_down.append(single_trend_indicators.aroon_down(data['Low'][-26:].tolist() + [latest_low]))
aroon_oscillator.append(single_trend_indicators.aroon_oscillator(data['High'][-26:].tolist() + [latest_high], data['Low'][-26:].tolist() + [latest_low]))

fig_ar = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_ar.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_ar.add_trace(
    go.Scatter(
        x=data.index[-len(aroon_up):],
        y=aroon_up,
        name='Aroon Up',
        line={'color': 'green'}
    ),
    row=2, col=1,
)
fig_ar.add_trace(
    go.Scatter(
        x=data.index[-len(aroon_down):],
        y=aroon_down,
        name='Aroon Down',
        line={'color': 'red'}
    ),
    row=2, col=1,
)
fig_ar.add_trace(
    go.Scatter(
        x=data.index[-len(aroon_oscillator):],
        y=aroon_oscillator,
        name='Aroon Oscillator',
        line={'color': 'blue'}
    ),
    row=2, col=1,
)
fig_ar.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_ar.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Aroon Oscillator',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_ar.write_image('assets/aroon_oscillator.png', height=800, width=1600)

# Personalised Aroon Oscillator
weekly_aroon_up = bulk_trend_indicators.aroon_up(data['High'].tolist(), 5)
weekly_aroon_down = bulk_trend_indicators.aroon_down(data['Low'].tolist(), 5)
weekly_aroon_oscillator = bulk_trend_indicators.aroon_oscillator(data['High'].tolist(), data['Low'].tolist(), 5)
# print(weekly_aroon_up)
weekly_aroon_up.append(single_trend_indicators.aroon_up(data['High'][-6:].tolist() + [latest_high], 5))
weekly_aroon_down.append(single_trend_indicators.aroon_down(data['Low'][-6:].tolist() + [latest_low], 5))
weekly_aroon_oscillator.append(single_trend_indicators.aroon_oscillator(data['High'][-6:].tolist() + [latest_high], data['Low'][-6:].tolist() + [latest_low], 5))

fig_war = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_war.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_war.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_aroon_up):],
        y=weekly_aroon_up,
        name='Aroon Up',
        line={'color': 'green'}
    ),
    row=2, col=1,
)
fig_war.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_aroon_down):],
        y=weekly_aroon_down,
        name='Aroon Down',
        line={'color': 'red'}
    ),
    row=2, col=1,
)
fig_war.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_aroon_oscillator):],
        y=weekly_aroon_oscillator,
        name='Aroon Oscillator',
        line={'color': 'blue'}
    ),
    row=2, col=1,
)
fig_war.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_war.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Weekly Aroon Oscillator',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_war.write_image('assets/weekly_aroon_oscillator.png', height=800, width=1600)

monthly_aroon_up = bulk_trend_indicators.aroon_up(data['High'].tolist(), 20)
monthly_aroon_down = bulk_trend_indicators.aroon_down(data['Low'].tolist(), 20)
monthly_aroon_oscillator = bulk_trend_indicators.aroon_oscillator(data['High'].tolist(), data['Low'].tolist(), 20)

monthly_aroon_up.append(single_trend_indicators.aroon_up(data['High'][-21:].tolist() + [latest_high], 20))
monthly_aroon_down.append(single_trend_indicators.aroon_down(data['Low'][-21:].tolist() + [latest_low], 20))
monthly_aroon_oscillator.append(single_trend_indicators.aroon_oscillator(data['High'][-21:].tolist() + [latest_high], data['Low'][-21:].tolist() + [latest_low], 20))

fig_mar = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_mar.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_mar.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_aroon_up):],
        y=monthly_aroon_up,
        name='Aroon Up',
        line={'color': 'green'}
    ),
    row=2, col=1,
)
fig_mar.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_aroon_down):],
        y=monthly_aroon_down,
        name='Aroon Down',
        line={'color': 'red'}
    ),
    row=2, col=1,
)
fig_mar.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_aroon_oscillator):],
        y=monthly_aroon_oscillator,
        name='Aroon Oscillator',
        line={'color': 'blue'}
    ),
    row=2, col=1,
)
fig_mar.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_mar.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Monthly Aroon Oscillator',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_mar.write_image('assets/monthly_aroon_oscillator.png', height=800, width=1600)

quarterly_aroon_up = bulk_trend_indicators.aroon_up(data['High'].tolist(), 60)
quarterly_aroon_down = bulk_trend_indicators.aroon_down(data['Low'].tolist(), 60)
quarterly_aroon_oscillator = bulk_trend_indicators.aroon_oscillator(data['High'].tolist(), data['Low'].tolist(), 60)

quarterly_aroon_up.append(single_trend_indicators.aroon_up(data['High'][-61:].tolist() + [latest_high], 60))
quarterly_aroon_down.append(single_trend_indicators.aroon_down(data['Low'][-61:].tolist() + [latest_low], 60))
quarterly_aroon_oscillator.append(single_trend_indicators.aroon_oscillator(data['High'][-61:].tolist() + [latest_high], data['Low'][-61:].tolist() + [latest_low], 60))

fig_qar = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_qar.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_qar.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_aroon_up):],
        y=quarterly_aroon_up,
        name='Aroon Up',
        line={'color': 'green'}
    ),
    row=2, col=1,
)
fig_qar.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_aroon_down):],
        y=quarterly_aroon_down,
        name='Aroon Down',
        line={'color': 'red'}
    ),
    row=2, col=1,
)
fig_qar.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_aroon_oscillator):],
        y=quarterly_aroon_oscillator,
        name='Aroon Oscillator',
        line={'color': 'blue'}
    ),
    row=2, col=1,
)
fig_qar.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_qar.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Quarterly Aroon Oscillator',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_qar.write_image('assets/quarterly_aroon_oscillator.png', height=800, width=1600)

# Parabolic Stop and Reverse

weekly_parabolic_sar = bulk_trend_indicators.parabolic_sar(data['High'].tolist(), data['Low'].tolist(), data['Close'].tolist(), 5)
monthly_parabolic_sar = bulk_trend_indicators.parabolic_sar(data['High'].tolist(), data['Low'].tolist(), data['Close'].tolist(), 20)
quarterly_parabolic_sar = bulk_trend_indicators.parabolic_sar(data['High'].tolist(), data['Low'].tolist(), data['Close'].tolist(), 60)

weekly_parabolic_sar.append(single_trend_indicators.parabolic_sar(
    data['High'][-4:].tolist() + [latest_high],
    data['Low'][-4:].tolist() + [latest_low],
    data['Close'][-4:].tolist() + [latest_close],
    weekly_parabolic_sar[-1][0],
    weekly_parabolic_sar[-1][1],
    weekly_parabolic_sar[-1][2],
    weekly_parabolic_sar[-1][3],
))
monthly_parabolic_sar.append(single_trend_indicators.parabolic_sar(
    data['High'][-19:].tolist() + [latest_high],
    data['Low'][-19:].tolist() + [latest_low],
    data['Close'][-19:].tolist() + [latest_close],
    monthly_parabolic_sar[-1][0],
    monthly_parabolic_sar[-1][1],
    monthly_parabolic_sar[-1][2],
    monthly_parabolic_sar[-1][3],
))
quarterly_parabolic_sar.append(single_trend_indicators.parabolic_sar(
    data['High'][-59:].tolist() + [latest_high],
    data['Low'][-59:].tolist() + [latest_low],
    data['Close'][-59:].tolist() + [latest_close],
    quarterly_parabolic_sar[-1][0],
    quarterly_parabolic_sar[-1][1],
    quarterly_parabolic_sar[-1][2],
    quarterly_parabolic_sar[-1][3],
))

weekly_psar_points = [i[0] for i in weekly_parabolic_sar]
monthly_psar_points = [i[0] for i in monthly_parabolic_sar]
quarterly_psar_points = [i[0] for i in quarterly_parabolic_sar]

fig_psar = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_psar.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_psar.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_psar_points):],
        y=weekly_psar_points,
        name='Weekly Parabolic SaR',
        line={'color': '#FFE4C4'},
        mode='markers'
    ),
    row=1, col=1,
)
fig_psar.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_psar_points):],
        y=monthly_psar_points,
        name='Monhtly Parabolic SaR',
        line={'color': '#E9967A'},
        mode='markers'
    ),
    row=1, col=1,
)
fig_psar.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_psar_points):],
        y=quarterly_psar_points,
        name='Quarterly Parabolic SaR',
        line={'color': '#FF7F50'},
        mode='markers'
    ),
    row=1, col=1,
)
fig_psar.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_psar.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Parabolic Stop and Reverse',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_psar.write_image('assets/psar.png', height=800, width=1600)

# Candle Indicators
# Bollinger Bands
bollinger_bands = bulk_candle_indicators.bollinger_bands(data['Typical Price'].tolist())
# print(bollinger_bands)
bollinger_bands.append(single_candle_indicators.bollinger_bands(data['Typical Price'][-19:].tolist() + [latest_typical_price]))

lower_band = [i[0] for i in bollinger_bands]
upper_band = [i[1] for i in bollinger_bands]
# moving_average = [i[2] for i in bolinger_bands]
fig_bband = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_bband.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_bband.add_trace(
    go.Scatter(
        x=data.index[-len(lower_band):],
        y=lower_band,
        name='Lower Band',
        line={'color': 'green'}
    ),
    row=1, col=1,
)
fig_bband.add_trace(
    go.Scatter(
        x=data.index[-len(upper_band):],
        y=upper_band,
        name='Upper Band',
        line={'color': 'red'}
    ),
    row=1, col=1,
)
# fig_bband.add_trace(
#     go.Scatter(
#         x=data.index[-len(quarterly_psar_points):],
#         y=quarterly_psar_points,
#         name='Quarterly Parabolic SaR',
#         line={'color': '#FF7F50'},
#         mode='markers'
#     ),
#     row=1, col=1,
# )
fig_bband.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_bband.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Bollinger Bands',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_bband.write_image('assets/bband.png', height=800, width=1600)

# Personalised Bollinger Bands

weekly_bband = bulk_candle_indicators.bollinger_bands(data['Typical Price'].tolist(), 5, 'ema', 2)
monthly_bband = bulk_candle_indicators.bollinger_bands(data['Typical Price'].tolist(), 20, 'ema', 2)
quarterly_bband = bulk_candle_indicators.bollinger_bands(data['Typical Price'].tolist(), 60, 'ema', 2)

# print(weekly_bband)

weekly_bband.append(single_candle_indicators.bollinger_bands(
    data['Typical Price'][-4:].tolist() + [latest_typical_price],
    'ema',
    2
))

weekly_lower_band = [i[0] for i in weekly_bband]
weekly_upper_band = [i[1] for i in weekly_bband]
# moving_average = [i[2] for i in bolinger_bands]
fig_wbband = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_wbband.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_wbband.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_lower_band):],
        y=weekly_lower_band,
        name='Lower Band',
        line={'color': 'green'}
    ),
    row=1, col=1,
)
fig_wbband.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_upper_band):],
        y=weekly_upper_band,
        name='Upper Band',
        line={'color': 'red'}
    ),
    row=1, col=1,
)
# fig_bband.add_trace(
#     go.Scatter(
#         x=data.index[-len(quarterly_psar_points):],
#         y=quarterly_psar_points,
#         name='Quarterly Parabolic SaR',
#         line={'color': '#FF7F50'},
#         mode='markers'
#     ),
#     row=1, col=1,
# )
fig_wbband.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_wbband.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Weekly Bollinger Bands',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_wbband.write_image('assets/weekly_bband.png', height=800, width=1600)

monthly_bband.append(single_candle_indicators.bollinger_bands(
    data['Typical Price'][-19:].tolist() + [latest_typical_price],
    'ema',
    2
))

monthly_lower_band = [i[0] for i in monthly_bband]
monthly_upper_band = [i[1] for i in monthly_bband]
# moving_average = [i[2] for i in monthly_bband]
fig_mbband = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_mbband.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_mbband.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_lower_band):],
        y=monthly_lower_band,
        name='Lower Band',
        line={'color': 'green'}
    ),
    row=1, col=1,
)
fig_mbband.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_upper_band):],
        y=monthly_upper_band,
        name='Upper Band',
        line={'color': 'red'}
    ),
    row=1, col=1,
)
# fig_bband.add_trace(
#     go.Scatter(
#         x=data.index[-len(quarterly_psar_points):],
#         y=quarterly_psar_points,
#         name='Quarterly Parabolic SaR',
#         line={'color': '#FF7F50'},
#         mode='markers'
#     ),
#     row=1, col=1,
# )
fig_mbband.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_mbband.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Monthly Bollinger Bands',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_mbband.write_image('assets/monthly_bband.png', height=800, width=1600)

quarterly_bband.append(single_candle_indicators.bollinger_bands(
    data['Typical Price'][-59:].tolist() + [latest_typical_price],
    'ema',
    2
))

quarterly_lower_band = [i[0] for i in quarterly_bband]
quarterly_upper_band = [i[1] for i in quarterly_bband]
# moving_average = [i[2] for i in quarterly_bband]
fig_mbband = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_mbband.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_mbband.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_lower_band):],
        y=quarterly_lower_band,
        name='Lower Band',
        line={'color': 'green'}
    ),
    row=1, col=1,
)
fig_mbband.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_upper_band):],
        y=quarterly_upper_band,
        name='Upper Band',
        line={'color': 'red'}
    ),
    row=1, col=1,
)
# fig_bband.add_trace(
#     go.Scatter(
#         x=data.index[-len(quarterly_psar_points):],
#         y=quarterly_psar_points,
#         name='Quarterly Parabolic SaR',
#         line={'color': '#FF7F50'},
#         mode='markers'
#     ),
#     row=1, col=1,
# )
fig_mbband.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_mbband.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Quarterly Bollinger Bands',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_mbband.write_image('assets/quarterly_bband.png', height=800, width=1600)

# Ichimoku Cloud
ichimoku_cloud = bulk_candle_indicators.ichimoku_cloud(data['High'].tolist(), data['Low'].tolist(), data['Close'].tolist())
# print(ichimoku_cloud)
ichimoku_cloud.append(single_candle_indicators.ichimoku_cloud(
    data['High'][-59:].tolist() + [latest_high],
    data['Low'][-59:].tolist() + [latest_low],
    data['Close'][-59:].tolist() + [latest_close]
))

icloud_span_a = [i[0] for i in ichimoku_cloud]
icloud_span_b = [i[1] for i in ichimoku_cloud]
icloud_base_line = [i[2] for i in ichimoku_cloud]
icloud_conversion_line = [i[3] for i in ichimoku_cloud]
icloud_lagged_price = [i[4] for i in ichimoku_cloud]

fig_icloud = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_icloud.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_icloud.add_trace(
    go.Scatter(
        x=data.index[-len(icloud_span_a):],
        y=icloud_span_a,
        name='Span A',
        line={'color': 'green'}
    ),
    row=1, col=1,
)
fig_icloud.add_trace(
    go.Scatter(
        x=data.index[-len(icloud_span_b):],
        y=icloud_span_b,
        name='Span B',
        line={'color': 'red'}
    ),
    row=1, col=1,
)
fig_icloud.add_trace(
    go.Scatter(
        x=data.index[-len(icloud_base_line):],
        y=icloud_base_line,
        name='Base Line',
        line={'color': 'lightgreen'}
    ),
    row=1, col=1,
)
fig_icloud.add_trace(
    go.Scatter(
        x=data.index[-len(icloud_conversion_line):],
        y=icloud_conversion_line,
        name='Conversion Line',
        line={'color': 'lightsalmon'}
    ),
    row=1, col=1,
)
fig_icloud.add_trace(
    go.Scatter(
        x=data.index[-len(icloud_lagged_price):],
        y=icloud_lagged_price,
        name='Lagged Price',
        line={'color': 'blue'}
    ),
    row=1, col=1,
)
fig_icloud.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_icloud.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Ichimoku Cloud',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_icloud.write_image('assets/icloud.png', height=800, width=1600)

# Personalised Ichimoku Cloud

personalised_ichimoku_cloud = bulk_candle_indicators.ichimoku_cloud(data['High'].tolist(), data['Low'].tolist(), data['Close'].tolist(), 5, 20, 60)

# print(personalised_ichimoku_cloud)

personalised_ichimoku_cloud.append(single_candle_indicators.ichimoku_cloud(
    data['High'][-60:].tolist() + [latest_high],
    data['Low'][-60:].tolist() + [latest_low],
    data['Close'][-60:].tolist() + [latest_close],
    5, 20, 60
))

picloud_span_a = [i[0] for i in personalised_ichimoku_cloud]
picloud_span_b = [i[1] for i in personalised_ichimoku_cloud]
picloud_base_line = [i[2] for i in personalised_ichimoku_cloud]
picloud_conversion_line = [i[3] for i in personalised_ichimoku_cloud]
picloud_lagged_price = [i[4] for i in personalised_ichimoku_cloud]

fig_picloud = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_picloud.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_picloud.add_trace(
    go.Scatter(
        x=data.index[-len(picloud_span_a):],
        y=picloud_span_a,
        name='Span A',
        line={'color': 'green'}
    ),
    row=1, col=1,
)
fig_picloud.add_trace(
    go.Scatter(
        x=data.index[-len(picloud_span_b):],
        y=picloud_span_b,
        name='Span B',
        line={'color': 'red'}
    ),
    row=1, col=1,
)
fig_picloud.add_trace(
    go.Scatter(
        x=data.index[-len(picloud_base_line):],
        y=picloud_base_line,
        name='Base Line',
        line={'color': 'lightgreen'}
    ),
    row=1, col=1,
)
fig_picloud.add_trace(
    go.Scatter(
        x=data.index[-len(picloud_conversion_line):],
        y=picloud_conversion_line,
        name='Conversion Line',
        line={'color': 'lightsalmon'}
    ),
    row=1, col=1,
)
fig_picloud.add_trace(
    go.Scatter(
        x=data.index[-len(picloud_lagged_price):],
        y=picloud_lagged_price,
        name='Lagged Price',
        line={'color': 'blue'}
    ),
    row=1, col=1,
)
fig_picloud.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_picloud.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Personalised Ichimoku Cloud',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_picloud.write_image('assets/picloud.png', height=800, width=1600)


# Volatility
# Average True Range
# TODO: the close price needs to be shifted one as it should be t-1 close
weekly_atr = bulk_volatility_indicators.average_true_range(
    data['High'].tolist(),
    data['Low'].tolist(),
    data['Close'].tolist(),
    5
)
monthly_atr = bulk_volatility_indicators.average_true_range(
    data['High'].tolist(),
    data['Low'].tolist(),
    data['Close'].tolist(),
    20
)
quarterly_atr = bulk_volatility_indicators.average_true_range(
    data['High'].tolist(),
    data['Low'].tolist(),
    data['Close'].tolist(),
    60
)
# print(weekly_atr)
weekly_atr.append(single_volatility_indicators.average_true_range(latest_high, latest_low, data['Close'].iloc[-1], weekly_atr[-1], 5))
monthly_atr.append(single_volatility_indicators.average_true_range(latest_high, latest_low, data['Close'].iloc[-1], weekly_atr[-1], 20))
quarterly_atr.append(single_volatility_indicators.average_true_range(latest_high, latest_low, data['Close'].iloc[-1], weekly_atr[-1], 60))

fig_atr = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_atr.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_atr.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_atr):],
        y=weekly_atr,
        name='Weekly ATR',
        line={'color': '#FFE4C4'}
    ),
    row=2, col=1,
)
fig_atr.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_atr):],
        y=monthly_atr,
        name='Monthly ATR',
        line={'color': '#E9967A'}
    ),
    row=2, col=1,
)
fig_atr.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_atr):],
        y=quarterly_atr,
        name='Quarterly ATR',
        line={'color': '#FF7F50'}
    ),
    row=2, col=1,
)
fig_atr.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_atr.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Average True Range',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_atr.write_image('assets/atr.png', height=800, width=1600)

# Ulcer Index
weekly_ui = bulk_volatility_indicators.ulcer_index(data['Close'].tolist(), 5)
monthly_ui = bulk_volatility_indicators.ulcer_index(data['Close'].tolist(), 20)
quarterly_ui = bulk_volatility_indicators.ulcer_index(data['Close'].tolist(), 60)
#print(weekly_ui)
weekly_ui.append(data['Close'][-4:].tolist() + [latest_close])
monthly_ui.append(data['Close'][-19:].tolist() + [latest_close])
quarterly_ui.append(data['Close'][-59:].tolist() + [latest_close])

fig_ui = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_ui.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_ui.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_ui):],
        y=weekly_ui,
        name='Weekly UI',
        line={'color': '#FFE4C4'}
    ),
    row=2, col=1,
)
fig_ui.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_ui):],
        y=monthly_ui,
        name='Monthly UI',
        line={'color': '#E9967A'}
    ),
    row=2, col=1,
)
fig_ui.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_ui):],
        y=quarterly_ui,
        name='Quarterly UI',
        line={'color': '#FF7F50'}
    ),
    row=2, col=1,
)
fig_ui.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_ui.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Ulcer Index',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_ui.write_image('assets/ui.png', height=800, width=1600)

# Welles Volatility Index
# TODO: Go to book to get better description, the internet has very little
weekly_vi = bulk_volatility_indicators.volatility_index(
    data['High'].tolist(),
    data['Low'].tolist(),
    data['Close'].tolist(),
    5
)
monthly_vi = bulk_volatility_indicators.volatility_index(
    data['High'].tolist(),
    data['Low'].tolist(),
    data['Close'].tolist(),
    20
)
quarterly_vi = bulk_volatility_indicators.volatility_index(
    data['High'].tolist(),
    data['Low'].tolist(),
    data['Close'].tolist(),
    60
)
# print(weekly_vi)
weekly_vi.append(single_volatility_indicators.volatility_index(
    latest_high,
    latest_low,
    latest_close,
    5,
    weekly_vi[-1]
))
monthly_vi.append(single_volatility_indicators.volatility_index(
    latest_high,
    latest_low,
    latest_close,
    20,
    monthly_vi[-1]
))
quarterly_vi.append(single_volatility_indicators.volatility_index(
    latest_high,
    latest_low,
    latest_close,
    60,
    quarterly_vi[-1]
))

fig_vi = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_vi.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_vi.add_trace(
    go.Scatter(
        x=data.index[-len(weekly_vi):],
        y=weekly_vi,
        name='Weekly VI',
        line={'color': '#FFE4C4'}
    ),
    row=2, col=1,
)
fig_vi.add_trace(
    go.Scatter(
        x=data.index[-len(monthly_vi):],
        y=monthly_vi,
        name='Monthly VI',
        line={'color': '#E9967A'}
    ),
    row=2, col=1,
)
fig_vi.add_trace(
    go.Scatter(
        x=data.index[-len(quarterly_vi):],
        y=quarterly_vi,
        name='Quarterly VI',
        line={'color': '#FF7F50'}
    ),
    row=2, col=1,
)
fig_vi.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_vi.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Volatility Index',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_vi.write_image('assets/vi.png', height=800, width=1600)

# Welles Volatility System
weekly_vs = bulk_volatility_indicators.volatility_system(
    data['High'].tolist(),
    data['Low'].tolist(),
    data['Close'].tolist(),
    5,
    2
)
monthly_vs = bulk_volatility_indicators.volatility_system(
    data['High'].tolist(),
    data['Low'].tolist(),
    data['Close'].tolist(),
    20,
    2
)
quarterly_vs = bulk_volatility_indicators.volatility_system(
    data['High'].tolist(),
    data['Low'].tolist(),
    data['Close'].tolist(),
    60,
    2
)

# print(weekly_vs)

weekly_vs.append(single_volatility_indicators.volatility_system(
    data['High'][-4:].tolist() + [latest_high],
    data['Low'][-4:].tolist() + [latest_low],
    data['Close'][-4:].tolist() + [latest_close],
    5,
    2,
    weekly_vs[-1]
))
monthly_vs.append(single_volatility_indicators.volatility_system(
    data['High'][-19:].tolist() + [latest_high],
    data['Low'][-19:].tolist() + [latest_low],
    data['Close'][-19:].tolist() + [latest_close],
    20,
    2,
    monthly_vs[-1]
))
quarterly_vs.append(single_volatility_indicators.volatility_system(
    data['High'][-59:].tolist() + [latest_high],
    data['Low'][-59:].tolist() + [latest_low],
    data['Close'][-59:].tolist() + [latest_close],
    60,
    2,
    quarterly_vs[-1]
))
#
# fig_vs = make_subplots(
#     rows=2,
#     cols=1,
#     specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
# )
# fig_vs.add_trace(
#     go.Candlestick(
#         x=data.index,
#         open=data['Open'],
#         low=data['Low'],
#         high=data['High'],
#         close=data['Close'],
#         name='S&P 500'
#     ),
#     row=1, col=1
# )
# fig_vs.add_trace(
#     go.Scatter(
#         x=data.index[-len(weekly_vs):],
#         y=weekly_vs,
#         name='Weekly VS',
#         line={'color': '#FFE4C4'}
#     ),
#     row=2, col=1,
# )
# fig_vs.add_trace(
#     go.Scatter(
#         x=data.index[-len(monthly_vs):],
#         y=monthly_vs,
#         name='Monthly VS',
#         line={'color': '#E9967A'}
#     ),
#     row=2, col=1,
# )
# fig_vs.add_trace(
#     go.Scatter(
#         x=data.index[-len(quarterly_vs):],
#         y=quarterly_vs,
#         name='Quarterly VS',
#         line={'color': '#FF7F50'}
#     ),
#     row=2, col=1,
# )
# fig_vs.update_xaxes(ticks="outside",
#               ticklabelmode="period",
#               tickcolor="white",
#               ticklen=10,
#               minor=dict(
#                  ticklen=5,
#                  dtick=7 * 24 * 60 * 60 * 1000,
#                  tick0=data.index[-1],
#                  griddash='dot',
#                  gridcolor='grey'),
#               rangebreaks=[
#                   {'bounds': ['sat', 'mon']},
#                   {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
#                           ],
#               showline=True,
#               linecolor='white',
#               gridcolor='lightpink',
# )
# fig_vs.update_layout(
#             xaxis_rangeslider_visible=False,
#             template='plotly_dark',
#             showlegend=True,
#             margin={
#                 'r': 50,
#                 't': 100,
#                 'b': 50,
#                 'l': 50
#             },
#             title_text='Volatility System',
#             title_font_family="Times New Roman",
#             title_font_color='white',
#             title_font_size=36,
#             font={
#                 'family': "Times New Roman",
#                 'color': 'white',
#                 'size': 18
#             },
#         )
# fig_vs.write_image('assets/vs.png', height=800, width=1600)

# Correlation
# Correlate asset prices
data2 = pandas.read_csv("example2.csv", sep=',', index_col=0, parse_dates=True)
data2.index.name = 'Date'
data2['Typical Price'] = (data['High'] + data['Low'] + data['Close']) / 3
data2.sort_index(inplace=True)
weekly_correlation = bulk_correlation_indicators.correlate_asset_prices(data['Typical Price'].tolist(), data2['Typical Price'].tolist(), 5)
monthly_correlation = bulk_correlation_indicators.correlate_asset_prices(data['Typical Price'].tolist(), data2['Typical Price'].tolist(), 20)
quarterly_correlation = bulk_correlation_indicators.correlate_asset_prices(data['Typical Price'].tolist(), data2['Typical Price'].tolist(), 60)
# print(correlation)
weekly_correlation.append(single_correlation_indicators.correlate_asset_prices(
    data['Typical Price'][-4:].tolist() + [latest_typical_price],
    data2['Typical Price'][-4:].tolist() + [52]
))
monthly_correlation.append(single_correlation_indicators.correlate_asset_prices(
    data['Typical Price'][-19:].tolist() + [latest_typical_price],
    data2['Typical Price'][-19:].tolist() + [52]
))
quarterly_correlation.append(single_correlation_indicators.correlate_asset_prices(
    data['Typical Price'][-59:].tolist() + [latest_typical_price],
    data2['Typical Price'][-59:].tolist() + [52]
))
fig_corr = make_subplots(
    rows=5,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "candlestick"}], [{"type": "bar"}], [{"type": "bar"}], [{"type": "bar"}]]
)
fig_corr.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500',
    ),
    row=1, col=1
)
fig_corr.add_trace(
    go.Candlestick(
        x=data2.index,
        open=data2['Open'],
        low=data2['Low'],
        high=data2['High'],
        close=data2['Close'],
        name='Dow Jones',
    ),
    row=2, col=1
)
fig_corr.add_trace(
    go.Bar(
        x=data.index[-len(weekly_correlation):],
        y=weekly_correlation,
        name='Weekly Correlation'
    ),
    row=3, col=1,
)
fig_corr.add_trace(
    go.Bar(
        x=data.index[-len(monthly_correlation):],
        y=monthly_correlation,
        name='Weekly Correlation'
    ),
    row=4, col=1,
)
fig_corr.add_trace(
    go.Bar(
        x=data.index[-len(quarterly_correlation):],
        y=quarterly_correlation,
        name='Weekly Correlation'
    ),
    row=5, col=1,
)
fig_corr.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_corr.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Correlation',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_corr.write_image('assets/correlation.png', height=1600, width=1600)

# Support and resistance indicators
# Pivot points
pivot_points = bulk_support_resistance_indicators.pivot_points(data['High'].tolist(), data['Low'].tolist(), data['Close'].tolist())
# print(pivot_points)
pivot_points.append(single_support_resistance_indicators.pivot_points(latest_high, latest_low, latest_close))

fig_pivot = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_pivot.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_pivot.add_trace(
    go.Scatter(
        x=data.index[-len(pivot_points):],
        y=[pivot_points[-1][0] for i in pivot_points],
        name='Pivot point'
    ),
    row=1, col=1,
)
fig_pivot.add_trace(
    go.Scatter(
        x=data.index[-len(pivot_points):],
        y=[pivot_points[-1][1] for i in pivot_points],
        name='Primary support'
    ),
    row=1, col=1,
)
fig_pivot.add_trace(
    go.Scatter(
        x=data.index[-len(pivot_points):],
        y=[pivot_points[-1][2] for i in pivot_points],
        name='Primary resistance'
    ),
    row=1, col=1,
)
fig_pivot.add_trace(
    go.Scatter(
        x=data.index[-len(pivot_points):],
        y=[pivot_points[-1][3] for i in pivot_points],
        name='Secondary support'
    ),
    row=1, col=1,
)
fig_pivot.add_trace(
    go.Scatter(
        x=data.index[-len(pivot_points):],
        y=[pivot_points[-1][4] for i in pivot_points],
        name='Secondary resistance'
    ),
    row=1, col=1,
)
fig_pivot.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_pivot.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Pivot points',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_pivot.write_image('assets/pivot_points.png', height=800, width=1600)

# Other indicators
# Value added index
value_added_index = bulk_other_indicators.value_added_index(data['Typical Price'].tolist())
# print(value_added_index)
value_added_index.append(single_other_indicators.value_added_index(data['Typical Price'].iloc[-1], latest_typical_price, value_added_index[-1]))

fig_vai = make_subplots(
    rows=2,
    cols=1,
    specs=[[{"type": "candlestick"}], [{"type": "scatter"}]]
)
fig_vai.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_vai.add_trace(
    go.Scatter(
        x=data.index[-len(value_added_index):],
        y=value_added_index,
        name='Value Added Index'
    ),
    row=2, col=1,
)
fig_vai.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_vai.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Value Added Index',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_vai.write_image('assets/value_added_index.png', height=800, width=1600)

# Chart Patterns
# Get peaks
weekly_peaks = peaks.get_peaks(data['High'].tolist() + [latest_high], 5)
monthly_peaks = peaks.get_peaks(data['High'].tolist() + [latest_high], 20)
quarterly_peaks = peaks.get_peaks(data['High'].tolist() + [latest_high], 60)
# print(weekly_peaks)

fig_peaks = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_peaks.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_peaks.add_trace(
    go.Scatter(
        x=[data.index[i[1]] for i in weekly_peaks],
        y=[i[0] for i in weekly_peaks],
        name='Weekly Peaks',
        line={'color': '#FFE4C4'},
        mode='markers'
    ),
    row=1, col=1,
)
fig_peaks.add_trace(
    go.Scatter(
        x=[data.index[i[1]] for i in monthly_peaks],
        y=[i[0] for i in monthly_peaks],
        name='Monthly Peaks',
        line={'color': '#E9967A'},
        mode='markers'
    ),
    row=1, col=1,
)
fig_peaks.add_trace(
    go.Scatter(
        x=[data.index[i[1]] for i in quarterly_peaks],
        y=[i[0] for i in quarterly_peaks],
        name='Quarterly Peaks',
        line={'color': '#FF7F50'},
        mode='markers'
    ),
    row=1, col=1,
)
fig_peaks.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_peaks.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Peaks',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_peaks.write_image('assets/peaks.png', height=800, width=1600)

# Valleys
# Get Valleys
weekly_valleys = valleys.get_valleys(data['Low'].tolist() + [latest_low], 5)
monthly_valleys = valleys.get_valleys(data['Low'].tolist() + [latest_low], 20)
quarterly_valleys = valleys.get_valleys(data['Low'].tolist() + [latest_low], 60)
# print(weekly_valleys)
fig_valleys = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_valleys.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_valleys.add_trace(
    go.Scatter(
        x=[data.index[i[1]] for i in weekly_valleys],
        y=[i[0] for i in weekly_valleys],
        name='Weekly Valleys',
        line={'color': '#FFE4C4'},
        mode='markers'
    ),
    row=1, col=1,
)
fig_valleys.add_trace(
    go.Scatter(
        x=[data.index[i[1]] for i in monthly_valleys],
        y=[i[0] for i in monthly_valleys],
        name='Monthly Valleys',
        line={'color': '#E9967A'},
        mode='markers'
    ),
    row=1, col=1,
)
fig_valleys.add_trace(
    go.Scatter(
        x=[data.index[i[1]] for i in quarterly_valleys],
        y=[i[0] for i in quarterly_valleys],
        name='Quarterly Valleys',
        line={'color': '#FF7F50'},
        mode='markers'
    ),
    row=1, col=1,
)
fig_valleys.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_valleys.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Valleys',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_valleys.write_image('assets/valleys.png', height=800, width=1600)

# Chart Trends
# Get Peak Trend
weekly_peak_trend = chart_trends.get_peak_trend(data['High'].tolist() + [latest_high], 5)
monthly_peak_trend = chart_trends.get_peak_trend(data['High'].tolist() + [latest_high], 20)
quarterly_peak_trend = chart_trends.get_peak_trend(data['High'].tolist() + [latest_high], 60)
# print(weekly_peak_trend)
weekly_peak_points = [(i*weekly_peak_trend[0]) + weekly_peak_trend[1] for i in range(0, len(data['High'])+1)]
monthly_peak_points = [(i*monthly_peak_trend[0]) + monthly_peak_trend[1] for i in range(0, len(data['High'])+1)]
quarterly_peak_points = [(i*quarterly_peak_trend[0]) + quarterly_peak_trend[1] for i in range(0, len(data['High'])+1)]
fig_ptrend = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_ptrend.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_ptrend.add_trace(
    go.Scatter(
        x=data.index,
        y=weekly_peak_points,
        name='Weekly Trend',
        line={'color': '#FFE4C4'}
    ),
    row=1, col=1,
)
fig_ptrend.add_trace(
    go.Scatter(
        x=data.index,
        y=monthly_peak_points,
        name='Monthly Trend',
        line={'color': '#E9967A'}
    ),
    row=1, col=1,
)
fig_ptrend.add_trace(
    go.Scatter(
        x=data.index,
        y=quarterly_peak_points,
        name='Quarterly Trend',
        line={'color': '#FF7F50'}
    ),
    row=1, col=1,
)
fig_ptrend.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_ptrend.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Peak Trend',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_ptrend.write_image('assets/peak_trend.png', height=800, width=1600)

# Get Valley Trend
weekly_valley_trend = chart_trends.get_valley_trend(data['Low'].tolist() + [latest_low], 5)
monthly_valley_trend = chart_trends.get_valley_trend(data['Low'].tolist() + [latest_low], 20)
quarterly_valley_trend = chart_trends.get_valley_trend(data['Low'].tolist() + [latest_low], 60)
# print(weekly_valley_trend)
weekly_valley_points = [(i*weekly_valley_trend[0]) + weekly_valley_trend[1] for i in range(0, len(data['Low'])+1)]
monthly_valley_points = [(i*monthly_valley_trend[0]) + monthly_valley_trend[1] for i in range(0, len(data['Low'])+1)]
quarterly_valley_points = [(i*quarterly_valley_trend[0]) + quarterly_valley_trend[1] for i in range(0, len(data['Low'])+1)]
fig_vtrend = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_vtrend.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_vtrend.add_trace(
    go.Scatter(
        x=data.index,
        y=weekly_valley_points,
        name='Weekly Trend',
        line={'color': '#FFE4C4'}

    ),
    row=1, col=1,
)
fig_vtrend.add_trace(
    go.Scatter(
        x=data.index,
        y=monthly_valley_points,
        name='Monthly Trend',
        line={'color': '#E9967A'}
    ),
    row=1, col=1,
)
fig_vtrend.add_trace(
    go.Scatter(
        x=data.index,
        y=quarterly_valley_points,
        name='Quarterly Trend',
        line={'color': '#FF7F50'}
    ),
    row=1, col=1,
)
fig_vtrend.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_vtrend.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Valley Trend',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_vtrend.write_image('assets/valley_trend.png', height=800, width=1600)

# Get overall trend
overall_trend = chart_trends.get_overall_trend(data['Typical Price'].tolist() + [latest_typical_price])
# print(overall_trend)
overall_trend_points = [(i*overall_trend[0]) + overall_trend[1] for i in range(0, len(data['Typical Price']))]
fig_otrend = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_otrend.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
fig_otrend.add_trace(
    go.Scatter(
        x=data.index,
        y=overall_trend_points,
        name='Overall Trend',
        line={'color': '#FFE4C4'}
    ),
    row=1, col=1,
)
fig_otrend.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_otrend.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Overall Trend',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_otrend.write_image('assets/overall_trend.png', height=800, width=1600)

# Break Down Trends
# TODO: There are more params that should be changed below or done in another graph (denominator param)
trends_low_sensitivity = chart_trends.break_down_trends(data['Typical Price'].tolist(), 1)

fig_bdtrend_low = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_bdtrend_low.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
date_index_list = data.index.tolist()
for i in trends_low_sensitivity:
    x_points = date_index_list[i[0]:i[1]+1]
    y_points = [(j*i[2]) + i[3] for j in range(i[0], i[1]+1)]
    fig_bdtrend_low.add_trace(
        go.Scatter(
            x=x_points,
            y=y_points,
            name='Trend'
        ),
        row=1, col=1,
    )
fig_bdtrend_low.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_bdtrend_low.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Overall Trend',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_bdtrend_low.write_image('assets/breakdown_trends_low_std.png', height=800, width=1600)

trends_default_sensitivity = chart_trends.break_down_trends(data['Typical Price'].tolist())
fig_bdtrend_default = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_bdtrend_default.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
for i in trends_default_sensitivity:
    x_points = date_index_list[i[0]:i[1]+1]
    y_points = [(j*i[2]) + i[3] for j in range(i[0], i[1]+1)]
    fig_bdtrend_default.add_trace(
        go.Scatter(
            x=x_points,
            y=y_points,
            name='Trend'
        ),
        row=1, col=1,
    )
fig_bdtrend_default.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_bdtrend_default.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Overall Trend',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_bdtrend_default.write_image('assets/breakdown_trends_default.png', height=800, width=1600)

trends_high_sensitivity = chart_trends.break_down_trends(data['Typical Price'].tolist(), 5)
fig_bdtrend_high = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_bdtrend_high.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
for i in trends_high_sensitivity:
    x_points = date_index_list[i[0]:i[1]+1]
    y_points = [(j*i[2]) + i[3] for j in range(i[0], i[1]+1)]
    fig_bdtrend_high.add_trace(
        go.Scatter(
            x=x_points,
            y=y_points,
            name='Trend'
        ),
        row=1, col=1,
    )
fig_bdtrend_high.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_bdtrend_high.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Overall Trend',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_bdtrend_high.write_image('assets/breakdown_trends_high_std.png', height=800, width=1600)

trends_low_denominator = chart_trends.break_down_trends(data['Typical Price'].tolist(), 2, 0.1)

fig_bdtrend_low_denom = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_bdtrend_low_denom.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
for i in trends_low_denominator:
    x_points = date_index_list[i[0]:i[1]+1]
    y_points = [(j*i[2]) + i[3] for j in range(i[0], i[1]+1)]
    fig_bdtrend_low_denom.add_trace(
        go.Scatter(
            x=x_points,
            y=y_points,
            name='Trend'
        ),
        row=1, col=1,
    )
fig_bdtrend_low_denom.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_bdtrend_low_denom.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Overall Trend',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_bdtrend_low_denom.write_image('assets/breakdown_trends_low_denom.png', height=800, width=1600)

trends_high_denom = chart_trends.break_down_trends(data['Typical Price'].tolist(), 2, 100)
fig_bdtrend_high_denom = make_subplots(
    rows=1,
    cols=1,
    specs=[[{"type": "candlestick"}]]
)
fig_bdtrend_high_denom.add_trace(
    go.Candlestick(
        x=data.index,
        open=data['Open'],
        low=data['Low'],
        high=data['High'],
        close=data['Close'],
        name='S&P 500'
    ),
    row=1, col=1
)
for i in trends_high_denom:
    x_points = date_index_list[i[0]:i[1]+1]
    y_points = [(j*i[2]) + i[3] for j in range(i[0], i[1]+1)]
    fig_bdtrend_high_denom.add_trace(
        go.Scatter(
            x=x_points,
            y=y_points,
            name='Trend'
        ),
        row=1, col=1,
    )
fig_bdtrend_high_denom.update_xaxes(ticks="outside",
              ticklabelmode="period",
              tickcolor="white",
              ticklen=10,
              minor=dict(
                 ticklen=5,
                 dtick=7 * 24 * 60 * 60 * 1000,
                 tick0=data.index[-1],
                 griddash='dot',
                 gridcolor='grey'),
              rangebreaks=[
                  {'bounds': ['sat', 'mon']},
                  {'values': ['2022-09-05', '2022-11-24', '2022-12-26', '2023-01-02', '2023-01-16', '2023-02-20', '2023-04-07', '2023-05-29', '2023-06-19', '2023-07-04', '2023-09-04']}
                          ],
              showline=True,
              linecolor='white',
              gridcolor='lightpink',
)
fig_bdtrend_high_denom.update_layout(
            xaxis_rangeslider_visible=False,
            template='plotly_dark',
            showlegend=True,
            margin={
                'r': 50,
                't': 100,
                'b': 50,
                'l': 50
            },
            title_text='Overall Trend',
            title_font_family="Times New Roman",
            title_font_color='white',
            title_font_size=36,
            font={
                'family': "Times New Roman",
                'color': 'white',
                'size': 18
            },
        )
fig_bdtrend_high_denom.write_image('assets/breakdown_trends_high_denom.png', height=800, width=1600)
