import os
import pymysql
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv

# 加载环境变量（避免硬编码密码）
load_dotenv()

# ---------------------- 配置数据库连接信息 ----------------------
# MySQL 本地配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'remoteuser',
    'password': 'password',
    'database': 'personal',
    'charset': 'utf8mb4'
}

# PostgreSQL 服务器配置
PG_CONFIG = {
    # 'host': '43.137.41.36',
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'password',
    'database': 'smalltarget'
}

# ---------------------- 表映射 + 字段映射 + 冲突字段配置 ----------------------
# 表映射（key: MySQL表名, value: PostgreSQL表名）
TABLE_MAPPING = {
    # 'budget_id': 'budget_category',
    # 'db_expend_wechat': 'expend_wechat',
    # 'db_expend_alipay': 'expend_alipay',
    # 'db_expend': 'expend_merged',
    'db_income': 'income',
}

# 字段映射（key: PG表名, value: {PG字段: MySQL字段/默认值}）
FIELD_MAPPING = {
    'budget_category': {
        'id': 'budget_id',  # PG.id 对应 MySQL.budget_id
        'main_category': 'main',  # PG.main_category 对应 MySQL.main
        'sub_category': 'child',  # PG.sub_category 对应 MySQL.child
        'is_fixed': False,  # 补充默认值
        'family_id': 1  # 补充默认值（根据实际业务调整）
    },
    'expend_wechat': {
        'transaction_id': 'transaction_id',
        'trade_time': 'trade_time',
        'trade_category': 'trade_catgry',  # PG.trade_category 对应 MySQL.trade_catgry
        'commodity': 'commodity',
        'person': 'person',
        'in_out': 'in_out',
        'price': 'price',
        'exchange': 'exchange',
        'status': 'status',
        'tenant_id': 'tenant_id',
        'remark': 'remark',
        'budget_id': None,  # 暂为空（可根据业务关联补充）
        'user_id': 1,  # 补充默认值（根据实际业务调整）
        'family_id': 1,  # 补充默认值（根据实际业务调整）
        'belonging': 'belonging',
    },
    'expend_alipay': {
        'transaction_id': 'transaction_id',
        'in_out': 'in_out',
        'person': 'person',
        'person_account': 'person_account',
        'commodity': 'commodity',
        'exchange': 'exchange',
        'price': 'price',
        'status': 'status',
        'trade_category': 'trade_catgry',  # PG.trade_category 对应 MySQL.trade_catgry
        'tenant_id': 'tenant_id',
        'trade_time': 'trade_time',
        'remark': 'remark',
        'budget_id': None,  # 暂为空（可根据业务关联补充）
        'user_id': 1,  # 补充默认值（根据实际业务调整）
        'family_id': 1,  # 补充默认值（根据实际业务调整）
        'belonging': 'belonging',
    },
    'expend_merged': {
        'transaction_id': 'transaction_id',  # 主键，严格对应
        'expend_channel': 'expend_catgry',
        'budget_id': 'budget_catgry',          # MySQL person → PG person_account
        'commodity': 'commodity',
        'in_out': 'in_out',                    # MySQL无此字段
        'person': 'person',  # decimal(10,2) → numeric
        'price': 'price',
        'status': 'status',   # MySQL expend_catgry → PG trade_category
        'trade_time': 'trade_time',                   # MySQL无此字段
        'belonging': 'belonging',  # 适配时区
        'family_id': 1,                      # MySQL无此字段
        'user_id': 1,  # 兼容非数字值
    },
    'income': {
        'payday': 'payday',
        'amount': 'salary',
        'insurance': 'insurance',
        'adjustment': 'adjustment',
        'income': 'income',
        'income_type_id':'1001',
        'create_time':None,
        'family_id':'1',
        'relate_asset_id':None,
        'user_id': '1'
    }

}

# 冲突字段配置（key: PG表名, value: 主键/唯一键字段名）
CONFLICT_FIELDS = {
    'budget_category': 'id',
    'expend_wechat': 'transaction_id',
    'expend_alipay': 'transaction_id',
    'expend_merged': 'transaction_id'  # 添加冲突处理
}


