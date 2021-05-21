import tkinter as tk
from tkinter import ttk
import os
import json
import csv
import time
import uuid
import random


random.seed()


global attributelist, skilllist, dice
attributelist=['Agility','Smarts','Spirit','Strength','Vigor']
skilllist=['Athletics','Boating','Driving','Fighting','Piloting','Riding','Shooting','Stealth','Thievery','Academics','Battle','Common Knowledge','Electronics','Gambling','Hacking','Healing','Native Language','Notice','Occult','Psionics','Repair','Research','Science','Spellcasting','Survival','Taunt','Weird Science','Faith','Focus','Intimidation','Performance','Persuasion']
dice=['d4','d6','d8','d10','d12']

def savenew(win,player):

    save(player)
    

    win.destroy()
def save(pl):
    
    data=[]
    with open('saves.json','a'): pass
    with open('saves.json','r+') as f:
        f.seek(0)
        try:
            data=json.load(f)
            
            added=0
            for i in range(len(data)):
                print('Checking #'+str(i))
                if pl['id'] in data[i]['id']:
                    data[i]=pl
                    print('Overwriting')
                    added=1
                i+=1
            if added==0:
                print('Adding')
                data.append(pl)
                
            
            f.seek(0)
            
            json.dump(data,f,indent=4)
        except:
            
            data.append(pl)
            
            f.seek(0)
            json.dump(data,f,indent=4)

        

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
    global mainplayer
    mainplayer={}
    
    with open('saves.json','rb') as f:
        data=json.load(f)
    players=[]
    i=0
    for i in range(len(data)):
        players.append(data[i]['id'])
        
        if players[i]==n[0]:
            mainplayer=data[i]
        
   
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
        tk.Label(frame,text='Name: ').grid(row=0,column=0)
        name=tk.Entry(frame,width=30)
        name.grid(row=0,column=1)
        tk.Label(frame,text='Item Category: ').grid(row=0,column=2)
        categories=['Select an option...','Animals and Tack','Adventuring Gear','Clothing','Computers and Electronics',
                    'Firearms Accessories','Food','Personal Defense','Surveillance','Ammunition']
        choice=tk.StringVar()
        choice.set(categories[0])
        tk.OptionMenu(frame,choice,*categories).grid(row=0,column=3)

        tk.Label(frame,text='Cost: ').grid(row=1,column=0)
        cost=tk.Entry(frame,width=10)
        cost.grid(row=1,column=1)
        cost.insert(0,'0')

        tk.Label(frame,text='Weight: ').grid(row=1,column=2)
        weight=tk.Entry(frame,width=10)
        weight.grid(row=1,column=3)
        weight.insert(0,'0')

        tk.Label(frame,text='Notes: ').grid(row=2,column=0)
        notes=tk.Text(frame,width=40,height=5)
        notes.grid(row=3,column=1,columnspan=3)
        tk.Button(frame,text='Save',command=lambda:[finished.set('Saved!'),savegear(mode='Gear',name=name.get(),style=choice.get(),money=cost.get(),lb=weight.get(),info=notes.get(1.0,tk.END)), finished.set('Saved '+name.get())]).grid(row=0,column=15)
        finished=tk.StringVar()
        finished.set('')
        tk.Label(frame,textvariable=finished).grid(row=0,column=17)
        tk.Button(frame,text='Clear',command=lambda:weapons(frame,weapon)).grid(row=0,column=16)          
    if mode=='Armor':
        tk.Label(frame,text='Name: ').grid(row=0,column=0)
        name=tk.Entry(frame,width=30)
        name.grid(row=0,column=1,columnspan=5)
        tk.Label(frame,text="Era: ").grid(row=0,column=6)
        times=['Midieval','Modern','Futuristic']
        age=tk.StringVar()
        age.set(times[0])
        drop0=tk.OptionMenu(frame,age,*times)
        drop0.grid(row=0,column=7)

        tk.Label(frame,text='Material type: ').grid(row=1,column=7)
        material_types=['Select one below...','Cloth/Light Leather','Thick Leather/Tough Hide','Chain Mail','Bronze Armor (Pre-Iron Age)','Plate Mail','Body Armor (Modern)','Light/Civilian (Futuristic)','Military (Futuristic)']
        mats=tk.StringVar()
        mats.set(material_types[0])
        drop1=tk.OptionMenu(frame,mats,*material_types)
        drop1.grid(row=1,column=8)

        tk.Label(frame,text='Slots').grid(row=1,column=0)
        armored1=tk.IntVar()
        armored2=tk.IntVar()
        armored3=tk.IntVar()
        armored4=tk.IntVar()
        armored5=tk.IntVar()
        slots=['Head','Face','Torso','Legs','Feet']

        
        tk.Checkbutton(frame,text=slots[0],variable=armored1,onvalue=1,offvalue=0).grid(row=1,column=1)
        tk.Checkbutton(frame,text=slots[1],variable=armored2,onvalue=1,offvalue=0).grid(row=1,column=2)
        tk.Checkbutton(frame,text=slots[2],variable=armored3,onvalue=1,offvalue=0).grid(row=1,column=3)
        tk.Checkbutton(frame,text=slots[3],variable=armored4,onvalue=1,offvalue=0).grid(row=1,column=4)
        tk.Checkbutton(frame,text=slots[4],variable=armored5,onvalue=1,offvalue=0).grid(row=1,column=5)
            
        tk.Label(frame,text='Armor Value').grid(row=2,column=0)
        armor_value=tk.Entry(frame,width=10)
        armor_value.grid(row=2,column=1)
        armor_value.insert(0,'0')

        tk.Label(frame,text='Cost: ').grid(row=3,column=0)
        cost=tk.Entry(frame,width=10)
        cost.grid(row=3,column=1)
        cost.insert(0,'0')

        tk.Label(frame,text='Weight: ').grid(row=3,column=2)
        weight=tk.Entry(frame,width=10)
        weight.grid(row=3,column=3)
        weight.insert(0,'0')

        tk.Label(frame,text='Notes: ').grid(row=4,column=0)
        notes=tk.Text(frame,width=40,height=5)
        notes.grid(row=5,column=1,columnspan=5)

        tk.Button(frame,text='Save',command=lambda:[finished.set('Saved!'),savegear(mode='Armor',material=mats.get(),slot=[armored1,armored2,armored3,armored4,armored5],armor=armor_value.get(),name=name.get(),era=age.get(),money=cost.get(),lb=weight.get(),info=notes.get(1.0,tk.END)), finished.set('Saved '+name.get())]).grid(row=0,column=15)
        finished=tk.StringVar()
        finished.set('')
        tk.Label(frame,textvariable=finished).grid(row=0,column=17)
        tk.Button(frame,text='Clear',command=lambda:weapons(frame,weapon)).grid(row=0,column=16)
        
        
    if mode=='Weapons':
        tk.Label(frame,text="Melee, Ranged, or Special? \n(melee includes shields,\nspecial includes things like cannons, \ngrenades, and siege equipment)").grid(row=0,column=0)
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
        name=tk.Entry(melee,width=30)
        name.grid(row=0,column=1,columnspan=3)
        
        tk.Label(melee,text="Era: ").grid(row=0,column=6)
        times=['Midieval','Modern','Futuristic']
        age=tk.StringVar()
        age.set(times[0])
        drop0=tk.OptionMenu(melee,age,*times)
        drop0.grid(row=0,column=7)
        
        tk.Label(melee,text="Damage:").grid(row=1,column=0)
        strdie=tk.IntVar()
        c1=tk.Checkbutton(melee,text='Str?',variable=strdie,onvalue=1,offvalue=0)
        c1.grid(row=1,column=1)
        ndice=tk.Entry(melee,width=5)
        ndice.grid(row=1,column=2)
        ndice.insert(0,'0')
        dice1=['0','d4','d6','d8','d10','d12']
        diechoice=tk.StringVar()
        diechoice.set('d4')
        drop=tk.OptionMenu(melee,diechoice,*dice1)
        drop.grid(row=1,column=3)
        tk.Label(melee,text='+').grid(row=1,column=4)
        extra=tk.Entry(melee,width=5)
        extra.grid(row=1,column=5)
        extra.insert(0,'0')
        
        tk.Label(melee,text="Min Str").grid(row=2,column=0)
        strchoice=tk.StringVar()
        strchoice.set('d4')
        drop2=tk.OptionMenu(melee,strchoice,*dice)
        drop2.grid(row=2,column=1)
        
        tk.Label(melee,text='AP').grid(row=3,column=0)
        ap=tk.Entry(melee,width=10)
        ap.grid(row=3,column=1)
        ap.insert(0,'0')
        
        tk.Label(melee,text='Parry bonus: ').grid(row=3,column=6)
        parry=tk.Entry(melee,width=10)
        parry.grid(row=3,column=7)
        parry.insert(0,'0')
        
        
        tk.Label(melee,text="Weight").grid(row=4,column=0)
        weight=tk.Entry(melee,width=10)
        weight.grid(row=4,column=1)
        weight.insert(0,'0')
        
        tk.Label(melee,text='Cost').grid(row=5,column=0)
        cost=tk.Entry(melee,width=10)
        cost.grid(row=5,column=1)
        cost.insert(0,'0')
        
        tk.Label(melee,text='Notes:').grid(row=7,column=0)
        notes=tk.Text(melee,width=40,height=5)
        notes.grid(row=8,column=1,columnspan=7)
        
        tk.Button(melee,text='Save',command=lambda:[finished.set('Saved!'),savegear(mode=weapon,name=name.get(),era=age.get(),damage=[strdie.get(),ndice.get()+diechoice.get(),extra.get(),ap.get(),parry.get()],
                                                            req=strchoice.get(),lb=weight.get(),money=cost.get(),info=notes.get(1.0,tk.END)), finished.set('Saved '+name.get())]).grid(row=0,column=15)
        finished=tk.StringVar()
        finished.set('')
        tk.Label(melee,textvariable=finished).grid(row=0,column=17)
        tk.Button(melee,text='Clear',command=lambda:weapons(frame,weapon)).grid(row=0,column=16)
    if weapon=='Ranged':
        ranged=tk.Frame(frame)
        ranged.grid()
        tk.Label(ranged,text="Weapon Name: ").grid(row=0,column=0)
        name=tk.Entry(ranged,width=30)
        name.grid(row=0,column=1,columnspan=3)
        range_styles=['Select one...','Thrown','Drawn','Black Powder - Pistol','Black Powder - Musket','Black Powder - Rifle',
                      'Pistol - Revolver','Pistol - Semi-Auto','Submachine Guns','Shotguns',
                      'Rifle - Lever/Bolt Action','Rifle - Assault','Machine Guns','Lasers (Futuristic)']
        tk.Label(ranged,text='Weapon Styles:').grid(row=0,column=6)
        choice1=tk.StringVar()
        choice1.set(range_styles[0])
        tk.OptionMenu(ranged,choice1,*range_styles).grid(row=0,column=7)
            
        
        tk.Label(ranged,text="Era: ").grid(row=0,column=8)
        times=['Midieval','Modern','Futuristic']
        age=tk.StringVar()
        age.set(times[0])
        drop0=tk.OptionMenu(ranged,age,*times)
        drop0.grid(row=0,column=9)
        
        tk.Label(ranged,text="Damage:").grid(row=1,column=0)
        strdie=tk.IntVar()
        c1=tk.Checkbutton(ranged,text='Str?',variable=strdie,onvalue=1,offvalue=0)
        c1.grid(row=1,column=1)
        ndice=tk.Entry(ranged,width=5)
        ndice.grid(row=1,column=2)
        ndice.insert(0,'1')
        dice1=['0','d4','d6','d8','d10','d12']
        diechoice=tk.StringVar()
        diechoice.set('d4')
        drop=tk.OptionMenu(ranged,diechoice,*dice1)
        drop.grid(row=1,column=3)
        tk.Label(ranged,text='+').grid(row=1,column=4)
        extra=tk.Entry(ranged,width=5)
        extra.grid(row=1,column=5)
        extra.insert(0,'0')
        
        baserange=[3,4,5,10,12,15,20,24,30,50]
        rangezones=[[1,2,4]]*len(baserange)
        rangestring=['']*len(baserange)
        for i in range(len(rangezones)):
            rangezones[i]=[x*baserange[i] for x in rangezones[i]]
            for j in range(len(rangezones[i])):
                rangestring[i]+=str(rangezones[i][j])
                if j<len(rangezones[i])-1:
                    rangestring[i]+='/'
        range_options=['Select one...']
        for i in range(len(rangezones)):
            range_options.append(rangestring[i])
        choice2=tk.StringVar()
        choice2.set(range_options[0])
        tk.Label(ranged,text='Range Markings: ').grid(row=2,column=0)
        tk.OptionMenu(ranged,choice2,*range_options).grid(row=2,column=1)

        tk.Label(ranged,text='Shots').grid(row=3,column=6)
        shots=tk.Entry(ranged,width=10)
        shots.grid(row=3,column=7)
        shots.insert(0,'10')

        tk.Label(ranged,text='Rate of Fire: ').grid(row=2,column=6)
        RoF=tk.Entry(ranged,width=10)
        RoF.grid(row=2,column=7)
        RoF.insert(0,'1')

        tk.Label(ranged,text="Min Str").grid(row=3,column=0)
        strchoice=tk.StringVar()
        strchoice.set('d4')
        drop2=tk.OptionMenu(ranged,strchoice,*dice)
        drop2.grid(row=3,column=1)

        
        tk.Label(ranged,text='AP').grid(row=4,column=0)
        ap=tk.Entry(ranged,width=10)
        ap.grid(row=4,column=1)
        ap.insert(0,'0')
        
        tk.Label(ranged,text='Parry bonus: ').grid(row=4,column=6)
        parry=tk.Entry(ranged,width=10)
        parry.grid(row=4,column=7)
        parry.insert(0,'0')
        
        
        tk.Label(ranged,text="Weight").grid(row=5,column=0)
        weight=tk.Entry(ranged,width=10)
        weight.grid(row=5,column=1)
        weight.insert(0,'0')
        
        tk.Label(ranged,text='Cost').grid(row=6,column=0)
        cost=tk.Entry(ranged,width=10)
        cost.grid(row=6,column=1)
        cost.insert(0,'0')
        
        tk.Label(ranged,text='Notes:').grid(row=7,column=0)
        notes=tk.Text(ranged,width=40,height=5)
        notes.grid(row=8,column=1,columnspan=7)
        
        tk.Button(ranged,text='Save',command=lambda:[savegear(mode=weapon,name=name.get(),era=age.get(),ammo=shots.get(),style=choice1.get(),rate=RoF.get(),range_marks=choice2.get(),
                                                                                    damage=[strdie.get(),ndice.get()+diechoice.get(),extra.get(),ap.get(),parry.get()],
                                                                                    req=strchoice.get(),lb=weight.get(),money=cost.get(),info=notes.get(1.0,tk.END)),
                                                                                    finished.set('Saved '+name.get())]).grid(row=0,column=15)
        finished=tk.StringVar()
        finished.set('')
        tk.Label(ranged,textvariable=finished).grid(row=0,column=17)
        tk.Button(ranged,text='Clear',command=lambda:weapons(frame,weapon)).grid(row=0,column=16)
    if weapon=='Special':
        special=tk.Frame(frame)
        special.grid()
        tk.Label(special,text="Weapon Name: ").grid(row=0,column=0)
        name=tk.Entry(special,width=30)
        name.grid(row=0,column=1,columnspan=3)
        range_styles=['Select one...','Cannons','Catapults','Flamethrowers','Grenades','Mines','Missiles','Rocket Launchers and Torpedos']
        tk.Label(special,text='Weapon Styles:').grid(row=0,column=6)
        choice1=tk.StringVar()
        choice1.set(range_styles[0])
        tk.OptionMenu(special,choice1,*range_styles).grid(row=0,column=7)
            
        
        tk.Label(special,text="Era: ").grid(row=0,column=8)
        times=['Midieval','Modern','Futuristic']
        age=tk.StringVar()
        age.set(times[0])
        drop0=tk.OptionMenu(special,age,*times)
        drop0.grid(row=0,column=9)
        
        tk.Label(special,text="Damage:").grid(row=1,column=0)
        strdie=tk.IntVar()
        c1=tk.Checkbutton(special,text='Str?',variable=strdie,onvalue=1,offvalue=0)
        c1.grid(row=1,column=1)
        ndice=tk.Entry(special,width=5)
        ndice.grid(row=1,column=2)
        ndice.insert(0,'1')
        dice1=['0','d4','d6','d8','d10','d12']
        diechoice=tk.StringVar()
        diechoice.set('d4')
        drop=tk.OptionMenu(special,diechoice,*dice1)
        drop.grid(row=1,column=3)
        tk.Label(special,text='+').grid(row=1,column=4)
        extra=tk.Entry(special,width=5)
        extra.grid(row=1,column=5)
        extra.insert(0,'0')
        
        baserange=[3,4,5,10,12,15,20,24,30,50]
        rangezones=[[1,2,4]]*len(baserange)
        rangestring=['']*len(baserange)
        for i in range(len(rangezones)):
            rangezones[i]=[x*baserange[i] for x in rangezones[i]]
            for j in range(len(rangezones[i])):
                rangestring[i]+=str(rangezones[i][j])
                if j<len(rangezones[i])-1:
                    rangestring[i]+='/'
        range_options=['Select one...']
        for i in range(len(rangezones)):
            range_options.append(rangestring[i])
        choice2=tk.StringVar()
        choice2.set(range_options[0])
        tk.Label(special,text='Range Markings: ').grid(row=2,column=0)
        tk.OptionMenu(special,choice2,*range_options).grid(row=2,column=1)

        tk.Label(special,text='Shots').grid(row=3,column=6)
        shots=tk.Entry(special,width=10)
        shots.grid(row=3,column=7)
        shots.insert(0,'10')

        tk.Label(special,text='Rate of Fire: ').grid(row=2,column=6)
        RoF=tk.Entry(special,width=10)
        RoF.grid(row=2,column=7)
        RoF.insert(0,'1')

        tk.Label(special,text="Min Str").grid(row=3,column=0)
        strchoice=tk.StringVar()
        strchoice.set('d4')
        drop2=tk.OptionMenu(special,strchoice,*dice)
        drop2.grid(row=3,column=1)

        
        tk.Label(special,text='AP').grid(row=4,column=0)
        ap=tk.Entry(special,width=10)
        ap.grid(row=4,column=1)
        ap.insert(0,'0')
        
        tk.Label(special,text='Blast Radius ').grid(row=4,column=6)
        blast_size=['Select one...','Cone','SBR','MBR','LBR']
        choice3=tk.StringVar()
        choice3.set(blast_size[0])
        tk.OptionMenu(special,choice3,*blast_size).grid(row=4,column=7)

        
        
        tk.Label(special,text="Weight").grid(row=5,column=0)
        weight=tk.Entry(special,width=10)
        weight.grid(row=5,column=1)
        weight.insert(0,'0')
        
        tk.Label(special,text='Cost').grid(row=6,column=0)
        cost=tk.Entry(special,width=10)
        cost.grid(row=6,column=1)
        cost.insert(0,'0')
        
        tk.Label(special,text='Notes:').grid(row=7,column=0)
        notes=tk.Text(special,width=40,height=5)
        notes.grid(row=8,column=1,columnspan=7)
        
        tk.Button(special,text='Save',command=lambda:[savegear(mode=weapon,name=name.get(),era=age.get(),ammo=shots.get(),style=choice1.get(),rate=RoF.get(),range_marks=choice2.get(),
                                                                                    damage=[strdie.get(),ndice.get()+diechoice.get(),extra.get(),ap.get(),'0'],blast_radius=choice3.get(),
                                                                                    req=strchoice.get(),lb=weight.get(),money=cost.get(),info=notes.get(1.0,tk.END)),
                                                                                    finished.set('Saved '+name.get())]).grid(row=0,column=15)
        finished=tk.StringVar()
        finished.set('')
        tk.Label(special,textvariable=finished).grid(row=0,column=17)
        tk.Button(special,text='Clear',command=lambda:weapons(frame,weapon)).grid(row=0,column=16)
        
        
