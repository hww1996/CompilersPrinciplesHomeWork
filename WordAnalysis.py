#encoding:utf-8
import copy
import wx
class WordAnalysis():
    def __init__(self,s):
        self.__s=s#输入的文件的路径

    def Analysis(self):
        f=open(self.__s,encoding="utf-8")
        #print(f.read())
        lines=f.readlines()
        '''
        MeetType:
            -1  初态
            0   遇到变量或者保留字
            1   遇到数字
            2   遇到符号
            3   遇到字符串
            4   0x
            5   xxe
            6   xx.
            7   0x后面跟东西了
            8   1e-
            9  1e跟东西
            10	xx.后面跟东西了
			11	xxxl
			12	xxxu
			13	/*
			14	/*.....*
			15  xxxf
			16  xxexxxl
			17  xxexxxll
        '''
        MeetType=-1
        keyword=["auto","break","case","char","const","continue","default","do","double","else","include"
                        "enum","extern","float","for","goto","if","int","long","redister","return","short","signed",
                        "sizeof","static","struct","switch","typedef","union","unsigned","void","volatile","while"]
        BaseOperator=[">","<","+","-","*","/","%","&","|","~","^","!","?",":","#","=","."]
        BaseSplit=["[","]","{","}","(",")",";",","]
        ans=""
        AllAns=[]
        isError=False
        FirstSginLetter=""
        line=0
        for s in lines:
            i=0
            n=len(s)
            result=[]
            start=-1
            line+=1
            while i<n:
                if MeetType==-1:
                    isError=False
                    ans=""
                    if (ord(s[i])<=ord('z') and ord(s[i])>=ord('a')) or (ord(s[i])<=ord('Z') and ord(s[i])>=ord('A')) or s[i]=="_":
                        MeetType=0
                        ans+=s[i]
                        start=i
                    elif ord(s[i])<=ord('9') and ord(s[i])>=ord('0'):
                        MeetType=1
                        start=i
                        ans+=s[i]
                    elif s[i]=="\'" or s[i]=="\"":
                        FirstSginLetter=s[i]
                        MeetType=3
                        r={}
                        r["type"]="split"
                        r["val"]=s[i]
                        r["start"]=i
                        result.append(r)
                        start=i+1
                    elif s[i] in BaseOperator:
                        ans+=s[i]
                        MeetType=2
                        start=i
                    elif s[i] in BaseSplit:
                        r={}
                        r["type"]="split"
                        r["val"]=s[i]
                        r["start"]=i
                        i+=1
                        result.append(r)
                        continue
                    elif s[i]==" " or s[i]=="\t" or s[i]=="\n":
                        pass
                    else:
                        r={}
                        r["type"]="error"
                        r["val"]=s[i]
                        r["start"]=i
                        i+=1
                        result.append(r)
                        continue

############################################################################变量，关键字等
                elif MeetType==0:
                    if (ord(s[i])<=ord('z') and ord(s[i])>=ord('a')) or (ord(s[i])<=ord('Z') and ord(s[i])>=ord('A')) or s[i]=="_" or (ord(s[i])<=ord('9') and ord(s[i])>=ord('0')):
                        ans+=s[i]
                    else:
                        r={}
                        if ans in keyword:
                            r["type"]="keyword"
                            r["val"]=ans
                            r["start"]=start
                        else:
                            r["type"]="id"
                            r["val"]=ans
                            r["start"]=start
                        ans=""
                        isError=False
                        result.append(r)
                        MeetType=-1
                        if s[i]==".":
                            rs={}
                            rs["type"]="oprator"
                            rs["val"]="."
                            rs["start"]=i
                            result.append(rs)
                            i+=1
                        continue


