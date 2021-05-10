import tkinter as tk
import pickle
import csv
import time
import random
random.seed()

def savenew(win,incoming):

    
    i=0
    data=[0,0,0,0,0]
    data2=[None]*32
    data3=[None]*5
    data4=[None]*32
    for item in incoming[2]:
        data[i]=item.get()
        i+=1
    i=0
    for item in incoming[4]:
        if item.get()==2:
            data4[i]=-2
            data2[i]=4
        else:
            data2[i]=item.get()
        i+=1

    i=0
    for item in incoming[3]:
        data3[i]=int(item.get())
        i+=1
    i=0
    for item in incoming[5]:
        if data4[i]!=-2:
            data4[i]=int(item.get())
        i+=1
    p1=Player(incoming[1],data,data2,data3,data4)
    save(p1,p1.name)

    win.destroy()
def save(pl,name):
    #temp.destroy()
    pl.name=name
    with open(pl.name+'.dat','wb') as f:
        pickle.dump(pl,f,protocol=2)
    exists=False
    with open('Saved Chars.csv',mode='r') as saves:
        reader=csv.reader(saves)
        for x in reader:
            
            if name in x:
                
                exists=True
    if exists==False:
        with open('Saved Chars.csv','a') as saves:
            saves.write(name+'\n')
def allchildren(win):
    list=win.winfo_children()
    for item in list:
        if item.winfo_children():
            list.extend(item.winfo_children())
    return list
def killchildren(wind):
    
    widgets=allchildren(wind)
    for item in widgets:
        item.grid_forget()
def kill(a):
    a.destroy()
def saveas(pl):
    temp=tk.Toplevel(main)
    tk.Label(temp,text="Save name:").pack()
    e1=tk.Entry(temp)
    e1.pack()
    b1=tk.Button(temp,text="Save",command=lambda:[save(pl,e1.get()),kill(temp)]).pack()
   

def load(win,n):
    win.destroy()
    killchildren(main)
    global pl
    
    with open(str(n)+'.dat','rb') as f:
        pl=pickle.load(f)
    mainstats()

def combat():
    killchildren(main)
    combatpage=tk.Frame(main)
    combatpage.grid()
    tk.Label(combatpage,text='Combat Goes Here').grid(row=0,column=0)

def newgear():
    killchildren(main)
    equipmentbuilder=tk.Frame(main)
    equipmentbuilder.grid()
    tk.Label(equipmentbuilder,text='Equipment Creator',font='Helvetica 20 bold',anchor='w').grid(row=0,column=0,columnspan=3)
    tk.Label(equipmentbuilder,text='Equipment Type: ').grid(row=1,column=0)
    options=['Gear','Armor','Weapons','Vehicles']
    clicked=tk.StringVar()
    clicked.set('Gear')
    equipmentdrop=tk.OptionMenu(equipmentbuilder,clicked,*options)
    equipmentdrop.grid(row=1,column=1)
    tk.Button(equipmentbuilder,text='Go',command=lambda:equipinfo(subframe,clicked.get())).grid(row=1,column=2)
    subframe=tk.Frame(equipmentbuilder)
    subframe.grid(row=2,column=0,columnspan=20)
    
def equipinfo(frame,mode):
    for widget in frame.winfo_children():
        widget.destroy()
    if mode=='Gear':
        tk.Label(frame,text="Gear hasn't been made yet").grid(row=0,column=0)
    if mode=='Armor':
        tk.Label(frame,text="Armor hasn't been made yet").grid(row=0,column=0)
    if mode=='Weapons':
        tk.Label(frame,text="Melee, Ranged, or Special? \n(special includes things like cannons, \ngrenades, and siege equipment)").grid(row=0,column=0)
        weapontypes=['Melee','Ranged','Special']
        weaponchoice=tk.StringVar()
        weaponchoice.set('Melee')
        choice=tk.OptionMenu(frame,weaponchoice,*weapontypes)
        choice.grid(row=0,column=1)
        subframe=tk.Frame(frame)
        subframe.grid(row=1,column=3)
        tk.Button(frame,text="Go",command=lambda:weapons(subframe,weaponchoice.get())).grid(row=0,column=2)

