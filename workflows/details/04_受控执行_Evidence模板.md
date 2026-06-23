# Evidence Block 完整模板和示例

本文档提供三种级别的 Evidence Block 完整模板和实战示例。

---

## 🟢 精简版（5个核心字段）

### 适用场景
- ACK-LITE (精简流程)
- 简单改动：改字段、加校验、修文案
- 涉及文件: 1-3 个

### 模板

```yaml
### Evidence Block (精简版)

**Compliance_Status**: 🟢 PASS / ⚠️ PARTIAL / 🔴 FAIL
**Target_Files**: 
  - [文件路径1]
  - [文件路径2]
**Test_Run**: 
  - [测试命令]
  - 结果: [测试结果]
**Constraints_Checked**: 
  - ✅ [检查项1]
  - ✅ [检查项2]
**Summary**: 
  [一句话总结本次变更]
```

### 实战示例1: 添加字段

```yaml
### Evidence Block (精简版)

**Compliance_Status**: 🟢 PASS
**Target_Files**: 
  - src/main/java/com/example/entity/User.java
  - src/main/resources/db/migration/V2024_06_23__add_email.sql
**Test_Run**: 
  - mvn test -Dtest=UserServiceTest
  - 结果: ✅ 2/2 passed
**Constraints_Checked**: 
  - ✅ Jackson 注解正确 (@JsonProperty)
  - ✅ 数据库字段类型匹配 (VARCHAR(255))
  - ✅ 字段非空约束正确
**Summary**: 
  在 User 实体增加 email 字段，已通过单元测试验证
```

### 实战示例2: 修改文案

```yaml
### Evidence Block (精简版)

**Compliance_Status**: 🟢 PASS
**Target_Files**: 
  - src/main/resources/i18n/messages_zh_CN.properties
**Test_Run**: 
  - mvn test -Dtest=I18nTest
  - 结果: ✅ 3/3 passed
**Constraints_Checked**: 
  - ✅ 文案格式正确
  - ✅ 占位符匹配
  - ✅ 无乱码
**Summary**: 
  修改登录页面提示文案，已验证国际化配置正确
```

---

## 🟡 标准版（10个字段）

### 适用场景
- ACK (标准流程)
- 新增功能：新增API、修改逻辑、业务功能
- 涉及文件: 4-10 个

### 模板

```yaml
### Evidence Block (标准版)

**Compliance_Status**: 🟢 PASS
**Target_Files**: 
  - [文件列表]

**Changes_Summary**: 
  [变更摘要，2-3句话]

**Constraint_Checklist_Status**: 
  - ✅ 1/N: [约束1]
  - ✅ 2/N: [约束2]
  ...

**Test_Run**: 
  - [测试命令]
  - 结果: [结果]
  - 覆盖率: [百分比]

**API_Test_Evidence**: 
  ```bash
  [API 测试命令和结果]
  ```

**Reverse_Proof**: 
  [回滚验证说明]

**KVC_Preview**: 
  - 预估 KVC: [数值]

**SCV_Preview**: 
  - 预估 SCV: [数值]

**Solid_Touch**: 
  None / Strict / Regulated

**Summary**: 
  [详细总结]
```

### 实战示例: 新增导出功能

```yaml
### Evidence Block (标准版)

**Compliance_Status**: 🟢 PASS
**Target_Files**: 
  - src/main/java/com/example/controller/UserController.java
  - src/main/java/com/example/service/UserService.java
  - src/main/java/com/example/service/impl/UserServiceImpl.java
  - src/main/java/com/example/mapper/UserMapper.java
  - src/test/java/com/example/controller/UserControllerTest.java

**Changes_Summary**: 
  新增用户列表导出API (/api/users/export)，支持 Excel 格式导出，
  包含分页参数和权限校验，已通过 API 测试验证。

**Constraint_Checklist_Status**: 
  - ✅ 1/5: 返回 Excel 文件流
  - ✅ 2/5: 支持分页参数 (page, size)
  - ✅ 3/5: 权限校验已添加 (@RequiresPermissions("user:export"))
  - ✅ 4/5: 异常处理已完善
  - ✅ 5/5: 日志记录已添加

**Test_Run**: 
  - mvn test -Dtest=UserControllerTest
  - 结果: ✅ 8/8 passed
  - 覆盖率: 92%

**API_Test_Evidence**: 
  ```bash
  # 测试导出功能
  curl -X GET "http://localhost:8080/api/users/export?page=1&size=10" \
    -H "Authorization: Bearer xxx"
  
  # 响应
  HTTP/1.1 200 OK
  Content-Type: application/vnd.ms-excel
  Content-Disposition: attachment; filename="users_20260623.xlsx"
  Content-Length: 15234
  ```

**Reverse_Proof**: 
  无需回滚，新增功能不影响现有代码。已验证原有用户查询API仍正常工作。

**KVC_Preview**: 
  - 预估 KVC: 1.0 (新增代码，键值完全一致)

**SCV_Preview**: 
  - 预估 SCV: +2.5 (新增一个 Controller 方法 + Service 实现)

**Solid_Touch**: 
  None (未触碰核心业务逻辑)

**Summary**: 
  新增用户导出功能，支持 Excel 格式，包含分页和权限校验。
  已通过 8 个单元测试和 API 集成测试验证，覆盖率 92%。
```

