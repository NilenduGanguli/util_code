import oracledb
import os
import tempfile
import csv
from typing import List

'''
Expected Environment Variables : 
ORA_USER_NAME : username for oracle
ORA_PSSWD : password for oracle db ( only dev )
ORA_HOST_NAME : ip for oracle host
ORA_PORT : port for oracle db
ORA_SID : SID for oracle_db
ORA_SERVICE_NAME : Service Name for oracle db
'''

#ORACLEDB Performance Params
ORA_ARRAY_SIZE = 1000
ORA_PREFETCH = 1001
FETCHSIZE = 1000

#Defined Values USED
ORA_USER_NAME = "ORA_USER_NAME"
ORA_PSSWD = "ORA_PSSWD"
ORA_HOST_NAME = "ORA_HOST_NAME"
ORA_PORT = "ORA_PORT"
ORA_SID = "ORA_SID"
ORA_SERVICE_NAME = "ORA_SERVICE_NAME"
USE_SID = True

DOC_EXTN_S0_PUSH_PATH = "../resources/oracle/doc_extn_S0_push.sql"
KYC_DOCS_S0_PULL_PATH = "../resources/oracle/kyc_doc_S0_pull.sql"

ALLOWED_QUERIES = {
    "DOC_EXTN_S0_PUSH" : os.path.join(os.path.abspath(__file__),DOC_EXTN_S0_PUSH_PATH),
    "KYC_DOCS_S0_PULL" : os.path.join(os.path.abspath(__file__),KYC_DOCS_S0_PULL_PATH)
}

class RETURN_PUSH_STRUCT :
    def __init__ (self,status : bool ,failed_rows : dict):
        self.status = status
        self.failed_rows = failed_rows
    def __str__(self) -> str:
        return str(self.failed_rows)

class RETURN_PULL_STRUCT :
    def __init__ (self,status : bool ,csv_path : str,count : int):
        self.status = status
        self.csv_path = csv_path
        self.count = count
        self.result = []

#method to put list of rows into 
def push_rows(data_list : List[List], query_name : str) -> RETURN_PUSH_STRUCT:
    """
    data_list : list of tuples
    query_name : string
    """
    #initialvariable initialization
    push_skeletal_query = ""
    rows_to_push = 0
    #add data_list checker
    failed_rows = {}
    status = False

    #load env variables
    if ORA_USER_NAME in os.environ :
        ora_user_name = os.getenv(ORA_USER_NAME)
    else :
        raise Exception("ENV Var Not Set : " + ORA_USER_NAME)
    if ORA_PSSWD in os.environ :
        ora_psswd = os.getenv(ORA_PSSWD)
    else :
        raise Exception("ENV Var Not Set : " + ORA_PSSWD)
    if ORA_HOST_NAME in os.environ :
        ora_host_name = os.getenv(ORA_HOST_NAME)
    else :
        raise Exception("ENV Var Not Set : " + ORA_HOST_NAME)
    if ORA_PORT in os.environ :
        ora_port = os.getenv(ORA_PORT)
    else :
        raise Exception("ENV Var Not Set : " + ORA_PORT)
    if ORA_SID in os.environ :
        ora_sid = os.getenv(ORA_SID)
    elif ORA_SERVICE_NAME in os.environ :
        ora_service_name = os.getenv(ORA_SERVICE_NAME)
        USE_SID = False
    else :
        raise Exception("ENV Var Not Set : " + ORA_SID + "/" + ORA_SERVICE_NAME)
    
    #load query for table selected
    if query_name in ALLOWED_QUERIES :
        file_path = ALLOWED_QUERIES[query_name]
        with open(file_path, 'r') as infile:
            push_skeletal_query = infile.readline()
    else : 
        raise Exception(str(query_name) + "Query Name Not Allowed")
    if len(push_skeletal_query) == 0:
            raise Exception(str(query_name) + "Empty Query Loaded")

    #create connection to database
    #create dsn
    if USE_SID : 
        ora_dsn = oracledb.makedsn(ora_host_name, ora_port, sid=ora_sid)
    else :
        ora_dsn = oracledb.makedsn(ora_host_name, ora_port, service_name=ora_service_name)
    try :
        connection = oracledb.connect(user=ora_user_name, password=ora_psswd, dsn=ora_dsn)
    except :
        raise Exception("Error Establishing Connection/ Retrieving Cursor")

    #set strict check for data length
    #Yet to implement. also add data input checker
    # cursor.setinputsizes(None, 25)  # Adjust this according to your table's column definitions
    
    #push to database
    rows_to_push = len(data_list)
    try :
        connection.begin()
        cursor = connection.cursor()
        if rows_to_push>0 :
            cursor.executemany(push_skeletal_query, data_list,batcherrors=True)
        failures = cursor.getbatcherrors()

        #handle failure

        if len(failures)>0 :
            for error in cursor.getbatcherrors():
                failed_rows[error.offset] = error.message
            connection.rollback()
        else :
            status = True
            connection.commit()
    except :
        raise Exception("Error Connecting/Writing to Database : " + str(ora_dsn))
    
    #return status and failued rows
    connection.close()
    return RETURN_PUSH_STRUCT(status=status,failed_rows=failed_rows)

