from datetime import datetime

import pytest
import pandas as pd

from mssql_dataframe import connect
from mssql_dataframe.core import helpers, create


class package:
    def __init__(self, connection):
        self.connection = connection
        self.create = create.create(connection)

@pytest.fixture(scope="module")
def sql():
    db = connect.connect(database_name='tempdb', server_name='localhost', autocommit=False)
    yield package(db)
    db.connection.close()


@pytest.fixture(scope="module")
def dataframe():
    dataframe = pd.DataFrame({
        '_varchar': [None,'b','c','4','e'],
        '_tinyint': [None,2,3,4,5],
        '_smallint': [256,2,6,4,5],
        '_int': [32768,2,3,4,5],
        '_bigint': [2147483648,2,3,None,5],
        '_float': [1.111111,2,3,4,5],
        '_time': [datetime.now().time()]*5,
        '_datetime': [datetime.now()]*4+[pd.NaT]
    })
    return dataframe


def test_table_column(sql):

    table_name = '##test_table_column'
    columns = {"A": "VARCHAR"}
    sql.create.table(table_name, columns)
    schema = helpers.get_schema(sql.connection, table_name)

    assert len(schema)==1
    assert all(schema.index=='A')
    assert all(schema['data_type']=='varchar')
    assert all(schema['max_length']==1)
    assert all(schema['precision']==0)
    assert all(schema['scale']==0)
    assert all(schema['is_nullable']==True)
    assert all(schema['is_identity']==False)
    assert all(schema['is_primary_key']==False)


def test_table_pk(sql):

    table_name = "##test_table_pk"
    columns = {"A": "TINYINT", "B": "VARCHAR(100)", "C": "DECIMAL(5,2)"}
    primary_key_column = "A"
    not_null = "B"
    sql.create.table(table_name, columns, not_null=not_null, primary_key_column=primary_key_column)
    schema = helpers.get_schema(sql.connection, table_name)

    assert len(schema)==3
    assert all(schema.index==['A','B','C'])
    assert all(schema['data_type']==['tinyint','varchar','decimal'])
    assert all(schema['max_length']==[1,100,5])
    assert all(schema['precision']==[3,0,5])
    assert all(schema['scale']==[0,0,2])
    assert all(schema['is_nullable']==[False, False, True])
    assert all(schema['is_identity']==[False, False, False])
    assert all(schema['is_primary_key']==[True, False, False])


def test_table_errorpk(sql):

    with pytest.raises(ValueError):
        table_name = "##test_table_errorpk"
        columns = {"A": "TINYINT", "B": "VARCHAR(100)", "C": "DECIMAL(5,2)"}
        primary_key_column = "A"
        not_null = "B"
        sql.create.table(table_name, columns, not_null=not_null, primary_key_column=primary_key_column, sql_primary_key=True)


def test_table_sqlpk(sql):

    table_name = '##test_table_sqlpk'
    columns = {"A": "VARCHAR"}
    sql.create.table(table_name, columns, sql_primary_key=True)
    schema = helpers.get_schema(sql.connection, table_name)

    assert len(schema)==2
    assert all(schema.index==['_pk','A'])
    assert all(schema['data_type']==['int','varchar'])
    assert all(schema['max_length']==[4,1])
    assert all(schema['precision']==[10,0])
    assert all(schema['scale']==[0,0])
    assert all(schema['is_nullable']==[False,True])
    assert all(schema['is_identity']==[True,False])
    assert all(schema['is_primary_key']==[True,False])


def test_table_from_dataframe_simple(sql):

    table_name = '##test_table_from_dataframe_simple'
    dataframe = pd.DataFrame({"ColumnA": [1]})
    sql.create.table_from_dataframe(table_name, dataframe)
    schema = helpers.get_schema(sql.connection, table_name)

    assert len(schema)==1
    assert all(schema.index=='ColumnA')
    assert all(schema['data_type']=='tinyint')
    assert all(schema['max_length']==1)
    assert all(schema['precision']==3)
    assert all(schema['is_nullable']==False)
    assert all(schema['is_identity']==False)
    assert all(schema['is_primary_key']==False)
    assert all(schema['python_type']=='Int8')


def test_table_from_dataframe_errorpk(sql):

    with pytest.raises(ValueError):
        table_name = '##test_table_from_dataframe_nopk'
        sql.create.table_from_dataframe(table_name, dataframe, primary_key="ColumnName")


def test_table_from_dataframe_nopk(sql, dataframe):

    table_name = '##test_table_from_dataframe_nopk'
    sql.create.table_from_dataframe(table_name, dataframe, primary_key=None)
    schema = helpers.get_schema(sql.connection, table_name)

    assert len(schema)==8
    assert all(schema.index==['_varchar', '_tinyint', '_smallint', '_int', '_bigint', '_float','_time', '_datetime'])
    assert all(schema['data_type']==['varchar', 'tinyint', 'smallint', 'int', 'bigint', 'float', 'time', 'datetime'])
    assert all(schema['max_length']==[1, 1, 2, 4, 8, 8, 5, 8])
    assert all(schema['precision']==[0, 3, 5, 10, 19, 53, 16, 23])
    assert all(schema['scale']==[0, 0, 0, 0, 0, 0, 7, 3])
    assert all(schema['is_nullable']==[True, True, False, False, True, False, False, True])
    assert all(schema['is_identity']==False)
    assert all(schema['is_primary_key']==False)


