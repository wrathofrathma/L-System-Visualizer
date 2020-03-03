import tkinter as tk
import time

""" Author(s): Lela Bones and Stephanie Warman
    file: UI-Layout.py """

fields = ("Axiom", "Production Rules", "Angle (degrees)", "Iterations")
alphabet = ("F", "f", "+", "-")
err_mess = "invalid"
flash_delay = 500  # msec between colour change
flash_colours = ("black", "red")  # Two colours to swap between


def flashColor(object, color_index, init_time):
    if time.time() - init_time < 2:
        object.config(foreground=flash_colours[color_index])
        root.after(flash_delay, flashColor, object, 1 - color_index, init_time)
    else:
        object.config(foreground=flash_colours[0])


def clear_box(object, init_time):
    if time.time() - init_time < 2:
        root.after(flash_delay, clear_box, object, init_time)
    else:
        object.delete(0, tk.END)


def print_invalid(object):
    object.delete(0, tk.END)
    object.insert(0, err_mess)
    flashColor(object, 0, time.time())
    clear_box(object, time.time())


def get_Axiom(entries):
    """
  This function input checks the input for axiom
  Input: entries is an array collected from makeform
  Ouput: invalid if not valid input
  """
    axiom = entries["Axiom"].get()
    for ch in axiom:
        if not ch in alphabet:
            print_invalid(entries["Axiom"])

        # root.after(10, entries['Axiom'].config(background=dfault_col))


def get_ProdRules(entries):
    """
  This function input checks the input for production rules
  Input: entries is an array collected from makeform
  Ouput: invalid if not valid input
  """
    prodRule = entries["Production Rules"].get()
    prodRule = prodRule.replace(" ", "")
    if not "->" in prodRule or prodRule[1] == ">" or prodRule[len(prodRule) - 1] == ">":
        print_invalid(entries["Production Rules"])
    tmp_prodRule = prodRule.replace("->", "")
    for ch in tmp_prodRule:
        if not ch in alphabet:
            print_invalid(entries["Production Rules"])


def get_Angle(entries):
    """
  This function input checks the input for angle
  Input: entries is an array collected from makeform
  Ouput: invalid if not valid input
  """
    try:
        angle = float(entries["Angle (degrees)"].get())
    except:
        print_invalid(entries["Angle (degrees)"])
        return
    if angle <= -360 or angle >= 360:
        print_invalid(entries["Angle (degrees)"])


def get_Iter(entries):
    """
  This function input checks the input for iterations
  Input: entries is an array collected from makeform
  Ouput: invalid if not valid input
  """
    try:
        iterat = int(entries["Iterations"].get())
    except:
        print_invalid(entries["Iterations"])
        return
    if iterat <= 0:
        print_invalid(entries["Iterations"])


def check_inputs(entries):
    get_Axiom(entries)
    get_ProdRules(entries)
    get_Angle(entries)
    get_Iter(entries)


def makeform(root, fields):
    """ 
  This function makes the input for the application
  Input: root is the object of the tk window
         fields are the input fields
  Output: entries for the field
  """

    entries = {}
    root.title("L-System")
    for field in fields:
        row = tk.Frame(root)
        label = tk.Label(row, width=22, text=field + ": ", anchor="w")
        entry = tk.Entry(row)
        entry.insert(0, "")
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        label.pack(side=tk.LEFT)
        entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entries[field] = entry

    return entries


if __name__ == "__main__":
    root = tk.Tk()
    entries = makeform(root, fields)
    frame = tk.Frame(width=200, height=200)
    frame.pack()
    b1 = tk.Button(
        root, text="Generate L-System", command=(lambda e=entries: check_inputs(e))
    )
    b1.pack(side=tk.LEFT)
    b2 = tk.Button(root, text="Quit", command=root.quit)
    b2.pack(side=tk.RIGHT)
    root.mainloop()
