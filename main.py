import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import asyncio

df = pd.DataFrame( pd.read_csv("stock_data.csv"))
df['date'] = pd.to_datetime(df['<DATE>'].astype(str), format="%Y%m%d")
df = df.drop(['<TICKER>','<PER>','<DATE>','<TIME>','<OPEN>','<HIGH>','<LOW>','<VOL>'], axis=1)
df.set_index(['date'], inplace=True)
df.columns = ['close']
df.dropna(inplace=True, axis=0)
df['change'] = df.close.pct_change()*100
df.dropna(inplace=True, axis=0)
print(df)
print(' ')

analysis = df.describe()
print('За все время')
print(analysis)
print(' ')

six_months = df[-120:].describe()
print('Предыдущие пол года')
print(six_months)
print(' ')

one_months = df[-30:].describe()
print('Предыдущий месяц')
print(six_months)
print(' ')

async def inex_percent_day():
    # график процентного изменения цены закрытия день ко дню
    plt.plot(df.index, df.change)
    plt.grid(linestyle='--')
    plt.yticks(np.arange(round(min(df.change)-1, 0), max(df.change)+1, 1))
    plt.show()

async def chart_profit_day():
    # колво прибыльных/убыточных закрытий день ко дню
    df['direction'] = df.change.apply(lambda x: "+" if x > 0 else "-")
    plt.pie(df.direction.value_counts(), labels=df.direction.value_counts().index, autopct="%.1f%%")
    plt.show()

async def histogram_profit_day():
    # гистограмма распределения ежедневных доходов
    sns.set_theme(style='darkgrid')
    fig, axs = plt.subplots()
    sns.histplot(data=df['change'], kde=True, color="orange", ax=axs)
    axs.set_xlim(-10,10)
    plt.show()

async def charts():
    task1 = asyncio.create_task(inex_percent_day())
    task2 = asyncio.create_task(chart_profit_day())
    task3 = asyncio.create_task(histogram_profit_day())

    await task1
    await task2
    await task3

asyncio.run(charts())
