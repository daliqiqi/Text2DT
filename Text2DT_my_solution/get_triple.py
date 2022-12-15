import json

# data_dir: data/Text2DT/
# train_file: Text2DT_train.json
# dev_file: Text2DT_dev.json
# test_file: Text2DT_tree_test.json
# label_file: label_rel_file.json
# in_data=json.load(open("data/Text2DT/Text2DT_train.json"))
# out_data=open("data/Text2DT/Text2DT_en_re_train.json","w+")

in_data=json.load(open("data/Text2DT/Text2DT_dev.json"))
out_data=open("data/Text2DT/Text2DT_en_re_dev.json","w+")
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


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
def recover_tree(traversal) -> TreeNode:
    tree=[i["role"] for i in traversal]
    mask=[i["triples"]==[]for i in traversal]
    
    back_ward_stack=-1
    path=[]
    first=""
    root=""
    condition_stack=[]
    len_=[]
    
    print(traversal)
    for index,item in enumerate(traversal):
    #    import pdb;pdb.set_trace()
        node=TreeNode(item)
        if index==0:
            root=node
            condition_stack.append(node)
            len_.append(0)
        else:           
            if len_[-1]==0:
                condition_stack[-1].left=node
                len_[-1]=len_[-1]+1
            elif len_[-1]==1:
                condition_stack[-1].right=node
                len_[-1]=len_[-1]+1
                condition_stack.pop()
                len_.pop()
            if tree[index]=="C":
                condition_stack.append(node)
                len_.append(0)
    return root      
def recover_tree_1(traversal) -> TreeNode:
    tree=[i["role"] for i in traversal]
    mask=[i["triples"]==[]for i in traversal]
    
    back_ward_stack=-1
    path=[]
    first=""
    root=""
    stack=[]
    for index,item in enumerate(traversal):
        if index==0:
            node=TreeNode(item)
            root= node 
            stack.append(node)
        # import pdb;pdb.set_trace()
        if index!=len(traversal):
            if tree[index]=="C":
                stack.append(node)
                len_=0
                
                node.left=TreeNode(traversal[index+1])
                
                
                    
                
                if index<=len(traversal)-3:
                    if tree[index+1]=="C" and tree[index+2]=="D":
                        node.right=TreeNode(traversal[back_ward_stack])
                        back_ward_stack=back_ward_stack-1
                    else:
                        node.right=TreeNode(traversal[index+2])
                    if index<len(traversal)-3:
                        
                        if tree[index+1]=="C":
                            node=node.left
                        elif tree[index+2]=="C":
                            node=node.right
                        else:
                            if "C" in tree[index+1:]:
                                import pdb;pdb.set_trace()
                    
                    
            if tree[index]=="D":
                continue
         
    return root
       
def preorderTraversal(root: TreeNode):
        def preorder(root: TreeNode):
            if not root:
                return
            res.append(root.val)
            preorder(root.left)
            preorder(root.right)
        
        res = list()
        preorder(root)
        return res
def preorderTraversal_get_relation(root: TreeNode):
    # "对应情况":["肯定治疗","否定治疗"],
    # "对应情况":["肯定情况","否定情况"],

        def preorder(root: TreeNode):
            if not root:
                return
            this_val=root.val
            right_val_list=[]
            left_val_list=[]
            to_right=root
            to_left=root

            # import pdb;pdb.set_trace()  
            while to_right.right:
                    right_val_list.append(to_right.right.val)
                    to_right=to_right.right
               
            while to_left.left:
                    left_val_list.append(to_left.left.val)
                    to_left=to_left.left
            # while to_l:
            #     if to_right.right:
            #         right_val.append(root.right.val)
            #         to_right=to_right.right
            
            for item in this_val['triples']:
                for left_val in left_val_list:
                    if left_val and left_val["role"]=="D":
                        for l_item in left_val['triples']:
                            relation.append([item[2],l_item[2],"肯定治疗"])
                    if left_val and left_val["role"]=="C":
                        for l_item in left_val['triples']:
                            relation.append([item[2],l_item[2],"肯定条件"])
                for    right_val in right_val_list:
                    if right_val and right_val["role"]=="D":
                        for r_item in right_val['triples']:
                            relation.append([item[2],r_item[2],"否定治疗"])
                    if right_val and right_val["role"]=="C":
                        for r_item in right_val['triples']:
                            relation.append([item[2],r_item[2],"否定条件"])
                    
                    
                  
            res.append(root.val)
            preorder(root.left)
            preorder(root.right)
        relation=[]
        res = list()
        preorder(root)
        # import pdb;pdb.set_trace()  
        return relation    


all_result=[]
for index,item in enumerate(in_data):
    
    one_item={}
    one_item["triple_list"]=[]
    one_item["text"]=item["text"]
    for tr in item["tree"]:
        for triple in tr["triples"]:
            one_item["triple_list"].append(triple)
    inner_tripple_relation=[]
    inner_node_relation=[]
    cross_node_relation=[]
    relation=[]
    tree=[]
    for tri_index,item in enumerate(in_data[index]["tree"]):
        # import pdb;pdb.set_trace()
        if "C" in item["role"]:
            if "and" in item['logical_rel']:
                for triplet in item['triples'][1:]:
                    inner_node_relation.append([item['triples'][0][2],triplet[2],"并列情况"])
            if "or" in item['logical_rel']:
                for triplet in item['triples'][1:]:
                    inner_node_relation.append([item['triples'][0][2],triplet[2],"或者情况"])
        
        if "D" in item["role"]:
            if "and" in item['logical_rel']:
                for triplet in item['triples'][1:]:
                    inner_node_relation.append([item['triples'][0][2],triplet[2],"并列治疗"])
            if "or" in item['logical_rel']:
                for triplet in item['triples'][1:]:
                    inner_node_relation.append([item['triples'][0][2],triplet[2],"或者治疗"])
            for triplet in item['triples']:
                if "用法用量" in triplet[1]:
                    inner_tripple_relation.append([triplet[0],triplet[2],"用量对应"])
        
                    
        # if "C" in item["role"] and "C" in item[tri_index-1]:
        #     for triplet in item['triples'][1:]:
        #             relation.append([item['triples'][0][2],triplet[2],"对应情况"])
    root_tree=recover_tree(in_data[index]["tree"])
    restuct_tree=preorderTraversal(root_tree)
    
    if restuct_tree!=in_data[index]["tree"]:
        import pdb;pdb.set_trace()
    
    restuct_reltion=preorderTraversal_get_relation(root_tree)
    all_relation=relation+restuct_reltion
    one_item["relation"]=restuct_reltion
    # import pdb;pdb.set_trace()
    
    all_result.append(one_item)
json.dump(all_result,out_data,ensure_ascii=False)       


            
        
        
        
   
            
        
    
        
                
                
    
    