"""
Copyright (c) 2020 cyrxdzj
PyCheer is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:
         http://license.coscl.org.cn/MulanPSL2
THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
# import some modules
from flask import Flask, request, make_response  # 主服务Flask引用
from urllib.request import unquote, quote  # 解析或编码有特殊字符的URL
import os  # 引用此模块，用于文件（夹）的其它功能。
import sys  # 获取命令行参数及自身目录
import requests  # 获取自身公网IP
import json  # 解析json
import time  # 获取当前时间
import hashlib  # 制作token
import webbrowser  # 启动浏览器
import threading  # 使用线程启动浏览器

try:  # 获取SVG
    from svg import *
except:
    from .svg import *


def get_version():  # 获得当前version
    try:
        return __version__  # 若此模块已通过setup.py安装，一定有__version__变量。
    except:
        return "DEBUG,No version."  # 如果没有__version__变量，则触发异常，返回一个这样的字符串。


# 用来默认展示的。
show_str = r'''
 _____  __    __  _____   _   _   _____   _____   _____   
|  _  \ \ \  / / /  ___| | | | | | ____| | ____| |  _  \  
| |_| |  \ \/ /  | |     | |_| | | |__   | |__   | |_| |  
|  ___/   \  /   | |     |  _  | |  __|  |  __|  |  _  /  
| |       / /    | |___  | | | | | |___  | |___  | | \ \  
|_|      /_/     \_____| |_| |_| |_____| |_____| |_|  \_\ 
AUTHOR:cyrxdzj
LICENSE:MulanPSL-2.0
VERSION:%s
A WEB editor for python.
Please see https://gitee.com/cyrxdzj/PyCheer
You can type "python -m PyCheer run" to launch this application.
You can type "python -m PyCheer help" for help.
''' % (get_version())

mydir = os.path.dirname(__file__)
workdir = os.getcwd()

help_str = r'''
##############################
pycheer version
View the version of this software.
------------------------------
No additional parameters are required.

##############################
pycheer run
Start pycheer in this directory.
------------------------------
-p  --port      Set the run port of PyCheer.
-b  --browser   Let PyCheer run and then automatically open the browser.
-n  --nogetip   Disable automatic acquisition of public IPs.

##############################
pycheer help
Get help.
------------------------------
No additional parameters are required.
'''


def get_suffix(file_path: str):  # 文件获取后缀。
    strs = file_path.split("/")
    if not strs[-1]:
        return ''
    file_name_strs = strs[-1].split(".")
    if len(file_name_strs) == 0:
        return ''
    if not file_name_strs[-1]:
        return ''
    return file_name_strs[-1]


def run(params):
    def open_browser(url):
        time.sleep(1)
        webbrowser.open(url=url)

    app = Flask("PyCheer Server")
    token = hashlib.sha256(
        time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()).encode(encoding="UTF-8", errors="strict")).hexdigest()
    print("The token for this run is\033[34m %s\033[0m." % token)
    common_ip = None
    if not params['-n']:
        try:
            common_ip = json.loads(requests.get("https://api.ipify.org/?format=json").text)['ip']
            print("Public netip acquisition is complete, but for reference only.")
        except:
            print("Failure to obtain a public network IP.")
    print(
        "If you are using your local browser to access PyCheer, please use the following address:\033[32m %s\033[0m" % (
                "http://localhost:%s/begin?token=%s" % (params["-p"], token)))
    if not common_ip:
        print(
            "If you are using a non-native browser to access PyCheer, please use the following address:\033[32m %s\033[0m" % (
                    "http://</Your public IP.>:%s/begin?token=%s" % (params["-p"], token)))
    else:
        print(
            "If you are using a non-native browser to access PyCheer, please use the following address:\033[32m %s\033[0m" % (
                    "http://%s:%s/begin?token=%s" % (common_ip, params["-p"], token)))
    if params['-b']:
        t = threading.Thread(target=open_browser, args=("http://localhost:%s/begin?token=%s" % (params["-p"], token),))
        t.start()

    # ------------------------------DO GET------------------------------
    @app.route("/", methods=["GET"])
    @app.route("/index", methods=['GET'])
    def index_handler():
        if request.args.get("token") != token and request.cookies.get("token") != token:
            return '', 302, [("Location", "begin")]
        response = make_response('')
        response.status = 302
        response.headers['Location'] = 'tree'
        if request.args.get("token") == token:
            response.set_cookie("token", token)
        return response

    @app.route("/begin", methods=['GET'])
    def begin_handler():
        if request.cookies.get("token") == token:
            return '', 302, [("Location", request.args.get("go_url") or "/index")]
        if request.args.get("token") == token:
            response = make_response("")
            response.status = 302
            response.set_cookie("token", token)
            response.headers["Location"] = request.args.get("go_url") or "/index"
            return response
        return open(os.path.join(mydir, "./html/begin.html"), encoding="UTF-8").read(), 200

    @app.route("/see", methods=["GET"])
    def see_handler():
        if request.args.get("token") != token and request.cookies.get("token") != token:
            return '', 302, [
                ("Location", "begin?go_url=" + (quote("/see?file_path=" + request.args.get("file_path", default=""))))]
        file_path = request.args.get('path')
        if not file_path:
            response = make_response('403 Forbidden')
            response.status = 403
            if request.args.get("token") == token:
                response.set_cookie("token", token)
            return response
        file_path = unquote(file_path)
        if not os.path.isfile(file_path):
            response = make_response("404 Not Found")
            response.status = 404
            if request.args.get("token") == token:
                response.set_cookie("token", token)
            return response
        if get_suffix(file_path) == 'py':
            response_data = open(os.path.join(mydir, "./html/editpy.html"), encoding="UTF-8").read().replace(
                "<init_code>", quote(open(file_path, encoding="UTF-8").read()))
            response = make_response(response_data)
            response.status = 200
            if request.args.get("token") == token:
                response.set_cookie("token", token)
            response.headers["Content-Type"] = "text/html;charset=utf-8"
            return response
        elif get_suffix(file_path) == 'png':
            response = make_response(open(file_path, "rb").read())
            response.status = 200
            if request.args.get("token") == token:
                response.set_cookie("token", token)
            response.headers["Content-Type"] = "image/png"
            return response
        elif get_suffix(file_path) == 'jpg':
            response = make_response(open(file_path, "rb").read())
            response.status = 200
            if request.args.get("token") == token:
                response.set_cookie("token", token)
            response.headers["Content-Type"] = "image/jpg"
            return response
        elif get_suffix(file_path) == 'md':
            response_data = open(os.path.join(mydir, "./html/editmd.html"), encoding="UTF-8").read().replace(
                "<init_code>", quote(open(file_path, encoding="UTF-8").read()))
            response = make_response(response_data)
            response.status = 200
            if request.args.get("token") == token:
                response.set_cookie("token", token)
            response.headers["Content-Type"] = "text/html;charset=utf-8"
            return response
        elif get_suffix(file_path) == 'html':
            response_data = open(os.path.join(mydir, "./html/edithtml.html"), encoding="UTF-8").read().replace(
                "<init_code>", quote(open(file_path, encoding="UTF-8").read()))
            response = make_response(response_data)
            response.status = 200
            if request.args.get("token") == token:
                response.set_cookie("token", token)
            response.headers["Content-Type"] = "text/html;charset=utf-8"
            return response
        elif get_suffix(file_path) == 'css':
            response_data = open(os.path.join(mydir, "./html/editcss.html"), encoding="UTF-8").read().replace(
                "<init_code>", quote(open(file_path, encoding="UTF-8").read()))
            response = make_response(response_data)
            response.status = 200
            if request.args.get("token") == token:
                response.set_cookie("token", token)
            response.headers["Content-Type"] = "text/html;charset=utf-8"
            return response
        elif get_suffix(file_path) == 'txt':
            response_data = open(os.path.join(mydir, "./html/edittxt.html"), encoding="UTF-8").read().replace(
                "<init_code>", quote(open(file_path, encoding="UTF-8").read()))
            response = make_response(response_data)
            response.status = 200
            if request.args.get("token") == token:
                response.set_cookie("token", token)
            response.headers["Content-Type"] = "text/html;charset=utf-8"
            return response
        elif get_suffix(file_path) == 'js':
            response_data = open(os.path.join(mydir, "./html/editjs.html"), encoding="UTF-8").read().replace(
                "<init_code>", quote(open(file_path, encoding="UTF-8").read()))
            response = make_response(response_data)
            response.status = 200
            if request.args.get("token") == token:
                response.set_cookie("token", token)
            response.headers["Content-Type"] = "text/html;charset=utf-8"
            return response
        else:
            response = make_response(open(file_path, encoding="UTF-8").read())
            response.status = 200
            if request.args.get("token") == token:
                response.set_cookie("token", token)
            response.headers["Content-Type"] = "text/plain;charset=utf-8"
            return response

    @app.route("/js/<js_path>", methods=['GET'])
    def js_handler(js_path=""):
        if not os.path.isfile(os.path.join(mydir, "./js/%s" % js_path)):
            response = make_response("404 Not Found")
            response.status = 404
        else:
            response = make_response(open(os.path.join(mydir, "./js/%s" % js_path), encoding="UTF-8").read())
            response.status = 200
            response.headers["Content-type"] = "text/script"
        if request.args.get("token") == token:
            response.set_cookie("token", token)
        return response

    @app.route("/css/<css_path>", methods=["GET"])
    def css_handler(css_path=""):
        if not os.path.isfile(os.path.join(mydir, "./css/%s" % css_path)):
            response = make_response("404 Not Found")
            response.status = 404
        else:
            response = make_response(open(os.path.join(mydir, "./css/%s" % css_path), encoding="UTF-8").read())
            response.status = 200
            response.headers["Content-type"] = "text/css"
        if request.args.get("token") == token:
            response.set_cookie("token", token)
        return response

    @app.route("/main-control1.html", methods=["get"])
    def mc1_handler():
        if request.args.get("token") != token and request.cookies.get("token") != token:
            return '', 302, [("Location", '/begin?go_url=' + quote("/main-control1.html"))]
        response = make_response(open(os.path.join(mydir, "./html/main-control1.html"), 'r', encoding="UTF-8").read())
        response.headers["Content-type"] = "text/html"
        if request.args.get("token") == token:
            response.set_cookie("token", token)
        return response

    @app.route("/main-control2.html", methods=["get"])
    def mc2_handler():
        if request.args.get("token") != token and request.cookies.get("token") != token:
            return '', 302, [("Location", '/begin?go_url=' + quote("/main-control2.html"))]
        response = make_response(open(os.path.join(mydir, "./html/main-control2.html"), 'r', encoding="UTF-8").read())
        response.headers["Content-type"] = "text/html"
        if request.args.get("token") == token:
            response.set_cookie("token", token)
        return response

    @app.route("/head.html", methods=["get"])
    def head_handler():
        if request.args.get("token") != token and request.cookies.get("token") != token:
            return '', 302, [("Location", '/begin?go_url=' + quote("/head.html"))]
        response = make_response(open(os.path.join(mydir, "./html/head.html"), 'r', encoding="UTF-8").read())
        response.headers["Content-type"] = "text/html"
        if request.args.get("token") == token:
            response.set_cookie("token", token)
        return response

    @app.route("/tree")
    def tree_handler():
        # 这个函数应该会很长，因为这个函数实在是太多功能了，需要动态加载。
        if request.args.get("token") != token and request.cookies.get("token") != token:
            return '', 302, [
                ("Location", '/begin?go_url=' + quote("/tree?path=%s" % quote(request.args.get("path", ""))))]
        path = unquote(request.args.get("path", "")).replace("\\", "/")  # 将反斜杠统一为正斜杠。
        if len(path) > 0:
            if path[0] == '/':
                path = ''.join(list(path)[1:])
        if not os.path.isdir("./" + path):
            return '404 dir not found.', 404
        path_split = path.split("/")
        if path_split[-1] == '':
            del path_split[-1]
        if len(path_split) > 0:
            if path_split[0] == '':
                del path_split[0]
        breadcrumb_code = ""
        if len(path_split) > 0:
            breadcrumb_code += '<ul class="breadcrumb" style="width:60%;"><li><a href="/tree">（根目录）</a></li>'
            for i in range(len(path_split) - 1):
                now_path = ""
                for j in range(i + 1):
                    now_path += "/" + path_split[j]
                breadcrumb_code += '<li><a href="/tree?path=%s">&nbsp;/&nbsp;%s</a></li>' % (now_path, path_split[i])
            breadcrumb_code += '<li class="active">&nbsp;/&nbsp;%s</li>' % path_split[-1]
            breadcrumb_code += "</ul>"
        dir_content = os.listdir("./" + path)
        with open(os.path.join(mydir, "./html/view_files_code_item_tpl.html").replace("\\.", ""),
                  encoding="UTF-8") as fobj:
            view_files_code_item_tpl = fobj.read()
        view_files_code = ""
        if len(path_split) > 0:
            view_files_code += view_files_code_item_tpl.replace("svg-icon", svg_by_type["folder"]).replace("file_name",
                                                                                                           "..（上一级目录）").replace(
                "file_link", 'tree?path=%s' % quote('/'.join(tuple(path_split[:-1]))))
        if len(dir_content) == 0:
            view_files_code += '<li class="list-group-item"><div style="width:100%;height:20px;padding:2px 0px;border:0px;margin:0px;"><a>此文件夹空空如也~</a></div></li>'
        for item in dir_content:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                view_files_code += view_files_code_item_tpl.replace("svg-icon", get_svg(item_path)).replace(
                    "file_name", item).replace("file_link", "tree?path=%s" % quote(item_path))
        for item in dir_content:
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                view_files_code += view_files_code_item_tpl.replace("svg-icon", get_svg(item_path)).replace(
                    "file_name", item).replace("file_link", "see?path=%s\" target=\"_blank" % quote(item_path))
        # 以上两个循环主要是将文件与文件夹做一下区分，文件夹在上。
        return open(os.path.join(mydir, "./html/tree_tpl.html"), "r", encoding="UTF-8").read().replace("{breadcrumb}",
                                                                                                       breadcrumb_code).replace(
            "{view_files}", view_files_code)

    @app.route("/logo/logo.png", methods=["GET"])
    def logo_handler():
        response = make_response(open(os.path.join(mydir, "./logo/logo.png"), "rb").read())
        return response, 200, [("Cache-Control", "public, max-age=86400")]

    @app.route("/logo.ico", methods=["GET"])
    def icon_handler():
        response = make_response(open(os.path.join(mydir, "./logo/logo.ico"), "rb").read())
        return response, 200, [("Cache-Control", "public, max-age=86400"), ("Content-Type", "image/x-icon")]

    # ------------------------------DO POST------------------------------
    @app.route("/rg", methods=["POST"])
    def rg_handler():
        if request.args.get("token") == token:
            response = make_response(json.dumps({"msg": "OK"}))
            response.headers["Content-type"] = "text/json"
            response.status = 200
            response.set_cookie("token", token)
            return response
        else:
            response = make_response(json.dumps({"msg": "The token is not match."}))
            response.headers["Content-type"] = "text/json"
            response.status = 403
            return response

    @app.route("/save", methods=["POST"])  # 保存文件。
    def save_handler():
        if request.cookies.get("token") != token:
            response = make_response(json.dumps({"msg": "The token is not match."}))
            response.headers["Content-type"] = "text/json"
            response.status = 403
            return response
        mode = request.args.get("mode", "w")
        path = unquote(request.args.get("path", ""))
        if not os.path.isfile(os.path.join(workdir, path)):
            response = make_response(json.dumps({"msg": "File not found."}))
            response.headers["Content-type"] = "text/json"
            response.status = 403
            return response
        data = unquote(request.get_data().decode())
        with open(os.path.join(workdir, path), mode, encoding="UTF-8") as fobj:
            fobj.write(data)
        response = make_response(json.dumps({"msg": "Success to save the file."}))
        response.headers["Content-type"] = "text/json"
        response.status = 200
        return response

    @app.route("/close", methods=["POST"])
    def close_handler():
        if request.cookies.get("token") != token:
            response = make_response(json.dumps({"msg": "The token is not match."}))
            response.headers["Content-type"] = "text/json"
            response.status = 403
            return response
        os._exit(0)

    @app.route("/quit", methods=["POST"])
    def quit_handler():
        if request.cookies.get("token") != token:
            response = make_response(json.dumps({"msg": "The token is not match."}))
            response.headers["Content-type"] = "text/json"
            response.status = 403
            return response
        response = make_response()
        response.delete_cookie("token")
        response.status = 200
        return response

    @app.route("/new_file", methods=["POST"])
    def new_file_handler():
        if request.cookies.get("token") != token:
            response = make_response(json.dumps({"msg": "The token is not match."}))
            response.headers["Content-type"] = "text/json"
            response.status = 403
            return response
        if not request.args.get("file_name"):
            response = make_response(json.dumps({"msg": "File name params not found."}))
            response.headers["Content-type"] = "text/json"
            response.status = 403
            return response
        path = request.args.get("path")
        file_name = request.args.get("file_name")
        if os.path.exists(os.path.join(path, file_name)):
            response = make_response(json.dumps({"msg": "File exists already."}))
            response.headers["Content-type"] = "text/json"
            response.status = 403
            return response
        open(os.path.join(path, file_name), "w")
        response = make_response(json.dumps({"msg": "OK"}))
        response.headers["Content-type"] = "text/json"
        response.status = 200
        return response

    @app.route("/new_folder", methods=["POST"])
    def new_folder_handler():
        if request.cookies.get("token") != token:
            response = make_response(json.dumps({"msg": "The token is not match."}))
            response.headers["Content-type"] = "text/json"
            response.status = 403
            return response
        if not request.args.get("folder_name"):
            response = make_response(json.dumps({"msg": "Folder name params not found."}))
            response.headers["Content-type"] = "text/json"
            response.status = 403
            return response
        path = request.args.get("path")
        folder_name = request.args.get("folder_name")
        if os.path.exists(os.path.join(path, folder_name)):
            response = make_response(json.dumps({"msg": "Folder exists already."}))
            response.headers["Content-type"] = "text/json"
            response.status = 403
            return response
        os.mkdir(os.path.join(path, folder_name))
        response = make_response(json.dumps({"msg": "OK"}))
        response.headers["Content-type"] = "text/json"
        response.status = 200
        return response

    @app.route("/rename", methods=["POST"])
    def rename_handler():
        if request.cookies.get("token") != token:
            response = make_response(json.dumps({"msg": "The token is not match."}))
            response.headers["Content-type"] = "text/json"
            response.status = 403
            return response
        if not request.args.get("new_file_name") or not request.args.get("file_name"):
            response = make_response(json.dumps({"msg": "File name or new file name params not found."}))
            response.headers["Content-type"] = "text/json"
            response.status = 403
            return response
        path = request.args.get("path")
        file_name = request.args.get("file_name")
        new_file_name = request.args.get("new_file_name")
        if not os.path.exists(os.path.join(path, file_name)):
            response = make_response(json.dumps({"msg": "File not found."}))
            response.headers["Content-type"] = "text/json"
            response.status = 403
            return response
        if os.path.exists(os.path.join(path, new_file_name)):
            response = make_response(json.dumps({"msg": "New file exists already."}))
            response.headers["Content-type"] = "text/json"
            response.status = 403
            return response
        os.rename(os.path.join(path, file_name), os.path.join(path, new_file_name))
        response = make_response(json.dumps({"msg": "OK"}))
        response.headers["Content-type"] = "text/json"
        response.status = 200
        return response

    # ------------------------------DO GET AND POST------------------------------
    @app.route("/hello", methods=["GET", "POST"])
    def hello_handler():  # 访问这个路径，获得关于PyCheer的信息。
        return "<h1>PyCheer Server</h1><br>Version %s<br>Running on %s" % (get_version(), workdir), 200, {
            "Content-type": "text/html"}

    app.run(host='0.0.0.0', port=int(params['-p']), debug=False)


# 主程序
def main_function():
    if len(sys.argv) < 2:
        print(show_str)
        quit(0)
    else:
        if sys.argv[1] == "run":
            params = {'-p': "1111", "-b": False, "-n": False}
            abbreviations = {'-p': '--port', '-b': '--browser', '-n': '--nogetip'}
            nindex = 2
            while nindex < len(sys.argv):
                if sys.argv[nindex] == '-p' or sys.argv[nindex] == abbreviations['-p']:
                    nindex += 1
                    params['-p'] = sys.argv[nindex]
                elif sys.argv[nindex] == '-b' or sys.argv[nindex] == abbreviations['-b']:
                    params['-b'] = True
                elif sys.argv[nindex] == '-n' or sys.argv[nindex] == abbreviations['-n']:
                    params['-n'] = True
                else:
                    print('"' + sys.argv[nindex] + '" is not available.')
                nindex += 1
            run(params)
        elif sys.argv[1] == 'version':
            print(get_version())
        elif sys.argv[1] == 'help':
            print(help_str)


if __name__ == "__main__":
    main_function()
