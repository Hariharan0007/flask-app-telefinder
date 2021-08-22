from os import name
from flask import Flask,redirect,render_template,request,jsonify
import firebase_admin
from firebase_admin import credentials,firestore


app = Flask(__name__)

cred = credentials.Certificate("tele****.json")  # Secret Credentials not on view
firebase_admin.initialize_app(cred)
store=firestore.client()

@app.route('/',methods=["GET"])
def home(): 
    #return render_template("home.html")
    return render_template("imported template.html")

@app.route('/getdata',methods=["POST","GET"])
def getdata():
    pname=request.form.get('Name')
    pnum=int(request.form.get('Num'))
    phnlst={}
    phnlst["Name"]=pname
    phnlst["Num"]=pnum
    store.collection("chklst").add(phnlst)
    return render_template("succ.html")



@app.route('/searchdatabyname',methods=["POST","GET"])
def searchdatabyname():
    sr_item=request.form.get('Name')
    docs=store.collection("chklst").stream()
    search_list=[]
    dit={}
    for doc in docs:
        dit[doc.id]=doc.to_dict()
        search_list.append(doc.to_dict())
    flag=1
    print(type(sr_item))
    for i in range(len(search_list)):
        for k in search_list[i]:
            if sr_item==search_list[i][k]:
                flag=0
                print("Found")
                if k=='Name':
                    sr_name=search_list[i][k]
                if k=='Num':
                    sr_num=search_list[i][k]
                if type(search_list[i][k])==str:
                    print("The Contact name is found in the Database")
                    return render_template("search.html",srfnd=search_list[i])
                if type(search_list[i][k])==int:
                    print("The Contact number is found in the Database")
                    return render_template("search.html",srfnd=search_list[i])
    if flag!=0:
        print("The contact is not found in the Database")
        return render_template("notfound.html")
    return "Better Luck Next Time"


@app.route('/searchdatabynum',methods=["POST","GET"])
def searchdatabynum():
    sr_item=int(request.form.get('Num'))
    print(type(sr_item))
    docs=store.collection("chklst").stream()
    search_list=[]
    dit={}
    for doc in docs:
        dit[doc.id]=doc.to_dict()
        search_list.append(doc.to_dict())
    flag=1
    for i in range(len(search_list)):
        for k in search_list[i]:
            if sr_item==search_list[i][k]:
                flag=0
                print("Found")
                if k=='Name':
                    sr_name=search_list[i][k]
                if k=='Num':
                    sr_num=search_list[i][k]
                if type(search_list[i][k])==str:
                    print("The Contact name is found in the Database")
                    return render_template("search.html",srfnd=search_list[i])
                if type(search_list[i][k])==int:
                    print("The Contact number is found in the Database")
                    return render_template("search.html",srfnd=search_list[i])
    if flag!=0:
        print("The contact is not found in the Database")
        return render_template("notfound.html")
    return "Better Luck Next Time"


@app.route('/readdata',methods=["GET"])
def readdata():
    docs=store.collection("chklst").order_by("Name").stream()
    read_lst=[]
    dit={}
    for doc in docs:
        dit[doc.id]=doc.to_dict()
        read_lst.append(doc.to_dict())
    print(read_lst)
    for i in range(len(read_lst)):
        print(read_lst[i])
        for k in read_lst[i]:
            print(read_lst[i][k])
    return render_template("read.html",pnlst=read_lst)
    #return render_template("authorizationfailed.html")


@app.route('/re',methods=["GET"])
def re():
    return render_template("searching.html")


if __name__=='__main__':
    app.run()