def weapons(frame,weapon):
    for widget in frame.winfo_children():
        widget.destroy()
    if weapon=='Melee':
        melee=tk.Frame(frame)
        melee.grid()
        tk.Label(melee,text="Weapon Name: ").grid(row=0,column=0)
        name=tk.Entry(melee)
        name.grid(row=0,column=1,columnspan=10)
        tk.Label(melee,text="Damage: Str+").grid(row=1,column=0)
        dice=['d4','d6','d8','d10','d12']
        diechoice=tk.StringVar()
        diechoice.set('d4')
        drop=tk.OptionMenu(melee,diechoice,*dice)
        drop.grid(row=1,column=1)
        tk.Label(melee,text='+').grid(row=1,column=2)
        extra=tk.Entry(melee)
        extra.grid(row=1,column=3,columnspan=10)
        extra.insert(0,'0')
        tk.Label(melee,text="Min Str").grid(row=2,column=0)
        strchoice=tk.StringVar()
        strchoice.set('d4')
        drop2=tk.OptionMenu(melee,strchoice,*dice).grid(row=2,column=1)
        tk.Label(melee,text="Weight").grid(row=3,column=0)
        weight=tk.Entry(melee)
        weight.grid(row=3,column=1,columnspan=10)
        weight.insert(0,'0')
        tk.Label(melee,text='Cost').grid(row=4,column=0)
        cost=tk.Entry(melee)
        cost.grid(row=4,column=1,columnspan=10)
        cost.insert(0,'0')
        tk.Label(melee,text='Notes:').grid(row=5,column=0)
        notes=tk.Text(melee)
        notes.grid(row=6,column=1,columnspan=50)
