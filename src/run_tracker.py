from sqlalchemy import text

from database import engine


PIPELINE_NAME = "ecommerce_etl"


def start_pipeline_run():
    with engine.begin() as connection:
        result = connection.execute(
            text("""
                INSERT INTO pipeline_runs (
                    pipeline_name,
                    status,
                    records_processed
                )
                VALUES (
                    :pipeline_name,
                    'RUNNING',
                    0
                )
                RETURNING run_id;
            """),
            {
                "pipeline_name": PIPELINE_NAME
            }
        )

        run_id = result.scalar()

    return run_id


def complete_pipeline_run(run_id, records_processed):
    with engine.begin() as connection:
        connection.execute(
            text("""
                UPDATE pipeline_runs
                SET
                    status = 'SUCCESS',
                    completed_at = CURRENT_TIMESTAMP,
                    records_processed = :records_processed
                WHERE run_id = :run_id;
            """),
            {
                "run_id": run_id,
                "records_processed": records_processed
            }
        )


def fail_pipeline_run(run_id):
    with engine.begin() as connection:
        connection.execute(
            text("""
                UPDATE pipeline_runs
                SET
                    status = 'FAILED',
                    completed_at = CURRENT_TIMESTAMP
                WHERE run_id = :run_id;
            """),
            {
                "run_id": run_id
            }
        )