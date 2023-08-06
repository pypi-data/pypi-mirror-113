import sqlite3
import struct


# https://sqlite.org/lang_createtable.html
SQL_MAKE_DB = """CREATE TABLE IF NOT EXISTS db (key BLOB, value BLOB);"""
# https://sqlite.org/lang_createindex.html
SQL_MAKE_DB_INDEX_ASC = """CREATE UNIQUE INDEX IF NOT EXISTS asc ON db (key ASC);"""
SQL_MAKE_DB_INDEX_DESC = """CREATE UNIQUE INDEX IF NOT EXISTS desc ON db (key DESC);"""


def open(path):
    cnx = sqlite3.connect(path)
    with cnx:
        cnx.execute(SQL_MAKE_DB)
        cnx.execute(SQL_MAKE_DB_INDEX_ASC)
        cnx.execute(SQL_MAKE_DB_INDEX_DESC)
    return cnx


def close(cnx):
    cnx.close()


def txn(cnx, func, *args, **kwargs):
    try:
        func(cnx, *args, **kwargs)
    except Exception:
        cnx.rollback()
        raise
    finally:
        cnx.commit()


SQL_QUERY_GET = """SELECT value FROM db WHERE key=?"""


def get(cnx, key):
    cursor = cnx.execute(SQL_QUERY_GET, (key,))
    out = cursor.fetchone()
    out = None if out is None else out[0]
    return out


SQL_QUERY_SET = """INSERT INTO db (key, value) VALUES(?, ?)"""


def set(cnx, key, value):
    cnx.execute(SQL_QUERY_SET, (key, value))


SQL_QUERY_E = """SELECT key FROM db WHERE key = ?"""


def e(cnx, key):
    cursor = cnx.execute(SQL_QUERY_E, (key,))
    out = cursor.fetchone()
    return out[0] if out is not None else None


SQL_QUERY_LT = """SELECT key FROM db WHERE key < ?"""


def lt(cnx, key):
    cursor = cnx.execute(SQL_QUERY_LT, (key,))
    out = cursor.fetchone()
    return out[0] if out is not None else None


SQL_QUERY_GT = """SELECT key FROM db WHERE key > ?"""


def gt(cnx, key):
    cursor = cnx.execute(SQL_QUERY_GT, (key,))
    out = cursor.fetchone()
    return out[0] if out is not None else None


def near(cnx, key):
    out = e(cnx, key)
    if out is not None:
        return 0, out
    out = lt(cnx, key)
    if out is not None:
        return -1, out
    out = gt(cnx, key)
    if out is not None:
        return 1, out
    return None, None


SQL_QUERY_ASC = """
SELECT key, value
FROM db WHERE key >= ? AND key < ?
ORDER BY key ASC
LIMIT ?
OFFSET ?
"""


SQL_QUERY_DESC = """
SELECT key, value
FROM db WHERE key >= ? AND key < ?
ORDER BY key DESC
LIMIT ?
OFFSET ?
"""


def query(cnx, key, other, limit=-1, offset=0):
    if key < other:
        query = SQL_QUERY_ASC
    else:
        query = SQL_QUERY_DESC
        key, other = other, key

    for item in cnx.execute(query, (key, other, limit, offset)):
        yield item


SQL_QUERY_COUNT = """SELECT COUNT(key) FROM db WHERE key >= ? AND key < ?"""


def count(cnx, key, other):
    cursor = cnx.execute(SQL_QUERY_COUNT, (key, other))
    out = cursor.fetchone()[0]
    return out


SQL_QUERY_SIZE = """SELECT SUM(length(key)) + SUM(length(value)) FROM db WHERE key >= ? AND key < ?"""


def size(cnx, key, other):
    cursor = cnx.execute(SQL_QUERY_SIZE, (key, other))
    out = cursor.fetchone()[0]
    return out


SQL_QUERY_DELETE = """DELETE FROM db WHERE key = ?"""
SQL_QUERY_DELETE_RANGE = """DELETE FROM db WHERE key >= ? AND key < ?"""


def delete(cnx, key, other=None):
    if other is None:
        cnx.execute(SQL_QUERY_DELETE, (key,))
    else:
        cnx.execute(SQL_QUERY_DELETE_RANGE, (key, other))