global mainarmory
with open('armory.json','a'): pass
with open('armory.json','r+') as f:
    f.seek(0)
    try:
        mainarmory=json.load(f)
        f.seek(0)
    except:
        mainarmory={'Weapons':{'Melee': {},'Ranged':{},'Special':{}},
            'Armor':{},
            'Gear':{},
            'Vehicles':{}}
        json.dump(mainarmory,f,indent=4)

def savegear(armory=mainarmory,mode = 'Melee',name = 'Unarmed Strike',era='Midieval', style='Pistol',rate='1',blast_radius='None',ammo='50',range_marks='3/6/12',
             damage = ['0','0','0','0','0'],slot=[0,0,0,0,0],armor='0',req='none',lb='0',money='0',info='Punch the sucka!',material='Cloth/Light Leather'):
    if mode=='Gear':
        display_string=name+'\nCategory: '+style+'\nWeight'+lb+'lbs\nCost: '+money+'\nNotes: '+info
        gear_keys=list(armory['Gear'].keys())
        check=False
        for x in gear_keys:
            if style in x:
                check=True
        if not check:
            armory['Gear'][style]={}
        armory['Gear'][style][name]={'display':display_string,
                                     'Weight':float(lb),
                                     'Cost':money,
                                     'Notes':info,
                                     'Source':'Homebrew'}        

    if mode=='Armor':
        display_string=f'{name}\nEra: {era}\nArmor Value: {armor}\nMin Str: {req}\nWeight: {lb}\nCost: {money}\nNotes: {info}'
    
        armored=[False]*5
        for i in range(len(slot)):
            if slot[i].get()==1:
                armored[i]=True
        armor_keys=list(armory['Armor'])
        check=False
        for x in armor_keys:
            if era in x:
                chekc=True
        if not check:
            armory['Armor'][material]={}
        armory['Armor'][material][name]={'display':display_string,
                                        'equipped':False,
                                        'type':material,
                                        'era':era,
                                        'armor':armor,
                                        'head':armored[0],
                                        'face':armored[1],
                                        'torso':armored[2],
                                        'legs':armored[3],
                                        'feet':armored[4],
                                        'Min Str':req,
                                        'Weight':float(lb),
                                        'Cost':money,
                                        'Notes':info,
                                        'Source':'Homebrew'}
                                       
    if mode=='Melee':
        if damage[0]==1:
            damage_string='Str'
            if damage[1]!=0:
                damage_string+='+'+damage[1]
        else:
            damage_string=damage[1]
        if int(damage[2])!=0:
            damage_string+='+'+damage[2]
        damage_number=0
        for i in range(len(dice)):
            if damage[0] == dice[i]:
                damage_number=4+2*i
                i=len(dice)
        display_string=name+'\nEra: '+era+'\n Damage '+damage_string+'\nStr Req: '+req+'\nWeight: '+lb+' lbs\nCost: '+money+'\nNotes: '+info
        armory['Weapons']['Melee'][name]={'display':display_string,
                                          'equipped':False,
                                          'era':era,
                                          'damage':damage_number,
                                          'modifier':int(damage[2]),
                                          'AP':int(damage[3]),
                                          'Parry':int(damage[4]),
                                          'Min Str':req,
                                          'Weight':float(lb),
                                          'Cost':money,
                                          'Notes':info,
                                          'Source':'Homebrew'}
    if mode=='Ranged':
        if damage[0]==1:
            damage_string='Str'
            if damage[1]!=0:
                damage_string+='+'+damage[1]
        else:
            damage_string=damage[1]
        if int(damage[2])!=0:
            damage_string+='+'+damage[2]
        if damage[3]!=0:
            damage_string+=' AP '+damage[4]
        damage_number=0
        for i in range(len(dice)):
            if damage[0] == dice[i]:
                damage_number=4+2*i
                i=len(dice)
        display_string=name+'\nWeapon Type: '+style+'\nEra: '+era+'\n Damage '+damage_string+'\nRange: '+range_marks+'\nShots: '+ammo+'\nRate of Fire: '+rate+'\nStr Req: '+req+'\nWeight: '+lb+' lbs\nCost: '+money+'\nNotes: '+info
        armory['Weapons']['Ranged'][name]={'display':display_string,
                                           'equipped':False,
                                           'era':era,
                                           'style':style,
                                           'damage_display':damage_string,
                                           'damage':damage_number,
                                           'modifier':int(damage[2]),
                                           'AP':int(damage[3]),
                                           'Parry':int(damage[4]),
                                           'Range':range_marks,
                                           'Rate of Fire':rate,
                                           'Min Str':req,
                                           'Weight':float(lb),
                                           'Cost':money,
                                           'Notes':info,
                                           'Source':'Homebrew'}
    if mode=='Special':
        if damage[0]==1:
            damage_string='Str'
            if damage[1]!=0:
                damage_string+='+'+damage[1]
        else:
            damage_string=damage[1]
        if int(damage[2])!=0:
            damage_string+='+'+damage[2]
        if damage[3]!=0:
            damage_string+=' AP '+damage[4]
        damage_number=0
        for i in range(len(dice)):
            if damage[0] == dice[i]:
                damage_number=4+2*i
                i=len(dice)
        display_string=name+'\nWeapon Type: '+style+'\nEra: '+era+'\n Damage '+damage_string+'\nRange: '+range_marks+'\nShots: '+ammo+'\nBlast Radius: '+blast_radius+'\nRate of Fire: '+rate+'\nStr Req: '+req+'\nWeight: '+lb+' lbs\nCost: '+money+'\nNotes: '+info
        armory['Weapons']['Special'][name]={'display':display_string,
                                            'equipped':False,
                                            'era':era,
                                            'style':style,
                                            'damage_display':damage_string,
                                            'damage':damage_number,
                                            'modifier':int(damage[2]),
                                            'AP':int(damage[3]),
                                            'Blast Radius':blast_radius, 
                                            'Range':range_marks,
                                            'Rate of Fire':rate,
                                            'Min Str':req,
                                            'Weight':float(lb),
                                            'Cost':money,
                                            'Notes':info,
                                            'Source':'Homebrew'}
    mainarmory=armory    
    with open('armory.json','w') as f:
        f.seek(0)
        json.dump(armory,f,indent=4)

    time.sleep(1)
        
