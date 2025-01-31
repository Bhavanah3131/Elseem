import pandas as pd
import psycopg2
from psycopg2 import sql
from datetime import datetime
from . database_setup import conn,cur
import os
from . browse_files import *



# Insert data into  tables
def insert_data(df, transactions_nov_11):
    for index, row in df.iterrows():
        cur.execute(sql.SQL('''
        INSERT INTO {} (nameOfIssuer, titleOfClass, cusip, value, sshPrnamt, sshPrnamtType, 
        investmentDiscretion)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING;
        ''').format(sql.Identifier(transactions_nov_11)), 
        (row['ns1:nameOfIssuer'], row['ns1:titleOfClass'], row['ns1:cusip'], row['ns1:value'], row['ns1:sshPrnamt'], 
          row['ns1:sshPrnamtType'], row['ns1:investmentDiscretion']))
        conn.commit()
def trunc():
    cur.execute("TRUNCATE TABLE  transactions_nov_11")
    cur.execute("TRUNCATE TABLE transactions_aug_02")
    cur.execute("TRUNCATE TABLE calculate_analysis")       
    conn.commit()

#merging the two tables and also taking out the differences of sshPrnamt in one table
def merging_table():
    insert_into_calculate_analysis="""INSERT INTO calculate_analysis(nameOfIssuer, 
    sshPrnamt_nov, sshPrnamt_aug, 
    differences)
    WITH trans_11_agg AS (    
    SELECT nameofissuer, SUM(sshPrnamt) AS total_shares
    FROM transactions_nov_11
    GROUP BY nameofissuer
    ),
    trans_02_agg AS (SELECT nameOfIssuer, SUM(sshPrnamt) AS total_shares FROM transactions_aug_02 GROUP BY nameOfIssuer )          
    SELECT 
    COALESCE(t11.nameOfIssuer, t02.nameOfIssuer) AS nameOfIssuer,
    t11.total_shares AS total_shares_transactions_nov_11, 
    t02.total_shares AS total_shares_transactions_aug_02,
    (COALESCE(t11.total_shares, 0) - COALESCE(t02.total_shares, 0)) AS differences                    
    FROM                                                               
    trans_11_agg t11                                                         
    FULL JOIN                                                
    trans_02_agg t02                             
    ON                                                                      
    t11.nameofissuer = t02.nameofissuer;
    """
    cur.execute(insert_into_calculate_analysis)
    conn.commit()

    # print("join operation successfully inserted") 

def insert_files(file1,file2):
    #load the excel file
    file_path_1 = file1
    file_path_2 = file2

    # Load data from Alphabet 13F files
    data_1 = pd.read_excel(file_path_1)
    data_2 = pd.read_excel(file_path_2)
    # print(data_1.info())
    trunc()
    insert_data(data_1, 'transactions_nov_11')
    insert_data(data_2, 'transactions_aug_02')
    merging_table()


# conn.close()
# cur.close()
# print("Data inserted successfully!")
if __name__ == '__main__':
    insert_files('C:/Users/Toshiba/OneDrive/Desktop/companies/alpha/Alphabet_08.xlsx','C:/Users/Toshiba/OneDrive/Desktop/companies/alpha/Alphabet_11.xlsx')