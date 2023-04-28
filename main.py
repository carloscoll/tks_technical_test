import sys

import uvicorn
from fastapi import FastAPI

from app.api.endpoints import inspector_endpoints, task_endpoints, task_assignment_endpoints
from app.core.db.session import get_db_session
from app.core.models.models import Base

app = FastAPI()

app.include_router(inspector_endpoints.router, prefix="/inspector", tags=["inspector"])
app.include_router(task_endpoints.router, prefix="/task", tags=["task"])
app.include_router(task_assignment_endpoints.router, prefix="/task_assignment", tags=["task_assignment"])


def main():
    if sys.argv[1] == "migrate":
        try:
            session = next(get_db_session())
            print(session.__dict__)
        except Exception as e:
            print(f"Unable to connect to the database. Exception: {e}")
            return

        try:
            Base.metadata.drop_all(bind=session.get_bind())
            Base.metadata.create_all(bind=session.get_bind())
        except Exception as e:
            print(f"Unable to create tables. Exception: {e}")
            session.close()
            return

        session.close()
        exit()

    if sys.argv[1] == "run":
        uvicorn.run("main:app", host="0.0.0.0", port=5050, log_level="info")


if __name__ == '__main__':
    main()
