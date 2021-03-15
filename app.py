import os
import json
import socket
import time

from flask_restplus import reqparse, Api, Resource, fields
from flask import Flask, Response, request
from flask_cors import CORS

import pandas as pd
import numpy as np
import sqlite3

from ast import literal_eval
import csv


app = Flask(__name__, static_url_path='/static/')
app.config ['CORS_HEADERS'] ='Content-Type'
Cors = CORS(app)

api = Api(app)


db_name=r"report.db"


print(" api started Successfully")

#----------------------------------------------------------

@app.route('/departments',methods = ['GET'])
def get_departments():
    try :
        return_status =None
        result =None
        sql_name ="""select distinct department_name from reports """
        con = sqlite3.connect(db_name)
        #df=pd.read_sql_query(sql_name, con)
        cursorObj = con.cursor()
        departments=[department_name[0]  for department_name in cursorObj.execute(sql_name).fetchall() ]
        cursorObj.close()
        con.close()
        #result= json.loads(df.to_json(orient="records"))  
        result= {"departments":departments}
        return_status=200
    except  :
        result ={}
        print('Exception while uploading the file  ')
        return_status = 500
        result['status'] =0
        result['message'] = 'Internal Error while reading Department data'
        raise 
    finally:
        resp = Response(json.dumps(result) ,status = return_status, mimetype ="application/json")
    return resp

@app.route('/reports',methods = ['GET'])
def get_reports():
    try :
        return_status =None
        result =None
        sql_name ="""select * from reports """
        con = sqlite3.connect(db_name)
        df=pd.read_sql_query(sql_name, con)
        in_department_name=request.args.get("department")
        #df["report_url"]=df["report_url"].str.replace("\\","")
        con.close()
        df=df[df.department_name==in_department_name]
        result= json.loads(df.to_json(orient="records"))
      
        return_status=200
    except  :
        result ={}
        print('Exception while uploading the file  ')
        return_status = 500
        result['status'] =0
        result['message'] = 'Internal Error has Occurred while processing Report Request'
    finally:
        resp = Response(json.dumps(result) ,status = return_status, mimetype ="application/json")
    return resp

@app.route('/addreports',methods = ['POST'])
def addreports():
    try :
        return_status =None
        result =None
        con = sqlite3.connect(db_name)
        cursorObj = con.cursor()
        sql_name="""INSERT INTO reports(id, department_name, report_name, report_url) VALUES(?, ?, ?, ?)"""
        
        records=request.json
        for row in  records.get('reports'):
            id=cursorObj.execute("""select max(id) from reports""").fetchone()[0]
            rec=(id+1,records["department_name"],row["report_name"],row["report_url"])
            print(rec)
            cursorObj.execute(sql_name, rec)
        '''
        for rec in  records:
           id+=1
           rec=(id,rec["department_name"],rec["report_name"],rec["report_url"])
           cursorObj.execute(sql_name, rec)
        '''
        con.commit()
        cursorObj.close()
        con.close()
        result= {"status":f"{len(records.get('reports'))} report added successfully"}
        return_status=200
    except  :
        result ={}
        print('Exception while uploading the file  ')
        return_status = 500
        result['status'] =0
        result['message'] = 'Internal Error has Occurred while processing the add request'
        raise
    finally:
        resp = Response(json.dumps(result) ,status = return_status, mimetype ="application/json")
    return resp
  
@app.route('/deletereports',methods = ['POST'])
def deletereports():
    try :
        return_status =None
        result =None
        con = sqlite3.connect(db_name)
        cursorObj = con.cursor()
        report_ids=request.json["ids"]
        sql_name="""delete from  reports where id = ?"""     
        for id in report_ids:
            print('--')
            print(id)
            cursorObj.execute(sql_name,(id,))
        con.commit()
        cursorObj.close()
        con.close()
        result= {"status":"reports deleted successfully"}
        return_status=200
    except  :
        result ={}
        print('Exception while uploading the file  ')
        return_status = 500
        result['status'] =0
        result['message'] = 'Internal Error has Occurred while processing the delete request'
        raise
    finally:
        resp = Response(json.dumps(result) ,status = return_status, mimetype ="application/json")
    return resp
    

@app.route('/updatereports',methods = ['POST'])
def updatereports():
    try :
        return_status =None
        result =None
        con = sqlite3.connect(db_name)
        cursorObj = con.cursor()
        record=request.json
        rec=(record["department_name"],record["report_name"],record["report_url"],record["id"])
        sql_name="""update  reports set department_name=?, report_name=? ,report_url=?  where report_id=?"""     
        cursorObj.execute(sql_name, rec)
        con.commit()
        cursorObj.close()
        con.close()
        result= {"status":"reports updated  successfully"}
        return_status=200
    except  :
        result ={}
        print('Exception while uploading the file  ')
        return_status = 500
        result['status'] =0
        result['message'] = 'Internal Error has Occurred while processing the update request'
        raise
    finally:
        resp = Response(json.dumps(result) ,status = return_status, mimetype ="application/json")
    return resp


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 7197))
    print("runing ...")
    app.run(host = '0.0.0.0', port=port)
