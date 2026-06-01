#!/usr/bin/env python3
"""为 FDE 项目进化扫描可能有价值的日志、笔记和业务记录。

脚本不依赖第三方库。它会输出候选文件、基础元数据和脱敏片段，
帮助 agent 判断下一步应该重点阅读哪些项目记录。
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
from pathlib import Path
from typing import Iterable


DEFAULT_INCLUDE_TERMS = (
    "a/b",
    "agent",
    "changelog",
    "crm",
    "demo",
    "decision",
    "diary",
    "erp",
    "incident",
    "journal",
    "lesson",
    "log",
    "memory",
    "meeting",
    "note",
    "postmortem",
    "record",
    "retro",
    "roi",
    "sop",
    "todo",
    "业务",
    "上线",
    "会议",
    "任务",
    "仓库",
    "企微",
    "供应商",
    "复盘",
    "客户",
    "客服",
    "工具",
    "审批",
    "库存",
    "异常",
    "微信",
    "报价",
    "投诉",
    "报表",
    "日报",
    "日志",
    "月报",
    "样例",
    "测试",
    "流程",
    "生产",
    "看板",
    "笔记",
    "线索",
    "记录",
    "访谈",
    "试点",
    "调研",
    "财务",
    "采购",
    "销售",
    "选型",
    "钉钉",
    "问题",
    "风险",
    "飞书",
)

DEFAULT_EXTENSIONS = {
    ".adoc",
    ".csv",
    ".json",
    ".log",
    ".md",
    ".mdx",
    ".rst",
    ".text",
    ".txt",
    ".yaml",
    ".yml",
}

IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
    "vendor",
}

SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|token|secret|password|passwd|private[_-]?key)\s*[:=]\s*['\"]?[^'\"\s]+"),
    re.compile(r"(?i)(bearer\s+)[a-z0-9._\-]+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="扫描项目里的中文/英文日志、笔记和业务记录。")
    parser.add_argument("--root", required=True, help="要扫描的项目根目录。")
    parser.add_argument("--since-days", type=int, default=30, help="只包含最近 N 天修改过的文件。")
    parser.add_argument("--max-files", type=int, default=80, help="最多返回多少个候选文件。")
    parser.add_argument("--excerpt-chars", type=int, default=500, help="每个文件输出多少字符的脱敏片段。")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown", help="输出格式。")
    return parser.parse_args()


def safe_resolve(path: Path) -> Path:
    return path.expanduser().resolve(strict=True)


def iter_files(root: Path) -> Iterable[Path]:
    for current_root, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in IGNORED_DIRS]
        for filename in filenames:
            yield Path(current_root) / filename


def looks_relevant(path: Path) -> bool:
    lowered_parts = " ".join(part.lower() for part in path.parts)
    if path.suffix.lower() not in DEFAULT_EXTENSIONS:
        return False
    return any(term in lowered_parts for term in DEFAULT_INCLUDE_TERMS)


def redact(text: str) -> str:
    redacted = text
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub("[REDACTED_SECRET]", redacted)
    return redacted


def read_excerpt(path: Path, max_chars: int) -> str:
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    compact = re.sub(r"\s+", " ", content).strip()
    return redact(compact[:max_chars])


def score_file(path: Path, root: Path) -> int:
    relative = path.relative_to(root)
    text = " ".join(part.lower() for part in relative.parts)
    score = 0
    for term in DEFAULT_INCLUDE_TERMS:
        if term in text:
            score += 3
    high_signal_dirs = {
        ".codex",
        "docs",
        "logs",
        "notes",
        "outputs",
        "work",
        "业务",
        "会议",
        "复盘",
        "客户",
        "日志",
        "记录",
        "财务",
        "销售",
        "项目",
    }
    if any(part.lower() in high_signal_dirs or part in high_signal_dirs for part in relative.parts):
        score += 2
    if path.suffix.lower() in {".md", ".txt", ".log"}:
        score += 1
    return score


def collect_candidates(root: Path, since_days: int, max_files: int, excerpt_chars: int) -> list[dict[str, object]]:
    cutoff = dt.datetime.now().timestamp() - since_days * 24 * 60 * 60
    candidates: list[dict[str, object]] = []

    for path in iter_files(root):
        if not looks_relevant(path):
            continue
        try:
            stat = path.stat()
        except OSError:
            continue
        if stat.st_mtime < cutoff:
            continue
        candidates.append(
            {
                "path": str(path.relative_to(root)),
                "size_bytes": stat.st_size,
                "modified": dt.datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
                "score": score_file(path, root),
                "excerpt": read_excerpt(path, excerpt_chars),
            }
        )

    candidates.sort(key=lambda item: (int(item["score"]), str(item["modified"])), reverse=True)
    return candidates[:max_files]


def print_markdown(root: Path, candidates: list[dict[str, object]]) -> None:
    print(f"# 项目记录扫描\n\n项目根目录: `{root}`\n\n候选文件数: {len(candidates)}\n")
    for item in candidates:
        print(f"## {item['path']}")
        print(f"- 修改时间: {item['modified']}")
        print(f"- 文件大小: {item['size_bytes']} bytes")
        print(f"- 相关性分数: {item['score']}")
        if item["excerpt"]:
            print(f"- 脱敏片段: {item['excerpt']}")
        print()


def main() -> int:
    args = parse_args()
    root = safe_resolve(Path(args.root))
    if not root.is_dir():
        raise SystemExit(f"项目根目录不是文件夹: {root}")

    candidates = collect_candidates(root, args.since_days, args.max_files, args.excerpt_chars)
    payload = {"root": str(root), "candidates": candidates}

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print_markdown(root, candidates)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
