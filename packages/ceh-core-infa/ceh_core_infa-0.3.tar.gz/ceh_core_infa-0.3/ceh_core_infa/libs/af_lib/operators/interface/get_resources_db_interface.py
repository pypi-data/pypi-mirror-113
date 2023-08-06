import pandas as pd

from .base_interface import BaseInterface
from .....utils.utils import get_conn_db, tuple2str__sql_query


def _get_mapping_from_db(
        db_param,
        workflows,
        query,
        load_type_cd,
        meta_version
):
    conn = get_conn_db(db_param)

    wrk = tuple2str__sql_query(workflows)
    df = pd.read_sql_query(
        sql=query % (load_type_cd, meta_version, wrk),
        con=conn
    )

    if not df.shape[0]:
        raise RuntimeError('Failed, no data')

    result = df.to_dict(orient='index')

    return result.values()


class GetResourcesDBInterface(BaseInterface):
    def __init__(
            self,
            db_param,
            workflows,
            query,
            load_type_cd,
            meta_version,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.db_param = db_param
        self.query = query
        self.load_type_cd = load_type_cd
        self.meta_version = meta_version
        self.workflows = workflows

    @staticmethod
    def get_resource(
            db_param,
            query,
            workflows,
            load_type_cd,
            meta_version,
            *args,
            **kwargs
    ):
        _, _ = args, kwargs
        return _get_mapping_from_db(
            db_param,
            workflows,
            query,
            load_type_cd,
            meta_version
        )

    def execute(self):
        executor = self.dynamic_executor(
            ex_func=self.get_resource,
            op_kwargs=self.__dict__,
            timer=self.timer
        )

        return executor.executor()
