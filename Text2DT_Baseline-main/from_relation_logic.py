
import json 
from utils.logic_predictor import logic_pre
from utils.eval import TreeStructureEval
import re
from copy import deepcopy
from eval import eval
import ahocorasick
dict={"临床表现":0,"治疗药物":0,"治疗方案":0,"用法用量":0,"基本情况":0,"禁用药物":0}
relation_schema=[{
                "relation":"治疗",
                "from":["临床表现","基本情况"],
                "to":["治疗药物","治疗方案","禁用药物","用法用量"]},
                 {
                "relation":"用药方法",
                "from":["治疗药物","治疗方案","禁用药物"],
                "to":["用法用量"]}]

json_data=json.load(open("data/Text2DT/Text2DT_tree_triplets_sub.json","r"))
# tree_data=json.load(open("data/Text2DT/Text2DT_dev.json","r"))
def node_to_tree( triple_divide,tail_entitys_to_index):
        #从节点对表中解码出树
        
        node_len = len(triple_divide)
        #寻找根节点
        root = tail_entitys_to_index[0][2][2]
        tree=[]
        add_flag=False
        
        for triples in triple_divide:
            
            cur=[]
            for triple in triples :
                if  triples[0][1][0]!="N" and tail_entitys_to_index[triple[0]][2] not in cur:
                    cur.append(tail_entitys_to_index[triple[0]][2])
            if triples[0][1]=="C":
                tree.append({"role": 'C', "triples": cur, "logical_rel": "null"})
            if triples[0][1][0]=="D":
                 tree.append({"role": 'D', "triples": cur, "logical_rel": "null"})
            if triples[0][1][0]=="N":
                tree.append({"role": 'D', "triples": [], "logical_rel": "null"})
        return tree
                  
def triple_to_node(tail_entitys_to_index):
        num_triple=len(tail_entitys_to_index)
        triple_divide = []
        node_flag = [True]*num_triple
        triple_divide =[]

        # while True in node_flag:
            #将同一节点中的三元组划分到一起
        # index = node_flag.index(True)
        node_flag[0] = "C"
        tmp = []
        for i in range(num_triple):
            
            
            if tail_entitys_to_index[i][2][1] in relation_schema[0]['from']  :
                node_flag[i] = "C"
            elif tail_entitys_to_index[i][2][1] in relation_schema[0]['to']  :
                if  tail_entitys_to_index[i][2][1] in relation_schema[1]['to']:
                    node_flag[i] = "D2"
                else:
                    node_flag[i] = "D1"
                    
                # [[(0, 'D1'), (1, 'D1')], [(2, 'C')], [(3, 'D1')], [(4, 'C')], [(5, 'D1'), (6, 'D1')], [(7, 'C')], [(8, 'D1')]]
                # node_flag[i] = "D"
            if i!=0 and node_flag[i][0]!=node_flag[i-1][0]:
                    
                triple_divide.append(tmp)
                tmp = []
            tmp.append((i,node_flag[i]))
                
        # import pdb;pdb.set_trace()
        triple_divide.append(tmp)
        return  triple_divide
def revert_D1_D2(triple_divide):
    from operator import itemgetter
    for index,triple in enumerate(deepcopy(triple_divide)):
        if "D" in triple[0][1]:
            triple.sort(key=itemgetter(1))
            triple_divide[index]=triple
    # import pdb;pdb.set_trace()
    return triple_divide
def get_append_d(text):
    # import pdb;pdb.set_trace()
    D=[]
    D_word=["暂","注意","使用","应用"]
    for and_word in D_word:
        
        if list(re.finditer(and_word,text)):
            for item in list(re.finditer(and_word,text)):
                 return [item.start(),text[item.start():-1]]
    
    return D