###########################################################################常量
                elif MeetType==1:
                    if ans=="0":
                        if s[i]=='x':
                            MeetType=4
                            ans+=s[i]
                            i+=1
                            continue
                    if s[i]=="e":
                        ans+=s[i]
                        MeetType=5
                    if ord(s[i])>=ord('0') and ord(s[i])<=ord('9'):
                        ans+=s[i]
                    elif s[i]==".":
                        MeetType=6
                        ans+=s[i]
                    elif s[i] in BaseOperator or s[i] in BaseSplit or s[i]=="\'" or s[i]=="\"" or s[i]==" " or s[i]=="\t" or s[i]=="\n":
                        r={}
                        if isError:
                            r["type"]="error"
                            r["val"]=ans
                            r["start"]=start
                        else:
                            r["type"]="const"
                            r["val"]=ans
                            r["start"]=start
                        isError=False
                        result.append(r)
                        MeetType=-1
                        continue
                    elif s[i]=='l':
                        ans+=s[i]
                        MeetType=11
                    elif s[i]=="u":
                        ans+=s[i]
                        MeetType=12
                    else:
                        isError=True
                        ans+=s[i]


                elif MeetType==4:
                    if (ord(s[i])>=ord('0') and ord(s[i])<=ord('9')) or (ord(s[i])>=ord('a') and ord(s[i])<=ord('f')):
                        ans+=s[i]
                    elif (ord(s[i])>=ord('g') and ord(s[i])<=ord('z')) or (ord(s[i])>=ord('A') and ord(s[i])<=ord('Z')) or s[i]=="_":
                        isError=True
                        ans+=s[i]
                    else:
                        isError=False
                        r={}
                        r["type"]="error"
                        r["val"]=ans
                        r["start"]=start
                        MeetType=-1
                        isError=False
                        result.append(r)
                        continue
                    MeetType=7

                elif MeetType==7:
                    if (ord(s[i])>=ord('0') and ord(s[i])<=ord('9')) or (ord(s[i])>=ord('a') and ord(s[i])<=ord('f')):
                        ans+=s[i]
                    elif s[i] in BaseOperator or s[i] in BaseSplit or s[i]==" " or s[i]=="\t" or s[i]=="\'" or s[i]=="\""or s[i]=="\n":
                        r={}
                        if isError:
                            r["type"]="error"
                        else:
                            r["type"]="const"
                        r["val"]=ans
                        r["start"]=start
                        isError=False
                        MeetType=-1
                        result.append(r)
                        continue
                    else:
                        isError=True
                        ans+=s[i]
#############################################################################################
                elif MeetType==5:
                    if (ord(s[i])>=ord('0') and ord(s[i])<=ord('9')):
                        ans+=s[i]
                        MeetType=9
                    elif s[i]=="-":
                        ans+=s[i]
                        MeetType=8
                    elif (ord(s[i])>=ord('a') and ord(s[i])<=ord('z')) or (ord(s[i])>=ord('A') and ord(s[i])<=ord('Z')) or s[i]=="_":
                        isError=True
                        ans+=s[i]
                        MeetType=9
                    else:
                        isError=False
                        r={}
                        r["type"]="error"
                        r["val"]=ans
                        r["start"]=start
                        MeetType=-1
                        result.append(r)
                        continue


                elif MeetType==8:
                    if (ord(s[i])>=ord('0') and ord(s[i])<=ord('9')):
                        ans+=s[i]
                    elif (ord(s[i])>=ord('a') and ord(s[i])<=ord('z')) or (ord(s[i])>=ord('A') and ord(s[i])<=ord('Z')) or s[i]=="_":
                        isError=True
                        ans+=s[i]
                    else:
                        isError=False
                        r={}
                        r["type"]="error"
                        r["val"]=ans
                        r["start"]=start
                        MeetType=-1
                        result.append(r)
                        continue
                    MeetType=9

                elif MeetType==9:
                    if (ord(s[i])>=ord('0') and ord(s[i])<=ord('9')):
                        ans+=s[i]
                    elif s[i]=="f":
                        ans+=s[i]
                        MeetType=15
                    elif s[i]=="l":
                        ans+=s[i]
                        MeetType=16
                    elif s[i] in BaseOperator or s[i] in BaseSplit or s[i]==" " or s[i]=="\t" or s[i]=="\'" or s[i]=="\""or s[i]=="\n":
                        r={}
                        if isError:
                            r["type"]="error"
                        else:
                            r["type"]="const"
                        r["val"]=ans
                        r["start"]=start
                        MeetType=-1
                        isError=False
                        result.append(r)
                        continue
                    else:
                        isError=True
                        ans+=s[i]

