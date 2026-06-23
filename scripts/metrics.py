#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
度量脚本 - 自动计算 KVC/SCV 指标

用途：
- 自动计算 KVC（键值一致性）
- 自动计算 SCV（复杂度变化）
- 生成度量报告

使用：
    python metrics.py <project-path>

示例：
    python metrics.py /path/to/project
"""

import os
import sys
import re
import csv
from datetime import datetime
from pathlib import Path

# 配置
KVC_THRESHOLD = 0.90  # KVC 阈值
SCV_THRESHOLD = 5.0   # SCV 阈值


def calculate_kvc(project_path):
    """
    计算 KVC（键值一致性）
    
    规则：检查 context.put() 调用是否符合 node:{nodeId} 格式
    """
    print("\n📊 计算 KVC（键值一致性）...")
    
    total_keys = 0
    compliant_keys = 0
    violations = []
    
    # 搜索所有 Java 文件
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.java'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # 查找所有 context.put() 调用
                    pattern = r'context\.put\s*\(\s*"([^"]+)"'
                    matches = re.finditer(pattern, content)
                    
                    for match in matches:
                        key = match.group(1)
                        total_keys += 1
                        
                        # 检查是否符合 node:{nodeId} 格式
                        if key.startswith('node:'):
                            compliant_keys += 1
                        else:
                            line_num = content[:match.start()].count('\n') + 1
                            violations.append({
                                'file': os.path.relpath(filepath, project_path),
                                'line': line_num,
                                'key': key,
                                'expected': f'node:{key}'
                            })
                except Exception as e:
                    print(f"⚠️  读取文件失败: {filepath} - {e}")
    
    # 计算 KVC
    kvc = compliant_keys / total_keys if total_keys > 0 else 1.0
    
    print(f"\n总 Key 数量: {total_keys}")
    print(f"符合规范: {compliant_keys}")
    print(f"违规: {len(violations)}")
    print(f"KVC = {compliant_keys} / {total_keys} = {kvc:.2f}")
    
    # 判断是否达标
    if kvc >= KVC_THRESHOLD:
        print(f"✅ KVC 达标 (≥ {KVC_THRESHOLD})")
    else:
        print(f"❌ KVC 未达标 (< {KVC_THRESHOLD})")
        print(f"\n违规详情:")
        for v in violations[:10]:  # 只显示前10个
            print(f"  - {v['file']}:{v['line']}")
            print(f"    当前: context.put(\"{v['key']}\", ...)")
            print(f"    应为: context.put(\"{v['expected']}\", ...)")
    
    return kvc, violations


def calculate_scv(project_path):
    """
    计算 SCV（复杂度变化）
    
    支持多种工具：
    1. radon（Python）
    2. lizard（多语言，包括 Java）
    3. 手动计算（基于方法行数）
    """
    print("\n📊 计算 SCV（复杂度变化）...")
    
    complexity_data = []
    
    # 方法1: 尝试使用 lizard（推荐，支持 Java）
    try:
        import subprocess
        result = subprocess.run(
            ['lizard', project_path, '-l', 'java'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ 使用 lizard 分析 Java 代码")
            lines = result.stdout.split('\n')
            
            # 解析 lizard 输出
            for line in lines:
                if '.java' in line and not line.startswith('='):
                    parts = line.split()
                    if len(parts) >= 4:
                        try:
                            complexity = int(parts[0])
                            nloc = int(parts[1])
                            function_name = parts[3] if len(parts) > 3 else 'unknown'
                            file_path = parts[-1] if len(parts) > 4 else 'unknown'
                            
                            complexity_data.append({
                                'file': file_path,
                                'function': function_name,
                                'complexity': complexity,
                                'nloc': nloc
                            })
                        except (ValueError, IndexError):
                            continue
            
            if complexity_data:
                avg_complexity = sum(d['complexity'] for d in complexity_data) / len(complexity_data)
                print(f"✅ 分析了 {len(complexity_data)} 个方法")
                print(f"平均圈复杂度: {avg_complexity:.2f}")
                
                # 找出复杂度最高的方法
                top_complex = sorted(complexity_data, key=lambda x: x['complexity'], reverse=True)[:5]
                print(f"\n🔴 复杂度最高的 5 个方法:")
                for item in top_complex:
                    print(f"  - {item['function']}: {item['complexity']} ({item['file']})")
                
                if avg_complexity < SCV_THRESHOLD:
                    print(f"✅ SCV 达标 (< {SCV_THRESHOLD})")
                else:
                    print(f"❌ SCV 超标 (≥ {SCV_THRESHOLD})")
                
                return avg_complexity, complexity_data
    
    except FileNotFoundError:
        print("ℹ️  未安装 lizard")
    except subprocess.TimeoutExpired:
        print("⚠️  lizard 执行超时")
    except Exception as e:
        print(f"⚠️  lizard 执行失败: {e}")
    
    # 方法2: 尝试使用 radon（仅支持 Python）
    try:
        from radon.complexity import cc_visit
        
        print("✅ 使用 radon 分析 Python 代码")
        
        # 搜索所有 Python 文件
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        results = cc_visit(content)
                        for result in results:
                            complexity_data.append({
                                'file': os.path.relpath(filepath, project_path),
                                'function': result.name,
                                'complexity': result.complexity
                            })
                    except Exception:
                        pass
        
        if complexity_data:
            avg_complexity = sum(d['complexity'] for d in complexity_data) / len(complexity_data)
            print(f"✅ 分析了 {len(complexity_data)} 个函数")
            print(f"平均圈复杂度: {avg_complexity:.2f}")
            
            if avg_complexity < SCV_THRESHOLD:
                print(f"✅ SCV 达标 (< {SCV_THRESHOLD})")
            else:
                print(f"❌ SCV 超标 (≥ {SCV_THRESHOLD})")
            
            return avg_complexity, complexity_data
    
    except ImportError:
        print("ℹ️  未安装 radon")
    
    # 方法3: 简易方法（统计方法行数作为复杂度估算）
    print("ℹ️  使用简易方法估算复杂度（基于方法行数）")
    
    # 搜索所有 Java 文件
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.java'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    # 简单识别方法（public/private/protected 开头，包含括号）
                    in_method = False
                    method_start = 0
                    method_name = 'unknown'
                    
                    for i, line in enumerate(lines):
                        stripped = line.strip()
                        
                        # 方法定义
                        if any(keyword in stripped for keyword in ['public ', 'private ', 'protected ']) and '(' in stripped and '{' in stripped:
                            in_method = True
                            method_start = i
                            # 提取方法名
                            try:
                                parts = stripped.split('(')[0].split()
                                method_name = parts[-1] if parts else 'unknown'
                            except:
                                method_name = 'unknown'
                        
                        # 方法结束
                        if in_method and stripped == '}':
                            method_lines = i - method_start
                            # 简单估算：每 10 行代码 ≈ 复杂度 1
                            estimated_complexity = max(1, method_lines // 10)
                            
                            complexity_data.append({
                                'file': os.path.relpath(filepath, project_path),
                                'function': method_name,
                                'complexity': estimated_complexity,
                                'nloc': method_lines
                            })
                            
                            in_method = False
                
                except Exception as e:
                    pass
    
    if not complexity_data:
        print("ℹ️  未找到可分析的代码文件")
        return None, []
    
    # 计算平均复杂度
    avg_complexity = sum(d['complexity'] for d in complexity_data) / len(complexity_data)
    
    print(f"✅ 估算了 {len(complexity_data)} 个方法")
    print(f"平均复杂度（估算）: {avg_complexity:.2f}")
    print("💡 建议安装 lizard 以获得更准确的复杂度分析:")
    print("   pip install lizard")
    
    if avg_complexity < SCV_THRESHOLD:
        print(f"✅ SCV 达标 (< {SCV_THRESHOLD})")
    else:
        print(f"❌ SCV 超标 (≥ {SCV_THRESHOLD})")
    
    return avg_complexity, complexity_data


def generate_report(project_path, kvc, scv, violations):
    """
    生成度量报告
    """
    print("\n📝 生成度量报告...")
    
    # 创建 metrics 目录
    metrics_dir = os.path.join(project_path, '.agent', 'metrics')
    os.makedirs(metrics_dir, exist_ok=True)
    
    # 生成报告文件
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = os.path.join(metrics_dir, f'report_{timestamp}.md')
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"# 度量报告\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write(f"## KVC（键值一致性）\n\n")
        f.write(f"- **得分**: {kvc:.2f}\n")
        f.write(f"- **阈值**: {KVC_THRESHOLD}\n")
        f.write(f"- **状态**: {'✅ 达标' if kvc >= KVC_THRESHOLD else '❌ 未达标'}\n\n")
        
        if violations:
            f.write(f"### 违规详情（共 {len(violations)} 个）\n\n")
            for v in violations[:20]:
                f.write(f"- `{v['file']}:{v['line']}` - 当前: `{v['key']}` → 应为: `{v['expected']}`\n")
        
        if scv is not None:
            f.write(f"\n## SCV（复杂度变化）\n\n")
            f.write(f"- **平均复杂度**: {scv:.2f}\n")
            f.write(f"- **阈值**: {SCV_THRESHOLD}\n")
            f.write(f"- **状态**: {'✅ 达标' if scv < SCV_THRESHOLD else '❌ 超标'}\n\n")
    
    print(f"✅ 报告已生成: {report_file}")
    
    # 追加到历史 CSV
    history_file = os.path.join(metrics_dir, 'history.csv')
    file_exists = os.path.exists(history_file)
    
    with open(history_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['date', 'module', 'kvc', 'scv', 'coverage', 'status'])
        
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d'),
            'project',
            f"{kvc:.2f}",
            f"{scv:.2f}" if scv else "N/A",
            "N/A",
            "PASS" if kvc >= KVC_THRESHOLD else "FAIL"
        ])
    
    print(f"✅ 历史数据已追加: {history_file}")


def main():
    if len(sys.argv) < 2:
        print("用法: python metrics.py <project-path>")
        sys.exit(1)
    
    project_path = sys.argv[1]
    
    if not os.path.exists(project_path):
        print(f"❌ 项目路径不存在: {project_path}")
        sys.exit(1)
    
    print(f"🔍 开始分析项目: {project_path}")
    
    # 计算 KVC
    kvc, violations = calculate_kvc(project_path)
    
    # 计算 SCV
    scv, complexity_data = calculate_scv(project_path)
    
    # 生成报告
    generate_report(project_path, kvc, scv, violations)
    
    print("\n✅ 度量分析完成！")


if __name__ == '__main__':
    main()
