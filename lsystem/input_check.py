
alphabet = ["F","f","G","g","H","h","-","+","[","]","|", "(", ")", ">", "<"]
ctrl_char = ['A','B','C','D','E','I','J','K','L,','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
error_message = "X"

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
  alphabetic_inputs = [obj.axiomEdit]
  for rule in obj.prodrulesEdit:
    alphabetic_inputs.append(rule)
  for input_box in alphabetic_inputs:
    if input_box.valid == True:
      for ch in input_box.text():
        if not ch in alphabet and not ch in ctrl_char:
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
def input_check(obj):
  valid = []
  valid.append(check_blank_line(obj))

  valid.append(check_in_alphabet(obj))
  valid.append(check_if_numeric(obj))
  valid.append(check_valid_numeric(obj))
  valid.append(check_prod_rule_format(obj))

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

def check_prod_rule_format(obj):
  valid = 1
  for input_box in obj.prodrulesEdit:
    if input_box.valid and not ':' in input_box.text():
      print_error_message(input_box," Missing : ")
      valid = 0
  return valid
def Input_check(obj):
  '''  This function checks the input
     Returns 1 if valid
     Returns 0 otherwise
  '''
  boxes = {}
  axiomInput = obj.axiomEdit.text()
  angleInput = obj.angleEdit.text()
  turnAngleInput = obj.turnAngleEdit.text()
  lineScaleInput = obj.lineScaleEdit.text()
  itersInput = obj.itersEdit.text()
  prodRulesArr = obj.prodrulesEdit

  ctrl_char_lhs=[] #control chars that are on the left hand side of a rule
  valid_input = 1

  string = 0
  if len(axiomInput)==0:
    print_error_message(obj.axiomEdit)
    valid_input = 0
  for ch in axiomInput:
    if not (ch in alphabet or ch in ctrl_char):
      print("[ ERROR ] ",ch," not in alphabet")
      obj.axiomEdit.setStyleSheet("color: red;")
      obj.axiomEdit.setText(error_message)
      valid_input = 0
  axiomInProd = 0

  for prod in obj.prodrulesEdit:
    prodInput = prod.text()
    prodInput=prodInput.replace(' ','')
    prodInputarr = prodInput.split("->")

    if not '->' in prodInput:
      prod.setStyleSheet("color: red;")
      prod.setText(error_message)
      valid_input = 0
    tmp_prodRule = prodInput.replace('->','')
    stack = []
    prevCh=''
    for ch in tmp_prodRule:
      if ch == '[':
        stack.append(ch)
      if ch == ']':
        if prevCh =='[':
            print("[ ERROR ] Branches should be non-empty")
            prod.setStyleSheet("color: red;")
            prod.setText(error_message)
            valid_input = 0
        if len(stack)==0:
          print("[ ERROR ] Each production rule must have balanced brackets")
          prod.setStyleSheet("color: red;")
          prod.setText(error_message)
          valid_input = 0
        else:
          stack.pop()
      if not (ch in alphabet or ch in ctrl_char):
        prod.setStyleSheet("color: red;")
        prod.setText(error_message)
        valid_input = 0
      prevCh=ch
    if len(stack)!=0:
      print("[ ERROR ] Each production rule must have balanced brackets")
      prod.setStyleSheet("color: red;")
      prod.setText(error_message)
      valid_input = 0
    tmp_prodRule = prodInput.split('->')
    for ch in tmp_prodRule[0]:
      if ch in ctrl_char:
        ctrl_char_lhs.append(ch)
  for prod in obj.prodrulesEdit:
    tmp_prodRule = prodInput.split('->')
    for ch in tmp_prodRule[1]:
      if ch in ctrl_char and not ch in ctrl_char_lhs:
        print("[ ERROR ] Control characters must be the key to a rule")
        prod.setStyleSheet("color: red;")
        prod.setText(error_message)
        valid_input = 0
  for ch in axiomInput:
    if ch in ctrl_char and not ch in ctrl_char_lhs:
      print("[ ERROR ] Control characters must be the key to a rule")
      obj.axiomEdit.setStyleSheet("color: red;")
      obj.axiomEdit.setText(error_message)
      valid_input = 0
  try:
    angleInput = float(angleInput)
  except:
    obj.angleEdit.setStyleSheet("color: red;")
    obj.angleEdit.setText("X")
    valid_input=0
    string = 1 #is a string
  if not string:
    if angleInput <= -360 or angleInput >= 360:
      obj.angleEdit.setStyleSheet("color: red;")
      obj.angleEdit.setText(error_message)
      valid_input = 0

  try:
    turnAngleInput = float(turnAngleInput)
  except:
    obj.turnAngleEdit.setStyleSheet("color: red;")
    obj.turnAngleEdit.setText("X")
    valid_input=0
    string = 1 #is a string
  if not string:
    if turnAngleInput <= -360 or turnAngleInput >= 360:
      obj.turnAngleEdit.setStyleSheet("color: red;")
      obj.turnAngleEdit.setText(error_message)
      valid_input = 0

  try:
    lineScaleInput = float(lineScaleInput)
  except:
    obj.lineScaleEdit.setStyleSheet("color: red;")
    obj.lineScaleEdit.setText(error_message)
    valid_input = 0
    string = 1 #is a string
  if not string:
    if lineScaleInput <= 0:
      obj.lineScaleEdit.setStyleSheet("color: red;")
      obj.lineScaleEdit.setText(error_message)
      valid_input = 0

  try:
    itersInput = int(itersInput)
  except:
    obj.itersEdit.setStyleSheet("color: red;")
    obj.itersEdit.setText(error_message)
    valid_input = 0
    string = 1 #is a string
  if not string:
    if itersInput <= 0:
      obj.itersEdit.setStyleSheet("color: red;")
      obj.itersEdit.setText(error_message)
      valid_input = 0
  return valid_input

def print_error_message(obj,msg):
  obj.setStyleSheet("color: red;")
  obj.setText(error_message)
  print("[ Error ] ",msg)
  obj.valid = False
