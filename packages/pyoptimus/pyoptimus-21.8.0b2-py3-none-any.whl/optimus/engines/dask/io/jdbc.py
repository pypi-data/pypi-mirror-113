from optimus.engines.base.dask.io.jdbc import DaskBaseJDBC


class JDBC(DaskBaseJDBC):
    def __init__(self, host, database, user, password, port=None, driver=None, schema="public", oracle_tns=None,
                 oracle_service_name=None, oracle_sid=None, presto_catalog=None, cassandra_keyspace=None,
                 cassandra_table=None, bigquery_project=None, bigquery_dataset=None):
        super().__init__(host, database, user, password, port=port, driver=driver, schema=schema,
                         oracle_tns=oracle_tns,
                         oracle_service_name=oracle_service_name, oracle_sid=oracle_sid,
                         presto_catalog=presto_catalog,
                         cassandra_keyspace=cassandra_keyspace,
                         cassandra_table=cassandra_table,
                         bigquery_project=bigquery_project,
                         bigquery_dataset=bigquery_dataset)
