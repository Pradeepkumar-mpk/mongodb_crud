from flask import Flask,render_template,request,redirect,url_for
from pymongo import MongoClient

app=Flask(__name__)
@app.route("/insert",methods=['POST',"GET"])
def insert():
    if request.form.get("id")!=None:
        id=request.form.get("id")
        name=request.form.get("name")
        language=request.form.get("language")
        dic={"id":id,"name":name,"language":language}
        
        client=MongoClient("mongodb://localhost:27017")
        database=client.dbname
        collection=database.tname
        collection.insert_one(dic)
        print("success")
        client.close()

    return render_template("insert.html")

@app.route("/")
def read():
    client=MongoClient("mongodb://localhost:27017")
    database=client.dbname
    collection=database.tname
    x=collection.find()
    l=[]
    for i in x:
        dic={"id":i.get("id"),"name":i.get("name"),"language":i.get("language")}
        l.append(dic)
    client.close()

    return render_template("index.html",data=l)

@app.route("/update/<id>",methods=["post","get"])
def update(id):
    if request.form.get("id")!=None:
        id=request.form.get("id")
        name=request.form.get("name")
        language=request.form.get("language")
        client=MongoClient("mongodb://localhost:27017")
        database=client.dbname
        collection=database.tname
        collection.update_one({"id":id},{"$set":{"name":name,"language":language}})
        client.close()
        return redirect(url_for("read"))

    client=MongoClient("mongodb://127.0.0.1:27017")
    database=client.dbname
    collection=database.tname
    x=collection.find_one({"id":id})
    dic={"id":x.get("id"),"name":x.get("name"),"mobile":x.get("language")}
    client.close()

    return render_template("update.html",data=dic)

@app.route("/delete/<id>")
def delete(id):
    client=MongoClient("mongodb://127.0.0.1:27017")
    database=client.dbname
    table=database.tname
    table.delete_one({"id":id})
    client.close()
    return redirect(url_for("read"))



if __name__ == "__main__":
 app.run(debug=True)
  