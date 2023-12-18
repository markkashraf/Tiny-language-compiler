from graphviz import Graph

def is_str(token):
    return token.isalpha()


def is_num(token):
    return token.isdigit()


def is_col(c):
    return True if c == ':' else False


def is_symbol(token):
    symbol = ['+', '-', '*', '/', '=', '<', '>', '(', ')', ';']
    return True if token in symbol else False


def is_comment(token):
    if token[0] == '{' or token[-1] == '}':
        return True
    else:
        return False


def get_file_text(file_name):
    with open(file_name, 'r') as f:
        input_text = f.read()
        input_text = input_text.replace('\n', ' ')
        input_text += ' '
        return input_text



def generate_Parse_Tree(Nodes,tokens):
    global iterator,connectParent,currentnode
    dot = Graph(comment='Syntax Tree',format = 'png')
    for Node in Nodes:
        if(Node.is_statment()):
            dot.node(str(Node.id),Node.value,shape='square')
        else:
            dot.node(str(Node.id),Node.value)
    for Node in Nodes:
        if(Node.parent_id!=0)and (Node.connect_Parent):
            dot.edge(str(Node.parent_id),str(Node.id))
        elif (Node.parent_id!=0):
            dot.edge(str(Node.parent_id),str(Node.id),style='dashed', color='white')
    for number in range(len(Nodes)):
        for number2 in range(number+1,len(Nodes)):
            if((Nodes[number].parent_id==Nodes[number2].parent_id) and
            (not Nodes[number2].connect_Parent)and
            Nodes[number2].is_statment() and (Nodes[number].is_statment())):
                dot.edge(str(Nodes[number].id),str(Nodes[number2].id),constraint='false')
                break
            elif((Nodes[number].parent_id==Nodes[number2].parent_id) and
                 (Nodes[number2].connect_Parent) and
                 Nodes[number2].is_statment() and (Nodes[number].is_statment())):
                break
    dot.render('Syntax-Tree.gv',view=True)
    while (len(tokens)):
        tokens.pop()
    while (len(Nodes)):
        Nodes.pop()

    return