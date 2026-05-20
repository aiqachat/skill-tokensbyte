---
name: doubao-seedance-2-0
description: 使用新一代多模态视频生成，支持 doubao-seedance-2-0-260128 和 doubao-seedance-2-0-fast-260128 模型，支持多模态参考、视频编辑、视频延长、联网搜索等功能
license: Apache-2.0
tags: ["video-generation", "seedance", "doubao-seedance-2-0", "text-to-video", "image-to-video", "multimodal"]
---

# Doubao Seedance 2.0 Video Generation

## Description

使用新一代多模态视频模型，支持 doubao-seedance-2-0-260128（质量优先）和 doubao-seedance-2-0-fast-260128（速度优先）两个模型。支持多模态参考（图片/视频/音频）、视频编辑、视频延长、联网搜索等功能。

## When to Use This Skill

Use this skill when:
- 用户想要从文本描述生成视频
- 用户需要基于参考图片生成视频
- 用户想要基于参考视频生成视频
- 用户需要使用多模态素材（图片+视频+音频）生成视频
- 用户想要延长已生成的视频
- 用户需要结合实时信息生成视频（联网搜索）
- 用户需要编辑已生成的视频

## Supported Models

| Model | Model Name | Features |
|-------|------------|----------|
| Seedance 2.0 | doubao-seedance-2-0-260128 | 质量优先，支持 1080p |
| Seedance 2.0 Fast | doubao-seedance-2-0-fast-260128 | 速度优先，支持 480p/720p |

## Features

- **文生视频**：从文本描述生成视频
- **图生视频**：基于参考图片生成视频（首帧/首尾帧/多参考图）
- **多模态参考**：同时使用图片、视频、音频作为参考
- **视频延长**：延长已生成的视频
- **视频编辑**：编辑已生成的视频
- **联网搜索**：结合实时信息生成视频
- **有声视频**：自动生成同步音频
- **多种分辨率**：支持 480p、720p、1080p
- **多种宽高比**：支持 16:9、4:3、1:1、3:4、9:16、21:9、adaptive
- **自适应模式**：根据输入自动选择最佳宽高比

## Installation & Setup

### Prerequisites

```bash
# Required: API Key 配置
export ARTS_API_KEY="your-api-key-here"

# Optional: API Base URL（默认已配置）
export ARTS_API_BASE="https://apis.artsapi.com/v1"
```

脚本会优先使用环境变量配置。

## Usage

### 基础用法

```bash
cd scripts
python seedance_2_0_generate.py create --prompt "一只可爱的橘猫在阳光下打滚玩耍" --wait
```

### 文生视频

```bash
python seedance_2_0_generate.py create --prompt "一只可爱的橘猫在阳光下打滚玩耍" --resolution 720p --ratio 16:9 --duration 5 --generate-audio --wait
```

### 参考图片生视频（平台标准方式）

支持本地图片路径或网络URL：
```bash
python seedance_2_0_generate.py create --prompt "将参考图中的人物放在海滩日落场景中" --images "https://example.com/ref1.jpg" "C:/Users/xxx/Pictures/ref2.jpg" --resolution 720p --ratio adaptive --duration 5 --wait
```

### 参考图片生视频（content 数组方式）

支持本地图片路径或网络URL：
```bash
python seedance_2_0_generate.py create --prompt "图中女孩对着镜头说'茄子'，360度环绕运镜" --content-images "https://example.com/ref1.jpg" "C:/Users/xxx/Pictures/ref2.jpg" --content-role reference_image --resolution 480p --ratio 16:9 --duration 4 --no-watermark --wait
```

### 首尾帧图生视频

支持本地图片路径或网络URL：
```bash
python seedance_2_0_generate.py create --prompt "从早晨到傍晚的日出日落场景" --first-frame "C:/Users/xxx/Pictures/sunrise.jpg" --last-frame "C:/Users/xxx/Pictures/sunset.jpg" --resolution 720p --ratio 16:9 --duration 5 --wait
```

### 参考视频生视频

