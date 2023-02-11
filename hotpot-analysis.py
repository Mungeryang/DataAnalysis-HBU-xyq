import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as mfm
import statsmodels.api as sm
import statsmodels.formula.api as smf



# raw_data = pd.read_excel("https://github.com/xiangyuchang/xiangyuchang.github.io/blob/master/BearData/shops_nm.xlsx?raw=true")
raw_data = pd.read_excel("E:\狗熊会数据科学实践\shops_nm.xlsx")
coupon_data = pd.read_excel("E:\狗熊会数据科学实践\coupon_nm.xlsx")
merge_data1 = pd.read_excel("E:\狗熊会数据科学实践\mergedata.xlsx")
print('数据的维度是:',raw_data.shape)

# print(raw_data.head())



# 判断是否存在完全一致的数据行
duplicated_data = raw_data[raw_data.duplicated()==True]
# if len(duplicated_data) == 0:
#     print("不存在完全一致的数据行")
# else:
#     print(duplicated_data)

# 判断是否有重复得点名
# duplicated_shop = raw_data['店名'][raw_data['店名'].duplicated()==True]
# if len(duplicated_shop)==0:
#     print('不存在')
# else:
#     print(duplicated_shop)

# 函数去重
drop_duplicated_shop = raw_data.drop_duplicates(subset=['店名'])
# print(drop_duplicated_shop.head)

# 单独打印某一列的内容
# print(raw_data['店名'])


# 关键的缺失值检查
is_null_data = raw_data[raw_data['评价数'].isnull()==True]
# print(is_null_data)

raw_data2 = raw_data[raw_data['评价数'].isnull()==False]
# print('数据的维度是:',raw_data2.shape)

# 一些简易小操作
print(raw_data2.columns)
# print(raw_data2.sort_values(['人均'],ascending=True))


# print(raw_data2['人均'])
# 发现人均列中并非完全都是数字；需要再次进行数据清洗
# def clean_data(x):
#     filter_words = ['人均：','人均','左右','差不多','大概']
#     if type(x) is int or type(x) is float:
#         return x
#     for word in filter_words:
#         value = raw_data2['人均'].iloc()
#         if word in value:
#             x = x.replace(word,'')
#     return x


# filter_words = ['人均：','人均','左右','差不多','大概']
# for i in range(len(raw_data2)):
#     value = raw_data2['人均'].iloc[i]
#     if type(value) is int or type(value) is float:
#         continue
#     for word in filter_words:
#         if word in value:
#             raw_data2.loc[i,'人均'] = raw_data2.loc[i,'人均'].replace(word,'')
#
# print(raw_data2['人均'])

# 把没有评价团购，购买人数为0的团购去除
coupon_data = coupon_data[coupon_data['团购评价']!='暂无评价'][coupon_data['评价人数']!='暂无评价']
coupon_data = coupon_data[coupon_data['购买人数']!=0]
coupon_data = coupon_data.dropna()
# print(coupon_data.head(5))

# 分组聚合
filter_coupon_data = coupon_data.groupby('店名').agg({
    '团购价':'mean',
    '购买人数':'mean'
})
# print(filter_coupon_data.head(10))

filter_coupon_data['店名']=filter_coupon_data.index
# 重新编号
filter_coupon_data.index = list(range(len(filter_coupon_data)))
filter_coupon_data.head(10)
# print(filter_coupon_data.head(10))

# 表格合并
merge_data = pd.merge(left=raw_data2,right=filter_coupon_data,on='店名',how='inner')

merge_data['购买人数'] = merge_data['购买人数'].astype(int)
# print(merge_data.shape)
#
# print(merge_data.head(10))

# merge_data.to_csv('合并表.csv',index=False)
# merge_data.to_excel('mergedata.xlsx',index=False)



font_path = r"E:\狗熊会数据科学实践\SimHei.ttf"
prop = mfm.FontProperties(fname=font_path)



