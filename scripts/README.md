# 自动化脚本

本目录包含工作流的自动化脚本，用于提高开发效率。

## 📜 脚本清单

### 1. metrics.py - 度量分析脚本
- **语言**: Python 3
- **用途**: 自动计算 KVC（键值一致性）和 SCV（复杂度变化）
- **支持语言**: Java（主要）、Python
- **依赖**: 
  ```bash
  # 推荐：支持 Java 复杂度分析
  pip install lizard
  
  # 可选：Python 复杂度分析
  pip install radon
  ```

**使用方法**:
```bash
# 分析当前项目（自动检测 Java 文件）
python metrics.py .

# 分析指定项目
python metrics.py /path/to/project
```

**复杂度分析优先级**:
1. **lizard**（推荐）- 支持 Java、Python、C/C++、JavaScript 等多种语言
2. **radon** - 仅支持 Python
3. **简易估算** - 基于方法行数估算（无需额外工具）

**输出**:
- `.agent/metrics/report_<timestamp>.md` - 详细报告
- `.agent/metrics/history.csv` - 历史数据

**示例输出**:
```
📊 计算 SCV（复杂度变化）...
✅ 使用 lizard 分析 Java 代码
✅ 分析了 45 个方法
平均圈复杂度: 3.2

🔴 复杂度最高的 5 个方法:
  - processOrder: 12 (OrderService.java)
  - validateUser: 8 (UserService.java)
  - calculatePrice: 7 (PriceService.java)
```

---

### 2. constraint-check.sh - 约束检查脚本
- **语言**: Bash
- **用途**: 自动检查项目是否符合约束清单
- **依赖**: grep, find, awk

**使用方法**:
```bash
# 检查当前项目
./constraint-check.sh .

# 检查指定项目
./constraint-check.sh /path/to/project
```

**检查项**:
- ✅ P0-001: Context Key 格式（`node:{nodeId}`）
- ✅ P0-002: 继承 BaseAlgoComponent
- ✅ P0-003: 使用 @AlgoOperator 注解
- ⚠️  P1-001: 变量驼峰命名
- ⚠️  P1-002: 方法注释完整
- ℹ️  P2-001: 代码风格统一（需 checkstyle）

**退出码**:
- `0` - 检查通过（无 P0 违规）
- `1` - 检查失败（存在 P0 违规）

---

### 3. evidence-gen.sh - Evidence Block 生成器
- **语言**: Bash
- **用途**: 根据流程类型自动生成 Evidence Block 模板
- **依赖**: git（可选）

**使用方法**:
```bash
# 生成精简版
./evidence-gen.sh lite

# 生成标准版
./evidence-gen.sh standard

# 生成完整版
./evidence-gen.sh full

# 指定项目路径
./evidence-gen.sh standard /path/to/project
```

**输出**: 标准输出（可重定向到文件）

**示例**:
```bash
# 生成并保存到文件
./evidence-gen.sh standard > evidence.md
```

---

### 4. auto-archive.py - 自动归档脚本 ⭐ 新增
- **语言**: Python 3
- **用途**: 自动从会话中提取内容并归档到项目
- **依赖**: 无（纯 Python 标准库）

**使用方法**:
```bash
# 1. 保存会话内容到 session.log（复制整个对话）

# 2. 运行归档脚本
python auto-archive.py

# 3. 指定会话文件和项目路径
python auto-archive.py --session-file chat.log --project-root /path/to/project
```

**自动提取**:
- ✅ SQL 脚本（```sql ... ```）→ `project-kernel/db/migrations/`
- ✅ 技术讨论（识别关键词）→ `project-kernel/03_决策日志/` (ADR 草稿)
- ✅ 代码片段（Java/Python/JS/Bash）→ `project-kernel/snippets/`
- ✅ 会话摘要（统计信息）→ `docs/session_summary_<timestamp>.md`

