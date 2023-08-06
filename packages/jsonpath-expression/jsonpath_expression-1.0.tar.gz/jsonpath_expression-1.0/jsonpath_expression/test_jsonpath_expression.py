#!/usr/bin/env python
# -*- coding: utf-8 -*-

from jsonpath_expression.jsonpath_expression import JsonpathExpression
import requests,jsonpath,json

if __name__ == "__main__" :
    je= JsonpathExpression()
    city_url = "https://www.zhipin.com/wapi/zpCommon/data/city.json"
    text=requests.get(url=city_url).json()
    response = json.dumps(text)
    exp_dict = je.jsonpath_expression(text,"杭州")
    je.test_jsonpath_expression(text,exp_dict)
