import tkinter as tk
''' Author(s): Lela Bones and Stephanie Warman
    file: UI-Layout.py '''

fields = ('Axiom', 'Production Rules', 'Angle (degrees)', 'Iterations')
alphabet = ('F','f','+','-')
err_mess = 'invalid'

def get_Axiom(entries):
  '''
  This function input checks the input for axiom
  Input: entries is an array collected from makeform
  Ouput: invalid if not valid input
  '''
  axiom = entries['Axiom'].get()
  for ch in axiom:
    if not ch in alphabet:
      entries['Axiom'].delete(0,tk.END)
      entries['Axiom'].insert(0,err_mess )
      error = tk.Button(root, text='X')
      error.pack(side=tk.RIGHT)
     
     # root.after(10, entries['Axiom'].config(background=dfault_col))
      
def get_ProdRules(entries):
  '''
  This function input checks the input for production rules
  Input: entries is an array collected from makeform
  Ouput: invalid if not valid input
  '''
  prodRule = ((entries['Production Rules'].get()))
  prodRule=prodRule.replace(' ','')
  if not '->' in prodRule or prodRule[1]=='>' or prodRule[len(prodRule)-1]=='>':
    entries['Production Rules'].delete(0,tk.END)
    entries['Production Rules'].insert(0,err_mess )
  tmp_prodRule = prodRule.replace('->','')
  for ch in tmp_prodRule:
    if not ch in alphabet:
      entries['Production Rules'].delete(0,tk.END)
      entries['Production Rules'].insert(0,err_mess )
def get_Angle(entries):
  '''
  This function input checks the input for angle
  Input: entries is an array collected from makeform
  Ouput: invalid if not valid input
  '''
  try:
    angle = (float(entries['Angle (degrees)'].get()))
  except: 
    entries['Iterations'].delete(0,tk.END)
    entries['Iterations'].insert(0,err_mess)
    return
  if angle <= -360 or angle >= 360:
    entries['Angle (degrees)'].delete(0,tk.END)
    entries['Angle (degrees)'].insert(0,err_mess)
def get_Iter(entries):
  '''
  This function input checks the input for iterations
  Input: entries is an array collected from makeform
  Ouput: invalid if not valid input
  '''
  try:
    iterat = (int(entries['Iterations'].get()))
  except: 
    entries['Iterations'].delete(0,tk.END)
    entries['Iterations'].insert(0,err_mess)
    return
  if iterat <= 0:
    entries['Iterations'].delete(0,tk.END)
    entries['Iterations'].insert(0,err_mess)

def check_inputs(entries):
  get_Axiom(entries)
  get_ProdRules(entries)
  get_Angle(entries)
  get_Iter(entries)
def makeform(root, fields):
  ''' 
  This function makes the input for the application
  Input: root is the object of the tk window
         fields are the input fields
  Output: entries for the field
  '''

  entries = {}
  root.title('L-System')
  for field in fields:
    row = tk.Frame(root)
    label = tk.Label(row, width=22, text=field+": ", anchor='w')
    entry = tk.Entry(row)
    entry.insert(0, "")
    row.pack(side=tk.TOP,
            fill=tk.X,
            padx=5,
            pady=5)
    label.pack(side=tk.LEFT)
    entry.pack(side=tk.RIGHT,
            expand=tk.YES,
            fill=tk.X)
    entries[field] = entry
  
  return entries

if __name__ == '__main__':
  root = tk.Tk()
  entries = makeform(root, fields)
  frame = tk.Frame(width=200, height=200)
  frame.pack()
  b1 = tk.Button(root, text='Generate L-System', 
                 command = (lambda e = entries: check_inputs(e)))
  b1.pack(side=tk.LEFT)
  b2 = tk.Button(root, text='Quit', command = root.quit)
  b2.pack(side=tk.RIGHT)
  root.mainloop()
