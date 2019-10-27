

def check_blank_line(obj):
  valid = 1
  non_blank_inputs = [obj.axiomEdit,obj.angleEdit,obj.itersEdit]
  if obj.madeAngle == True:
    non_blank_inputs.append(obj.turnAngleEdit)
  if obj.madeLine == True:
    non_blank_inputs.append(obj.lineScaleEdit)
  for rule in obj.prodrulesEdit:
    non_blank_inputs.append(rule)

  for input_box in non_blank_inputs:
    if input_box.valid == True and len(input_box.text()) == 0:
      print_error_message(input_box, "Blank input")
      valid=0
  return valid

def check_in_alphabet(obj):
  valid = 1
  obj.alphabetic_inputs = [obj.axiomEdit]
  prod_input = []
  for rule in obj.prodrulesEdit:
    prod_input.append(rule)
  for input_box in prod_input:
    if input_box.valid == True:
      for ch in input_box.text():
        if not ch in obj.alphabet and not ch in obj.ctrl_char and not ch == ':':
          print_error_message(input_box, ch + " not in obj.alphabet")
          valid=0
  for input_box in obj.alphabetic_inputs:
    if input_box.valid == True:
      for ch in input_box.text():
        if not ch in obj.alphabet and not ch in obj.ctrl_char:
          print_error_message(input_box, ch + " not in alphabet")
          valid=0
  return valid

def check_if_numeric(obj):
  valid = 1
  numeric_inputs = [ obj.angleEdit, obj.itersEdit]
  if obj.madeAngle == True:
    numeric_inputs.append(obj.turnAngleEdit)
  if obj.madeLine == True:
    numeric_inputs.append(obj.lineScaleEdit)
  for input in numeric_inputs:
    if input.valid==True:
      try:
        float(input.text())
      except:
        print_error_message(input,"Not a number")
        valid = 0
  return valid

def check_valid_numeric(obj):
  valid = 1
  angle_input = [obj.angleEdit]
  if obj.madeAngle == True:
    angle_input.append(obj.madeAngle)
  for input in angle_input:
    if input.valid == True and (float(input.text()) >360 or float(input.text())<-360):
      print_error_message(input,"Not a valid angle")
      valid = 0
  positive_input = [obj.itersEdit]
  if obj.madeLine == True:
    positive_input.append(obj.lineScaleEdit)
  for input in positive_input:
    if input.valid == True and float(input.text()) <= 0:
      print_error_message(obj.itersEdit,"Not a valid number of iterations")
      valid = 0
  return valid

def check_prod_rule_format(obj):
  valid = 1
  for input_box in obj.prodrulesEdit:
    if input_box.valid and not ':' in input_box.text():
      print_error_message(input_box," Missing : ")
      valid = 0
  return valid

def check_branching(obj):
  valid = 1
  stack = []
  if obj.axiomEdit.valid:
    for ch in obj.axiomEdit.text():
      if ch == '[':
        stack.append("[")
      if ch == ']':
        if len(stack) == 0:
          print_error_message(obj.axiomEdit,"Must have matching [ ]")
          valid=0
        else:
          stack.pop()
      if len(stack)>0:
        print_error_message(obj.axiomEdit,"Must have matching [ ]")
        valid = 0

  for input_box in obj.prodrulesEdit:
    if input_box.valid:
      text = input_box.text().split(":")
      if '[' in text[0] or ']' in text[0]:
        print_error_message(input_box, "Can't have [ ] in key")
      stack = []
      for ch in text[1]:
        if ch == '[':
          stack.append("[")
        if ch == ']':
          if len(stack) == 0:
            print_error_message(input_box,"Must have matching [ ]")
            valid=0
          else:
            stack.pop()
      if len(stack)>0:
        print_error_message(input_box,"Must have matching [ ]")
        valid = 0
  return valid


def input_check(obj):
  valid = []

  valid.append(check_blank_line(obj))

  valid.append(check_in_alphabet(obj))
  valid.append(check_if_numeric(obj))
  valid.append(check_valid_numeric(obj))
  valid.append(check_prod_rule_format(obj))
  valid.append(check_branching(obj))
  #reset valid
  obj.axiomEdit.valid = 1
  obj.angleEdit.valid = 1
  if obj.madeAngle == True:
    obj.turnAngleEdit.valid =1
  if obj.madeLine:
    obj.lineScaleEdit.valid = 1
  obj.itersEdit.valid = 1
  for input_box in obj.prodrulesEdit:
    input_box.valid = 1
  return (sum(valid) == len(valid))


def print_error_message(obj,msg):
  obj.setStyleSheet("color: red;")
  print("[ Error ] ",msg)
  obj.valid = False