def mainstats():
    killchildren(main)
    statspage=tk.Frame(main)
    statspage.grid()
    tk.Label(statspage,text=pl.name,font='Helvetica 30 bold',padx=10, pady=10).grid(row=0,column=0,columnspan=4)
    i=0
    global buttons
    buttons=[None]*37
    m=[None]*5
    l1=[None]*5
    stringa=str()
    wounds=tk.IntVar()
    wounds.set(pl.wounds)
    fatigue=tk.IntVar()
    fatigue.set(pl.fatigue)
    wstring=tk.StringVar()
    wstring.set('Wounds: '+str(wounds.get()))
    fstring=tk.StringVar()
    fstring.set('Fatigue: '+str(fatigue.get()))
    global texta
    texta=[None]*5
    for x1 in pl.attributes:
        string=x1[0]+': d'+str(x1[1])
        if x1[2]>0:
            string+='+'+str(x1[2])
        if x1[2]<0:
            string+='-'+str(abs(x1[2]))
        
        texta[i]=tk.StringVar()
        texta[i].set(string)
        if i < 3:
            tk.Label(statspage,textvariable=texta[i], font='Helvetica',padx=10,pady=3).grid(row=2,column=4*i)
            m[i]=tk.Entry(statspage,width=10)
            m[i].grid(row=2,column=4*i+1)
            m[i].insert(0,'0')
            l1[i]=tk.Label(statspage,text='',width=20,padx=10,pady=3)
            l1[i].grid(row=2,column=4*i+3)
            buttons[i]=tk.Button(statspage,text='ROLL',command=lambda j=i:rollskills(0,statspage,l1[j],pl.attributes[j][1],pl.attributes[j][2]-wounds.get()-fatigue.get()+int(isBlank(m[j].get()))))
            buttons[i].grid(row=2,column=4*i+2)
        else:
            tk.Label(statspage,textvariable=texta[i], font='Helvetica',padx=10,pady=3).grid(row=25,column=4*i-12)
            m[i]=tk.Entry(statspage,width=10)
            m[i].grid(row=25,column=4*i+1-12)
            m[i].insert(0,'0')
            l1[i]=tk.Label(statspage,text='',width=20,padx=10,pady=3)
            l1[i].grid(row=25,column=4*i+3-12)
            buttons[i]=tk.Button(statspage,text='ROLL',command=lambda j=i:rollskills(0,statspage,l1[j],pl.attributes[j][1],pl.attributes[j][2]-wounds.get()-fatigue.get()+int(isBlank(m[j].get()))))
            buttons[i].grid(row=25,column=4*i+2-12)
        i+=1
    
    i=0
    m2=[None]*32
    l2=[None]*32
    global texts
    texts=[None]*32
    for x in pl.skills:
        string=x[0]+': d'+str(x[1])
        if x[2]>0:
            string+='+'+str(x[2])
        if x[2]<0:
            string+='-'+str(abs(x[2]))
        texts[i]=tk.StringVar()
        texts[i].set(string)
        if i < 9:
            tk.Label(statspage,textvariable=texts[i], font='Helvetica',padx=10,pady=3).grid(row=3+i,column=0)
            m2[i]=tk.Entry(statspage,width=10)
            m2[i].grid(row=3+i,column=1)
            m2[i].insert(0,'0')
            l2[i]=tk.Label(statspage,text='',width=20,padx=10,pady=3)
            l2[i].grid(row=3+i,column=3)
            buttons[i+5]=tk.Button(statspage,text='ROLL',command=lambda j=i:rollskills(0,statspage,l2[j],pl.skills[j][1],pl.skills[j][2]-wounds.get()-fatigue.get()+int(isBlank(m2[j].get()))))
            buttons[i+5].grid(row=3+i,column=2)
        elif i<27:
            tk.Label(statspage,textvariable=texts[i], font='Helvetica',padx=10,pady=3).grid(row=3+i-9,column=4)
            m2[i]=tk.Entry(statspage,width=10)
            m2[i].grid(row=3+i-9,column=5)
            m2[i].insert(0,'0')
            l2[i]=tk.Label(statspage,text='',width=20,padx=10,pady=3)
            l2[i].grid(row=3+i-9,column=7)
            buttons[i+5]=tk.Button(statspage,text='ROLL',command=lambda j=i:rollskills(0,statspage,l2[j],pl.skills[j][1],pl.skills[j][2]-wounds.get()-fatigue.get()+int(isBlank(m2[j].get()))))
            buttons[i+5].grid(row=3+i-9,column=6)
        else:
            tk.Label(statspage,textvariable=texts[i], font='Helvetica',padx=10,pady=3).grid(row=3+i-27,column=8)
            m2[i]=tk.Entry(statspage,width=10)
            m2[i].grid(row=3+i-27,column=9)
            m2[i].insert(0,'0')
            l2[i]=tk.Label(statspage,text='',width=20,padx=10,pady=3)
            l2[i].grid(row=3+i-27,column=11)
            buttons[i+5]=tk.Button(statspage,text='ROLL',command=lambda j=i:rollskills(0,statspage,l2[j],pl.skills[j][1],pl.skills[j][2]-wounds.get()-fatigue.get()+int(isBlank(m2[j].get()))))
            buttons[i+5].grid(row=3+i-27,column=10)
        i+=1
    incap('w',pl.wounds,buttons)
    incap('f',pl.fatigue,buttons)
    tk.Button(statspage,textvariable=wstring,command=lambda:[wounds.set(min(3,wounds.get()+1)),wstring.set('Wounds: '+str(wounds.get())),incap('w',wounds.get(),buttons)]).grid(row=0,column=10)
    tk.Button(statspage,text='Heal',command=lambda:[wounds.set(max(0,wounds.get()-1)),wstring.set('Wounds: '+str(wounds.get())),incap('w',wounds.get(),buttons)]).grid(row=0,column=11)
    tk.Button(statspage,textvariable=fstring,command=lambda:[fatigue.set(min(2,fatigue.get()+1)),fstring.set('Fatigue: '+str(fatigue.get())),incap('f',fatigue.get(),buttons)]).grid(row=0,column=8)
    tk.Button(statspage,text='Rest',command=lambda:[fatigue.set(max(0,fatigue.get()-1)),fstring.set('Fatigue: '+str(fatigue.get())),incap('f',fatigue.get(),buttons)]).grid(row=0,column=9)
def isBlank(string):
    if string and string.strip():
        return string
    return 0
