#encoding:utf-8
__author__ = 'Administrator'
import wx,wx.html
import copy
import re
sen='''
E->TE'
E'->+TE'|ε
T->FT'
T'->*FT'|ε
F->(E)|i
'''
st='''
E->TG
G->+TG|-TG|ε
T->FS
S->*FS|/FS|ε
F->(E)|i
'''

ssss='''
S->ABC
A->DE
B->FG
C->HI
D->d|ε
E->e|ε
F->f|ε
G->g|ε
H->h|ε
I->i|ε
'''

kkkkk='''
S->AaAb|BbBa
A->ε
B->ε
'''

yyyyyy='''
S->A
A->CD
C->c|ε
D->d|ε
'''


class Table():
    def __init__(self,s):
        self.__s=re.split("\\r\\n|\\n",s)
        self.__SplitSet={}
        self.__SplitSet["keys"]=[]
        self.__FirstSet={}
        self.__FollowSet={}


    def __getItSplitly(self,s):
        if len(s)==0:
            return None
        t=s.split("->")
        ans={}
        ans[t[0]]=[]
        t2=t[1].split("|")
        for i in range(len(t2)):
            st=t2[i]
            sta=[]
            MeetLetter=False
            ss=""
            for i in range(len(st)):
                if MeetLetter:
                    if ord(st[i])>=ord('A') and ord(st[i])<=ord('Z'):
                        sta.append(ss)
                        ss=st[i]
                    elif st[i]=='\'':
                        ss+="\'"
                    else:
                        sta.append(ss)
                        ss=st[i]
                        MeetLetter=False
                else:
                    if ord(st[i])>=ord('A') and ord(st[i])<=ord('Z'):
                        if len(ss)>0:
                            sta.append(ss)
                        ss=st[i]
                        MeetLetter=True
                    else:
                        if len(ss)>0:
                            sta.append(ss)
                        ss=st[i]
            if len(ss)>0:
                sta.append(ss)
            ans[t[0]].append([i for i in sta])
        return ans
###################################################################        First集
    '''def __firstSet(self,Key,AnsList):
        if self.__SplitSet.get(Key)==None:
            AnsList.append(Key)
            return
        val=self.__SplitSet.get(Key)
        for i in range(len(val)):
            self.__firstSet(val[i][0],AnsList)'''

    def __firstSet(self,Key):
        Ans=[]
        if self.__SplitSet.get(Key)==None:
            Ans.append(Key)
            return Ans
        val=self.__SplitSet.get(Key)
        for i in range(len(val)):
            if self.__SplitSet.get(val[i][0])==None:
                if not(val[i][0] in Ans):
                    Ans.append(val[i][0])
            else:
                CountNone=0
                for j in range(len(val[i])):
                    NextRound=self.__firstSet(val[i][j])
                    CanBreak=True
                    for next in NextRound:
                        if next=="ε":
                            CanBreak=False
                            CountNone+=1
                        elif not(next in Ans):
                            Ans.append(next)
                    if CanBreak:
                        break

                if CountNone==len(val[i]):
                    if not("ε" in Ans):
                        Ans.append("ε")
        return Ans


    def __getFirstSet(self):
        for i in range(len(self.__s)):
            t=self.__getItSplitly(self.__s[i])
            if t:
                key=list(t.keys())[0]
                self.__SplitSet[key]=t[key]
                self.__SplitSet["keys"].append(key)
        keys=self.__SplitSet["keys"]
        for i in range(len(keys)):
            AnsList=self.__firstSet(keys[i])
            self.__FirstSet[keys[i]]=copy.deepcopy(AnsList)
