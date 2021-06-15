import tkinter as tk 
from tkinter import ttk
from tkcalendar import Calendar
from tkinter.scrolledtext import ScrolledText
from time import strftime

todos = {}

def DetailTodo(cb=None):
    win = tk.Toplevel()
    win.wm_title('Detail Todo')
    tanggal = str(cal.selection_get())
    selecteditem = treev.focus()
    selectedIndex = treev.item(selecteditem)['text']
    selectedTodo = todos[tanggal][selectedIndex]
    judul = tk.StringVar(value= selectedTodo['judul'])
    tk.Label(win, text = 'Date:').grid(row = 0, column = 0, sticky = 'NW')#Mengubah posisi text
    tk.Label(win, text = '{} | {}'.format(tanggal, selectedTodo['waktu'])).grid(row = 0, column = 1, sticky = 'E')
    tk.Label(win, text = 'Title:').grid(row = 1, column = 0, sticky = 'NW')#Mengubah posisi text
    tk.Entry(win, state = 'disabled', textvariable = judul).grid(row = 1, column = 1, sticky = 'E')
    tk.Label(win, text = 'Information:').grid(row = 2, column = 0, sticky ='NW') #Mengubah posisi text 
    keterangan = ScrolledText(win, width = 12, height = 5)
    keterangan.grid(row = 2, column = 1, sticky = 'E')
    keterangan.insert(tk.INSERT, selectedTodo['keterangan'])
    keterangan.configure(state = 'disabled')
    
def LoadTodo():
    global todos
    f = open('mytodo.dat', 'r')
    data = f.read()
    f.close()
    todos = eval(data)
    ListTodo()
    
def SaveTodo():
    f = open('mytodo.dat', 'w')
    f.write(str(todos))
    f.close

def delTodo():
    tanggal = str(cal.selection_get())
    selecteditem = treev.focus()
    todos[tanggal].pop(treev.item(selecteditem)['text'])
    ListTodo()

def ListTodo(cb=None):
    for i in treev.get_children():
        treev.delete(i)
    tanggal = str(cal.selection_get())
    if tanggal in todos:
        for i in range(len(todos[tanggal])):
            treev.insert('','end', text=i, values=(todos[tanggal][i]['waktu'], todos[tanggal][i]['judul']))

def addTodo(win, key, jam, menit, judul, keterangan):
    newTodo = {
        'waktu':'{}:{}'.format(jam.get(), menit.get()),
        'judul': judul.get(),
        'keterangan': keterangan.get('1.0', tk.END)
    }
    if key in todos:
        todos[key].append(newTodo)
    else:
        todos[key] = [newTodo]
    win.destroy()
    ListTodo()

def AddForm():
    win = tk.Toplevel()
    win.wm_title('+')
    jam = tk.IntVar(value=10)
    menit = tk.IntVar(value=30)
    judul = tk.StringVar(value='')
    tk.Label(win, text='Date: ').grid(row=0, column=0, sticky = 'NW') #menambah sticky 
    tk.Spinbox(win, from_=0, to=23, textvariable=jam, width=3).grid(row=0, column=1)
    tk.Spinbox(win, from_=0, to=59, textvariable=menit, width=3).grid(row=0, column=2)
    tk.Label(win, text='Title:').grid(row=1, column=0, sticky = 'NW')#menambah sticky 
    tk.Entry(win, textvariable=judul).grid(row=1, column=1, columnspan=2)
    tk.Label(win, text='Information:').grid(row=2, column=0, sticky = 'NW')#menambah sticky 
    keterangan = ScrolledText(win, width=12, height=5)
    keterangan.grid(row=2, column=1, columnspan=2, rowspan=4)
    tanggal = str(cal.selection_get())
    tk.Button(win, text='Add', command=lambda: addTodo(win, tanggal, jam, menit, judul, keterangan)).grid(row=6, column=2) #mengubah posisi tombol add
    
def title():
    waktu = strftime('%H:%M')
    tanggal = str(cal.selection_get())
    root.title(tanggal + ' | ' + waktu +  " | Tiara's Calendar") #mengubah nama judul
    root.after(1000, title)
    
root = tk.Tk()
s = ttk.Style()
s.configure('Treeview', rowheight=20) #mengubah ukuran 
root.title('My Calendar')

cal = Calendar(root, font=('Sunshine Demo', 12), selectmode='day', locale='en_US', cursor='hand2', background="#9FA673", selectbackground = "#9FA673") #Mengubah font, bahasa, warna
cal.configure(headersbackground='#BB8F62', weekendbackground='#425967', weekendforeground='black', othermonthbackground='#E9D8BE') #penambahan konfigurasi
cal.grid(row=0, column=0, sticky='NS', rowspan=6)
cal.bind('<<CalendarSelected>>', ListTodo)
tanggal = str(cal.selection_get())
treev = ttk.Treeview(root)
treev.grid(row=0, column=1, sticky='WNES', rowspan=5, columnspan=2)
scrollBar = tk.Scrollbar(root, orient='vertical', command=treev.yview)
scrollBar.grid(row=0, column=3, sticky='ENS', rowspan=5)
treev.configure(yscrollcommand=scrollBar.set)
treev.bind('<Double-1>', DetailTodo)
treev['columns'] = ('1','2')
treev['show'] = 'headings'
treev.column('1', width=65)
treev.heading('1', text='Time')
treev.heading('2', text='Title')

btnAdd = tk.Button(root, text='Add', width=18, bg= '#425967', command=AddForm) #mengubah warna background
btnAdd.grid(row=5, column=1, sticky='N')

btnDel = tk.Button(root, text='Delete', width=18, bg= '#9FA673', command=delTodo)#mengubah warna background
btnDel.grid(row=5, column=2, sticky='N')

btnLoad = tk.Button(root, text='Load', width=18, bg= '#BB8F62', command=LoadTodo)#mengubah warna background
btnLoad.grid(row=6, column=1, sticky='S')

btnSave = tk.Button(root, text='Save', width=18, bg= '#3E3A2F', command=SaveTodo)#mengubah warna background
btnSave.grid(row=6, column=2, sticky='S')

btnNama = tk.Button(root, text = "Tiara Firdausa Abdillah", width = 38, fg='#BB8F62', font=('Arial Black', 8)) #penambahan nama
btnNama.grid(row = 6 , column = 0, sticky = "W")

title()
root.mainloop()