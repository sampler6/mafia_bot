import csv
import string

from sqlalchemy import delete, insert
from src.db.database import async_session
from src.db.tables import Roles


async def update_roles():
    columns: list[list] = []
    async with async_session() as session:
        await session.execute(delete(Roles).where(Roles.__table__.c.role_id != -1))
        with open("src/data.csv") as data:
            reader = csv.reader(data, delimiter=';')
            for i in range(0, 11):
                columns.append([])
            count = -1
            for row in reader:
                count += 1
                if count == 0:
                    continue
                columns[count-1] = row

        for i in range(1, len(columns) + 1):
            stmt = insert(Roles).values([i]+columns[i-1])
            await session.execute(stmt)
        await session.commit()