###########################################################################     Follow集
    def __followSet(self,Target,AnsList,HasChange):
        keys=self.__SplitSet["keys"]
        for i in keys:
            child=self.__SplitSet[i]
            for j in child:
                k=0
                size=len(j)
                while k<size:
                    '''
                    A->αBβ1...βn
                    β1->ε|Expression
                    β2->ε|Expression
                    ...
                    βk->Expression
                    '''
                    if j[k]==Target:
                        next=k+1
                        if next==size:
                        #表示找到target的时候刚好在结尾，这时将key的follow集放到target的follow集
                            if Target!=i:
                                for m in self.__FollowSet[i]:
                                    if not (m in AnsList):
                                        AnsList.append(m)
                                        HasChange[0]=True
                            break


                        else:
                            '''
                            这时target不在表达式的最尾部，看他后面的元素：
                                1.若不为可以推的元素则直接放入follow集
                                2.若为可推的元素则要判断：
                                    a.若其可以为空，则继续判断下一个元素并重复上诉过程，假如一直到最后的一个元素都可以推出空，则将key的follow集给target
                                    b.若不可能为空，则直接将其的first集给target的follow集
                            '''
                            MeetEmpty=True
                            while next<size and MeetEmpty:
                                MeetEmpty=False
                                if self.__FirstSet.get(j[next])==None:
                                    if not (j[next] in AnsList):#防止出现重复
                                        AnsList.append(j[next])
                                        HasChange[0]=True
                                    k=next
                                    break
                                else:
                                    NeedFirstSet=self.__FirstSet.get(j[next])
                                    for m in NeedFirstSet:
                                        if m!='ε':
                                            if not (m in AnsList):#防止出现重复
                                                AnsList.append(m)
                                                HasChange[0]=True
                                        else:
                                            MeetEmpty=True
                                next+=1


                            if next==size and MeetEmpty:
                                if Target!=i:
                                    for m in self.__FollowSet[i]:
                                        if not (m in AnsList):#防止出现重复
                                            AnsList.append(m)
                                            HasChange[0]=True
                                k=size
                                break
                    k+=1
    def __getFollowSet(self):
        self.__getFirstSet()
        keys=self.__SplitSet["keys"]
        First=True
        Change=True
        for i in keys:
            self.__FollowSet[i]=[]
        while Change:
            Change=False
            for i in keys:
                AnsList=copy.deepcopy(self.__FollowSet[i])
                if First:
                    AnsList.append('#')
                    First=False
                HasChange=[False]
                self.__followSet(i,AnsList,HasChange)
                self.__FollowSet[i]=copy.deepcopy(AnsList)
                if HasChange[0]:
                    Change=True
##################################################################################
    def getTable(self):
        '''
        算法参考：http://blog.csdn.net/hit_rxz/article/details/41652171
        '''
        self.__getFollowSet()
        TableSet={}
        keys=self.__SplitSet["keys"]
        TableSet["Start"]=keys[0]
        for i in keys:
            TableSet[i]={}
        for key in keys:
            for child in self.__SplitSet[key]:
                FirstKey=child[0]
                if FirstKey=='ε':
                    for i in self.__FollowSet.get(key):
                        TableSet[key][i]=child
                elif self.__FirstSet.get(FirstKey)==None:
                    TableSet[key][FirstKey]=child
                else:
                    '''
                    FSet=self.__FirstSet.get(FirstKey)
                    MeetNone=False
                    for i in FSet:
                        if i!='ε':
                            TableSet[key][i]=child
                        else:
                            MeetNone=True
                    if MeetNone:
                        FoSet=self.__FollowSet.get(FirstKey)
                        for i in FoSet:
                            TableSet[key][i]=['ε']'''
                    SizeOfChild=len(child)
                    Pointer=0
                    while Pointer<SizeOfChild:
                        '''
                        为了防止入S->ABC,A->ε的情况产生
                        '''
                        if self.__FirstSet.get(child[Pointer])==None:
                            TableSet[key][child[Pointer]]=child
                            break
                        else:
                            FSet=self.__FirstSet.get(child[Pointer])
                            MeetNone=False
                            for i in FSet:
                                if i!='ε':
                                    TableSet[key][i]=child
                                else:
                                    MeetNone=True
                            if not MeetNone:
                                break
                            else:
                                Pointer+=1

                    if Pointer==SizeOfChild:#说明这个产生式可以产生空串（隐式的）
                        for i in self.__FollowSet.get(key):
                            TableSet[key][i]=child

        return TableSet