def incap(mode,wounds,buttons):
    if mode=='w':
        pl.wounds=wounds
    if mode=='f':
        pl.fatigue=wounds
    
    if wounds==3 and mode=='w':
        i=0
        for x in buttons:
            if i!=4:
                
                buttons[i].config(state='disabled')
            i+=1
    elif wounds==2 and mode=='f':
        i=0
        for x in buttons:
            if i!=4:
                
                buttons[i].config(state='disabled')
            i+=1
    else:
        i=0
        for x in buttons:
            buttons[i].config(state='normal')
            i+=1
def loadsaves():
    with open('Saved Chars.csv',mode='r') as saves:
        reader=csv.DictReader(saves)
        lines=0
        names=[]
        for row in reader:
            names.append(row['names'])
            lines+=1
        
        loading=tk.Toplevel(main)
        tk.Label(loading,text="Who do you want to load?").pack()
        i=0
        while i<len(names):
            
            tk.Button(loading,text=names[i],command=lambda j=i:load(loading,names[j])).pack()
            i+=1

def dexp(d,exp):
    roll=random.randint(1,d)
    
    if roll==d:
        exp+=1
        temp=dexp(d,exp)
        roll+=temp[0]
        exp=temp[1]
        
    
    return roll,exp
def rollskills(top,window,output,d,m):
    
    rollmain=dexp(d,0)
    wild=dexp(6,0)
    output.configure(text="Rolling...")
    output.update()
    time.sleep(1)
    if rollmain[0]==1 and wild[0]==1:
        roll='CRIT FAIL!!!'
    elif rollmain[0]>=wild[0]:
        
        roll=str(rollmain[0]+m)+' (skill)'
        if rollmain[1]>0:
            roll+=str(rollmain[1])+' Explosion(s)!'

    else:
        roll=str(wild[0]+m)+' (wild)'
        if wild[1]>0:
            roll+=str(wild[1])+' Explosion(s)!'
        
    output.configure(text=roll)
    output.update()
        
    
    


        


def newcharstats():
    creation=tk.Toplevel(main)
    label=tk.Label(creation, text="Character Creation")
    attributelist=['Agility','Smarts','Spirit','Strength','Vigor']
    skilllist=['Athletics','Boating','Driving','Fighting','Piloting','Riding','Shooting','Stealth','Thievery','Academics','Battle','Common Knowledge','Electronics','Gambling','Hacking','Healing','Native Language','Notice','Occult','Psionics','Repair','Research','Science','Spellcasting','Survival','Taunt','Weird Science','Faith','Focus','Intimidation','Performance','Persuasion']
    baseskills=[None]*32
    skillmods=[None]*32
    attributes=[None]*5
    attributemods=[None]*5
    options=['Unskilled','d4','d6','d8','d10','d12']
    label.grid(row=0,column=0,columnspan=6)
    tk.Label(creation,text="Character Name?").grid(row=1,column=0)
    name=tk.Entry(creation,width=10)
    name.grid(row=1,column=1)
    tk.Label(creation,text="Die Size").grid(row=2,column=1)
    tk.Label(creation,text="Modifier").grid(row=2,column=2)
    tk.Label(creation,text="Die Size").grid(row=2,column=4)
    tk.Label(creation,text="Modifier").grid(row=2,column=5)
    tk.Label(creation,text="Die Size").grid(row=2,column=7)
    tk.Label(creation,text="Modifier").grid(row=2,column=8)
    a=[None]*5
    s=[None]*32
    
    i=0
    c=None
    r=None
    for x in attributelist:
        attributes[i]=tk.IntVar()
        attributes[i].set(4)
        attributemods[i]=tk.IntVar()
        attributemods[i].set(0)
        a[i]=tk.StringVar()
        a[i].set(options[1])
        if i<3:
            c=4*i
            r=3
        else:
            c=4*(i-3)
            r=23
        tk.Label(creation,text=attributelist[i]).grid(row=r,column=c)
            
        tk.Label(creation,textvariable=a[i]).grid(row=r,column=c+1)
        tk.Button(creation,text='-',command=lambda j=i:[attributes[j].set(max(4,attributes[j].get()-2)),
                                                        a[j].set(options[int(attributes[j].get()/2-1)])]).grid(row=r,column=c+2)
        tk.Button(creation,text='+',command=lambda j=i:[attributes[j].set(min(12,attributes[j].get()+2)),
                                                        a[j].set(options[int(attributes[j].get()/2-1)])]).grid(row=r,column=c+3)     
        i+=1
    

    i=0
    c=None
    r=None
    for x in skilllist:
        baseskills[i]=tk.IntVar()
        baseskills[i].set(2)
        
        skillmods[i]=tk.IntVar()
        skillmods[i].set(0)
        s[i]=tk.StringVar()
        s[i].set(options[0])
        if i<9:
            c=0
            r=i+4
        elif i<27:
            c=4
            r=i+4-9
        else:
            c=8
            r=i+4-27
        tk.Label(creation,text=skilllist[i]).grid(row=r,column=c)
            
        tk.Label(creation,textvariable=s[i]).grid(row=r,column=c+1)
        tk.Button(creation,text='-',command=lambda j=i:[baseskills[j].set(max(2,baseskills[j].get()-2)),
                                                        s[j].set(options[int(baseskills[j].get()/2-1)])]).grid(row=r,column=c+2)
        tk.Button(creation,text='+',command=lambda j=i:[baseskills[j].set(min(12,baseskills[j].get()+2)),
                                                        s[j].set(options[int(baseskills[j].get()/2-1)])]).grid(row=r,column=c+3)     
        i+=1    
    player=tk.Button(creation,text="Save!",command=lambda:newcharother([creation,name.get(),attributes,attributemods,baseskills,skillmods],creation))
    player.grid(row=23,column=9)

