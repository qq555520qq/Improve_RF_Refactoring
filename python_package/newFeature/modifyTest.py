import ast
from robot.api import get_model, get_resource_model, Token


class KeywordRenamer(ast.NodeVisitor):

    def __init__(self, old_name, new_name):
        self.old_name = self.normalize(old_name)
        self.new_name = new_name

    def normalize(self, name):
        return name.lower().replace(' ', '').replace('_', '')

    def visit_KeywordName(self, node):
        # Rename keyword definitions.
        if self.normalize(node.name) == self.old_name:
            token = node.get_token(Token.KEYWORD_NAME)
            token.value = self.new_name

    def visit_KeywordCall(self, node):
        # Rename keyword usages.
        if self.normalize(node.keyword) == self.old_name:
            token = node.get_token(Token.KEYWORD)
            token.value = self.new_name

model = get_resource_model('C:/Users/Gene/Desktop/test_automation/RobotTests/keywords/assets.txt')
renamer = KeywordRenamer('New Name', 'Keyword')
renamer.visit(model)
# model.save()