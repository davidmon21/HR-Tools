import os
import random
import argparse
import pysword_repo
import configparser
from datetime import datetime
import pydoc
import re

try:
    from pysword.modules import SwordModules
    from pysword.bible import SwordBible
    import pysword 
except:
    print("You are missing pysword, to install: pip install [--user] pysword\nOr check your repository")
    exit(1)



class Heathen():

    now = datetime.now()
    biblepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),".bibles")
    heathennotes = os.path.join(biblepath,".heathennotes")
    tempfiles =  os.path.join(biblepath,".tempfiles")
    version = "drc.conf-drc"
    thebiblepath = ""
    bible = None
    heathennotes_conf = configparser.ConfigParser()
    heathenconf = configparser.ConfigParser()
    heathenconf_path = os.path.dirname(os.path.realpath(__file__)),'.heathen'
    pyrepoz = None
    shortversion = 'drc'
    
    def __init__(self, configuration,handlerfunction):
        self.heathenconf_path = configuration
        if os.path.exists(self.heathenconf_path):
            self.heathenconf.read(self.heathenconf_path)
            self.thebiblepath = self.heathenconf['MAIN']['swordpath']
            self.pyrepoz = pysword_repo.PyswordRepo(swrdpath=self.biblepath,repoconf=".heathenrepo")
        else:
            self.heathen_first_run(handlerfunction)
        if len(self.version.split('-')) > 1:
            self.shortversion = self.version.split('-')[1]
        self.heathennotes = os.path.join(self.biblepath,".heathennotes")
    
    def open_bible(self):
        checkeroo = self.thebiblepath.rsplit('.',1)
        if len(checkeroo) > 1:
            if checkeroo[1] == "zip":
                modules = SwordModules(self.thebiblepath)
                modules.parse_modules()
                self.bible = modules.get_bible_from_module(self.shortversion.upper())
            else:
                self.bible = SwordBible(self.thebiblepath)
        else:
            self.bible = SwordBible(self.thebiblepath)
    
    def add_verse_numbers(self, versenumbers, verselines):
        verses = versenumbers['verses']
        chapter = versenumbers['chapter']
        book = versenumbers['book']
        returnlist = []
        lines = zip(verses,verselines)
        for number,verse in lines: returnlist.append([{'verse':number, 'chapter':chapter,'book':book},"\n{}: ".format(number)+verse])
        return returnlist
        
    def grabnotes_to_verses(self,verses,chapter,book):
        if os.path.exists(self.heathennotes):
            self.heathennotes_conf.read(self.heathennotes)
        else:
            return [None,"no notes"]
        returndict = {}
        for verse in verses:
            section = self.shortversion+"-"+book+"-"+str(chapter)+"_"+str(verse)
            if section in self.heathennotes_conf.keys():
                returnnotes=[]
                for notes in self.heathennotes_conf[section].keys():
                    returnnotes.append(self.heathennotes_conf[section][notes])
                returndict[section]=returnnotes
        
        return returndict
                    

                
    
    def compile_verse_text(self, bookline,verseline, versenumbers=True, versenotes=False):
        self.grab_module()
        outputer = []    
        books = bookline.split(',')
        topparts = verseline.split(',')
        returndictlist = []
        string=""
        if len(books) == 1 and len(topparts) != 1:
            books = books*len(topparts)
        if len(topparts) == 1 and len(books) != 1:
            topparts = topparts*len(books)
        thedict = zip(books,topparts)
        for book,part in thedict:
            parts = part.split('-')
            
            chapter = parts[0]
            
            if ':' in str(parts[0]):
                parts2 = parts[0].split(':')
                versespieces = part.split(':')[1]
                chapter = int(parts2[0])
                parts = versespieces.split('-')
                if len(parts) > 1:
                    verse2 = parts[1]
                    verse1 = int(parts[0])
                    if verse2 == "+":
                        verse2 = self.bible.get_structure().find_book(book)[1].chapter_lengths[chapter-1]
                    verse2 = int(verse2)
                    outputer.append([chapter, list(range(verse1,verse2+1))])
                    
                else:
                    outputer.append([chapter, [versespieces]])
                    
                
            else:
                if parts[0] == '+':
                    for chapter in range(1,self.bible.get_structure().find_book(book)[1].num_chapters+1):
                        verse2 = list(range(1,int(self.bible.get_structure().find_book(book)[1].chapter_lengths[chapter-1])+1))
                        outputer.append([int(chapter), verse2])
                else:
                    verse2 = list(range(1,int(self.bible.get_structure().find_book(book)[1].chapter_lengths[chapter-1])+1))
                    outputer.append([int(chapter), verse2])
            returnnotes = []
            for part in outputer:
                chapter=part[0]
                verses=part[1]
                
                if verses[0] == '+':
                    verses = list(range(1,self.bible.get_structure().find_book(book)[1].chapter_lengths[chapter-1]))
            #try:
                verses[0] = int(verses[0])
                results = self.bible.get(books=[book], chapters=[int(chapter)], verses=verses).splitlines()
                returnresults = list(results)
                if versenumbers:
                    results = self.add_verse_numbers({'verses':verses, 'chapter':chapter, 'book':book}, results)
                if versenotes and os.path.exists(self.heathennotes):
                    notes = self.grabnotes_to_verses(verses, chapter, book)
                    returnnotes = dict(notes)
                else: 
                    returnnotes = {}
                    notes = {}
                string+="\n\n{}, {}, {}\n\n".format(self.shortversion.upper(), book.title(), chapter)
                while len(results)!= 0:
                    currentresult = results.pop(0)
                    currentverse = currentresult[0]['verse']
                    string+=currentresult[1]
                    if versenotes:
                        section = "{}-{}-{}_{}".format(self.shortversion.lower(),book.lower(),chapter,currentverse)
                        if section in notes:
                            for note in notes[section]:
                                string+="\n"+(note)
                            
                    returndictlist.append({'chapter':chapter, 'verses':verses, 'book':book, 'plain':returnresults, 'notes':returnnotes, 'string':string })
                #except:
                 #   string+="\n\nTried to grab verses that didnt exist, or error in name:{} {}:{}-{}\n\n".format(book,chapter,verses[0],verses[-1])
                  #  returndictlist.append({'chapter':None, 'verse':None, 'book':None, 'plain':None, 'notes':returnnotes, 'string':None })
                
            outputer = []
        returndictlist.append(string)
        return returndictlist
    
    def grab_module(self):
        v1 = self.version.lower()
        modules = self.pyrepoz.find_module(v1, installed=True)
        if len(modules) == 1:
            installfiles = modules[0][1]['installed files'].split("## ")
            installfiles.remove("")
            if len(installfiles) == 1:
                self.thebiblepath = installfiles[0]
            else:
                self.thebiblepath = os.path.dirname(installfiles[0])
            self.shortversion = modules[0][1]['name'].strip('[]')
        else:
            print("You need a bible for what you are trying to do, maybe install one with -a")
            exit(1)
    
    def add_to_notes(self,bookver_notes):
        if os.path.exists(self.heathennotes):
            self.heathennotes_conf.read(self.heathennotes)
        for bookver_chapter_verse, newkey, note in bookver_notes:
            if bookver_chapter_verse not in self.heathennotes_conf.keys():
                self.heathennotes_conf[bookver_chapter_verse] = {}
            elif newkey in self.heathennotes_conf[bookver_chapter_verse] and not note.isspace():
                lastnote = self.heathennotes_conf[bookver_chapter_verse][newkey]
                note=note+" "+lastnote
                del self.heathennotes_conf[bookver_chapter_verse][newkey]
            self.heathennotes_conf[bookver_chapter_verse][newkey] = note
        with open(self.heathennotes, 'w') as conf:
            self.heathennotes_conf.write(conf)
    
    def compare_verse_lines(self,compare,results,linenumbers=True,oldnotes=False):
        try:
            compare.remove("")
        except: pass
        try:
            compare.remove("\n")
        except: pass
        try:
            compare.remove(" ")
        except: pass
        
        result = results.pop(0)
        verse = result['verses'][0]
        chapter = result['chapter']
        book = result['book']
        lowerversion = self.shortversion.lower()
        bookver_chapter_verse = "{}-{}-{}_{}".format(lowerversion,book,chapter,verse)
        date_time = self.now.strftime("%d-%m-%Y,%H-%M-%S")
        notes = result['notes']
        newnotes=[]
        newkeys=[]
        thesections=[]
        newnote=""
        
        change_over = False
        while len(compare) != 0:
            go_on = True
            line = compare.pop(0)
            if change_over:
                bookver_chapter_verse = "{}-{}-{}_{}".format(lowerversion, book, chapter, verse)
                change_over = False
                notes = result['notes']
            
            if linenumbers:
                if re.match('[0-9]{1,3}:',line):
                    line = line.split(':',1)[1]
            
            line = line.strip().rstrip()
            if len(result['plain']) != 0:
                if result['plain'][0] == line:
                    result['plain'].pop(0)
                    if len(result['verses']) != 0:
                        verse = result['verses'].pop(0)
                    go_on = False
                    change_over = True
            
            elif len(results) != 0:
                result = results.pop(0)
                print(result)
                if len(result['verses']) != 0:
                    verse = result['verses'][0]
                chapter = result['chapter']
                book = result['book']
                
            
            if line.lower() == lowerversion+", "+book+", "+str(chapter):
                go_on =  False
                change_over = False
            
            if oldnotes and go_on != False:
                if bookver_chapter_verse in notes:
                    if len(notes[bookver_chapter_verse]) != 0:
                        if line in notes[bookver_chapter_verse]:
                            notes[bookver_chapter_verse].remove(line)
                            go_on = False
                    change_over=False
            
            if go_on:
                change_over = False
                if not line.strip().rstrip().isspace() and (line != ""):
                    newnotes.append(line.strip().rstrip())
                    thesections.append(bookver_chapter_verse)
                
    
        newkeys = [date_time]*len(newnotes)
        return zip(thesections, newkeys, newnotes)
    
    def grab_and_open(self):
        try:
            self.grab_module()
            self.open_bible()
        except:
            response = input("The bible version you are looking for, you do not have.\nWould you like to download?(y/n): ")
            if 'y' in response:
                version = self.install_the_module()
                self.grab_module()
                self.open_bible()
            else:
                exit(1)
    
    def heathen_first_run(self,handlingfunction):
        print("Welcome to heathen!")
        answer = handlingfunction("Do you have an existing sword path?(y/n)").lower()
        
        if 'y' in answer:
            answer = handlingfunction("Enter your sword directory path: ")
            self.biblepath = answer.strip().rstrip()
            
            
            self.pyrepoz = pysword_repo.PyswordRepo(swrdpath=self.biblepath,repoconf=".heathenrepo")
            
            answer = handlingfunction("Would you like heathen to manage your repo?(y/n): ")
            if 'y' in answer:
                installedmodules = self.pyrepoz.bootstrap_ibm()
                self.repo_management = 'y'
            elif 'n' in answer:
                installedmodules = self.pyrepoz.find_installed_modules()
                repo_management = 'n'
            installedmodules = self.pyrepoz.list_installed_modules()
            installedmodslen = range(0,len(installedmodules))
            for x in installedmodslen:
                print(str(x+1)+": "+installedmodules[x])
            answer = handlingfunction("Select module as default version: ")
            if answer.isdigit and (int(answer)-1) in installedmodslen:
                version = self.installedmodules[int(answer)-1][0]
            self.heathenconf['MAIN'] = {'swordpath':self.biblepath, 'version':self.shortversion, 'repo management':self.repo_management }
            
        elif 'n' in answer:
            self.biblepath = os.path.join(os.path.dirname(os.path.realpath(self.heathenconf_path)),".bibles")
            if not os.path.exists(self.biblepath):
                os.makedirs(self.biblepath)
            self.pyrepoz = pysword_repo.PyswordRepo(swrdpath=self.biblepath,repoconf=".heathenrepo")
            self.pyrepoz.initiate_repo()
            self.pyrepoz.update_repo_list()
            self.pyrepoz.download_repos()
            self.pyrepoz.install_module('drc.conf-drc')
            self.version = 'drc.conf-drc'
            self.repo_management = 'y'
            self.heathenconf['MAIN'] = { 'swordpath':self.biblepath, 'version':self.version, 'repo management':'y' }
            
        with open(os.path.join(self.heathenconf_path),'w') as conf2:
            self.heathenconf.write(conf2)
