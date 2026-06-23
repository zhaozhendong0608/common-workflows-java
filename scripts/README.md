# 自动化脚本

本目录包含项目自动化脚本。

---

## 📜 脚本列表

### init-project-kernel.py ⭐

**功能**: 自动初始化项目内核（project-kernel/）

**使用方法**:
```bash
# 在旧项目中初始化
python scripts/init-project-kernel.py /path/to/your-project

# 示例
python scripts/init-project-kernel.py ~/my-old-project
```

**脚本会自动**:
1. ✅ 检测项目技术栈（Spring Boot, MyBatis, Vue.js 等）
2. ✅ 分析编码风格（命名、注释语言、格式）
3. ✅ 创建 project-kernel/ 目录结构
4. ✅ 生成基础规约文件：
   - 00_系统总纲.md（根据检测结果生成）
   - 01_项目全景.md（复制模板）
   - 02_开发规约/01_编码规范.md（根据风格生成）
   - 02_开发规约/02_架构规范.md（生成标准架构）
   - 03_决策日志/（创建空目录）
   - 04_答疑库.md（复制模板）
   - 05_项目进度.md（复制模板）
   - 06_业务拓扑.md（复制模板）

**输出示例**:
```
🔍 正在分析项目: etl-station

📊 检测技术栈...
  ✅ Maven
  ✅ Spring Boot
  ✅ MyBatis
  ✅ Vue.js
  ✅ Vite

🎨 检测编码风格...
  - 命名风格: 驼峰命名
  - 注释语言: 中文
  - 代码格式: 4空格缩进

📁 创建目录结构...
  ✅ 目录创建完成

📝 生成基础规约...
  ✅ 00_系统总纲.md
  ✅ 01_项目全景.md
  ✅ 02_开发规约/01_编码规范.md
  ✅ 02_开发规约/02_架构规范.md
  ✅ 03_决策日志/README.md
  ✅ 04_答疑库.md
  ✅ 05_项目进度.md
  ✅ 06_业务拓扑.md

============================================================
✅ 项目内核初始化完成！
============================================================

📂 生成位置: /path/to/your-project/project-kernel

📋 后续步骤:
  1. 编辑 00_系统总纲.md，补充项目信息
  2. 检查 02_开发规约/，根据实际情况调整
  3. 提交到 Git:
     git add project-kernel/
     git commit -m 'init: 初始化项目内核'
```

---

### metrics.py

**功能**: 自动度量分析（KVC/SCV）

**使用方法**:
```bash
python scripts/metrics.py /path/to/project
```

**输出**:
- `.agent/metrics/report_{timestamp}.md` - 详细报告
- `.agent/metrics/history.csv` - 历史数据

---

### auto-archive.py

**功能**: 自动归档会话内容

**使用方法**:
```bash
python scripts/auto-archive.py
```

**功能**:
- 提取 SQL 脚本 → `project-kernel/db/migrations/`
- 识别技术讨论 → `project-kernel/03_决策日志/`（ADR 草稿）
- 提取代码片段 → `project-kernel/snippets/`
- 生成会话摘要 → `docs/session_summary_{timestamp}.md`

---

### constraint-check.sh

**功能**: 约束检查

**使用方法**:
```bash
./scripts/constraint-check.sh
```

---

## 🎯 使用场景

### 新项目
```bash
# 1. 创建项目
mkdir new-project && cd new-project
git init

# 2. 初始化内核
python /path/to/common-workflows-java/scripts/init-project-kernel.py .

# 3. 补充信息
vim project-kernel/00_系统总纲.md

# 4. 提交
git add project-kernel/
git commit -m "init: 初始化项目内核"
```

---

### 旧项目
```bash
# 1. 进入项目
cd your-old-project

# 2. 初始化内核（自动分析）
python /path/to/common-workflows-java/scripts/init-project-kernel.py .

# 3. 检查生成的规约
cat project-kernel/00_系统总纲.md
cat project-kernel/02_开发规约/01_编码规范.md

# 4. 根据实际情况调整

# 5. 提交
git add project-kernel/
git commit -m "init: 初始化项目内核"
```

---

## 🔧 依赖要求

### init-project-kernel.py
- Python 3.6+
- 标准库（无需额外依赖）

### metrics.py
- Python 3.6+
- radon, lizard（可选）

### auto-archive.py
- Python 3.6+
- 标准库

---

## 💡 最佳实践

### 初始化后的检查清单

- [ ] 检查 `00_系统总纲.md` - 补充项目目标、团队信息
- [ ] 检查 `02_开发规约/01_编码规范.md` - 确认命名、注释规范
- [ ] 检查 `02_开发规约/02_架构规范.md` - 确认分层架构
- [ ] 补充 `04_答疑库.md` - 添加常见问题
- [ ] 更新 `05_项目进度.md` - 记录当前进度

---

## 📖 相关文档

- [AI 输出规范](../docs/guides/AI输出规范.md)
- [工作流详解](../workflows/)
- [项目内核模板](../kernel-template/)

---

**版本**: v1.2.1  
**更新日期**: 2026-06-23