##############################################################################################
                elif MeetType==6:
                    if (ord(s[i])>=ord('0') and ord(s[i])<=ord('9')):
                        ans+=s[i]
                    elif (ord(s[i])>=ord('a') and ord(s[i])<=ord('z')) or (ord(s[i])>=ord('A') and ord(s[i])<=ord('Z')) or s[i]=="_":
                        isError=True
                        ans+=s[i]
                    else:
                        isError=False
                        r={}
                        r["type"]="error"
                        r["val"]=ans
                        r["start"]=start
                        MeetType=-1
                        result.append(r)
                        continue
                    MeetType=10

                elif MeetType==10:
                    if (ord(s[i])>=ord('0') and ord(s[i])<=ord('9')):
                        ans+=s[i]
                    elif s[i]=="e":
                        ans+=s[i]
                        MeetType=5
                    elif s[i]=="f":
                        ans+=s[i]
                        r={}
                        if isError:
                            r["type"]="error"
                        else:
                            r["type"]="const"
                        r["val"]=ans
                        r["start"]=start
                        MeetType=-1
                        isError=False
                        result.append(r)
                    elif s[i]=='.':
                        ans+=s[i]
                        isError=True
                    elif s[i] in BaseOperator or s[i] in BaseSplit or s[i]==" " or s[i]=="\t" or s[i]=="\'" or s[i]=="\""or s[i]=="\n":
                        r={}
                        if isError:
                            r["type"]="error"
                        else:
                            r["type"]="const"
                        r["val"]=ans
                        r["start"]=start
                        MeetType=-1
                        isError=False
                        result.append(r)
                        continue
                    else:
                        ans+=s[i]
                        isError=True

                elif MeetType==11:
                    if s[i]=="l" or s[i]=="u":
                        ans+=s[i]
                        r={}
                        if isError:
                            r["type"]="error"
                        else:
                            r["type"]="const"
                        r["val"]=ans
                        r["start"]=start
                        MeetType=-1
                        isError=False
                        result.append(r)
                    else:
                        r={}
                        if isError:
                            r["type"]="error"
                        else:
                            r["type"]="const"
                        r["val"]=ans
                        r["start"]=start
                        MeetType=-1
                        isError=False
                        result.append(r)
                        continue

                elif MeetType==12:
                    if s[i]=="l":
                        ans+=s[i]
                        r={}
                        if isError:
                            r["type"]="error"
                        else:
                            r["type"]="const"
                        r["val"]=ans
                        r["start"]=start
                        MeetType=-1
                        isError=False
                        result.append(r)
                    else:
                        r={}
                        if isError:
                            r["type"]="error"
                        else:
                            r["type"]="const"
                        r["val"]=ans
                        r["start"]=start
                        MeetType=-1
                        isError=False
                        result.append(r)
                        continue


#####################################################################################字符串
                elif MeetType==3:
                    if s[i]!=FirstSginLetter:
                        ans+=s[i]
                    else:
                        if FirstSginLetter=="\'":
                            if len(ans)==1 and ans=="\\":
                                ans+=s[i]
                            elif len(ans)==1:
                                r={}
                                rs={}
                                r["type"]="char"
                                r["val"]=ans
                                r["start"]=start
                                result.append(r)
                                rs["type"]="split"
                                rs["val"]=FirstSginLetter
                                rs["start"]=i
                                ans=""
                                isError=False
                                result.append(rs)
                                MeetType=-1
                                FirstSginLetter=""
                            elif len(ans)==2:
                                if ans[0]=="\\":
                                    r={}
                                    rs={}
                                    r["type"]="char"
                                    r["val"]=ans
                                    r["start"]=start
                                    result.append(r)
                                    rs["type"]="split"
                                    rs["val"]=FirstSginLetter
                                    rs["start"]=i
                                    ans=""
                                    isError=False
                                    result.append(rs)
                                    MeetType=-1
                                    FirstSginLetter=""
                            else:
                                r={}
                                rs={}
                                r["type"]="error"
                                r["val"]=ans
                                r["start"]=start
                                result.append(r)
                                rs["type"]="split"
                                rs["val"]=FirstSginLetter
                                rs["start"]=i
                                ans=""
                                isError=False
                                result.append(rs)
                                MeetType=-1
                                FirstSginLetter=""
                        else:
                            SpritCount=0
                            AnsLen=len(ans)-1
                            while AnsLen>=0 and ans[AnsLen]=="\\":
                                SpritCount+=1
                                AnsLen-=1
                            if SpritCount%2==0:
                                r={}
                                rs={}
                                r["type"]="string"
                                r["val"]=ans
                                r["start"]=start
                                result.append(r)
                                rs["type"]="split"
                                rs["val"]=FirstSginLetter
                                rs["start"]=i
                                ans=""
                                isError=False
                                result.append(rs)
                                MeetType=-1
                                FirstSginLetter=""
                            else:
                                ans+=s[i]


