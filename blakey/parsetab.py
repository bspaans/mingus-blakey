
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.5'

_lr_method = 'LALR'

_lr_signature = '7F1DFD322D8FF4B8B35FBF4677970FD2'
    
_lr_action_items = {'IDENT':([17,19,20,41,],[26,30,33,33,]),'SEQUENCE':([0,21,23,],[13,13,13,]),'PATTERN':([0,21,23,],[2,2,2,]),'NEWLINE':([0,5,6,7,9,10,12,14,20,21,23,24,26,27,28,29,30,31,32,33,35,37,38,39,40,41,42,43,44,],[-4,-5,-7,-6,20,21,23,24,-4,-4,-4,-4,-20,-16,-19,-21,-9,-8,-14,41,-23,-15,-18,42,-22,-4,-4,-13,-17,]),'BPM':([0,21,23,],[3,3,3,]),'CHOICE':([0,21,23,],[15,15,15,]),'PATTERN_LINE':([24,42,],[39,39,]),'COMBINE':([0,21,23,],[4,4,4,]),'INTEGER':([17,18,22,25,],[28,29,35,40,]),'COLON':([2,3,4,8,11,13,15,16,],[17,18,-11,19,22,-10,-12,25,]),'RESOLUTION':([0,21,23,],[11,11,11,]),'LOOP':([0,21,23,],[16,16,16,]),'$end':([0,1,12,21,23,34,36,],[-4,0,-3,-4,-4,-1,-2,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statements':([0,21,23,],[1,34,36,]),'pattern_body':([24,42,],[37,44,]),'section_type':([0,21,23,],[8,8,8,]),'section':([0,21,23,],[7,7,7,]),'pattern_header':([0,21,23,],[14,14,14,]),'var_decl':([0,21,23,],[5,5,5,]),'section_body':([20,41,],[31,43,]),'section_header':([0,21,23,],[9,9,9,]),'value':([17,],[27,]),'statement':([0,21,23,],[10,10,10,]),'pattern':([0,21,23,],[6,6,6,]),'empty':([0,20,21,23,24,41,42,],[12,32,12,12,38,32,38,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statements","S'",1,None,None,None),
  ('statements -> statement NEWLINE statements','statements',3,'p_statements','yacc.py',46),
  ('statements -> empty NEWLINE statements','statements',3,'p_statements','yacc.py',47),
  ('statements -> empty','statements',1,'p_statements','yacc.py',48),
  ('empty -> <empty>','empty',0,'p_empty','yacc.py',53),
  ('statement -> var_decl','statement',1,'p_statement','yacc.py',57),
  ('statement -> section','statement',1,'p_statement','yacc.py',58),
  ('statement -> pattern','statement',1,'p_statement','yacc.py',59),
  ('section -> section_header NEWLINE section_body','section',3,'p_section','yacc.py',63),
  ('section_header -> section_type COLON IDENT','section_header',3,'p_section_header','yacc.py',68),
  ('section_type -> SEQUENCE','section_type',1,'p_section_type','yacc.py',74),
  ('section_type -> COMBINE','section_type',1,'p_section_type','yacc.py',75),
  ('section_type -> CHOICE','section_type',1,'p_section_type','yacc.py',76),
  ('section_body -> IDENT NEWLINE section_body','section_body',3,'p_section_body','yacc.py',80),
  ('section_body -> empty','section_body',1,'p_section_body','yacc.py',81),
  ('pattern -> pattern_header NEWLINE pattern_body','pattern',3,'p_pattern','yacc.py',86),
  ('pattern_header -> PATTERN COLON value','pattern_header',3,'p_pattern_header','yacc.py',90),
  ('pattern_body -> PATTERN_LINE NEWLINE pattern_body','pattern_body',3,'p_pattern_body','yacc.py',94),
  ('pattern_body -> empty','pattern_body',1,'p_pattern_body','yacc.py',95),
  ('value -> INTEGER','value',1,'p_value_integer','yacc.py',101),
  ('value -> IDENT','value',1,'p_value_integer','yacc.py',102),
  ('var_decl -> BPM COLON INTEGER','var_decl',3,'p_var_decl','yacc.py',106),
  ('var_decl -> LOOP COLON INTEGER','var_decl',3,'p_var_decl','yacc.py',107),
  ('var_decl -> RESOLUTION COLON INTEGER','var_decl',3,'p_var_decl','yacc.py',108),
]