def newcharother(data,window):
    
    killchildren(window)
    tk.Label(window,text="This is where you load info about gear, spells, etc.").pack()
    tk.Button(window,text="Save my shit",command=lambda:savenew(window,data)).pack()



class Player:
    def __init__(self,name,attributes,skills,attmods,skmods):
        self.name=name
        self.attributes=[['Agility',attributes[0],attmods[0]],['Smarts',attributes[1],attmods[1]],['Spirit',attributes[2],attmods[2]],['Strength',attributes[3],attmods[3]],['Vigor',attributes[4],attmods[4]]]
        skilllist=['Athletics','Boating','Driving','Fighting','Piloting','Riding','Shooting','Stealth','Thievery','Academics','Battle','Common Knowledge','Electronics','Gambling','Hacking','Healing','Native Language','Notice','Occult','Psionics','Repair','Research','Science','Spellcasting','Survival','Taunt','Weird Science','Faith','Focus','Intimidation','Performance','Persuasion']        
        self.skills=[[None,None,None]]*32
        i=0
        for item in self.skills:
            self.skills[i]=[skilllist[i],skills[i],skmods[i]]
            i+=1
        self.wounds=0
        self.fatigue=0

def change_attribute(row,column,value):
    if value==-2 and pl.attributes[row][column]!=4:
        pl.attributes[row][column]-=2
    if value==2 and pl.attributes[row][column]!=12:
        pl.attributes[row][column]+=2
    string='d'+str(pl.attributes[row][1])
    
    if pl.attributes[row][2]>0:
        string+='+'+str(pl.attributes[row][2])
    if pl.attributes[row][2]<0:
        string+='-'+str(abs(pl.attributes[row][2]))
    fullstring=pl.attributes[row][0]+': '+string
    texta[row].set(fullstring)
    
    return string
def attribute_update():
    update=tk.Toplevel(main)
    tk.Label(update, text="Attributes", font='Helvetica 20 bold').grid(row=0,column=0)
    i=0
    string=str()
    die=[None]*5
    for x in pl.attributes:
        string='d'+str(x[1])
        if x[2]>0:
            string+='+'+str(x[2])
        if x[2]<0:
            string+='-'+str(abs(x[2]))
        die[i]=tk.StringVar()
        die[i].set(string)
        tk.Label(update,text=x[0]).grid(row=i+1,column=0)
        tk.Label(update,textvariable=die[i]).grid(row=i+1,column=1)
        tk.Button(update,text='Step Down',command=lambda j=i:die[j].set(change_attribute(j,1,-2))).grid(row=i+1,column=2)
        tk.Button(update,text='Step Up',command=lambda j=i:die[j].set(change_attribute(j,1,2))).grid(row=i+1,column=3)
        i+=1
    
