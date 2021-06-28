# fixme : note host is localhost
import mysql.connector
import traceback


def connect_database(hostname, db_name):
    """

    :return:
    """
    try:
        print('connect_database() : hostname=' + hostname)
        mydb = mysql.connector.connect(
            host=hostname,
            database=db_name,
            user="metmini",
            password="metmini"
        )

        mycursor = mydb.cursor()

        return (mydb, mycursor)

    except Exception as e:
        print(e.__str__())
        traceback.print_exc()
        return (None, None)