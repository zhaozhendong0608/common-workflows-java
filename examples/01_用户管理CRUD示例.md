# 实战示例：用户管理 CRUD 功能开发

本示例展示如何使用工作流完成一个完整的功能开发。

## 📋 任务描述

**功能**: 实现用户管理 CRUD（增删改查）功能

**需求**:
- 新增用户
- 查询用户列表（分页）
- 修改用户信息
- 删除用户

**涉及文件**:
- `UserController.java`
- `UserService.java`
- `UserMapper.java`
- `UserDTO.java`

---

## 🚀 完整流程演示

### Step 1: 启动自检 (5 min)

```
向 AI: 请执行 01_启动自检.md

AI 输出:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 信心评分: 85/100 (可以开始)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ 项目全景理解
  - 技术栈: Spring Boot + MyBatis + MySQL
  - 架构模式: MVC 三层架构
  - 已有规范: 编码规范.md + 架构规范.md

✅ ADR 加载
  - ADR-001: 使用 MyBatis 而非 JPA
  - ADR-002: 统一异常处理

✅ 开发规约理解
  - P0: 必须使用 @RestController
  - P0: 返回值必须包装为 Result<T>
  - P1: Controller 方法需要 @ApiOperation 注解

准备就绪，可以开始任务规划！
```

---

### Step 2: 需求雷达 (10 min)

```
向 AI: 请执行 02_需求雷达.md

任务: 实现用户管理 CRUD 功能

AI 输出:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 需求雷达扫描完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Node D: 智能分流评估
  - 文件数量: 4 个 (1.5 分)
  - 代码行数: 约 120 行 (1.5 分)
  - Pizza 切片: 未触发 (0 分)
  - Solid 触碰: None (0 分)
  - 风险等级: 低 (1 分)
  
  综合得分: 4.0 / 5 = 1.6 / 3.0

✅ 建议流程: 🟡 标准流程 (60 min)

请选择:
  1. ACK-LITE → 精简流程 (30 min)
  2. ACK → 标准流程 (60 min) [推荐]
  3. ACK-FULL → 完整流程 (93 min)
```

**用户确认**:
```
向 AI: ACK

AI: 好的，启动标准流程 (60 min)
```

---

### Step 3: 规约形式化 (8 min)

```
AI 自动执行: 03_规约形式化.md

AI 输出:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 约束清单生成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

P0 约束（强制）:
  - P0-001: Controller 必须使用 @RestController
  - P0-002: 返回值必须包装为 Result<T>
  - P0-003: Service 必须添加 @Transactional

P1 约束（建议）:
  - P1-001: 方法需要 @ApiOperation 注解
  - P1-002: DTO 字段需要校验注解

人工检查清单:
  - [ ] 分页参数校验（pageNum, pageSize）
  - [ ] 用户名唯一性校验
  - [ ] 删除前检查关联数据

约束清单已保存: .agent/constraint-checklist.yml
```

---

### Step 4: 受控执行 (25 min)

```
AI 自动执行: 04_受控执行.md

AI 输出:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 代码生成完成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

生成文件:
  ✅ UserController.java (新增)
  ✅ UserService.java (新增)
  ✅ UserMapper.java (新增)
  ✅ UserDTO.java (新增)

测试文件:
  ✅ UserControllerTest.java (新增)
  ✅ UserServiceTest.java (新增)

测试运行:
  mvn test
  ✅ Pass (8/8)
  ✅ Coverage: 87%

约束检查:
  ✅ P0_Violations: 0 个
  ⚠️  P1_Warnings: 1 个 (UserDTO 缺少 @NotNull 注解)

### 📦 Context Evidence (Standard)
- **Compliance_Status**: 🟢 Pass
- **Target_Files**: [UserController.java, UserService.java, UserMapper.java, UserDTO.java]
- **Diff_Summary**: 
  - 修改文件: 4 个
  - 代码行数: 约 120 行
  - 关键变更: 新增用户管理 CRUD 功能
- **Test_Run**:
  - Runner: JUnit5
  - Command: mvn test
  - Result: Pass (8/8)
  - Coverage: 87%
- **Constraint_Check**:
  - Source: 03_规约形式化
  - P0_Violations: 0 个
  - P1_Warnings: 1 个
- **Commit_Hash**: a1b2c3d

**生成时间**: 2026-06-23 14:30:00
```

---

### Step 5: 度量分析 (8 min)