def change_skills(row,column,value):
 
    if column==1:
        if value==-2 and pl.skills[row][column]!=4:
            pl.skills[row][column]-=2
            
        if value==2 and pl.skills[row][column]!=12:
            
            pl.skills[row][column]+=2
    if column==2:
        pl.skills[row][column]+=value
    string='d'+str(pl.skills[row][1])
    
    if pl.skills[row][2]>0:
        string+='+'+str(pl.skills[row][2])
    if pl.skills[row][2]<0:
        string+='-'+str(abs(pl.skills[row][2]))
    fullstring=pl.skills[row][0]+': '+string
    texts[row].set(fullstring)

def skills_update():
    update=tk.Toplevel(main)
    tk.Label(update, text="Skills", font='Helvetica 20 bold').grid(row=0,column=0)
    i=0
    string=str()
    die=[None]*32
    for x in pl.skills:

        if i<9:
            r=i+1
            c=0
        elif i<27:
            r=i-8
            c=3
        else:
            r=i-26
            c=6
        tk.Label(update,textvariable=texts[i]).grid(row=r,column=c)

        tk.Button(update,text='Step Down',command=lambda j=i:change_skills(j,1,-2)).grid(row=r,column=c+1)
        tk.Button(update,text='Step Up',command=lambda j=i:change_skills(j,1,2)).grid(row=r,column=c+2)
        i+=1


def modifier_update():
    update=tk.Toplevel(main)
    tk.Label(update, text="Modifiers", font='Helvetica 20 bold').grid(row=0,column=0)
    i=0
    string=str()
    die=[None]*32
    for x in pl.skills:

        if i<9:
            r=i+2
            c=0
        elif i<27:
            r=i-7
            c=3
        else:
            r=i-25
            c=6
        tk.Label(update,textvariable=texts[i]).grid(row=r,column=c)

        tk.Button(update,text='Step Down',command=lambda j=i:change_skills(j,2,-1)).grid(row=r,column=c+1)
        tk.Button(update,text='Step Up',command=lambda j=i:change_skills(j,2,1)).grid(row=r,column=c+2)
        i+=1

def fullrest():
    incap('w',0,buttons)
    incap('f',0,buttons)
    mainstats()

global main
main=tk.Tk()
main.title("SWADE CHaracter Sheet v3")
#w,h=main.winfo_screenwidth(),main.winfo_screenheight()
#main.geometry('%dx%d+0+0'%(w,h))
main.state('zoomed')
menubar=tk.Menu()


filemenu=tk.Menu(menubar)
filemenu.add_command(label="New",command=lambda:newcharstats())
filemenu.add_command(label="Save",command=lambda:save(pl,pl.name))
filemenu.add_command(label="Load",command=lambda:loadsaves())
filemenu.add_command(label="Save as ...",command=lambda:saveas(pl))
menubar.add_cascade(label='File',menu=filemenu)

editmenu=tk.Menu(menubar)
editmenu.add_command(label="Attributes", command=lambda:attribute_update())
editmenu.add_command(label="Skills", command=lambda:skills_update())
editmenu.add_command(label="Modifiers",command=lambda:modifier_update())
editmenu.add_command(label="Full Rest",command=lambda:fullrest())
menubar.add_cascade(label="Edit Character",menu=editmenu)

csmenu=tk.Menu(menubar)
csmenu.add_command(label="Stats",command=lambda:mainstats())
csmenu.add_command(label="Combat",command=lambda:combat())
menubar.add_cascade(label="Character Sheet",menu=csmenu)

codex=tk.Menu(menubar)
codex.add_command(label="Combat effects",command=lambda:print("I explain combat effects"))
codex.add_command(label='Equipment',command=lambda:print('I let you access equipment data, and add it to your character sheet'))
codex.add_command(label='New Equipment',command=lambda:newgear())
codex.add_command(label="Help",command=lambda:print("I explain how to use the app"))
menubar.add_cascade(label="Codex",menu=codex)

main.config(menu=menubar)
main.mainloop()
