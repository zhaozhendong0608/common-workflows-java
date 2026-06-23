#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动归档脚本 - 从会话中提取内容并归档到项目

用途：
- 自动提取 SQL 脚本
- 自动识别技术讨论并生成 ADR 草稿
- 自动补充 FAQ
- 自动保存代码片段

使用：
    python auto-archive.py [--session-file <file>] [--project-root <path>]
"""

import os
import sys
import re
import json
from datetime import datetime
from pathlib import Path

# 配置
DEFAULT_SESSION_FILE = "session.log"  # 会话记录文件
PROJECT_ROOT = os.getcwd()

class ArchiveManager:
    def __init__(self, session_file, project_root):
        self.session_file = session_file
        self.project_root = project_root
        self.session_content = self._read_session()
        
        # 归档目录
        self.docs_dir = os.path.join(project_root, 'docs')
        self.kernel_dir = os.path.join(project_root, 'project-kernel')
        self.migrations_dir = os.path.join(self.kernel_dir, 'db', 'migrations')
        self.adr_dir = os.path.join(self.kernel_dir, '03_决策日志')
        self.snippets_dir = os.path.join(self.kernel_dir, 'snippets')
        
        # 创建目录
        self._ensure_dirs()
    
    def _read_session(self):
        """读取会话内容"""
        if not os.path.exists(self.session_file):
            print(f"⚠️  会话文件不存在: {self.session_file}")
            print("💡 提示：手动复制对话内容到 session.log")
            return ""
        
        with open(self.session_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _ensure_dirs(self):
        """确保目录存在"""
        for d in [self.docs_dir, self.migrations_dir, self.adr_dir, self.snippets_dir]:
            os.makedirs(d, exist_ok=True)
    
    def extract_sql_scripts(self):
        """提取 SQL 脚本"""
        print("\n🔍 搜索 SQL 脚本...")
        
        # 匹配 ```sql ... ``` 代码块
        sql_pattern = r'```sql\n(.*?)\n```'
        matches = re.finditer(sql_pattern, self.session_content, re.DOTALL)
        
        sql_scripts = []
        for i, match in enumerate(matches, 1):
            sql_content = match.group(1).strip()
            sql_scripts.append({
                'index': i,
                'content': sql_content,
                'context': self._extract_context(match.start(), 200)
            })
        
        if not sql_scripts:
            print("  ℹ️  未找到 SQL 脚本")
            return
        
        print(f"  ✅ 找到 {len(sql_scripts)} 个 SQL 脚本")
        
        # 保存 SQL 脚本
        for script in sql_scripts:
            self._save_sql_script(script)
    
    def _extract_context(self, position, length=200):
        """提取上下文"""
        start = max(0, position - length)
        end = min(len(self.session_content), position + length)
        context = self.session_content[start:end]
        return context.replace('\n', ' ').strip()
    
    def _save_sql_script(self, script):
        """保存 SQL 脚本"""
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"V{timestamp}__session_migration_{script['index']}.sql"
        filepath = os.path.join(self.migrations_dir, filename)
        
        # 生成内容（带注释）
        header = f"""-- Migration from session
-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- Context: {script['context'][:100]}...

"""
        content = header + script['content']
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  📄 已保存: {filename}")
    
    def extract_technical_discussions(self):
        """提取技术讨论并生成 ADR 草稿"""
        print("\n🔍 搜索技术讨论...")
        
        # 识别技术决策关键词
        decision_keywords = [
            r'选择.*(?:而不是|vs|对比)',
            r'为什么.*(?:采用|使用)',
            r'技术选型',
            r'方案.*(?:对比|选择)',
            r'ADR',
        ]
        
        discussions = []
        for keyword in decision_keywords:
            matches = re.finditer(keyword, self.session_content, re.IGNORECASE)
            for match in matches:
                context = self._extract_context(match.start(), 500)
                discussions.append({
                    'keyword': keyword,
                    'context': context,
                    'position': match.start()
                })
        
        if not discussions:
            print("  ℹ️  未找到技术讨论")
            return
        
        print(f"  ✅ 找到 {len(discussions)} 处技术讨论")
        
        # 生成 ADR 草稿
        self._generate_adr_draft(discussions)
    
    def _generate_adr_draft(self, discussions):
        """生成 ADR 草稿"""
        # 获取下一个 ADR 编号
        adr_num = self._get_next_adr_number()
        
        timestamp = datetime.now().strftime('%Y-%m-%d')
        filename = f"ADR-{adr_num:03d}-会话讨论_{timestamp}.md"
        filepath = os.path.join(self.adr_dir, filename)
        
        # 生成内容
        content = f"""# ADR-{adr_num:03d}: 会话中的技术讨论

**状态**: 草稿 (需要人工整理)
**日期**: {timestamp}
**决策者**: 待填写

---

## 背景

在会话中讨论了以下技术问题：

"""
        
        for i, disc in enumerate(discussions[:5], 1):  # 只取前5个
            content += f"\n### 讨论 {i}\n\n"
            content += f"**上下文**:\n```\n{disc['context']}\n```\n"
        
        content += """

---

## 决策

**待整理**: 请根据上述讨论内容，补充具体决策

---

## 理由

**待整理**: 请补充决策理由

---

## 后果

**待整理**: 请补充决策后果和影响

---