```bash
python seedance_2_0_generate.py create --prompt "延续参考视频的风格，生成城市夜景" --extra-reference-videos "https://example.com/ref-video.mp4" --resolution 720p --ratio 16:9 --duration -1 --wait
```

### 参考音频生视频

```bash
python seedance_2_0_generate.py create --prompt "根据音乐节奏生成舞蹈画面" --images "https://example.com/dancer.jpg" --extra-reference-audios "https://example.com/music.mp3" --resolution 720p --ratio 16:9 --duration 10 --generate-audio --wait
```

### 视频延长

```bash
python seedance_2_0_generate.py create --prompt "延续之前的画面，继续展示城市全景" --extend-video-id "cgt-20260410152408-p2rp2" --resolution 720p --ratio 16:9 --duration 5 --wait
```

### 联网搜索

```bash
python seedance_2_0_generate.py create --prompt "展示今天北京天安门广场的实时天气画面" --web-search --resolution 720p --ratio 16:9 --duration 5 --wait
```

### 查询任务状态

```bash
python seedance_2_0_generate.py status "cgt-20260421155014-h7dlm"
```

### 等待任务完成

```bash
python seedance_2_0_generate.py wait "cgt-20260421155014-h7dlm" --download ~/Desktop
```

### 列出任务

```bash
python seedance_2_0_generate.py list --status succeeded
```

## Command Line Options

### create 命令选项

| Option | Shortcut | Description | Default |
|--------|----------|-------------|---------|
| `--prompt` | `-p` | 视频描述文本 | - |
| `--model` | `-m` | 模型名称 | doubao-seedance-2-0-260128 |
| `--images` | `-i` | 参考图片URL（平台标准方式） | - |
| `--content-images` | | 参考图片URL（content 数组方式） | - |
| `--content-videos` | | 参考视频URL（content 数组方式） | - |
| `--content-audios` | | 参考音频URL（content 数组方式） | - |
| `--content-role` | | content 数组方式的 role | reference_image |
| `--first-frame` | | 首帧图片URL | - |
| `--last-frame` | | 尾帧图片URL | - |
| `--extra-reference-videos` | | 参考视频URL（extra 方式） | - |
| `--extra-reference-audios` | | 参考音频URL（extra 方式） | - |
| `--extend-video-id` | | 要延长的视频任务ID | - |
| `--resolution` | `-r` | 分辨率 | 720p |
| `--ratio` | | 宽高比 | 16:9 |
| `--duration` | `-d` | 时长（秒） | 5 |
| `--seed` | | 随机种子 | -1 |
| `--camera-fixed` | | 固定相机位置 | false |
| `--watermark` | | 添加水印 | false |
| `--generate-audio` | | 生成音频 | true |
| `--web-search` | | 启用联网搜索 | false |
| `--service-tier` | | 服务层级 | default |
| `--wait` | `-w` | 创建后等待完成 | false |
| `--interval` | | 轮询间隔（秒） | 15 |
| `--download` | | 下载目录 | - |

### 其他命令

- `status <task_id>`: 查询任务状态
- `wait <task_id>`: 等待任务完成
- `list`: 列出任务
- `delete <task_id>`: 删除/取消任务

## Python API Usage

```python
import asyncio
import sys

sys.path.append("scripts")
from seedance_2_0_generate import seedance_2_0_create, seedance_2_0_wait

async def main():
    # 创建视频生成任务
    task_id = await seedance_2_0_create({
        "prompt": "一只可爱的橘猫在阳光下打滚玩耍",
        "resolution": "720p",
        "ratio": "16:9",
        "duration": 5,
        "generate_audio": True
    })
    print(f"任务ID: {task_id}")

    # 等待任务完成
    result = await seedance_2_0_wait(task_id)
    print(result)

asyncio.run(main())
```

## 参数说明

### 基础参数

