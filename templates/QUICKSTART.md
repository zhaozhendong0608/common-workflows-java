# 快速开始 - 5 分钟创建新项目

> 使用多语言模板快速初始化项目

---

## 🎯 目标

从零开始，5 分钟内创建一个完整的项目骨架，包含：
- ✅ 项目内核（已填充项目信息）
- ✅ 工作流文件
- ✅ 项目文档
- ✅ Git 仓库

---

## 📋 前置要求

### 必需
- Python 3.8+
- Git

### 可选
```bash
# 安装 Jinja2（模板引擎）
pip install jinja2 pyyaml
```

---

## 🚀 三步创建

### Step 1: 准备配置文件 (2 分钟)

```bash
# 进入模板目录
cd /path/to/common-workflows-java

# 复制配置示例
cp templates/java/project-config.example.yml my-config.yml

# 编辑配置
vim my-config.yml
```

**最小配置**（只改 3 处）：
```yaml
project:
  name: "我的新项目"          # 改这里
  code: "my-project"          # 改这里
  owner: "李四"               # 改这里

tech:
  backend:
    framework: "Spring Boot"
    version: "2.7.5"
  # ... 其他保持默认
```

### Step 2: 运行初始化 (1 分钟)

```bash
# 方式 1: 使用绝对路径
python scripts/init-project.py \
  --config my-config.yml \
  --output ~/projects/my-new-project \
  --language java

# 方式 2: 使用相对路径
python scripts/init-project.py \
  --config my-config.yml \
  --output ./output/my-project \
  --language java
```

**输出示例**：
```
🚀 开始初始化项目...

📋 Step 1/6: 加载配置文件
   ✓ 配置文件: my-config.yml
   ✓ 项目名称: 我的新项目
   ✓ 项目代号: my-project

📁 Step 2/6: 准备输出目录
   ✓ 创建目录: ~/projects/my-new-project

🎨 Step 3/6: 渲染项目内核
   ✓ 00_系统总纲.md
   ✓ 01_项目全景.md
   ✓ 02_开发规约/01_编码规范.md
   ✓ 02_开发规约/02_架构规范.md
   ...
   共渲染 8 个文件

📂 Step 4/6: 复制工作流文件
   ✓ 复制了 9 个工作流文件

📝 Step 5/6: 跳过自定义规范（使用默认）

📄 Step 6/6: 生成项目文档
   ✓ 生成 README.md

============================================================
✅ 项目初始化完成！
============================================================

📂 项目位置: ~/projects/my-new-project
📋 项目内核: ~/projects/my-new-project/project-kernel
🔄 工作流: ~/projects/my-new-project/.hermes/workflows

下一步操作:
  1. cd ~/projects/my-new-project
  2. 查看 project-kernel/00_系统总纲.md
  3. git init && git add . && git commit -m 'chore: 初始化项目'
```

### Step 3: 验证结果 (2 分钟)

```bash
# 进入项目目录
cd ~/projects/my-new-project

# 查看目录结构
tree -L 2

# 查看项目内核
cat project-kernel/00_系统总纲.md

# 初始化 Git
git init
git add .
git commit -m "chore: 初始化项目"
```

---

## 📁 生成的目录结构

```
my-new-project/
├── project-kernel/              # 项目内核（已填充）
│   ├── 00_系统总纲.md          # ✅ 项目信息已填充
│   ├── 01_项目全景.md          # ✅ 技术栈已填充
│   ├── 02_开发规约/
│   │   ├── 01_编码规范.md      # Java 编码规范
│   │   └── 02_架构规范.md      # Spring Boot 架构规范
│   ├── 03_决策日志.md          # ADR 模板
│   ├── 04_答疑库.md            # FAQ 模板
│   ├── 05_项目进度.md          # 任务管理模板
│   └── 06_业务拓扑.md          # 依赖关系模板
│
├── .hermes/                     # Hermes Agent 配置
│   └── workflows/              # Sentinel Kernel 工作流
│       ├── 00_领航员.md
│       ├── 01_启动自检.md
│       ├── 02_需求雷达.md
│       ├── 03_规约形式化.md
│       ├── 04_受控执行.md
│       ├── 05_度量分析.md
│       ├── 06_业务测试.md
│       ├── 07_质量关卡.md
│       └── 08_归档重启.md
│
└── README.md                    # ✅ 项目说明（自动生成）
```

---

## 🎨 高级用法

### 1. 自定义编码规范

**场景**: 团队有自己的编码规范文件

