# actionsystem
从课程选择开始的动作训练系统
# 目录结构
```
.
├── 动作数据库表单.docx
├── add_student.py
├── auxiliary_tools 各种工具类，主要进程函数
│   ├── action_model
│   │   ├── action_rec.py 用于读取配置文件返回动作识别主类Processor
│   │   ├── configs
│   │   ├── __init__.py
│   │   ├── model 存放模型文件
│   │   └── src 模型源码，包含数据处理以及网络架构
│   ├── bvh_process.py bvh数据解析用
│   ├── camera_tools.py 双目姿态估计使用
│   ├── count_main 动作计数相关文件
│   │   ├── checkpoints
│   │   ├── count.py
│   │   ├── __init__.py
│   │   ├── pytorch-image-models 存放resnet50v2
│   │   ├── repnet
│   │   └── run.py
│   ├── database_operation.py 数据库操作
│   ├── __init__.py
│   ├── key_frame.py 
│   ├── processtest.py 多进程相关
│   ├── skeleton_judge.py
│   ├── skeleton_process 双目姿态估计相关，已弃用
│   └── threadtest.py 多线程相关，已弃用
├── data
│   ├── a.mp4
│   ├── bvh 处理传感器数据需要的bvh文件
│   │   ├── 真实.bvh
│   │   ├── a.txt
│   │   └── test.bvh
│   ├── course_action 课程视频存放路径
│   │   ├── response
│   │   └── std
│   ├── dbconfig 数据库配置以及和后端连接配置
│   ├── empty.png
│   ├── score_matrix.txt 动作反应评分配置
│   ├── sensor
│   │   └── config.json 传感器配置文件
│   └── wait.png
├── main1.py 直接进入训练界面
├── main.py 从课程选择开始
├── main.spec 打包配置文件
├── README.md
├── remove.py 打包过程中用于移除多余的qt文件
├── res_rc.py 图片资源文件，由qurc生成
├── test.bat  打包bat脚本，一键式处理
└── widgets
    ├── action_eval_main.py 跟随训练
    ├── action_follow_main.py 动作讲解
    ├── action_select_main.py 动作选择
    ├── center_menu_main.py 大菜单
    ├── figs 存放图片资源
    ├── Grade_main.py 成绩
    ├── __init__.py
    ├── lessons_select_main.py 课程选择
    ├── login_main.py 登录，已弃用
    ├── login_window.py 登录，已弃用
    ├── reaction_train_contral.py 动作反应训练控制类
    ├── reaction_train_main.py 动作反应训练
    ├── res.qrc 资源文件
    ├── res_rc.py 资源文件，由qurc生成，和外部的是一个文件
    ├── setting_main.py 设置
    ├── Std_show_main.py 规范训练结果展示
    ├── std_train_select_main.py 规范训练模式选择
    └── ui
