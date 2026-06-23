# AI 输出规范

本文档定义 AI 执行工作流时，各类文件的输出位置。

---

## 📂 目录规范

### 临时文件（不提交 Git）

```
.agent/                           # AI 临时输出
├── metrics/                      # 度量报告
│   ├── report_20260623_143000.md
│   └── history.csv
├── sessions/                     # 会话记录
│   └── session_20260623_143000.md
└── temp/                         # 临时文件
    └── *.tmp
```

**特点**:
- ✅ 本地生成，不提交 Git
- ✅ 可随时删除重新生成
- ✅ 已添加到 .gitignore

---

### 持久化文件（提交 Git）

```
project-kernel/                   # 项目知识库
├── 03_决策日志/                 # ADR 决策记录
│   ├── ADR-001.md
│   └── ADR-002.md
├── 04_答疑库.md                 # FAQ 问题库
├── 05_项目进度.md               # 项目进度
└── db/migrations/               # SQL 迁移脚本
    └── V20260623__*.sql
```

**特点**:
- ✅ 持久化知识
- ✅ 团队共享
- ✅ 提交到 Git

---

## 🤖 AI 输出指令

### 度量报告

```bash
# AI 执行 /measure 时
输出位置: .agent/metrics/report_{timestamp}.md
追加历史: .agent/metrics/history.csv

# 示例
.agent/metrics/report_20260623_143000.md
.agent/metrics/history.csv
```

---

### 会话记录

```bash
# AI 执行 /archive 时
输出位置: .agent/sessions/session_{timestamp}.md

# 示例
.agent/sessions/session_20260623_143000.md
```

---

### ADR 决策记录

```bash
# AI 识别到技术决策时
输出位置: project-kernel/03_决策日志/ADR-{number}-{title}.md

# 示例
project-kernel/03_决策日志/ADR-006-缓存方案选型.md
```

---

### SQL 迁移脚本

```bash
# AI 生成 SQL 时
输出位置: project-kernel/db/migrations/V{timestamp}__{description}.sql

# 示例
project-kernel/db/migrations/V20260623_143000__add_user_email.sql
```

---

### FAQ 更新

```bash
# AI 识别到常见问题时
追加到: project-kernel/04_答疑库.md

# 格式
### Q: {问题}
**A**: {答案}
**相关**: ADR-{编号}, {文件路径}
**添加时间**: {日期}
```

---

### Evidence Block

```bash
# AI 执行 /execute 后
# 精简版: 输出到终端（不保存）
# 标准版: 输出到终端（不保存）
# 完整版: 保存到 .agent/evidence/evidence_{timestamp}.md

# 示例
.agent/evidence/evidence_20260623_143000.md
```

---

## 📋 AI 行为规范

### 何时输出到 .agent/

- ✅ 度量报告（每次 /measure）
- ✅ 会话记录（每次 /archive 自动模式）
- ✅ 临时文件（中间结果）

### 何时输出到 project-kernel/

- ✅ ADR 决策（重要技术决策）
- ✅ SQL 脚本（数据库变更）
- ✅ FAQ 更新（常见问题）
- ✅ 项目进度（阶段性更新）

### 何时不保存文件

- ✅ Evidence Block（精简版、标准版）
- ✅ 中间分析结果
- ✅ 临时验证数据

---

## 🎯 AI 提示示例

### 执行度量分析

```
User: /measure

AI: 开始度量分析...
    
    📊 度量结果
    - KVC: 0.93 (达标)
    - SCV: 2.6 (正常)
    
    ✅ 报告已保存: .agent/metrics/report_20260623_143000.md
    ✅ 历史已追加: .agent/metrics/history.csv
```

---

### 执行归档

```
User: /archive

AI: 开始归档...
    
    识别到:
    - 1 个技术决策 → ADR-006
    - 2 个 SQL 脚本
    - 3 个 FAQ 条目
    
    ✅ ADR 已创建: project-kernel/03_决策日志/ADR-006-缓存方案选型.md
    ✅ SQL 已保存: project-kernel/db/migrations/V20260623_143000__add_cache.sql
    ✅ FAQ 已更新: project-kernel/04_答疑库.md
    ✅ 会话已归档: .agent/sessions/session_20260623_143000.md
```

---

## ⚙️ 配置文件

### .gitignore

```gitignore
# AI 临时输出目录（不提交）
.agent/

# 其他
.DS_Store
*.log
*.tmp
```

---

## 📖 相关文档

- [工作流详解](../workflows/)
- [度量分析详细指南](../workflows/details/05_度量分析_详细指南.md)
- [归档重启自动化指南](../workflows/details/08_归档重启_自动化指南.md)

---

**版本**: v1.2.1  
**更新日期**: 2026-06-23