def mainstats():
    killchildren(main)
    tabcontrol=ttk.Notebook(main)
    statspage=tk.Frame(tabcontrol)
    combatpage=tk.Frame(tabcontrol)
    settings=tk.Frame(tabcontrol)
    concept=tk.Frame(tabcontrol)
    edges=tk.Frame(tabcontrol)
    inventory=tk.Frame(tabcontrol)
    journal=tk.Frame(tabcontrol)
    advances=tk.Frame(tabcontrol)
#Settings Page    
    
#Attributes Page
    statspage.grid(sticky='nesw')
    tk.Label(statspage,text=mainplayer['concept']['Name'],font='Helvetica 30 bold',padx=10, pady=10).grid(row=0,column=0,columnspan=4)
    i=0
    global buttons
    buttons=[None]*37
    m=[None]*37
    l1=[None]*37
    stringa=str()
    wounds=tk.IntVar()
    wounds.set(mainplayer['stats']['Wounds'])
    fatigue=tk.IntVar()
    fatigue.set(mainplayer['stats']['Fatigue'])
    wstring=tk.StringVar()
    wstring.set('Wounds: '+str(mainplayer['stats']['Wounds']))
    fstring=tk.StringVar()
    fstring.set('Fatigue: '+str(mainplayer['stats']['Fatigue']))
    global texta
    texta=[None]*37
    for x in attributelist:
        texta[i]=tk.StringVar()
        texta[i].set(attributelist[i]+': '+mainplayer['Attributes'][attributelist[i]]['display'])
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
        buttons[i]=tk.Button(statspage,text='ROLL',command=lambda j=i:rollskills(statspage,l1[j],mainplayer['Attributes'][attributelist[j]]['size'],mainplayer['Attributes'][attributelist[j]]['size']-wounds.get()-fatigue.get()+int(isBlank(m[j].get()))))
        buttons[i].grid(row=r,column=c+2)
        i+=1
    agiskills=tk.Frame(statspage,bd=3,relief='sunken')
    smartskills=tk.Frame(statspage,bd=3,relief='sunken')
    spiritskills=tk.Frame(statspage,bd=3,relief='sunken')
    agiskills.grid(row=3,column=0,rowspan=9,columnspan=4)
    smartskills.grid(row=3,column=4,rowspan=18,columnspan=4)
    spiritskills.grid(row=3,column=8,rowspan=5,columnspan=4)
    for x in skilllist:
        k=i-5
        texta[i]=tk.StringVar()
        texta[i].set(skilllist[k]+': '+mainplayer['Skills'][skilllist[k]]['display'])
        
        if k<9:
            r=k
            c=0
            tk.Label(agiskills,textvariable=texta[i], font='Helvetica',padx=10,pady=3).grid(row=r,column=c)
            m[i]=tk.Entry(agiskills,width=10)
            m[i].grid(row=r,column=c+1)
            m[i].insert(0,'0')
            l1[i]=tk.Label(agiskills,text='',width=20,padx=10,pady=3)
            l1[i].grid(row=r,column=c+3)
            buttons[i]=tk.Button(agiskills,text='ROLL',command=lambda j=i:rollskills(statspage,l1[j],mainplayer['Skills'][skilllist[j]]['size'],mainplayer['Skills'][skilllist[j]]['modifier']-wounds.get()-fatigue.get()+int(isBlank(m[j].get()))))
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
            buttons[i]=tk.Button(smartskills,text='ROLL',command=lambda j=i:rollskills(statspage,l1[j],mainplayer['Skills'][skilllist[j]]['size'],mainplayer['Skills'][skilllist[j]]['modifier']-wounds.get()-fatigue.get()+int(isBlank(m[j].get()))))
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
            buttons[i]=tk.Button(spiritskills,text='ROLL',command=lambda j=i:rollskills(statspage,l1[j],mainplayer['Skills'][skilllist[j]]['size'],mainplayer['Skills'][skilllist[j]]['modifier']-wounds.get()-fatigue.get()+int(isBlank(m[j].get()))))
            buttons[i].grid(row=r,column=c+2)

        i+=1
        
    
    
    incap('w',mainplayer['stats']['Wounds'],buttons)
    incap('f',mainplayer['stats']['Fatigue'],buttons)
    tk.Button(statspage,textvariable=wstring,command=lambda:[wounds.set(min(3,wounds.get()+1)),wstring.set('Wounds: '+str(wounds.get())),incap('w',wounds.get(),buttons)]).grid(row=0,column=10)
    tk.Button(statspage,text='Heal',command=lambda:[wounds.set(max(0,wounds.get()-1)),wstring.set('Wounds: '+str(wounds.get())),incap('w',wounds.get(),buttons)]).grid(row=0,column=11)
    tk.Button(statspage,textvariable=fstring,command=lambda:[fatigue.set(min(2,fatigue.get()+1)),fstring.set('Fatigue: '+str(fatigue.get())),incap('f',fatigue.get(),buttons)]).grid(row=0,column=8)
    tk.Button(statspage,text='Rest',command=lambda:[fatigue.set(max(0,fatigue.get()-1)),fstring.set('Fatigue: '+str(fatigue.get())),incap('f',fatigue.get(),buttons)]).grid(row=0,column=9)