# 散点图、线图
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.set_title('购买人数-评价数关系图',fontproperties=prop,fontsize=20)
ax1.set_xlabel('购买人数',fontproperties=prop,fontsize=15)
ax1.set_ylabel('评级数',fontproperties=prop,fontsize=15)
ax1.scatter(y=merge_data['评价数'],x=merge_data['购买人数'],color='r',marker='v')

ax1.set_xlim((0,3000))
ax1.set_ylim((0,3000))
#警告
# ax1.set_xticklabels(labels=[i for i in range(1,10,1)],fontproperties=prop,fontsize=15)
# ax1.set_yticklabels(labels=[i for i in range(500,7000,1000)],fontproperties=prop,fontsize=15)

ax1.hlines(2000,20,60,colors="r",linestyles="dashed")
#
# x = [i for i in range(3000)]
x = np.arange(3000)
y = [i for i in range(3000)]
#
ax1.plot(x,y,color='black')
plt.show()
plt.close()


#plotly美化箱线图

d1 = merge_data1['评价数'][merge_data1['购买人数']<500]
d2 = merge_data1['评价数'][merge_data1['购买人数']>=500][merge_data1['购买人数']<1000]
d3 = merge_data1['评价数'][merge_data1['购买人数']>=1000][merge_data1['购买人数']<1500]
d4 = merge_data1['评价数'][merge_data1['购买人数']>=1500][merge_data1['购买人数']<2000]
ys = [d1,d2,d3,d4]
xs = [1,2,3,4]
# 构造4个RGB颜色
# colors = ['hsl('+str(h)+',50%'+',50%)'for h in np.linspace(0,360,4)]

# num_cols = ['评分','评价数','购买人数','团购价']
# model_data = merge_data1.loc[:,num_cols]
# corr_matrix = np.corrcoef(model_data.loc[:,num_cols])
# smg.plot_corr(corr_matrix,xnames=num_cols)
# plt.show()

# print(merge_data1['购买人数'])

fig1,ax = plt.subplots()
x1 = np.linspace(-5,2,100)
y1 = x**3 + 5*x**2 + 10
y2 = 3*x**2 + 10*x
y3 = 6*x + 10

ax.plot(x,y1,color="blue",label="y(x)")
ax.plot(x,y2,color="red",label="y'(x)")
ax.plot(x,y2,color="green",label="y''(x)")

ax.set_xlabel("x")
ax.set_ylabel("y")

# plt.show()
# plt.close()

# 子图的嵌套
fig2,axes = plt.subplots(2,2,figsize=(6,6),sharex=True,sharey=True,squeeze=False)

x11 = np.random.randn(100)
x12 = np.random.randn(100)

axes[0,0].set_title("Uncorrelated")
axes[0,0].scatter(x11,x12)

axes[0,1].set_title("Weakly positive correlated")
axes[0,1].scatter(x11,x11+x12)

axes[1,0].set_title("Weakly negative correlated")
axes[1,0].scatter(x11,-x11+x12)

axes[1,1].set_title("Strongly correlated")
axes[1,1].scatter(x11,x11+0.15*x12)

axes[1,1].set_xlabel("x")
axes[1,0].set_xlabel("x")
axes[1,0].set_ylabel("y")
axes[0,0].set_ylabel("y")

plt.subplots_adjust(left=0.1,right=0.95,bottom=0.1,top=0.95,wspace=0.1,hspace=0.2)
# plt.show()
# plt.close()

# 差值
x21 = np.array([0,1,2,3,4,5,6,7])
y21 = np.array([3,4,3.5,2,1,1.5,1.25,0.9])
xx = np.linspace(x21.min(),x21.max(),100)
fig,ax2 = plt.subplots(figsize=(8,4))

ax2.scatter(x21,y21)
# for n in [1,2,3,5]:
#     f = interpolate.interp1d(x21,y21,kind=n)
#     ax2.plot(xx,f(xx),label='order %d'% n)
#     ax2.set_xlabel(r"$x$",fontsize=18)
#     ax2.set_ylabel(r"$y$",fontsize=18)
# plt.show()
# plt.close()




