import psycopg2
from psycopg2 import sql
from . database_setup import conn,cur
from . graph import *



def Overall_tbl():
    query= "SELECT * FROM calculate_analysis;"
    cur.execute(query)
    data = cur.fetchall()
    return data
def high_data():
    query="""
    SELECT nameOfIssuer, sshPrnamt_nov, sshPrnamt_aug, differences
    FROM calculate_analysis 
    WHERE sshPrnamt_nov > sshPrnamt_aug;
    """
    cur.execute(query)
    data = cur.fetchall()
    query= """SELECT nameOfIssuer, sshPrnamt_nov, sshPrnamt_aug, differences
    FROM calculate_analysis 
    WHERE SUM(sshPrnamt_nov > sshPrnamt_aug);
    """
    return data
def low_data():
    query="""
    SELECT nameOfIssuer, sshPrnamt_nov, sshPrnamt_aug, differences
    FROM calculate_analysis 
    WHERE sshPrnamt_nov < sshPrnamt_aug ORDER BY sshPrnamt_nov ASC;
    """
    cur.execute(query)
    data = cur.fetchall()
    return data

def equal_data():
    query="""
    SELECT nameOfIssuer, sshPrnamt_nov, sshPrnamt_aug, differences
    FROM calculate_analysis 
    WHERE sshPrnamt_nov = sshPrnamt_aug;
    """
    cur.execute(query)
    data = cur.fetchall()
    return data

def new_data():
    query="""
    SELECT 
    t_nov.nameOfIssuer,
    t_nov.sshPrnamt
    FROM 
    transactions_nov_11 t_nov
    LEFT JOIN (
    SELECT nameOfIssuer
    FROM transactions_nov_11   
    EXCEPT   
    SELECT nameOfIssuer
    FROM transactions_aug_02
    ) except_result
    ON t_nov.nameOfIssuer = except_result.nameOfIssuer
    WHERE except_result.nameOfIssuer IS NOT NULL;
    """
    cur.execute(query)
    data = cur.fetchall()
    return data
    
def Overall():
    query="""SELECT 
    (SELECT SUM(sshPrnamt) FROM transactions_nov_11) AS total_sshPrnamt_nov,
    (SELECT SUM(sshPrnamt) FROM transactions_aug_02) AS total_sshPrnamt_aug;"""
    cur.execute(query)
    result=cur.fetchone()
    
    query = """SELECT SUM(sshPrnamt_nov) AS total_sum_nov
    FROM calculate_analysis
    WHERE sshPrnamt_nov > sshPrnamt_aug;
    """
    query= """SELECT SUM(sshPrnamt_aug) AS total_sum_aug
    FROM calculate_analysis
    WHERE sshPrnamt_nov > sshPrnamt_aug;"""
    cur.execute(query)
    high_val=cur.fetchone()
    query = """SELECT SUM(sshPrnamt_nov) AS total_sum_nov
    FROM calculate_analysis
    WHERE sshPrnamt_nov < sshPrnamt_aug;
    """
    cur.execute(query)
    low_val=cur.fetchone()
    
    query="""SELECT SUM(sshPrnamt_nov) AS total_sum_nov
    FROM calculate_analysis
    WHERE sshPrnamt_nov = sshPrnamt_aug;
    """
    cur.execute(query)
    equal_val = cur.fetchone()
    query="""SELECT SUM(sshPrnamt) AS total_sum
    FROM transactions_nov_11
    WHERE nameOfIssuer IN (
    SELECT nameOfIssuer
    FROM transactions_nov_11
    EXCEPT
    SELECT nameOfIssuer
    FROM transactions_aug_02
    );
    """
    cur.execute(query)
    new_val=cur.fetchone()
    
    return result[0],result[1],high_val,low_val, equal_val, new_val
def percentage(countOfcatagery):
    if countOfcatagery is None:
        return 0
    query="""SELECT SUM(sshPrnamt) FROM transactions_nov_11"""
    cur.execute(query)
    total_count=cur.fetchone()
    percent = countOfcatagery/total_count[0]*100
    if int(percent) == 0:
        return 1
    return int(percent)
 

def sumof(data):
    if len(data[0]) != 2 :
        total_november = sum(item[1] for item in data)
        total_august = sum(item[2] for item in data)
        return total_november, total_august
    else:
        total_november = sum(item[1] for item in data)
        return total_november

#fetching individual value by their nameOfIssuer
def data_by_name(name_Of_Issuer):
    query=f"""
        select nameOfIssuer,
        sshPrnamt_nov,
        sshPrnamt_aug,
        differences
        FROM calculate_analysis
        where nameOfIssuer='{name_Of_Issuer}';     
    """
    cur=conn.cursor()
    cur.execute(query, (name_Of_Issuer,))
    conn.commit()
    result=cur.fetchone()
    
    if result:
         return result
    else:
        print("Issuer not found.")
    cur.close()
    conn.close()


if __name__ == "__main__":
    merging_table()
    # x,y = Overall()
     #name = 'Overall'
     #print(x,y)
    # name_Of_Issuer='REVOLUTION MEDICINES INC'
    # name,x,y,dif = data_by_name(name_Of_Issuer)
    # nov,aug,high,low,equal,new = Overall()
    # print(high[0], low[0], equal[0], new[0])
    # show_line(name,x,y)
    # show_piechart(percentage(high[0]),percentage(low[0]),percentage(equal[0]),percentage(new[0]))
    # print(percentage(high[0]),percentage(low[0]),percentage(equal[0]),percentage(new[0]))
    data = high_data()
    print(sumof(data))