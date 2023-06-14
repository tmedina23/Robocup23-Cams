import auto
import time
from pysondb import db

camdb = db.getDb("camdb.json")

time.sleep(5)
auto.run_auto()
auto.ip()
camdb.updateById(209847509711096578,{"index":"False"})
camdb.updateById(283699290575417516,{"index":"7"})