#Combat Page
    combatpage.grid()
    tk.Label(combatpage,text='Combat').grid(row=0,column=0)
    tk.Label(combatpage,text='Statistics').grid(row=1,column=0)
    keys=list(mainplayer['stats'].keys())
    i=0
    cp_strings=[]
    
    for x in keys:
        cp_strings.append(tk.StringVar())
        cp_strings[i].set(mainplayer['stats'][x])
        print (x,mainplayer['stats'][x])
        i+=1
        tk.Label(combatpage,text=x).grid(row=i,column=0)
        tk.Label(combatpage,textvariable=cp_strings[i-1]).grid(row=i,column=1)
#Background page

#Edges Page

#Inventory Page
    inventory.grid(sticky='nesw')
    w=int(main.winfo_width()/2)
    h=int(main.winfo_height()/2)
    gear=tk.Frame(inventory,bd=3,relief='sunken',width=w,height=h)
    armor=tk.Frame(inventory,bd=3,relief='sunken',width=w,height=h)
    weapons=tk.Frame(inventory,bd=3,relief='sunken',width=w,height=h)
    vehicles=tk.Frame(inventory,bd=3,relief='sunken',width=w,height=h)
    inventory.grid_rowconfigure(0,weight=1)
    inventory.grid_columnconfigure(0,weight=10)
    inventory.grid_rowconfigure(1,weight=1)
    inventory.grid_columnconfigure(1,weight=10)
    inventory.grid_columnconfigure(2,weight=2)
    gear.grid(row=0,column=0,sticky='nesw',padx=5)
    armor.grid(row=0,column=1,sticky='nesw',padx=5)
    weapons.grid(row=1,column=0,sticky='nesw',padx=5)
    vehicles.grid(row=1,column=1,sticky='nesw',padx=5)


    gear.grid_columnconfigure(0,weight=1)
    gear.grid_rowconfigure(1,weight=1)
    tk.Label(gear,text='Gear',font='helvetica',bd=3).grid(row=0,column=0)
    gear_canvas=tk.Canvas(gear, borderwidth=0)
    gear_subframe=tk.Frame(gear_canvas,bd=1,relief='sunken')
    gear_scroll=tk.Scrollbar(gear,orient='vertical',command=gear_canvas.yview)
    gear_canvas.configure(yscrollcommand=gear_scroll.set)
    gear_scroll.grid(row=1,column=1,sticky='nesw')
    gear_canvas.grid(row=1,column=0,sticky='nesw')
    gear_id=gear_canvas.create_window((0,0), window=gear_subframe)
    #gear_subframe.pack(fill='both',expand=1)
    def onFrameConfigure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))
    def onCanvasConfigure(canvas,identifier):
        print('hello')
        canvas.itemconfigure(identifier,width=canvas.winfo_width())
    gear_canvas.bind('<Configure>',lambda event,canvas=canvas:onCanvasConfigure(gear_canvas,gear_id))
    gear_subframe.bind('<Configure>',lambda event,canvas=canvas:onFrameConfigure(gear_canvas))
    gear_subframe.grid_columnconfigure(0,weight=1)
    gear_subframe.grid_columnconfigure(1,weight=1)
    gear_subframe.grid_columnconfigure(2,weight=1)
    gear_subframe.grid_columnconfigure(3,weight=5)
    getgear=list(mainplayer['Gear']['Inventory'].keys())
    tk.Label(gear_subframe,text='Item').grid(row=0,column=0)
    tk.Label(gear_subframe,text='Weight').grid(row=0,column=1)
    tk.Label(gear_subframe,text='Cost').grid(row=0,column=2)
    tk.Label(gear_subframe,text='Notes').grid(row=0,column=3)
    print(getgear)
    if len(getgear)>0:
        for i in range(len(getgear)):
            tk.Label(gear_subframe,text=getgear[i]).grid(row=i+1,column=0)
            tk.Label(gear_subframe,text=mainplayer['Gear']['Inventory'][getgear[i]]['Weight']).grid(row=i+1,column=1)
            tk.Label(gear_subframe,text=mainplayer['Gear']['Inventory'][getgear[i]]['Cost']).grid(row=i+1,column=2)
            tk.Label(gear_subframe,text=mainplayer['Gear']['Inventory'][getgear[i]]['Notes'],wraplength=250).grid(row=i+1,column=3)

    
    armor.grid_columnconfigure(0,weight=1)
    armor.grid_rowconfigure(1,weight=1)
    tk.Label(armor,text='Armor',font='helvetica',bd=3).grid(row=0,column=0)
    armor_canvas=tk.Canvas(armor, borderwidth=0)
    armor_subframe=tk.Frame(armor_canvas,bd=1,relief='sunken')
    armor_scroll=tk.Scrollbar(armor,orient='vertical',command=armor_canvas.yview)
    armor_canvas.configure(yscrollcommand=armor_scroll.set)
    armor_scroll.grid(row=1,column=1,sticky='nesw')
    armor_canvas.grid(row=1,column=0,sticky='nesw')
    armor_id=armor_canvas.create_window((0,0), window=armor_subframe)
    #armor_subframe.pack(fill='both',expand=1)
    armor_canvas.bind('<Configure>',lambda event,canvas=canvas:onCanvasConfigure(armor_canvas,armor_id))
    armor_subframe.bind('<Configure>',lambda event,canvas=canvas:onFrameConfigure(armor_canvas))
    armor_subframe.grid_columnconfigure(0,weight=1)
    armor_subframe.grid_columnconfigure(1,weight=1)
    armor_subframe.grid_columnconfigure(2,weight=1)
    armor_subframe.grid_columnconfigure(3,weight=4)
    getarmor=list(mainplayer['Gear']['Armor'].keys())
    tk.Label(armor_subframe,text='Item').grid(row=0,column=0)
    tk.Label(armor_subframe,text='Weight').grid(row=0,column=1)
    tk.Label(armor_subframe,text='Cost').grid(row=0,column=2)
    tk.Label(armor_subframe,text='Notes').grid(row=0,column=3)
    #print(getarmor)
    if len(getarmor)>0:
        equiptext=[]
        for i in range(len(getarmor)):
            equiptext.append(tk.StringVar())
            if mainplayer['Gear']['Armor'][getarmor[i]]['equipped']:
                equiptext[i].set('Unequip')
            else:
                equiptext[i].set('Equip')
            for x in equiptext:
                print(x.get())
            tk.Label(armor_subframe,text=getarmor[i]).grid(row=i+1,column=0)
            tk.Label(armor_subframe,text=mainplayer['Gear']['Armor'][getarmor[i]]['Weight']).grid(row=i+1,column=1)
            tk.Label(armor_subframe,text=mainplayer['Gear']['Armor'][getarmor[i]]['Cost']).grid(row=i+1,column=2)
            tk.Label(armor_subframe,text=mainplayer['Gear']['Armor'][getarmor[i]]['Notes'],wraplength=250).grid(row=i+1,column=3)
            tk.Button(armor_subframe,textvariable=equiptext[i],command= lambda j=i:[equiptext[j].set(equipunequip(mainplayer,'Armor',getarmor[j])),stat_checker(mainplayer),cp_strings[5].set(mainplayer['stats']['Armor'])]).grid(row=i+1,column=4)

    weapons.grid_columnconfigure(0,weight=1)
    weapons.grid_rowconfigure(1,weight=1)
    tk.Label(weapons,text='Weapons',font='helvetica',bd=3).grid(row=0,column=0)
    weapons_canvas=tk.Canvas(weapons, borderwidth=0)
    weapons_subframe=tk.Frame(weapons_canvas,bd=1,relief='sunken')
    weapons_scroll=tk.Scrollbar(weapons,orient='vertical',command=weapons_canvas.yview)
    weapons_canvas.configure(yscrollcommand=weapons_scroll.set)
    weapons_scroll.grid(row=1,column=1,sticky='nesw')
    weapons_canvas.grid(row=1,column=0,sticky='nesw')
    weapons_id=weapons_canvas.create_window((0,0), window=weapons_subframe)
    #weapons_subframe.pack(fill='both',expand=1)
    weapons_canvas.bind('<Configure>',lambda event,canvas=canvas:onCanvasConfigure(weapons_canvas,weapons_id))
    weapons_subframe.bind('<Configure>',lambda event,canvas=canvas:onFrameConfigure(weapons_canvas))
    weapons_subframe.grid_columnconfigure(0,weight=1)
    weapons_subframe.grid_columnconfigure(1,weight=1)
    weapons_subframe.grid_columnconfigure(2,weight=1)
    weapons_subframe.grid_columnconfigure(3,weight=5)
    getweapon=list(mainplayer['Gear']['Weapons']['Melee'].keys())
    tk.Label(weapons_subframe,text='Item').grid(row=0,column=0)
    tk.Label(weapons_subframe,text='Weight').grid(row=0,column=1)
    tk.Label(weapons_subframe,text='Cost').grid(row=0,column=2)
    tk.Label(weapons_subframe,text='Notes').grid(row=0,column=3)
    print(getweapon)
    if len(getweapon)>0:
        for i in range(len(getweapon)):
            tk.Label(weapons_subframe,text=getweapon[i]).grid(row=i+1,column=0)
            tk.Label(weapons_subframe,text=mainplayer['Gear']['Weapons']['Melee'][getweapon[i]]['Weight']).grid(row=i+1,column=1)
            tk.Label(weapons_subframe,text=mainplayer['Gear']['Weapons']['Melee'][getweapon[i]]['Cost']).grid(row=i+1,column=2)
            tk.Label(weapons_subframe,text=mainplayer['Gear']['Weapons']['Melee'][getweapon[i]]['Notes'],wraplength=250).grid(row=i+1,column=3)
    
    vehicles.grid_columnconfigure(0,weight=1)
    vehicles.grid_rowconfigure(1,weight=1)
    tk.Label(vehicles,text='vehicles',font='helvetica',bd=3).grid(row=0,column=0)
    vehicles_canvas=tk.Canvas(vehicles, borderwidth=0)
    vehicles_subframe=tk.Frame(vehicles_canvas,bd=1,relief='sunken')
    vehicles_scroll=tk.Scrollbar(vehicles,orient='vertical',command=vehicles_canvas.yview)
    vehicles_canvas.configure(yscrollcommand=vehicles_scroll.set)
    vehicles_scroll.grid(row=1,column=1,sticky='nesw')
    vehicles_canvas.grid(row=1,column=0,sticky='nesw')
    vehicles_id=vehicles_canvas.create_window((0,0), window=vehicles_subframe)
    #vehicles_subframe.pack(fill='both',expand=1)
    vehicles_canvas.bind('<Configure>',lambda event,canvas=canvas:onCanvasConfigure(vehicles_canvas,vehicles_id))
    vehicles_subframe.bind('<Configure>',lambda event,canvas=canvas:onFrameConfigure(vehicles_canvas))
    vehicles_subframe.grid_columnconfigure(0,weight=1)
    vehicles_subframe.grid_columnconfigure(1,weight=1)
    vehicles_subframe.grid_columnconfigure(2,weight=1)
    vehicles_subframe.grid_columnconfigure(3,weight=5)
    getcar=list(mainplayer['Gear']['Inventory'].keys())
    tk.Label(vehicles_subframe,text='Item').grid(row=0,column=0)
    tk.Label(vehicles_subframe,text='Weight').grid(row=0,column=1)
    tk.Label(vehicles_subframe,text='Cost').grid(row=0,column=2)
    tk.Label(vehicles_subframe,text='Notes').grid(row=0,column=3)
    print(getcar)
    if len(getcar)>0:
        for i in range(len(getcar)):
            tk.Label(vehicles_subframe,text=getcar[i]).grid(row=i+1,column=0)
            tk.Label(vehicles_subframe,text=mainplayer['Gear']['Inventory'][getcar[i]]['Weight']).grid(row=i+1,column=1)
            tk.Label(vehicles_subframe,text=mainplayer['Gear']['Inventory'][getcar[i]]['Cost']).grid(row=i+1,column=2)
            tk.Label(vehicles_subframe,text=mainplayer['Gear']['Inventory'][getcar[i]]['Notes'],wraplength=250).grid(row=i+1,column=3)
    

