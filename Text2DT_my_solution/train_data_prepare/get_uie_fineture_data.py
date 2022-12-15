import json

in_data=open("data/Text2DT/Text2DT_en_re_dev.json","r")
out_file=open("data/Text2DT/dev.txt","w+")

# in_data=open("data/Text2DT/Text2DT_en_node_re_train.json","r")
# out_file=open("data/Text2DT/train.txt","w+")


import ahocorasick

schema=["基本情况","临床表现"]
schema2=["治疗药物","治疗方案","用法用量",'禁用药物']

for index,ins_json_data in enumerate(json.load(in_data)):
    fine_ture_data=[]
    on_item={}
    print(ins_json_data)
    text = ins_json_data['text']
    tail_entitys=[]
    # nodes = ins_json_data['triple_list']
    root=text.split("@")[0]
    print(root)
    tail_entitys=[]
    tail_entitys_to_index=[]
    A = ahocorasick.Automaton()
    for triple in ins_json_data['triple_list']:
        if triple[2] not in tail_entitys:
            tail_entitys.append(triple[2])
    for idx, key in enumerate(tail_entitys):
          A.add_word(key, (idx, key))
            # entity_index_in_texts_ie=list(re.finditer(re.escape(triple[2]),text))
            # # import pdb;pdb.set_trace()
            # entity_index_in_texts=[ i.span() for i in entity_index_in_texts_ie]
            
            # entity_index_in_text = text.find(triple[2])
    A.make_automaton()
    result=[]  
    for item in A.iter_long(text):
        result.append(item)
    tr_list=[]
    for idx,item in enumerate(result):
        
        for id,triple in enumerate(ins_json_data['triple_list']):
           
           if item[1][1]==ins_json_data['triple_list'][id][2]:
            #    if ins_json_data['triple_list'][id] not in tr_list:
                    tr_list.append([ins_json_data['triple_list'][id][1],ins_json_data['triple_list'][id][2],item[0]])
    # import pdb;pdb.set_trace()
    relation_list=[]
    for idx,item in enumerate(result):
        for triple in ins_json_data['relation']:
            if item[1][1]==triple[1]:
                # import pdb;pdb.set_trace()
                relation_list.append([triple[0]+"的"+triple[2],triple[1],item[0]])
    
    r_text="".join(text.split("@")[1:])
    schema_0=["条件","治疗"]
    # for p_item in schema_0:
    #     prompt=p_item
    #     result_list=[]
    result_list_1=[]
    result_list_2=[]
    for tr in tr_list:
        # import pdb;pdb.set_trace()
        if tr[0] in schema:
            result_list_1.append({"text":tr[1],"start":tr[2],"end":tr[2]+len(tr[1])})
        else:
            result_list_2.append({"text":tr[1],"start":tr[2],"end":tr[2]+len(tr[1])})
        
    on_item_0={"content":r_text,"result_list":result_list_1,"prompt":"条件"}
    on_item_1={"content":r_text,"result_list":result_list_2,"prompt":"治疗"}

    json.dump(on_item_0,out_file,ensure_ascii=False)
    out_file.write("\n")    
    json.dump(on_item_1,out_file,ensure_ascii=False)
    out_file.write("\n")    
        
        
    for per_re in relation_list:
        # import pdb;pdb.set_trace()
        on_item={"content":r_text,"result_list":[{"text":per_re[1],"start":per_re[2],"end":per_re[2]+len(per_re[1])}],"prompt":per_re[0]}
        json.dump(on_item,out_file,ensure_ascii=False)
        
        out_file.write("\n")
                    
            
                 
        # tr_list=list(set(tr_list))
        # if len(tr_list)>1:
           
        
        
