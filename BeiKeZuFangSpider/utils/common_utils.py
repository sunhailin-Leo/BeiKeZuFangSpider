# -*- coding: UTF-8 -*-
"""
Created on 2018年9月17日
@author: Leo
"""

import difflib
import logging

# 日志
logger = logging.getLogger(__name__)


# 字典模糊匹配
class DictMatching:
    def __init__(self, matching_dict: dict, words: str, max_result: bool):
        """
        字典key值的模糊匹配, 选出最有可能的结果
        :param matching_dict: 待匹配的字典
        :param words: 需要进行模糊匹配的值
        :param max_result: 是否输出最大可能的值
        :return: 结果返回 -> 存在结果则返回 List[Tuple[float, Dict]]; 不存在则为 List[None]
        """
        self._matching_dict = matching_dict
        self._words = words
        self._max_result = max_result

    def dict_keys_matching(self) -> list:

        # 获取字典的key的list
        keys = list(self._matching_dict.keys())
        logger.debug("Key List: {}".format(keys))
        # 输出匹配结果(概率列表)
        possible_list = [self._possible_score(acc_word=key, input_word=self._words) for key in keys]
        logger.debug("Possible List: {}".format(possible_list))
        # 将结果不等于0.0的数据输出成[tuple(分数, 对应的key)]
        matching_result = \
            [(score, {keys[i]: self._matching_dict[keys[i]]}) for i, score in enumerate(possible_list) if score != 0.0]
        # 降序排序
        matching_result = sorted(matching_result, key=lambda item: -item[0])
        # 判断长度是否大于0(存在多个结果)
        if self._max_result:
            matching_result = matching_result[:1]
        return [[None], matching_result][len(matching_result) > 0]

    @staticmethod
    def _possible_score(acc_word: str, input_word: str) -> float:
        """
        返回匹配的概率
        :param acc_word: 准确值
        :param input_word: 输入值
        :return: 概率值
        """
        return difflib.SequenceMatcher(a=acc_word, b=input_word).quick_ratio()


def flatten(nested_list: list) -> list:
    """
    扁平化list
    :param nested_list: list
    :return: list
    """
    res_list = []
    for i in nested_list:
        if isinstance(i, list):
            res_list.extend(flatten(nested_list=i))
        else:
            res_list.append(i)
    return res_list


# if __name__ == '__main__':
#     t_dict = {"罗湖区": "456", "南山区": "789", "福田": "1234", "福田区": "123"}
#     d = DictMatching(matching_dict=t_dict, words="福田", max_result=True)
#     res = d.dict_keys_matching()
#     print(res)