def reform_triple(triple_divide,tail_entitys_to_index,text):
    C=[]
    D=[]
    if '自身免疫性肝炎妊娠期患者' in text:
        # for item in triple_divide:
        #     if "C" in item[0][1]:
        #         C.append(tail_entitys_to_index[
        #                                        ])
        # C1=tail_entitys_to_index[0]
        
        import pdb;pdb.set_trace()
    pa=triple_divide[0]
    
    
    return_this=[]
    # import pdb;pdb.set_trace()
    triple_divide=revert_C_D(triple_divide, tail_entitys_to_index, text) 
    triple_divide=revert_D1_D2(triple_divide)
    
    
    
    # for and_word in and_words:
    #     if and_word in text:
    #         add=True
    
    
          
    
        
    p_root = get_root(triple_divide, tail_entitys_to_index)
    
    
    add = if_add(text, p_root) 
    exception = if_exception(text, p_root) 
    # import pdb;pdb.set_trace()
    if exception:
    
        triple_divide,tail_entitys_to_index=except_split(triple_divide, tail_entitys_to_index, exception)
                     
        return_this= triple_divide    
        # import pdb;pdb.set_trace()
    
    elif  p_root:
        
        broadcast = if_broadcast(triple_divide, tail_entitys_to_index, p_root)
        if broadcast or add:
            for index,triples in enumerate(deepcopy(triple_divide)):
                if index==0:
                    continue
                for triple in triples:
                    
                        if triple[1][0]=="D":
                            triple_divide[index]=pa
                            triple_divide[index]=pa+triples
                        pass
        if not broadcast:
            import pdb;pdb.set_trace()
            
            return_this= triple_divide[1:]+[pa]
        if broadcast:
            
            return_this= triple_divide[1:]
    else:
        return_this= triple_divide
    
    if "C" in return_this[-1][0][1]:   
            return_this.append([(len(tail_entitys_to_index),"D")])

            start,word=get_append_d(text) 
            tail_entitys_to_index.append([word,start,[tail_entitys_to_index[0][2][0],"治疗方案",word]])
            print(tail_entitys_to_index[-1])
            import pdb;pdb.set_trace()
    
    
    len_d=0
    for idx,item in enumerate(deepcopy(return_this)):
        if "D" in item[0][1]:
            len_d=len_d+1
        else:
            # if len_d==1 and idx==len(return_this)-1:
            #     return_this[idx-1].append((0,"N"))
                
            len_d=0
    if len_d==1 and idx==len(return_this)-1:
                return_this.append([(0,"N")])
    # import pdb;pdb.set_trace()
    return return_this

def except_split(triple_divide, tail_entitys_to_index, exception):
    
    if tail_entitys_to_index[0][2][1]=='禁用药物':
        tail_entitys_to_index.append([tail_entitys_to_index[0][0],tail_entitys_to_index[0][1],[tail_entitys_to_index[0][2][0],"治疗药物",tail_entitys_to_index[0][2][2]]])
    else:
        tail_entitys_to_index.append([tail_entitys_to_index[0][0],tail_entitys_to_index[0][1],[tail_entitys_to_index[0][2][0],"禁用药物",tail_entitys_to_index[0][2][2]]])

    
    for triples_index,triples in enumerate(deepcopy(triple_divide)):
        for triple_idx,triple in enumerate(triples[:-1]):
            if tail_entitys_to_index[triples[triple_idx][0]][1]<exception and tail_entitys_to_index[triples[triple_idx+1][0]][1]>exception:
                split_this=triple_divide[triples_index]
                triple_divide[triples_index]=split_this[0:triple_idx+1]
                triple_divide.append(triple_divide[0])
                triple_divide.append(split_this[triple_idx+1:])
                triple_divide.append([(len(tail_entitys_to_index)-1,"D")])
    # import pdb ;pdb.set_trace()
    return triple_divide[1:],tail_entitys_to_index

def if_exception(text, p_root):
    exception=False
    exception_word=["仅","除","否则"]
    for and_word in exception_word:
        if p_root:
            if list(re.finditer(and_word,text[p_root[1]:])):
                # import pdb;pdb.set_trace()
                for item in list(re.finditer(and_word,text[p_root[1]:])):
                    return item.start()+p_root[1]
                
    return exception

