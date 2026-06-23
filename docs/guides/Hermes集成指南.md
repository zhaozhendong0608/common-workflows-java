# Hermes Agent 集成指南

**版本**: v1.2.1  
**更新日期**: 2026-06-23

本文档说明如何将 common-workflows-java 与 Hermes Agent 集成，实现工作流自动化执行。

---

## 🔥 集成价值

### common-workflows-java 提供
- 📋 工作流标准（流程规范）
- 📝 项目内核模板（知识管理）
- ✅ 质量保障体系（度量、测试）

### Hermes Agent 提供
- 🤖 AI 执行引擎（工具调用）
- 💬 对话管理（上下文、会话）
- 🔧 工具集成（终端、文件、搜索等）

### 结合效果
- common-workflows-java 定义"做什么、怎么做"
- Hermes Agent 提供"执行能力"
- **完美互补，实现工作流自动化！**

---

## 🚀 快速集成（5分钟）

### 方式1: 直接使用（最简单）⭐

**无需安装**，直接在 Hermes 中使用：

```bash
# 1. 进入项目目录
cd your-project

# 2. 告诉 Hermes 加载工作流
hermes> 加载 common-workflows-java 工作流标准

# 3. 开始使用
hermes> /boot
hermes> /radar 添加用户导出功能
hermes> ACK
hermes> /execute
```

**Hermes 会自动**:
- 读取工作流规范
- 调用相应工具（terminal, write_file, search_files 等）
- 执行开发任务
- 生成 Evidence Block

---

### 方式2: 创建 Hermes Skill（推荐）

```bash
# 1. 创建 skill 目录
mkdir -p ~/.hermes/skills/sentinel-workflow

# 2. 复制工作流文件
cp -r common-workflows-java/workflows ~/.hermes/skills/sentinel-workflow/

# 3. 在 Hermes 中加载
hermes> skill_view("sentinel-workflow")

# 4. 使用命令
hermes> /boot
hermes> /radar
```

---

## 📂 项目结构选择

### 小白推荐：最小化结构 ⭐

```
your-project/
├── src/
├── pom.xml
└── README.md
```

**无需创建额外文件夹！** Hermes 临时使用工作流。

**适用**:
- 小项目
- 快速验证
- 学习阶段

---

### 进阶推荐：完整结构

```
your-project/
├── src/
├── pom.xml
├── README.md
└── project-kernel/              ← 唯一需要的
    ├── 00_系统总纲.md
    ├── 02_开发规约/
    │   ├── 01_编码规范.md
    │   └── 02_架构规范.md
    ├── 03_决策日志/
    ├── 04_答疑库.md
    └── 05_项目进度.md
```

**只需 project-kernel/ 一个文件夹！**

**优势**:
- ✅ 项目规约持久化
- ✅ ADR 决策记录
- ✅ FAQ 问题库
- ✅ 度量数据追踪

---

## 🎯 使用场景

### 场景1: 自动化开发

```
User: 我想在 User 表增加 email 字段

Hermes:
  1. 自动执行 /boot（加载项目上下文）
  2. 自动执行 /radar（分析需求）
     → 建议: 🟢 精简流程 (30min)
  
  3. 用户确认: ACK
  
  4. 自动执行 /execute
     → write_file: 修改 User.java
     → write_file: 生成 SQL 脚本
     → terminal: mvn test
     → 生成 Evidence Block
     
  5. 自动执行 /quality
     → 检查代码规范 ✅
     → 检查测试覆盖率 ✅
     
  6. 完成！代码已生成，测试已通过
```

---

### 场景2: 智能度量分析

```
User: /measure

Hermes:
  → execute_code: 运行 metrics.py
  → read_file: 读取代码
  → 自动计算 KVC/SCV
  → 生成度量报告
  
  ✅ KVC: 0.93 (达标)
  ✅ SCV: 2.6 (正常)
```

---

### 场景3: 自动归档

```
User: /archive

Hermes:
  → session_search: 提取会话内容
  → 识别技术讨论、SQL 脚本
  → write_file: 创建 ADR
  → 更新 FAQ
  
  ✅ 已归档到 project-kernel/
```

---

## ⚙️ 集成方式对比

| 方式 | 优势 | 适用场景 |
|------|------|---------|
| **直接使用** | 零配置，立即可用 | 小白、小项目 |
| **Hermes Skill** | 命令简洁，自动加载 | 日常开发 |
| **Cron 定时** | 自动执行，无需手动 | 定期度量、归档 |

---

## 🎓 进阶集成

### 1. 创建自定义 Skill

```yaml
# ~/.hermes/skills/sentinel-workflow/SKILL.md
---
name: sentinel-workflow
description: Sentinel Kernel 工作流自动化
trigger_patterns:
  - "/boot"
  - "/radar"
  - "/execute"
---

# Sentinel Workflow

当用户输入 /boot, /radar 等命令时:
1. 加载对应的工作流文件
2. 解析步骤
3. 自动调用 Hermes 工具执行
4. 生成 Evidence Block
```

---

### 2. 定时自动化

```bash
# 每天 9 点自动执行度量分析
hermes cronjob create \
  --schedule "0 9 * * *" \
  --prompt "执行 /measure 度量分析并生成报告" \
  --skills sentinel-workflow
```

---

### 3. 团队协作

```bash
# 多人协作工作流
hermes workflow collaborate \
  --share-with team \
  --notify-on-complete
```

---

## ❓ 常见问题

### Q1: 必须创建 project-kernel/ 吗？

**A**: **不需要！**

- **小白**: 零配置，直接用
- **进阶**: 创建 project-kernel/ 持久化知识

---

### Q2: 每个项目都要复制 workflows/ 吗？

**A**: **不需要！**

- workflows/ 在 Hermes skill 中（全局一次）
- 每个项目只需要 project-kernel/（可选）

---

### Q3: Hermes 会自动执行所有步骤吗？

**A**: **看模式**

- **引导模式**: AI 提示下一步，你确认
- **自动模式**: AI 自动执行完整流程（需配置）

---

### Q4: 如何初始化新项目？

**A**: 

```bash
# 方式1: 最简单
hermes> /boot
# 选择"轻量模式"

# 方式2: 完整模式
hermes> 帮我初始化 Sentinel Kernel 项目结构
# Hermes 自动创建 project-kernel/
```

---

## 🎯 最佳实践

### 小白使用建议

1. **直接用，不建目录**
2. **只记 3 个命令**: /boot, /radar, /execute
3. **跟着 AI 提示走**
4. **不用管 Evidence Block**（AI 自动生成）

---

### 进阶使用建议

1. **创建 project-kernel/**（知识积累）
2. **填写项目规约**（提高准确率）
3. **记录 ADR**（技术决策）
4. **定期执行 /measure**（质量追踪）

---

## 🔗 相关资源

- [Hermes Agent 文档](https://hermes-agent.nousresearch.com/docs)
- [命令速查表](../COMMANDS.md)
- [5分钟快速开始](../快速开始_5分钟版.md)
- [完整 README](../README.md)

---

**版本**: v1.2.1  
**更新日期**: 2026-06-23
