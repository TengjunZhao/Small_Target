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
    'budget_id': 'budget_category',
    'db_expend_wechat': 'expend_wechat',
    'db_expend_alipay': 'expend_alipay',
    'db_expend': 'expend_merged'
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
        'in_out': 'in_out',
        'price': 'price',
        'exchange': 'exchange',
        'status': 'status',
        'tenant_id': 'tenant_id',
        'remark': 'remark',
        'budget_id': None,  # 暂为空（可根据业务关联补充）
        'user_id': 1,  # 补充默认值（根据实际业务调整）
        'family_id': 1  # 补充默认值（根据实际业务调整）
    },
    'expend_alipay': {
        'transaction_id': 'transaction_id',
        'in_out': 'in_out',
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
        'family_id': 1  # 补充默认值（根据实际业务调整）
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

}

# 冲突字段配置（key: PG表名, value: 主键/唯一键字段名）
CONFLICT_FIELDS = {
    'budget_category': 'id',
    'expend_wechat': 'transaction_id',
    'expend_alipay': 'transaction_id',
    'expend_merged': None  # 无冲突字段/暂不处理
}


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
        extras.execute_batch(pg_cursor, insert_sql, rows, page_size=1000)
        pg_conn.commit()

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