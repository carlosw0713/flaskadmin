from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)

# 创建后台调度器
scheduler = BackgroundScheduler()

# 启动调度器
scheduler.start()

# 注册关闭时清理调度器的钩子
atexit.register(lambda: scheduler.shutdown())

# 存储任务ID和任务映射关系
tasks = {}


@app.route('/add-task', methods=['POST'])
def add_task():
    """
    添加一个新的定时任务。
    入参：
    - cron_expression: Cron表达式，如 '*/5 * * * *' 表示每5分钟执行一次。
    - method_info: 要调用的方法信息（可以是函数名或实际的函数对象）。
    """
    data = request.get_json()

    cron_expression = data.get('cron_expression')
    method_info = data.get('method_info')

    if not cron_expression or not method_info:
        return jsonify({"error": "Missing required fields"}), 400

    # 解析Cron表达式
    try:
        second, minute, hour, day, month, day_of_week = cron_expression.split()
    except ValueError:
        return jsonify({"error": "Invalid cron expression format"}), 400

    # 假设method_info是一个字符串形式的函数名
    if isinstance(method_info, str):
        func = globals().get(method_info)
        if not callable(func):
            return jsonify({"error": "Method not found or not callable"}), 400
    else:
        func = method_info

    # 创建任务ID
    task_id = f"task_{len(tasks) + 1}"

    # 添加任务到调度器
    scheduler.add_job(
        func=func,
        trigger='cron',
        second=second,
        minute=minute,
        hour=hour,
        day=day,
        month=month,
        day_of_week=day_of_week,
        id=task_id
    )

    # 记录任务
    tasks[task_id] = {
        'cron_expression': cron_expression,
        'method_info': method_info
    }

    return jsonify({"message": "Task added successfully", "task_id": task_id}), 201


# 示例方法：打印当前时间
def print_current_time():
    from datetime import datetime
    print(f"Current time is {datetime.now()}")


# 示例路由：用于测试
@app.route('/')
def index():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True)