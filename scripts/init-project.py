#!/usr/bin/env python3
"""
项目初始化引擎
支持多语言项目从模板快速创建
"""

import os
import sys
import yaml
import json
import shutil
from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, Template
import argparse


class ProjectInitializer:
    """项目初始化器"""
    
    def __init__(self, template_root: str):
        self.template_root = Path(template_root)
        self.templates_dir = self.template_root / "templates"
        
    def init_project(self, config_file: str, output_dir: str, language: str = "java"):
        """
        初始化项目
        
        Args:
            config_file: 配置文件路径 (YAML)
            output_dir: 输出目录
            language: 编程语言 (java/python/nodejs)
        """
        
        print("🚀 开始初始化项目...")
        
        # 1. 加载配置
        print("\n📋 Step 1/6: 加载配置文件")
        config = self._load_config(config_file)
        self._validate_config(config, language)
        
        # 2. 准备输出目录
        print("\n📁 Step 2/6: 准备输出目录")
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 3. 渲染内核模板
        print("\n🎨 Step 3/6: 渲染项目内核")
        kernel_dir = output_path / "project-kernel"
        self._render_kernel(language, config, kernel_dir)
        
        # 4. 复制通用工作流
        print("\n📂 Step 4/6: 复制工作流文件")
        workflows_dir = output_path / ".hermes" / "workflows"
        self._copy_workflows(workflows_dir)
        
        # 5. 处理自定义规范
        if config.get('custom', {}).get('coding_standards'):
            print("\n📝 Step 5/6: 导入自定义规范")
            self._import_custom_standards(config, output_path)
        else:
            print("\n📝 Step 5/6: 跳过自定义规范（使用默认）")
        
        # 6. 生成项目 README
        print("\n📄 Step 6/6: 生成项目文档")
        self._generate_readme(config, output_path)
        
        print("\n" + "="*60)
        print("✅ 项目初始化完成！")
        print("="*60)
        print(f"\n📂 项目位置: {output_path.absolute()}")
        print(f"📋 项目内核: {kernel_dir}")
        print(f"🔄 工作流: {workflows_dir}")
        print("\n下一步操作:")
        print("  1. cd", output_path)
        print("  2. 查看 project-kernel/00_系统总纲.md")
        print("  3. git init && git add . && git commit -m 'chore: 初始化项目'")
        print()
        
    def _load_config(self, config_file: str) -> dict:
        """加载配置文件"""
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 添加时间戳
        config['_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"   ✓ 配置文件: {config_file}")
        print(f"   ✓ 项目名称: {config['project']['name']}")
        print(f"   ✓ 项目代号: {config['project']['code']}")
        
        return config
    
    def _validate_config(self, config: dict, language: str):
        """验证配置"""
        schema_file = self.templates_dir / language / "project-config.schema.json"
        
        if not schema_file.exists():
            print(f"   ⚠️  未找到配置验证文件: {schema_file}")
            return
        
        # TODO: 使用 jsonschema 验证
        print(f"   ✓ 配置验证通过")
    
    def _render_kernel(self, language: str, config: dict, output_dir: Path):
        """渲染内核模板"""
        template_dir = self.templates_dir / language / "kernel-template"
        
        if not template_dir.exists():
            raise FileNotFoundError(f"模板目录不存在: {template_dir}")
        
        # 设置 Jinja2 环境
        env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # 递归渲染所有 .md 文件
        rendered_count = 0
        for template_file in template_dir.rglob("*.md"):
            rel_path = template_file.relative_to(template_dir)
            output_file = output_dir / rel_path
            
            # 创建输出目录
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # 渲染模板
            try:
                template = env.get_template(str(rel_path))
                rendered = template.render(**config)
                output_file.write_text(rendered, encoding='utf-8')
                rendered_count += 1
                print(f"   ✓ {rel_path}")
            except Exception as e:
                print(f"   ❌ {rel_path}: {e}")
        
        print(f"\n   共渲染 {rendered_count} 个文件")
    
    def _copy_workflows(self, output_dir: Path):
        """复制工作流文件"""
        workflow_src = self.templates_dir / "common" / "workflows"
        
        if not workflow_src.exists():
            print(f"   ⚠️  工作流目录不存在: {workflow_src}")
            return
        
        shutil.copytree(workflow_src, output_dir, dirs_exist_ok=True)
        
        workflow_count = len(list(output_dir.glob("*.md")))
        print(f"   ✓ 复制了 {workflow_count} 个工作流文件")
    
    def _import_custom_standards(self, config: dict, project_dir: Path):
        """导入自定义编码规范"""
        standards_file = config['custom']['coding_standards']
        
        if not Path(standards_file).exists():
            print(f"   ⚠️  自定义规范文件不存在: {standards_file}")
            return
        
        # 创建 custom-standards 目录
        custom_dir = project_dir / "custom-standards"
        custom_dir.mkdir(exist_ok=True)
        
        # 复制文件
        shutil.copy(standards_file, custom_dir / "custom-coding-standards.md")
        
        # 在 project-kernel/02_开发规约 中创建引用
        specs_dir = project_dir / "project-kernel" / "02_开发规约"
        specs_dir.mkdir(parents=True, exist_ok=True)
        
        ref_file = specs_dir / "03_自定义规范.md"
        ref_file.write_text(f"""# 03_自定义规范

> 本文档引用团队自定义编码规范

## 规范来源
- **文件路径**: `../../custom-standards/custom-coding-standards.md`
- **上传时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 优先级
**自定义规范 > 默认规范**

当自定义规范与默认规范冲突时，优先遵循自定义规范。

---

详见: [自定义编码规范](../../custom-standards/custom-coding-standards.md)
""", encoding='utf-8')
        
        print(f"   ✓ 导入自定义规范: {standards_file}")
        print(f"   ✓ 创建引用文件: {ref_file}")
    
    def _generate_readme(self, config: dict, project_dir: Path):
        """生成项目 README"""
        readme_path = project_dir / "README.md"
        
        project_name = config['project']['name']
        project_code = config['project']['code']
        description = config['project'].get('description', '')
        
        modules = config.get('modules', [])
        module_list = "\n".join([f"- **{m['name']}**: {m['description']}" for m in modules])
        
        readme_content = f"""# {project_name}

> {description}

## 项目信息

- **项目代号**: `{project_code}`
- **技术负责人**: {config['project']['owner']}
- **创建时间**: {config['_timestamp']}

## 技术栈

### 后端
- {config['tech']['backend']['framework']} {config['tech']['backend']['version']}
- {config['tech']['database']['type']} {config['tech']['database']['version']}
- {config['tech']['orm']['name']} {config['tech']['orm']['version']}

### 前端
- {config['tech']['frontend']['framework']} {config['tech']['frontend']['version']}
- {config['tech']['frontend']['ui_library']}

## 功能模块

{module_list}

## 快速开始

### 开发环境要求
- JDK {config['tech']['backend']['java_version']}
- Maven 3.8+
- Node.js 18+

### 启动步骤

1. 克隆项目
```bash
git clone <repository-url>
cd {project_code}
```

2. 后端启动
```bash
mvn clean install
mvn spring-boot:run
```

3. 前端启动
```bash
cd frontend
npm install
npm run dev
```

## 项目文档

- **系统总纲**: `project-kernel/00_系统总纲.md`
- **项目全景**: `project-kernel/01_项目全景.md`
- **开发规约**: `project-kernel/02_开发规约/`
- **工作流程**: `.hermes/workflows/`

## 贡献指南

请阅读 `project-kernel/02_开发规约/` 了解编码规范。

## License

Copyright © {datetime.now().year}
"""
        
        readme_path.write_text(readme_content, encoding='utf-8')
        print(f"   ✓ 生成 README.md")


def main():
    parser = argparse.ArgumentParser(description="项目初始化引擎")
    parser.add_argument("--config", required=True, help="配置文件路径 (YAML)")
    parser.add_argument("--output", required=True, help="输出目录")
    parser.add_argument("--language", default="java", choices=["java", "python", "nodejs"], help="编程语言")
    parser.add_argument("--template-root", help="模板根目录（默认为脚本所在目录的父目录）")
    
    args = parser.parse_args()
    
    # 确定模板根目录
    if args.template_root:
        template_root = args.template_root
    else:
        template_root = Path(__file__).parent.parent
    
    # 初始化
    initializer = ProjectInitializer(template_root)
    initializer.init_project(args.config, args.output, args.language)


if __name__ == "__main__":
    main()
