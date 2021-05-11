import tkinter as tk
import os
import json
import csv
import time
import random
random.seed()

def savenew(win):

    save(player)
    

    win.destroy()
def save(pl):
    
    data=[]
    with open('saves.json','a'): pass
    with open('saves.json','r+') as f:
        f.seek(0)
        try:
            data=json.load(f)
            i=0
            added=False
            for x in data:
                
                if pl['Name'] in x:
                    data[i]={pl['Name']:pl}
                    
                    added=True
                i+=1
            if not added:
                data.append({pl['Name']:pl})
                
            
            f.seek(0)
            
            json.dump(data,f)
        except:
            
            data.append({pl['Name']:pl})
            
            f.seek(0)
            json.dump(data,f)

        

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
    
    
    with open('saves.json','rb') as f:
        data=json.load(f)
    players=[]
    i=0
    for x in data:
        players.append(list(x.keys()))
        
        if players[i]==n:
            install(x[n[0]])
        i+=1
   
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
        subframe.grid(row=1,column=4)
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
    tk.Label(statspage,text=player['Name'],font='Helvetica 30 bold',padx=10, pady=10).grid(row=0,column=0,columnspan=4)
    i=0
    global buttons
    buttons=[None]*37
    m=[None]*37
    l1=[None]*37
    stringa=str()
    wounds=tk.IntVar()
    wounds.set(player['Wounds'])
    fatigue=tk.IntVar()
    fatigue.set(player['Fatigue'])
    wstring=tk.StringVar()
    wstring.set('Wounds: '+str(player['Wounds']))
    fstring=tk.StringVar()
    fstring.set('Fatigue: '+str(player['Fatigue']))
    global texta
    texta=[None]*37
    for x in attributelist:
        texta[i]=tk.StringVar()
        texta[i].set(attributelist[i]+': '+player[attributelist[i]]['display'])
        if i < 3:
            r=2
            c=4*i
        else:
            r=25
            c=4*(i-3)
        tk.Label(statspage,textvariable=texta[i], font='Helvetica',padx=10,pady=3).grid(row=r,column=c)
        m[i]=tk.Entry(statspage,width=10)
        m[i].grid(row=r,column=c+1)
        m[i].insert(0,'0')
        l1[i]=tk.Label(statspage,text='',width=20,padx=10,pady=3)
        l1[i].grid(row=r,column=c+3)
        buttons[i]=tk.Button(statspage,text='ROLL',command=lambda j=i:rollskills(statspage,l1[j],player[attributelist[j]]['size'],player[attributelist[j]]['size']-wounds.get()-fatigue.get()+int(isBlank(m[j].get()))))
        buttons[i].grid(row=r,column=c+2)
        i+=1
    agiskills=tk.Frame(statspage,bd=3)
    smartskills=tk.Frame(statspage,bd=3)
    spiritskills=tk.Frame(statspage,bd=3)
    agiskills.grid(row=3,column=0,rowspan=9,columnspan=4)
    smartskills.grid(row=3,column=4,rowspan=18,columnspan=4)
    spiritskills.grid(row=3,column=8,rowspan=5,columnspan=4)
    for x in skilllist:
        k=i-5
        texta[i]=tk.StringVar()
        texta[i].set(skilllist[k]+': '+player[skilllist[k]]['display'])
        
        if k<9:
            r=k
            c=0
            tk.Label(agiskills,textvariable=texta[i], font='Helvetica',padx=10,pady=3).grid(row=r,column=c)
            m[i]=tk.Entry(agiskills,width=10)
            m[i].grid(row=r,column=c+1)
            m[i].insert(0,'0')
            l1[i]=tk.Label(agiskills,text='',width=20,padx=10,pady=3)
            l1[i].grid(row=r,column=c+3)
            buttons[i]=tk.Button(agiskills,text='ROLL',command=lambda j=i:rollskills(statspage,l1[j],player[skilllist[j]]['size'],player[skilllist[j]]['modifier']-wounds.get()-fatigue.get()+int(isBlank(m[j].get()))))
            buttons[i].grid(row=r,column=c+2)
        elif k<27:
            r=k-9
            c=0
            tk.Label(smartskills,textvariable=texta[i], font='Helvetica',padx=10,pady=3).grid(row=r,column=c)
            m[i]=tk.Entry(smartskills,width=10)
            m[i].grid(row=r,column=c+1)
            m[i].insert(0,'0')
            l1[i]=tk.Label(smartskills,text='',width=20,padx=10,pady=3)
            l1[i].grid(row=r,column=c+3)
            buttons[i]=tk.Button(smartskills,text='ROLL',command=lambda j=i:rollskills(statspage,l1[j],player[skilllist[j]]['size'],player[skilllist[j]]['modifier']-wounds.get()-fatigue.get()+int(isBlank(m[j].get()))))
            buttons[i].grid(row=r,column=c+2)
        else:
            r=k-27
            c=0
            tk.Label(spiritskills,textvariable=texta[i], font='Helvetica',padx=10,pady=3).grid(row=r,column=c)
            m[i]=tk.Entry(spiritskills,width=10)
            m[i].grid(row=r,column=c+1)
            m[i].insert(0,'0')
            l1[i]=tk.Label(spiritskills,text='',width=20,padx=10,pady=3)
            l1[i].grid(row=r,column=c+3)
            buttons[i]=tk.Button(spiritskills,text='ROLL',command=lambda j=i:rollskills(statspage,l1[j],player[skilllist[j]]['size'],player[skilllist[j]]['modifier']-wounds.get()-fatigue.get()+int(isBlank(m[j].get()))))
            buttons[i].grid(row=r,column=c+2)

        i+=1
        
    
    
    incap('w',player['Wounds'],buttons)
    incap('f',player['Fatigue'],buttons)
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
        player['Wounds']=wounds
    if mode=='f':
        player['Fatigue']=wounds
    
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
    with open('saves.json',mode='r') as saves:
        saves.seek(0)
        savedata=json.load(saves)
    players=[]
    for x in savedata:
        players.append(list(x.keys()))
    loading=tk.Toplevel(main)
    tk.Label(loading,text="Who do you want to load?").pack()
    i=0
    while i<len(players):
            
        tk.Button(loading,text=players[i],command=lambda j=i:load(loading,players[j])).pack()
        i+=1

