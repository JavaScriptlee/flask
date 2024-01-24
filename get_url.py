import re
import psutil
import subprocess
from time import sleep
from os.path import exists
from flask import Flask, render_template, request, jsonify

import logging

def create_app():
    app = Flask(__name__)

    def get_user_input(data):
        secret_key = str(data.get('secret_key'))
        user_url = data.get('user_url')
        return secret_key, user_url

    def is_process_running(process_name):
        for proc in psutil.process_iter(['pid', 'cmdline']):
            try:
                if isinstance(proc.info['cmdline'], (list, tuple)):
                    cmdline = " ".join(map(str, proc.info['cmdline']))
                else:
                    cmdline = str(proc.info['cmdline'])
            
                if re.search(rf'\b{re.escape(process_name)}\b', cmdline):
                    return "恭喜！正在保活中！"
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass  # Handle exceptions if process no longer exists or access is denied
        return "哦No！ 你的项目没有执行保活！"


    def terminate_process_by_name(process_name):
        try:
            subprocess.run(["pkill", "-f", process_name])
            return f"进程 {process_name} 已成功终止！"
        except Exception as e:
            return f"无法终止进程 {process_name}，发生错误： {str(e)}"

    # 设置日志级别
    logging.basicConfig(level=logging.DEBUG)

    @app.route('/')
    def index_html():
        return render_template('index.html')

    @app.route('/add_url', methods=['POST'])
    def add_url():
        data = request.get_json()
        secret_key, user_url = get_user_input(data)

        if exists('./users/' + secret_key):
            with open(f'./users/{secret_key}/url_list.txt', "a+") as url_lit:
                url_lit.write(user_url + "\n")
                message = f"添加链接成功！！"
                return jsonify({"message": message})
        else:
            message = "！！无效密钥！！"
            return jsonify({"message": message})

    @app.route('/del_url', methods=['POST'])
    def del_url():
        data = request.get_json()
        secret_key, user_url = get_user_input(data)

        if exists('./users/' + secret_key):
            try:
                with open(f'./users/{secret_key}/url_list.txt', "r") as url_lit:
                    urls = url_lit.readlines()
                with open(f'./users/{secret_key}/url_list.txt', "w") as url_lit:
                    if user_url + "\n" not in urls:
                        url_lit.write("\n".join(urls))
                        return jsonify({"message": "链接原本就不在列表内！"})
                    else:
                        urls.remove(user_url + "\n")
                        url_lit.write("\n".join(urls))
                        return jsonify({"message": "删除成功。"})
            except (FileNotFoundError, IOError) as e:
                return jsonify({"message": f"删除时出现异常！{e}"})
        else:
            return jsonify({"message": "！！无效密钥！！"})

    @app.route('/show_all', methods=['POST'])
    def show_all():
        data = request.get_json()
        secret_key, _ = get_user_input(data)

        if exists('./users/' + secret_key):
            try:
                with open(f'./users/{secret_key}/url_list.txt') as url_lit:
                    urls = url_lit.read()
                    return jsonify({"message": f'{urls}'})
            except (FileNotFoundError, IOError) as e:
                return jsonify({f"message": f"读取时出现异常！{e}"})
        else:
            return jsonify({"message": "！！无效密钥！！"})

    @app.route('/run_shell', methods=['POST'])
    def run_shell():
        data = request.get_json()
        secret_key, _ = get_user_input(data)

        if exists('./users/' + secret_key):
            process_name = f'get_{secret_key.split("-")[0]}.sh'
            sh_exist = is_process_running(process_name)

            if "恭喜" not in sh_exist:
                try:
                    subprocess.Popen(['sh', f'./users/{secret_key}/{process_name}'])
                    sleep(1)
                    app.logger.info("成功执行启动命令，请手动查看保活状态！")
                    return jsonify({"message": "已执行启动命令，请手动查看保活状态！！"})
                except Exception as e:
                    app.logger.error(f"启动命令失败：{e}")
                    return jsonify({"message": f"启动命令失败：{e}"})
            else:
                app.logger.info("请手动停止保活一下，再来启动！！")
                return jsonify({"message": "请手动停止保活一下，再来启动！！"})

    @app.route('/kill_baohuo', methods=['POST'])
    def kill_baohuo():
        data = request.get_json()
        secret_key, _ = get_user_input(data)

        if exists('./users/' + secret_key):
            process_name = f'get_{secret_key.split("-")[0]}.sh'
            message = terminate_process_by_name(process_name)
            app.logger.info(f"成功执行终止命令：{message}")
            return jsonify({"message": f"{message}"})
        else:
            return jsonify({"message": "！！无效密钥！！"})

    @app.route('/status_baohuo', methods=['POST'])
    def status_baohuo():
        data = request.get_json()
        secret_key, _ = get_user_input(data)

        if exists('./users/' + secret_key):
            process_name = f'get_{secret_key.split("-")[0]}.sh'
            ok_no = is_process_running(process_name)
            app.logger.info(f"查询保活状态：{ok_no}")
            return jsonify({"message": f"{ok_no}"})
        else:
            return jsonify({"message": "！！无效密钥！！"})

    return app

# if __name__ == "__main__":
#     app = create_app()
#     app.run(host='0.0.0.0', port=5000, debug=True)
