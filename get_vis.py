import json
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

from graphviz import Digraph


def plot_model(this, name):
    tree_list=this["tree"]
    print("text",this["text"])
    tree_root=recover_tree(tree_list)
    restuct_tree=preorderTraversal(tree_root)
    if restuct_tree!=tree_list:
        import pdb;pdb.set_trace()
    
    tree=tree_root
    g = Digraph("G", filename=name, format='svg', strict=False)
    g.node("pp", this["text"],color="white")
    g.edge("pp", "0",color="white")
    first_label = str(tree.val)
    g.node("0", first_label)
    if tree.left:
        _sub_plot(g, tree.left, "0","是")
    if tree.right:
        _sub_plot(g, tree.right, "0",'否')
    g.view()


root = "0"


def _sub_plot(g, tree, inc,lable):
        global root
        
        print(tree)
        print("root",root)

    # first_label = list(tree.keys())[0]
    # ts = tree[first_label]
        if tree.left or tree.right :
        # if isinstance(tree[first_label][i], dict):
            root = str(int(root) + 1)
            g.node(root, str(tree.val))
            g.edge(inc, root, lable)
            # import pdb;pdb.set_trace()
            if tree.left:
                _sub_plot(g, tree.left, root,"是")
            if tree.right:
                if tree.left:
                    _sub_plot(g, tree.right, str(int(root)-1),"否")
                else:    
                    _sub_plot(g, tree.right, root,"否")
        else:
            # import pdb;pdb.set_trace()
            root = str(int(root) + 1)
            g.node(root, str(tree.val),fillcolor="lightgrey")
            g.edge(inc, root, lable)
def main():
    all=json.load(open("Text2DT_sub.json","r"))
    for this in  all:
        
        plot_model(this,"images/"+this["text"].split("@")[0]+".gv")
        # import pdb;pdb.set_trace()
main()
    
    
    