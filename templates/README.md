# 模板文件

本目录包含工作流中使用的各类模板文件。

## 📄 模板清单

### 1. constraint-checklist-template.md - 约束清单模板
- **用途**: 在 `03_规约形式化` 阶段生成约束清单
- **包含内容**:
  - P0 约束（强制 - Must）
  - P1 约束（建议 - Should）
  - P2 约束（可选 - Could）
  - FSM 状态序列
  - 人工检查清单

**使用方法**:
1. 复制模板到项目的 `.agent/constraint-checklist.yml`
2. 根据项目实际情况填充内容
3. 在 `04_受控执行` 阶段逐项检查

---

### 2. adr-template.md - ADR 架构决策记录模板
- **用途**: 记录重要的架构决策
- **包含内容**:
  - 背景 (Context)
  - 决策 (Decision)
  - 备选方案 (Alternatives)
  - 后果 (Consequences)
  - 实施细节 (Implementation)

**使用方法**:
1. 在做出重要架构决策时，复制模板
2. 命名：`ADR-{编号}-{简短标题}.md`
3. 保存到项目的 `kernel-template/03_决策日志/`

**命名示例**:
- `ADR-001-选择Redis作为缓存.md`
- `ADR-002-采用微服务架构.md`

---

### 3. evidence-block-template.md - Evidence Block 模板
- **用途**: 在 `04_受控执行` 阶段生成 Evidence Block
- **包含内容**:
  - 🟢 精简版（5 字段）- 小改动
  - 🟡 标准版（8 字段）- 新增功能
  - 🔴 完整版（20 字段）- 架构变更

**使用方法**:
1. 根据流程类型选择对应深度
2. 复制模板并填充实际值
3. 或使用脚本自动生成：`./scripts/evidence-gen.sh <lite|standard|full>`

---

## 🎯 使用场景

### 场景1：开始新任务
```
1. 执行 02_需求雷达
2. 根据分流建议确定流程类型
3. 执行 03_规约形式化
   → 使用 constraint-checklist-template.md 生成约束清单
4. 执行 04_受控执行
   → 使用 evidence-block-template.md 生成 Evidence
```

### 场景2：重大架构决策
```
1. 讨论架构方案
2. 使用 adr-template.md 记录决策
3. 保存到 kernel-template/03_决策日志/
4. 在 Evidence Block 中引用 ADR 编号
```

### 场景3：项目初始化
```
1. 复制所有模板到项目
2. 根据项目特点调整模板内容
3. 团队评审并达成共识
4. 作为项目标准使用
```

---

## 📝 模板使用指南

### 1. 复制模板
```bash
# 复制约束清单模板
cp templates/constraint-checklist-template.md .agent/constraint-checklist.md

# 复制 ADR 模板
cp templates/adr-template.md kernel-template/03_决策日志/ADR-001-XXX.md

# 复制 Evidence 模板
cp templates/evidence-block-template.md .agent/evidence-template.md
```

### 2. 填充占位符

模板中的占位符使用 `{PLACEHOLDER}` 格式，需要替换为实际值：

| 占位符 | 说明 | 示例 |
|--------|------|------|
| {PROJECT_NAME} | 项目名称 | etl_station |
| {TIMESTAMP} | 时间戳 | 2026-06-23 12:00:00 |
| {TASK_DESCRIPTION} | 任务描述 | 实现用户管理 CRUD |
| {MAINTAINER} | 维护人 | 张三 |
| {NUMBER} | ADR 编号 | 001 |
| {DECISION_TITLE} | 决策标题 | 选择 Redis 作为缓存 |

### 3. 自定义模板

可以根据项目需要自定义模板：

```bash
# 复制模板
cp templates/adr-template.md templates/adr-template-custom.md

# 编辑自定义模板
vim templates/adr-template-custom.md
```

---

## 🛠️ 模板维护

### 添加新模板
1. 创建模板文件（Markdown 格式）
2. 添加 YAML frontmatter（description 字段）
3. 使用 `{PLACEHOLDER}` 标记需要填充的字段
4. 添加使用说明
5. 更新本 README

### 模板命名规范
- 使用小写字母和连字符
- 格式：`<功能>-template.md`
- 示例：`constraint-checklist-template.md`

### 模板结构规范
```markdown
---
description: 模板用途简述
---

# 模板标题

**字段1**: {PLACEHOLDER1}
**字段2**: {PLACEHOLDER2}

## 章节1
内容...

## 使用说明
1. 步骤1
2. 步骤2

---

**模板版本**: vX.Y.Z
```

---

## 📚 相关资源

### 工作流文档
- [02_需求雷达](../workflows/02_需求雷达.md) - 任务规划
- [03_规约形式化](../workflows/03_规约形式化.md) - 约束清单
- [04_受控执行](../workflows/04_受控执行.md) - Evidence Block

### 脚本工具
- [evidence-gen.sh](../scripts/evidence-gen.sh) - Evidence 生成脚本
- [constraint-check.sh](../scripts/constraint-check.sh) - 约束检查脚本

---

## 🤝 贡献指南

### 反馈改进建议
如果在使用模板时发现问题或有改进建议：

1. 在项目中使用模板
2. 记录遇到的问题
3. 提出改进建议
4. 提交 Pull Request

### 分享自定义模板
如果你创建了有价值的自定义模板：

1. 确保模板通用性
2. 添加详细的使用说明
3. 提交到 templates/ 目录
4. 更新本 README

---

**维护人**: {MAINTAINER}
**最后更新**: 2026-06-23
