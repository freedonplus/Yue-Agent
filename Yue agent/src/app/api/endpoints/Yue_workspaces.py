from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from settings import BASE_DIR, settings

"""
    ═══════════════════════════════════════════════════
                    工作区列表
    ═══════════════════════════════════════════════════

    GET /api/workspaces

    返回对话页工作区下拉可选项。工作区就是 chat/stream 里的 workdir：
    一个本地目录的绝对路径。

    优先读取 .env 的 WORKSPACES（JSON 数组），格式：
        [{"id": "yue", "name": "Yue Agent", "root_path": "C:/Users/xxx/Desktop/Yue Agent"}]

    未配置时自动返回项目目录、项目上级目录和用户主目录（只保留真实存在的目录）。
    路径统一用正斜杠，便于前端直接作为 workdir 回传。
"""

router = APIRouter()


class WorkspaceOut(BaseModel):
    id: str
    name: str
    root_path: str


def _slug(text: str) -> str:
    value = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
    return "-".join(part for part in value.split("-") if part)


def _resolve(value) -> Path | None:
    text = " ".join(str(value or "").split())
    if not text:
        return None
    path = Path(text).expanduser()
    if not path.is_absolute():
        path = BASE_DIR / path
    try:
        path = path.resolve()
    except OSError:
        return None
    return path if path.is_dir() else None


def _entry(path: Path, *, ws_id=None, name=None) -> WorkspaceOut:
    return WorkspaceOut(
        id=(str(ws_id).strip() if ws_id else "") or _slug(path.name) or "workspace",
        name=(str(name).strip() if name else "") or path.name,
        root_path=path.as_posix(),
    )


def _configured() -> list[WorkspaceOut]:
    result: list[WorkspaceOut] = []
    for item in settings.WORKSPACES or []:
        if not isinstance(item, dict):
            continue
        path = _resolve(item.get("root_path") or item.get("path"))
        if path is None:
            continue
        result.append(
            _entry(path, ws_id=item.get("id"), name=item.get("name"))
        )
    return result


def _defaults() -> list[WorkspaceOut]:
    result: list[WorkspaceOut] = []
    for candidate in (BASE_DIR, BASE_DIR.parent, Path.home()):
        path = _resolve(candidate)
        if path is not None:
            result.append(_entry(path))
    return result


def _dedupe(items: list[WorkspaceOut]) -> list[WorkspaceOut]:
    """同一目录只留一条；id 撞车时依次加 -2、-3 后缀。"""
    result: list[WorkspaceOut] = []
    seen_paths: set[str] = set()
    used_ids: set[str] = set()
    for item in items:
        key = item.root_path.lower()
        if key in seen_paths:
            continue
        seen_paths.add(key)

        base = item.id
        ws_id = base
        index = 2
        while ws_id in used_ids:
            ws_id = f"{base}-{index}"
            index += 1
        used_ids.add(ws_id)
        result.append(item.model_copy(update={"id": ws_id}))
    return result


@router.get("", response_model=list[WorkspaceOut])
async def list_workspaces():
    items = _configured()
    if not items:
        items = _defaults()
    return _dedupe(items)
