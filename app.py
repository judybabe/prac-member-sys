#初始化資料庫連線
import pymongo
client=pymongo.MongoClient("mongodb+srv://root:rootpassword@cluster0.wykva7s.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db=client.member_system
print("資料庫連線建立成功")

# 初始化 Flask 伺服器
from flask import *
app=Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)
app.secret_key="any string but keep secret"
# 處理路由
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/member")
def member():
    if "name" in session:
        return render_template("member.html")
    else:
        return redirect("/")
@app.route("/error")
def error():
    message=request.args.get("msg", "發生錯誤，請聯繫客服")
    return render_template("error.html", message=message) 
@app.route("/signup", methods=["POST"])
def signup():
    name=request.form["name"]
    email=request.form["email"]
    password=request.form["password"]
    collection=db.user
    result=collection.find_one({
        "email":email
    })
    if result != None:
        return redirect("/error?msg=信箱已經被註冊")
    
    collection.insert_one({
        "name":name,
        "email":email,
        "password":password
    })
    return redirect("/")
@app.route("/signin", methods=["POST"])
def signin():
    # 從前端取得使用者的輸入
    email=request.form["email"]
    password=request.form["password"]
    # 和資料庫作互動
    collection=db.user
    # 檢查信箱密碼是否正確
    result=collection.find_one({
        "$and":[
            {"email":email},
            {"password":password}
        ]
    })
    if result==None:
        return redirect("/error?msg=帳號或密碼輸入錯誤")
    # 登入成功，在 Session 紀錄會員資訊，導向到會員頁面
    session["name"]=result["name"]
    return redirect("/member")

@app.route("/signout")
def signout():
    # 移除 Session 中的會員資訊
    del session["name"]
    return redirect("/")

app.run(port=3000)