```
├── .idea/                        # PyCharm IDE 的专属配置文件夹，存储项目的编辑器配置、断点、运行配置等
    └── [...]                     # 具体配置文件（如workspace.xml、misc.xml等）
├── BackEnd/                      # 项目后端核心目录（Django + Python）
    ├── Small_Target/             # Django 项目的主配置包（项目名：Small_Target）
    │   ├── __pycache__/          # Python 编译后的字节码缓存目录，加快代码运行速度（可忽略/加入.gitignore）
    │   │   └── [...]             # 缓存的.pyc/.pyo文件
    │   ├── __init__.py           # 标识该目录为Python包的空文件，使Python能识别并导入该目录下的模块
    │   ├── asgi.py               # Django 的ASGI配置文件，用于支持异步Web服务器（如Daphne）和WebSocket等异步功能
    │   ├── settings.py           # Django 项目核心配置文件：数据库（PostgreSQL）、中间件、应用注册、静态文件路径、跨域等
    │   ├── urls.py               # Django 项目的主路由配置文件，定义后端API接口的URL映射关系（分发到各app的urls）
    │   └── wsgi.py               # Django 的WSGI配置文件，用于部署到传统WSGI服务器（如Gunicorn、uWSGI）
    ├── db.sqlite3                # Django 默认的SQLite数据库文件（你项目实际用PostgreSQL，此文件可删除/忽略）
    └── manage.py                 # Django 项目的核心管理脚本：启动服务、创建app、数据库迁移、创建超级用户等（如python manage.py runserver）
├── Docs/                         # 项目文档目录：需求文档、接口文档、数据库设计文档、部署文档、开发规范等
├── FrontEnd/                     # 项目前端核心目录（Vue3 + Vite）
    ├── Small_Target/             # Vue3 前端项目根目录（项目名：Small_Target）
    │   ├── .vscode/              # VSCode 编辑器的配置文件夹（如插件配置、格式化规则等，PyCharm开发可忽略）
    │   │   └── [...]             # VSCode配置文件（如settings.json）
    │   ├── node_modules/         # 前端依赖包目录：存储package.json中安装的所有npm包（如vue、vue-router、pinia、axios等）
    │   │   └── [...]             # 具体依赖包文件
    │   ├── public/               # 前端静态资源公共目录（不会被Vite编译）：存放favicon.ico、robots.txt、全局静态图片等
    │   │   └── favicon.ico       # 网站的图标文件（浏览器标签页显示的小图标）
    │   ├── src/                  # Vue3 前端源码核心目录
    │   │   ├── router/           # Vue Router 路由配置目录：管理前端页面的路由跳转、路由守卫、懒加载等
    │   │   │   └── index.js      # 路由核心配置文件：定义路由规则（路径、组件、参数等）
    │   │   ├── stores/           # Pinia 状态管理目录（Vue3替代Vuex的方案）：管理全局共享数据
    │   │   │   └── counter.js    # 示例Pinia仓库：存储计数器相关的状态和方法（可根据业务修改/删除）
    │   │   ├── App.vue           # 前端根组件：所有页面的父组件，定义全局布局（如导航栏、页脚、路由出口<router-view>）
    │   │   └── main.js           # Vue3 入口文件：创建Vue应用实例、挂载全局组件、引入路由/Pinia/样式等，挂载到#app
    │   ├── .editorconfig         # 编辑器统一配置文件：定义缩进、换行符、编码等，保证团队开发编辑器行为一致
    │   ├── .gitattributes        # Git 属性配置文件：定义文件的换行符、合并策略等（如文本文件lf，二进制文件binary）
    │   ├── .gitignore            # Git 忽略文件配置：指定不需要提交到Git的文件/目录（如node_modules、__pycache__、venv等）
    │   ├── .prettierrc.json      # Prettier 格式化工具配置文件：定义代码格式化规则（如单引号、行长度、尾逗号等）
    │   ├── README.md             # 前端项目说明文档：安装依赖、启动命令、打包命令、项目结构等
    │   ├── eslint.config.js      # ESLint 代码检查工具配置文件：检测代码语法错误、规范代码风格（如未定义变量、代码格式问题）
    │   ├── index.html            # 前端入口HTML文件：包含Vue挂载点<div id="app"></div>，Vite编译的JS/CSS会自动注入
    │   ├── jsconfig.json         # JavaScript 项目配置文件：定义路径别名、编译目标等，提升IDE的代码提示和跳转能力
    │   ├── package-lock.json     # npm 依赖版本锁定文件：记录安装的每个依赖的精确版本，保证不同环境依赖一致
    │   ├── package.json          # 前端项目核心配置文件：项目名称、版本、脚本命令（dev/build）、依赖包（dependencies/devDependencies）
    │   └── vite.config.js        # Vite 构建工具配置文件：配置开发服务器、打包规则、路径别名、跨域代理（对接后端API）等
    └── package-lock.json         # 可能是前端目录外层误生成的依赖锁定文件（可删除，以Small_Target下的为准）
├── Utils/                        # 项目工具脚本目录：存放通用的辅助脚本（非业务代码）
    └── struct_tree.py            # 生成项目结构树的Python脚本（如你当前提供的结构就是此脚本输出的）
├── venv/                         # Python 虚拟环境目录：隔离项目的Python依赖（如Django、psycopg2（PostgreSQL驱动）等）
    └── [...]                     # 虚拟环境的bin/Scripts、lib、site-packages等目录
├── .gitattributes                # 项目根目录的Git属性配置文件（全局生效，优先级高于前端目录下的）
└── .gitignore                    # 项目根目录的Git忽略文件（全局生效，如忽略venv、.idea、node_modules等）
```