```
AI 自动执行: 05_度量分析.md

AI 输出:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 度量分析结果
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KVC (键值一致性): N/A (无 Context 操作)
SCV (复杂度变化): 2.8 (✅ < 5.0)
测试覆盖率: 87% (✅ > 80%)

圈复杂度:
  - UserController: 平均 1.5
  - UserService: 平均 2.3
  - 最高: UserService.list() = 4

✅ 所有指标达标

度量数据已追加: .agent/metrics/history.csv
```

---

### Step 6: 质量关卡 (5 min)

```
AI 自动执行: 07_质量关卡.md

AI 输出:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 质量审查
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Evidence 审计:
  ✅ Compliance_Status = Pass
  ✅ P0_Violations = 0
  ✅ 测试覆盖率 87% > 80%

度量指标审查:
  ✅ KVC: N/A
  ✅ SCV: 2.8 < 5.0
  ✅ 复杂度: 最高 4 < 10

人工检查清单:
  ✅ 分页参数校验 - 已实现
  ✅ 用户名唯一性校验 - 已实现
  ✅ 删除前检查关联数据 - 已实现

质量评级: A 级 ✅

可以提交代码！
```

---

### Step 7: 提交代码

```bash
# 提交代码
git add .
git commit -m "feat: 实现用户管理 CRUD 功能

- 新增用户管理 Controller/Service/Mapper
- 完成增删改查功能
- 测试覆盖率 87%
- 质量评级: A 级

Evidence: 标准流程 (60 min)
"

git push origin feature/user-management
```

---

## 📊 最终成果

### 生成的代码

**UserController.java** (核心片段):
```java
@RestController
@RequestMapping("/api/users")
@Api(tags = "用户管理")
public class UserController {
    
    @Autowired
    private UserService userService;
    
    @PostMapping
    @ApiOperation("新增用户")
    public Result<Long> create(@RequestBody @Valid UserDTO dto) {
        Long id = userService.create(dto);
        return Result.success(id);
    }
    
    @GetMapping
    @ApiOperation("查询用户列表")
    public Result<PageInfo<UserDTO>> list(
        @RequestParam(defaultValue = "1") Integer pageNum,
        @RequestParam(defaultValue = "10") Integer pageSize
    ) {
        PageInfo<UserDTO> page = userService.list(pageNum, pageSize);
        return Result.success(page);
    }
    
    // ... 其他方法
}
```

### 测试文件

**UserControllerTest.java** (核心片段):
```java
@SpringBootTest
@AutoConfigureMockMvc
class UserControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    void testCreate() throws Exception {
        String json = "{\"username\":\"test\",\"email\":\"test@example.com\"}";
        
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content(json))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.code").value(200));
    }
    
    // ... 其他测试
}
```

---

## 🎯 关键要点

### 标准流程的优势
- ✅ 自动生成约束清单
- ✅ 实时约束检查
- ✅ 完整的测试覆盖
- ✅ 度量数据追踪
- ✅ 质量关卡保障

### 时间分配
| 步骤 | 预计 | 实际 | 说明 |
|------|------|------|------|
| 启动自检 | 5 min | 5 min | AI 自动完成 |
| 需求雷达 | 10 min | 10 min | 包含智能分流 |
| 规约形式化 | 8 min | 8 min | 自动生成 |
| 受控执行 | 25 min | 25 min | 代码+测试 |
| 度量分析 | 8 min | 8 min | 自动计算 |
| 质量关卡 | 5 min | 5 min | 人工审查 |
| **总计** | **61 min** | **61 min** | 符合预期 |

### 节省的时间
相比传统开发方式：
- ❌ 传统: 约 90 分钟（无约束检查、手动测试、缺少度量）
- ✅ 工作流: 61 分钟（自动化检查、完整测试、度量追踪）
- **节省**: 29 分钟 (32%)

---

## 💡 经验总结

### 做得好的地方
1. ✅ 智能分流准确（任务规模 1.6 → 标准流程）
2. ✅ 约束清单全面（P0/P1 分级清晰）
3. ✅ 测试覆盖充分（87% > 80%）
4. ✅ 度量指标达标（SCV 2.8 < 5.0）

### 可以改进的地方
1. ⚠️  P1 警告：UserDTO 缺少 @NotNull 注解（已修复）
2. 💡 建议：增加集成测试（端到端测试）

### 下次注意
- 在 DTO 定义时就加上校验注解
- 考虑增加异常场景测试

---

## 📚 相关资源

- [工作流文档](../workflows/)
- [约束清单模板](../templates/constraint-checklist-template.md)
- [Evidence 模板](../templates/evidence-block-template.md)

---

**示例版本**: v1.0
**最后更新**: 2026-06-23
