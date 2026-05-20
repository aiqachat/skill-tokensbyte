#!/usr/bin/env python3
# Copyright (c) 2026 ArtsAPI. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
doubao-seedance-2-0-generate - 使用 doubao-seedance-2-0 模型生成视频
支持多模态参考、视频编辑、视频延长、联网搜索等功能
"""

import argparse
import asyncio
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional

import httpx

# Configuration constants
API_KEY = os.getenv("ARTS_API_KEY")
API_BASE = os.getenv("ARTS_API_BASE", "https://apis.artsapi.com/v1").rstrip("/")

# Default model
DEFAULT_MODEL = "doubao-seedance-2-0-260128"


def image_to_data_url(image_path: str) -> str:
    """
    将本地图片文件转换为base64 data URL
    """
    p = Path(image_path)
    if not p.exists():
        raise FileNotFoundError(f"图片文件不存在: {image_path}")

    ext = p.suffix.lower().lstrip(".")
    mime_map = {
        "jpg": "jpeg", "jpeg": "jpeg", "png": "png",
        "webp": "webp", "bmp": "bmp", "tiff": "tiff",
        "tif": "tiff", "gif": "gif", "heic": "heic", "heif": "heif",
    }
    mime_ext = mime_map.get(ext, ext)

    file_size = p.stat().st_size
    if file_size > 30 * 1024 * 1024:
        raise ValueError(f"图片文件过大 ({file_size / 1024 / 1024:.1f} MB). 最大支持 30 MB.")

    with open(p, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")

    return f"data:image/{mime_ext};base64,{b64}"


def resolve_image_input(image_input: str) -> str:
    """
    解析图片输入，自动识别本地路径并转换为data URL
    支持URL、data URL和本地文件路径
    """
    if image_input.startswith(("http://", "https://", "data:")):
        return image_input
    # 检查是否是本地文件路径
    if Path(image_input).exists():
        return image_to_data_url(image_input)
    # 否则按URL处理
    return image_input


def _get_headers() -> dict:
    """
    构建 API 请求头
    """
    if not API_KEY:
        raise ValueError(
            "请设置 ARTS_API_KEY 环境变量"
        )
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }


async def seedance_2_0_create(
    params: dict,
    timeout: int = 1200,
) -> str:
    """
    创建视频生成任务

    Args:
        params: 任务参数
        timeout: 超时时间（秒）

    Returns:
        任务 ID
    """
    url = f"{API_BASE}/video/generations"

    # Build request body
    body = {
        "model": params.get("model", DEFAULT_MODEL),
    }

    # Handle prompt
    if "prompt" in params:
        body["prompt"] = params["prompt"]

    # Handle images (platform standard way)
    if "images" in params and params["images"]:
        body["images"] = [resolve_image_input(img) for img in params["images"]]

    # Handle content array (native way)
    if "content" in params and params["content"]:
        # 处理content数组中的图片
        processed_content = []
        for item in params["content"]:
            if item.get("type") == "image_url" and "image_url" in item:
                item_copy = item.copy()
                item_copy["image_url"]["url"] = resolve_image_input(item_copy["image_url"]["url"])
                processed_content.append(item_copy)
            else:
                processed_content.append(item)
        body["content"] = processed_content

    # Handle extra parameters
    extra = {}
    if "extra_reference_videos" in params and params["extra_reference_videos"]:
        extra["reference_videos"] = params["extra_reference_videos"]
    if "extra_reference_audios" in params and params["extra_reference_audios"]:
        extra["reference_audios"] = params["extra_reference_audios"]
    if "extend_video_id" in params and params["extend_video_id"]:
        extra["extend_video_id"] = params["extend_video_id"]

    if extra:
        body["extra"] = extra

    # Add other parameters
    if "resolution" in params:
        body["resolution"] = params["resolution"]
    if "ratio" in params:
        body["ratio"] = params["ratio"]
    if "duration" in params:
        body["duration"] = params["duration"]
    if "seed" in params:
        body["seed"] = params["seed"]
    if "camera_fixed" in params:
        body["camera_fixed"] = params["camera_fixed"]
    if "watermark" in params:
        body["watermark"] = params["watermark"]
    if "generate_audio" in params:
        body["generate_audio"] = params["generate_audio"]
    if "service_tier" in params:
        body["service_tier"] = params["service_tier"]
    if "tools" in params:
        body["tools"] = params["tools"]

    # Print request
    print("\n" + "="*80)
    print("📤 创建视频生成任务:")
    print("="*80)
    print(f"URL: {url}")
    print(f"Body: {json.dumps(body, indent=2, ensure_ascii=False)}")
    print("="*80 + "\n")

    async with httpx.AsyncClient(timeout=float(timeout)) as client:
        response = await client.post(url, headers=_get_headers(), json=body)
        response.raise_for_status()
        result = response.json()
        task_id = result.get("id", "")
        print(f"✅ 任务创建成功，任务ID: {task_id}")
        return task_id


async def seedance_2_0_get(
    task_id: str,
    timeout: int = 1200,
) -> dict:
    """
    查询任务状态

    Args:
        task_id: 任务 ID
        timeout: 超时时间（秒）

    Returns:
        任务信息
    """
    url = f"{API_BASE}/video/generations/{task_id}"

    async with httpx.AsyncClient(timeout=float(timeout)) as client:
        response = await client.get(url, headers=_get_headers())
        response.raise_for_status()
        return response.json()


async def seedance_2_0_wait(
    task_id: str,
    interval: int = 15,
    download_dir: Optional[str] = None,
    timeout: int = 1200,
) -> dict:
    """
    等待任务完成

    Args:
        task_id: 任务 ID
        interval: 轮询间隔（秒）
        download_dir: 下载目录
        timeout: 超时时间（秒）

    Returns:
        任务信息
    """
    print(f"⏳ 等待任务 {task_id} 完成（每 {interval} 秒轮询一次...")

    while True:
        result = await seedance_2_0_get(task_id, timeout=timeout)
        status = result.get("status", "unknown")

        if status in ["succeeded", "success"]:
            video_url = result.get("content", {}).get("video_url", "")
            duration = result.get("duration", "?")
            resolution = result.get("resolution", "?")
            ratio = result.get("ratio", "?")

            print(f"\n✅ 视频生成成功！")
            print(f"  时长: {duration}秒 | 分辨率: {resolution} | 宽高比: {ratio}")
            print(f"  视频URL: {video_url}")

            # Download video
            if download_dir and video_url:
                download_path = Path(download_dir).expanduser()
                download_path.mkdir(parents=True, exist_ok=True)
                filename = f"seedance_2_0_{task_id}_{int(time.time())}.mp4"
                filepath = download_path / filename

                print(f"\n📥 下载视频到 {filepath}...")
                try:
                    urllib.request.urlretrieve(video_url, str(filepath))
                    print(f"✅ 已保存到: {filepath}")

                    # Open on macOS
                    if sys.platform == "darwin":
                        os.system(f'open "{filepath}"')
                except Exception as e:
                    print(f"❌ 下载失败: {e}", file=sys.stderr)

            return result

        elif status in ["failed", "error"]:
            error = result.get("error", {})
            print(f"\n❌ 视频生成失败！")
            print(f"  错误: {error}")
            return result

        elif status == "expired":
            print(f"\n⏰ 视频生成任务已过期。")
            return result

        else:
            print(f"  状态: {status}...", flush=True)
            time.sleep(interval)


async def seedance_2_0_list(
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    timeout: int = 1200,
) -> dict:
    """
    列出任务

    Args:
        status: 状态过滤
        page: 页码
        page_size: 每页数量
        timeout: 超时时间（秒）

    Returns:
        任务列表
    """
    url = f"{API_BASE}/video/generations/tasks"
    params = {
        "page_num": page,
        "page_size": page_size,
    }
    if status:
        params["filter"] = {"status": status}

    async with httpx.AsyncClient(timeout=float(timeout)) as client:
        response = await client.get(url, headers=_get_headers(), params=params)
        response.raise_for_status()
        return response.json()


async def seedance_2_0_delete(
    task_id: str,
    timeout: int = 1200,
) -> None:
    """
    删除/取消任务

    Args:
        task_id: 任务 ID
        timeout: 超时时间（秒）
    """
    url = f"{API_BASE}/video/generations/{task_id}"

    async with httpx.AsyncClient(timeout=float(timeout)) as client:
        await client.delete(url, headers=_get_headers())
        print(f"✅ 任务 {task_id} 已删除/取消")


def parse_bool(v):
    """
    解析布尔值
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ("true", "1", "yes"):
        return True
    if v.lower() in ("false", "0", "no"):
        return False
    raise argparse.ArgumentTypeError(f"Boolean expected, got '{v}'")


