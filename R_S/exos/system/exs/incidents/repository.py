from typing import Any
from uuid import UUID

from sqlalchemy import create_engine
from sqlalchemy import ResultProxy
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from entities import Incident
from schemas import IncidentSchema


Base = declarative_base()


class IncidentRepository:
    def __init__(self):
        self.engine = create_engine('sqlite:///sqlalchemy_example.db')
        Base.metadata.create_all(bind=self.engine)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def create(self, incident: Incident) -> Incident | None:
        try:
            with self.session as session:
                result: IncidentSchema | None = session.scalar(
                    insert(IncidentSchema)
                    .values(
                        id=incident.id,
                        title=incident.title,
                        level=incident.level,
                        created=incident.created,
                        updated=incident.updated,
                    )
                    .returning(IncidentSchema)
                )
                if not result:
                    print("Incident non créé en base de données")
                saved_entity = self._map_db_result_to_entity(result)
                session.commit()
        except SQLAlchemyError as exc:
            print("Erreur à la création de l'incident en base de données")
        except (KeyError, AttributeError) as exc:
            print("Erreur à lors du mapping")
        else:
            print("Incident inséré en base de données")
            return saved_entity

    # def update_task(self, task_id: UUID, input_file_link: str | None) -> None:
    #     query = update(TaskSchema).values(input_file_link=input_file_link).where(TaskSchema.id == task_id)
    #     try:
    #         with self.db as _db:
    #             result: ResultProxy = _db.execute(query)
    #             _db.commit()
    #             assert result.rowcount == 1  # noqa: S101
    #     except SQLAlchemyError as exc:
    #         message_sql: str = (
    #             f"[update-task] SQL error when updating the task {task_id}" + "."
    #             if input_file_link is None
    #             else f" linked to the file: {input_file_link}."
    #         )
    #         logger.exception(message_sql)
    #         raise TaskRepositoryException(message_sql) from exc
    #     except AssertionError as exc:
    #         message_assert: str = (
    #             f"[update-task] Row count error when updating the task {task_id}" + "."
    #             if input_file_link is None
    #             else f" linked to the file: {input_file_link}."
    #         )
    #         logger.exception(message_assert)
    #         raise TaskRepositoryException(message_assert) from exc
    #     else:
    #         message_success: str = (
    #             f"[update-task] Successfully updated the task {task_id}" + "."
    #             if input_file_link is None
    #             else f" linked to the file: {input_file_link}."
    #         )
    #         logger.info(message_success)

    # def get_task(self, task_id: UUID) -> Task:
    #     try:
    #         with self.read_only_db as _db:
    #             result = _db.execute(select(TaskSchema).where(TaskSchema.id == task_id)).scalar_one()
    #     except SQLAlchemyError as e:
    #         message: str = f"[get-task] Error when getting the task: {task_id}."
    #         logger.exception(message)
    #         raise TaskRepositoryNotFoundException(message) from e
    #
    #     return self._map_db_result_to_task(result)

    @staticmethod
    def _map_db_result_to_entity(result: IncidentSchema) -> Incident:

        return Incident(
            id=result.id,
            title=result.title,
            level=result.level,
            created=result.created,
            updated=result.updated,
        )