def dexp(d,exp):
    roll=random.randint(1,d)
    
    if roll==d:
        exp+=1
        temp=dexp(d,exp)
        roll+=temp[0]
        exp=temp[1]
        
    
    return roll,exp
def rollskills(window,output,d,m):
    
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
    player={}
    label=tk.Label(creation, text="Character Creation")
    baseskills=[None]*32
    skillmods=[None]*32
    attributes=[None]*5
    attributemods=[None]*5
    options=['Unskilled','d4','d6','d8','d10','d12']
    options_dict={'Unskilled':{'display':'Unskilled',
                               'size':4,
                               'modifier':-2},
                  'd4':{'display':'d4',
                               'size':4,
                               'modifier':0},
                  'd6':{'display':'d6',
                               'size':6,
                               'modifier':0},
                  'd8':{'display':'d8',
                               'size':8,
                               'modifier':0},
                  'd10':{'display':'d10',
                               'size':10,
                               'modifier':0},
                  'd12':{'display':'d12',
                               'size':12,
                               'modifier':0}}
    label.grid(row=0,column=0,columnspan=6)
    tk.Label(creation,text="Character Name?").grid(row=1,column=0)
    name=tk.Entry(creation,width=10)
    name.grid(row=1,column=1)
    install({'Name':'New'})
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
        newstat={attributelist[i]:options_dict['d4']}
        install(newstat)
        tk.Label(creation,textvariable=a[i]).grid(row=r,column=c+1)
        tk.Button(creation,text='-',command=lambda j=i:[attributes[j].set(max(4,attributes[j].get()-2)),
                                                        install({attributelist[j]:options_dict[options[int(attributes[j].get()/2)-1]]}),
                                                        a[j].set(str(options[int(attributes[j].get()/2)-1]))]).grid(row=r,column=c+2)
        tk.Button(creation,text='+',command=lambda j=i:[attributes[j].set(min(12,attributes[j].get()+2)),
                                                        install({attributelist[j]:options_dict[options[int(attributes[j].get()/2)-1]]}),
                                                        a[j].set(str(options[int(attributes[j].get()/2)-1]))]).grid(row=r,column=c+3)     
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
        newstat={skilllist[i]:options_dict['Unskilled']}
        install(newstat)
        tk.Label(creation,textvariable=s[i]).grid(row=r,column=c+1)
        tk.Button(creation,text='-',command=lambda j=i:[baseskills[j].set(max(2,baseskills[j].get()-2)),
                                                        install({skilllist[j]:options_dict[options[int(baseskills[j].get()/2)-1]]}),
                                                        s[j].set(str(options[int(baseskills[j].get()/2)-1]))]).grid(row=r,column=c+2)
        tk.Button(creation,text='+',command=lambda j=i:[baseskills[j].set(min(12,baseskills[j].get()+2)),
                                                        install({skilllist[j]:options_dict[options[int(baseskills[j].get()/2)-1]]}),
                                                        s[j].set(str(options[int(baseskills[j].get()/2)-1]))]).grid(row=r,column=c+3)     
        i+=1
    install({'Wounds':0})
    install({'Fatigue':0})
    
    player=tk.Button(creation,text="Next",command=lambda:[install({'Name':name.get()}),newcharother(creation)])
    player.grid(row=23,column=9)

