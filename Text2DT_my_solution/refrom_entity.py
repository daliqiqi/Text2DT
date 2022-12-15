import json
from copy import deepcopy
import json
def refrom_entity(json_data,relation_data,outpath_data):
    # json_data=json.load(open("data/Text2DT/Text2DT_uie_result_sub.json","r"))
    schema=["基本情况","临床表现","治疗药物","治疗方案","用法用量",'禁用药物']
# relation_data=json.load(open("data/Text2DT/Text2DT_uie_relation2_result_test.json","r"))
    # relation_data=json.load(open("data/Text2DT/Text2DT_uie_relation2_result_sub.json","r"))
    triple_lists=[]

    for index_j,data in enumerate(json_data):
        for item in data["result"]:
            triple_list=[]
            root=data["text"].split("@")[0]
        # ["糖尿病酮症酸中毒患者", "临床表现", "轻度脱水"]
            for key in schema:
                    if key in item:
                    # if key!="用法用量":
                            for v in item[key]:
                            # for trp in v:
                                triple_list.append([root,key,v['text'],v['start']])
            triple_list.sort(key=lambda x: x[-1])
        
            for index,triple in enumerate(deepcopy(triple_list)):
                if triple[1]=="用法用量":
                    if len(relation_data[index_j]['result'])>1:
                        import pdb;pdb.set_trace()
                    print(triple)
                
                    
                    for re_item  in relation_data[index_j]['result'][0]['用法用量']:
                        if re_item['text']==triple[2] and re_item['start']==triple[-1]:
                            com_pos=[]
                            if "relations" in re_item:
                                for per_re in re_item['relations']["治疗药物"]:
                                    com_pos.append([per_re["text"],per_re["start"],abs(per_re["start"]-triple[-1])])
                            
                            com_pos.sort(key=lambda x: x[-1])   
                    # if triple==['眶周蜂窝织炎患者', '用法用量', '静脉用', 23]:
                    #     import pdb;pdb.set_trace()
                    if   com_pos:     
                        triple_list[index][0]=com_pos[0][0]          
                            
        # import pdb;pdb.set_trace()
            triple_lists.append({"text":data["text"],"triple_list":triple_list})
    json.dump(triple_lists,open(outpath_data,"w+"),ensure_ascii=False)
    return    triple_lists
                # if index==0 and "药物" in triple_list[index+1][1]:
                    
                # if index!=0 and "药物" in triple_list[index-1][1]:
                #     triple_list[index][0]=triple_list[index-1][0]
                    # else:

                    
                
        
          
                            
        
        
        