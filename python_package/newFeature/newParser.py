import ast
from robot.api import get_model, get_resource_model


class TestNamePrinter(ast.NodeVisitor):

    # def visit_File(self, node):
    #     print(f"File '{node.source}' has following tests:")
    #     # Must call `generic_visit` to visit also child nodes.
    #     self.generic_visit(node)

    # def visit_TestCaseName(self, node):
    #     print(f"- {node.name} (on line {node.lineno})")
    
    def visit_Teardown(self, node):
        print(node.args)
        # self.generic_visit(node)


# model = get_model('../test_data/suite1/add sprint.robot')
model = get_resource_model('../test_data/ezScrum.txt')
printer = TestNamePrinter()
printer.visit(model)