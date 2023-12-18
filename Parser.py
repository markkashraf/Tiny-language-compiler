#from graphviz import Graph
import Scanner as src
outputs = []
iterator = 0
Nodes = []
Parents = []
Parents.append(0)
currentnode = 1
connectParent = True

class node:
    parentNode = 0
    value = ""
    Node = 0
    connectParent = True
    def __init__(self,value,Node, parentNode):
        self.Node = Node
        self.parentNode = parentNode
        self.value = value
    def is_statment(self):
        statment = ["if","repeat","assign","read","write"]
        splitted = self.value.split("\n")
        for token in splitted:
            if(token in statment):
                return True
        return False
    def getvalue(self):
        return self.Node
def match(expectedtoken):
    global iterator
    if(outputs[iterator][0]==expectedtoken)or(outputs[iterator][1]==expectedtoken):
        iterator += 1
    else:
       iterator = -1
def program():
    global iterator
    stmtsequence()
def stmtsequence():
    global iterator,connectParent
    connectParent = True
    statment()

    while(iterator < len(outputs) and outputs[iterator][0]==';'):
        connectParent = False
        match(";")
        statment()

def statment():
    global iterator,currentnode,connectParent
    if(len(outputs)):
        newnode = node(outputs[iterator][0],currentnode, Parents[-1])
        newnode.connectParent =connectParent
        Nodes.append(newnode)
        currentnode = newnode.getvalue() + 1
        Parents.append(newnode.getvalue())
        if(outputs[iterator][0]=="if"):
            if_stmt()
            Parents.pop()
        elif(outputs[iterator][0]=="repeat"):
            repeat_stmt()
            Parents.pop()
        elif(outputs[iterator][0]=="read"):
            read_stmt()
            Parents.pop()
        elif(outputs[iterator][0]=="write"):
            write_stmt()
            Parents.pop()
        else:
            Nodes[-1].value = "assign\n(" + outputs[iterator][0] + ")"
            assign_stmt()
            Parents.pop()
def if_stmt():
    global iterator,currentnode
    match("if")
    exp()
    match("then")
    stmtsequence()
    if(outputs[iterator][0]=="else"):
        match("else")
        stmtsequence()
    match("end")
def repeat_stmt():
    global iterator,currentnode
    match("repeat")
    stmtsequence()
    match("until")
    exp()
def read_stmt():
    global iterator,currentnode
    match("read")
    if(outputs[iterator][1]=="Identifier"):
        Nodes[-1].value = "read\n(" + outputs[iterator][0] + ")"
        match("Identifier")
def write_stmt():
    global iterator
    match("write")
    exp()
    return
def assign_stmt():
    global iterator,currentnode
    if(outputs[iterator][1]=="Identifier"):
        match("Identifier")
    match(":=")
    exp()
    return
def exp():
    global iterator,currentnode
    simple_exp()
    if (iterator < len(outputs)):
        if (outputs[iterator][0]=="<"or outputs[iterator][0]=="="):
            comparison_exp()
            simple_exp()
            Parents.pop()
    return
def simple_exp():
    global iterator,currentnode
    term()
    nestedOp=0
    if (iterator < len(outputs)):
        while (outputs[iterator][0]=="+"or outputs[iterator][0]=="-"):
            addop()
            term()
            nestedOp+=1
    while(nestedOp>0):
        Parents.pop()
        nestedOp-=1
    return
def comparison_exp():
    global iterator,currentnode
    newnode = node("Op\n("+outputs[iterator][0]+")",currentnode, Parents[-1])
    Nodes.append(newnode)
    Parents.append(newnode.getvalue())
    Nodes[currentnode-2].parentNode = Parents[-1]
    currentnode = newnode.getvalue() + 1
    if(outputs[iterator][0]=="<"):
        match("<")
    elif(outputs[iterator][0]=="="):
        match("=")
def addop():
    global iterator,currentnode
    newnode = node("Op\n("+outputs[iterator][0]+")",currentnode, Parents[-1])
    Nodes.append(newnode)
    Parents.append(newnode.getvalue())
    Nodes[currentnode-2].parentNode = Parents[-1]
    currentnode = newnode.getvalue() + 1
    if(outputs[iterator][0]=="+"):
        match("+")
    elif(outputs[iterator][0]=="-"):
        match("-")
def term():
    global iterator,currentnode
    factor()
    nestedOp=0
    if(iterator<len(outputs)):
        while (outputs[iterator][0] == "*"):
            mulop()
            factor()
            nestedOp += 1
    while(nestedOp>0):
        Parents.pop()
        nestedOp-=1
def mulop():
    global iterator,currentnode
    newnode = node("Op\n("+outputs[iterator][0]+")",currentnode, Parents[-1])
    Nodes.append(newnode)
    Parents.append(newnode.getvalue())
    Nodes[currentnode-2].parentNode = Parents[-1]
    currentnode = newnode.getvalue() + 1
    if(outputs[iterator][0]=="*"):
        match("*")
    elif(outputs[iterator][0]=="/"):
        match("/")
def factor():
    global iterator,currentnode
    if(outputs[iterator][1]=="Number"):
        newnode = node("const\n("+outputs[iterator][0]+")",currentnode, Parents[-1])
        Nodes.append(newnode)
        currentnode = newnode.getvalue() + 1
        match("Number")
    elif(outputs[iterator][1]=="Identifier"):
        newnode = node("Identifier\n("+outputs[iterator][0]+")",currentnode, Parents[-1])
        Nodes.append(newnode)
        currentnode = newnode.getvalue() + 1
        match("Identifier")
# def generate_tree():
#     global iterator,connectParent,currentnode
#     dot = Graph(comment='Syntax Tree',format = 'png')
#     for Node in Nodes:
#         if(Node.is_statment()):
#             dot.node(str(Node.Node),Node.value,shape='square')
#         else:
#             dot.node(str(Node.Node),Node.value)
#     for Node in Nodes:
#         if(Node.parentNode!=0)and (Node.connectParent):
#             dot.edge(str(Node.parentNode),str(Node.Node))
#         elif (Node.parentNode!=0):
#             dot.edge(str(Node.parentNode),str(Node.Node),style='dashed', color='white')
#     for number in range(len(Nodes)):
#         for number2 in range(number+1,len(Nodes)):
#             if((Nodes[number].parentNode==Nodes[number2].parentNode) and
#             (not Nodes[number2].connectParent)and
#             Nodes[number2].is_statment() and (Nodes[number].is_statment())):
#                 dot.edge(str(Nodes[number].Node),str(Nodes[number2].Node),constraint='false')
#                 break
#             elif((Nodes[number].parentNode==Nodes[number2].parentNode) and
#             (Nodes[number2].connectParent)and
#             Nodes[number2].is_statment() and (Nodes[number].is_statment())):
#                 break
#     dot.render('test-output/Syntax-Tree.gv',view=True)
#     while (len(outputs)):
#         outputs.pop()
#     while (len(Nodes)):
#         Nodes.pop()
#     iterator = 0
#     currentnode = 1
#     connectParent = True
#     return
