#!/usr/bin/python
# -*- coding: utf-8 -*-

from pprint import pprint
from paddlenlp import Taskflow
import json 
json_data=json.load(open("data/Text2DT/Text2DT_test.json","r"))

schema=["基本情况","临床表现","治疗药物","治疗方案","用法用量",'禁用药物']
# ie.set_schema(schema)

schema2={"治疗药物":["用法用量"],'禁用药物':['用法用量']}
# inner_tripple_relation
schema3={"用法用量":["治疗药物",'禁用药物']}

# inner node relation
schema4={"条件":["并列情况","或者情况"],
         "治疗":["并列治疗","或者治疗"]}


# between node relation
schema5={
         "条件":["肯定治疗","否定治疗"],
         "条件":["肯定条件","否定条件"],   
         }



# schema4={"用法用量":["治疗药物",'禁用药物'],
#          "条件":["肯定治疗","否定治疗"],
#          "条件":["肯定条件","否定条件"],
#           "条件":["并列情况","或者情况"],
#          "治疗":["并列治疗","或者治疗"]
#          }

ie = Taskflow("information_extraction", schema=schema5, task_path='/root/pipa/paddle//root/pipa/paddle/checkpoint_new/model_model_8000')
import json 
result_json=[]
for item in json_data:
    text="".join(item['text'].split("@")[1:])
    result=ie(text)
    print(ie(text))
    result_json.append({"text":item['text'],"result":result})
    # import pdb;pdb.set_trace()
json.dump(result_json,open("data/Text2DT/Text2DT_uie_result_sub_fancy.json","w+"),ensure_ascii=False)


# ie = Taskflow("information_extraction", schema=schema4, task_path='/root/pipa/paddle/checkpoint/model_9300')
# import json 
# result_json=[]
# for item in json_data:
#     text="".join(item['text'].split("@")[1:])
#     result=ie(text)
#     print(ie(text))
#     result_json.append({"text":item['text'],"result":result})
#     # import pdb;pdb.set_trace()
# json.dump(result_json,open("data/Text2DT/Text2DT_uie_relation2_result_sub_fancy.json","w+"),ensure_ascii=False)