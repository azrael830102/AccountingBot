import sqlite3
import time
from datetime import datetime

helpMsg = "* h/H: Help, show this help message\n* c/C: Delete all records\n* a/A: Show all records\n* Enter the amount of money to create a new record"
TABLE_NAME = "AccountingRecord"
VIEW_NAME = "TotalRecord"
def current_milli_time_formatter(currTime, showTime=True):
    if showTime:
        return datetime.fromtimestamp(currTime / 1000).strftime("%Y/%m/%d %H:%M:%S")
    else:
        return datetime.fromtimestamp(currTime / 1000).strftime("%Y/%m/%d")

def current_milli_time():
    return round(time.time() * 1000)


class MessageHandler:

    def handleMsg(self, msg:str) -> str:
        resultMsg = "Unknown request"
        if len(msg) == 1:
            prefix = str.upper(msg[0])
            match prefix:
                case 'H':
                    resultMsg = self._showHelp()
                case 'C':
                    resultMsg = self._clearRecords()
                case 'A':
                    resultMsg = self._showTotalRecords()
                case _:
                    pass
        else:
            try:
                cash = int(msg)
                if cash > 0:
                    resultMsg = self._insertRecord(cash)
                else:
                    resultMsg = "Would not create a new record(cash = 0)."
            except: 
                pass
        return resultMsg

    def _showHelp(self) -> str:
        return helpMsg

    def _insertRecord(self, cash:int) -> str:
        con = sqlite3.connect("accounting_record.db")
        cur = con.cursor()
        resultMsg = ""
        try:
            currTime = current_milli_time()
            cur.execute(f"INSERT INTO {TABLE_NAME} VALUES (NULL,{cash},{currTime})")
            con.commit()
            currDateTime = current_milli_time_formatter(currTime)
            resultMsg = f"New record: {currDateTime} → ${cash}"
        except Exception as e:
            resultMsg = f"{e}"
        return resultMsg

    def _showTotalRecords(self)->str:
        con = sqlite3.connect("accounting_record.db")
        cur = con.cursor()
        resultMsg = ""
        try:
            res = cur.execute(f"SELECT * FROM {VIEW_NAME}")
            record = res.fetchone()
            if record[0] is None:
                resultMsg = "No record"
            else:
                startDateTime = current_milli_time_formatter(record[0], showTime=False)
                endDateTime = current_milli_time_formatter(record[1], showTime=False)
                totalCash = record[2]
                resultMsg = f"{startDateTime} ~ {endDateTime} → Total: ${totalCash}"
                pass
        except Exception as e:
            resultMsg = f"{e}"
        return resultMsg

    def _clearRecords(self) -> str:
        con = sqlite3.connect("accounting_record.db")
        cur = con.cursor()
        resultMsg = ""
        try:
            cur.execute(f"DELETE FROM {TABLE_NAME}")
            cur.execute(f"DELETE FROM sqlite_sequence WHERE name='{TABLE_NAME}'")
            con.commit()
            resultMsg = "All records cleared"
        except Exception as e:
            resultMsg = f"{e}"
        return resultMsg

    
