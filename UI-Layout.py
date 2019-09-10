import tkinter as tk

''' Author(s): Lela Bones and Stephanie Warman
    file: UI-Layout.py '''

fields = ('Axiom', 'Production Rules', 'Angle (degrees)', 'Iterations')

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
    entry.insert(0, "0")
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
  b1 = tk.Button(root, text='Generate L-System')
  b1.pack(side=tk.LEFT)
  b2 = tk.Button(root, text='Quit', command = root.quit)
  b2.pack(side=tk.RIGHT)
  root.mainloop()
