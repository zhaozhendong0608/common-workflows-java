# 多语言模板体系说明

> AI 驱动开发平台 - 项目初始化模板库

---

## 📁 目录结构

```
common-workflows-java/
│
├── templates/                          # 多语言模板库
│   │
│   ├── java/                          # Java 项目模板
│   │   ├── kernel-template/           # 项目内核模板（插值）
│   │   │   ├── 00_系统总纲.md         # {{project.name}}
│   │   │   ├── 01_项目全景.md         # {{tech.backend.framework}}
│   │   │   ├── 02_开发规约/
│   │   │   ├── 03_决策日志.md
│   │   │   ├── 04_答疑库.md
│   │   │   ├── 05_项目进度.md
│   │   │   └── 06_业务拓扑.md
│   │   ├── project-config.schema.json  # 配置验证
│   │   └── project-config.example.yml  # 配置示例
│   │
│   ├── python/                        # Python 项目模板
│   │   ├── kernel-template/           # （待创建）
│   │   ├── project-config.schema.json
│   │   └── project-config.example.yml
│   │
│   ├── nodejs/                        # Node.js 项目模板
│   │   ├── kernel-template/           # （待创建）
│   │   ├── project-config.schema.json
│   │   └── project-config.example.yml
│   │
│   └── common/                        # 语言无关通用模板
│       └── workflows/                 # Sentinel Kernel 工作流
│           ├── 00_领航员.md
│           ├── 01_启动自检.md
│           ├── 02_需求雷达.md
│           ├── 03_规约形式化.md
│           └── ...
│
├── scripts/                           # 初始化引擎
│   ├── init-project.py               # 主初始化脚本 ⭐
│   ├── validate-config.py            # 配置验证
│   └── check-placeholders.py         # 占位符检测
│
└── kernel-template/                   # 原始模板（已迁移到 templates/java/）
```

---

## 🎯 设计理念

### 1. 模板化（Template-based）

所有内核文件使用 **Jinja2 插值语法**：

```markdown
# 00_系统总纲.md

**项目名称**: {{project.name}}
**技术栈**: {{tech.backend.framework}} {{tech.backend.version}}

{% for module in modules -%}
- {{module.name}}: {{module.description}}
{% endfor -%}
```

### 2. 配置驱动（Config-driven）

通过 YAML 配置文件驱动项目生成：

```yaml
# project-config.yml
project:
  name: "智明工业数据平台"
  code: "etl-station"
  owner: "张三"

tech:
  backend:
    framework: "Spring Boot"
    version: "2.7.5"
```

### 3. 多语言支持（Multi-language）

每种语言独立模板目录：
- `templates/java/` - Java + Spring Boot + MyBatis
- `templates/python/` - Python + Django/FastAPI
- `templates/nodejs/` - Node.js + Express/Nest.js

### 4. 通用工作流（Common Workflows）

Sentinel Kernel 工作流语言无关：
- 01_启动自检
- 02_需求雷达
- 03_规约形式化
- ...

---

## 🚀 使用流程

### Step 1: 创建配置文件

```bash
# 从示例复制
cp templates/java/project-config.example.yml my-project-config.yml

# 编辑配置
vim my-project-config.yml
```

### Step 2: 运行初始化脚本

```bash
python scripts/init-project.py \
  --config my-project-config.yml \
  --output ./my-new-project \
  --language java
```

### Step 3: 查看生成结果

```bash
my-new-project/
├── project-kernel/              # ✅ 已渲染的项目内核
│   ├── 00_系统总纲.md          # 项目信息已填充
│   ├── 01_项目全景.md          # 技术栈已填充
│   └── ...
├── .hermes/
│   └── workflows/              # ✅ 工作流已复制
├── custom-standards/           # 自定义规范（如有）
└── README.md                   # ✅ 自动生成
```

---

## 📋 配置文件说明

### Java 项目配置

**必填字段**：
```yaml
project:
  name: "项目名称"             # 必填
  code: "project-code"         # 必填，小写+连字符
  owner: "技术负责人"          # 必填

tech:
  backend:
    framework: "Spring Boot"   # 必选
  database:
    type: "MySQL"             # 必选
```

**可选字段**：
```yaml
modules:                      # 业务模块列表
  - name: "用户管理"
    code: "user"
    description: "用户CRUD"

custom:
  coding_standards: "./custom.md"  # 自定义规范
```

### 完整示例

参考：
- `templates/java/project-config.example.yml`
- `templates/python/project-config.example.yml`

---

## 🛠️ 扩展新语言

### 添加 Go 语言支持

1. **创建目录结构**
```bash
mkdir -p templates/go/kernel-template/02_开发规约
```

2. **创建配置 schema**
```bash
vim templates/go/project-config.schema.json
```

3. **创建内核模板**
```bash
# 复制 Java 模板作为基础
cp templates/java/kernel-template/00_系统总纲.md \
   templates/go/kernel-template/

# 修改为 Go 技术栈
vim templates/go/kernel-template/00_系统总纲.md
```

模板示例：
```markdown
# 00_系统总纲.md

**项目名称**: {{project.name}}

## 技术栈
- **语言**: Go {{tech.go_version}}
- **框架**: {{tech.backend.framework}}  # Gin/Echo/Fiber
- **数据库**: {{tech.database.type}}
```

4. **创建示例配置**
```yaml
# templates/go/project-config.example.yml
project:
  name: "示例项目"
  code: "demo"
  language: "go"

tech:
  go_version: "1.21"
  backend:
    framework: "Gin"
  database:
    type: "PostgreSQL"
```

5. **测试**
```bash
python scripts/init-project.py \
  --config templates/go/project-config.example.yml \
  --output ./test-go-project \
  --language go
```

---

## 🎨 模板语法速查

### 变量插值
```jinja2
{{project.name}}              # 简单变量
{{tech.backend.framework}}    # 嵌套对象
{{modules[0].name}}           # 数组索引
```

### 条件渲染
```jinja2
{% if tech.microservices.enabled -%}
微服务架构
{% else -%}
单体架构
{% endif -%}
```

### 循环渲染
```jinja2
{% for module in modules -%}
- {{module.name}}: {{module.description}}
{% endfor -%}
```

### 过滤器
```jinja2
{{project.code | upper}}      # 大写
{{project.code | capitalize}} # 首字母大写
```

---

## 📊 当前状态

| 语言 | 内核模板 | 配置 Schema | 示例配置 | 状态 |
|------|---------|------------|---------|------|
| Java | ✅ | ✅ | ✅ | 完成 |
| Python | ⏳ | ✅ | ⏳ | 进行中 |
| Node.js | ⏳ | ⏳ | ⏳ | 计划中 |
| Go | ⏳ | ⏳ | ⏳ | 计划中 |

---

## 🔄 与原始 kernel-template 的关系

### 迁移说明

原始 `kernel-template/` 目录已迁移为：
- **新位置**: `templates/java/kernel-template/`
- **改造**: 从静态文本改为 Jinja2 模板
- **原目录**: 保留作为向后兼容（暂不删除）

### 使用建议

- **新项目**: 使用 `templates/java/` + `init-project.py`
- **旧项目**: 继续使用原 `kernel-template/` 手动复制

---

## 🎯 下一步计划

1. ✅ 完成 Java 模板化改造
2. ⏳ 完成 Python 内核模板
3. ⏳ 完成 Node.js 内核模板
4. ⏳ 添加自定义规范合并逻辑
5. ⏳ Web UI 集成（表单 → 配置 → 初始化）

---

**最后更新**: 2026-06-24
**维护者**: dongzi
