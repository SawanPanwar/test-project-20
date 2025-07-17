from ..models import Course
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection


class CourseService(BaseService):

    def search(self, params):
        pageNo = (params['pageNo'] - 1) * self.pageSize
        sql = "select * from sos_course where 1=1"
        val = params.get("name", None)
        if DataValidator.isNotNull(val):
            sql += " and name = '" + val + "' "
        sql += " limit %s,%s"
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize])
        params['index'] = ((params['pageNo'] - 1) * self.pageSize) + 1
        result = cursor.fetchall()
        columnName = ('id', 'name', 'description', 'duration')
        res = {
            "data": [],
            "MaxId": 1,
        }
        count = 0
        res["index"] = params["index"]
        for x in result:
            print({columnName[i]: x[i] for i, _ in enumerate(x)})
            params['MaxId'] = x[0]
            res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return Course
