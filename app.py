from flask import Flask, request, jsonify, url_for, g, render_template
from markupsafe import escape

app = Flask(__name__)

# Simulated in-memory storage
items = {}


@app.route("/")
def hello_world():
    print(g)
    dir(g)
    return "<p>Hello, World!</p>"


# @app.route("/hello/<name>")
# def hello(name):
#     # name = '<script>alert("bad")</script>'
#     # the escape(name) function converts <script>alert("bad")</script> to &lt;script&gt;alert(&quot;bad&quot;)&lt;/script&gt;. This way, the browser displays <script>alert("bad")</script> as plain text rather than interpreting it as a script.
#     return f"Hello, {escape(name)}!"


"""
在 Jinja2 模板中，自动转义是默认开启的，这意味着如果一个变量包含 HTML 代码,Jinja2 会自动将其转义为安全的文本，以避免 XSS 跨站脚本攻击）等安全风险。
示例 1：自动转义

name = "<h1>欢迎来到我们的网站</h1>"
在模板中直接使用 {{ name }} 会自动将 HTML 标签转义：<p>{{ name }}</p>
渲染结果：
<p>&lt;h1&gt;欢迎来到我们的网站&lt;/h1&gt;</p>
示例 2： 使用 |safe 过滤器

如果你可以信任 name 的值，并希望渲染它时保留 HTML 标签，可以使用 |safe 过滤器：
<p>{{ name|safe }}</p>

示例 3：使用 Markup 类标记为安全
在 Python 代码中，你也可以使用 Markup 类来标记某个变量为安全 HTML：
name = Markup("<h1>欢迎来到我们的网站</h1>")


"""


@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    return render_template("hello.html", person=name)


@app.route("/user/<int:userId>")
def show_user_profile(userId):
    # show the user profile for that user
    return f"User {escape(userId)}"


# curl -X POST http://127.0.0.1:5000/items -H "Content-Type: application/json" -d '{"id": 1, "name": "Item1"}'
# In Flask, the return statement in a route handler can return two values:
# The response content: This is usually JSON data created with jsonify or plain text/HTML.
# The HTTP status code: This indicates the outcome of the request, such as 200 OK, 400 Bad Request, or 201 Created.
# default is 200
@app.route("/post/", methods=["POST"])
def post():
    print(type(request.get_json()))
    print(request.get_data())
    
    data = request.get_json()  # Get JSON data from the request body
    if not data:
        return jsonify({"error": "Missing JSON data"}), 400

    item_id = (
        data["id"] if id in data.keys() else None
    )  # If the key "id" is missing in data, Python raises a KeyError, which can crash your application
    name = data.get("name")  #  If "name" is missing, get() returns None
    if not item_id or not name:
        return jsonify({"error": "Missing 'id' or 'name'"}), 400

    if item_id in items:
        return jsonify({"error": "Item already exists"}), 400

    items[item_id] = {"id": item_id, "name": name}

    return jsonify({"message": "Item created", "item": items[item_id]}), 201


@app.route(
    "/search/"
)  # URL 没有尾部斜杠，因此其行为表现与一个文件类似。如果访问 这个 URL 时添加了尾部斜杠（ /about/ ）就会得到一个 404 “未找到” 错误。
def show_search_result():
    # query string: 要操作 URL （如 ?key=value ）中提交的参数可以使用 args 属性:
    
    print(type(request.args), type(request.form), type(request.data), type(request.values),  type(request.environ), type(request.headers))
    print(request.args.to_dict())
    print(request.args.get("id", "xxxx"))
    user_id = request.args.get("id", type=int)
    print(escape(user_id))
    if user_id is None:
        user_id = -1

    return f"User {escape(user_id)}"


@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    # show the subpath after /path/
    return f"Subpath {escape(subpath)}"


# string（缺省值） 接受任何不包含斜杠的文本
# int 接受正整数
# float 接受正浮点数
# path 类似 string ，但可以包含斜杠
# uuid 接受 UUID 字符串


# url_for() 函数用于构建指定函数的 URL。它把函数名称作为第 一个参数。它可以接受任意个关键字参数，
# 每个关键字参数对应 URL 中的变量。 未知变量将添加到 URL 中作为查询参数。

# app.test_request_context() sets up a temporary request context for testing without needing an actual server request.
# It’s useful for testing functions that use request, session, or url_for.
# In Flask, certain objects, such as request, session, and g, only work within a request context. This means you can normally only access them when an HTTP request is being processed. By using app.test_request_context(), you create a simulated request context, which allows you to interact with these objects in your code or tests without needing a real client request.

with app.test_request_context():
    print(
        url_for("show_search_result", next="/")
    )  # 未知变量将添加到 URL 中作为查询参数。
    print(url_for("show_subpath", subpath="aa/bb"))  # 已知的关键字参数对应 URL 中的变量



@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            print(f"user name is {request.form['username']}")
            print(f"password is {request.form['password']}")
            return {"status": 'ok'}, 200
        else:    
            error = 'Invalid Credentials. Please try again.'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)




@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')


# if __name__ == "__main__":
#     app.run(debug=True)
