
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'COMMA DROP EQUAL IDENTIFIER LPAREN NUMBER RPAREN SPLITstatement : expressionexpression : DROP LPAREN IDENTIFIER COMMA NUMBER RPAREN'
    
_lr_action_items = {'DROP':([0,],[3,]),'$end':([1,2,8,],[0,-1,-2,]),'LPAREN':([3,],[4,]),'IDENTIFIER':([4,],[5,]),'COMMA':([5,],[6,]),'NUMBER':([6,],[7,]),'RPAREN':([7,],[8,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement':([0,],[1,]),'expression':([0,],[2,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> expression','statement',1,'p_statement_expr','playground.py',52),
  ('expression -> DROP LPAREN IDENTIFIER COMMA NUMBER RPAREN','expression',6,'p_expression_drop','playground.py',57),
]
