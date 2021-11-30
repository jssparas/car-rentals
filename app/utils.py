from pathlib import Path
from app import log


def errors_to_desc(errors):
    msg = []

    for k in errors:
        if isinstance(errors[k][0], str):
            msg.append('\"{}\": {}'.format(k, ';'.join(errors[k])))
        else:
            inner_message = ''
            for inner_errors in errors[k]:
                inner_message += errors_to_desc(inner_errors)
            msg.append('\"{}\": {}'.format(k, inner_message))

    return '. '.join(msg)


LOG = log.get_logger()


def seed(engine):
    """ seeds the test db with dummy data """
    # imports all seed data from csv files
    LOG.debug('Importing seed data...')
    populate_testdb(engine, "app/tests/database")


def populate_testdb(engine, csv_folder="tests"):
    test_dir = Path(csv_folder)
    connection = engine.raw_connection()
    connection.cursor().execute("SET session_replication_role = 'replica';")
    for filename in test_dir.glob("*.csv"):
        csv_file = filename.as_posix()
        table_name = filename.stem
        import_csv(connection, csv_file, table_name)

    connection.cursor().execute("select setval('city_id_seq', 2, true);")
    connection.cursor().execute("select setval('rental_zone_id_seq', 4, true);")
    connection.commit()
    connection.cursor().execute("SET session_replication_role = 'origin';")


def import_csv(connection, csv_file, table_name):
    with open(csv_file) as f:
        cursor = connection.cursor()
        # this will disable all triggers, foreign-key checks etc.
        csv_header = f.readline()
        cmd = (
            f"COPY {table_name}({csv_header}) from STDIN"
            " with (FORMAT CSV, HEADER FALSE)"
        )
        cursor.copy_expert(cmd, f)
