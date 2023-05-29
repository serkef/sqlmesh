import os

from sqlmesh.core.config import (
    AirflowSchedulerConfig,
    AutoCategorizationMode,
    CategorizerConfig,
    Config,
    DuckDBConnectionConfig,
)
from sqlmesh.core.notification_target import (
    BasicSMTPNotificationTarget,
    NotificationStatus,
    SlackWebhookNotificationTarget,
)
from sqlmesh.core.user import User, UserRole

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class CustomSMTPNotificationTarget(BasicSMTPNotificationTarget):
    def notify_run_failure(self, exc: Exception) -> None:
        with open("/home/sqlmesh/sqlmesh.log", "r", encoding="utf-8") as f:
            msg = f"{exc}\n\n{f.read()}"
        subject = "SQLMesh Run Failed!"
        self.send(notification_status=NotificationStatus.FAILURE, msg=msg, subject=subject)


# An in memory DuckDB config.
config = Config(default_connection=DuckDBConnectionConfig())


# A configuration used for SQLMesh tests.
test_config = Config(
    default_connection=DuckDBConnectionConfig(),
    auto_categorize_changes=CategorizerConfig(sql=AutoCategorizationMode.SEMI),
)

# A stateful DuckDB config.
local_config = Config(
    default_connection=DuckDBConnectionConfig(database=f"{DATA_DIR}/local.duckdb"),
)

# Due to a 3.7 mypy bug we ignore. Can remove once 3.7 support is dropped.
airflow_config = Config(default_scheduler=AirflowSchedulerConfig())  # type: ignore


# Due to a 3.7 mypy bug we ignore. Can remove once 3.7 support is dropped.
airflow_config_docker = Config(  # type: ignore
    default_scheduler=AirflowSchedulerConfig(airflow_url="http://airflow-webserver:8080/")
)


required_approvers_config = Config(
    default_connection=DuckDBConnectionConfig(),
    users=[User(username="test", roles=[UserRole.REQUIRED_APPROVER])],
    notification_targets=[
        SlackWebhookNotificationTarget(
            notify_on_apply_start=True,
            notify_on_run_start=True,
            notify_on_apply_failure=True,
            notify_on_run_failure=True,
            notify_on_audit_failure=True,
            url=os.getenv("SLACK_WEBHOOK_URL"),
        ),
        CustomSMTPNotificationTarget(
            notify_on_run_failure=True,
            host=os.getenv("SMTP_HOST"),
            user=os.getenv("SMTP_USER"),
            password=os.getenv("SMTP_PASSWORD"),
            sender="sushi@example.com",
            recipients=[
                "team@example.com",
            ],
        ),
    ],
)