# ---------------------- 辅助函数 ----------------------
def clean_mysql_duplicates(mysql_conn, table_name, key_column):
    """清理 MySQL 表中的重复数据，保留最小ID的记录"""
    cursor = mysql_conn.cursor()
    try:
        # 查找重复的记录
        check_sql = f"""
            SELECT {key_column}, COUNT(*) as cnt 
            FROM {table_name} 
            GROUP BY {key_column} 
            HAVING COUNT(*) > 1
        """
        cursor.execute(check_sql)
        duplicates = cursor.fetchall()
        
        if duplicates:
            print(f"发现 {len(duplicates)} 组重复的 {key_column} 数据")
            
            # 删除重复项，保留最小ID的记录
            delete_sql = f"""
                DELETE t1 FROM {table_name} t1
                INNER JOIN {table_name} t2
                WHERE t1.{key_column} = t2.{key_column}
                AND t1.id > t2.id
            """
            cursor.execute(delete_sql)
            mysql_conn.commit()
            print(f"已清理 {cursor.rowcount} 条重复记录")
        else:
            print(f"表 {table_name} 中无重复数据")
            
    except Exception as e:
        print(f"清理重复数据失败: {str(e)}")
        mysql_conn.rollback()
    finally:
        cursor.close()


def check_pg_duplicates(pg_conn, table_name, key_column):
    """检查 PostgreSQL 表中是否存在重复数据"""
    cursor = pg_conn.cursor()
    try:
        check_sql = f"""
            SELECT {key_column}, COUNT(*) as cnt 
            FROM {table_name} 
            GROUP BY {key_column} 
            HAVING COUNT(*) > 1
            LIMIT 10
        """
        cursor.execute(check_sql)
        duplicates = cursor.fetchall()
        
        if duplicates:
            print(f"警告: PostgreSQL 表 {table_name} 中发现重复数据:")
            for dup in duplicates:
                print(f"  {key_column} = {dup[0]}, 出现次数: {dup[1]}")
            return True
        return False
    except Exception as e:
        print(f"检查重复数据失败: {str(e)}")
        return False
    finally:
        cursor.close()


