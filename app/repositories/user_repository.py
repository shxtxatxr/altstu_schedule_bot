from app.database.engine import get_connection

async def save_user_group(
    user_id: int,
    external_id: str,
    group_name: str,
):
    conn = await get_connection()

    try:
        await conn.execute(
            """
            INSERT INTO user_groups
            (
                user_id,
                external_id,
                group_name
            )
            VALUES ($1, $2, $3)

            ON CONFLICT (user_id)
            DO UPDATE SET
                external_id = EXCLUDED.external_id,
                group_name = EXCLUDED.group_name
            """,
            user_id,
            external_id,
            group_name,
        )

    finally:
        await conn.close()


async def get_user_group(
    user_id: int,
):
    conn = await get_connection()

    try:
        row = await conn.fetchrow(
            """
            SELECT
                external_id,
                group_name
            FROM user_groups
            WHERE user_id = $1
            """,
            user_id,
        )

        if not row:
            return None

        return {
            "external_id": row["external_id"],
            "name": row["group_name"],
        }

    finally:
        await conn.close()