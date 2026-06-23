# Java 项目通用工作流标准

**版本**: v1.2.1  
**创建日期**: 2026-06-23  
**维护人**: {YOUR_NAME}

> 基于 Sentinel Kernel 理论的 Java 项目开发流程标准
> 
> 🆕 v1.2.1 重磅更新：Token 消耗降低 83%，AI 响应速度提升 5-8 倍

---

## ⚡ v1.2.1 核心改进

### Token 优化 🚀
- **Token 消耗**: 22,000 → 3,700 (↓83%)
- **文件行数**: 3,307 → 1,104 (↓67%)
- **AI 加载速度**: 5-8秒 → <1秒 (↑5-8倍)
- **对话轮次**: 3-5轮 → 15-20轮 (↑4-5倍)

### 两层架构 📚
- **精简版工作流**: 只包含核心指令（workflows/*.md）
- **详细文档**: 按需加载（workflows/details/*.md）
- **智能分流**: 自动建议合适的流程类型

### 命令优化 🎯
- **英文短命令**: `/boot`, `/radar`, `/execute`...
- **向后兼容**: `/01`, `/02`... 仍然有效
- **命令速查表**: COMMANDS.md

---

## 简介

这是一套适用于 **Java 项目** 的通用开发工作流标准，包含：

✅ **工作流**: 9 步标准开发流程 + 智能分流机制  
✅ **命令系统**: 统一的英文短命令  
✅ **内核模板**: 项目知识管理体系  
✅ **示例**: 实战开发指南  
✅ **脚本**: 自动化工具（可选）

---

## 🚀 快速上手（5分钟）

### 只需记住 3 个命令

```bash
/boot      # 启动系统
/radar     # 分析需求（自动建议流程）
/execute   # 执行开发
```

其他命令 AI 会根据流程类型自动提示。

📖 [完整的5分钟快速开始指南](./快速开始_5分钟版.md)

---

## 核心价值

### 1. 上手简单
- 5 分钟快速开始
- 只需记住 3 个核心命令
- 清晰的命令索引

### 2. 准确率高
- 命令格式统一
- 步骤完整可追溯
- 向后兼容旧命令

### 3. Token 节省
- 精简版工作流（平均 110 行）
- 详细文档按需加载
- 节省 83% Token 消耗

### 4. 质量保障
- KVC (键值一致性) ≥ 0.90
- SCV (复杂度变化) < 5.0
- 分级 Evidence Block（5/10/20 字段）

### 5. 知识积累
- 架构决策记录（ADR）
- 技术问题库（FAQ）
- 项目进度追踪
- 度量数据归档

---

## 目录结构

```
common-workflows-java/
├── README.md                      # 项目文档（本文件）
├── COMMANDS.md                    # 命令速查表 ⭐
├── 快速开始_5分钟版.md            # 新手快速上手指南 ⭐
├── CHANGELOG.md                   # 版本更新日志
├── VERSION_UPDATE.md              # v1.2.0 更新说明
├── 改进总结.md                    # v1.2.0 改进总结
├── 优化结果报告.md                # Token 优化报告
│
├── workflows/                     # 精简版工作流（指令卡片）⭐
│   ├── 00_领航员.md              [123行] - 任务调度中心
│   ├── 01_启动自检.md            [52行]  - 系统启动
│   ├── 02_规约形式化.md          [108行] - 约束清单生成
│   ├── 03_需求雷达.md            [98行]  - 需求分析+智能分流
│   ├── 04_受控执行.md            [105行] - 编码开发
│   ├── 05_度量分析.md            [109行] - KVC/SCV度量
│   ├── 06_业务测试.md            [133行] - API/E2E测试
│   ├── 07_质量关卡.md            [111行] - 质量审查
│   ├── 08_归档重启.md            [161行] - 知识沉淀
│   ├── 09_流程选择指南.md        [104行] - 流程选择参考
│   └── details/                   # 详细文档（按需加载）⭐
│       ├── README.md
│       ├── 04_受控执行_Evidence模板.md
│       ├── 05_度量分析_详细指南.md
│       └── 06_业务测试_完整指南.md
│
├── kernel-template/               # 内核模板
│   ├── 00_系统总纲.md
│   ├── 01_项目全景.md
│   ├── 02_开发规约/
│   │   ├── 01_编码规范.md
│   │   └── 02_架构规范.md
│   ├── 03_决策日志.md
│   ├── 04_答疑库.md
│   ├── 05_项目进度.md
│   └── 06_业务拓扑.md
│
├── templates/                     # 模板文件
│   ├── README.md
│   ├── constraint-checklist-template.md
│   ├── adr-template.md
│   └── evidence-block-template.md
│
├── scripts/                       # 自动化脚本
│   ├── README.md
│   ├── metrics.py
│   ├── auto-archive.py
│   └── constraint-check.sh
│
├── examples/                      # 实战示例
│   ├── README.md
│   └── 01_用户管理CRUD示例.md
│
└── docs/                          # 文档中心
    ├── README.md
    ├── architecture/
    │   └── 智能分流架构图.md
    └── releases/
        └── v1.1.0_改进报告.md
```

---

## 快速开始

### 方式1: 使用新命令系统（推荐）⭐

**第1步**: 复制工作流到项目
```bash
# 复制到项目根目录
cp -r /path/to/common-workflows-java/workflows .agent/
```

**第2步**: 开始使用
```bash
# 告诉 AI 执行工作流
/boot      # 启动自检
/radar     # 分析需求，AI 会自动建议流程类型
/execute   # 执行开发
```

**就这么简单！**其他命令 AI 会根据流程类型自动提示。

📖 [完整的5分钟快速开始](./快速开始_5分钟版.md)

---

### 方式2: 传统方式（兼容）

<details>
<summary>点击展开传统方式</summary>

#### Step 1: 创建新项目

```bash
mkdir my-project && cd my-project
git init
```

#### Step 2: 复制工作流

```bash
mkdir -p .agent
cp -r /path/to/common-workflows-java/workflows .agent/
```

#### Step 3: 初始化项目内核

```bash
mkdir -p project-kernel
cp -r /path/to/common-workflows-java/kernel-template/* project-kernel/
```

#### Step 4: 定制项目内核

```bash
# 编辑项目信息
vim project-kernel/00_系统总纲.md

# 填充编码规范
vim project-kernel/02_开发规约/01_编码规范.md
```

</details>

---

## 三种流程模板

### 🟢 精简流程（30分钟）
```
/boot → /radar → /execute → /quality
```
**适用**: 改字段、加校验、修文案

---

### 🟡 标准流程（60分钟）
```
/boot → /constraint → /radar → /execute → /measure → /test → /quality
```
**适用**: 新增API、修改逻辑、业务功能

---

### 🔴 完整流程（93分钟）
```
/boot → /constraint → /radar → /execute → /measure → /test → /quality → /archive
```
**适用**: 重构模块、架构变更、技术决策

📖 [流程选择详细指南](./workflows/09_流程选择指南.md)

---

## 命令速查表

| 命令 | 说明 | 耗时 | 别名 |
|------|------|------|------|
| `/boot` | 启动自检 | 5 min | `/01` |
| `/constraint` | 规约形式化 | 10 min | `/02` |
| `/radar` | 需求雷达 + 智能分流 | 15 min | `/03` |
| `/execute` | 受控执行 | 20-60 min | `/04` |
| `/measure` | 度量分析 | 5 min | `/05` |
| `/test` | 业务测试 | 15 min | `/06` |
| `/quality` | 质量关卡 | 10 min | `/07` |
| `/archive` | 归档重启 | 5 min | `/08` |

📖 [完整命令速查表](./COMMANDS.md)

---

## 实战示例

### 示例1: 添加一个字段（精简流程）

```
User: /boot
AI: ✅ 系统已启动，信心自评 85/100

User: 我想在 User 表增加 email 字段
AI: 收到需求，请执行 /radar

User: /radar
AI: 📊 建议 🟢 ACK-LITE (精简流程, 30min)
    包含: /boot → /radar → /execute → /quality
    是否接受？

User: ACK
AI: ✅ 已确认精简流程，请执行 /execute

User: /execute
AI: [按照项目规约生成代码...]
    ✅ 已修改 User.java
    ✅ 已生成测试
    请执行 /quality

User: /quality
AI: ✅ 质量关卡通过！可以提交代码了
```

📖 [更多实战示例](./examples/)

---

## 版本历史

### v1.2.1 (2026-06-23) - Token 优化版 🚀
- ✅ Token 消耗降低 83%（22,000 → 3,700）
- ✅ 工作流文件精简 67%（3,307行 → 1,104行）
- ✅ 两层架构：精简版 + 详细版（按需加载）
- ✅ 新增详细文档目录（workflows/details/）
- ✅ AI 加载速度提升 5-8 倍
- ✅ 可用对话轮次提升 4-5 倍

### v1.2.0 (2026-06-23) - 命令优化版
- ✅ 统一命令格式（英文短命令）
- ✅ 命令速查表（COMMANDS.md）
- ✅ 5分钟快速开始
- ✅ 分级 Evidence Block（5/10/20 字段）
- ✅ 补全工作流步骤

### v1.1.0 (2026-06-23) - 智能分流版
- ✅ 智能分流机制
- ✅ 三种流程模板
- ✅ 流程选择指南

📖 [完整更新日志](./CHANGELOG.md)

---

## 核心文档

### 新手必读 ⭐
- [5分钟快速开始](./快速开始_5分钟版.md) - 最快上手
- [命令速查表](./COMMANDS.md) - 所有命令说明
- [流程选择指南](./workflows/09_流程选择指南.md) - 如何选择流程

### 进阶文档
- [领航员](./workflows/00_领航员.md) - 任务调度中心
- [Evidence 模板](./workflows/details/04_受控执行_Evidence模板.md) - 完整模板
- [度量分析指南](./workflows/details/05_度量分析_详细指南.md) - KVC/SCV
- [业务测试指南](./workflows/details/06_业务测试_完整指南.md) - API/E2E/UI

### 版本说明
- [v1.2.0 更新说明](./VERSION_UPDATE.md) - 命令优化
- [改进总结](./改进总结.md) - v1.2.0 改进分析
- [优化结果报告](./优化结果报告.md) - Token 优化详情

---

## 常见问题

### Q1: 为什么要用这套工作流？
**A**: 
- 提高开发效率：智能分流避免过度设计
- 保证代码质量：90分标准，度量可追溯
- 降低 AI 成本：Token 消耗降低 83%
- 积累团队知识：ADR、FAQ、度量数据

### Q2: 新手如何快速上手？
**A**: 
1. 阅读《5分钟快速开始》
2. 只记住 3 个核心命令：`/boot`, `/radar`, `/execute`
3. 其他命令 AI 会自动提示

### Q3: 是否必须严格按流程执行？
**A**: 
- 精简流程：可跳过部分步骤（度量、测试、归档）
- 标准流程：建议完整执行
- 完整流程：必须完整执行

### Q4: Token 优化后会影响功能吗？
**A**: 
- 不会！精简版保留了所有核心指令
- 详细内容通过链接按需加载
- 功能完整性 100% 保留

### Q5: 旧项目如何迁移？
**A**: 
- 旧命令（`/01`, `/02`...）仍然有效
- 逐步替换为新命令（`/boot`, `/radar`...）
- 向后兼容，无需修改

---

## 技术支持

- **GitHub**: https://github.com/zhaozhendong0608/common-workflows-java
- **Issues**: https://github.com/zhaozhendong0608/common-workflows-java/issues
- **文档**: 本仓库 docs/ 目录

---

## 许可证

MIT License

---

## 贡献指南

欢迎贡献！请：
1. Fork 本仓库
2. 创建特性分支
3. 提交 Pull Request

---

**版本**: v1.2.1  
**更新日期**: 2026-06-23  
**核心改进**: Token 消耗降低 83%，AI 响应速度提升 5-8 倍 🚀
