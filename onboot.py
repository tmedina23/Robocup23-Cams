import auto
from pysondb import db

camdb = db.getDb("camdb.json")

auto.run_auto()
camdb.updateById(209847509711096578,{"index":"False"})
camdb.updateById(283699290575417516,{"index":"7"})