import sqlite3

# 병합할 새로운 데이터베이스 생성
new_db = sqlite3.connect('merged.db')
new_cursor = new_db.cursor()

# 병합할 데이터베이스 파일 목록
db_files = ['50000.db', '100000.db', '150000.db', '200000.db', '250000.db', '300000.db', '350000.db', '400000.db', '450000.db', '500000.db', '550000.db', '600000.db', '650000.db', '700000.db', '750000.db', '800000.db', '850000.db', '900000.db', '950000.db', '1000000.db', '1050000.db', '1100000.db', '1146461.db']


for db_file in db_files:
    print(f"Processing database: {db_file}")
    old_db = sqlite3.connect(db_file)
    old_cursor = old_db.cursor()
    
    # 기존 데이터베이스의 테이블 목록 가져오기
    old_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = old_cursor.fetchall()
    
    for table_name in tables:
        table_name = table_name[0]
        
        if table_name == 'sqlite_sequence':
            # sqlite_sequence 테이블은 건너뜁니다
            continue
        
        print(f"  Processing table: {table_name}")
        
        # 테이블 스키마 가져오기
        old_cursor.execute(f"PRAGMA table_info({table_name});")
        schema = old_cursor.fetchall()
        column_names = [col[1] for col in schema]
        
        # 새로운 데이터베이스에 테이블 생성 (존재하지 않을 경우)
        columns = ", ".join([f"{col[1]} {col[2]}" for col in schema])
        new_cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});")
        
        # 기존 데이터 가져오기
        old_cursor.execute(f"SELECT * FROM {table_name};")
        rows = old_cursor.fetchall()
        
        # 새로운 데이터베이스에 데이터 삽입
        placeholders = ", ".join(["?" for _ in column_names])
        new_cursor.executemany(f"INSERT INTO {table_name} VALUES ({placeholders});", rows)
        
        print(f"    Inserted {len(rows)} rows into {table_name}")
        
    old_db.close()

new_db.commit()
new_db.close()
print("Database merging complete.")
