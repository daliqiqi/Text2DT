import json
from get_ner_from_uie import get_ner_from_uie,get_ner_and_nre_from_iue
from refrom_entity import refrom_entity
from new_logic import parse_tree_by_logit


# 获取实体识别和关系识别结果
schema=["基本情况","临床表现","治疗药物","治疗方案","用法用量",'禁用药物']
# ie.set_schema(schema)

schema2={"治疗药物":["用法用量"],'禁用药物':['用法用量']}
schema3={"用法用量":["治疗药物",'禁用药物']}


schema4={"用法用量":["治疗药物",'禁用药物'],
         "对应情况":["肯定治疗","否定治疗"],
         "对应情况":["肯定情况","否定情况"],
          "对应情况":["并列情况","或者情况"],
         "治疗情况":["并列治疗","或者治疗"]
         }
inputdata=json.load(open("data/Text2DT/Text2DT_test.json","r"))
outpath="data/Text2DT/Text2DT_uie_result_sub.json"
# ner_data=get_ner_from_uie(inputdata,outpath)
outpath="data/Text2DT/Text2DT_uie_relation2_result_sub.json"
# relation_data=get_ner_and_nre_from_iue(inputdata,outpath)
ner_data=json.load(open("data/Text2DT/Text2DT_uie_result_sub.json","r"))
# relation_data=json.load(open("data/Text2DT/Text2DT_uie_relation2_result_test.json","r"))
relation_data=json.load(open("data/Text2DT/Text2DT_uie_relation2_result_sub.json","r"))
outpath="data/Text2DT/Text2DT_tree_triplets_sub.json"
# "data/Text2DT/Text2DT_tree_triplets_sub.json"
triplets_data=refrom_entity(ner_data,relation_data,outpath)
# json_data=json.load(open("data/Text2DT/Text2DT_tree_triplets_sub.json","r"))
trees=parse_tree_by_logit(triplets_data)
json.dump(trees,open("data/Text2DT/Text2DT_sub.json","w+"),indent=4,ensure_ascii=False)