---
description: Evidence Block 模板 - 三种深度
---

# Evidence Block 模板

根据流程类型选择对应的 Evidence Block 深度。

---

## 🟢 精简版 (Lite) - 5 字段

适用场景：小改动（改字段、加校验）

```markdown
### 📦 Context Evidence (Lite)
- **Compliance_Status**: 🟢 Pass | ⚠️ Warning | 🔴 Fail
- **Target_Files**: [修改的文件列表]
- **Test_Result**: ✅ 单元测试通过 (mvn test)
- **P0_Violations**: 0 个
- **Commit_Hash**: {git_commit_hash}

**生成时间**: {timestamp}
```

### 填写说明

| 字段 | 说明 | 示例 |
|------|------|------|
| Compliance_Status | 合规状态 | 🟢 Pass |
| Target_Files | 修改的文件 | UserDTO.java, UserService.java |
| Test_Result | 测试结果 | ✅ 单元测试通过 (mvn test) |
| P0_Violations | P0 级违规 | 0 个 |
| Commit_Hash | Git 提交哈希 | a1b2c3d |

---

## 🟡 标准版 (Standard) - 8 字段

适用场景：新增功能、修改逻辑

```markdown
### 📦 Context Evidence (Standard)
- **Compliance_Status**: 🟢 Pass | ⚠️ Warning | 🔴 Fail
- **Target_Files**: [修改的文件列表]
- **Diff_Summary**: 
  - 修改文件: {file_count} 个
  - 代码行数: 约 {line_count} 行
  - 关键变更: {brief_description}
- **Test_Run**:
  - Runner: JUnit5
  - Command: mvn test
  - Result: Pass ({passed}/{total})
  - Coverage: {coverage}%
- **Constraint_Check**:
  - Source: 03_规约形式化
  - P0_Violations: {count} 个
  - P1_Warnings: {count} 个
- **Commit_Hash**: {git_commit_hash}

**生成时间**: {timestamp}
```

### 填写说明

| 字段 | 说明 | 示例 |
|------|------|------|
| Diff_Summary | 变更摘要 | 修改文件: 4 个，代码行数: 约 120 行 |
| Test_Run | 测试执行 | Pass (15/15)，Coverage: 85% |
| Constraint_Check | 约束检查 | P0_Violations: 0 个，P1_Warnings: 2 个 |

---

## 🔴 完整版 (Full) - 20 字段

适用场景：重构模块、架构变更

```markdown
### 📦 Context Evidence (Full)
- **Compliance_Status**: 🟢 Pass | ⚠️ Warning | 🔴 Fail
- **Context_Log**:
  - Packs: [Pack-0 + Pack-1 + Pack-2]
  - Target_Files: [修改的文件列表]
  - Commands: [mvn clean install, mvn test, sonar-scanner]
- **Diff_Summary**: 
  - 修改文件: {file_count} 个
  - 代码行数: 约 {line_count} 行
  - 关键变更: {brief_description}
  - Pizza 切片: {yes/no}
- **Test_Run**:
  - Runner: JUnit5 + Mockito
  - Command: mvn test
  - Result: Pass ({passed}/{total})
  - Coverage: {coverage}%
- **Scan_Result**:
  - Runner: SonarQube
  - Command: sonar-scanner
  - Blocker_Count: {count}
  - Critical_Count: {count}
  - Major_Count: {count}
- **Reverse_Proof**: 
  - Position: {test_class}#{test_method}
  - Action: {破坏性操作描述}
  - Error: {expected_error} ✅
  - Recover: 恢复后测试通过 ✅
- **Solid_Touch**: None | Solid-Regulated | Solid-Strict
- **Approval_Hash**: {approval_hash} (如需要)
- **Asset_Update**: {asset_update_description} (如需要)
- **ADR_Entry**: ADR-{number}: {title} (如需要)
- **Constraint_Check**:
  - Source: 03_规约形式化
  - P0_Violations: {count} 个
  - P1_Warnings: {count} 个
  - Manual_Checklist: [已验证]
  
**生成时间**: {timestamp}
```

### 填写说明

| 字段 | 说明 | 示例 |
|------|------|------|
| Context_Log | 上下文日志 | Packs: [Pack-0 + Pack-1 + Pack-2] |
| Scan_Result | 代码扫描 | Blocker_Count: 0, Critical_Count: 0 |
| Reverse_Proof | 破坏性证明 | 修改关键逻辑，测试红灯，恢复后绿灯 |
| Solid_Touch | 核心资产 | Solid-Strict（需 Approval_Hash） |
| Approval_Hash | 批准哈希 | 人工确认签名 |
| Asset_Update | 资产更新 | 更新数据库 schema，迁移脚本: V001_xxx.sql |
| ADR_Entry | ADR 条目 | ADR-001: 选择 Redis 作为缓存 |

---

## 使用指南

### 1. 选择合适的深度

根据 `02_需求雷达` 的智能分流建议：

- 🟢 **精简流程 (ACK-LITE)** → 使用精简版 Evidence
- 🟡 **标准流程 (ACK)** → 使用标准版 Evidence
- 🔴 **完整流程 (ACK-FULL)** → 使用完整版 Evidence

### 2. 填充模板

1. 复制对应深度的模板
2. 替换 `{placeholder}` 为实际值
3. 删除不适用的字段（标记为"如需要"的）

### 3. 生成脚本

也可以使用自动化脚本生成：

```bash
# 生成精简版
./scripts/evidence-gen.sh lite

# 生成标准版
./scripts/evidence-gen.sh standard

# 生成完整版
./scripts/evidence-gen.sh full
```

---

## 字段说明

### 必填字段（所有深度）

- **Compliance_Status**: 合规状态
- **Target_Files**: 修改的文件
- **Test_Result** / **Test_Run**: 测试结果
- **P0_Violations**: P0 级违规数量
- **Commit_Hash**: Git 提交哈希

### 条件字段

- **Reverse_Proof**: 核心算法必须提供
- **Solid_Touch**: 触碰核心资产时必须填写
- **Approval_Hash**: Solid-Strict 必须提供
- **ADR_Entry**: 架构变更必须提供

---

## 检查清单

### 精简版检查
- [ ] Compliance_Status 不为 Fail
- [ ] P0_Violations = 0
- [ ] 测试通过

### 标准版检查
- [ ] Compliance_Status 不为 Fail
- [ ] P0_Violations = 0
- [ ] 测试通过
- [ ] 测试覆盖率 > 80%
- [ ] P1_Warnings 已知晓

### 完整版检查
- [ ] Compliance_Status 不为 Fail
- [ ] P0_Violations = 0
- [ ] 测试通过
- [ ] 测试覆盖率 > 80%
- [ ] 代码扫描无 Blocker
- [ ] Reverse_Proof 已执行（如适用）
- [ ] Solid 触碰已审批（如适用）
- [ ] ADR 已记录（如适用）

---

**模板版本**: v1.1.0
**最后更新**: 2026-06-23
