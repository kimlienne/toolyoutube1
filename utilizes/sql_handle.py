import mysql.connector
from mysql.connector import errors

from utilizes.txt_handler import read_txt


def sql_login():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        port=3306
    )


def create_database(database_name):
    mydb = sql_login()
    mycursor = mydb.cursor()
    mycursor.execute(f'CREATE DATABSE {database_name}')


# def show_list_database():
#     mydb = sql_login()
#     my_cursor = mydb.cursor()
#     my_cursor.execute("SHOW DATABASES")
#     for x in my_cursor:
#         print(x)


def return_if_exist_database(db_name, host='107.98.32.9', port='3306', user='root', password='root'):
    try:
        mydb = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db_name,
            connection_timeout=10  # Thêm timeout 10 giây
        )
        return mydb
    except errors.ProgrammingError:
        print(f"SQL database name '{db_name}' does not exist.")
        return False
    except errors.InterfaceError:
        print("Unable to connect to the database server. Please check your connection settings.")
        return False
    except errors.OperationalError:
        print("Operational error occurred while connecting to the database.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def create_table(db, table, content):
    my_cursor = return_if_exist_database(db)
    my_cursor = my_cursor.cursor()
    # print(my_cursor)
    print(f"CREATE TABLE {table} ({content})")
    my_cursor.execute(f"CREATE TABLE {table} ({content})")


def insert_account(value):
    """ex value: [('tinhhd02', 'Hoàng Đạo Tĩnh'), ('tam.hong', 'Nguyễn Hồng Tâm'), ('duy.nm1', 'Nguyễn Mạnh Duy')]"""
    mydb = return_if_exist_database('datateam')
    my_cursor = mydb.cursor()
    sql = f'INSERT INTO Account (username, fullname) VALUES (%s, %s)'
    my_cursor.executemany(sql, value)
    print(my_cursor.rowcount, "record inserted.")
    mydb.commit()


def querry_all(table):
    mydb = return_if_exist_database('datateam', host='107.98.72.37', user='datateam', password='1', port='3306')
    cursor = mydb.cursor(dictionary=True)
    query = f'SELECT * from {table}'
    cursor.execute(query)
    result = cursor.fetchall()
    for x in result:
        print(x)
    mydb.close()
    return result


def insert_data(value):
    """Ex data: [('abc', 'abc.wav', 'abc link', '1'), ('def', 'def.wav', 'abc link', '1')]"""
    mydb = return_if_exist_database('datateam')
    my_cursor = mydb.cursor()
    sql = f'INSERT INTO data (ans, scp, link_audio_folder, task_id) VALUES (%s, %s, %s, %s)'
    my_cursor.executemany(sql, value)
    print(my_cursor.rowcount, "record inserted.")
    mydb.commit()


def query_by(type_q, table, value, get_list=None, is_unique=False, sql_instance=None, debug=False):
    """index ex: [1]\n
    table: tìm ở bảng nào\n
    type_q: 'index' | 'scp'\n
    get_list: những thuộc tính của thông tin tìm được muốn trả về\n
    is_unique: True nếu muốn trả về 1 phần tử"""
    mydb = sql_instance
    cursor = mydb.cursor(dictionary=True)
    get_info = "*" if not get_list else ','.join(get_list)
    if not isinstance(type_q, list):
        type_q = [type_q]
    if len(value) != len(type_q):
        raise AttributeError('len of list value is not match with type_q')
    type_q = ' and '.join([f'{item}=%s' for item in type_q])
    query = f"SELECT {get_info} from {table} WHERE {type_q}"
    cursor.execute(query, value)
    result = cursor.fetchall()
    if debug:
        print(f'Query result:') if len(result) \
            else print(f'Query result empty in table {table} by {type_q} with value {value}')
        for x in result:
            print(x)
    return result if not is_unique or not len(result) else result[0]


def query_user_at_now(value):
    mydb = return_if_exist_database('datateam')
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * from assignment join `account` on user_id=`account`.id where username=%s and task_id=%s"
    cursor.execute(query, value)
    result = cursor.fetchall()
    print(f'Query result:') if len(result) else print('Query result empty')
    for x in result:
        print(x)
    mydb.close()
    return result


def query_frv(value):
    mydb = return_if_exist_database('datateam')
    cursor = mydb.cursor()
    cursor.execute(value)
    result = cursor.fetchall()
    print(f'Query result:') if len(result) else print('Query result empty')
    for x in result:
        print(x)
    mydb.commit()
    mydb.close()
    return result


def update_database(data, user):
    mydb = return_if_exist_database('datateam')
    cursor = mydb.cursor()
    item_id = data.get('index')
    if not item_id:
        return
    new_ans = data.get('ans')
    fail = data.get('fail')
    need_cut = data.get('need_cut')

    modifier_id = user.get('user_id')
    is_get_cutter = data.get('is_get_cutter')
    if is_get_cutter:
        value = [new_ans, fail, need_cut, modifier_id, modifier_id, item_id]
        query = (f"UPDATE data SET ans=%s, is_fail=%s, is_need_to_cut=%s, "
                 f"cutter_id=%s, modifier_id=%s, modified_time=NOW() where (id=%s)")
    else:
        value = [new_ans, fail, need_cut, modifier_id, item_id]
        query = (f"UPDATE data SET ans=%s, is_fail=%s, is_need_to_cut=%s, "
                 f"modifier_id=%s, modified_time=NOW() where (id=%s)")
    cursor.execute(query, value)
    mydb.commit()
    mydb.close()


def update_current_index(value):
    mydb = return_if_exist_database('datateam')
    cursor = mydb.cursor()
    query = f"UPDATE assignment SET last_data_id=%s where (id=%s)"
    cursor.execute(query, value)
    mydb.commit()
    mydb.close()


def update_table(type_q, table, value, update_values, addition_value=[], sql_instance=None):
    """table: tìm ở bảng nào\n
    type_q: 'index' | 'scp' -- value tương ứng trong update_values để cuối\n
    update_values: những thuộc tính muốn update\n
    addition_value: 1 vài thuộc tính muốn update thêm mà ko add value. Ex: ['modified_time=NOW()']"""
    mydb = sql_instance
    cursor = mydb.cursor(dictionary=True)
    if not isinstance(type_q, list):
        type_q = [type_q]
    if not isinstance(addition_value, list):
        addition_value = [addition_value]
    if len(value) != len(type_q) + len(update_values):
        raise AttributeError('len of list value is not match with type_q and update_values')
    type_q = ' and '.join([f'{item}=%s' for item in type_q])
    set_v = [f'{item}=%s' for item in update_values]
    set_v = set_v + addition_value
    set_v = ', '.join(set_v)
    # query = "UPDATE data SET status=%s, modifier_id=%s, modified_time=NOW() where (id=%s)"
    query = f"UPDATE {table} SET {set_v} WHERE {type_q}"
    cursor.execute(query, value)
    mydb.commit()


def update_table_many(type_q, table, value, update_values, addition_value=[], sql_instance=None):
    """table: tìm ở bảng nào\n
    type_q: 'index' | 'scp' -- value tương ứng trong update_values để cuối\n
    update_values: những thuộc tính muốn update\n
    addition_value: 1 vài thuộc tính muốn update thêm mà ko add value. Ex: ['modified_time=NOW()']"""
    if not sql_instance:
        print('Chưa kết nối database')
        return
    mydb = sql_instance
    cursor = mydb.cursor(dictionary=True)
    if not isinstance(type_q, list):
        type_q = [type_q]
    if not isinstance(addition_value, list):
        addition_value = [addition_value]
    if len(value[0]) != len(type_q) + len(update_values):
        raise AttributeError('len of list value is not match with type_q and update_values')
    type_q = ' and '.join([f'{item}=%s' for item in type_q])
    set_v = [f'{item}=%s' for item in update_values]
    set_v = set_v + addition_value
    set_v = ', '.join(set_v)
    query = f"UPDATE {table} SET {set_v} WHERE {type_q}"
    cursor.executemany(query, value)
    mydb.commit()


def get_user_info(user, task_id):
    mydb = return_if_exist_database('datateam')
    cursor = mydb.cursor(dictionary=True)
    value = [user]
    user_query = query_by('username', 'account', value, ['id', 'username', 'fullname'], is_unique=True)
    query = "SELECT * FROM `assignment` where user_id=%s and task_id=%s"
    cursor.execute(query, [user_query.get('id'), task_id])
    result = cursor.fetchall()
    print(f'Query result:') if len(result) else print('Query result empty')
    for x in result:
        print(x)
    mydb.close()
    return result


def valid_assignment(index, assignment_id, is_permit_only=False):
    assignment_q = query_by('id',
                            'assignment',
                            [assignment_id],
                            ['start_data_id', 'end_data_id', 'last_data_id'],
                            is_unique=True)
    if not len(assignment_q):
        return False
    last_data_id = assignment_q.get('last_data_id')
    start_data_id = assignment_q.get('start_data_id')
    end_data_id = assignment_q.get('end_data_id')
    if is_permit_only:
        if start_data_id <= index <= end_data_id:
            return True
        else:
            return False
    if index < 0 and last_data_id:
        return last_data_id
    elif index < 0 and not last_data_id:
        return start_data_id
    if start_data_id <= index <= end_data_id:
        return index
    if index < start_data_id:
        return start_data_id
    if index > end_data_id:
        return end_data_id


def finish_job(user):
    mydb = return_if_exist_database('datateam')
    cursor = mydb.cursor()
    query = f"UPDATE account SET is_finish_job=1 where (username=%s)"
    cursor.execute(query, [user])
    mydb.commit()
    mydb.close()


if __name__ == '__main__':
 #    a = [['1881'
 #  'đó cứ vừa đi hành quân vừa vừa đốt cho nên là khoảng bao nhiêu thời gian đấy thì cơm tám người xem xem cơm của anh nào là ngon thì cũng được nhất vào một tên vua đấy thế còn ngoài ra là còn vật vật cầu']
 # ['1897'
 #  'tháng tám thì dỗ bà dưới kia vào rằm tháng hai để các cụ ở dưới lại lên đây dự đỗ']
 # ['1954'
 #  'phía trước đây là cách đây độ khoảng tám cây số đường chim bay là thành phố nam định']
 # ['2411'
 #  'toàn hành động không à không phải ba tháng đâu ngài ngài làm thần y sao vậy tám tháng mười bốn ngày rồi của ngài mà ngài từ chối sao']
 # ['2422'
 #  'đầu mỡ trong máu à dạ không người ta là mỡ trong máu là người ta nghĩ gì mỡ nó ít còn máu nó nhiều còn em bây giờ là mỡ đến tám chục phần trăm rồi cho nên em bị mỡ trong mỡ']]
 #   update_table_many('id', 'data', self.search_list[:, ::-2].tolist(), ['ans'], sql_instance=eu.my_sql)
    pass