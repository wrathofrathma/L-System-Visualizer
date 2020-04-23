def check_blank_line(obj):
    """Determines if the inputs are blank"""
    valid = 1
    non_blank_inputs = [obj.axiom_edit, obj.angle_edit, obj.iters_edit]
    if obj.made_angle == True:
        non_blank_inputs.append(obj.turn_angle_edit)
    if obj.made_line == True:
        non_blank_inputs.append(obj.line_scale_edit)
    for rule in obj.prod_rules_edit:
        non_blank_inputs.append(rule)

    for input_box in non_blank_inputs:
        if input_box.valid == True and len(input_box.text()) == 0:
            print_error_message(input_box, "Blank input")
            valid = 0
    return valid


def check_in_alphabet(obj):
    """determines if the characters are in the alphabet"""
    valid = 1
    obj.alphabetic_inputs = [obj.axiom_edit]
    prod_input = []
    for rule in obj.prod_rules_edit:
        prod_input.append(rule)
    for input_box in prod_input:
        if input_box.valid == True:
            for ch in input_box.text():
                if obj.graphix == obj.three_d and (ch =='H' or ch =='h'):
                    print_error_message(input_box, ch+" not allowed for 3D")
                    valid =0
                if not ch in obj.alphabet and not ch in obj.ctrl_char and not ch == ':':
                    print_error_message(input_box, ch + " not in obj.alphabet")
                    valid = 0
    for input_box in obj.alphabetic_inputs:
        if input_box.valid == True:
            for ch in input_box.text():
                if obj.graphix == obj.three_d and (ch =='H' or ch =='h'):
                    print_error_message(input_box, ch+" not allowed for 3D")
                    valid =0
                if not ch in obj.alphabet and not ch in obj.ctrl_char:
                    print_error_message(input_box, ch + " not in alphabet")
                    valid = 0
    return valid


def check_if_numeric(obj):
    """determines if the inputs are numeric"""
    valid = 1
    numeric_inputs = [obj.angle_edit, obj.iters_edit]
    if obj.made_angle == True:
        numeric_inputs.append(obj.turn_angle_edit)
    if obj.made_line == True:
        numeric_inputs.append(obj.line_scale_edit)
    for input in numeric_inputs:
        if input.valid == True:
            try:
                float(input.text())
            except:
                print_error_message(input, "Not a number")
                valid = 0
    return valid


def check_valid_numeric(obj):
    """determines if the numbers are valid"""
    valid = 1
    angle_input = [obj.angle_edit]
    if obj.made_angle == True:
        angle_input.append(obj.turn_angle_edit)
    for input in angle_input:
        if input.valid == True and (float(input.text()) > 360 or float(input.text()) < -360):
            print_error_message(input, "Not a valid angle")
            valid = 0
    positive_input = [obj.iters_edit]
    if obj.made_line == True:
        positive_input.append(obj.line_scale_edit)
    for input in positive_input:
        if input.valid == True and float(input.text()) <= 0:
            print_error_message(obj.iters_edit, "Not a valid number of iterations")
            valid = 0
    return valid


def check_prod_rule_format(obj):
    """determines if the production rules are in the proper format"""
    valid = 1
    for input_box in obj.prod_rules_edit:
        if input_box.valid and not ':' in input_box.text():
            print_error_message(input_box, " Missing : ")
            valid = 0
    return valid


def check_branching(obj):
    """determines if there is branching and if it is in a valid syntax"""
    valid = 1
    stack = []
    if obj.axiom_edit.valid:
        for ch in obj.axiom_edit.text():
            if ch == '[':
                stack.append("[")
            if ch == ']':
                if len(stack) == 0:
                    print_error_message(obj.axiom_edit, "Must have matching [ ]")
                    valid = 0
                else:
                    stack.pop()
            if len(stack) > 0:
                print_error_message(obj.axiom_edit, "Must have matching [ ]")
                valid = 0

    for input_box in obj.prod_rules_edit:
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
                        print_error_message(input_box, "Must have matching [ ]")
                        valid = 0
                    else:
                        stack.pop()
            if len(stack) > 0:
                print_error_message(input_box, "Must have matching [ ]")
                valid = 0
    return valid


def input_check(obj):
    """collects all the input checks and determines if they are valid"""
    valid = []

    valid.append(check_blank_line(obj))
    valid.append(check_in_alphabet(obj))
    valid.append(check_if_numeric(obj))
    valid.append(check_valid_numeric(obj))
    valid.append(check_prod_rule_format(obj))
    valid.append(check_branching(obj))
    valid.append(check_nd(obj))
    # reset valid
    obj.axiom_edit.valid = 1
    obj.angle_edit.valid = 1
    if obj.made_angle == True:
        obj.turn_angle_edit.valid = 1
    if obj.made_line:
        obj.line_scale_edit.valid = 1
    obj.iters_edit.valid = 1
    for input_box in obj.prod_rules_edit:
        input_box.valid = 1
    return (sum(valid) == len(valid))


def print_error_message(obj, msg):
    obj.setStyleSheet("color: red;")
    print("[ Error ] ", msg)
    obj.valid = False


def check_nd(obj):
    """determine if the percentages are valid"""
    valid = 1
    productions = dict()
    for rule in obj.prod_rules_edit:
        temprule = rule.text().split(":")
        productions[temprule[0]] = 0
    for i,rule in enumerate(obj.prod_rules_edit):
        if rule.valid:
            temprule = rule.text().split(":")
            try:
                productions[temprule[0]] = productions[temprule[0]] + (float(obj.prod_percent[i].text()))
            except:
                print("[ ERROR ] ",obj.prod_percent[i].text()," is not a number.")
                valid =0
                return valid
    for prod,perc in productions.items():
        if perc != 1.0:
            print("[ ERROR ] Invalid percent of ",perc," entered for ",prod)
            valid = 0
    return valid
