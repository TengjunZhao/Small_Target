```
Small_Target/
├── .git/                          # Git版本控制目录
├── .gitattributes                 # Git属性配置文件
├── .gitignore                     # Git忽略文件配置
├── BackEnd/                       # Django后端项目
│   ├── Small_Target/             # Django项目主目录
│   │   ├── __init__.py           # Python包初始化文件
│   │   ├── asgi.py               # ASGI配置文件
│   │   ├── settings.py           # Django设置文件
│   │   ├── urls.py               # 主URL路由配置
│   │   └── wsgi.py               # WSGI配置文件
│   ├── kana/                     # 50音练习Django应用
│   │   ├── __init__.py           # Python包初始化文件
│   │   ├── admin.py              # Django管理后台配置
│   │   ├── apps.py               # 应用配置文件
│   │   ├── migrations/           # 数据库迁移文件目录
│   │   │   ├── 0001_initial.py   # 初始模型迁移
│   │   │   ├── 0002_auto_20260204_1043.py  # 数据初始化迁移
│   │   │   └── __init__.py       # 迁移包初始化
│   │   ├── models.py             # 数据模型定义
│   │   ├── tests.py              # 单元测试文件
│   │   ├── urls.py               # 应用URL路由
│   │   └── views.py              # 视图函数
│   └── manage.py                 # Django管理命令行工具
├── Docs/                         # 项目文档目录
│   └── readme.md                 # 项目说明文档
├── FrontEnd/                     # Vue.js前端项目
│   ├── Small_Target/            # Vite项目根目录
│   │   ├── .editorconfig        # 编辑器配置文件
│   │   ├── .gitattributes       # Git属性配置
│   │   ├── .gitignore           # Git忽略配置
│   │   ├── .prettierrc.json     # Prettier代码格式化配置
│   │   ├── .vscode/             # VSCode配置目录
│   │   │   └── extensions.json  # 推荐VSCode扩展
│   │   ├── README.md            # 项目说明文件
│   │   ├── eslint.config.js     # ESLint配置文件
│   │   ├── index.html           # HTML入口文件
│   │   ├── jsconfig.json        # JavaScript配置文件
│   │   ├── node_modules/        # Node.js依赖包目录
│   │   ├── package-lock.json    # npm锁定文件
│   │   ├── package.json         # npm包配置文件
│   │   ├── public/              # 静态资源目录
│   │   │   └── favicon.ico      # 网站图标
│   │   ├── src/                 # Vue源代码目录
│   │   │   ├── App.vue          # 根Vue组件
│   │   │   ├── assets/          # 静态资源目录
│   │   │   │   └── main.css     # 全局CSS样式文件
│   │   │   ├── main.js          # Vue应用入口文件
│   │   │   ├── router/          # Vue路由配置
│   │   │   │   └── index.js     # 路由定义文件
│   │   │   ├── stores/          # Pinia状态管理
│   │   │   │   └── counter.js   # 计数器store
│   │   │   └── views/           # 页面组件目录
│   │   │       ├── Home.vue     # 首页组件
│   │   │       └── KanaPractice.vue  # 50音练习页面
│   │   └── vite.config.js       # Vite构建配置
│   └── package-lock.json        # 前端npm锁定文件
└── Utils/                        # 工具脚本目录
    └── struct_tree.py           # 项目结构树生成工具
```

push test
