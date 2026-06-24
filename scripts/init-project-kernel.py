#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 项目内核初始化脚本

自动分析项目，生成 kernel-template/ 目录和基础规约
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime


def detect_tech_stack(project_dir):
    """检测项目技术栈"""
    tech_stack = []
    
    # 检测 Java
    if (Path(project_dir) / "pom.xml").exists():
        tech_stack.append("Maven")
        # 读取 pom.xml 检测框架
        try:
            with open(Path(project_dir) / "pom.xml", 'r', encoding='utf-8') as f:
                content = f.read()
                if 'spring-boot' in content:
                    tech_stack.append("Spring Boot")
                if 'mybatis' in content:
                    tech_stack.append("MyBatis")
        except:
            pass
    
    if (Path(project_dir) / "build.gradle").exists():
        tech_stack.append("Gradle")
    
    # 检测前端
    if (Path(project_dir) / "package.json").exists():
        try:
            with open(Path(project_dir) / "package.json", 'r', encoding='utf-8') as f:
                pkg = json.load(f)
                deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                if 'vue' in deps:
                    tech_stack.append("Vue.js")
                if 'react' in deps:
                    tech_stack.append("React")
                if 'vite' in deps:
                    tech_stack.append("Vite")
        except:
            pass
    
    # 检测数据库
    sql_files = list(Path(project_dir).rglob("*.sql"))
    if sql_files:
        tech_stack.append("SQL Database")
    
    return tech_stack


