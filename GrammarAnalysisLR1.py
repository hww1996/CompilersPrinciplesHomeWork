__author__ = 'Administrator'
#encoding:utf-8
import copy,re
from collections import deque
import wx,wx.html
import pdb
st='''
S->E
E->E+T
E->T
T->T*F
T->F
F->(E)
F->i
'''

sst='''
S->E
E->BB
B->aB
B->b
'''

ssssst='''
A->E
E->TG
G->+TG
G->@TG
G->ε
T->FS
S->*FS
S->/FS
S->ε
F->(E)
F->i
'''

ssss='''
S->X
X->ABC
A->DE
B->FG
C->HI
D->d
D->ε
E->e
E->ε
F->f
F->ε
G->g
G->ε
H->h
H->ε
I->i
I->ε
'''

kkkkk='''
S->E
E->AaAb
E->BbBa
A->ε
B->ε
'''

ttttttttttt='''
S->A
A->CD
C->c
D->d
C->ε
D->ε
'''

class GrammarAnalysis():
    def __init__(self,s):
        self.__s=s  #文法
        self.__GrammarTable={}
        self.__GrammarList=[]
        self.__FirstSet={}
        self.__Status=[]
        self.__Action={}
        self.__Goto={}

    def __getGrammar(self):
        GrammarList=re.split("\n|\r\n",self.__s)
        count=0
        for grammar in GrammarList:
            if len(grammar)==0:
                continue
            SplitList=grammar.split("->")
            if self.__GrammarTable.get(SplitList[0])==None:
                self.__GrammarTable[SplitList[0]]=[]
            self.__GrammarTable[SplitList[0]].append([SplitList[1],False,count])
            count+=1
            self.__GrammarList.append(copy.deepcopy(SplitList))
#############################################################################获取变量的First集
    '''def __firstSet(self,AnsList,key):
        for i in range(len(self.__GrammarTable[key])):
            if not self.__GrammarTable[key][i][1]:
                self.__GrammarTable[key][i][1]=True
                #k=self.__GrammarTable[key][i][0]
                if self.__GrammarTable.get(self.__GrammarTable[key][i][0][0])!=None:
                    self.__firstSet(AnsList,self.__GrammarTable[key][i][0][0])
                else:
                    AnsList.append(self.__GrammarTable[key][i][0][0])'''


    def __firstSet(self,Key):
        Ans=[]
        if self.__GrammarTable.get(Key)==None:
            Ans.append(Key)
            return Ans
        val=self.__GrammarTable.get(Key)
        for i in range(len(val)):
            if not self.__GrammarTable[Key][i][1]:
                self.__GrammarTable[Key][i][1]=True
                if self.__GrammarTable.get(val[i][0][0])==None:
                    if not(val[i][0][0] in Ans):
                        Ans.append(val[i][0][0])
                else:
                    CountNone=0
                    for j in range(len(val[i][0])):
                        NextRound=self.__firstSet(val[i][0][j])
                        CanBreak=True
                        for next in NextRound:
                            if next=="ε":
                                CanBreak=False
                                CountNone+=1
                            elif not(next in Ans):
                                Ans.append(next)
                        if CanBreak:
                            break

                    if CountNone==len(val[i][0]):
                        if not("ε" in Ans):
                            Ans.append("ε")
        return Ans



    def __getFirstSet(self):
        self.__getGrammar()
        for key in self.__GrammarTable:
            AnsList=self.__firstSet(key)
            self.__FirstSet[key]=copy.deepcopy(AnsList)
            for k in self.__GrammarTable:
                for i in range(len(self.__GrammarTable[k])):
                    self.__GrammarTable[k][i][1]=False
