def validate_sql(sql):

    sql = sql.strip().upper()

    dangerous_keywords = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE",
        "CREATE"
    ]

    for keyword in dangerous_keywords:
        if keyword in sql:
            return False

    return sql.startswith("SELECT")