def detect_coding_style(project_dir):
    """检测编码风格"""
    style = {
        "命名风格": "未知",
        "注释语言": "未知",
        "代码格式": "未知"
    }
    
    # 检测 Java 文件
    java_files = list(Path(project_dir).rglob("*.java"))[:5]  # 只检查前5个
    
    if java_files:
        # 检测注释语言
        chinese_comments = 0
        english_comments = 0
        
        for java_file in java_files:
            try:
                with open(java_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 检测中文注释
                    if any('\u4e00' <= c <= '\u9fff' for c in content):
                        chinese_comments += 1
                    else:
                        english_comments += 1
            except:
                pass
        
        if chinese_comments > english_comments:
            style["注释语言"] = "中文"
        else:
            style["注释语言"] = "英文"
        
        # 检测命名风格（驼峰）
        style["命名风格"] = "驼峰命名"
        style["代码格式"] = "4空格缩进"
    
    return style


def generate_system_overview(project_dir, project_name, tech_stack):
    """生成系统总纲"""
    return f"""# {project_name} - 系统总纲

**创建日期**: {datetime.now().strftime('%Y-%m-%d')}  
**维护人**: {{YOUR_NAME}}  
**版本**: v1.0.0

---

## 项目简介

{project_name} 是一个 [项目简介，请补充]

---

## 技术栈

### 后端
{chr(10).join(f'- {tech}' for tech in tech_stack if tech in ['Maven', 'Gradle', 'Spring Boot', 'MyBatis'])}

### 前端
{chr(10).join(f'- {tech}' for tech in tech_stack if tech in ['Vue.js', 'React', 'Vite'])}

### 数据库
{chr(10).join(f'- {tech}' for tech in tech_stack if tech in ['SQL Database'])}

---

## 项目目标

[请补充项目目标]

---

## 团队信息

- **团队规模**: [请补充]
- **开发模式**: [请补充]
- **协作方式**: [请补充]

---

## 项目结构

```
{project_name}/
├── src/                  # 源代码
├── docs/                 # 文档
├── scripts/              # 脚本
└── kernel-template/       # 项目内核（本目录）
```

---

**注意**: 本文件由 AI 自动生成，请根据实际情况补充完善。
"""


def generate_coding_rules(style):
    """生成编码规范"""
    return f"""# 编码规范

**版本**: v1.0.0  
**更新日期**: {datetime.now().strftime('%Y-%m-%d')}

---

## 命名规范

### 类名
- 使用 `PascalCase`（大驼峰）
- 示例: `UserService`, `OrderController`

### 方法名
- 使用 `camelCase`（小驼峰）
- 示例: `getUserById()`, `saveOrder()`

### 变量名
- 使用 `camelCase`
- 示例: `userName`, `orderId`

### 常量
- 使用 `UPPER_SNAKE_CASE`
- 示例: `MAX_SIZE`, `DEFAULT_TIMEOUT`

---

## 注释规范

### 类注释
```java
/**
 * 用户服务类
 * 
 * @author {{YOUR_NAME}}
 * @date {datetime.now().strftime('%Y-%m-%d')}
 */
public class UserService {{
}}
```

### 方法注释
```java
/**
 * 根据ID获取用户
 * 
 * @param id 用户ID
 * @return 用户信息
 */
public User getUserById(Long id) {{
}}
```

### 注释语言
- **使用 {style["注释语言"]}**

---

## 代码格式

### 缩进
- 使用 **{style["代码格式"]}**

### 括号
- 左括号不换行
- 右括号单独一行

### 空格
- 运算符两侧留空格
- 逗号后留空格

---

## 日志规范

### 日志级别
- `ERROR`: 错误
- `WARN`: 警告
- `INFO`: 信息
- `DEBUG`: 调试

### 日志格式
```java
log.info("用户登录成功: userId={{}}", userId);
log.error("查询失败: {{}}", e.getMessage(), e);
```

---

## 异常处理

### 统一异常
```java
throw new BusinessException("用户不存在");
```

### 捕获异常
```java
try {{
    // 业务逻辑
}} catch (Exception e) {{
    log.error("操作失败", e);
    throw new BusinessException("操作失败");
}}
```

---

**注意**: 本文件由 AI 自动生成，请根据实际情况补充完善。
"""


def generate_architecture_rules():
    """生成架构规范"""
    return f"""# 架构规范

**版本**: v1.0.0  
**更新日期**: {datetime.now().strftime('%Y-%m-%d')}

---

## 分层架构

```
Controller 层
    ↓
Service 层
    ↓
Mapper/DAO 层
    ↓
Database
```

### Controller 层
- 负责接收请求、参数校验
- 调用 Service 层
- 返回统一响应格式

### Service 层
- 负责业务逻辑
- 事务管理
- 调用 Mapper 层

### Mapper 层
- 负责数据访问
- SQL 操作
- 对象映射

---

## 依赖规则

### 允许
- ✅ Controller → Service → Mapper
- ✅ Service → Service (同级调用)

### 禁止
- ❌ Controller 直接访问 Mapper
- ❌ Mapper 调用 Service
- ❌ 循环依赖

---

## 模块划分

### 核心模块
- [请根据项目补充]

### 通用模块
- common: 通用工具
- config: 配置
- exception: 异常处理

---

## API 规范

### RESTful API
```
GET    /api/users         # 查询列表
GET    /api/users/:id     # 查询详情
POST   /api/users         # 创建
PUT    /api/users/:id     # 更新
DELETE /api/users/:id     # 删除
```

### 响应格式
```json
{{
  "code": 0,
  "msg": "success",
  "data": {{}}
}}
```

---

**注意**: 本文件由 AI 自动生成，请根据实际情况补充完善。
"""


def init_project_kernel(project_dir, template_dir):
    """初始化项目内核"""
    project_dir = Path(project_dir)
    template_dir = Path(template_dir)
    kernel_dir = project_dir / "kernel-template"
    
    # 检测项目名称
    project_name = project_dir.name
    
    print(f"🔍 正在分析项目: {project_name}")
    print()
    
    # 检测技术栈
    print("📊 检测技术栈...")
    tech_stack = detect_tech_stack(project_dir)
    if tech_stack:
        for tech in tech_stack:
            print(f"  ✅ {tech}")
    else:
        print("  ⚠️  未检测到明确的技术栈")
    print()
    
    # 检测编码风格
    print("🎨 检测编码风格...")
    style = detect_coding_style(project_dir)
    for key, value in style.items():
        print(f"  - {key}: {value}")
    print()
    
    # 创建目录结构
    print("📁 创建目录结构...")
    kernel_dir.mkdir(exist_ok=True)
    (kernel_dir / "02_开发规约").mkdir(exist_ok=True)
    (kernel_dir / "03_决策日志").mkdir(exist_ok=True)
    (kernel_dir / "db" / "migrations").mkdir(parents=True, exist_ok=True)
    print("  ✅ 目录创建完成")
    print()
    
    # 生成文件
    print("📝 生成基础规约...")
    
    # 00_系统总纲.md
    with open(kernel_dir / "00_系统总纲.md", 'w', encoding='utf-8') as f:
        f.write(generate_system_overview(project_dir, project_name, tech_stack))
    print("  ✅ 00_系统总纲.md")
    
    # 01_项目全景.md（复制模板）
    if (template_dir / "01_项目全景.md").exists():
        with open(template_dir / "01_项目全景.md", 'r', encoding='utf-8') as f:
            content = f.read()
        with open(kernel_dir / "01_项目全景.md", 'w', encoding='utf-8') as f:
            f.write(content)
        print("  ✅ 01_项目全景.md")
    
    # 02_开发规约/01_编码规范.md
    with open(kernel_dir / "02_开发规约" / "01_编码规范.md", 'w', encoding='utf-8') as f:
        f.write(generate_coding_rules(style))
    print("  ✅ 02_开发规约/01_编码规范.md")
    
    # 02_开发规约/02_架构规范.md
    with open(kernel_dir / "02_开发规约" / "02_架构规范.md", 'w', encoding='utf-8') as f:
        f.write(generate_architecture_rules())
    print("  ✅ 02_开发规约/02_架构规范.md")
    
    # 其他文件（复制模板）
    template_files = [
        "04_答疑库.md",
        "05_项目进度.md",
        "06_业务拓扑.md"
    ]
    
    for file_name in template_files:
        src = template_dir / file_name
        dst = kernel_dir / file_name
        if src.exists():
            with open(src, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {file_name}")
    
    # 创建空的决策日志目录说明
    with open(kernel_dir / "03_决策日志" / "README.md", 'w', encoding='utf-8') as f:
        f.write(f"""# 决策日志

本目录存放 ADR (Architecture Decision Record) 决策记录。

## 命名规则

`ADR-{{编号}}-{{标题}}.md`

示例: `ADR-001-缓存方案选型.md`

## 模板

参考: `../templates/adr-template.md`

---

**创建日期**: {datetime.now().strftime('%Y-%m-%d')}
""")
    print("  ✅ 03_决策日志/README.md")
    
    print()
    print("=" * 60)
    print("✅ 项目内核初始化完成！")
    print("=" * 60)
    print()
    print("📂 生成位置:", kernel_dir)
    print()
    print("📋 后续步骤:")
    print("  1. 编辑 00_系统总纲.md，补充项目信息")
    print("  2. 检查 02_开发规约/，根据实际情况调整")
    print("  3. 提交到 Git:")
    print("     git add kernel-template/")
    print("     git commit -m 'init: 初始化项目内核'")
    print()


def main():
    if len(sys.argv) < 2:
        print("用法: python init-kernel-template.py <项目目录>")
        print("示例: python init-kernel-template.py /path/to/your-project")
        sys.exit(1)
    
    project_dir = sys.argv[1]
    
    # 获取 template 目录
    script_dir = Path(__file__).parent
    template_dir = script_dir.parent / "kernel-template"
    
    if not template_dir.exists():
        print(f"❌ 模板目录不存在: {template_dir}")
        sys.exit(1)
    
    if not Path(project_dir).exists():
        print(f"❌ 项目目录不存在: {project_dir}")
        sys.exit(1)
    
    init_project_kernel(project_dir, template_dir)


if __name__ == "__main__":
    main()