def main():
    """
    命令行入口
    """
    parser = argparse.ArgumentParser(description="doubao-seedance-2-0-generate - 使用 doubao-seedance-2-0 模型生成视频")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # create command
    p_create = subparsers.add_parser("create", help="创建视频生成任务")
    p_create.add_argument("--prompt", "-p", help="视频描述文本")
    p_create.add_argument("--model", "-m", default=DEFAULT_MODEL, help=f"模型名称（默认：{DEFAULT_MODEL}）")
    p_create.add_argument("--images", "-i", nargs="+", help="参考图片URL（平台标准方式）")
    p_create.add_argument("--content-images", nargs="+", help="参考图片URL（content 数组方式）")
    p_create.add_argument("--content-videos", nargs="+", help="参考视频URL（content 数组方式）")
    p_create.add_argument("--content-audios", nargs="+", help="参考音频URL（content 数组方式）")
    p_create.add_argument("--content-role", default="reference_image", help="content 数组方式的 role")
    p_create.add_argument("--first-frame", help="首帧图片URL")
    p_create.add_argument("--last-frame", help="尾帧图片URL")
    p_create.add_argument("--extra-reference-videos", nargs="+", help="参考视频URL（extra 方式）")
    p_create.add_argument("--extra-reference-audios", nargs="+", help="参考音频URL（extra 方式）")
    p_create.add_argument("--extend-video-id", help="要延长的视频任务ID")
    p_create.add_argument("--resolution", "-r", choices=["480p", "720p", "1080p"], default="720p", help="分辨率")
    p_create.add_argument("--ratio", choices=["16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"], help="宽高比")
    p_create.add_argument("--duration", "-d", type=int, default=5, help="时长（秒）")
    p_create.add_argument("--seed", type=int, default=-1, help="随机种子")
    p_create.add_argument("--camera-fixed", type=parse_bool, default=False, help="固定相机位置")
    p_create.add_argument("--watermark", type=parse_bool, default=False, help="添加水印")
    p_create.add_argument("--generate-audio", type=parse_bool, default=True, help="生成音频")
    p_create.add_argument("--web-search", action="store_true", help="启用联网搜索")
    p_create.add_argument("--service-tier", choices=["default", "flex"], help="服务层级")
    p_create.add_argument("--wait", "-w", action="store_true", help="创建后等待完成")
    p_create.add_argument("--interval", type=int, default=15, help="轮询间隔（秒）")
    p_create.add_argument("--download", help="下载目录")

    # status command
    p_status = subparsers.add_parser("status", help="查询任务状态")
    p_status.add_argument("task_id", help="任务 ID")

    # wait command
    p_wait = subparsers.add_parser("wait", help="等待任务完成")
    p_wait.add_argument("task_id", help="任务 ID")
    p_wait.add_argument("--interval", type=int, default=15, help="轮询间隔（秒）")
    p_wait.add_argument("--download", help="下载目录")

    # list command
    p_list = subparsers.add_parser("list", help="列出任务")
    p_list.add_argument("--status", choices=["queued", "processing", "running", "succeeded", "success", "failed", "error", "expired"], help="状态过滤")
    p_list.add_argument("--page", type=int, default=1, help="页码")
    p_list.add_argument("--page-size", type=int, default=10, help="每页数量")

    # delete command
    p_delete = subparsers.add_parser("delete", help="删除/取消任务")
    p_delete.add_argument("task_id", help="任务 ID")

    args = parser.parse_args()

    # Check API key
    if not API_KEY:
        print("❌ 错误：请设置 ARTS_API_KEY 环境变量！")
        print("提示：export ARTS_API_KEY='your-api-key'")
        sys.exit(1)

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Handle commands
    if args.command == "create":
        # Build parameters
        params = {
            "model": args.model,
            "resolution": args.resolution,
            "duration": args.duration,
            "seed": args.seed,
            "camera_fixed": args.camera_fixed,
            "watermark": args.watermark,
            "generate_audio": args.generate_audio,
        }

        if args.prompt:
            params["prompt"] = args.prompt
        if args.ratio:
            params["ratio"] = args.ratio
        if args.service_tier:
            params["service_tier"] = args.service_tier

        # Handle images (platform standard way)
        if args.images:
            params["images"] = [resolve_image_input(img) for img in args.images]

        # Handle content array (native way)
        content = []
        if args.prompt:
            content.append({"type": "text", "text": args.prompt})

        # Handle first/last frame
        if args.first_frame:
            content.append({
                "type": "image_url",
                "image_url": {"url": resolve_image_input(args.first_frame)},
                "role": "first_frame"
            })
        if args.last_frame:
            content.append({
                "type": "image_url",
                "image_url": {"url": resolve_image_input(args.last_frame)},
                "role": "last_frame"
            })

        # Handle content images/videos/audios
        if args.content_images:
            for img_url in args.content_images:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": resolve_image_input(img_url)},
                    "role": args.content_role
                })
        if args.content_videos:
            for vid_url in args.content_videos:
                content.append({
                    "type": "video_url",
                    "video_url": {"url": vid_url},
                    "role": "reference_video"
                })
        if args.content_audios:
            for aud_url in args.content_audios:
                content.append({
                    "type": "audio_url",
                    "audio_url": {"url": aud_url},
                    "role": "reference_audio"
                })

        if len(content) > 1:
            params["content"] = content

        # Handle extra parameters
        if args.extra_reference_videos:
            params["extra_reference_videos"] = args.extra_reference_videos
        if args.extra_reference_audios:
            params["extra_reference_audios"] = args.extra_reference_audios
        if args.extend_video_id:
            params["extend_video_id"] = args.extend_video_id

        # Handle web search
        if args.web_search:
            params["tools"] = [{"type": "web_search"}]

        # Create task
        task_id = asyncio.run(seedance_2_0_create(params))

        # Wait if requested
        if args.wait:
            result = asyncio.run(seedance_2_0_wait(task_id, args.interval, args.download))
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\n📋 任务ID: {task_id}")
            print(f"使用以下命令查询状态: python seedance_2_0_generate.py status {task_id}")
            print(f"使用以下命令等待完成: python seedance_2_0_generate.py wait {task_id}")

    elif args.command == "status":
        result = asyncio.run(seedance_2_0_get(args.task_id))
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.command == "wait":
        result = asyncio.run(seedance_2_0_wait(args.task_id, args.interval, args.download))
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.command == "list":
        result = asyncio.run(seedance_2_0_list(args.status, args.page, args.page_size))
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.command == "delete":
        asyncio.run(seedance_2_0_delete(args.task_id))


if __name__ == "__main__":
    main()
