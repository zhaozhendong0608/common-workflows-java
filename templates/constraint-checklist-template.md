---
description: 约束清单模板 - 用于 03_规约形式化
---

# 约束清单 (Constraint Checklist)

**项目**: {PROJECT_NAME}
**生成时间**: {TIMESTAMP}
**任务**: {TASK_DESCRIPTION}

---

## P0 约束（强制 - Must）

### P0-001: Context Key 格式
- **规则**: 所有 `context.put()` 的 Key 必须使用 `node:{nodeId}` 格式
- **检查方式**: `grep -rn 'context\.put' src/ | grep -v 'node:'`
- **示例**:
  ```java
  // ❌ 错误
  context.put("temperature", value);
  
  // ✅ 正确
  context.put("node:temperature", value);
  ```

### P0-002: Context Value 类型
- **规则**: 所有 `context.put()` 的 Value 必须是 `AlgoValue<T>` 类型
- **检查方式**: 人工审查
- **示例**:
  ```java
  // ❌ 错误
  context.put("node:temperature", rawValue);
  
  // ✅ 正确
  context.put("node:temperature", AlgoValue.of(rawValue));
  ```

### P0-003: 继承 BaseAlgoComponent
- **规则**: 所有算子类必须继承 `BaseAlgoComponent`
- **检查方式**: `grep -L 'extends BaseAlgoComponent' src/**/*Operator.java`
- **示例**:
  ```java
  // ✅ 正确
  public class TemperatureOperator extends BaseAlgoComponent {
      // ...
  }
  ```

### P0-004: 使用 @AlgoOperator 注解
- **规则**: 所有算子类必须使用 `@AlgoOperator` 注解
- **检查方式**: `grep -L '@AlgoOperator' src/**/*Operator.java`
- **示例**:
  ```java
  // ✅ 正确
  @AlgoOperator(name = "temperature", version = "1.0")
  public class TemperatureOperator extends BaseAlgoComponent {
      // ...
  }
  ```

---

## P1 约束（建议 - Should）

### P1-001: 变量驼峰命名
- **规则**: 变量名使用小驼峰（camelCase）
- **检查方式**: 人工审查或 checkstyle
- **示例**:
  ```java
  // ❌ 错误
  String user_name = "test";
  String USER_NAME = "test";
  
  // ✅ 正确
  String userName = "test";
  ```

### P1-002: 方法注释完整
- **规则**: public 方法必须有 Javadoc 注释
- **检查方式**: 人工审查或 checkstyle
- **示例**:
  ```java
  /**
   * 计算温度平均值
   * 
   * @param values 温度值列表
   * @return 平均温度
   */
  public double calculateAverage(List<Double> values) {
      // ...
  }
  ```

### P1-003: 异常处理规范
- **规则**: 不允许吞没异常，必须记录日志或重新抛出
- **检查方式**: `grep -rn 'catch.*Exception.*{\s*}' src/`
- **示例**:
  ```java
  // ❌ 错误
  try {
      // ...
  } catch (Exception e) {
      // 空 catch 块
  }
  
  // ✅ 正确
  try {
      // ...
  } catch (Exception e) {
      log.error("操作失败", e);
      throw new BusinessException("操作失败", e);
  }
  ```

---

## P2 约束（可选 - Could）

### P2-001: 代码风格统一
- **规则**: 遵循 Google Java Style Guide
- **检查方式**: `checkstyle -c google_checks.xml src/`

### P2-002: 日志使用中文
- **规则**: 业务日志使用中文，便于问题定位
- **检查方式**: 人工审查
- **示例**:
  ```java
  // ✅ 推荐
  log.info("开始执行温度计算，测点数量: {}", pointCount);
  ```

---

## FSM 状态序列（如适用）

### 预期状态转换
```
INIT → LOADING → VALIDATING → PROCESSING → COMPLETED
```

### 关键检查点
- [ ] LOADING 后必须有数据校验
- [ ] PROCESSING 前必须获取锁
- [ ] COMPLETED 后必须释放资源

---

## 人工检查清单

### 代码质量
- [ ] 无魔法数字（magic number）
- [ ] 无硬编码（hard-coded values）
- [ ] 无重复代码（DRY 原则）
- [ ] 无过长方法（< 50 行）
- [ ] 无过深嵌套（< 4 层）

### 业务逻辑
- [ ] 边界条件处理完整
- [ ] 异常分支考虑充分
- [ ] 空值检查到位
- [ ] 并发安全保障

### 测试覆盖
- [ ] 核心逻辑有单元测试
- [ ] 边界条件有测试用例
- [ ] 异常场景有测试覆盖
- [ ] 测试覆盖率 > 80%

---

## 使用说明

### 1. 生成约束清单
在 `03_规约形式化` 阶段，根据项目实际情况填充本模板。

### 2. 执行检查
在 `04_受控执行` 阶段，逐项检查约束是否满足。

### 3. 记录结果
在 Evidence Block 的 `Constraint_Check` 字段中记录检查结果。

---

**维护人**: {MAINTAINER}
**版本**: v1.0
