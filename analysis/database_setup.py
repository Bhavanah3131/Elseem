import psycopg2

# Database connection parameters
DB_USERNAME = 'postgres'
DB_PASSWORD = 'Elseem@123'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'stock_analysis'

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# Create transactions table
cur.execute('''
    CREATE TABLE IF NOT EXISTS transactions_nov_11 (
        id SERIAL,
        nameOfIssuer VARCHAR(100) NOT NULL,
        titleOfClass VARCHAR(100),
        cusip VARCHAR(100) NOT NULL,
        value FLOAT,
        sshPrnamt FLOAT,
        sshPrnamtType VARCHAR(10),
        investmentDiscretion VARCHAR(50))   
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS transactions_aug_02 (
        id SERIAL,
        nameOfIssuer VARCHAR(100) NOT NULL,
        titleOfClass VARCHAR(100),
        cusip VARCHAR(100) NOT NULL,
        value FLOAT,
        sshPrnamt FLOAT,
        sshPrnamtType VARCHAR(10),
        investmentDiscretion VARCHAR(50))
''')

cur.execute('''
        CREATE TABLE IF NOT EXISTS calculate_analysis(
            nameOfIssuer VARCHAR(300) NOT NULL, 
            sshPrnamt_nov FLOAT,
            sshPrnamt_aug FLOAT,
            differences FLOAT)    
            ''')
conn.commit()

conn.commit()
if __name__ == '__main__':
    cur.close()
    conn.close()

    print("Tables created successfully!")