################################################################################符号
                elif MeetType==2:
                    if ans=="-":
                        if s[i]=="-" or s[i]==">" or s[i]=="=":
                            ans+=s[i]
                            r={}
                            r["type"]="operator"
                            r["val"]=ans
                            r["start"]=start
                            result.append(r)
                            MeetType=-1
                        else:
                            r={}
                            r["type"]="operator"
                            r["val"]=ans
                            r["start"]=start
                            ans=""
                            result.append(r)
                            MeetType=-1
                            continue

                    elif ans=="+":
                        if s[i]=="+" or s[i]=="=":
                            ans+=s[i]
                            r={}
                            r["type"]="operator"
                            r["val"]=ans
                            r["start"]=start
                            ans=""
                            result.append(r)
                            MeetType=-1
                        else:
                            r={}
                            r["type"]="operator"
                            r["val"]=ans
                            r["start"]=start
                            ans=""
                            result.append(r)
                            MeetType=-1
                            continue

                    elif ans=="|" or ans=="&":
                        if s[i]=="=":
                            ans+=s[i]
                            r={}
                            r["type"]="operator"
                            r["val"]=ans
                            r["start"]=start
                            ans=""
                            result.append(r)
                            MeetType=-1
                        elif s[i]==ans:
                            ans+=s[i]
                            r={}
                            r["type"]="operator"
                            r["val"]=ans
                            r["start"]=start
                            ans=""
                            result.append(r)
                            MeetType=-1
                        else:
                            r={}
                            r["type"]="operator"
                            r["val"]=ans
                            r["start"]=start
                            ans=""
                            result.append(r)
                            MeetType=-1
                            continue

                    elif ans=="<" or ans==">":
                        if s[i]=="=":
                            ans+=s[i]
                        elif s[i]==ans:
                            ans+=s[i]
                        else:
                            r={}
                            r["type"]="operator"
                            r["val"]=ans
                            r["start"]=start
                            ans=""
                            result.append(r)
                            MeetType=-1
                            continue

                    elif ans=="=" or ans=="!":
                        if s[i]=="=":
                            ans+=s[i]
                            r={}
                            r["type"]="operator"
                            r["val"]=ans
                            r["start"]=start
                            ans=""
                            result.append(r)
                            MeetType=-1
                        else:
                            r={}
                            r["type"]="operator"
                            r["val"]=ans
                            r["start"]=start
                            ans=""
                            result.append(r)
                            MeetType=-1
                            continue

                    elif ans=="~" or ans==".":
                        r={}
                        r["type"]="operator"
                        r["val"]=ans
                        r["start"]=start
                        ans=""
                        result.append(r)
                        MeetType=-1
                        continue

                    elif ans=="^" or ans=="*" or ans=="%" or ans=="<<" or ans==">>":
                        if s[i]=="=":
                            ans+=s[i]
                            r={}
                            r["type"]="operator"
                            r["val"]=ans
                            r["start"]=start
                            ans=""
                            result.append(r)
                            MeetType=-1
                        else:
                            r={}
                            r["type"]="operator"
                            r["val"]=ans
                            r["start"]=start
                            ans=""
                            result.append(r)
                            MeetType=-1
                            continue


                    elif ans=="/":
                        if s[i]=="/":
                            ans=""
                            MeetType=-1
                            break
                        elif s[i]=="*":
                            MeetType=13
                        elif s[i]=="=":
                            ans+=s[i]
                            r={}
                            r["type"]="operator"
                            r["val"]=ans
                            r["start"]=start
                            ans=""
                            result.append(r)
                            MeetType=-1
                        else:
                            r={}
                            r["type"]="operator"
                            r["val"]=ans
                            r["start"]=start
                            ans=""
                            result.append(r)
                            MeetType=-1
                            continue


                elif MeetType==13:
                    if s[i]=="*":
                        MeetType=14

                elif MeetType==14:
                    if s[i]=="/":
                        MeetType=-1
                    else:
                        MeetType=13

                elif MeetType==15:
                    if s[i] in BaseOperator or s[i] in BaseSplit or s[i]==" " or s[i]=="\t" or s[i]=="\'" or s[i]=="\""or s[i]=="\n":
                        r={}
                        if isError:
                            r["type"]="error"
                        else:
                            r["type"]="const"
                        r["val"]=ans
                        r["start"]=start
                        MeetType=-1
                        isError=False
                        result.append(r)
                        continue
                    else:
                        ans+=s[i]
                        isError=True

                elif MeetType==16:
                    if s[i] in BaseOperator or s[i] in BaseSplit or s[i]==" " or s[i]=="\t" or s[i]=="\'" or s[i]=="\""or s[i]=="\n":
                        r={}
                        if isError:
                            r["type"]="error"
                        else:
                            r["type"]="const"
                        r["val"]=ans
                        r["start"]=start
                        MeetType=-1
                        isError=False
                        result.append(r)
                        continue
                    elif s[i]=="l":
                        ans+=s[i]
                        MeetType=15
                    else:
                        ans+=s[i]
                        isError=True
                i+=1
            if len(ans)>0:
                if MeetType==-1 or MeetType==14 or MeetType==13:
                    pass
                elif MeetType==0:
                    if isError:
                        r={}
                        r["type"]="error"
                        r["val"]=ans
                        r["start"]=start
                        result.append(r)
                    elif ans in keyword:
                        r={}
                        r["type"]="keyword"
                        r["val"]=ans
                        r["start"]=start
                        result.append(r)
                    else:
                        r={}
                        r["type"]="id"
                        r["val"]=ans
                        r["start"]=start
                        result.append(r)
                elif MeetType==2:
                    r={}
                    r["type"]="operator"
                    r["val"]=ans
                    r["start"]=start
                    result.append(r)
                elif MeetType==3:
                    r={}
                    r["type"]="string"
                    r["val"]=ans
                    r["start"]=start
                    result.append(r)

                elif MeetType==1 or MeetType==7 or MeetType==9 or MeetType==10 or MeetType==11 or MeetType==12:
                    if isError:
                        r={}
                        r["type"]="error"
                        r["val"]=ans
                        r["start"]=start
                        result.append(r)
                    else:
                        r={}
                        r["type"]="const"
                        r["val"]=ans
                        r["start"]=start
                        result.append(r)
                else:
                    r={}
                    r["type"]="error"
                    r["val"]=ans
                    r["start"]=start
                    result.append(r)
            if len(result)>0:
                dict={}
                dict["line"]=line
                dict["content"]=copy.deepcopy(result)
                AllAns.append(copy.deepcopy(dict))
            if MeetType!=13 and MeetType!=14:
                MeetType=-1
        return AllAns


