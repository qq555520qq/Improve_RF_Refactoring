import ast
from robot.api import get_model, Token
from robot.parsing.model import SettingSection, Statement


class TestModifier(ast.NodeTransformer):

    def visit_TestCase(self, node):
        # The matched `TestCase` node is a block with `header` and `body`
        # attributes. `header` is a statement with familiar `get_token` and
        # `get_value` methods for getting certain tokens or their value.
        name = node.header.get_value(Token.TESTCASE_NAME)
        # Returning `None` drops the node altogether i.e. removes this test.
        if name == 'Second example':
            return None
        # Construct new keyword call statement from tokens.
        new_keyword = Statement.from_tokens([
            Token(Token.SEPARATOR, '    '),
            Token(Token.KEYWORD, 'New Keyword'),
            Token(Token.SEPARATOR, '    '),
            Token(Token.ARGUMENT, 'xxx'),
            Token(Token.EOL, '\n')
        ])
        # Add the keyword call to test as the second item. `body` is a list.
        node.body.insert(1, new_keyword)
        # No need to call `generic_visit` because we are not modifying child
        # nodes. The node itself must to be returned to avoid dropping it.
        return node

    def visit_File(self, node):
        # Create settings section with documentation.
        setting_header = Statement.from_tokens([
            Token(Token.SETTING_HEADER, '*** Settings ***'),
            Token(Token.EOL, '\n')
        ])
        documentation = Statement.from_tokens([
            Token(Token.DOCUMENTATION, 'Documentation'),
            Token(Token.SEPARATOR, '    '),
            Token(Token.ARGUMENT, 'This is getting pretty advanced'),
            Token(Token.EOL, '\n'),
            Token(Token.CONTINUATION, '...'),
            Token(Token.SEPARATOR, '    '),
            Token(Token.ARGUMENT, 'and this API definitely could be better.'),
            Token(Token.EOL, '\n')
        ])
        empty_line = Statement.from_tokens([
            Token(Token.EOL, '\n')
        ])
        body = [documentation, empty_line]
        settings = SettingSection(setting_header, body)
        # Add settings to the beginning of the file.
        node.sections.insert(0, settings)
        # Must call `generic_visit` to visit also child nodes.
        return self.generic_visit(node)


model = get_model('example.robot')
modifier = TestModifier()
modifier.visit(model)
model.save()