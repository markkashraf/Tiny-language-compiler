from Code.Tree_node import Tree_node


class Parser:

    def __init__(self):
        self.tokens = []
        self.iterator = 0
        self.Nodes = []
        self.Parents = []
        self.Parents.append(0)

        self.current_node_id = 1
        self.connect_Parent = True

    def match(self, expectedtoken):
        if (self.tokens[self.iterator][0] == expectedtoken) or (self.tokens[self.iterator][1] == expectedtoken):
            self.iterator += 1
        else:
            self.iterator = -1

    def program(self):
        self.stmtsequence()

    def stmtsequence(self):
        self.connect_Parent = True
        self.statment()

        while (self.iterator < len(self.tokens) and self.tokens[self.iterator][0] == ';'):
            self.connect_Parent = False
            self.match(";")
            self.statment()

    def statment(self):

        if (len(self.tokens)):
            newnode = Tree_node(self.tokens[self.iterator][0], self.current_node_id, self.Parents[-1])
            newnode.connect_Parent = self.connect_Parent
            self.Nodes.append(newnode)
            self.current_node_id = newnode.get_id() + 1
            self.Parents.append(newnode.get_id())
            if (self.tokens[self.iterator][0] == "if"):
                self.if_stmt()
                self.Parents.pop()
            elif (self.tokens[self.iterator][0] == "repeat"):
                self.repeat_stmt()
                self.Parents.pop()
            elif (self.tokens[self.iterator][0] == "read"):
                self.read_stmt()
                self.Parents.pop()
            elif (self.tokens[self.iterator][0] == "write"):
                self.write_stmt()
                self.Parents.pop()
            else:
                self.Nodes[-1].value = "assign\n(" + self.tokens[self.iterator][0] + ")"
                self.assign_stmt()
                self.Parents.pop()

    def if_stmt(self):
        self.match("if")
        self.exp()
        self.match("then")
        self.stmtsequence()
        if (self.tokens[self.iterator][0] == "else"):
            self.match("else")
            self.stmtsequence()
        self.match("end")

    def repeat_stmt(self):
        self.match("repeat")
        self.stmtsequence()
        self.match("until")
        self.exp()

    def read_stmt(self):
        self.match("read")
        if (self.tokens[self.iterator][1] == "IDENTIFIER"):
            self.Nodes[-1].value = "read\n(" + self.tokens[self.iterator][0] + ")"
            self.match("IDENTIFIER")

    def write_stmt(self):

        self.match("write")
        self.exp()
        return

    def assign_stmt(self):
        if (self.tokens[self.iterator][1] == "IDENTIFIER"):
            self.match("IDENTIFIER")
        self.match(":=")
        self.exp()
        return

    def exp(self):

        self.simple_exp()
        if (self.iterator < len(self.tokens)):
            if (self.tokens[self.iterator][0] == "<" or self.tokens[self.iterator][0] == "="):
                self.comparison_exp()
                self.simple_exp()
                self.Parents.pop()
        return

    def simple_exp(self):

        self.term()
        nestedOp = 0
        if (self.iterator < len(self.tokens)):
            while (self.tokens[self.iterator][0] == "+" or self.tokens[self.iterator][0] == "-"):
                self.addop()
                self.term()
                nestedOp += 1
        while (nestedOp > 0):
            self.Parents.pop()
            nestedOp -= 1
        return

    def comparison_exp(self):

        newnode = Tree_node("Op\n(" + self.tokens[self.iterator][0] + ")", self.current_node_id, self.Parents[-1])
        self.Nodes.append(newnode)
        self.Parents.append(newnode.get_id())
        self.Nodes[self.current_node_id - 2].parentNode = self.Parents[-1]
        self.current_node_id = newnode.get_id() + 1
        if (self.tokens[self.iterator][0] == "<"):
            self.match("<")
        elif (self.tokens[self.iterator][0] == "="):
            self.match("=")

    def addop(self):

        newnode = Tree_node("Op\n(" + self.tokens[self.iterator][0] + ")", self.current_node_id, self.Parents[-1])
        self.Nodes.append(newnode)
        self.Parents.append(newnode.get_id())
        self.Nodes[self.current_node_id - 2].parentNode = self.Parents[-1]
        self.current_node_id = newnode.get_id() + 1
        if (self.tokens[self.iterator][0] == "+"):
            self.match("+")
        elif (self.tokens[self.iterator][0] == "-"):
            self.match("-")

    def term(self):

        self.factor()
        nestedOp = 0
        if (self.iterator < len(self.tokens)):
            while (self.tokens[self.iterator][0] == "*"):
                self.mulop()
                self.factor()
                nestedOp += 1
        while (nestedOp > 0):
            self.Parents.pop()
            nestedOp -= 1

    def mulop(self):

        newnode = Tree_node("Op\n(" + self.tokens[self.iterator][0] + ")", self.current_node_id, self.Parents[-1])
        self.Nodes.append(newnode)
        self.Parents.append(newnode.get_id())
        self.Nodes[self.current_node_id - 2].parentNode = self.Parents[-1]
        self.current_node_id = newnode.get_id() + 1
        if (self.tokens[self.iterator][0] == "*"):
            self.match("*")
        elif (self.tokens[self.iterator][0] == "/"):
            self.match("/")

    def factor(self):

        if (self.tokens[self.iterator][1] == "NUMBER"):
            newnode = Tree_node("const\n(" + self.tokens[self.iterator][0] + ")", self.current_node_id,
                                self.Parents[-1])
            self.Nodes.append(newnode)
            self.current_node_id = newnode.get_id() + 1
            self.match("NUMBER")
        elif (self.tokens[self.iterator][1] == "IDENTIFIER"):
            newnode = Tree_node("Identifier\n(" + self.tokens[self.iterator][0] + ")", self.current_node_id,
                                self.Parents[-1])
            self.Nodes.append(newnode)
            self.current_node_id = newnode.get_id() + 1
            self.match("IDENTIFIER")
