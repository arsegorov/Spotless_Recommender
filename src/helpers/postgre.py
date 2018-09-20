import psycopg2


def read_from_postgresql(sqlContext, config):
    """
    reads from PostgreSQL database with given configurations into Spark DataFrame
    :type sqlContext: SQLContext        Spark SQL Context for saving
    :type config    : dict              dictionary with PostgreSQL configurations
    :rtype          : Spark DataFrame   SQL DataFrame representing the table
    """
    options = "".join([".options(%s=config[\"%s\"])" % (opt, opt) for opt in config.keys()])
    command = "sqlContext.read.format(\"jdbc\")%s.load()" % options
    return eval(command)


def add_index_postgresql(dbtable, column, config):
    """
    adds index to PostgreSQL table dbtable on column
    :type dbtable: str      name of the table
    :type column : str      name of the column
    :type config : dict     dictionary with PostgreSQL configurations
    """
    conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (config["host"],
                                                                     config["dbname"],
                                                                     config["user"],
                                                                     config["password"])
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX ON %s (%s)" % (dbtable, column))
    conn.commit()
    cursor.close()
    conn.close()
