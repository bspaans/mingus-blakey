
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.5'

_lr_method = 'LALR'

_lr_signature = '5AB4A123D90BD6B1A77AFDA73B047908'
    
_lr_action_items = {'IDENT':([6,7,],[8,9,]),'SEQUENCE':([0,],[1,]),'PATTERN':([0,],[5,]),'NEWLINE':([8,],[12,]),'COLON':([1,5,],[6,7,]),'INTEGER':([7,],[11,]),'$end':([2,3,4,9,10,11,12,],[-2,-1,0,-6,-4,-5,-3,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'pattern':([0,],[2,]),'value':([7,],[10,]),'statement':([0,],[4,]),'sequence':([0,],[3,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> sequence','statement',1,'p_statements','yacc.py',24),
  ('statement -> pattern','statement',1,'p_statements','yacc.py',25),
  ('sequence -> SEQUENCE COLON IDENT NEWLINE','sequence',4,'p_sequence','yacc.py',29),
  ('pattern -> PATTERN COLON value','pattern',3,'p_pattern','yacc.py',33),
  ('value -> INTEGER','value',1,'p_value_integer','yacc.py',37),
  ('value -> IDENT','value',1,'p_value_integer','yacc.py',38),
]