#Journal Page

#Advances Page

#Create Tabs
    tabcontrol.grid(row=0,column=0)
    tabcontrol.add(settings,text='Settings')
    tabcontrol.add(statspage,text='Attributes and Skills')
    tabcontrol.add(combatpage,text='Combat')
    tabcontrol.add(concept, text='Background')
    tabcontrol.add(edges,text='Edges')
    tabcontrol.add(inventory,text='Inventory')
    tabcontrol.add(journal,text='Journal')
    tabcontrol.add(advances,text='Advances')
def isBlank(string):
    if string and string.strip():
        return string
    return 0
def incap(mode,wounds,buttons):
    if mode=='w':
        mainplayer['stats']['Wounds']=wounds
    if mode=='f':
        mainplayer['stats']['Fatigue']=wounds
    
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
    print(len(savedata))
    players=[['','']]*len(savedata)
    for i in range(len(savedata)):
        players[i]=[savedata[i]['id'],savedata[i]['concept']['Name']]
    loading=tk.Toplevel(main)
    tk.Label(loading,text="Who do you want to load?").pack()
    i=0
    while i<len(players):
            
        tk.Button(loading,text=players[i][1],command=lambda j=i:load(loading,players[j])).pack()
        i+=1

def dexp(d,exp):
    roll=random.randint(1,d)
    
    if roll==d:
        exp+=1
        temp=dexp(d,exp)
        roll+=temp[0]
        exp=temp[1]
    return roll,exp