####################################################################################获取table
    def __Expand(self,Given):
        for s in Given:
            t=s.split("-")
            type=int(t[0])
            position=int(t[1])
            n=len(self.__GrammarList[type][1])

            if position==n:
                pass

            elif position==n-1:
                key=self.__GrammarList[type][1][position]
                if self.__GrammarTable.get(key)==None:
                    continue
                if self.__GrammarTable.get(key)!=None:
                    for K in self.__GrammarTable[key]:
                        result=str(K[2])+"-0-"+t[2]
                        if not(result in Given):
                            Given.append(result)

            else:
                key=self.__GrammarList[type][1][position]
                if self.__GrammarTable.get(key)==None:
                    continue
                #Follow=self.__GrammarList[type][1][position+1]
                #FollowChars=[]
                FollowString=self.__GrammarList[type][1][position+1:]+t[2]
                '''
                if self.__FirstSet.get(Follow)!=None:
                    FollowChars=self.__FirstSet.get(Follow)
                else:
                    FollowChars.append(Follow)
                if self.__GrammarTable.get(key)!=None:
                    for K in self.__GrammarTable[key]:
                        for c in FollowChars:
                            result=str(K[2])+"-0-"+c
                            if result not in Given:
                                Given.append(result)
                                '''
                FollowSet=[]
                for FS in range(len(FollowString)):
                    FollowTemp=self.__firstSet(FollowString[FS])
                    findEmpty=False
                    for FT in FollowTemp:
                        if FT!="ε":
                            if not(FT in FollowSet):
                                FollowSet.append(FT)
                        else:
                            findEmpty=True

                    for k in self.__GrammarTable:
                        for i in range(len(self.__GrammarTable[k])):
                            self.__GrammarTable[k][i][1]=False

                    if not findEmpty:
                        break
                for K in self.__GrammarTable[key]:
                    for c in FollowSet:
                        if len(c)==0:
                            print(FollowSet)
                        result=str(K[2])+"-0-"+c
                        if not (result in Given):
                            Given.append(result)




    def __CheckBelong(self,Item,CheckResult):
        count=0
        for status in self.__Status:
            AllIn=True
            if len(Item)==len(status):
                for i in Item:
                    if not (i in status):
                        AllIn=False
                        break
                if AllIn:
                    CheckResult[0]=count
                    break
            count+=1

    def getTable(self):
        self.__getFirstSet()
        NowItem=["0-0-#"]
        self.__Expand(NowItem)
        ItemQueue=deque()
        ItemQueue.append(copy.deepcopy(NowItem))
        self.__Status.append(copy.deepcopy(NowItem))
        self.__Action[str(0)]={}
        self.__Goto[str(0)]={}
        NumberCount=0

        while len(ItemQueue)!=0:
            NowItem=ItemQueue.popleft()
            NowPointer={}
            NowPointer["keys"]=[]
            if self.__Action.get(str(NumberCount))==None:
                self.__Action[str(NumberCount)]={}
            if self.__Goto.get(str(NumberCount))==None:
                self.__Goto[str(NumberCount)]={}
            for item in NowItem:
                t=item.split("-")
                type=int(t[0])
                position=int(t[1])
                n=len(self.__GrammarList[type][1])
                child=self.__GrammarList[type][1]
                if child=="ε":
                    self.__Action[str(NumberCount)][t[2]]="ε"+t[0]
                elif position==n:
                    self.__Action[str(NumberCount)][t[2]]="r"+t[0]
                else:
                    NowChar=self.__GrammarList[type][1][position]
                    if NowPointer.get(NowChar)==None:
                        NowPointer[NowChar]=[]
                    NowPointer[NowChar].append(t[0]+"-"+str(position+1)+"-"+t[2])
                    if not (NowChar in NowPointer["keys"]):
                        NowPointer["keys"].append(NowChar)


            for npKey in NowPointer["keys"]:
                CreatedItem=copy.deepcopy(NowPointer[npKey])
                self.__Expand(CreatedItem)
                CheckResult=[-1]
                self.__CheckBelong(CreatedItem,CheckResult)
                NeedGotoStatus=-1
                if CheckResult[0]==-1:
                    self.__Status.append(copy.deepcopy(CreatedItem))
                    ItemQueue.append(copy.deepcopy(CreatedItem))
                    NeedGotoStatus=len(self.__Status)-1
                else:
                    NeedGotoStatus=CheckResult[0]
                if self.__GrammarTable.get(npKey)!=None:
                    self.__Goto[str(NumberCount)][npKey]=str(NeedGotoStatus)
                else:
                    self.__Action[str(NumberCount)][npKey]="s"+str(NeedGotoStatus)

            NumberCount+=1
        self.__Action[str(1)]["#"]="acc"
        Table={}
        Table["Action"]=self.__Action
        Table["Goto"]=self.__Goto
        Table["GrammarList"]=self.__GrammarList
        return Table

