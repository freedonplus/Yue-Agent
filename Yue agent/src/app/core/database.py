from collections.abc import AsyncIterator

from sqlalchemy import URL, event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from settings import settings


"""
    ═══════════════════════════════════════════════════
                        数据库配置
    ═══════════════════════════════════════════════════
"""


# sqlite的url
DATABASE_URL = URL.create("sqlite+aiosqlite", database=str(settings.DB_PATH))

# 创建连接池引擎
engine = create_async_engine(
                DATABASE_URL,
                echo=settings.SQLALCHEMY_ECHO,
                pool_size=settings.POOL_SIZE,
                max_overflow=settings.MAX_OVERFLOW,
                pool_timeout=settings.POOL_TIMEOUT,
        )


# 创建基类
class Base(DeclarativeBase):
    pass


# 每次连上数据库时先念的“咒语”
@event.listens_for(engine.sync_engine, "connect")
def _set_sqlite_pragmas(dbapi_connection, _connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    # WAL 下 NORMAL 已足够可靠，减少每次提交的 fsync 开销
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA busy_timeout=5000")
    cursor.close()


SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,    # 产出异步 session
    expire_on_commit=False, # commit() 后对象属性仍然可读，不会触发额外查询
    autoflush=False,        # 查询前不自动把未提交的改动刷进数据库，行为可预测
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session


# —————————SQLite 轻量迁移：create_all 不会给旧表补列————————
async def _table_columns(conn, table: str) -> set[str]:
    result = await conn.exec_driver_sql(f'PRAGMA table_info("{table}")')
    return {row[1] for row in result.fetchall()}


async def _ensure_columns(conn) -> None:
    tool_columns = await _table_columns(conn, "tools")
    if "available_tools" not in tool_columns:
        await conn.exec_driver_sql(
            "ALTER TABLE tools ADD COLUMN available_tools "
            "TEXT NOT NULL DEFAULT '[]'"
        )
    if "tools_checked_at" not in tool_columns:
        await conn.exec_driver_sql(
            "ALTER TABLE tools ADD COLUMN tools_checked_at DATETIME"
        )

    link_columns = await _table_columns(conn, "agent_role_tools")
    if "tool_names" not in link_columns:
        await conn.exec_driver_sql(
            "ALTER TABLE agent_role_tools ADD COLUMN tool_names TEXT"
        )

    session_columns = await _table_columns(conn, "chat_sessions")
    if "workdir" not in session_columns:
        await conn.exec_driver_sql(
            "ALTER TABLE chat_sessions ADD COLUMN workdir "
            "TEXT NOT NULL DEFAULT ''"
        )

    role_columns = await _table_columns(conn, "agent_roles")
    if "approval_tools" not in role_columns:
        await conn.exec_driver_sql(
            "ALTER TABLE agent_roles ADD COLUMN approval_tools "
            "TEXT NOT NULL DEFAULT '[]'"
        )
    if "is_output_gate" not in role_columns:
        await conn.exec_driver_sql(
            "ALTER TABLE agent_roles ADD COLUMN is_output_gate "
            "BOOLEAN NOT NULL DEFAULT 0"
        )


async def init_db() -> None:
    from app.model import agent_roles
    from app.model import chat_messages
    from app.model import chat_sessions
    from app.model import providers
    from app.model import skills
    from app.model import tools
    from Yue.memory import models as memory_models

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await _ensure_columns(conn)


async def close_db() -> None:
    await engine.dispose()