class MyMenu(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        self.panel=wx.Panel(self,100)
        btn=wx.Button(self.panel,1,"打开文件",style=wx.TE_LEFT)
        self.label=wx.StaticText(self.panel,2,"路径为空",style=wx.TE_LEFT)
        self.Bind(wx.EVT_BUTTON,self.__OnOpen,id=1)
        self.text=wx.TextCtrl(self.panel,9,"",size=(800,1000),style=wx.VSCROLL|wx.TE_MULTILINE)
        self.text.SetEditable(False)
        box=wx.BoxSizer(orient=wx.VERTICAL)
        box.Add(btn,border=5,flag=wx.EXPAND)
        box.Add(self.label,border=5,flag=wx.EXPAND)
        box.Add(self.text,border=5,flag=wx.EXPAND)
        self.panel.SetSizer(box)





    def __OnOpen(self,event):
        fd=wx.FileDialog(self,"打开c文件","C:\\",wildcard="C files(*.c)|*.c|All files(*.*)|*.*" )
        if fd.ShowModal()==wx.ID_OK:
            filePath=fd.GetPath()
            self.label.SetLabelText("路径为:"+filePath)
            a=WordAnalysis(filePath)
            t=a.Analysis()
            #print(t)
            self.text.SetLabel("")
            self.text.AppendText("行\t\t列\t\t种类\t\t值\r\n")
            for i in t:
                for j in i["content"]:
                    self.text.AppendText(str(i["line"])+"\t\t"+str(j["start"])+"\t\t"+j["type"]+"\t\t"+j["val"]+"\r\n")
        fd.Destroy()




class MyApp(wx.App):
    def OnInit(self):
        frame = MyMenu(None, -1, '词法分析器')
        frame.SetSize(1280,720)
        frame.Show(True)
        frame.Center()
        return True

app = MyApp(0)
app.MainLoop()






