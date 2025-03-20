"""초기 데이터베이스 마이그레이션

Revision ID: 001
Revises:
Create Date: 2024-03-20 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """업그레이드 마이그레이션을 실행합니다."""
    # 사용자 테이블 생성
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("salt", sa.String(64), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("is_superuser", sa.Boolean(), default=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    # 세션 테이블 생성
    op.create_table(
        "sessions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("token", sa.String(255), unique=True, nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    # 문서 테이블 생성
    op.create_table(
        "documents",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    # 인덱스 생성
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_sessions_token", "sessions", ["token"])
    op.create_index("ix_documents_title", "documents", ["title"])


def downgrade() -> None:
    """다운그레이드 마이그레이션을 실행합니다."""
    # 인덱스 삭제
    op.drop_index("ix_documents_title")
    op.drop_index("ix_sessions_token")
    op.drop_index("ix_users_email")

    # 테이블 삭제
    op.drop_table("documents")
    op.drop_table("sessions")
    op.drop_table("users")
