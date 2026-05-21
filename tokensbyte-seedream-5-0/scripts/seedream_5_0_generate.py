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
doubao-seedream-5-0-generate - 使用 doubao-seedream-5-0-260128 模型生成高质量图片
支持文生图、图生图、多图融合、联网搜索等功能
"""

import argparse
import asyncio
import json
import os
import sys
from typing import Dict, List, Tuple

import httpx

# Configuration constants
API_KEY = os.getenv("ARTS_API_KEY")
API_BASE = os.getenv("ARTS_API_BASE", "https://ai.artsapi.com/v1").rstrip("/")

# Model name
MODEL_NAME = "doubao-seedream-5-0-260128"


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


def _build_request_body(item: dict) -> dict:
    """
    构建 API 请求体
    """
    print("\n" + "="*80)
    print("📋 构建请求体 - 输入参数:")
    print("="*80)
    print(f"item: {json.dumps(item, indent=2, ensure_ascii=False, default=str)}")
    print(f"model: {MODEL_NAME}")
    print("="*80 + "\n")

    body = {
        "model": MODEL_NAME,
        "prompt": item.get("prompt", ""),
    }

    # Add optional parameters
    if "size" in item:
        body["size"] = item["size"]
    if "image" in item and item["image"] is not None:
        body["image"] = item["image"]
    if "sequential_image_generation" in item:
        body["sequential_image_generation"] = item["sequential_image_generation"]
    if "sequential_image_generation_options" in item:
        body["sequential_image_generation_options"] = item["sequential_image_generation_options"]
    if "stream" in item:
        body["stream"] = item["stream"]
    if "response_format" in item:
        body["response_format"] = item["response_format"]
    if "watermark" in item:
        body["watermark"] = item["watermark"]
    if "tools" in item:
        body["tools"] = item["tools"]

    print("\n" + "="*80)
    print("✅ 构建请求体 - 最终输出:")
    print("="*80)
    print(f"body: {json.dumps(body, indent=2, ensure_ascii=False, default=str)}")
    print("="*80 + "\n")

    return body


async def _call_image_api(item: dict, timeout: int) -> dict:
    """
    调用图片生成 API
    """
    url = f"{API_BASE}/images/generations"
    body = _build_request_body(item)

    # Print complete request
    print("\n" + "="*80)
    print("📤 完整 API 请求:")
    print("="*80)
    print(f"URL: {url}")
    print(f"Headers: {json.dumps(_get_headers(), indent=2, ensure_ascii=False)}")
    print(f"Request Body: {json.dumps(body, indent=2, ensure_ascii=False)}")
    print("="*80 + "\n")

    async with httpx.AsyncClient(timeout=float(timeout)) as client:
        response = await client.post(url, headers=_get_headers(), json=body)
        response.raise_for_status()
        return response.json()


async def handle_single_task(
    idx: int,
    item: dict,
    timeout: int,
) -> Tuple[List[dict], List[str], List[dict]]:
    """
    处理单个图片生成任务
    """
    success_list = []
    error_list = []
    error_detail_list = []

    try:
        response = await _call_image_api(item, timeout)

        if "data" in response:
            data_list = response.get("data", [])
            for i, image_data in enumerate(data_list):
                image_name = f"task_{idx}_image_{i}"

                # Check if image has error
                if "error" in image_data:
                    error_list.append(image_name)
                    error_detail_list.append(
                        {
                            "task_idx": idx,
                            "image_name": image_name,
                            "error": image_data.get("error"),
                        }
                    )
                    continue

                # Get image URL or Base64 data
                image_url = image_data.get("url")
                if image_url:
                    success_list.append({image_name: image_url})
                else:
                    b64 = image_data.get("b64_json")
                    if b64:
                        success_list.append(
                            {image_name: f"data:image/jpeg;base64,{b64}"}
                        )
                    else:
                        error_list.append(image_name)
                        error_detail_list.append(
                            {
                                "task_idx": idx,
                                "image_name": image_name,
                                "error": "missing data (no url/b64)",
                            }
                        )
        elif "error" in response:
            # API returned error
            error_info = response.get("error", {})
            error_list.append(f"task_{idx}")
            error_detail_list.append({"task_idx": idx, "error": error_info})

    except Exception as e:
        # Handle exception
        error_list.append(f"task_{idx}")
        error_detail_list.append({"task_idx": idx, "error": str(e)})

    return success_list, error_list, error_detail_list


async def seedream_5_0_generate(
    tasks: List[dict],
    timeout: int = 1200,
) -> Dict:
    """
    doubao-seedream-5-0 图片生成主函数

    使用 doubao-seedream-5-0-260128 模型生成高质量图片

    Args:
        tasks: 任务列表，每个任务是一个字典
        timeout: 超时时间（秒），默认 1200 秒

    Returns:
        包含生成结果的字典
    """
    if not API_KEY:
        return {
            "status": "error",
            "success_list": [],
            "error_list": ["缺少 API Key，请设置 ARTS_API_KEY 环境变量"],
            "error_detail_list": [{"error": "Missing API Key"}],
        }

    success_list = []
    error_list = []
    error_detail_list = []

    # Process all tasks concurrently
    coroutines = [
        handle_single_task(idx, item, timeout)
        for idx, item in enumerate(tasks)
    ]

    results = await asyncio.gather(*coroutines, return_exceptions=True)

    # Compile results
    for res in results:
        if isinstance(res, Exception):
            error_list.append("unknown_task_exception")
            error_detail_list.append({"error": str(res)})
            continue
        s, e, ed = res
        success_list.extend(s)
        error_list.extend(e)
        error_detail_list.extend(ed)

    return {
        "status": "success" if success_list else "error",
        "success_list": success_list,
        "error_list": error_list,
        "error_detail_list": error_detail_list,
        "model": MODEL_NAME,
    }


def main():
    """
    命令行入口
    """
    parser = argparse.ArgumentParser(
        description="doubao-seedream-5-0-generate - 使用 doubao-seedream-5-0-260128 模型生成高质量图片"
    )
    parser.add_argument(
        "--prompt", "-p", required=True, help="图片描述文本"
    )
    parser.add_argument(
        "--size", "-s", default="2K",
        help="图片尺寸，如 2K、4K、2048x2048"
    )
    parser.add_argument(
        "--image", "-i", nargs="+", default=None,
        help="参考图片URL（可多个）"
    )
    parser.add_argument(
        "--group", "-g", action="store_true",
        help="启用组图生成"
    )
    parser.add_argument(
        "--max-images", type=int, default=15,
        help="组图最多图片数（1-15）"
    )
    parser.add_argument(
        "--response-format", choices=["url", "b64_json"], default="url",
        help="响应格式：url 或 b64_json"
    )
    parser.add_argument(
        "--stream", action="store_true",
        help="启用流式返回"
    )
    parser.add_argument(
        "--web-search", action="store_true",
        help="启用联网搜索工具"
    )
    parser.add_argument(
        "--timeout", "-t", type=int, default=1200,
        help="超时时间（秒）"
    )
    parser.add_argument(
        "--no-watermark", action="store_true",
        help="禁用水印"
    )

    args = parser.parse_args()

    # Check API key
    if not API_KEY:
        print(
            "  错误：请设置 ARTS_API_KEY 环境变量！"
        )
        print("  提示：export ARTS_API_KEY='your-api-key'")
        sys.exit(1)

    # Build task
    task = {
        "prompt": args.prompt,
        "size": args.size,
        "response_format": args.response_format,
        "watermark": not args.no_watermark,
        "stream": args.stream,
    }

    # Handle images
    if args.image:
        if len(args.image) == 1:
            task["image"] = args.image[0]
        else:
            task["image"] = args.image

    # Handle group generation
    if args.group:
        if not (1 <= args.max_images <= 15):
            print("  错误：--max-images 必须在 1-15 范围内")
            sys.exit(1)
        task["sequential_image_generation"] = "auto"
        task["sequential_image_generation_options"] = {"max_images": args.max_images}

    # Handle web search
    if args.web_search:
        task["tools"] = [{"type": "web_search"}]

    print(f"  使用 Seedream 5.0 生成图片...")
    print(f"  提示词：{args.prompt}")
    print(f"  尺寸：{args.size}")
    print(f"  响应格式：{args.response_format}")
    print(f"  水印：{'禁用' if args.no_watermark else '启用'}")
    if args.web_search:
        print(f"  联网搜索：启用")
    print("")

    # Execute generation
    result = asyncio.run(
        seedream_5_0_generate([task], timeout=args.timeout)
    )

    # Output results
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result["status"] == "success":
        print(f"\n✅ Seedream 5.0 图片生成成功！")
        print(f"  生成了 {len(result['success_list'])} 张图片")
        print(f"\n📷 生成的图片：")
        for img in result["success_list"]:
            for name, url in img.items():
                print(f"  - {name}: {url}")
    else:
        print(f"\n❌ 图片生成失败")
        print(f"  错误信息：{result['error_list']}")


if __name__ == "__main__":
    main()
