#!/usr/bin/python
# -*- coding: utf-8 -*-

from pprint import pprint
from paddlenlp import Taskflow
import json 

# ie.set_schema(schema)




def get_ner_from_uie(json_data, outpath="data/Text2DT/Text2DT_uie_result_sub.json"):
    
    schema=["基本情况","临床表现","治疗药物","治疗方案","用法用量",'禁用药物']
    ie = Taskflow("information_extraction", schema=schema, task_path='checkpoint_decision_tree/model_best')
    result_json=[]
    for item in json_data:
        text="".join(item['text'].split("@")[1:])
        result=ie(text)
        print(ie(text))
        result_json.append({"text":item['text'],"result":result})
    # import pdb;pdb.set_trace()
    json.dump(result_json,open(outpath,"w+"),ensure_ascii=False)
    return result_json

# get_ner_from_uie(json_data)




def get_ner_and_nre_from_iue(json_data,outpath):
    schema4={"用法用量":["治疗药物",'禁用药物'],
         "对应情况":["肯定治疗","否定治疗"],
         "对应情况":["肯定情况","否定情况"],
          "对应情况":["并列情况","或者情况"],
         "治疗情况":["并列治疗","或者治疗"]
         }
    schema2={"治疗药物":["用法用量"],'禁用药物':['用法用量'],
         "临床表现":["否定临床表现"]}
    schema3={"用法用量":["治疗药物",'禁用药物']}
    ie = Taskflow("information_extraction", schema=schema3, task_path='checkpoint_decision_tree/model_best')
    result_json=[]
    for item in json_data:
        text="".join(item['text'].split("@")[1:])
        result=ie(text)
        print(ie(text))
        result_json.append({"text":item['text'],"result":result})
    # import pdb;pdb.set_trace()
    json.dump(result_json,open(outpath,"w+"),ensure_ascii=False)
    return result_json

# get_ner_and_nre_from_iue(json_data)