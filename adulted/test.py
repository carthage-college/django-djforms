from djzbar.settings import INFORMIX_EARL_TEST

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

import sys

def main():

    DATE = datetime.now().strftime("%m-%d-%Y")
    TIME = datetime.now().strftime("%H%M")

    username = "coldfuse"
    password = "carth10"
    host = "wilson"
    port = 18001
    db="train"

    earl = 'informix://%s:%s@%s:%s/%s' % (username,password,host,port,db)
    #engine = create_engine(earl)
    engine = create_engine(INFORMIX_EARL_TEST)
    connection = engine.connect()

    # initialize and create id
    sql =   'INSERT INTO apptmp_rec (add_date,add_tm,app_source,stat) VALUES (%s, %s, "AEA", "P")' % (DATE,TIME)
    connection.execute(sql)
    #engine.execute(sql)

    # get unifying id (uid)
    sql =   """
            SELECT apptmp_no
            FROM   apptmp_rec
            WHERE apptmp_no = DBINFO( 'sqlca.sqlerrd1' )
            """
    sql = "SELECT DISTINCT dbinfo('sqlca.sqlerrd1') FROM apptmp_rec"
    objects = connection.execute(sql)
    #objects = engine.execute(sql)

    for r in objects:
        #print(r[0])
        #print(r.cw_no)
        uid = r[0]

    print uid

    connection.close()

if __name__ == "__main__":
    sys.exit(main())

"""
CREATE TABLE cars:apptmp_rec (
    apptmp_no serial NOT NULL,
    stu_id int DEFAULT 0 NOT NULL,
    ss_no char(11) NOT NULL,
    birth_date date,
    add_date date,
    add_tm smallint DEFAULT 0 NOT NULL,
    app_source char(5),
    stat char(1),
    rsv char(1),
    payment_method char(20),
    pay_amt money(16,2) DEFAULT 0 NOT NULL,
    card_type char(20),
    card_number char(10),
    response_code char(1),
    reason_code char(2),
    reason_txt char(60),
    pymt_req char(1),
    waiver_code char(10),
    waiver_txt varchar(200),
    webtrans_no int DEFAULT 0,
    bmsg_no int DEFAULT 0,
    pymt_guid char(36)
);
"""

