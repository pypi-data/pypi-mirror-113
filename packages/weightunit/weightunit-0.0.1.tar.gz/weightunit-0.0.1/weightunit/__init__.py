#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
# @Time : 2021/7/12 上午10:01
# @Author : wangchong
# @Email: chongwangcc@gmail.com
# @File : __init__.py
# @Software: PyCharm
'''

import re
import copy
from itertools import chain

DEBUG = True


class UnitLevel:
    """
    单位层级
    """

    def __init__(self, level1=None, level2=None, level3=None, special_unit=None):
        if special_unit is None:
            special_unit = {}
        if level3 is None:
            level3 = []
        if level1 is None:
            level1 = []
        if level2 is None:
            level2 = []
        self.level1 = level1
        self.level2 = level2
        self.level3 = level3
        self.special_unit = special_unit
        self.fix_unit_level()

    def fix_unit_level(self):
        level1 = sorted(self.level1, key=lambda i: len(i), reverse=True)
        level2 = sorted(self.level2, key=lambda i: len(i), reverse=True)
        level3 = sorted(self.level3, key=lambda i: len(i), reverse=True)
        special_unit = self.special_unit
        level1 = [l1 + "/" + l2 for l1 in level1 for l2 in level2] + ["/" + l for l in level1] + [" " + l for l in level1] + level1
        level2 = [l2 + "/" + l3 for l2 in level2 for l3 in level3] + ["/" + l for l in level2] + level2
        level3 = ["/" + l for l in level3] + level3
        new_dict = {}
        for k in special_unit:
            new_dict["/" + k] = special_unit[k]
            for l2 in level2:
                new_dict[k + "/" + l2] = special_unit[k]
        special_unit.update(new_dict)
        self.level1 = level1
        self.level2 = level2
        self.level3 = level3
        self.special_unit = special_unit

    def get_all_unit_name(self):
        self.unit_name = self.level1 + self.level2 + self.level3
        return self.unit_name

    def is_unit_char(self, i_char):
        if i_char in self.get_all_unit_name():
            return True
        else:
            return False

    def add_unit_word(self, word, level=1):
        """
        添加指定层级的level word
        :param word:
        :param level:
        :return:
        """
        if level == 1:
            if isinstance(word, list):
                self.level1.extend(word)
            else:
                self.level1.append(word)
            self.level1 = list(set(self.level1))
        elif level == 2:
            if isinstance(word, list):
                self.level2.extend(word)
            else:
                self.level2.append(word)
            self.level2 = list(set(self.level2))
        elif level == 3:
            if isinstance(word, list):
                self.level3.extend(word)
            else:
                self.level3.append(word)
            self.level3 = list(set(self.level3))

    def format_unit(self, unit):
        """
        格式单位字符串
        :param unit:
        :return:
        """
        if unit in self.special_unit:
            return 'g'
        return unit

    @staticmethod
    def gen_default():
        dict_special_unit = {"l": "*1000",
                             "升": "*1000",
                             'kg': '*1000',
                             '千克': '*1000',
                             '公斤': '*1000',
                             '斤': '*500'}
        level1 = ["ml", "g", "kg", "L", "l", "斤", "千克", "公斤", "克", "升", "毫升", "mg", '毫克']
        level2 = ["包", "袋", '片', '支', '礼盒装', '礼盒', "盒", '碗', "瓶", '听', "罐", "桶", "杯", "硬袋", "小袋", "个", '根']
        level3 = ['箱', '提', '件', "包", "天"]
        return UnitLevel(level1, level2, level3, dict_special_unit)


DEFAULT_LEVEL  = UnitLevel.gen_default()


class Operator:
    """
    操作符类，多个计量单位的是如何连接的计算的
    """

    op_dict = {
        "*": ["X", 'x', "×", "*"],  # 乘法
        "+": ["+", '加', '赠'],  # 加法
        "|": ["-", "或", "至"],  # 或 运算
    }

    def __init__(self, op, start=None, end=None):
        """

        :param op:
        :param start:
        :param end:
        """
        self.op = self.standardize_operator(op)
        self.start_index = start
        self.end_index = end
        self.org_op = op

    @classmethod
    def standardize_operator(cls, op_name):
        for k, v_list in cls.op_dict.items():
            if op_name in v_list or op_name == k:
                return k
        return None

    @classmethod
    def parser_from_str(cls, input_str):
        op_list = []
        op_pattern = r"({})".format("|".join([v if v not in ["*", "|", "+", "?", "\\", "-"] else "\\" + v
                                              for k, v1 in cls.op_dict.items()
                                              for v in v1]))
        match_obj_list = re.finditer(op_pattern, input_str)
        for match_obj in match_obj_list:
            i_s, i_e = match_obj.span()[0], match_obj.span()[1]
            op_str = input_str[i_s:i_e]
            op_list.append(Operator(op_str, i_s, i_e))
        return op_list

    @classmethod
    def is_char_op(cls, i_char):
        """
        判断字母是不是操作符
        :param i_char:
        :return:
        """
        if i_char is None:
            return False
        for k, v_list in cls.op_dict.items():
            if i_char in v_list:
                return True
        return False

    def __str__(self):
        return self.op

    def __repr__(self):
        s = "(op=" + str(self.op) + ","
        s += "start=" + str(self.start_index) + ","
        s += "end=" + str(self.end_index) + ")"
        return s


class SingleUnit:
    """
    表示单个的计量单位，例如200ml、1箱这种
    """

    unit_level = DEFAULT_LEVEL

    def __init__(self, number, unit, start_index=None, end_index=None, total=0):
        """
        :param number:
        :param unit:
        """
        self.number = number
        self.unit = unit
        self.start_index = start_index
        self.end_index = end_index
        self.level = self.infer_level()
        self.total_flag = total

    def infer_level(self):
        """
        推断这个计量单位的层级
        :return:
        """
        if self.unit in self.unit_level.level1:
            return 1
        elif self.unit in self.unit_level.level2:
            return 2
        elif self.unit in self.unit_level.level3:
            return 3
        else:
            return 0

    def __str__(self):
        return str(self.number) + str(self.unit)

    def __repr__(self):
        return "(number=" + self.number + \
               ", unit=" + self.unit + \
               ",level=" + str(self.level) + \
               ",total_flag=" + str(self.total_flag) + \
               ",start_index=" + str(self.start_index) + \
               ",end_index=" + str(self.end_index) + \
               ")"

    def is_same_unit_with_another(self, su, same_level=False, empty_unit=False):
        """
        判断两个singleunit的单位是否相同
        :param su:
        :param same_level: 是不是层级相同就认为是相同的单位了
        :return:
        """
        if su is None:
            return False

        if su.unit == self.unit and su.unit != '':
            return True
        if su.unit == self.unit and su.unit == '' and empty_unit:
            return True
        if same_level and self.level == su.level:
            return True
        return False

    @classmethod
    def parser_from_str(cls, input_str, first=True, su_filter=None, unit_level=None):
        """
        解析字符串来获得字符串
        :param first:
        :param input_str:
        :return:
        """

        if unit_level is None:
            unit_level = DEFAULT_LEVEL

        cls.unit_level = unit_level
        unit_name = unit_level.get_all_unit_name()
        pattern_str = r"[0-9]*\.?[0-9]+({})?".format("|".join(unit_name))
        match_obj_list = re.finditer(pattern_str, input_str)
        unit_list = []
        for match_obj in match_obj_list:
            i_s, i_e = match_obj.span()[0], match_obj.span()[1]
            match_str = input_str[i_s:i_e]
            unit_str = re.sub(r'([0-9]*\.?[0-9]+)', r' \1 ', match_str)
            unit_ll = unit_str.split(" ")
            unit_ll = [l for l in unit_ll if len(l) > 0] + ['']
            u = SingleUnit(unit_ll[0], unit_ll[1], i_s, i_e)
            if su_filter is None or su_filter(u, input_str):
                unit_list.append(u)

            # 判断 是不是 总共类的词语
            f_char ='' if i_s <=0 else input_str[i_s-1:i_s]
            f2_char ='' if i_s <=0 else input_str[i_s-2:i_s]
            if f_char in ["共"] or f2_char in ["≈ "] or match_str==input_str :
                u.total_flag = 1

        if len(unit_list) == 0:
            return []
        elif first:
            return unit_list[0]
        else:
            return unit_list


class MultiUnit:
    """
    表示多个计量单位连乘的结果,例如200ml*12袋
    """

    unit_level = DEFAULT_LEVEL

    def __init__(self, unit_list, fix_l1=True):
        """
        单计量单位的列表
        :param unit_list:
        """
        if len(unit_list) > 1 and isinstance(unit_list[-1], Operator):
            unit_list = unit_list[:-1]
        self.org_units = copy.deepcopy(unit_list)
        self.formula = self.formula_str()
        self.weight = self.calc_weight()

    def __len__(self):
        return len([u for u in self.org_units if isinstance(u, SingleUnit) or isinstance(u, MultiUnit)])

    def __str__(self):
        f_str = ""
        for u in self.org_units:
            if isinstance(u, SingleUnit):
                f_str += str(u)
            elif isinstance(u, Operator):
                f_str += str(u)
            elif isinstance(u, MultiUnit):
                f_str += "(" + str(u) + ")"
        return f_str

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, n):
        new_single_units = [n for n in self.org_units if isinstance(n, SingleUnit) or isinstance(n, MultiUnit)]
        return new_single_units[n]

    def __setitem__(self, key, value):
        i = 0
        new_units = []
        for su in self.org_units:
            if isinstance(su, SingleUnit):
                if i == key:
                    new_units.append(value)
                    continue
                i = i + 1
            new_units.append(su)
        self.org_units = new_units
        self.formula = self.formula_str()
        self.weight = self.calc_weight()

    @property
    def start_index(self):
        # 最小的那个start_index
        min_i = None
        for u in self.org_units:
            if min_i is None or(u.start_index is not None and min_i > u.start_index):
                min_i = u.start_index
        return min_i

    @property
    def end_index(self):
        max_i = None
        for u in self.org_units:
            if max_i is None or (u.end_index is not None and max_i < u.end_index):
                max_i = u.end_index
        return max_i

    @property
    def level(self):
        """
        取最大的level
        :return:
        """
        i = None
        for u in self.org_units:
            if not isinstance(u, Operator):
                if i is None or (u.level is not None and i < u.level):
                    i = u.level
        return i

    def is_contains(self, su):
        if isinstance(su, SingleUnit):
            return False
        for u in self.org_units:
            if isinstance(u, SingleUnit):
                if float(u.number) == float(su.number) and u.unit==su.unit and u.level == u.level:
                    return True
            elif isinstance(u, MultiUnit):
                b = u.is_contains(su)
                if b: return True
        return False

    def simple_formula(self):
        """
        简化公式
        :return:
        """
        # 如果只有一种单位，提前计算结果
        su = self.get_first_single_unit()
        if self.is_all_unit_same(su.unit):
            su.number = self.calc_weight()
            mu = MultiUnit([su])
            return mu
        # 不包含乘号，并且单位为空，或者空和某一种
        if not self.have_operator('*') :
            all_unit = list(set(self.get_all_unit()))
            try:
                all_unit.remove('')
            except:
                pass
            if len(all_unit) == 0 or len(all_unit)==1:
                su.number = self.calc_weight()
                mu = MultiUnit([su])
                return mu
        return self

    def add_same_unit(self, su, op):
        """
        将类目下项目的unit项目合并，如果没有的话不修改
        :param su:
        :param op:
        :return:
        """
        if isinstance(op, str):
            op = Operator(op)
        if isinstance(su, MultiUnit):
            if len(su) > 1:
                return False
            else:
                su = su.org_units[0]
        if not isinstance(su, SingleUnit):
            return False
        new_units = []
        found = False
        for t_u in self.org_units:
            if isinstance(t_u, SingleUnit):
                if su.is_same_unit_with_another(t_u, same_level=True) and op.op !='*' and not found:
                    t_mu = MultiUnit([t_u, op, su])
                    new_units.append(t_mu)
                    found = True
                else:
                    new_units.append(t_u)
            elif isinstance(t_u, Operator):
                new_units.append(t_u)
            elif isinstance(t_u, MultiUnit):
                if self.is_all_unit_same(unit_name=su.unit) and not found:
                    new_units.append(MultiUnit([*t_u.org_units, op, su]))
                    found = True
                else:
                    new_units.append(t_u)
        self.org_units = new_units
        return found

    def replace_same_unit(self, su, empty_same=False):
        """
        替换相同单位的值
        :param su:
        :return:
        """
        if isinstance(su, MultiUnit) and len(su) == 1:
            su = su.org_units[0]
        elif isinstance(su, MultiUnit) and su.is_all_unit_same(su.get_first_single_unit().unit):
            number = str(su.calc_weight())
            unit = self.unit_level.format_unit(su.get_first_single_unit().unit)
            su = SingleUnit(number, unit)
        if not isinstance(su, SingleUnit):
            return False
        new_units = []
        found = False
        for t_u in self.org_units:
            if isinstance(t_u, SingleUnit):
                if su.is_same_unit_with_another(t_u, True, empty_unit=empty_same):
                    found = True
                    new_units.append(su)
                else:
                    new_units.append(t_u)
            elif isinstance(t_u, Operator):
                new_units.append(t_u)
            elif isinstance(t_u, MultiUnit):
                if t_u.is_all_unit_same(t_u.get_first_single_unit().unit):
                    number = str(t_u.calc_weight())
                    unit = self.unit_level.format_unit(t_u.get_first_single_unit().unit)
                    t_u = MultiUnit([SingleUnit(number, unit)])
                if t_u.replace_same_unit(su, empty_same):
                    found = True
                new_units.append(t_u)
        self.org_units = new_units
        return found

    def get_first_single_unit(self):
        """
        获得第一个single_unit值
        :return:
        """
        for u in self.org_units:
            if isinstance(u, SingleUnit):
                return u
            elif isinstance(u, MultiUnit):
                return u.get_first_single_unit()
        return None

    def verify_unit_level(self, su):
        """
        检验公式中指定层级的是否正确
        :param su:  为共多少箱，共多少盒这类的词语, 一个single_unit类型
        :return:
        """
        if not isinstance(su, SingleUnit) :
            return False
        w = self.sum_level(su.level)
        if w == float(su.number):
            return True
        else:
            # TODO 要支持更多种1情况
            if self.have_operator('+'):
                return False
            else:
                # 只有乘法，没有其他操作符的话，替换
                su1 = self.get_all_level_1()
                if su1 is None or len(su1)==0:
                    return True
                if len(su1) == 1:
                    self.org_units = [su1[0], Operator('*'), su]
                else:
                    # TODO
                    result = []
                    for sss1 in su1:
                        result.append(MultiUnit([sss1, Operator('*'), su]))
                    self.org_units = list(chain.from_iterable(zip(result, [Operator('|')]*len(result))))[:-1]
        return False

    def append(self, single_unit, op='*', same_unit="append"):
        """
        :param single_unit:
        :param op:
        :param same_unit:
        :return:
        """
        if isinstance(single_unit, MultiUnit) and len(single_unit) == 1:
            single_unit = single_unit.org_units[0]
        if same_unit == "append":
            if len(self) > 0:
                self.org_units.append(Operator(op) if isinstance(op, str) else op)
            self.org_units.append(single_unit)
            return True
        elif same_unit == "merge":
            return self.add_same_unit(single_unit, op)
        elif same_unit == "replace":
            return self.replace_same_unit(single_unit)
        elif same_unit == "verify":
            return self.verify_unit_level(single_unit)
        # 忽略要添加的单位
        return False

    def calc_weight(self):
        """
        计算重量
        :return:
        """
        try:
            cal_units = [SingleUnit(u.calc_weight(), '') if isinstance(u, MultiUnit) else u for u in self.org_units]
            # cal_units应该不包含multi了
            # 如果只包含 或操作符，全部数值里取最大的
            # TODO 传入公式只支持全 或 的MultiUnit计算, 其它情况抛异常
            if self.have_operator("|"):
                max_number = max(
                    [float(cu.number) for cu in cal_units if isinstance(cu, SingleUnit) and cu is not None])
                return max_number
            else:
                return eval(self.formula_str(cal_units))
        except:
            return None

    def formula_str(self, units=None):
        """
        生成计算公式字符串
        :return:
        """
        # 1. 转换单位
        new_units = []
        if units is None:
            units = self.org_units
        for u in units:
            if isinstance(u, SingleUnit):
                if u.level == 1 and u.unit in self.unit_level.special_unit.keys():
                    new_u = SingleUnit(u.number + self.unit_level.special_unit[u.unit], '')
                    new_u.level = 1
                    new_units.append(new_u)
                    continue
            new_units.append(u)

        f_str = ""
        for u in new_units:
            if isinstance(u, SingleUnit):
                f_str += str(u.number)
            elif isinstance(u, Operator):
                f_str += str(u.op)
            elif isinstance(u, MultiUnit):
                f_str += "(" + str(u) + ")"
        return f_str

    def have_level(self, level=1):
        """
        判断是否有指定的层级单位
        :param level:
        :return:
        """
        for u in self.org_units:
            if isinstance(u, SingleUnit):
                if u.level == level:
                    return True
            elif isinstance(u, MultiUnit):
                if u.have_level(level):
                    return True
        return False

    def count_level(self, level=1):
        """
        判断不同level的数字有几个
        :param level:
        :return:
        """

        level_1 = []
        for u in self.org_units:
            if isinstance(u, SingleUnit):
                if u.level == level:
                    level_1.append(u)
        return len(level_1)

    def sum_level(self, level=2):
        """
        TODO 实际情况更复杂，需要更细致的判断
        计算某个level的单位求和
        :param level:
        :return:
        """
        # 复制一个一模一样的
        sub = MultiUnit(self.org_units)
        sub.replace_level_below(level)
        result = 0
        for u in self.org_units:
           if isinstance(u, SingleUnit):
               if u.level == level:
                   result += float(u.number)
        # return result
        return sub.calc_weight()

    def get_all_level_1(self):
        """
        获得说是有level1的值
        :return:
        """
        all_level1 = []
        for u in self.org_units:
            if isinstance(u, SingleUnit):
                if u.level == 1:
                    all_level1.append(u)
            elif isinstance(u, MultiUnit):
                ll = u.get_all_level_1()
                if ll is not None:
                    all_level1.extend(ll)
        return all_level1

    def replace_level_below(self, level=2):
        for u in self.org_units:
            if isinstance(u, SingleUnit):
                if u.level < level:
                    u.number = str(1)
                    u.unit = ''
            elif isinstance(u, MultiUnit):
                u.replace_level_below(level)

    def get_index_by_level(self, level=1):
        new_single_units = [n for n in self.org_units if isinstance(n, SingleUnit) or isinstance(n, MultiUnit)]
        for i, u in enumerate(new_single_units):
            if u.level == level:
                return i
        return None

    def have_special_unit(self, special_unit):
        """
        判断某个单位是否出现,spcial_unit是传入的一个列表
        :return:
        """
        for u in self.org_units:
            if isinstance(u, SingleUnit):
                if u.unit in special_unit:
                    return True
            elif isinstance(u, MultiUnit):
                if u.have_special_unit(special_unit):
                    return True
        return False

    def have_unit(self, unit_name):
        """
        是否有指定单位
        :param unit_name:
        :return:
        """
        return self.have_special_unit([unit_name])

    def is_all_unit_same(self, unit_name):
        """
        是不是所有的单位都是指定的名称
        :param unit_name:
        :return:
        """
        for v in self.org_units:
            if isinstance(v, SingleUnit):
                if v.unit != unit_name:
                    return False
            elif isinstance(v, MultiUnit):
                if not v.is_all_unit_same(unit_name):
                    return False
        return True

    def get_all_unit(self):
        all_unit = []
        for u in self.org_units:
            if isinstance(u, SingleUnit):
                all_unit.append(u.unit)
            elif isinstance(u, MultiUnit):
                rr = u.get_all_unit()
                all_unit.extend(rr)
        return all_unit

    def infer_unit_level(self):
        """
        推断单位层级，将level0的单位补全
        :return:
        """
        if self.have_level(0) and len(self) > 1:
            # 只对全是singleunit，并且是乘法的单位推断,
            if not any([isinstance(u, MultiUnit) for u in self.org_units]):
                ttt_list = []
                for ii, l in enumerate(self.org_units):
                    if (isinstance(l, Operator) and l.op != "*") or ii == len(self.org_units) - 1:
                        # 进行推断, 把对应的连乘片段找到了
                        if not isinstance(l, Operator):
                            ttt_list.append(l)
                        level = 0
                        # 排序，将ttt_list中level排到第一个元素
                        new_ll = []
                        for l in ttt_list:
                            if l.level == 1:
                                new_ll.insert(0, l)
                            else:
                                new_ll.append(l)
                        ttt_list = new_ll
                        # ttt_list.sort(key=lambda x:100 if x.level==0 else x.level)
                        for l in ttt_list:
                            if isinstance(l, SingleUnit):
                                if l.level == 0:
                                    if l.unit not in self.unit_level.level1:
                                        l.level = level
                                else:
                                    level = l.level + 1
                        # 如果还有level是0的，用后一个元素的level-1填补
                        for v1, v2 in zip(ttt_list[:-1], ttt_list[1:]):
                            if v1.level == 0 and v1.level!=0:
                                if l.unit not in self.unit_level.level1:
                                    v1.level = v2.level-1
                        # 如果还有level是0，并且第一个元素level是0，并且总元素大于1个，每个level+1
                        if ttt_list[0].level==0 and len(ttt_list) >1:
                            d_l = 1
                            for v1 in ttt_list:
                                if l.unit not in self.unit_level.level1:
                                    v1.level = d_l
                                d_l += 1
                        ttt_list = []
                    elif isinstance(l, MultiUnit):
                        #  暂时不支持 MultiUnit推断不会有这种情况
                        print("should not be here！")
                    elif isinstance(l, SingleUnit):
                        ttt_list.append(l)

    def have_operator(self, op_str="|"):
        """
        判断操作符是否存在
        :param op_str:
        :return:
        """
        for i, pp in enumerate(self.org_units):
            if isinstance(pp, Operator):
                if pp.op == op_str:
                    return True
        return False

    def get_fb_operator(self, op_str='+') -> (SingleUnit, SingleUnit):
        """
        获取加号前后的信息
        :param op_str:
        :return:
        """
        for i, pp in enumerate(self.org_units):
            if isinstance(pp, Operator):
                if pp.op == op_str:
                    p1 = self.org_units[i - 1]
                    p2 = self.org_units[i + 1]
                    return p1, p2
                else:
                    continue
        return None, None

    def replace_operator_ba(self, unit_single, op_str='+'):
        """
        将加号前后合并的single_unit替换原来的single_unit
        :param unit_single:
        :param op_str:
        :return:
        """
        i1 = None
        i2 = None
        for i, pp in enumerate(self.org_units):
            if isinstance(pp, Operator):
                if pp.op == op_str:
                    i1 = i - 1
                    i2 = i + 1
        if i1 is not None and i2 is not None:
            del self.org_units[i1:i2 + 1]
            self.org_units.insert(i1, unit_single)

    @staticmethod
    def have_op_between_two_single(su1, su2, op_list, distance=0):
        """
        两个single unit中间是否有操作符, 如果有的话，返回指定的操作符
        su1 在前，su2在后
        :param su1:
        :param su2:
        :param op_list:
        :param distance: 距离多远算是有操作符
        :return:
        """
        for op in op_list:
            if 0 <= op.start_index - su1.end_index <= distance \
                    and 0<= su2.start_index - op.end_index <= distance:
                return op
        return None

    @staticmethod
    def is_unit_existed(search_list, element: SingleUnit):
        """
        判断某个单位是否出现过，如有出现返回true,否则返回False
        :param search_list: [singleunit]
        :param element: singleunit类型
        :return:
        """
        for unit in search_list:
            if isinstance(unit, SingleUnit):
                if unit.unit == element.unit and element.unit != '':
                    return True
        return False

    @classmethod
    def replace_slash(cls, input_str):
        """
        替换反斜杠
        10/15盒 ——> 10or15盒
        180*10/15 ——> 180*10or15
        10/15 ——> 空
        2020/10/15 ——> 空
        10/15/20/30 ——> 10or15or20or30
        180/15 ——> 180*15
        :param input_str:
        :return:
        """
        final_str = input_str
        input_str = input_str + ' '
        unit_name = cls.unit_level.get_all_unit_name()
        # 将年月日类型的日期（xxxx/xx/xx)替换为空字符串
        # print('aaaaa',input_str)
        match_list = re.finditer(r"20[0-9]{2}\/[0-9]{1,2}\/[0-9]{1,2}", input_str)
        for match_obg in match_list:
            i0 = match_obg.span()[0]
            i1 = match_obg.span()[1]
            bb = input_str[i1]
            if not (bb == "/" or bb in unit_name):
                final_str = input_str[0:i0] + '$' * (i1 - i0) + input_str[i1:]
        # 将月日类型的日期（xx/xx)替换为空字符串
        input_str = ' ' + final_str + ' '
        match_list = re.finditer(r"[0-9]{1,4}\/[0-3][0-9]", input_str)
        for match_obg in match_list:
            i0, i1 = match_obg.span()
            bb = input_str[i1]
            aa = input_str[i0 - 1]
            # print(aa)
            if not (bb == "/" or bb in unit_name or aa == '/'):
                month_str, day_str = input_str[i0:i1].split(('/'))
                if 1 <= int(month_str) <= 12 and 1 <= int(day_str) <= 31:
                    final_str = input_str[0:i0] + '$' * (i1 - i0) + input_str[i1:]
                if 2010 <= int(month_str) < 2030 and 1 <= int(day_str) <= 12:
                    final_str = input_str[0:i0] + '$' * (i1 - i0) + input_str[i1:]
        final_str = final_str.replace("$", '')
        # 将180ml/12箱，的情况转为180*12
        pattern_str = r"[0-9]*\.?[0-9]+({})?(\/[0-9]*\.?[0-9]+({})?)".format("|".join(unit_name), "|".join(unit_name))
        pattern_str += "{1,2}"
        match_list = re.finditer(pattern_str, final_str)
        for match_obg in match_list:
            i0, i1 = match_obg.span()
            xx = final_str[i0:i1]
            xx_single = SingleUnit.parser_from_str(xx, first=False)
            f_str = xx.replace("/", '*')
            # print(f_str)
            if len(xx_single) == 3:
                if xx_single[0].level == 1 and xx_single[1].level == 2 and xx_single[2].level == 3:
                    final_str = final_str[:i0] + f_str + final_str[i1:]
            elif len(xx_single) == 2:
                if (xx_single[0].level == 1 and xx_single[1].level == 2) or (
                        xx_single[0].level == 2 and xx_single[1].level == 3):
                    # TODO
                    final_str = final_str[:i0] + f_str + final_str[i1:]
        # final_str = final_str.replace("/", '或')
        return final_str
        # final_str = re.sub(r"[0-9]{4}\/\d+\/\d+",'',input_str)

    @classmethod
    def parser_from_str(cls, input_str, unit_level, su_filter):
        """
        解析字符串，获得连乘结果
        :param input_str:
        :param first:
        :return:
        """
        if input_str is None:
            return None
        cls.unit_level = unit_level
        # 获得所有的total类别
        total_mu, input_str = cls.parser_total_format(input_str)
        if total_mu is not None and len(total_mu) > 0:
            return total_mu, []
        # 获得所有单计量的位置
        units_list = SingleUnit.parser_from_str(input_str, first=False, su_filter=su_filter, unit_level=unit_level)
        # 获得所有操作符的位置
        op_list = Operator.parser_from_str(input_str)
        if DEBUG: print("unit_list=", units_list, "\n", "op_list=", op_list)

        # 根据字符出现位置排序，并且把紧邻的两个合并
        result_list = total_mu
        temp_mu = None
        for s_u in units_list:
            if s_u.total_flag == 1 and s_u.level==1 and s_u.unit !='':
                result_list = [MultiUnit([s_u])]
                temp_mu = None
                break
            if temp_mu is None:
                temp_mu = MultiUnit([s_u])
                continue
            f_op = MultiUnit.have_op_between_two_single(temp_mu[-1], s_u, op_list)
            # 不要追加两个1级单位
            if f_op is not None and not (temp_mu.have_level(1) and s_u.level == 1 and f_op.op == '*'):
                if f_op.op == "+":
                    temp_mu.infer_unit_level()
                    if s_u.level > 1 and temp_mu.have_operator('*') and temp_mu.have_level(s_u.level):
                        temp_mu.append(s_u, op=f_op, same_unit="merge")
                        continue
                temp_mu.append(s_u, op=f_op, same_unit="append")
                op_list.remove(f_op)
            else:
                temp_mu.infer_unit_level()
                result_list.append(temp_mu)
                temp_mu = MultiUnit([s_u])
        if temp_mu is not None:
            temp_mu.infer_unit_level()
            result_list.append(temp_mu)
        if len(result_list) == 0:
            return None
        else:
            return result_list, op_list

    @classmethod
    def parser_total_format(cls, input_str):
        """
        解析共多少斤这种
        :param input_str:
        :param unit_level:
        :return:
        """
        pattern_str = "共(发)?[0-9]*\.?[0-9]+({})".format("|".join(cls.unit_level.level1))
        match_obj_list = re.finditer(pattern_str, input_str)
        new_str = input_str
        result_list = []
        for match_obj in match_obj_list:
            i_s, i_e = match_obj.span()[0], match_obj.span()[1]
            match_str = input_str[i_s:i_e]
            new_str = new_str.replace(match_str, "")
            su = SingleUnit.parser_from_str(match_str, unit_level=cls.unit_level)
            mu = MultiUnit([su])
            result_list.append(mu)
        return result_list, new_str

    @classmethod
    def mu_from_list(cls, su_list, op="|", input_str=''):
        """
        通过一个single 列表来 生成新的mu， su_list至少两个元素
        :param su_list:
        :param op:
        :return:
        """
        if su_list is None:
            return None
        elif len(su_list) == 1:
            return su_list[0]
        else:
            op_list = Operator.parser_from_str(input_str)
            fill_op_list = [Operator(op)] * len(su_list)
            for i,(su1, su2 ) in enumerate(zip(su_list[:-1:], su_list[1::])):
                t_op = MultiUnit.have_op_between_two_single(su1, su2, op_list, 20)
                if t_op:
                    fill_op_list[i] = t_op
            unit_list = list(chain.from_iterable(zip(su_list, fill_op_list)))[:-1]
            return MultiUnit(unit_list)


def default_str_modifier(input_str):
    """
    过滤字符串中的干扰数字
    :param title:
    :return:
    """
    input_str = str(input_str).lower()
    input_str = re.sub(' +', ' ', input_str)  # 连续空格变单个空格
    # input_str = re.sub("\/   ", r"*\1", input_str) # 替换处理不了的/15这种
    input_str = re.sub(r"\d+\-\d+", '', input_str)
    input_str = re.sub(r"\d+-+\d+-+\d+", '', input_str)
    input_str = re.sub(r"\d+\.+\d+\.+\d+", '', input_str)
    input_str = re.sub(r"\d+月\d+号", '', input_str)
    input_str = re.sub(r"\d+月\d+日", '', input_str)
    input_str = re.sub(r"\d+年\d+号", '', input_str)
    input_str = re.sub(r"\d+月", '', input_str)
    input_str = re.sub(r"\d+个月", '', input_str)
    input_str = re.sub(r"\d+到期", '', input_str)
    input_str = re.sub(r"\d{2,4}年", '', input_str)
    input_str = re.sub(r"入会加购", '', input_str)
    input_str = re.sub(r"\d+日", '', input_str)
    input_str = re.sub(r"\d+件", '', input_str)
    input_str = re.sub(r"\d+岁", '', input_str)
    input_str = re.sub(r"\d+种", '', input_str)
    input_str = re.sub(r"\d+只", '', input_str)
    #---------------
    # input_str = re.sub(r"\d+支", '', input_str)
    # input_str = re.sub(r"\d+片", '', input_str)
    # input_str = re.sub(r"\d+黄片", '', input_str)
    #---------------
    input_str = re.sub(r"[0-9]*\.?[0-9]+元", '', input_str)
    input_str = re.sub(r"\d+黄片", '', input_str)
    input_str = re.sub(r"拍\d+", '', input_str)
    input_str = re.sub(r"\d+起", '', input_str)
    input_str = re.sub(r"\d+天保质期", '', input_str)
    input_str = re.sub(r"奶粉\d+\+段", '', input_str)
    input_str = re.sub(r"\d+段", '', input_str)
    input_str = input_str.replace("-", "占位符")
    input_str = input_str.replace("nl", "ml")
    input_str = input_str.replace(".ml", "ml")
    input_str = re.sub(r"内装\d+", '', input_str)
    input_str = re.sub(r"[0-9]*\.?[0-9]+%", '', input_str)
    input_str= re.sub("赠送大麦", '', input_str)
    input_str= re.sub("苹果\+青稞", '', input_str)
    input_str= re.sub("\d+片新疆面包", '', input_str)
    # input_str = MultiUnit.replace_slash(input_str)
    if (input_str.count('*')>=2 and input_str.count('+')>=1) \
        or (input_str.count('*') ==3 and input_str.count('+') ==2):
        # 删除+，*中间的非汉子，非单位字符串
        input_str = re.sub(r"【.{1,10}】", '', input_str)
        input_str = re.sub(r"(?<=\d)(g|ml)?[\u4e00-\u9fa5]{1,10}(?=\*)", '', input_str)
        input_str = re.sub(r"(?<=\+).*?(?=\d)", lambda x: x.group() if x.group().isdigit() else '', input_str)
        input_str = re.sub("\++", '+', input_str)
        input_str = re.sub("\+ ", '+', input_str)
        pass

    return input_str


def default_su_filter(single_unit, input_str):
    """
    过滤single_unit判断它要不要保留
    :param single_unit:
    :param input_str: 提取的原始字符串
    :return:
    """
    if single_unit is None:
        return False
    if not isinstance(single_unit, SingleUnit):
        return False

    # 删除 0和负数
    if float(single_unit.number) <= 0:
        return False
    # 删除 数值大于1万的值
    if float(single_unit.number) >= 1e4:
        return False

    if single_unit.unit=='' and float(single_unit.number)>5000:
        return False

    # 只是一个数字，没有单位,并且前后没有操作符的话，删除
    def sub_str(i_s, i_e):
        if i_s <=0: i_s =0
        if i_e >= len(input_str): i_e = len(input_str)
        return input_str[i_s:i_e]

    def contain_num(i_s, i_e):
        if i_s <=0: i_s =0
        if i_e >= len(input_str): i_e = len(input_str)
        f = False
        for cc in input_str[i_s:i_e]:
           try:
               int(cc)
               f = True
               continue
           except:
               pass
        return f
    f_char = None if single_unit.start_index <= 0 else input_str[single_unit.start_index - 1]
    b_char = None if single_unit.end_index >= len(input_str) else input_str[single_unit.end_index]
    if single_unit.unit == '' \
            and (not Operator.is_char_op(f_char)) and (not Operator.is_char_op(b_char))\
            and (not (single_unit.unit_level.is_unit_char(f_char) and contain_num(single_unit.start_index-3, single_unit.start_index-1))): # 前面是单位，并且单位前面是数字
        return False

    if single_unit.unit=='' and float(single_unit.number)>50 and (not Operator.is_char_op(f_char)) and (not Operator.is_char_op(b_char)):
        return False

    # 去掉包邮紧邻的单位
    by_char = None if single_unit.end_index >= len(input_str) + 1 else input_str[
                                                                       single_unit.end_index:single_unit.end_index + 2]
    if by_char is not None and by_char == "包邮" \
            and (not Operator.is_char_op(f_char)) and (not Operator.is_char_op(b_char)):
        return False

    # 去掉3.3g这样的单位
    w = sub_str(single_unit.start_index-2, single_unit.start_index)
    w2 = sub_str(single_unit.end_index, single_unit.end_index+5)
    if single_unit.unit in ["g", "ml"] and float(single_unit.number) < 4 and not ("*" in w or "+" in w2):
        return False

    # 如果是麦片多少g删除
    w = sub_str(single_unit.start_index-2, single_unit.start_index)
    w2 = sub_str(single_unit.end_index, single_unit.end_index+5)
    if (w is not None and w in ['麦片', '姜茶']) or (w2 is not None and "麦片" in w2):
        return False
    if single_unit.unit in ["片"] and '列巴' in w2:
        return False
    if '谷物' in w2:
        return False

    # 去掉特别大的 二级单位，三级单位
    if single_unit.level == 2 or single_unit.level==3:
        if float(single_unit.number) >=500:
            return False
        # 浮点数值不对，删除1.2箱这样的值
        if float(single_unit.number) != int(float(single_unit.number)):
            return False
    if single_unit.unit in ["L", 'l', '升'] and float(single_unit.number)>5:
        single_unit.total_flag=1
    if single_unit.unit in ["L", 'l', '升'] and float(single_unit.number) in [220, 250]:
        single_unit.total_flag=0
        single_unit.unit = "ml"

    # 去掉内含多少小袋的，情况
    if single_unit.unit in ['小袋'] and ('含' in w or '含' in w2):
        return False
    if '买' in w and '送' in w2 and any(chr.isdigit() for chr in w2):
        return False

    if single_unit.unit in ['天'] and ("同城配送" not in sub_str(single_unit.start_index-5, single_unit.start_index) and '*' not in sub_str(single_unit.start_index-3, single_unit.start_index)):
        return False

    if "年卡" in str(input_str) or "年卡" in str(input_str) or "季卡" in str(input_str):
        return False

    if single_unit.unit in ['支', '片', '簧片'] and '*' not in w:
        return False

    if single_unit.unit in ["袋", '', '支'] and "【" in w and "】" in w2:
        return False

    if single_unit.unit in ["箱"] and '起' in w2 and float(single_unit.number) >=100:
        return False

    return True


def default_mu_filter(multi_unit, input_str, multi_list):
    """
    默认的multi_unit过滤器
    :param multi_unit:
    :param input_str:
    :return:
    """
    # multi_unit = MultiUnit(multi_unit)
    if multi_unit is not None:
        if len(multi_unit) == 2 and multi_unit.have_level(1) and multi_unit.have_operator('*'):
            l1_list = multi_unit.get_all_level_1()
            if len(l1_list) == 1:
                if float(l1_list[0].number) < 100 and l1_list[0].unit=='':
                    l1_list[0].level = 0
        # 木糖醇4桶8斤（无糖无脂方）
        if len(multi_list) == 2 and str(multi_list[0])[-1]=='桶' and str(multi_list[1])[-1]=='斤':
            if str(multi_unit)[-1] == '桶':
                return False


    return True


def default_mu_merge(multi_list, input_str='', op_list=None):
    """
    合并多个multi
    :return:
    """
    l1_existed = any(t_mu.have_level(1) for t_mu in multi_list)
    l1_list = [t_mu for t_mu in multi_list if
               t_mu.have_level(1) or (t_mu.have_level(0) and len(t_mu) > 1 and not l1_existed)]
    l2_total = [t_mu for t_mu in multi_list
                if len(t_mu)==1 and t_mu[0].level==2 and isinstance(t_mu[0], SingleUnit) and t_mu[0].total_flag==1]
    l_others = [t_mu for t_mu in multi_list if t_mu not in l1_list and t_mu not in l2_total]
    if op_list is None:
        op_list = Operator.parser_from_str(input_str)
    # print("l1_existed=",l1_list)
    # print("l_other",l_other_list)
    for v in l1_list:
        for t_v in l_others:
            if isinstance(v, MultiUnit) and isinstance(t_v, MultiUnit) and len(t_v)==1 and len(v)==4 and v.have_operator("*") and v.have_operator('+') and t_v.have_level(2):
                if v.sum_level(2) == float(t_v.get_first_single_unit().number):
                    continue
                if v.is_contains(t_v.get_first_single_unit()):
                    continue

            if len(v)==1 and v.have_level(1) and v.get_first_single_unit().total_flag == 1:
                continue
            if v.have_unit(t_v.get_first_single_unit().unit) and t_v.get_first_single_unit().unit != ''\
                or v.have_level(t_v.get_first_single_unit().level) and t_v.get_first_single_unit().level != 0:
                # 判断两个 之间是否有操作符，有操作符的话，使用找到的操作符
                # v的最后一个元素，和t_v的第一个元素
                op_between = MultiUnit.have_op_between_two_single(v, t_v, op_list, 20)
                if op_between:
                    if op_between.op !='*':
                        v.append(t_v, op_between, same_unit="merge")
                    else:
                        v.append(t_v,'*', same_unit='append')
                elif len(t_v)==1 and t_v.get_first_single_unit().level==2 and len(v)==3 and v.have_level(2):
                    v.append(t_v, "*", same_unit='verify')
                    pass
                else:
                    v.append(t_v, "|", same_unit="merge")
            elif len(t_v) == 1 and v.have_level(t_v.org_units[0].level) \
                and v.sum_level(t_v.org_units[0].level) == float(t_v.org_units[0].number):
                pass
            else:
                v.append(t_v, "*", same_unit="append")
    fix_multi_list = l1_list

    # 没有一级单位的话，直接用原始数据替换
    if len(fix_multi_list) == 0:
        fix_multi_list = multi_list
    # TODO 根据有没有操作符，以及出现位置，判断操作符是什么
    mu = MultiUnit.mu_from_list(fix_multi_list, "|", input_str)
    for t_v in l2_total:
        mu.append(t_v, '*', same_unit='verify')
    return mu


def parse_str(input_str,
              unit_level=None,
              str_modifier=default_str_modifier,
              su_filter=default_su_filter,
              mu_filter=default_mu_filter,
              only_one=True):
    """
    解析字符串，返回1个multi_unit
    :param input_str:
    :param unit_level: UnitLevel对象表示单位的层级
    :param str_modifier: input_str的查找替换函数
    :param su_filter: single_unit类的过滤函数
    :param mu_filter: multi_unit类的过滤函数
    :param only_one: True只有一个公式，合并成一个公式返回；False， 多个公式，不合并
    :return:
    """
    # 0. 检查参数是否合法
    if input_str is None:
        return None

    if unit_level is None:
        unit_level = DEFAULT_LEVEL
    MultiUnit.unit_level = unit_level

    # 1. 修改原始字符串, 替换原始字符串中会干扰判断的数字
    if DEBUG: print("input_str before modifier=", input_str)

    if str_modifier is not None and callable(str_modifier):
        input_str = str_modifier(input_str)
    if DEBUG: print("input_str after modifier=", input_str)

    # 2. 解析字符串 获得multiU_unit列表
    multi_list = MultiUnit.parser_from_str(input_str, unit_level, su_filter)
    op_list = None
    if multi_list is not None:
        multi_list, op_list = multi_list
    if DEBUG: print("MUltiUnit.parser_from_str=", multi_list)

    # 3. 过滤multi_unit
    if multi_list is not None and mu_filter is not None and callable(mu_filter):
        multi_list = [m for m in multi_list if mu_filter(m, input_str, multi_list)]

    # 4. 判断要不要合并多个multi_unit 到一个公式里
    if multi_list is None or len(multi_list) == 0:
        return None
    if only_one:
        mu = default_mu_merge(multi_list, input_str, op_list)
        if mu is not None:
            mu.infer_unit_level()
        if DEBUG: print("final the one multi unit:", mu)
        return mu
    else:
        return multi_list


if __name__ == "__main__":
    # TODO 各6瓶的情况支持

    title = "悦鲜活450ml+鲜动力酸奶135g（各6瓶） 12瓶"
    title = "250ml全脂+250ml0脂（各6瓶） 12瓶"
    # TODO 买xx送xx
    title = "全脂甜奶粉400g*5袋【买5送1袋300g高钙】"
    title = "木糖醇4桶8斤（无糖无脂方）"
    title = "原味芝士180g*12袋+芝芝多莓180g*12袋 24袋"
    title = "白桃燕麦6瓶+苹果粒6瓶【苹果味再升级 苹果+青稞】 12瓶"
    title = "草莓树莓*2+无花果*2+芒果*2+黑莓蓝莓*2 8杯"
    title = "【奶酪棒75】奶酪酱120g*5+吉利丁2.5g*10+奶酪棒模+ 糖霜250g+裱花袋+可可粉【四川不发】"
    title = "【大口更过瘾】混合水果味320g*3+原味100g*2共58支（赠160g奶片）"
    title = "简醇150g*6袋+慢醇150g*6袋 /入会加购 优先发货 12袋"
    title = "【简醇】160g*15袋+【慢醇】160g*15袋"
    title = "500水果*2+500原味*2+500梅子*1"
    title = "【奶酪棒75】奶酪酱120g*5+吉利丁2.5g*10+奶酪棒模+ 糖霜250g+裱花袋20只+可可粉【四川不发】"
    title = "3箱起包邮 德国进口 爱氏晨曦 全脂牛奶 纯牛奶 200ml*24 整箱装"
    title = "500克原味，果粒，混合水果3袋75"


    mu = parse_str(title)
    print("----------")
    for m in mu.org_units:
        print(m.__repr__())
    print("----------")
    print(mu.__repr__())
    print(mu.calc_weight())
    # file_path = "../data_labeled/低温牛奶测试用例.xlsx"

    # df = pd.read_excel(file_path)
    #
    # # 判断total-weight是否正确
    #
    # print(df)