class MyMenu(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        panel=wx.Panel(self,1,style=wx.EXPAND|wx.VSCROLL)
        self.Grammar=wx.TextCtrl(panel,2,"S->E\nE->BB\nB->aB\nB->b",size=(640,150),style=wx.VSCROLL|wx.TE_MULTILINE)
        self.Sentence=wx.TextCtrl(panel,3,"aabab",size=(640,30))
        self.Result=wx.html.HtmlWindow(panel,4,style=wx.html.HW_SCROLLBAR_AUTO,size=(1280,720))
        self.Table=wx.html.HtmlWindow(panel,5,style=wx.html.HW_SCROLLBAR_AUTO,size=(1280,360))
        btn=wx.Button(panel,5,"开始检查",style=wx.TE_LEFT)
        self.Bind(wx.EVT_BUTTON,self.__OnAnalysis,id=5)
        box=wx.BoxSizer(orient=wx.VERTICAL)
        box.Add(wx.StaticText(panel,label="语法"),flag=wx.EXPAND)
        box.Add(self.Grammar,border=5,flag=wx.EXPAND)
        box.Add(wx.StaticText(panel,label="句子"),flag=wx.EXPAND)
        box.Add(self.Sentence,border=5,flag=wx.EXPAND)
        box.Add(btn,border=5,flag=wx.EXPAND)
        box.Add(wx.StaticText(panel,label="分析表"),flag=wx.EXPAND)
        box.Add(self.Table,border=5,flag=wx.EXPAND)
        box.Add(wx.StaticText(panel,label="结果"),flag=wx.EXPAND)
        box.Add(self.Result,border=5,flag=wx.EXPAND)
        panel.SetSizer(box)

    def __OnAnalysis(self,event):
        self.Result.SetPage("<html><body><p>请稍后</p></body></html>")
        g=self.Grammar.GetValue()
        Input=self.Sentence.GetValue()
        Table=GrammarAnalysis(g).getTable()
        Action=Table["Action"]
        Goto=Table["Goto"]
        self.__ShowTable(Action,Goto)
        GrammarList=Table["GrammarList"]
        Status=["0"]
        Sign=["#"]
        InputString=[Input[i] for i in range(len(Input))]
        InputString.append("#")
        InputString.reverse()
        ans="<html><body><table border='1'><tr><th>状态</th><th>符号</th><th>输入串</th></tr>"
        isError=False
        while True:
            ans=ans+"<tr><td>"+str(Status)+"</td><td>"+str(Sign)+"</td><td>"+str(InputString)+" </td></tr>"
            StatusKey=Status.pop()
            InputKey=InputString.pop()
            if Action[StatusKey].get(InputKey)!=None:
                NowAction=Action[StatusKey].get(InputKey)
                NeedDo=NowAction[0]
                ActionNumber=NowAction[1:]
                if NowAction=="acc":
                    break
                elif NeedDo=="ε":
                    father=GrammarList[int(ActionNumber)][0]
                    InputString.append(InputKey)
                    if Goto[StatusKey].get(father)!=None:
                        gotoStatus=Goto[StatusKey].get(father)
                        Sign.append(father)
                        Status.append(StatusKey)
                        Status.append(gotoStatus)
                    else:
                        isError=True
                        break
                elif NeedDo=="s":
                    Status.append(StatusKey)
                    Status.append(ActionNumber)
                    Sign.append(InputKey)
                elif NeedDo=="r":
                    Status.append(StatusKey)
                    InputString.append(InputKey)
                    position=int(ActionNumber)
                    son=GrammarList[position][1]
                    father=GrammarList[position][0]
                    NeedPopSize=len(son)
                    while NeedPopSize>0:
                        Status.pop()
                        Sign.pop()
                        NeedPopSize-=1
                    NowStatus=Status.pop()
                    if Goto[NowStatus].get(father)!=None:
                        gotoStatus=Goto[NowStatus].get(father)
                        Sign.append(father)
                        Status.append(NowStatus)
                        Status.append(gotoStatus)
                    else:
                        isError=True
                        break
            else:
                isError=True
                break
        if isError:
            ans="<html><body><p>输入出现错误</p></body></html>"
        else:
            ans=ans+"</table><p>成功acc</p></body></html>"
        self.Result.SetPage(ans)

    def __ShowTable(self,Action,Goto):
        CSet=[]
        SymbolSet=[]
        n=len(Action.keys())
        #print(n)
        #print(Action)
        #print(Goto)
        CharacterSet=[str(i) for i in range(n)]
        for i in CharacterSet:
            if Action.get(i)!=None:
                for j in Action[i]:
                    if not(j in SymbolSet):
                        SymbolSet.append(j)
            if Goto.get(i)!=None:
                for j in Goto[i]:
                    if not(j in CSet):
                        CSet.append(j)
        ans="<html><body><table border='1'><tr><th></th>"
        for i in SymbolSet:
            ans=ans+"<th>"+i+"</th>"
        ans+="</tr><th>&nbsp;&nbsp;&nbsp;&nbsp;</th>"
        for i in CSet:
            ans=ans+"<th>"+i+"</th>"
        ans+="</tr>"
        for character in CharacterSet:
            #ans=ans+"<tr><td>"+character+"</td>"
            t="<tr><td>"+character+"</td>"
            Symbol=[]
            for i in Action[character]:
                for j in range(len(SymbolSet)):
                    if i==SymbolSet[j]:
                        Symbol.append([i,j])
            count=0
            for i in range(len(SymbolSet)):
                if count<len(Symbol) and i==Symbol[count][1]:
                    #ans=ans+"<td>"+character+"->"+str(TableSet[character][Symbol[count][0]])+"</td>"
                    if Action[character][Symbol[count][0]][0]=="ε":
                        t=t+"<td>"+"r"+Action[character][Symbol[count][0]][1:]+"</td>"
                    else:
                        t=t+"<td>"+Action[character][Symbol[count][0]]+"</td>"
                    #t=t+"<td>"+character+"->"+str(Action[character][Symbol[count][0]])+"</td>"
                    count+=1
                else:
                    #ans=ans+"<td></td>"
                    t=t+"<td></td>"
            t=t+"<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>"
            Symbol1=[]
            for i in Goto[character]:
                for j in range(len(CSet)):
                    if i==CSet[j]:
                        Symbol1.append([i,j])
            count=0
            #print(Symbol1)
            for i in range(len(CSet)):
                if count<len(Symbol1) and i==Symbol1[count][1]:
                    #ans=ans+"<td>"+character+"->"+str(TableSet[character][Symbol[count][0]])+"</td>"
                    t=t+"<td>"+Goto[character][Symbol1[count][0]]+"</td>"
                    count+=1
                else:
                    t=t+"<td></td>"
            t=t+"</tr>"
            ans+=t
        ans=ans+"</table></body></html>"
        self.Table.SetPage(ans)




class MyApp(wx.App):
    def OnInit(self):
        frame = MyMenu(None, -1, 'LR1型分析器')
        frame.SetSize(1280,720)
        frame.Show(True)
        frame.Center()
        return True




app = MyApp(0)
app.MainLoop()

