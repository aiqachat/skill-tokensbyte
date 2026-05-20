
# Plugin-Skill

基于字节跳动豆包 AI 模型的技能集合，集成图片生成和视频生成功能。

## 项目简介

本项目提供了一组 OpenClaw 技能，用于 AI 内容生成，包括：

- **图片生成**：基于 doubao-seedream-5-0 模型的高质量图像创作
- **视频生成**：基于 doubao-seedance-2-0 模型的多模态视频生成
- **提示词优化**：Seedance 2.0 提示词工程化优化工具

## 技能列表

### 1. doubao-seedream-5-0

使用最新的 doubao-seedream-5-0-260128 模型生成高质量图片。

**功能特性**：
- 文生图：从详细的文本描述生成图片
- 图生图：基于参考图片生成新图片
- 多图融合：融合多张图片的特征
- 图生组图：生成一组连续的图片
- 联网搜索：结合实时信息生成图片
- 多种尺寸：支持 2K、4K、自定义宽高

**详细文档**：[doubao-seedream-5-0/SKILL.md](doubao-seedream-5-0/SKILL.md)

### 2. doubao-seedance-2-0

使用新一代多模态视频模型，支持视频生成和编辑。

**功能特性**：
- 文生视频：从文本描述生成视频
- 图生视频：基于参考图片生成视频
- 多模态参考：同时使用图片、视频、音频
- 视频延长：延长已生成的视频
- 视频编辑：编辑已生成的视频
- 联网搜索：结合实时信息生成视频
- 有声视频：自动生成同步音频

**详细文档**：[doubao-seedance-2-0/SKILL.md](doubao-seedance-2-0/SKILL.md)

### 3. Demo 技能

演示技能目录，包含：
- byted-seedream-image-generate-1.0.0：图片生成演示
- seedance-video-gen-1.0.1：视频生成演示
- sd2-pe：提示词优化器

## 安装与配置

### 前置要求

- Python 3.8+
- OpenClaw agent 环境
- Volcengine Ark API Key

### API Key 配置

```bash
# 配置图片生成 API Key
export ARTS_API_KEY="your-api-key-here"

# 配置视频生成 API Key
export ARK_API_KEY="your-api-key-here"

# 可选：配置 API Base URL
export ARTS_API_BASE="https://apis.artsapi.com/v1"
```

## 快速开始

### 图片生成

```bash
cd doubao-seedream-5-0/scripts
python seedream_5_0_generate.py -p "一只可爱的橘猫在阳光下打滚玩耍" --size 2K
```

### 视频生成

```bash
cd doubao-seedance-2-0/scripts
python seedance_2_0_generate.py create --prompt "一只可爱的橘猫在阳光下打滚玩耍" --resolution 720p --wait
```

## 目录结构

```
plugin-skill/
├── doubao-seedream-5-0/          # 图片生成技能
│   ├── scripts/
│   │   └── seedream_5_0_generate.py
│   ├── SKILL.md
│   └── _meta.json
├── doubao-seedance-2-0/          # 视频生成技能
│   ├── scripts/
│   │   └── seedance_2_0_generate.py
│   ├── SKILL.md
│   └── _meta.json
├── demo/                         # 演示技能
│   ├── byted-seedream-image-generate-1.0.0/
│   ├── seedance-video-gen-1.0.1/
│   └── SKILL.md
├── README.md                     # 项目说明
└── UPDATE.md                     # 更新日志
```

## 许可证

本项目使用 Apache License 2.0 许可证。

## 注意事项

- 生成的图片/视频 URL 通常有 24 小时有效期，请及时下载保存
- 使用本技能时请遵守相关法律法规和服务条款
- 详细使用说明请参考各技能目录下的 SKILL.md 文件

