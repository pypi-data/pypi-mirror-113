from sqlalchemy import event
from sqlalchemy.orm import Session


def before_request_log(app, model, user_id, method, raw_id):
    app.logger.info(
        f"User with id={user_id} has started {method} model {model} (raw ID={raw_id})"
    )


def after_request_log(app, model, user_id, method, raw_id):
    app.logger.info(
        f"User with id={user_id} has finished {method} model {model} (raw ID={raw_id})"
    )


def before_rollback_log(app, model, user_id, method, raw_id):
    app.logger.info(
        f"Before rollback user with id={user_id} has started {method} model {model} (raw ID={raw_id})"
    )


def check_owner(instance):
    try:
        owner_id = instance.add_by_user
    except:
        owner_id = None
    return owner_id


def session_handler(session):
    session_info = {}
    session_instance = ""
    method = ""
    for instance in session.new:
        method = "creating"
        session_instance = instance
    for instance in session.deleted:
        method = "deleting"
        session_instance = instance
    for instance in session.dirty:
        method = "updating"
        session_instance = instance
    owner_id = check_owner(session_instance)
    session_info["user_id"] = owner_id
    session_info["method"] = method
    session_info["model"] = session_instance.__tablename__
    session_info["raw_id"] = session_instance.id
    return session_info


class Logger:

    def __init__(self, app):
        self.app = app

    def session_before_flush(self, session, flush_context, instanses):
        about_session = session_handler(session)
        before_request_log(
            self.app,
            about_session["model"],
            about_session["user_id"],
            about_session["method"],
            about_session["raw_id"],
        )

    def listen_before_flush(self):
        event.listen(Session, "before_flush", self.session_before_flush)

    def session_after_flush(self, session, flush_context):
        about_session = session_handler(session)
        after_request_log(
            self.app,
            about_session["model"],
            about_session["user_id"],
            about_session["method"],
            about_session["raw_id"],
        )

    def listen_after_flush(self):
        event.listen(Session, "after_flush", self.session_after_flush)

    def session_after_rollback(self, session):
        about_session = session_handler(session)
        before_rollback_log(
            self.app,
            about_session["model"],
            about_session["user_id"],
            about_session["method"],
            about_session["raw_id"],
        )

    def listen_after_rollback(self):
        event.listen(Session, "after_rollback", self.session_after_rollback)
