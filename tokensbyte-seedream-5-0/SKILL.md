---
name: doubao-seedream-5-0
description: 使用最新的 doubao-seedream-5-0-260128 模型生成高质量图片，支持文生图、图生图、多图融合、联网搜索等功能
license: Apache-2.0
tags: ["image-generation", "seedream", "doubao-seedream-5-0", "ai-art", "text-to-image", "image-to-image"]
---

# doubao-seedream-5-0 Image Generation

## Description

使用最新的 doubao-seedream-5-0-260128 模型生成高质量图片。Seedream 5.0 是新一代图像创作模型，精准解析复杂指令，支持文生图、图生图、多图融合、联网搜索等功能。

## When to Use This Skill

Use this skill when:
- 用户想要从文本描述生成图片
- 用户需要基于参考图片生成新图片
- 用户想要融合多张图片的特征
- 用户需要生成多张连续图片
- 用户想要结合实时信息生成图片（联网搜索）
- 用户需要高质量的艺术创作

## Features

- **文生图**：从详细的文本描述生成高质量图片
- **图生图**：基于参考图片生成新图片
- **多图融合**：融合多张图片的特征
- **图生组图**：生成一组连续的图片
- **联网搜索**：支持实时信息获取（通过 tools 参数）
- **多种尺寸**：支持 2K、4K、自定义宽高等多种尺寸
- **水印控制**：可选择是否添加水印
- **多种响应格式**：支持 URL 和 Base64 两种格式

## Installation & Setup

### Prerequisites

```bash
# Required: API Key 配置
export ARTS_API_KEY="your-api-key-here"

# Optional: API Base URL（默认已配置）
export ARTS_API_BASE="https://ai.artsapi.com/v1"
```

脚本会优先使用环境变量配置。

## Usage

### 基础用法

```bash
cd scripts
python seedream_5_0_generate.py -p "一只可爱的橘猫在阳光下打滚玩耍"
```

### 文生图

```bash
python seedream_5_0_generate.py -p "星际穿越,黑洞,黑洞里冲出一辆快支离破碎的复古列车,抢视觉冲击力,电影大片,末日既视感,动感,对比色,oc渲染,光线追踪,动态模糊,景深,超现实主义,深蓝" --size 2K --no-watermark
```

### 图生图

```bash
python seedream_5_0_generate.py -p "生成狗狗趴在草地上的近景画面" -i "https://example.com/reference.jpg" --size 2K
```

### 图生组图

```bash
python seedream_5_0_generate.py -p "生成3张女孩和奶牛玩偶在游乐园开心地坐过山车的图片,涵盖早晨、中午、晚上" -i "https://example.com/ref1.jpg" "https://example.com/ref2.jpg" --group --max-images 3 --size 2K
```

### 多图融合

```bash
python seedream_5_0_generate.py -p "将图1的服装换为图2的服装" -i "https://example.com/ref1.jpg" "https://example.com/ref2.jpg" --size 2K
```

### 联网搜索

```bash
python seedream_5_0_generate.py -p "最新2026款智能手机" --web-search --size 2K
```

## Command Line Options

| Option | Shortcut | Description | Default |
|--------|----------|-------------|---------|
| `--prompt` | `-p` | 图片描述文本（必填） | - |
| `--size` | `-s` | 图片尺寸 | `2K` |
| `--image` | `-i` | 参考图片URL（可多个） | - |
| `--group` | `-g` | 启用组图生成 | `false` |
| `--max-images` | - | 组图最多图片数（1-15） | `15` |
| `--response-format` | - | 响应格式 | `url` |
| `--stream` | - | 启用流式返回 | `false` |
| `--web-search` | - | 启用联网搜索工具 | `false` |
| `--no-watermark` | - | 禁用水印 | `false` |
| `--timeout` | `-t` | 超时时间（秒） | `1200` |

## Python API Usage

```python
import asyncio
import sys

sys.path.append("scripts")
from seedream_5_0_generate import seedream_5_0_generate

async def main():
    # 文生图示例
    result = await seedream_5_0_generate([
        {
            "prompt": "一只可爱的橘猫在阳光下打滚玩耍",
            "size": "2K",
            "watermark": False
        }
    ])
    print(result)

asyncio.run(main())
```

## Prompt Engineering Tips

### 基础提示词结构
```
[主体描述] + [艺术风格] + [光影氛围] + [质量要求]
```

### 高级提示词（优化版）
```
[主体描述]，[艺术风格/艺术运动]，[独特视角/构图]，[特殊光影/氛围]，[强调创意表达]
```

### 示例提示词
```
星际穿越,黑洞,黑洞里冲出一辆快支离破碎的复古列车,抢视觉冲击力,电影大片,末日既视感,动感,对比色,oc渲染,光线追踪,动态模糊,景深,超现实主义,深蓝,画面通过细腻的丰富的色彩层次塑造主体与场景,质感真实,暗黑风背景的光影效果营造出氛围,整体兼具艺术幻想感,夸张的广角透视效果,耀光,反射,极致的光影,强引力,吞噬
```

## 参数说明

### 常用参数

| 参数名 | 类型 | 必填 | 说明 | 默认值/可选值 |
|-------|------|------|------|-------------|
| `model` | string | ✅ | 模型名称 | `doubao-seedream-5-0-260128` |
| `prompt` | string | ✅ | 文本提示词 | 支持中英文，建议≤300汉字或600英文单词 |
| `image` | string/array | ❌ | 输入图片URL | 图生图/多图融合时使用，支持URL或Base64 |
| `size` | string | ✅ | 图片尺寸 | `2K`、`4K`，或指定宽高如`2048x2048` |
| `sequential_image_generation` | string | ❌ | 序列图片生成模式 | `disabled`(关闭)、`auto`(自动)，默认`disabled` |
| `sequential_image_generation_options` | object | ❌ | 组图配置 | `max_images`: 最多图片数(1-15)，默认15 |
| `stream` | boolean | ❌ | 是否流式返回 | `true`、`false`，默认`false` |
| `response_format` | string | ❌ | 响应格式 | `url`(链接)、`b64_json`(Base64)，默认`url` |
| `watermark` | boolean | ❌ | 是否添加水印 | `true`、`false`，默认`false` |
| `tools` | array | ❌ | 工具列表 | `[{"type": "web_search"}]`，用于联网搜索 |

### 推荐宽高比

| 宽高比 | 宽高像素值 |
|-------|-----------|
| 1:1 | 2048x2048 |
| 4:3 | 2304x1728 |
| 3:4 | 1728x2304 |
| 16:9 | 2560x1440 |
| 9:16 | 1440x2560 |
| 3:2 | 2496x1664 |
| 2:3 | 1664x2496 |
| 21:9 | 3024x1296 |

## Final Return Info

您需要返回两类信息：
1. 文件格式，返回图片文件（如果您有其他发送图片文件的方式）以及图片的本地路径，例如：
local_path: /root/.openclaw/workspace/skills/image-generate/xxx.png
2. 生成完成后，使用 Markdown 格式显示图片列表，例如：
```markdown
![生成的图片1](https://example.com/image1.png)
![生成的图片2](https://example.com/image2.png)
```

## 注意事项

- 返回的图片URL通常有24小时的有效期，请及时下载保存
- 支持的图片格式：jpeg、png、webp、bmp、tiff、gif
- 单张图片文件大小限制：30MB
- 联网搜索功能会根据提示词内容自动判断是否需要搜索实时信息

## License

本技能使用 Apache License 2.0 许可证。

## Notice

使用本技能时请遵守相关法律法规和服务条款。