**📝 提示**: 这是自动生成的 ADR 草稿，请根据实际情况修改和完善。
"""
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  📄 已生成 ADR 草稿: {filename}")
        print(f"  💡 请手工编辑完善: {filepath}")
    
    def _get_next_adr_number(self):
        """获取下一个 ADR 编号"""
        if not os.path.exists(self.adr_dir):
            return 1
        
        # 扫描现有 ADR
        adr_pattern = r'ADR-(\d+)'
        max_num = 0
        
        for filename in os.listdir(self.adr_dir):
            match = re.match(adr_pattern, filename)
            if match:
                num = int(match.group(1))
                max_num = max(max_num, num)
        
        return max_num + 1
    
    def extract_code_snippets(self):
        """提取代码片段"""
        print("\n🔍 搜索代码片段...")
        
        # 匹配各种语言的代码块
        code_patterns = {
            'java': r'```java\n(.*?)\n```',
            'python': r'```python\n(.*?)\n```',
            'javascript': r'```(?:javascript|js)\n(.*?)\n```',
            'bash': r'```(?:bash|sh)\n(.*?)\n```',
        }
        
        snippets = []
        for lang, pattern in code_patterns.items():
            matches = re.finditer(pattern, self.session_content, re.DOTALL)
            for match in matches:
                code = match.group(1).strip()
                # 只保存有意义的代码（> 3 行）
                if code.count('\n') >= 2:
                    snippets.append({
                        'language': lang,
                        'code': code,
                        'context': self._extract_context(match.start(), 150)
                    })
        
        if not snippets:
            print("  ℹ️  未找到代码片段")
            return
        
        print(f"  ✅ 找到 {len(snippets)} 个代码片段")
        
        # 保存代码片段
        for snippet in snippets:
            self._save_code_snippet(snippet)
    
    def _save_code_snippet(self, snippet):
        """保存代码片段"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{snippet['language']}_snippet.{self._get_extension(snippet['language'])}"
        filepath = os.path.join(self.snippets_dir, filename)
        
        # 生成内容（带注释）
        comment_prefix = self._get_comment_prefix(snippet['language'])
        header = f"""{comment_prefix} Code snippet from session
{comment_prefix} Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{comment_prefix} Context: {snippet['context'][:80]}...

"""
        content = header + snippet['code']
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  📄 已保存: {filename}")
    
    def _get_extension(self, language):
        """获取文件扩展名"""
        extensions = {
            'java': 'java',
            'python': 'py',
            'javascript': 'js',
            'bash': 'sh',
        }
        return extensions.get(language, 'txt')
    
    def _get_comment_prefix(self, language):
        """获取注释前缀"""
        prefixes = {
            'java': '//',
            'python': '#',
            'javascript': '//',
            'bash': '#',
        }
        return prefixes.get(language, '#')
    
    def generate_session_summary(self):
        """生成会话摘要"""
        print("\n📝 生成会话摘要...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"session_summary_{timestamp}.md"
        filepath = os.path.join(self.docs_dir, filename)
        
        # 统计信息
        sql_count = len(re.findall(r'```sql', self.session_content))
        code_count = len(re.findall(r'```(?:java|python|javascript)', self.session_content))
        
        content = f"""# 会话摘要

**日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**归档时间**: {timestamp}

---

## 📊 统计

- SQL 脚本: {sql_count} 个
- 代码片段: {code_count} 个
- 会话长度: {len(self.session_content)} 字符

---

## 📁 归档位置

- **SQL 脚本**: `project-kernel/db/migrations/`
- **ADR 草稿**: `project-kernel/03_决策日志/`
- **代码片段**: `project-kernel/snippets/`
- **会话摘要**: `docs/session_summary_{timestamp}.md`

---

## 💡 后续操作

1. 检查并完善 ADR 草稿
2. 审查自动生成的 SQL 脚本
3. 整理代码片段
4. 提交到 Git

---

**生成工具**: auto-archive.py
"""
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 已保存摘要: {filename}")
    
    def run(self):
        """执行归档流程"""
        print("=" * 60)
        print("📦 自动归档系统")
        print("=" * 60)
        
        if not self.session_content:
            print("\n❌ 无法读取会话内容")
            print("\n💡 使用方法:")
            print("   1. 复制对话内容到 session.log")
            print("   2. 运行: python auto-archive.py")
            return
        
        print(f"\n📂 项目根目录: {self.project_root}")
        print(f"📄 会话文件: {self.session_file}")
        print(f"📏 会话长度: {len(self.session_content)} 字符")
        
        # 执行各种提取
        self.extract_sql_scripts()
        self.extract_technical_discussions()
        self.extract_code_snippets()
        self.generate_session_summary()
        
        print("\n" + "=" * 60)
        print("✅ 归档完成！")
        print("=" * 60)
        
        print("\n📋 后续操作:")
        print("1. 审查自动生成的文件")
        print("2. 完善 ADR 草稿")
        print("3. 提交到 Git:")
        print("   git add project-kernel/ docs/")
        print("   git commit -m 'chore: 归档会话内容'")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='自动归档会话内容')
    parser.add_argument('--session-file', default='session.log', 
                       help='会话记录文件路径')
    parser.add_argument('--project-root', default='.', 
                       help='项目根目录')
    
    args = parser.parse_args()
    
    manager = ArchiveManager(args.session_file, args.project_root)
    manager.run()


if __name__ == '__main__':
    main()