```bash
# 1. 准备自定义规范
cat > my-company-java-style.md <<EOF
# 公司 Java 编码规范

## 命名规范
- 类名: PascalCase
- 方法名: camelCase
...
EOF

# 2. 在配置中引用
vim my-config.yml
```

```yaml
custom:
  coding_standards: "./my-company-java-style.md"  # 添加这行
```

```bash
# 3. 重新初始化
python scripts/init-project.py \
  --config my-config.yml \
  --output ./my-project \
  --language java
```

**结果**:
```
my-project/
├── project-kernel/
│   └── 02_开发规约/
│       ├── 01_编码规范.md         # 默认规范
│       ├── 02_架构规范.md
│       └── 03_自定义规范.md       # ✅ 引用自定义规范
│
└── custom-standards/
    └── custom-coding-standards.md  # ✅ 复制的自定义规范
```

### 2. 添加业务模块

```yaml
modules:
  - name: "用户管理"
    code: "user"
    description: "用户认证、授权、角色管理"
  
  - name: "设备管理"
    code: "device"
    description: "设备接入、配置、监控"
  
  - name: "数据采集"
    code: "collection"
    description: "多协议数据采集与存储"
```

**效果**: `01_项目全景.md` 中会自动生成模块列表和目录结构

### 3. 微服务配置

```yaml
tech:
  microservices:
    enabled: true           # 启用微服务
    registry: "Nacos"       # 注册中心
    gateway: "Spring Cloud Gateway"
    mq: "RabbitMQ"         # 消息队列
```

**效果**: `00_系统总纲.md` 和 `01_项目全景.md` 会渲染微服务架构图

---

## 🌍 多语言示例

### Python + FastAPI

```bash
# 1. 复制 Python 配置示例
cp templates/python/project-config.example.yml python-config.yml

# 2. 编辑
vim python-config.yml

# 3. 初始化
python scripts/init-project.py \
  --config python-config.yml \
  --output ./my-python-api \
  --language python
```

### Node.js + Express

```bash
# （待完成）
python scripts/init-project.py \
  --config node-config.yml \
  --output ./my-node-api \
  --language nodejs
```

---

## 🔍 验证工具

### 检查占位符

```bash
# 检查是否有未填充的占位符
python scripts/check-placeholders.py \
  ~/projects/my-new-project/project-kernel
```

### 验证配置

```bash
# 验证配置文件格式
python scripts/validate-config.py my-config.yml java
```

---

## ❓ 常见问题

### Q1: 如何修改已生成的项目？

**A**: 直接编辑生成的文件即可，或修改配置后重新生成

```bash
# 方式 1: 直接编辑
vim ~/projects/my-new-project/project-kernel/00_系统总纲.md

# 方式 2: 修改配置重新生成（会覆盖）
vim my-config.yml
python scripts/init-project.py --config my-config.yml --output ./my-project --language java
```

### Q2: 生成的项目包含代码吗？

**A**: 不包含。这只是**项目内核**（文档体系），实际代码需要：
- 使用 Spring Initializr 创建 Spring Boot 项目
- 使用 create-vue 创建 Vue 3 前端
- 然后将生成的 `project-kernel/` 和 `.hermes/` 复制过去

### Q3: 能否集成到 CI/CD？

**A**: 可以。在 CI/CD 中添加初始化步骤：

```yaml
# .gitlab-ci.yml
init-project:
  stage: setup
  script:
    - python scripts/init-project.py --config config.yml --output ./project
```

### Q4: 如何在 AI 平台中使用？

**A**: 
1. 用户在 Web UI 填写表单
2. 后端生成 `project-config.yml`
3. 调用 `init-project.py` 初始化
4. 打包下载给用户

---

## 📚 相关文档

- [多语言模板体系说明](./templates/README.md)
- [Java 配置 Schema](./templates/java/project-config.schema.json)
- [模板语法参考](https://jinja.palletsprojects.com/)

---

## 🎯 下一步

初始化完成后：

1. **查看项目内核**
   ```bash
   cat project-kernel/00_系统总纲.md
   ```

2. **开始开发**
   - 按照工作流执行：`/boot` → `/radar` → `/execute`
   - 参考 `.hermes/workflows/`

3. **持续积累**
   - ADR 记录决策 → `03_决策日志.md`
   - FAQ 记录问题 → `04_答疑库.md`
   - 更新进度 → `05_项目进度.md`

---

**祝开发顺利！** 🚀
