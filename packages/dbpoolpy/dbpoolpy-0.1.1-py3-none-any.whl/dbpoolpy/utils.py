import time
import logging
from .conf import LOG_CONF

log = logging.getLogger()

class DBFunc(object):
    def __init__(self, data):
        self.value = data

def timeit(func):
    def _(*args, **kwargs):
        starttm = time.time()
        ret = 0
        num = 0
        err = ''
        try:
            retval = func(*args, **kwargs)
            t = str(type(retval))
            if t == "<class 'list'>":
                num = len(retval)
            elif t == "<class 'dict'>":
                num = 1
            elif t == "<class 'int'>":
                ret = retval
            return retval
        except Exception as e:
            err = str(e)
            ret = -1
            raise
        finally:
            endtm = time.time()
            conn = args[0]
            # dbcf = conn.pool.dbcf
            dbcf = conn.param

            sql = repr(args[1])
            if not LOG_CONF.get('log_allow_print_sql', True):
                sql = '***'

            log.info(
                'server=%s|id=%d|name=%s|user=%s|addr=%s:%d|db=%s|idle=%d|busy=%d|max=%d|trans=%d|time=%d|ret=%s|num=%d|sql=%s|err=%s',
                conn.type, conn.conn_id % 10000,
                conn.name, dbcf.get('user', ''),
                dbcf.get('host', ''), dbcf.get('port', 0),
                dbcf.get('db', ''),
                len(conn.pool.dbconn_idle),
                len(conn.pool.dbconn_using),
                conn.pool.max_conn, conn.trans,
                int((endtm - starttm) * 1000000),
                str(ret), num,
                sql, err)

    return _