#function to execute query and fetch list of tuples from oracle db
def pull_rows(query_name : str, save_data : bool = False) -> RETURN_PULL_STRUCT :
    """
    query_name : string
    """
    #initialvariable initialization
    pull_query = ""
    #add data_list checker
    row_count = 0
    return_struct = RETURN_PULL_STRUCT(status=False)

    #load env variables
    if ORA_USER_NAME in os.environ :
        ora_user_name = os.getenv(ORA_USER_NAME)
    else :
        raise Exception("ENV Var Not Set : " + ORA_USER_NAME)
    if ORA_PSSWD in os.environ :
        ora_psswd = os.getenv(ORA_PSSWD)
    else :
        raise Exception("ENV Var Not Set : " + ORA_PSSWD)
    if ORA_HOST_NAME in os.environ :
        ora_host_name = os.getenv(ORA_HOST_NAME)
    else :
        raise Exception("ENV Var Not Set : " + ORA_HOST_NAME)
    if ORA_PORT in os.environ :
        ora_port = os.getenv(ORA_PORT)
    else :
        raise Exception("ENV Var Not Set : " + ORA_PORT)
    if ORA_SID in os.environ :
        ora_sid = os.getenv(ORA_SID)
    elif ORA_SERVICE_NAME in os.environ :
        ora_service_name = os.getenv(ORA_SERVICE_NAME)
        USE_SID = False
    else :
        raise Exception("ENV Var Not Set : " + ORA_SID + "/" + ORA_SERVICE_NAME)
    
    #load query for table selected
    if query_name in ALLOWED_QUERIES :
        file_path = ALLOWED_QUERIES[query_name]
        with open(file_path, 'r') as infile:
            pull_query = infile.readline()
    else : 
        raise Exception(str(query_name) + "Query Name Not Allowed")
    if len(pull_query) == 0:
            raise Exception(str(query_name) + "Empty Query Loaded")

    #create connection to database
    #create dsn
    if USE_SID : 
        ora_dsn = oracledb.makedsn(ora_host_name, ora_port, sid=ora_sid)
    else :
        ora_dsn = oracledb.makedsn(ora_host_name, ora_port, service_name=ora_service_name)
    try :
        connection = oracledb.connect(user=ora_user_name, password=ora_psswd, dsn=ora_dsn)
    except :
        raise Exception("Error Establishing Connection/ Retrieving Cursor")\

    #pull from database
    try :
        connection.begin()
        cursor = connection.cursor()

        #executing query on database
        cursor.execute(pull_query)

        #performance tuning
        cursor.prefetchrows = ORA_PREFETCH
        cursor.arraysize = ORA_ARRAY_SIZE
        fetch_size = FETCHSIZE

        #fetch and save all rows to tempfile
        if save_data :
            #creating tempfile
            temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='')
            csv_file_path = temp_file.name
            temp_file.close()

            #start batch fetch
            while True :
                rows = cursor.fetchmany(size=fetch_size)
                row_count+=len(rows)
                if not rows:
                    break
                with open(csv_file_path, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerows(rows)
            return_struct.status = True
            return_struct.csv_path = csv_file_path
            return_struct.count = row_count
        else:
            rows = cursor.fetchall()
            return_struct.status = True
            return_struct.result = rows
    except :
        raise Exception("Error fetching data from Oracle : "+ str(ora_dsn))
    
    #cleanup and return
    connection.close()
    return return_struct





    
    