---

## 🔴 完整版（23个字段）

### 适用场景
- ACK-FULL (完整流程)
- 复杂改动：重构模块、架构变更、技术决策
- 涉及文件: 10+ 个

### 字段分类
- **核心字段** (5个，必填): Compliance_Status, Target_Files, Changes_Summary, Test_Run, Summary
- **架构相关** (3个): Architecture_Impact, Affected_Modules, Solid_Touch
- **约束检查** (1个): Constraint_Checklist_Status
- **测试验证** (2个): API_Test_Evidence, Reverse_Proof
- **性能影响** (1个): Performance_Impact
- **依赖变更** (2个): Dependencies_Added, Migration_SQL
- **度量指标** (5个): KVC_Before, KVC_After, SCV_Before, SCV_After, Complexity_Justification
- **回滚相关** (1个): Rollback_Plan
- **知识沉淀** (3个): ADR_Required, FAQ_Update, Documentation_Updated

### 模板

```yaml
### Evidence Block (完整版)

**Compliance_Status**: 🟢 PASS

**Target_Files**: 
  - [完整文件列表，包括新增、修改、重构]

**Changes_Summary**: 
  [详细变更摘要]

**Architecture_Impact**: 
  - 🔴 [高影响变更]
  - 🟡 [中影响变更]
  - 🟢 [低影响变更]

**Constraint_Checklist_Status**: 
  - ✅ 1/N: [约束检查清单]
  ...

**Test_Run**: 
  - [完整测试命令]
  - 结果: [详细结果]
  - 覆盖率: [各层覆盖率]

**API_Test_Evidence**: 
  [API 测试完整证据]

**Performance_Impact**: 
  - [性能对比数据]

**Reverse_Proof**: 
  [详细回滚验证]

**Dependencies_Added**: 
  [新增依赖列表]

**Migration_SQL**: 
  [数据库迁移脚本]

**KVC_Before**: [数值]
**KVC_After**: [数值]

**SCV_Before**: [数值]
**SCV_After**: [数值]

**Complexity_Justification**: 
  [复杂度增加合理性说明]

**Solid_Touch**: 
  Strict (核心代码重构)

**Affected_Modules**: 
  - ✅ [已测试模块]
  - ⚠️ [需手动测试模块]

**Rollback_Plan**: 
  [详细回滚步骤]

**ADR_Required**: 
  ✅ 是 / ❌ 否
  [ADR 编号和标题]

**FAQ_Update**: 
  [FAQ 更新内容]

**Documentation_Updated**: 
  [文档更新清单]

**Summary**: 
  [完整总结]
```

### 实战示例: 引入缓存层

