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
    'host': '43.137.41.36',
    # 'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'password',
    'database': 'smalltarget'
}

# PostgreSQL 本地配置（用于服务器到本地的同步）
LOCAL_PG_CONFIG = {
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
    'db_expend_wechat': 'expend_wechat',
    'db_expend_alipay': 'expend_alipay',
    'db_expend': 'expend_merged',
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
                ON CONFLICT ({conflict_field}) DO UPDATE SET
                 {', '.join([f"{col} = EXCLUDED.{col}" for col in columns_str.split(', ') if col != conflict_field])}
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


# ---------------------- 服务器到本地同步函数 ----------------------
def sync_server_to_local():
    """从服务器PostgreSQL向本地PostgreSQL同步数据"""
    print("\n=== 开始服务器到本地数据同步 ===")
    
    # 连接服务器PostgreSQL
    try:
        server_pg_conn = psycopg2.connect(**PG_CONFIG)
        print("服务器PostgreSQL连接成功")
    except Exception as e:
        print(f"服务器PostgreSQL连接失败：{str(e)}")
        return
    
    # 连接本地PostgreSQL
    try:
        local_pg_conn = psycopg2.connect(**LOCAL_PG_CONFIG)
        print("本地PostgreSQL连接成功")
    except Exception as e:
        print(f"本地PostgreSQL连接失败：{str(e)}")
        server_pg_conn.close()
        return
    
    # 定义需要同步的表（可以根据需要调整）
    tables_to_sync = [
        'expend_wechat',
        'expend_alipay',
        'expend_merged',
        'income',
    ]
    
    # 同步每个表
    for table_name in tables_to_sync:
        try:
            sync_pg_table(server_pg_conn, local_pg_conn, table_name)
        except Exception as e:
            print(f"表 {table_name} 同步失败: {str(e)}")
            continue
    
    # 关闭连接
    server_pg_conn.close()
    local_pg_conn.close()
    print("服务器到本地同步完成")


def sync_pg_table(source_conn, target_conn, table_name):
    """同步PostgreSQL表数据（从源到目标）"""
    try:
        # 1. 从源表读取数据
        source_cursor = source_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        source_cursor.execute(f"SELECT * FROM {table_name}")
        data = source_cursor.fetchall()
        
        if not data:
            print(f"【{table_name}】无数据，跳过同步")
            return
        
        print(f"【{table_name}】从源表读取到 {len(data)} 条记录")
        
        # 2. 获取表结构信息
        source_cursor.execute(f"SELECT column_name, data_type "
                              f"FROM information_schema.columns "
                              f"WHERE table_name = '{table_name}' "
                              f"ORDER BY ordinal_position")
        columns_info = source_cursor.fetchall()
        column_names = [col['column_name'] for col in columns_info]
        
        # 3. 清空目标表数据（可选，根据需求决定是否清空）
        target_cursor = target_conn.cursor()
        # target_cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE")
        # target_conn.commit()
        # print(f"已清空目标表 {table_name}")
        
        # 4. 构建插入语句
        columns_str = ', '.join(column_names)
        placeholders = ', '.join(['%s'] * len(column_names))
        insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
        
        # 5. 准备数据
        rows = []
        for row in data:
            row_values = [row[col] for col in column_names]
            rows.append(row_values)
        
        # 6. 批量插入
        try:
            extras.execute_batch(target_cursor, insert_sql, rows, page_size=1000)
            target_conn.commit()
            print(f"【{table_name}】成功同步 {len(rows)} 条记录到本地")
        except psycopg2.errors.UniqueViolation as e:
            # 处理主键冲突
            target_conn.rollback()
            print(f"检测到主键冲突，正在处理...")
            
            # 获取主键字段
            source_cursor.execute(f"SELECT ccu.column_name FROM information_schema.table_constraints tc "
                                    f"JOIN information_schema.constraint_column_usage ccu "
                                    f"ON tc.constraint_name = ccu.constraint_name "
                                    f"WHERE tc.table_name = '{table_name}' "
                                    f"AND tc.constraint_type = 'PRIMARY KEY'")
            pk_result = source_cursor.fetchone()
            pk_column = pk_result['column_name'] if pk_result else None
            
            if pk_column:
                # 删除冲突数据后重新插入
                pk_values = [row[pk_column] for row in data if row[pk_column] is not None]
                if pk_values:
                    delete_sql = f"DELETE FROM {table_name} WHERE {pk_column} = ANY(%s)"
                    target_cursor.execute(delete_sql, (pk_values,))
                    target_conn.commit()
                    print(f"已删除 {target_cursor.rowcount} 条冲突记录")
                    
                    # 重新插入
                    extras.execute_batch(target_cursor, insert_sql, rows, page_size=1000)
                    target_conn.commit()
                    print(f"重新插入 {len(rows)} 条记录成功")
            else:
                raise e
        
    except Exception as e:
        target_conn.rollback()
        print(f"【{table_name}】同步失败：{str(e)}")
        raise
    finally:
        if 'source_cursor' in locals():
            source_cursor.close()
        if 'target_cursor' in locals():
            target_cursor.close()


# ---------------------- 主函数 ----------------------
def main():
    """主函数 - 支持多种同步模式"""
    import sys
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == 'server-to-local':
            sync_server_to_local()
            return
        elif mode == 'mysql-to-pg':
            # 继续执行原有的MySQL到PostgreSQL同步
            pass
        else:
            print("用法: python database_transfer.py [mode]")
            print("模式: mysql-to-pg (默认) | server-to-local")
            return
    
    # 原有的MySQL到PostgreSQL同步逻辑
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


# ---------------------- 使用说明 ----------------------
"""
使用方法：

1. MySQL到PostgreSQL同步（默认模式）：
   python database_transfer.py
   或
   python database_transfer.py mysql-to-pg

2. 服务器PostgreSQL到本地PostgreSQL同步：
   python database_transfer.py server-to-local

注意事项：
- 请根据实际情况修改数据库连接配置
- 建议在生产环境中备份数据后再执行同步
- 同步过程中会自动处理主键冲突
- 可以根据需要调整需要同步的表列表
"""