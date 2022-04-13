from flask import *
from flask import jsonify
from mysql.connector import Error
import data.connector as connector


member = Blueprint("member", __name__,
                   static_folder="static",
                   template_folder="templates")

trip_pool = connector.connect()

# api user /  signup / POST


@member.route("/api/user", methods=["POST"])
def api_user_signup():
    try:
        data = request.get_json()
        username = data["name"]
        usermail = data["email"]
        password = data["password"]
        print(username)
        print(usermail)
        print(password)
        if username == None or usermail == None or password == None:
            return jsonify({
                "error": True,
                "message": "註冊資料未完整輸入"
            })
        cnx = trip_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM `taipeitrip_member` WHERE `email`=%s", [usermail])
        result = cursor.fetchone()
        if result == None:
            data = (username, usermail, password)
            insert = "INSERT INTO `taipeitrip_member` (`name`,`email`,`password`) VALUES (%s, %s,%s);"
            cursor.execute(insert, data)
            cnx.commit()
            return jsonify({
                "ok": True
            })
        else:
            return jsonify({
                "error": True,
                "message": "帳號已存在"
            })
    except Error as e:
        print("Error", e)
    finally:
        if (cnx.is_connected()):
            cursor.close()
        cnx.close()

# api user /  signin / PATCH


@member.route("/api/user", methods=["PATCH"])
def api_user_signin():
    try:
        data = request.get_json()
        usermail = data["email"]
        password = data["password"]
        print(usermail)
        print(password)
        if usermail == None or password == None:
            return jsonify({
                "error": True,
                "message": "登入資料未完整輸入"
            })
        cnx = trip_pool.get_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM `taipeitrip_member` WHERE `email`=%s AND `password`=%s;", [usermail, password])
        result = cursor.fetchone()
        print(result)
        if result == None:
            return jsonify({
                "error": True,
                "message": "帳號或密碼輸入錯誤"
            })
        else:
            session["userid"] = result["id"]
            session["username"] = result["name"]
            session["usermail"] = result["email"]
            return jsonify({
                "ok": True
            })
    except Error as e:
        print("Error", e)
    finally:
        if (cnx.is_connected()):
            cursor.close()
        cnx.close()

# api user / get user info / GET


@member.route("/api/user", methods=["GET"])
def api_getuser():
    if "usermail" in session:
        userid = session["userid"]
        username = session["username"]
        usermail = session["usermail"]
        return jsonify({
            "data": {
                "id": userid,
                "name": username,
                "email": usermail
            }
        })
    else:
        return jsonify({
            "data": None
        })

# api user / signout / DELETE


@member.route("/api/user", methods=["DELETE"])
def api_user_signout():
    if "usermail" in session:
        del session["usermail"]
        del session["userid"]
        del session["username"]
    if "booking_info" in session:
        del session["booking_info"]
    return jsonify({
        "ok": True
    })