def if_add(text, p_root):
    and_words = ['同时', '再', '然后', '联合', '继而', '并', '还需', "无需.*但"]

    add=False
    for and_word in and_words:
        if p_root:
            # import pdb;pdb.set_trace()
            if list(re.finditer(and_word,text[p_root[1]:])):
                for item in list(re.finditer(and_word,text[p_root[1]:])):
                    return item.start()+p_root[1]
            # for item in list(re.finditer(and_word,text)):
            #     reverse_index_list.append(item.span()[0])
    return add

def if_broadcast(triple_divide, tail_entitys_to_index, p_root):
    broadcast=False
    for index,triples in enumerate(deepcopy(triple_divide)):
        if index==0:
            continue
        for triple in triples:
                # import pdb;pdb.set_trace()
            if triple[1]=="D2" and  tail_entitys_to_index[triple[0]][2][0]==p_root[0]  :
                if "D1" not in [ item[1] for item in triples]:
                    broadcast=True
    return broadcast

def revert_C_D(triple_divide, tail_entitys_to_index, text):
    reverse_words=["用于","是.*的首选","治疗.*效果"]
    
    reverse=False
    reverse_index_list=[]
    for and_word in reverse_words:
        if list(re.finditer(and_word,text)):
            for item in list(re.finditer(and_word,text)):
                reverse_index_list.append(item.span()[0])
            reverse=True
    if reverse:
        index_postion={}
        for idx,item in enumerate(tail_entitys_to_index):
                index_postion[idx]=tail_entitys_to_index[idx][1]
            
        DC_pair=[]
        for idx,item in enumerate(triple_divide[0:-1]):
            if item[-1][1][0]=="D" and triple_divide[idx+1][-1][1]=="C":
                DC_pair.append((item,triple_divide[idx+1]))
                
        r_DC_pair=[]
        for item in DC_pair:
            for reverse_index in reverse_index_list:
                if index_postion[item[0][-1][0]]<reverse_index and index_postion[item[1][0][0]]>reverse_index:
                    r_DC_pair.append(item)
        # if len(r_DC_pair)>1:
        #     import pdb;pdb.set_trace()
        # import pdb;pdb.set_trace() 
        for index,item in enumerate(deepcopy(triple_divide)):
            for pair in r_DC_pair:
                if item == pair[0]:
                    triple_divide[index],triple_divide[index+1]=triple_divide[index+1],triple_divide[index]
    return triple_divide

def get_root(triple_divide, tail_entitys_to_index):
    p_root=False
    for triple_divide_per in triple_divide[0:1]:
        for item in triple_divide_per:
            if "D1" in item[1]:
                p_root=tail_entitys_to_index[item[0]]
                return p_root
    return p_root

            
    
            
        
        
    #     pa=triple_divide[0]
    #     for index,triples in enumerate(deepcopy(triple_divide)):
    #         if index==0:
    #             continue
    #         for triple in triples:
    #             if triple[1]=="D2":
    #                 # import pdb;pdb.set_trace()
    #                 triple_divide[index]=pa
    #                 triple_divide[index]=pa+triples
    #                 pass
    #     return triple_divide[1:]
    # else:
    #     return triple_divide
                
                
        
        
            
