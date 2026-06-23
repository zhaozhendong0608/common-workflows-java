#!/bin/bash
# 约束检查脚本 - 自动检查项目是否符合约束清单

set -e

PROJECT_PATH="${1:-.}"
CONSTRAINT_FILE="${PROJECT_PATH}/.agent/constraint-checklist.yml"

echo "🔍 约束检查脚本"
echo "项目路径: ${PROJECT_PATH}"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 计数器
P0_VIOLATIONS=0
P1_WARNINGS=0
P2_INFO=0

# P0 约束检查：Context Key 格式
echo "📋 P0-001: 检查 Context Key 格式（必须为 node:{nodeId}）"
if grep -rn 'context\.put' "${PROJECT_PATH}/src" 2>/dev/null | grep -v 'node:' > /tmp/p0_001.txt; then
    COUNT=$(wc -l < /tmp/p0_001.txt)
    P0_VIOLATIONS=$((P0_VIOLATIONS + COUNT))
    echo -e "${RED}❌ 发现 ${COUNT} 个违规${NC}"
    head -5 /tmp/p0_001.txt
    if [ $COUNT -gt 5 ]; then
        echo "   ... 还有 $((COUNT - 5)) 个违规（详见 /tmp/p0_001.txt）"
    fi
else
    echo -e "${GREEN}✅ 通过${NC}"
fi
echo ""

# P0 约束检查：继承 BaseAlgoComponent
echo "📋 P0-002: 检查算子是否继承 BaseAlgoComponent"
if find "${PROJECT_PATH}/src" -name "*Operator.java" -type f 2>/dev/null | while read file; do
    if ! grep -q 'extends BaseAlgoComponent' "$file"; then
        echo "$file"
    fi
done > /tmp/p0_002.txt && [ -s /tmp/p0_002.txt ]; then
    COUNT=$(wc -l < /tmp/p0_002.txt)
    P0_VIOLATIONS=$((P0_VIOLATIONS + COUNT))
    echo -e "${RED}❌ 发现 ${COUNT} 个违规${NC}"
    cat /tmp/p0_002.txt
else
    echo -e "${GREEN}✅ 通过${NC}"
fi
echo ""

# P0 约束检查：使用 @AlgoOperator 注解
echo "📋 P0-003: 检查算子是否使用 @AlgoOperator 注解"
if find "${PROJECT_PATH}/src" -name "*Operator.java" -type f 2>/dev/null | while read file; do
    if ! grep -q '@AlgoOperator' "$file"; then
        echo "$file"
    fi
done > /tmp/p0_003.txt && [ -s /tmp/p0_003.txt ]; then
    COUNT=$(wc -l < /tmp/p0_003.txt)
    P0_VIOLATIONS=$((P0_VIOLATIONS + COUNT))
    echo -e "${RED}❌ 发现 ${COUNT} 个违规${NC}"
    cat /tmp/p0_003.txt
else
    echo -e "${GREEN}✅ 通过${NC}"
fi
echo ""

# P1 约束检查：变量驼峰命名
echo "📋 P1-001: 检查变量驼峰命名"
if grep -rn 'private.*[A-Z_][A-Z_]' "${PROJECT_PATH}/src" --include="*.java" 2>/dev/null | head -5 > /tmp/p1_001.txt && [ -s /tmp/p1_001.txt ]; then
    COUNT=$(wc -l < /tmp/p1_001.txt)
    P1_WARNINGS=$((P1_WARNINGS + COUNT))
    echo -e "${YELLOW}⚠️  发现 ${COUNT} 个警告${NC}"
    cat /tmp/p1_001.txt
else
    echo -e "${GREEN}✅ 通过${NC}"
fi
echo ""

# P1 约束检查：方法注释完整
echo "📋 P1-002: 检查方法注释完整性"
if find "${PROJECT_PATH}/src" -name "*.java" -type f 2>/dev/null | while read file; do
    # 查找 public 方法但没有 Javadoc 的情况
    awk '/public.*\(.*\).*{/ {if (!prev) print FILENAME":"NR":"$0} {prev=/\/\*\*/}' "$file"
done > /tmp/p1_002.txt && [ -s /tmp/p1_002.txt ]; then
    COUNT=$(wc -l < /tmp/p1_002.txt)
    P1_WARNINGS=$((P1_WARNINGS + COUNT))
    echo -e "${YELLOW}⚠️  发现 ${COUNT} 个警告（部分方法缺少注释）${NC}"
else
    echo -e "${GREEN}✅ 通过${NC}"
fi
echo ""

# P2 约束检查：代码风格统一
echo "📋 P2-001: 检查代码风格统一（需要 checkstyle）"
if command -v checkstyle &> /dev/null; then
    if checkstyle -c /google_checks.xml "${PROJECT_PATH}/src" 2>/dev/null | grep "Checkstyle ends" > /tmp/p2_001.txt; then
        echo -e "${GREEN}✅ 代码风格检查通过${NC}"
    else
        echo -e "${YELLOW}ℹ️  发现代码风格问题（可选修复）${NC}"
    fi
else
    echo -e "${YELLOW}ℹ️  未安装 checkstyle，跳过检查${NC}"
fi
echo ""

# 生成报告
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 约束检查汇总"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "P0 违规（强制）: ${RED}${P0_VIOLATIONS}${NC}"
echo -e "P1 警告（建议）: ${YELLOW}${P1_WARNINGS}${NC}"
echo -e "P2 信息（可选）: ${P2_INFO}"
echo ""

if [ $P0_VIOLATIONS -gt 0 ]; then
    echo -e "${RED}❌ 约束检查失败：存在 P0 级违规${NC}"
    exit 1
else
    echo -e "${GREEN}✅ 约束检查通过：无 P0 级违规${NC}"
    if [ $P1_WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠️  建议修复 ${P1_WARNINGS} 个 P1 级警告${NC}"
    fi
    exit 0
fi