def test_table_from_dataframe_sqlpk(sql, dataframe):

    table_name = '##test_table_from_dataframe_sqlpk'
    sql.create.table_from_dataframe(table_name, dataframe, primary_key='sql')
    schema = helpers.get_schema(sql.connection, table_name)

    assert len(schema)==9
    assert all(schema.index==['_pk','_varchar', '_tinyint', '_smallint', '_int', '_bigint', '_float','_time', '_datetime'])
    assert all(schema['data_type']==['int','varchar', 'tinyint', 'smallint', 'int', 'bigint', 'float', 'time', 'datetime'])
    assert all(schema['max_length']==[4, 1, 1, 2, 4, 8, 8, 5, 8])
    assert all(schema['precision']==[10, 0, 3, 5, 10, 19, 53, 16, 23])
    assert all(schema['scale']==[0, 0, 0, 0, 0, 0, 0, 7, 3])
    assert all(schema['is_nullable']==[False, True, True, False, False, True, False, False, True])
    assert all(schema['is_identity']==[True, False, False, False, False, False, False, False, False])
    assert all(schema['is_primary_key']==[True, False, False, False, False, False, False, False, False])


def test_table_from_dataframe_indexpk(sql, dataframe):

    # unamed dataframe index
    table_name = '##test_table_from_dataframe_indexpk'
    sql.create.table_from_dataframe(table_name, dataframe, primary_key='index')
    schema = helpers.get_schema(sql.connection, table_name)

    assert len(schema)==9
    assert all(schema.index==['_index','_varchar', '_tinyint', '_smallint', '_int', '_bigint', '_float','_time', '_datetime'])
    assert all(schema['data_type']==['tinyint','varchar', 'tinyint', 'smallint', 'int', 'bigint', 'float', 'time', 'datetime'])
    assert all(schema['max_length']==[1, 1, 1, 2, 4, 8, 8, 5, 8])
    assert all(schema['precision']==[3, 0, 3, 5, 10, 19, 53, 16, 23])
    assert all(schema['scale']==[0, 0, 0, 0, 0, 0, 0, 7, 3])
    assert all(schema['is_nullable']==[False, True, True, False, False, True, False, False, True])
    assert all(schema['is_identity']==False)
    assert all(schema['is_primary_key']==[True, False, False, False, False, False, False, False, False])

    # named dataframe index
    table_name = '##DataFrameIndexPKNamed'
    dataframe.index.name = 'NamedIndex'
    sql.create.table_from_dataframe(table_name, dataframe, primary_key='index')
    schema = helpers.get_schema(sql.connection, table_name)

    assert len(schema)==9
    assert all(schema.index==['NamedIndex','_varchar', '_tinyint', '_smallint', '_int', '_bigint', '_float','_time', '_datetime'])
    assert all(schema['data_type']==['tinyint','varchar', 'tinyint', 'smallint', 'int', 'bigint', 'float', 'time', 'datetime'])
    assert all(schema['max_length']==[1, 1, 1, 2, 4, 8, 8, 5, 8])
    assert all(schema['precision']==[3, 0, 3, 5, 10, 19, 53, 16, 23])
    assert all(schema['scale']==[0, 0, 0, 0, 0, 0, 0, 7, 3])
    assert all(schema['is_nullable']==[False, True, True, False, False, True, False, False, True])
    assert all(schema['is_identity']==False)
    assert all(schema['is_primary_key']==[True, False, False, False, False, False, False, False, False])


def test_table_from_dataframe_inferpk(sql):

    table_name = '##test_table_from_dataframe_inferpk_integer'

    # integer primary key
    dataframe = pd.DataFrame({
        '_varchar1': ['a','b','c','d','e'],
        '_varchar2': ['aa','b','c','d','e'],
        '_tinyint': [None, 2, 3, 4, 5],
        '_smallint': [265, 2, 6, 4, 5],
        '_int': [32768, 2, 3, 4, 5],
        '_float1': [1.1111, 2, 3, 4, 5],
        '_float2': [1.1111, 2, 3, 4, 6]
    })
    sql.create.table_from_dataframe(table_name, dataframe, primary_key='infer')
    schema = helpers.get_schema(sql.connection, table_name)
    assert schema.at['_smallint','is_primary_key']

    # float primary key
    dataframe = pd.DataFrame({
        '_varchar1': ['a','b','c','d','e'],
        '_varchar2': ['aa','b','c','d','e'],
        '_tinyint': [None, 2, 3, 4, 5],
        '_float1': [1.1111, 2, 3, 4, 5],
        '_float2': [1.1111, 2, 3, 4, 6]
    })
    table_name = '##test_table_from_dataframe_inferpk_float'
    sql.create.table_from_dataframe(table_name, dataframe, primary_key='infer')
    schema = helpers.get_schema(sql.connection, table_name)
    assert schema.at['_float1','is_primary_key']

    # string primary key
    dataframe = pd.DataFrame({
        '_varchar1': ['a','b','c','d','e'],
        '_varchar2': ['aa','b','c','d','e'],
    })
    table_name = '##test_table_from_dataframe_inferpk_string'
    sql.create.table_from_dataframe(table_name, dataframe, primary_key='infer')
    schema = helpers.get_schema(sql.connection, table_name)
    assert schema.at['_varchar1','is_primary_key']

    # uninferrable primary key
    dataframe = pd.DataFrame({
        '_varchar1': [None,'b','c','d','e'],
        '_varchar2': [None,'b','c','d','e'],
    })
    table_name = '##test_table_from_dataframe_inferpk_uninferrable'
    sql.create.table_from_dataframe(table_name, dataframe, primary_key='infer')
    schema = helpers.get_schema(sql.connection, table_name)
    assert all(schema['is_primary_key']==False)

