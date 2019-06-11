
import pandas as pd
import numpy as py
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['font.family']='sans-serif'
import seaborn as sns
import re

# 一、读入数据
data_user = pd.read_csv(r'E:/python/data/user_behavior_analysis/tianchi_mobile_recommend_train_user1.csv')
#print(data_user.shape)

# 二、数据预处理
# 2.1缺失值审查
missingTotal = data_user.isnull().sum()
missingExist = missingTotal[missingTotal>0]
missingExist = missingExist.sort_values(ascending=False)
#print(missingTotal)

# 2.2数据拆分及类型转化
# 将time列分割为年月日和小时
data_user['date'] = data_user['time'].map(lambda s:re.compile(' ').split(s)[0])
data_user['hour'] = data_user['time'].map(lambda s:re.compile(' ').split(s)[1])
#print(data_user.head())

# 数据类型转化
#print(data_user.dtypes)
data_user['time'] = pd.to_datetime(data_user['time'])
data_user['date'] = pd.to_datetime(data_user['date'])
data_user['hour'] = data_user['hour'].astype('int64')
#print(data_user.dtypes)

# 2.3异常值审查
data_user = data_user.sort_values(by='time',ascending=True)#排序处理
data_user = data_user.reset_index(drop=True)#建立索引
#print(data_user.describe())

# 三、用户行为分析
# (一)pv和uv分析
# 3.1.1日访问量分析
'''pv_daily = data_user.groupby('date')['user_id'].count().reset_index().rename(columns={'user_id':'pv'})
uv_daily = data_user.groupby('date')['user_id'].apply(lambda x:x.drop_duplicates().count()).reset_index().rename(columns={'user_id':'uv'})
fig,axes = plt.subplots(2,1,sharex=True)
pv_daily.plot(x='date',y='pv',ax=axes[0])
uv_daily.plot(x='date',y='uv',ax=axes[1])
axes[0].set_title('pv_daily')
axes[1].set_title('uv_daily')

# 3.1.2小时访问量分析
pv_hour = data_user.groupby('hour')['user_id'].count().reset_index().rename(columns={'user_id':'pv'})
uv_hour = data_user.groupby('hour')['user_id'].apply(lambda x:x.drop_duplicates().count()).reset_index().rename(columns={'user_id':'uv'})
fig,axes = plt.subplots(2,1,sharex=True)
pv_hour.plot(x='hour',y='pv',ax=axes[0])
uv_hour.plot(x='hour',y='uv',ax=axes[1])
axes[0].set_title('pv_hour')
axes[1].set_title('uv_hour')'''

# (二)转化率
# 3.2.1收藏转化率:添加收藏的用户数/总访问数
'''data_user['operation']=1
data_use_buy2 = data_user.groupby(['date','behavior_type'])['operation'].count().\
              reset_index().rename(columns={'operation':'total'})
data_use_buy2.groupby('date').apply(lambda x:x[x.behavior_type==2].total.sum()/x[x.behavior_type==1].total.sum()).plot()
plt.title('收藏转化率')
plt.show()

# 3.2.2添加转化率:添加购物车的用户数/总访问数
data_use_buy2 = data_user.groupby(['date','behavior_type'])['operation'].count().\
              reset_index().rename(columns={'operation':'total'})
data_use_buy2.groupby('date').apply(lambda x:x[x.behavior_type==3].total.sum()/x[x.behavior_type==1].total.sum()).plot()
plt.title('添加购物车转化率')
plt.show()
# 3.2.3成交转化率:成交用户数/总访问数
data_use_buy2 = data_user.groupby(['date','behavior_type'])['operation'].count().\
              reset_index().rename(columns={'operation':'total'})
data_use_buy2.groupby('date').apply(lambda x:x[x.behavior_type==4].total.sum()/x[x.behavior_type==1].total.sum()).plot()
plt.title('成交转化率')
plt.show()

# （三）复购率
date_rebuy=data_user[data_user.behavior_type==4].groupby('user_id')['date'].apply(lambda x:len(x.unique())).rename('rebuy_count')
print('复购率:',round(date_rebuy[date_rebuy>=2].count()/date_rebuy.count(),4))
plt.show()
# 多数用户复购次数
sns.distplot(date_rebuy-1,kde=False)
plt.title('rebuy_user')
print('多数用户复购次数：{}次'.format((date_rebuy-1).mode()[0]))
plt.show()'''

#（四）漏斗分析-流失率
data_user_count = data_user.groupby('behavior_type')['behavior_type'].count()
pv_all = data_user['user_id'].count()
print(data_user_count)
print("总浏览量:",pv_all)
print('总浏览量—点击量 流失率: {:.2f}'.format((pv_all-502835)/pv_all))
print("点击量-加入购物车量 流失率:{:.2f}".format((502835-10756)/502835))
print("加入购物车量-收藏量 流失率:{:.2f}".format((10756-14896)/10756))
print("收藏量-购买量 流失率:{:.2f}".format((14896-5195)/14896))

from pyecharts import Funnel
funnel = Funnel("漏斗分析", width=600, height=400, title_pos='center')
funnel.add("用户行为数据", ['点击','收藏','加入购物车','支付'],[502835,10756,14896,5195], is_label_show=True,label_formatter='{b} {c}',label_pos="outside",legend_orient='vertical', legend_pos='left')
funnel.render('E:/python/data/user_behavior_analysis_tb/data.html')

# （五）用户价值度分析
from datetime import datetime
datenow = datetime(2014,12,20)
# 计算每位用户最近购买时间
recent_buy_time = data_user[data_user.behavior_type==4].groupby('user_id')\
                 .date.apply(lambda x:datetime(2014,12,20)-x.sort_values().iloc[-1])\
                 .reset_index().rename(columns={'date':'recent'})
recent_buy_time.recent = recent_buy_time.recent.map(lambda x:x.days)
# 计算每位用户消费频率
buy_freq = data_user[data_user.behavior_type==4].groupby('user_id').date.count().\
         reset_index().rename(columns={'date':'freq'})
# 将最近购买时间和消费频率合并在一起
rfm = pd.merge(recent_buy_time,buy_freq,left_on='user_id',right_on='user_id',how='outer')
# 将各维度分成3级,得数越高越好
rfm['recent_value'] = pd.cut(rfm.recent,3,labels=['3','2','1'])
rfm['freq_value'] = pd.cut(rfm.freq,3,labels=['1','2','3'])
rfm['rfm'] = rfm['recent_value'].str.cat(rfm['freq_value'])
rfm.to_csv('E:/python/data/user_behavior_analysis/rfm.csv')