def roll_damage(command):
    results=[0]*len(command)
    for i in range(len(command)):
        print(f'Rolling {command[i][0]}d{command[i][1]}')
        for j in range(command[i][0]):
            results[i]+=dexp(command[i][1],0)[0]
            print(results)
    total=0
    for i in range(len(results)):
        total+=results[i]
    print(total)
    
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
    player={'id':str(uuid.uuid4()),
            'concept':{'Name':'new',
                       'Gender':'',
                       'Age':'',
                       'Description':'',
                       'Background':''},
            'stats':{'Wounds':0,
                     'Fatigue':0,
                     'Run':6,
                     'Parry':2,
                     'Toughness':2,
                     'Armor':0,
                     'Max PP':0,
                     'PP=':0},
            'Race':{'name':'human'},
            'Hinderances':{},
            'Attributes':{},
            'Skills':{},
            'Edges':{},
            'Gear':{'Inventory':{},
                    'Armor':{},
                    'Weapons':{'Melee':{},
                               'Ranged':{},
                               'Special':{}},
                    'Vehicles:':{}},
            'Allies':{},
            'Advances':{}}
                    
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
        install(newstat,player['Attributes'])
        tk.Label(creation,textvariable=a[i]).grid(row=r,column=c+1)
        
        
        tk.Button(creation,text='-',command=lambda j=i:[print(player),attributes[j].set(max(4,attributes[j].get()-2)),
                                                        install({attributelist[j]:options_dict[options[int(attributes[j].get()/2)-1]]},player['Attributes']),
                                                        a[j].set(str(options[int(attributes[j].get()/2)-1]))]).grid(row=r,column=c+2)
        tk.Button(creation,text='+',command=lambda j=i:[attributes[j].set(min(12,attributes[j].get()+2)),
                                                        install({attributelist[j]:options_dict[options[int(attributes[j].get()/2)-1]]},player['Attributes']),
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
        install(newstat,player['Skills'])
        tk.Label(creation,textvariable=s[i]).grid(row=r,column=c+1)
        tk.Button(creation,text='-',command=lambda j=i:[baseskills[j].set(max(2,baseskills[j].get()-2)),
                                                        install({skilllist[j]:options_dict[options[int(baseskills[j].get()/2)-1]]},player['Skills']),
                                                        s[j].set(str(options[int(baseskills[j].get()/2)-1]))]).grid(row=r,column=c+2)
        tk.Button(creation,text='+',command=lambda j=i:[baseskills[j].set(min(12,baseskills[j].get()+2)),
                                                        install({skilllist[j]:options_dict[options[int(baseskills[j].get()/2)-1]]},player['Skills']),
                                                        s[j].set(str(options[int(baseskills[j].get()/2)-1]))]).grid(row=r,column=c+3)     
        i+=1

    print(player)
    tk.Button(creation,text="Next",command=lambda:[install({'Name':name.get()},player['concept']),newcharother(creation,player)]).grid(row=23,column=9)

def newcharother(window,player):
    
    killchildren(window)
    player['stats']['Parry']=player['Skills']['Fighting']['size']/2
    player['stats']['Toughness']=player['Attributes']['Vigor']['size']/2
    tk.Label(window,text="This is where you load info about gear, spells, etc.").pack()
    tk.Button(window,text="Save my shit",command=lambda:savenew(window,player)).pack()
    
    player['stats']['Parry']=player['Skills']['Fighting']['size']/2
    player['stats']['Toughness']=player['Attributes']['Vigor']['size']/2
    



def install(newinfo,storage):
    directory=list(newinfo.keys())
    for x in directory:
        storage[str(x)]=newinfo[str(x)]

def change_attribute(stattype,trait,mode,value):
    options=['Unskilled','d4','d6','d8','d10','d12']
    
    if mode=='modifier':
        mainplayer[stattype][trait][mode]+=value
    if mode=='size':
        if value==-2 and mainplayer[stattype][trait]['display']!=options[0]:
            i=1
            while i<len(options):
                if options[i]==mainplayer[stattype][trait]['display']:
                    mainplayer[stattype][trait]['display']=options[i-1]
                    mainplayer[stattype][trait]['size']+=value
                    if mainplayer[stattype][trait]['display']==options[0]:
                        mainplayer[stattype][trait]['modifier']-=2
                    i=7
                else:
                    i+=1
        elif value==2 and mainplayer[stattype][trait]['display']!=options[5]:
            i=0
            while i < len(options)-1:
                if options[i]==mainplayer[stattype][trait]['display']:
                    mainplayer[stattype][trait]['display']=options[i+1]
                    if i==0:
                        mainplayer[stattype][trait]['modifier']+=2
                    
                    else:
                        mainplayer[stattype][trait]['size']+=value
                    i=7
                else:
                    i+=1
    if mainplayer[stattype][trait]['modifier']<0 and mainplayer[stattype][trait]['display']!=options[0]:
        mainplayer[stattype][trait]['display']='d'+str(mainplayer[stattype][trait]['size'])+'-'+str(abs(mainplayer[stattype][trait]['modifier']))
    elif mainplayer[stattype][trait]['modifier']>0 and mainplayer[stattype][trait]['display']!=options[0]:
        mainplayer[stattype][trait]['display']='d'+str(mainplayer[stattype][trait]['size'])+'+'+str(mainplayer[stattype][trait]['modifier'])
    elif mainplayer[stattype][trait]['modifier']==0 and mainplayer[stattype][trait]['display']!=options[0]:
        mainplayer[stattype][trait]['display']='d'+str(mainplayer[stattype][trait]['size'])
    
                        
    
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
    stattype=['']*37
    die=[None]*37
    for x in allstats:
        if i<3:
            r=1
            c=5*i
            stattype[i]='Attributes'
        elif i<5:
            r=21
            c=5*(i-3)
            stattype[i]='Attributes'
        elif i<14:
            r=i-3
            c=0
            stattype[i]='Skills'
        elif i<32:
            r=i-12
            c=5
            stattype[i]='Skills'
        else:
            r=i-30
            c=10
            stattype[i]='Skills'
        die[i]=tk.StringVar()
        die[i].set(allstats[i]+': '+mainplayer[stattype[i]][allstats[i]]['display'])
        
        tk.Label(update,textvariable=die[i]).grid(row=r,column=c)
        tk.Button(update,text='Step Down',command=lambda j=i:[change_attribute(stattype[j],allstats[j],'size',-2),die[j].set(allstats[j]+': '+mainplayer[stattype[j]][allstats[j]]['display'])]).grid(row=r,column=c+1)
        tk.Button(update,text='Step Up',command=lambda j=i:[change_attribute(stattype[j],allstats[j],'size',2),die[j].set(allstats[j]+': '+mainplayer[stattype[j]][allstats[j]]['display'])]).grid(row=r,column=c+2)
        tk.Button(update,text='-1',command=lambda j=i:[change_attribute(stattype[j],allstats[j],'modifier',-1),die[j].set(allstats[j]+': '+mainplayer[stattype[j]][allstats[j]]['display'])]).grid(row=r,column=c+3)
        tk.Button(update,text='+1',command=lambda j=i:[change_attribute(stattype[j],allstats[j],'modifier',1),die[j].set(allstats[j]+': '+mainplayer[stattype[j]][allstats[j]]['display'])]).grid(row=r,column=c+4)
        i+=1
    
    
    tk.Button(update,text="Apply",command=lambda:[update.destroy(),mainstats()]).grid(row=0, column=3)

def equipment_tab():
    killchildren(main)
    equip=tk.Frame(main)
    equip.grid(row=1,column=0)
    tk.Label(main,text='Equipment Codex\nUse this page to view equipment stats and add them to the character sheet.',font='Helvetica').grid(row=0,column=0)
    equipment_types=list(mainarmory.keys())
    tk.Label(equip,text='What kind of equipment?').grid(row=1,column=0)
    choice=tk.StringVar()
    choice.set(equipment_types[0])
    tk.OptionMenu(equip,choice,*equipment_types).grid(row=1,column=1)
    subframea=tk.Frame(equip)
    subframea.grid(row=2,column=0,columnspan=3)
    tk.Button(equip,text='Go',command=lambda:get_equipment(subframea,choice.get())).grid(row=1,column=2)

def get_equipment(frame, mode='Weapons'):
    for widget in frame.winfo_children():
        widget.destroy()
    
    tk.Label(frame,text='What are you looking for?').grid(row=0,column=0)
    
    
        
    combat=tk.StringVar()
    combat_styles=list(mainarmory[mode].keys())
    combat.set(combat_styles[0])
    tk.OptionMenu(frame,combat,*combat_styles).grid(row=0,column=1)
    subframeb=tk.Frame(frame)
    subframeb.grid(row=2,column=0,columnspan=3)
    tk.Button(frame,text='Go',command=lambda:get_weapons(subframeb,mode,combat.get())).grid(row=0,column=2)

def get_weapons(frame,mode='Weapon',style='Melee'):
    for widget in frame.winfo_children():
        widget.destroy()
    if mode=='Gear':
        tk.Label(frame,text=style+' currently installed:').grid(row=0,column=0)
    if mode=='Armor':
        tk.Label(frame,text=style+' currently installed:\n(Shields are counted as Melee Weapons)').grid(row=0,column=0)
    if mode=='Vehicles':
        tk.Label(frame,text=style+' currently installed:\n(Horses and other living mounts are counted as Gear)').grid(row=0,column=0)
    if mode=='Weapons' and style=='Melee':
        tk.Label(frame,text='Melee weapons currently installed:').grid(row=0,column=0)
    if mode=='Weapons' and style=='Ranged':
        tk.Label(frame,text='Ranged weapons currently installed:').grid(row=0,column=0)
    if mode=='Weapons' and style=='Special':
        tk.Label(frame,text='Special weapons currently installed:').grid(row=0,column=0)
    avail_weapons=list(mainarmory[mode][style].keys())
    weapon_choice=tk.StringVar()
    weapon_choice.set(avail_weapons[0])
    print(avail_weapons)
    tk.OptionMenu(frame,weapon_choice,*avail_weapons).grid(row=0,column=1)
    subframec=tk.Frame(frame)
    subframec.grid(row=2,column=0, columnspan=3)
    tk.Button(frame,text='View',command=lambda:get_weapon_info(subframec,mode,style,weapon_choice.get())).grid(row=0,column=2)

def get_weapon_info (frame,mode='Weapons',style='Melee',item='Axe, Hand'):
    for widget in frame.winfo_children():
        widget.destroy()
    data=mainarmory[mode][style][item]
    keys=list(data.keys())
    string=data['display']
    tk.Label(frame,text=string).grid(row=2,column=0,columnspan=3)
    if mode=='Weapons':
        tk.Button(frame,text='Add to inventory',command=lambda:install({item:data},mainplayer['Gear']['Weapons'][style])).grid(row=2,column=4)
    if mode=='Gear':
        tk.Button(frame,text='Add to inventory',command=lambda:install({item:data},mainplayer['Gear']['Inventory'])).grid(row=2,column=4)
    if mode=='Armor':
        tk.Button(frame,text='Add to inventory',command=lambda:install({item:data},mainplayer['Gear']['Armor'])).grid(row=2,column=4)
    if mode=='Vehicles':
        tk.Button(frame,text='Add to inventory',command=lambda:install({item:data},mainplayer['Vehicles'])).grid(row=2,column=4)

def fullrest():
    incap('w',0,buttons)
    incap('f',0,buttons)
    mainstats()

def stat_checker(player):
    #armor value update
    
    armor_key=list(player['Gear']['Armor'])
    equipped_armor=[[0,'head'],[0,'face'],[0,'torso'],[0,'legs'],[0,'feet']]
    armor_is_heavy=False
    if armor_key!=0:
        for i in range(len(armor_key)):
            if player['Gear']['Armor'][armor_key[i]]['head'] and player['Gear']['Armor'][armor_key[i]]['equipped']:
                equipped_armor[0][0]+=int(player['Gear']['Armor'][armor_key[i]]['armor'])
            if player['Gear']['Armor'][armor_key[i]]['face'] and player['Gear']['Armor'][armor_key[i]]['equipped']:
                equipped_armor[1][0]+=int(player['Gear']['Armor'][armor_key[i]]['armor'])
            if player['Gear']['Armor'][armor_key[i]]['torso'] and player['Gear']['Armor'][armor_key[i]]['equipped']:
                equipped_armor[2][0]+=int(player['Gear']['Armor'][armor_key[i]]['armor'])
            if player['Gear']['Armor'][armor_key[i]]['legs'] and player['Gear']['Armor'][armor_key[i]]['equipped']:
                equipped_armor[3][0]+=int(player['Gear']['Armor'][armor_key[i]]['armor'])
            if player['Gear']['Armor'][armor_key[i]]['feet'] and player['Gear']['Armor'][armor_key[i]]['equipped']:
                equipped_armor[4][0]+=int(player['Gear']['Armor'][armor_key[i]]['armor'])
            #armor_is_heavy=player['Gear']['Armor'][armor_key[i]]['heavy']
    #need code here to check for natural armor
    natural_armor=[0]*5
    
    total_armor=equipped_armor
    for i in range(len(natural_armor)):
        total_armor[i][0]+=natural_armor[i]
    player['stats']['Armor']=total_armor

def equipunequip(player,equipment_type,item):
    player['Gear'][equipment_type][item]['equipped']=not player['Gear'][equipment_type][item]['equipped']
    if player['Gear'][equipment_type][item]['equipped']:
        return 'Unequip'
    else:
        return 'Equip'
    

global main
main=tk.Tk()
main.title("SWADE CHaracter Sheet v5")

main.minsize(800,600)

main.bind("<F11>",lambda event: main.attributes("-fullscreen", not main.attributes("-fullscreen")))
main.bind("<Escape>",lambda event: main.attributes("-fullscreen",False))

menubar=tk.Menu()

photo=tk.PhotoImage(file='SW_LOGO_FP_2018-300x200-1.gif')

licenseframe=tk.Frame(main)
licenseframe.grid()
canvas=tk.Canvas(licenseframe,width=300,height=200)
canvas.grid()
canvas.create_image((150,100),image=photo)
tk.Label(licenseframe,text="This game references the Savage Worlds game system, available from Pinnacle Entertainment Group at \nwww.peginc.com. Savage Worlds and all associated logos and trademarks are \ncopyrights of Pinnacle Entertainment Group. Used with permission. \nPinnacle makes no representation or warranty as to the quality, viability, or suitability \nfor purpose of this product.").grid()


filemenu=tk.Menu(menubar)
filemenu.add_command(label="New",command=lambda:newcharstats())
filemenu.add_command(label="Save",command=lambda:save(mainplayer))
filemenu.add_command(label="Load",command=lambda:loadsaves())
filemenu.add_command(label="Save as ...",command=lambda:saveas(mainplayer))
menubar.add_cascade(label='File',menu=filemenu)

editmenu=tk.Menu(menubar)
editmenu.add_command(label="Attributes", command=lambda:attribute_update())
editmenu.add_command(label='Background', command=lambda:print('farts'))
editmenu.add_command(label='Inventory',command=lambda:print('boogers'))
editmenu.add_command(label='More stuff',command=lambda:print('asdfasdf'))
editmenu.add_command(label="Full Rest",command=lambda:fullrest())
menubar.add_cascade(label="Edit Character",menu=editmenu)

csmenu=tk.Menu(menubar)
csmenu.add_command(label="Stats",command=lambda:mainstats())
csmenu.add_command(label="Combat",command=lambda:combat())
menubar.add_cascade(label="Character Sheet",menu=csmenu)

codex=tk.Menu(menubar)
codex.add_command(label="Combat effects",command=lambda:print("I explain combat effects"))
codex.add_command(label='Equipment',command=lambda:equipment_tab())
codex.add_command(label='New Equipment',command=lambda:newgear())
codex.add_command(label="Help",command=lambda:print("I explain how to use the app"))
menubar.add_cascade(label="Codex",menu=codex)

main.config(menu=menubar)
main.mainloop()