# pack and unpack

_size_limits = tuple((1 << (i * 8)) - 1 for i in range(9))

# Define type codes:
BYTES_CODE = 0x01
FALSE_CODE = 0x02
NESTED_CODE = 0x08
NULL_CODE = 0x00
INTEGER_NEGATIVE_CODE = 0x04
INTEGER_ZERO = 0x05
INTEGER_POSITIVE_CODE = 0x06
STRING_CODE = 0x07
TRUE_CODE = 0x03

INTEGER_MAX = struct.unpack('>Q', b'\xff' * 8)[0]


def _find_terminator(v, pos):
    # Finds the start of the next terminator [\x00]![\xff] or the end of v
    while True:
        pos = v.find(b"\x00", pos)
        if pos < 0:
            return len(v)
        if pos + 1 == len(v) or v[pos + 1:pos + 2] != b"\xff":
            return pos
        pos += 2


def _decode(v, pos):
    code = v[pos]
    if code == NULL_CODE:
        return None, pos + 1
    elif code == BYTES_CODE:
        end = _find_terminator(v, pos + 1)
        return v[pos + 1 : end].replace(b"\x00\xFF", b"\x00"), end + 1
    elif code == STRING_CODE:
        end = _find_terminator(v, pos + 1)
        return v[pos + 1 : end].replace(b"\x00\xFF", b"\x00").decode("utf-8"), end + 1
    elif code == INTEGER_ZERO:
        return 0, pos + 1
    elif code == INTEGER_NEGATIVE_CODE:
        end = pos + 1 + 8
        value = struct.unpack(">Q", v[pos + 1 : end])[0] - INTEGER_MAX
        return value, end
    elif code == INTEGER_POSITIVE_CODE:
        end = pos + 1 + 8
        value = struct.unpack(">Q", v[pos + 1 : end])[0]
        return value, end
    elif code == FALSE_CODE:
        return False, pos + 1
    elif code == TRUE_CODE:
        return True, pos + 1
    elif code == NESTED_CODE:
        ret = []
        end_pos = pos + 1
        while end_pos < len(v):
            if v[end_pos] == 0x00:
                if end_pos + 1 < len(v) and v[end_pos + 1] == 0xFF:
                    ret.append(None)
                    end_pos += 2
                else:
                    break
            else:
                val, end_pos = _decode(v, end_pos)
                ret.append(val)
        return tuple(ret), end_pos + 1
    else:
        raise ValueError("Unknown data type in DB: " + repr(v))


def _encode(value, nested=False):
    if value is None:
        if nested:
            return bytes((NULL_CODE, 0xFF))
        else:
            return bytes((NULL_CODE,))
    elif isinstance(value, bool):
        if value:
            return bytes((TRUE_CODE,))
        else:
            return bytes((FALSE_CODE,))
    elif isinstance(value, bytes):
        return bytes((BYTES_CODE,)) + value.replace(b"\x00", b"\x00\xFF") + b"\x00"
    elif isinstance(value, str):
        return (
            bytes((STRING_CODE,))
            + value.encode("utf-8").replace(b"\x00", b"\x00\xFF")
            + b"\x00"
        )
    elif value == 0:
        return bytes((INTEGER_ZERO,))
    elif isinstance(value, int):
        if value > 0:
            out = bytes((INTEGER_POSITIVE_CODE,)) + struct.pack('>Q', value)
            return out
        else:
            value = INTEGER_MAX + value
            out = bytes((INTEGER_NEGATIVE_CODE,)) + struct.pack('>Q', value)
            return out
    elif isinstance(value, (tuple, list)):
        child_bytes = list(map(lambda x: _encode(x, True), value))
        return b''.join([bytes((NESTED_CODE,))] + child_bytes + [bytes((0x00,))])
    else:
        raise ValueError("Unsupported data type: {}".format(type(value)))


def pack(t):
    return b"".join((_encode(x) for x in t))


def unpack(key):
    pos = 0
    res = []
    while pos < len(key):
        r, pos = _decode(key, pos)
        res.append(r)
    return tuple(res)


def next_prefix(x):
    x = x.rstrip(b"\xff")
    return x[:-1] + bytes((x[-1] + 1,))