def parse_tree_by_logit(json_data):
  
  trees=[]
  f=open("bas_case.txt","w+")
  for all_idx,ins_json_data in enumerate(json_data):
    text_old = ins_json_data['text']
    # tree_dev=tree_data
    text= "".join(ins_json_data['text'].split("@")[1:])
    # print(tree_dev[all_idx])
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
    
    for idx,item in enumerate(result):
        tr_list=[]
        for id,triple in enumerate(ins_json_data['triple_list']):
           
           if item[1][1]==ins_json_data['triple_list'][id][2]:
               if ins_json_data['triple_list'][id] not in tr_list:
                    tr_list.append(ins_json_data['triple_list'][id])
               
        # tr_list=list(set(tr_list))
        # if len(tr_list)>1:
        # import pdb;pdb.set_trace()
        this=[]
        type=""
        for tr in tr_list:
            type=type+tr[1]
        this=[tr_list[0][0],tr_list[0][1],tr_list[0][2]]
            
        tail_entitys_to_index.append([item[1][1],item[0],this])
        
        
        import pdb;pdb.set_trace()
        # entity_index_in_text=result
    tail_entitys_to_index=[]  
        
        # tail_entitys_to_index.append([triple[2], entity_index_in_text,triple])
    # for index ,triple in enumerate(ins_json_data['triple_list']):           
    tail_entitys_to_index.sort(key=lambda x: x[1])
    triple_divide=triple_to_node(tail_entitys_to_index)
    re_triple_divide=reform_triple(triple_divide,tail_entitys_to_index,text)
    tree=node_to_tree( re_triple_divide,tail_entitys_to_index)
    tree=logic_pre(text,tree)
    trees.append({"text":text_old ,"tree":tree})
    # print(tree,tree_dev[all_idx]["tree"])
    # eval(tree,tree_dev[all_idx]["tree"])
    # if eval(tree,tree_dev[all_idx]["tree"])[1] !=1:
    #     print(tree_dev[all_idx]["text"],"\n","golden:",tree_dev[all_idx]["tree"],"\n","predic:",tree,file=f)
    #     # import pdb;pdb.set_trace()
        
    # print(eval(tree,tree_dev[all_idx]["tree"])[1])

  return trees
trees=parse_tree_by_logit(json_data)
json.dump(trees,open("data/Text2DT/Text2DT_sub.json","w+"),indent=4,ensure_ascii=False)
# tree_dev=tree_data
# tree_eval = TreeStructureEval(trees,tree_dev)
# tree_acc, triplet_f1, path_f1, tree_edit_distance, node_f1 = tree_eval.tree_structure_eval()
# # (0.3500000064999999, 0.8728414444696367, 0.488495577031874, 5.3499999465000005, 0.73726541625398)#
# print(tree_eval.tree_structure_eval())
# eval(trees,tree_dev)
# (0.4100000058999999, 0.9262634632539131, 0.5559566803034055, 4.6699999533000005, 0.7617728538455046)

# (0.6500000035, 0.985915492979788, 0.7153024921163613, 3.7899999621000005, 0.8640646033268785)
#  (0.6800000032, 0.9859375000219727, 0.746003553300165, 3.6099999639000004, 0.8802153435256654)

    # node_matrix = nodematrix(nodes)

    # #获得三元组在树中的关系
    # for i in range(len(node_matrix)):
    #     for j in range(len(node_matrix)):
    #         node_relation = node_matrix[i][j]
    #         if node_relation != 0:
    #             for head_triple in nodes[i]['triples']:
    #                 for tail_triple in nodes[j]['triples']:
    #                     triple_relation_in_tree.append([tail_triple,node_relation,head_triple])

    # #获取尾实体在句子中的索引，按照索引顺序将代表三元组的尾实体拼接在句子后
    # for triple in triple_relation_in_tree:
    #     if triple[0][2] not in tail_entitys:
    #         entity_index_in_text = text.find(triple[0][2])
    #         if entity_index_in_text != -1:
    #             tail_entitys_to_index.append([triple[0][2],entity_index_in_text, triple[0]])
    #             tail_entitys.append(triple[0][2])
    #     if triple[2][2] not in tail_entitys:
    #         entity_index_in_text = text.find(triple[2][2])
    #         if entity_index_in_text != -1:
    #             tail_entitys_to_index.append([triple[2][2], entity_index_in_text, triple[2]])
    #             tail_entitys.append(triple[2][2])
    # tail_entitys_to_index.sort(key=lambda x: x[1])
    
    
    
    # tree = self.node_to_tree(node_matrix)

    #         #将三元组索引转换为三元组
    #         for node in tree:
    #             tmp=[]
    #             map_index=node['triples']
    #             if map_index !='none' :
    #                 for j in triple_divide[map_index]:
    #                     tmp.append(entity2triple[j][2])
    #                 node['triples'] = tmp
    #                 #判断三元组间对逻辑关系
    #                 node['logical_rel'] = self.logic_pre(node['triples'])
    #             else:
    #                 node['triples']=[]
    #                 node['logical_rel'] = 'null'

    #         trees.append({"text":'',"tree":tree})
    #     return trees