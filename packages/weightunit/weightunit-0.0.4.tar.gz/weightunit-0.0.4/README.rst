

******
介绍
******
解析字符串中的重量单位，并进行简单的计算，主要在淘宝的商品标题中做了测试

**************
一些使用例子
**************

.. code:: python

    from weightunit import parse_str, UnitLevel

    # 乘法情况, 将升转化为毫升
    mu = parse_str("德国进口德亚全脂纯牛奶1L*12盒整箱营养早餐奶学生儿童老人")
    print(mu)
    print((mu.start_index, mu.end_index))
    print(mu.calc_weight())# 计算单位，并转换为ml
    print("---------------------")

    # 有加法的情况
    mu = parse_str("简醇0蔗糖250g*1瓶+开啡尔草莓味200g*5瓶")
    print(mu)
    print((mu.start_index, mu.end_index))
    print(mu.calc_weight())
    print("---------------------")

    # 或的情况
    mu = parse_str("德国进口德亚全脂纯牛奶1L*12盒|24盒整箱营养早餐奶学生儿童老人")
    print(mu)
    print((mu.start_index, mu.end_index))
    print(mu.calc_weight())# 计算单位，并转换为ml
    print("---------------------")

    # 添加自定义的重量单位
    mu = parse_str("手拉葫芦吊机手动2吨倒链1吨10t小型5吨家用起重机3吨工业吊葫芦")
    print("未添加【吨】",mu)
    ul = UnitLevel.gen_default()
    ul.add_unit_word("吨", level=1)
    ul.add_unit_word("t", level=1)
    mu = parse_str("手拉葫芦吊机手动2吨倒链1吨10t小型5吨家用起重机3吨工业吊葫芦", unit_level=ul)
    print("添加【吨】",mu)
    print("---------------------")


    # 设置str_modifier函数，可以在真正解析前字符串前，删除一些字符，让长串的计算公式连一起
    def str_modifier(input_str):
    # 替代默认的str修改，不对input_str进行修改
    return input_str
    mu = parse_str("爱尔培 奶酪500g*6盒11月29到期", )
    print(mu)
    mu = parse_str("爱尔培 奶酪500g*6盒11月29到期", str_modifier=str_modifier)
    print(mu)
    print("---------------------")

    # 获得所有的段落，不强制合并到一个公式里
    mu_list = parse_str("3箱爱尔培 奶酪500g*6盒11月29到期", only_one=False)
    print(type(mu_list))
    print(mu_list)
    mu_list = parse_str("3箱爱尔培 奶酪500g*6盒11月29到期", only_one=True)
    print(type(mu_list))
    print(mu_list)
    print("---------------------")
