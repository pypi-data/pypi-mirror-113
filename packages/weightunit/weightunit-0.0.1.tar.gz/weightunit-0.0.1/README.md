# 项目介绍
## 工单地址
http://pm.moojing.com/issues/38063
## 内容介绍
将奶制品加奶制品分类的数据与sku级详单数据进行合并，提取出不同分类的奶制品数据。在奶制品数据上根据标题，skuname,
属性等信息提取有效信息，增加标签列。如奶制品杀菌方式，是否高钙等。其中工作量最大的部分为通过标题和skuname提取商品
重量。
## 对接人
### 上游数据提供者：储鹏
### 文件时间范围： 2020年1月至2021年5月
### 文件提供方式： csv文件路径
    * sku加奶制品分类标签数据：
    path = "/share/home/chupeng/adopt_a_cow/sku/my_data/"
    path1 = '/share/home/chupeng/adopt_a_cow/sku/my_data/2021_05/'
    * sku详单数据
        "/share/new/share/tmp/taobao/cid/123222007/item_attr_sku_123222007_2020_01_2021_05.csv",
        "/share/new/share/tmp/taobao/cid/201284105/item_attr_sku_201284105_2020_01_2021_05.csv",
        "/share/new/share/tmp/taobao/cid/50008431/item_attr_sku_50008431_2020_01_2021_05.csv",
        "/share/new/share/tmp/taobao/cid/50016427/item_attr_sku_50016427_2020_01_2021_05.csv",
        "/share/new/share/tmp/taobao/cid/50010422/item_attr_sku_50010422_2020_01_2021_05.csv",
        "/share/new/share/tmp/taobao/cid/50016094/item_attr_sku_50016094_2020_01_2021_05.csv",
        "/share/new/share/tmp/taobao/cid/211104/item_attr_sku_211104_2020_01_2021_05.csv",
        "/share/new/share/tmp/taobao/cid/201228111/item_attr_sku_201228111_2020_01_2021_05.csv",
        "/share/new/share/tmp/taobao/cid/50018184/item_attr_sku_50018184_2020_01_2021_05.csv",
        "/share/new/share/tmp/taobao/cid/200670003/item_attr_sku_200670003_2020_01_2021_05.csv",
        "/share/new/share/tmp/taobao/cid/50012391/item_attr_sku_50012391_2020_01_2021_05.csv",
        "/share/new/share/tmp/taobao/cid/50012392/item_attr_sku_50012392_2020_01_2021_05.csv"

### 下游对接人：阳澜（行业分析师）
### 文件时间范围：2020年1月至2021年5月
### 文件提供方式：csv文件路径
    /data/zhangwenhui/奶酪_label_v3.csv   奶酪
    /data/zhangwenhui/成人奶粉_label_v4.csv 成人奶粉
    /data/zhangwenhui/lt_yogurt_v4.csv 低温酸奶
    /data/zs/lt_milk_3.csv   低温纯牛奶 
    /data/zhangwenhui/df_milk_zs_v4.csv
### 文件内容描述
    sku详单信息 ：时间；类目信息，销售信息：价格，销量，销售额，商品描述信息：属性，标题，skuname，所属类目，1-4级，叶子类目，商品ID，skuid等；;
    店铺信息：店铺名，店铺地址
    加标签信息 ：口味，是否高蛋白，是否高钙等，商品总重量，商品百克单价，所属聚类品牌名
## 处理流程
    1.将sku加label信息与sku详单信息合并（按照item_id和时间进行merge)
    2.增加标签（口味，是否高蛋白，是否高钙，所属类型等）
    3。提取重量信息
    4.增加聚合品牌，修改部分品牌名
## notebook 链接
    获取全部未加标签的合并数据:1_认养一头牛_获取各个类目未加标签数据.ipynb
    纯牛奶：
    低温牛奶：
    低温酸奶：
    常温酸奶：
    奶粉：
    奶酪：
    