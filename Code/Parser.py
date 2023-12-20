from Code.Tree_node import Tree_node
from Code import Util


class Parser:

    def __init__(self):
        self.tokens = []
        self.iterator = 0
        self.Nodes = []
        self.Parents = []
        self.Parents.append(0)
        self.error = False
        self.current_node_id = 1
        self.connect_Parent = True
        self.nested_op = 0
        self.nested_parents_to_pop = 0

    def match(self, expectedtoken):
        if (self.tokens[self.iterator][0] == expectedtoken) or (self.tokens[self.iterator][1] == expectedtoken):
            self.iterator += 1
        else:
            raise ValueError()

    def program(self):
        self.stmtsequence()
        if (self.iterator < len(self.tokens)):
            raise ValueError()

    def stmtsequence(self):

        self.connect_Parent = True
        self.statment()

        while self.iterator < len(self.tokens) and self.tokens[self.iterator][0] == ';':

            self.connect_Parent = False
            self.match(";")
            if self.iterator >= len(self.tokens):
                raise ValueError()
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
        if (self.iterator < len(self.tokens)):
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
        self.Nodes[-1].value = "read\n(" + self.tokens[self.iterator][0] + ")"
        self.match("IDENTIFIER")

    def write_stmt(self):
        self.match("write")
        if (not (self.tokens[self.iterator][1] == "IDENTIFIER" or
                 self.tokens[self.iterator][1] == "NUMBER" or self.tokens[self.iterator][0] == '(')):
            raise ValueError()

        self.exp()
        return

    def assign_stmt(self):
        self.match("IDENTIFIER")
        self.match(":=")
        self.exp()
        return

    def exp(self):

        self.simple_exp()
        self.nested_op = 0
        if (self.iterator < len(self.tokens)):
            if (self.tokens[self.iterator][0] == "<" or self.tokens[self.iterator][0] == "="):
                self.comparison_exp()
                self.simple_exp()
                self.Parents.pop()
        return

    def simple_exp(self):

        self.term()
        while ((self.iterator < len(self.tokens)) and (
                self.tokens[self.iterator][0] == "+" or self.tokens[self.iterator][0] == "-")):
            self.addop()
            self.term()
            self.nested_parents_to_pop += 1
            if self.iterator < len(self.tokens):

                if (self.tokens[self.iterator][0] == "+" or self.tokens[self.iterator][0] == "-" or
                        self.tokens[self.iterator][0] == "*" or self.tokens[self.iterator][0] == "/"):
                    self.nested_op += 1
                else:
                    self.nested_op = 0

        while self.nested_parents_to_pop > 0 and self.nested_op == 0:
            self.Parents.pop()
            self.nested_parents_to_pop -= 1
        return

    def comparison_exp(self):

        newnode = Tree_node("Op\n(" + self.tokens[self.iterator][0] + ")", self.current_node_id, self.Parents[-1])
        self.Nodes.append(newnode)
        self.Parents.append(newnode.get_id())
        self.Nodes[self.current_node_id - 2].parent_id = self.Parents[-1]
        self.current_node_id = newnode.get_id() + 1
        if (self.tokens[self.iterator][0] == "<"):

            if Util.check_left(self.tokens, self.iterator) and Util.check_right(self.tokens, self.iterator):
                self.match("<")
            else:
                raise ValueError()

        elif (self.tokens[self.iterator][0] == "="):

            if Util.check_left(self.tokens, self.iterator) and Util.check_right(self.tokens, self.iterator):
                self.match("=")
            else:
                raise ValueError()

    def addop(self):

        newnode = Tree_node("Op\n(" + self.tokens[self.iterator][0] + ")", self.current_node_id, self.Parents[-1])
        self.Nodes.append(newnode)
        self.Parents.append(newnode.get_id())

        if self.nested_op > 0:
            self.Nodes[self.current_node_id - 3].parent_id = self.Parents[-1]
            self.Nodes[self.current_node_id - 1].parent_id = self.Parents[-3 - (self.nested_op - 1)]
        else:
            self.Nodes[self.current_node_id - 2].parent_id = self.Parents[-1]

        self.current_node_id = newnode.get_id() + 1

        if (self.tokens[self.iterator][0] == "+"):
            if Util.check_left(self.tokens, self.iterator) and Util.check_right(self.tokens, self.iterator):
                self.match("+")
            else:
                raise ValueError()

        elif (self.tokens[self.iterator][0] == "-"):
            if Util.check_left(self.tokens, self.iterator) and Util.check_right(self.tokens, self.iterator):
                self.match("-")
            else:
                raise ValueError()

    def term(self):

        self.factor()

        while ((self.iterator < len(self.tokens)) and (
                self.tokens[self.iterator][0] == "*" or self.tokens[self.iterator][0] == "/")):

            self.mulop()
            self.factor()
            self.nested_parents_to_pop += 1
            if self.iterator < len(self.tokens):

                if (self.tokens[self.iterator][0] == "*" or self.tokens[self.iterator][0] == "/" or
                        self.tokens[self.iterator][0] == "+" or self.tokens[self.iterator][0] == "-"):
                    self.nested_op += 1
                else:
                    self.nested_op = 0

        while self.nested_parents_to_pop > 0 and self.nested_op == 0:
            self.Parents.pop()
            self.nested_parents_to_pop -= 1

    def mulop(self):

        newnode = Tree_node("Op\n(" + self.tokens[self.iterator][0] + ")", self.current_node_id, self.Parents[-1])
        self.Nodes.append(newnode)
        self.Parents.append(newnode.get_id())

        if self.nested_op > 0:
            self.Nodes[self.current_node_id - 3].parent_id = self.Parents[-1]
            self.Nodes[self.current_node_id - 1].parent_id = self.Parents[-3 - (self.nested_op - 1)]
        else:
            self.Nodes[self.current_node_id - 2].parent_id = self.Parents[-1]
        self.current_node_id = newnode.get_id() + 1
        if (self.tokens[self.iterator][0] == "*"):
            if Util.check_left(self.tokens, self.iterator) and Util.check_right(self.tokens, self.iterator):
                self.match("*")
            else:
                raise ValueError()
        elif (self.tokens[self.iterator][0] == "/"):
            if Util.check_left(self.tokens, self.iterator) and Util.check_right(self.tokens, self.iterator):
                self.match("/")
            else:
                raise ValueError()

    def factor(self):

        if (self.iterator < len(self.tokens)):

            if (self.tokens[self.iterator][0] == "("):
                self.match("(")
                self.exp()
                self.match(")")
            elif (self.tokens[self.iterator][1] == "NUMBER"):
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
