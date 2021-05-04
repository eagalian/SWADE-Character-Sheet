import tkinter as tk
import pickle
import csv
def savenew(win,n,att,skills):
    #print("Character Name: "+n)
    i=0
    data=[0,0,0,0,0]
    for item in att:
        data[i]=int(item)
        i+=1
    i=0
    for item in skills:
        data2[i]=int(item)
        item+=1
    p1=Player(n,data,data2)
    with open(p1.name+'.dat','wb') as f:
        pickle.dump(p1,f,protocol=2)
    with open('Saved Chars.csv','a') as saves:
        saves.write(p1.name)
        saves.write('\n')

    win.destroy()

def load(win,n):
    win.destroy()
    with open(str(n)+'.dat','rb') as f:
        pl=pickle.load(f)
    sheet=tk.Toplevel(main)
    tk.Label(sheet,text=pl.name).pack()
    tk.Label(sheet,text='Agility d'+str(pl.agi)).pack()
    tk.Label(sheet,text='Smarts d'+str(pl.smarts)).pack()
    tk.Label(sheet,text='Spirit d'+str(pl.spirit)).pack()
    tk.Label(sheet,text='Strength d'+str(pl.str)).pack()
    tk.Label(sheet,text='Vigor d'+str(pl.vigor)).pack()
    
              
def loadsaves():
    with open('Saved Chars.csv',mode='r') as saves:
        reader=csv.DictReader(saves)
        lines=0
        names=[]
        for row in reader:
            names.append(row['names'])
            lines+=1
        #print(names)
        loading=tk.Toplevel(main)
        tk.Label(loading,text="Who do you want to load?").pack()
        i=0
        while i<len(names):
            
            tk.Button(loading,text=names[i],command=lambda j=i:load(loading,names[j])).pack()
            i+=1
   


def newcharacter():
    creation=tk.Toplevel(main)
    label=tk.Label(creation, text="Character Creation")

    label.grid(row=0,column=0,columnspan=6)
    tk.Label(creation,text="Character Name?").grid(row=1,column=0)
    name=tk.Entry(creation)
    name.grid(row=1,column=1)
    tk.Label(creation,text="Agility").grid(row=2,column=0,)
    agility=tk.Entry(creation)
    agility.grid(row=2,column=1)
    tk.Label(creation,text="Smarts").grid(row=2,column=2)
    smarts=tk.Entry(creation)
    smarts.grid(row=2,column=3)
    tk.Label(creation,text="Spirit").grid(row=2,column=4)
    spirit=tk.Entry(creation)
    spirit.grid(row=2,column=5)
    tk.Label(creation,text="Strength").grid(row=10,column=0,columnspan=2)
    strength=tk.Entry(creation)
    strength.grid(row=10,column=2)
    tk.Label(creation,text="Vigor").grid(row=10,column=3,columnspan=2)
    vigor=tk.Entry(creation)
    vigor.grid(row=10,column=5)

    player=tk.Button(creation,text="Save!",command=lambda:savenew(creation,name.get(),[agility.get(),smarts.get(),spirit.get(),strength.get(),vigor.get()]))
    player.grid(row=12,column=5)



class Player:
    def __init__(self,name,attributes,skills):
        self.name=name
        self.agi=attributes[0]
        self.smarts=attributes[1]
        self.spirit=attributes[2]
        self.str=attributes[3]
        self.vigor=attributes[4]
        
        self.athletics=skills[0]
        self.boating=skills[1]
        self.driving=skills[2]
        self.fighting=skills[3]
        self.piloting=skills[4]
        self.riding=skills[5]
        self.shooting=skills[6]
        self.stealth=skills[7]
        self.theivery=skills[8]
        
        self.academics=skills[9]
        self.battle=skills[10]
        self.commonknowledge=skills[11]
        self.electronics=skills[12]
        self.gambling=skills[13]
        self.hacking=skills[14]
        self.healing=skills[15]
        self.nativelanguage=skills[16]
        self.notice=skills[17]
        self.occult=skills[18]
        self.psionics=skills[19]
        self.repair=skills[20]
        self.research=skills[21]
        self.science=skills[22]
        self.spellcasting=skills[23]
        self.survival=skills[24]
        self.taunt=skills[25]
        self.weirdscience=skills[26]

        self.faith=skills[27]
        self.focus=skills[28]
        self.intimidation=skills[29]
        self.performance=skills[30]
        self.persuasion=skills[31]








main=tk.Tk()
main.title("SWADE CHaracter Sheet v1")
menubar=tk.Menu()

filemenu=tk.Menu(menubar)
filemenu.add_command(label="New",command=lambda:newcharacter())
filemenu.add_command(label="Save",command=lambda:print("I save your current character."))
filemenu.add_command(label="Load",command=lambda:loadsaves())
filemenu.add_command(label="Save as ...",command=lambda:print("I save your character as a new character."))
menubar.add_cascade(label='File',menu=filemenu)

editmenu=tk.Menu(menubar)
editmenu.add_command(label="Attributes", command=lambda:print("I let you change your base stats"))
editmenu.add_command(label="Skills", command=lambda:print("I let you change your base skills"))
editmenu.add_command(label="Modifiers",command=lambda:print("I let you change your base modifiers"))
editmenu.add_command(label="Full Rest",command=lambda:print("I let you reset all temporary modifiers (wounds, fatigue, effects, etc."))
menubar.add_cascade(label="Character",menu=editmenu)

codex=tk.Menu(menubar)
codex.add_command(label="Combat effects",command=lambda:print("I explain combat effects"))
codex.add_command(label="Help",command=lambda:print("I explain how to use the app"))
menubar.add_cascade(label="Codex",menu=codex)

main.config(menu=menubar)
main.mainloop()
