# -*- coding: utf-8 -*-

import celery
import sqlalchemy.orm

import skopy.command
import skopy.feature

broker = celery.Celery("tasks", backend="rpc://", broker="amqp://localhost")


class Session(celery.Task):
    def __init__(self):
        self._engine = sqlalchemy.create_engine("postgresql+pg8000://allen@localhost/skopy-test", echo=True)

        skopy.feature.Base.metadata.create_all(self._engine)

        self._session = None

    def after_return(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        pass

    @property
    def session(self):
        if self._session is None:
            session_maker = sqlalchemy.orm.sessionmaker()

            session_maker.configure(bind=self._engine)

            self._session = session_maker()

        return self._session


@broker.task(base=Session, bind=True)
def measure(self, x, y):
    image = skopy.feature.Image(x, y)

    self.session.add(image)

    # self.session.commit()
