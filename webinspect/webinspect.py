"""
inspect any python object with a slick web interface.

Usage:
    import webinspect
    webinspect.launch("any object you want") #launches a web browser

"""

__version__ = '0.3.0'

import webbrowser
import tempfile
import time
import datetime
import copy

delicate=False

blacklist=[] # append to this list to prevent execution of some functions
blacklist.append('destroy')

def launch(thing,title=False):
    """analyze a thing, create a nice HTML document, and launch it."""
    html=htmlFromThing(thing,title=title)
    if not html:
        print("no HTML was generated.")
        return
    fname="%s/%s.html"%(tempfile.gettempdir(),str(time.time()))
    with open(fname,'w') as f:
        f.write(html)
    webbrowser.open(fname)

def thingToString(thing,MAXSTRINGLENGTH=10000):
    if type(thing)==dict:
        s="DICT (%d):\n\n"%len(thing.keys())
        for key in sorted(thing.keys()):
            s+="%s : %s\n"%(key,thing[key])
    elif type(thing)==list:
        s="LIST (%d):\n\n"%len(thing)
        for i,val in enumerate(thing):
            thing[i]=str(val)
        s+=", ".join(thing)
    elif type(thing)==tuple:
        thing=list(thing)
        s="tuple (%d):\n\n"%len(thing)
        for i,val in enumerate(thing):
            thing[i]=str(val)
        s+=", ".join(thing)
    else:
        s=str(thing)
    if len(s)>MAXSTRINGLENGTH:
        s=s[:MAXSTRINGLENGTH]+" ..."
    return s

def analyzeThing(originalThing2):
    """analyze an object and all its attirbutes. Returns a dictionary."""
    originalThing = copy.copy(originalThing2)
    things={}
    for name in sorted(dir(originalThing)):
        print("analyzing",name)
        thing = copy.copy(originalThing)
        try:
            if delicate:
                print(1/0)
            item=getattr(thing,name)
        except:
            continue
        itemType=type(item).__name__
        itemStr=thingToString(item)
        itemEval=""
        if "method" in itemStr:
            try:
                if delicate or name in blacklist:
                    print(1/0)
                itemEval=thingToString(getattr(thing,name)())
                print("executing %s()"%name)
            except:
                itemEval="DID NOT EVALUATE"

        #print("[%s] (%s) %s {%s}"%(name,itemType,itemStr,itemEval))
        things[name]=[itemType,itemStr,itemEval]
    return things

def websafe(s):
    """return a string with HTML-safe text"""
    s=s.replace("<","&lt;").replace(">","&gt;")
    s=s.replace(r'\x',r' \x')
    s=s.replace("\n","<br>")
    return s

def htmlFromThing(thing,title):
    """create pretty formatted HTML from a things dictionary."""
    try:
        thing2 = copy.copy(thing)
    except:
        print("crashed copying the thing! I can't document it.")
        return False
    stuff=analyzeThing(thing2)
    names2=list(stuff.keys())
    for i,name in enumerate(names2):
        if name.startswith("_"):
            names2[i]="zzzzzzzzzz"+name

    html="""<html><head><style>
    body {font-family: courier, monospace;}
    .name {font-weight: bold;}
    .type {font-style: italic; font-family: serif; color: #AAA;}
    .desc {}
    .itemEval {background-color: #DDFFDD;}
    .itemEvalFail {}
    table {font-size: .8em;
           margin-top: 20px;
           border-collapse: collapse;}
    tr {border: 1px solid #CCC; vertical-align: text-top;}
    td {padding: 2px 10px 2px 10px;}
    .credits {text-align: center;
              opacity: 0.5;
              margin-top: 50px;
              font-size: .8em;
              font-family: sans-serif;}
    </style></head><body>"""

    if title:
        html+='<span style="color: #CCC;">title: </span>%s<br>'%title
    textTitle=""
    textType=""
    try:
        textTitle=str(thing)
        textType=type(thing).__name__
    except:
        pass
    html+='<span style="color: #CCC;">value: </span>%s<br>'%textTitle
    html+='<span style="color: #CCC;">&nbsp;type: </span>%s<br>'%textType
    html+='<table cellpadding=3 align="center">'
    html+='<tr style="background-color: #000; color: #FFF; font-weight: bold;">'
    html+='<td>property</td><td>type</td><td>value</td>'
    html+='<td>evaluated (without arguments)</td></tr>'
    for name in sorted(names2):
        if name.startswith("zzzzzzzzzz"):
            name=name[10:]
        itemName=str(name)
        itemType=websafe(stuff[name][0])
        itemStr=websafe(stuff[name][1])
        itemEval=websafe(stuff[name][2])
        color="DDDDFF"
        color2=""
        if "method" in itemType:
            itemName+="()"
            color="FFDDDD"
        if itemName.startswith("_"):
            color="EEEEEE"
        if itemStr.startswith("&lt;") and not ", " in itemStr:
            itemStr="""<span style="color: #CCC; font-family: serif;
                font-style: italic;">%s</span>"""%itemStr
        else:
            color2="DDFFDD"
            if itemEval=="":
                itemEval="FAILED TO EVALUATE"
        html+='<tr>'
        html+='<td class="name" style="background-color: #%s;">%s</td>'%(color,itemName)
        html+='<td class="type">%s</td>'%(itemType)
        html+='<td class="itemStr" style="background-color: #%s;">%s</td>'%(color2,itemStr)
        if itemEval=="FAILED TO EVALUATE":
            html+='<td class="itemEvalFail"></td>'
        else:
            html+='<td class="itemEval">%s</td>'%(itemEval)
        html+='</tr>'

    dt=datetime.datetime.now()
    html+="""</table><p class="credits">
    page automatically generated by
    <a href="https://pypi.python.org/pypi/webinspect/">webinspect</a>
    (version %s) %s</p>
    </body></html>"""%(__version__,dt.strftime("at %I:%M %p on %B %d, %Y"))

    return html

class TESTCLASS:
    """test class to demonstrate how inspection works."""
    def __init__(self):
        self.x=123
        self.s="scott"
        self.demoList=[1,8,3,5,6]
        self.demoTup=(1,8,3,5,6)
        self.demoDict={"dog":5,"cat":"awful","gecko":False}

    def func(self):
        self.f='asdf'

    def __repr__(self):
        return repr(["array","of","things",1234])

if __name__=="__main__":
    launch(TESTCLASS(), "here is a demo class")