def newcharother(window):
    
    killchildren(window)
    tk.Label(window,text="This is where you load info about gear, spells, etc.").pack()
    tk.Button(window,text="Save my shit",command=lambda:savenew(window)).pack()
    


global player, attributelist, skilllist
player={}
attributelist=['Agility','Smarts','Spirit','Strength','Vigor']
skilllist=['Athletics','Boating','Driving','Fighting','Piloting','Riding','Shooting','Stealth','Thievery','Academics','Battle','Common Knowledge','Electronics','Gambling','Hacking','Healing','Native Language','Notice','Occult','Psionics','Repair','Research','Science','Spellcasting','Survival','Taunt','Weird Science','Faith','Focus','Intimidation','Performance','Persuasion']


def install(newinfo):
    directory=list(newinfo.keys())
    for x in directory:
        player[str(x)]=newinfo[str(x)]

def change_attribute(trait,mode,value):
    options=['Unskilled','d4','d6','d8','d10','d12']
    
    if mode=='modifier':
        player[trait][mode]+=value
    if mode=='size':
        if value==-2 and player[trait]['display']!=options[0]:
            i=1
            while i<len(options):
                if options[i]==player[trait]['display']:
                    player[trait]['display']=options[i-1]
                    player[trait]['size']+=value
                    if player[trait]['display']==options[0]:
                        player[trait]['modifier']-=2
                    i=7
                else:
                    i+=1
        elif value==2 and player[trait]['display']!=options[5]:
            i=0
            while i < len(options)-1:
                if options[i]==player[trait]['display']:
                    player[trait]['display']=options[i+1]
                    if i==0:
                        player[trait]['modifier']+=2
                    
                    else:
                        player[trait]['size']+=value
                    i=7
                else:
                    i+=1
    if player[trait]['modifier']<0 and player[trait]['display']!=options[0]:
        player[trait]['display']='d'+str(player[trait]['size'])+'-'+str(abs(player[trait]['modifier']))
    elif player[trait]['modifier']>0 and player[trait]['display']!=options[0]:
        player[trait]['display']='d'+str(player[trait]['size'])+'+'+str(player[trait]['modifier'])
    elif player[trait]['modifier']==0 and player[trait]['display']!=options[0]:
        player[trait]['display']='d'+str(player[trait]['size'])
    
                        
    
def attribute_update():
    update=tk.Toplevel(main)
    tk.Label(update, text="Stats Update", font='Helvetica 20 bold').grid(row=0,column=1)
    i=0
    allstats=[None]*37
    for x in allstats:
        if i<5:
            allstats[i]=attributelist[i]
        else:
            allstats[i]=skilllist[i-5]
        i+=1

    i=0
    
    die=[None]*37
    for x in allstats:
        if i<3:
            r=1
            c=5*i
        elif i<5:
            r=21
            c=5*(i-3)
        elif i<14:
            r=i-3
            c=0
        elif i<32:
            r=i-12
            c=5
        else:
            r=i-30
            c=10
        die[i]=tk.StringVar()
        die[i].set(allstats[i]+': '+player[allstats[i]]['display'])
        
        tk.Label(update,textvariable=die[i]).grid(row=r,column=c)
        tk.Button(update,text='Step Down',command=lambda j=i:[change_attribute(allstats[j],'size',-2),die[j].set(allstats[j]+': '+player[allstats[j]]['display'])]).grid(row=r,column=c+1)
        tk.Button(update,text='Step Up',command=lambda j=i:[change_attribute(allstats[j],'size',2),die[j].set(allstats[j]+': '+player[allstats[j]]['display'])]).grid(row=r,column=c+2)
        tk.Button(update,text='-1',command=lambda j=i:[change_attribute(allstats[j],'modifier',-1),die[j].set(allstats[j]+': '+player[allstats[j]]['display'])]).grid(row=r,column=c+3)
        tk.Button(update,text='+1',command=lambda j=i:[change_attribute(allstats[j],'modifier',1),die[j].set(allstats[j]+': '+player[allstats[j]]['display'])]).grid(row=r,column=c+4)
        i+=1
    
    
    tk.Button(update,text="Apply",command=lambda:[update.destroy(),mainstats()]).grid(row=0, column=3)


def fullrest():
    incap('w',0,buttons)
    incap('f',0,buttons)
    mainstats()

global main
main=tk.Tk()
main.title("SWADE CHaracter Sheet v4")

main.state('zoomed')
menubar=tk.Menu()


filemenu=tk.Menu(menubar)
filemenu.add_command(label="New",command=lambda:newcharstats())
filemenu.add_command(label="Save",command=lambda:save(player))
filemenu.add_command(label="Load",command=lambda:loadsaves())
filemenu.add_command(label="Save as ...",command=lambda:saveas(player))
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
