import sqlite3
import xml.etree.ElementTree as ET

a = ['50000', '100000', '150000', '200000', '250000', '300000', '350000', '400000', '450000', '500000', '550000', '600000', '650000', '700000', '750000', '800000', '850000', '900000', '950000', '1000000', '1050000', '1100000', '1146461']

for i in a:
    # XML 파일 경로
    print(i + ' 시작')
    xml_file = i + '.xml'

    # XML 파일 로드
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # SQLite 데이터베이스 연결 및 테이블 생성
    conn = sqlite3.connect(i + '.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_code INTEGER,
            group_code INTEGER,
            group_order INTEGER,
            link TEXT,
            word TEXT,
            word_unit TEXT,
            word_type TEXT,
            sense_no TEXT,
            pos TEXT,
            type TEXT,
            definition TEXT,
            definition_original TEXT,
            region TEXT
        )
    ''')

    # XML 데이터를 SQLite 데이터베이스로 변환
    for item in root.findall('item'):
        target_code = item.find('target_code').text if item.find('target_code') is not None else None
        group_code = item.find('group_code').text if item.find('group_code') is not None else None
        group_order = item.find('group_order').text if item.find('group_order') is not None else None
        link = item.find('link').text if item.find('link') is not None else None
        
        word = item.find('wordInfo/word').text if item.find('wordInfo/word') is not None else None
        word_unit = item.find('wordInfo/word_unit').text if item.find('wordInfo/word_unit') is not None else None
        word_type = item.find('wordInfo/word_type').text if item.find('wordInfo/word_type') is not None else None
        
        sense_no = item.find('senseInfo/sense_no').text if item.find('senseInfo/sense_no') is not None else None
        pos = item.find('senseInfo/pos').text if item.find('senseInfo/pos') is not None else None
        type_ = item.find('senseInfo/type').text if item.find('senseInfo/type') is not None else None
        definition = item.find('senseInfo/definition').text if item.find('senseInfo/definition') is not None else None
        definition_original = item.find('senseInfo/definition_original').text if item.find('senseInfo/definition_original') is not None else None
        region = item.find('senseInfo/region_info/region').text if item.find('senseInfo/region_info/region') is not None else None
        
        cursor.execute('''
            INSERT INTO item (
                target_code, group_code, group_order, link, word, word_unit, word_type,
                sense_no, pos, type, definition, definition_original, region
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (target_code, group_code, group_order, link, word, word_unit, word_type,
            sense_no, pos, type_, definition, definition_original, region))

    # 변경 사항 커밋 및 연결 종료
    conn.commit()
    conn.close()
    print(i + " 완료")