# ---------------------- 核心同步函数 ----------------------
def sync_table(mysql_conn, pg_conn, mysql_table, pg_table):
    """同步单张表的数据（支持字段映射+按表适配冲突字段）"""
    try:
        # 1. 读取 MySQL 数据
        mysql_cursor = mysql_conn.cursor(pymysql.cursors.DictCursor)
        mysql_cursor.execute(f"SELECT * FROM {mysql_table}")
        data = mysql_cursor.fetchall()
        if not data:
            print(f"【{mysql_table}】无数据，跳过同步")
            return

        # 2. 获取当前表的字段映射规则和冲突字段
        field_map = FIELD_MAPPING.get(pg_table, {})
        conflict_field = CONFLICT_FIELDS.get(pg_table)

        if not field_map:
            print(f"【{mysql_table} → {pg_table}】无字段映射规则，跳过同步")
            return

        # 3. 构建 PG 字段列表和数据值
        pg_columns = []
        pg_values = []

        for pg_col, mysql_col_or_default in field_map.items():
            pg_columns.append(pg_col)
            # 提取每条数据的对应值（优先取MySQL字段值，无则用默认值）
            col_values = []
            for row in data:
                if mysql_col_or_default is None:
                    # 空值
                    col_values.append(None)
                elif mysql_col_or_default in row:
                    # 取MySQL字段值
                    col_values.append(row[mysql_col_or_default])
                else:
                    # 用默认值
                    col_values.append(mysql_col_or_default)
            pg_values.append(col_values)

        # 转置：从按字段分组 → 按行分组（适配批量插入）
        rows = list(zip(*pg_values))

        # 4. 构建 PG 插入语句（适配不同表的冲突字段）
        columns_str = ', '.join(pg_columns)
        placeholders = ', '.join(['%s'] * len(pg_columns))

        if conflict_field:
            # 有冲突字段：按指定字段做冲突处理
            insert_sql = f"""
                INSERT INTO {pg_table} ({columns_str}) 
                VALUES ({placeholders}) 
                ON CONFLICT ({conflict_field}) DO NOTHING
            """
        else:
            # 无冲突字段：不做冲突处理（或根据需求调整）
            insert_sql = f"""
                INSERT INTO {pg_table} ({columns_str}) 
                VALUES ({placeholders})
            """

        # 5. 批量插入 PostgreSQL
        pg_cursor = pg_conn.cursor()
        try:
            extras.execute_batch(pg_cursor, insert_sql, rows, page_size=1000)
            pg_conn.commit()
        except psycopg2.errors.UniqueViolation as e:
            # 处理重复键冲突
            pg_conn.rollback()
            print(f"检测到重复键冲突，正在处理...")
            
            # 方法1: 先删除重复数据再插入
            if conflict_field:
                # 获取所有 transaction_id
                transaction_ids = [row[pg_columns.index(conflict_field)] for row in rows if row[pg_columns.index(conflict_field)] is not None]
                if transaction_ids:
                    # 删除已存在的记录
                    delete_sql = f"DELETE FROM {pg_table} WHERE {conflict_field} = ANY(%s)"
                    pg_cursor.execute(delete_sql, (transaction_ids,))
                    pg_conn.commit()
                    print(f"已删除 {pg_cursor.rowcount} 条重复记录")
                    
                    # 重新插入
                    extras.execute_batch(pg_cursor, insert_sql, rows, page_size=1000)
                    pg_conn.commit()
                    print(f"重新插入 {len(rows)} 条记录成功")
            else:
                raise e  # 如果没有冲突字段配置，重新抛出异常

        print(f"【{mysql_table} → {pg_table}】同步成功，共 {len(data)} 条数据")

    except Exception as e:
        pg_conn.rollback()
        print(f"【{mysql_table} → {pg_table}】同步失败：{str(e)}")
        raise e  # 可选：抛出异常便于调试
    finally:
        if 'mysql_cursor' in locals():
            mysql_cursor.close()
        if 'pg_cursor' in locals():
            pg_cursor.close()


# ---------------------- 主函数 ----------------------
def main():
    # 连接 MySQL
    try:
        mysql_conn = pymysql.connect(**MYSQL_CONFIG)
        print("MySQL 连接成功")
    except Exception as e:
        print(f"MySQL 连接失败：{str(e)}")
        return

    # 连接 PostgreSQL
    try:
        pg_conn = psycopg2.connect(**PG_CONFIG)
        print("PostgreSQL 连接成功")
    except Exception as e:
        print(f"PostgreSQL 连接失败：{str(e)}")
        mysql_conn.close()
        return

    # 数据预处理阶段
    print("\n=== 数据预处理阶段 ===")
    
    # 清理 MySQL 重复数据
    for mysql_table, pg_table in TABLE_MAPPING.items():
        if pg_table in ['expend_wechat', 'expend_alipay', 'expend_merged']:
            clean_mysql_duplicates(mysql_conn, mysql_table, 'transaction_id')
    
    # 检查 PostgreSQL 重复数据
    for mysql_table, pg_table in TABLE_MAPPING.items():
        conflict_field = CONFLICT_FIELDS.get(pg_table)
        if conflict_field and pg_table in ['expend_wechat', 'expend_alipay', 'expend_merged']:
            check_pg_duplicates(pg_conn, pg_table, conflict_field)
    
    print("\n=== 开始数据同步 ===")
    
    # 遍历表映射，逐个同步
    for mysql_table, pg_table in TABLE_MAPPING.items():
        # 跳过无字段映射的表（如 expend_merged）
        if pg_table not in FIELD_MAPPING:
            print(f"【{mysql_table} → {pg_table}】无字段映射，跳过")
            continue
        sync_table(mysql_conn, pg_conn, mysql_table, pg_table)

    # 关闭连接
    mysql_conn.close()
    pg_conn.close()
    print("所有表同步完成")


if __name__ == "__main__":
    main()