class MyMenu(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        panel=wx.Panel(self,1,style=wx.EXPAND|wx.VSCROLL)
        self.Grammar=wx.TextCtrl(panel,2,"E->TE'\nE'->+TE'|ε\nT->FT'\nT'->*FT'|ε\nF->(E)|i",size=(640,150),style=wx.VSCROLL|wx.TE_MULTILINE)
        self.Sentence=wx.TextCtrl(panel,3,"i*i+i",size=(640,30))
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
        TableSet=Table(g).getTable()
        self.__ShowTable(TableSet)
        Sentence=self.Sentence.GetValue()
        SentenceStack=[]
        SentenceStack.append('#')
        SymbolStack=[]
        SymbolStack.append('#')
        SymbolStack.append(TableSet["Start"])
        for i in range(len(Sentence))[::-1]:
            SentenceStack.append(Sentence[i])
        ans="<html><body><table border='1'><tr><th>分析栈</th><th>输入串</th><th>产生式</th><th>动作</th></tr>"
        ans=ans+"<tr><td>"+str(SymbolStack)+"</td><td>"+str(SentenceStack)+"</td><td>"+" </td><td>"+"初始化</td></tr>"
        isError=False
        while len(SymbolStack)>0:
            if len(SentenceStack)==0:
                isError=True
                break
            Symbol=SymbolStack.pop()
            Character=SentenceStack.pop()
            if Symbol==Character:
                ans=ans+"<tr><td>"+str(SymbolStack)+"</td><td>"+str(SentenceStack)+"</td><td>"+" </td><td>"+"去掉"+Character+"</td></tr>"
                continue
            else:
                if TableSet.get(Symbol)!=None:
                    if TableSet.get(Symbol).get(Character)!=None:
                        Next=TableSet.get(Symbol).get(Character)
                        for i in range(len(Next))[::-1]:
                            if Next[i]!='ε':
                                SymbolStack.append(Next[i])
                        SentenceStack.append(Character)
                        ans=ans+"<tr><td>"+str(SymbolStack)+"</td><td>"+str(SentenceStack)+"</td><td>"+Symbol+"->"+str(Next)+"</td><td>"+"pop,push"+str(Next)+"</td></tr>"
                    else:
                        isError=True
        isError=not(len(SentenceStack)==0 and len(SymbolStack)==0)
        if not isError:
            ans=ans+"</table><p style='color:#FF0000'>成功</p></body></html>"
        else:
            ans="<html><body>输入出现错误</body></html>"
        self.Result.SetPage(ans)

    def __ShowTable(self,TableSet):
        SymbolSet=[]
        CharacterSet=[]
        for i in TableSet:
            if i=="Start":
                continue
            CharacterSet.append(i)
            for j in TableSet[i]:
                if not(j in SymbolSet):
                    SymbolSet.append(j)
        print(SymbolSet)
        print(TableSet)
        ans="<html><body><table border='1'><tr><th></th>"
        for i in SymbolSet:
            ans=ans+"<th>"+i+"</th>"
        ans+="</tr>"
        for character in CharacterSet:
            #ans=ans+"<tr><td>"+character+"</td>"
            t="<tr><td>"+character+"</td>"
            Symbol=[]
            for i in TableSet[character]:
                for j in range(len(SymbolSet)):
                    if i==SymbolSet[j]:
                        Symbol.append([i,j])
            count=0
            print(Symbol)
            for i in range(len(SymbolSet)):
                if count<len(Symbol) and i==Symbol[count][1]:
                    #ans=ans+"<td>"+character+"->"+str(TableSet[character][Symbol[count][0]])+"</td>"
                    t=t+"<td>"+character+"->"+str(TableSet[character][Symbol[count][0]])+"</td>"
                    count+=1
                else:
                    #ans=ans+"<td></td>"
                    t=t+"<td></td>"
            #ans=ans+"</tr>"
            t=t+"</tr>"
            ans+=t
            print(t)
        ans=ans+"</table></body></html>"
        self.Table.SetPage(ans)



class MyApp(wx.App):
    def OnInit(self):
        frame = MyMenu(None, -1, 'LL1型分析器')
        frame.SetSize(1280,720)
        frame.Show(True)
        frame.Center()
        return True




app = MyApp(0)
app.MainLoop()