**预期输出**:
```
📦 自动归档系统
============================================================
📂 项目根目录: /path/to/project
📄 会话文件: session.log
📏 会话长度: 5234 字符

🔍 搜索 SQL 脚本...
  ✅ 找到 2 个 SQL 脚本
  📄 已保存: V20260623_143000__session_migration_1.sql

🔍 搜索技术讨论...
  ✅ 找到 3 处技术讨论
  📄 已生成 ADR 草稿: ADR-006-会话讨论_2026-06-23.md

🔍 搜索代码片段...
  ✅ 找到 5 个代码片段
  📄 已保存: 20260623_143000_java_snippet.java

📝 生成会话摘要...
  ✅ 已保存摘要: session_summary_20260623_143000.md

============================================================
✅ 归档完成！
============================================================
```

**后续操作**:
1. 审查自动生成的文件
2. 完善 ADR 草稿
3. 提交到 Git

**何时使用**:
- 在 `08_归档重启` 阶段
- 会话中产生了 SQL 脚本、技术讨论、代码片段
- 需要快速归档会话内容

---

## 🔧 安装依赖

### Python 依赖
```bash
# 安装度量工具
pip install radon lizard

# 或使用 requirements.txt
pip install -r requirements.txt
```

### 系统依赖
```bash
# macOS
brew install grep findutils gawk

# Linux (Ubuntu/Debian)
apt-get install grep findutils gawk

# 可选：代码风格检查
brew install checkstyle  # macOS
apt-get install checkstyle  # Linux
```

---

## 🎯 使用场景

### 场景1：完成代码后自动检查
```bash
# 1. 检查约束
./constraint-check.sh .

# 2. 计算度量
python metrics.py .

# 3. 生成 Evidence
./evidence-gen.sh standard > .agent/evidence.md
```

### 场景2：集成到 Git Hooks
```bash
# 创建 pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# 提交前检查约束
./scripts/constraint-check.sh . || exit 1
EOF

chmod +x .git/hooks/pre-commit
```

### 场景3：集成到 CI/CD
```yaml
# .github/workflows/quality.yml
name: Quality Check

on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: pip install radon lizard
      - name: Constraint check
        run: ./scripts/constraint-check.sh .
      - name: Metrics analysis
        run: python scripts/metrics.py .
```

---

## 🛠️ 自定义配置

### 修改度量阈值
编辑 `metrics.py`:
```python
# 配置
KVC_THRESHOLD = 0.90  # KVC 阈值
SCV_THRESHOLD = 5.0   # SCV 阈值
```

### 修改约束规则
编辑 `constraint-check.sh`:
```bash
# P0 约束检查：Context Key 格式
echo "📋 P0-001: 检查 Context Key 格式（必须为 node:{nodeId}）"
```

---

## 📊 脚本执行流程

### 完整质量检查流程
```
代码完成
  ↓
constraint-check.sh   ← 检查约束合规
  ↓ [通过]
metrics.py            ← 计算度量指标
  ↓
evidence-gen.sh       ← 生成 Evidence
  ↓
手动审查
```

---

## 🐛 常见问题

### Q1: metrics.py 报错 "ModuleNotFoundError: No module named 'radon'"
**A**: 安装依赖
```bash
pip install radon lizard
```

### Q2: constraint-check.sh 没有执行权限
**A**: 添加执行权限
```bash
chmod +x scripts/*.sh
```

### Q3: 如何在 Windows 上运行 .sh 脚本？
**A**: 
1. 使用 Git Bash
2. 使用 WSL (Windows Subsystem for Linux)
3. 手动移植为 .bat 或 .ps1 脚本

---

## 📝 贡献指南

### 添加新脚本
1. 创建脚本文件（Python/Bash）
2. 添加 shebang 行（`#!/usr/bin/env python3` 或 `#!/bin/bash`）
3. 添加使用说明注释
4. 更新本 README

### 脚本命名规范
- 使用小写字母和连字符
- 功能清晰：`<功能>-<动作>.sh`
- 示例：`constraint-check.sh`, `evidence-gen.sh`

---

**维护人**: {MAINTAINER}
**最后更新**: 2026-06-23