```yaml
### Evidence Block (完整版)

**Compliance_Status**: 🟢 PASS

**Target_Files**: 
  - src/main/java/com/example/service/UserService.java (重构)
  - src/main/java/com/example/service/impl/UserServiceImpl.java (新增)
  - src/main/java/com/example/cache/UserCacheManager.java (新增)
  - src/main/java/com/example/cache/CacheConfig.java (新增)
  - src/main/java/com/example/config/ApplicationConfig.java (修改)
  - src/test/java/com/example/service/UserServiceTest.java (重构)
  - src/test/java/com/example/cache/UserCacheTest.java (新增)

**Changes_Summary**: 
  重构用户服务层，引入 Caffeine 本地缓存，优化查询性能。
  Service 层接口抽取（面向接口编程），新增 CacheManager 封装缓存逻辑，
  配置层增加缓存配置。已通过 18 个测试，覆盖率 94%。

**Architecture_Impact**: 
  - 🔴 新增缓存层 (CacheManager) - 架构新增一层
  - 🟡 Service 层接口抽取 - 修改现有架构
  - 🟢 Config 层增加缓存配置 - 配置扩展

**Constraint_Checklist_Status**: 
  - ✅ 1/8: 缓存 TTL 设置为 60 秒
  - ✅ 2/8: 缓存 Key 格式统一 (user:{id})
  - ✅ 3/8: 缓存失效机制已实现
  - ✅ 4/8: 缓存穿透防护已添加（空值缓存）
  - ✅ 5/8: 单元测试覆盖 >90%
  - ✅ 6/8: 集成测试已添加
  - ✅ 7/8: 日志记录缓存命中率
  - ✅ 8/8: 监控指标已暴露（Micrometer）

**Test_Run**: 
  - mvn clean test
  - 结果: ✅ 18/18 passed
  - 覆盖率: 
    - Service 层: 94%
    - Cache 层: 88%
    - 整体: 91%

**API_Test_Evidence**: 
  ```bash
  # 第一次查询 (缓存未命中)
  curl http://localhost:8080/api/users/1
  Response Time: 120ms
  Cache-Status: MISS
  
  # 第二次查询 (缓存命中)
  curl http://localhost:8080/api/users/1
  Response Time: 5ms
  Cache-Status: HIT
  
  # 更新用户后查询 (缓存失效)
  curl -X PUT http://localhost:8080/api/users/1 -d '{"name":"新名称"}'
  curl http://localhost:8080/api/users/1
  Cache-Status: MISS (缓存已自动失效)
  ```

**Performance_Impact**: 
  - 查询性能提升: 120ms → 5ms (缓存命中时, ↑95%)
  - 内存占用: +50MB (预估 1 万用户缓存)
  - CPU 占用: 无明显变化
  - 数据库压力: ↓60% (缓存命中率约 60%)

**Reverse_Proof**: 
  已验证缓存关闭后功能正常：
  ```properties
  # application.properties
  cache.enabled=false
  ```
  测试结果: ✅ 所有功能正常，性能退化到优化前水平

**Dependencies_Added**: 
  ```xml
  <dependency>
      <groupId>com.github.ben-manes.caffeine</groupId>
      <artifactId>caffeine</artifactId>
      <version>3.1.8</version>
  </dependency>
  <dependency>
      <groupId>io.micrometer</groupId>
      <artifactId>micrometer-core</artifactId>
      <version>1.11.0</version>
  </dependency>
  ```

**Migration_SQL**: 
  无数据库变更

**KVC_Before**: 0.92
**KVC_After**: 0.93 (+0.01)

**SCV_Before**: 45.2
**SCV_After**: 47.8 (+2.6)

**Complexity_Justification**: 
  SCV 增加 2.6 属于可接受范围 (<5.0)，原因：
  1. 新增 CacheManager 封装了缓存逻辑（+1.5 复杂度）
  2. Service 层复杂度降低（查询逻辑简化，-0.8 复杂度）
  3. 配置层增加缓存配置（+1.9 复杂度）
  4. 整体代码可维护性提升，职责更清晰

**Solid_Touch**: 
  Strict (核心 Service 层重构)

**Affected_Modules**: 
  - ✅ UserService (已测试 ✅)
  - ✅ UserController (已测试 ✅)
  - ⚠️ 报表模块 (间接依赖，需手动回归测试)
  - ⚠️ 统计模块 (间接依赖，需手动回归测试)

**Rollback_Plan**: 
  1. 回滚 Git commit: `git revert HEAD`
  2. 删除缓存配置: 移除 CacheConfig.java
  3. 还原 UserService 接口: 恢复为实现类
  4. 移除 Caffeine 依赖: 修改 pom.xml
  5. 重新运行测试: `mvn clean test`
  6. 重新部署: `mvn clean package && deploy.sh`

**ADR_Required**: 
  ✅ 是
  - ADR 编号: ADR-006
  - 决策标题: "采用 Caffeine 本地缓存优化查询性能"
  - 记录位置: project-kernel/03_决策日志/ADR-006.md

**FAQ_Update**: 
  ✅ 已添加 FAQ 条目：
  1. Q: 为什么选择 Caffeine 而不是 Redis？
     A: 本地缓存延迟更低（5ms vs 50ms），数据量小（1万用户），无需维护 Redis 集群
  
  2. Q: 缓存 TTL 为什么设置为 60 秒？
     A: 平衡数据新鲜度和缓存命中率，用户信息更新频率低，60秒可接受
  
  3. Q: 如何监控缓存性能？
     A: 通过 Micrometer 暴露指标，在 /actuator/metrics/cache.* 查看

**Documentation_Updated**: 
  - ✅ 架构文档已更新: docs/architecture.md (添加缓存层说明)
  - ✅ API 文档已更新: docs/api.md (添加 Cache-Status 响应头说明)
  - ✅ 部署文档已更新: docs/deployment.md (添加缓存配置说明)
  - ✅ 监控文档已更新: docs/monitoring.md (添加缓存指标说明)

**Summary**: 
  重构用户服务层，引入 Caffeine 本地缓存，查询性能提升 95%（120ms→5ms）。
  已通过 18 个测试（覆盖率 94%），需要记录 ADR-006 决策。
  影响报表和统计模块，需手动回归测试。
```

---

## 💡 使用建议

### 选择合适的级别
1. **精简版**: 用于日常小改动，快速记录
2. **标准版**: 用于常规功能开发，平衡详细度和效率
3. **完整版**: 用于重大变更，确保可追溯和可回滚

### 填写技巧
1. **简洁明了**: 每个字段用 1-3 句话说清楚
2. **数据说话**: 提供具体的数值和证据
3. **问题导向**: 重点记录潜在风险和解决方案
4. **可验证**: 提供命令和步骤，让他人可以复现

### 常见错误
- ❌ 字段留空或填 "无"
- ❌ 测试结果写 "通过" 但无具体数据
- ❌ 复杂度变化无合理性说明
- ❌ 回滚计划写 "恢复代码" 但无具体步骤

---

**版本**: v1.2.1  
**更新日期**: 2026-06-23