| 参数名 | 类型 | 必填 | 说明 | 默认值/可选值 |
|-------|------|------|------|-------------|
| `model` | string | ✅ | 模型名称 | doubao-seedance-2-0-260128、doubao-seedance-2-0-fast-260128 |
| `prompt` | string | ✅ | 文本提示词 | 支持中英文 |
| `images` | array | ❌ | 参考图片URL（平台标准方式） | - |
| `content` | array | ❌ | Content数组（原生方式） | 包含文本、图片、视频、音频 |
| `resolution` | string | ❌ | 分辨率 | 480p、720p、1080p |
| `ratio` | string | ❌ | 宽高比 | 16:9、4:3、1:1、3:4、9:16、21:9、adaptive |
| `duration` | integer | ❌ | 时长（秒） | 4-15，-1（智能） |
| `seed` | integer | ❌ | 随机种子 | -1 |
| `camera_fixed` | boolean | ❌ | 固定相机位置 | false |
| `watermark` | boolean | ❌ | 添加水印 | false |
| `generate_audio` | boolean | ❌ | 生成音频 | true |
| `tools` | array | ❌ | 工具列表 | [{"type": "web_search"}] |
| `extra` | object | ❌ | 额外参数 | reference_videos、reference_audios、extend_video_id |

### content 数组类型

| 类型 | content.type | 主要属性 | 可选 role |
|------|--------------|----------|-----------|
| 文本 | text | text | - |
| 图片 | image_url | image_url.url | first_frame、last_frame、reference_image |
| 视频 | video_url | video_url.url | reference_video |
| 音频 | audio_url | audio_url.url | reference_audio |

### 参考素材限制

| 素材类型 | 数量限制 | 单个限制 |
|---------|---------|---------|
| 参考图片 | 0-9 张 | - |
| 参考视频 | 0-3 个 | 单个 2-15 秒，总时长≤15秒 |
| 参考音频 | 0-3 段 | 单个 2-15 秒，总时长≤15秒 |

## 查询响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 任务 ID |
| `model` | string | 使用的模型名称 |
| `status` | string | 任务状态 |
| `content.video_url` | string | 生成的视频 URL（成功时返回，含签名参数，有效期 24 小时） |
| `usage.completion_tokens` | integer | 消耗的 Token 数 |
| `usage.total_tokens` | integer | 总消耗 Token 数 |
| `created_at` | integer | 任务创建时间戳 |
| `updated_at` | integer | 任务更新时间戳 |
| `seed` | integer | 随机种子 |
| `resolution` | string | 视频分辨率 |
| `ratio` | string | 宽高比 |
| `duration` | integer | 视频时长（秒） |
| `framespersecond` | integer | 帧率 |
| `service_tier` | string | 服务层级，如 default |
| `execution_expires_after` | integer | 执行过期时间（秒），默认 172800（48 小时） |
| `generate_audio` | boolean | 是否生成了音频 |
| `draft` | boolean | 是否为草稿 |

## 任务状态

| 状态 | 说明 |
|------|------|
| queued | 任务排队中 |
| processing/running | 任务处理中 |
| succeeded/success | 任务成功完成 |
| failed/error | 任务失败 |

## Final Return Info

您需要返回两类信息：
1. 文件格式，返回视频文件（如果您有其他发送视频文件的方式）以及视频的本地路径，例如：
local_path: /root/.openclaw/workspace/skills/video-generate/xxx.mp4
2. 生成完成后，显示任务信息和视频URL，例如：
```markdown
任务ID: cgt-20260421155014-h7dlm
视频URL: https://example.com/video.mp4
```

## 注意事项

- 视频URL包含签名参数，有效期通常为24小时，请及时下载视频文件
- 任务历史保留7天，过期后无法查询
- 支持的图片格式：jpeg、png、webp、bmp、tiff、gif
- 支持的视频格式：mp4、avi、mov、wmv
- 支持的音频格式：mp3、wav、aac、flac
- 单张图片文件大小限制：30MB
- ✨ 支持本地图片路径直接上传，自动转换为base64格式
- 单个视频文件大小限制：100MB
- 单个音频文件大小限制：50MB
- 联网搜索功能会根据提示词内容自动判断是否需要搜索实时信息

## License

本技能使用 Apache License 2.0 许可证。

## Notice

使用本技能时请遵守相关法律法规和服务条款。
