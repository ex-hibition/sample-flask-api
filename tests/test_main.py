from flask import json
import unittest
import main


class TestFlask(unittest.TestCase):
    def setUp(self):
        self.app = main.app.test_client()
        main.init()

    def tearDown(self):
        pass

    def test_working_index(self):
        # 指定パスにhttp getリクエストを送る
        result_values = self.app.get("/")

        self.assertEqual(result_values.status_code, 200)
        self.assertEqual(result_values.data, "it's works.".encode('utf-8'))

    def test_working_records(self):
        # 指定パスにhttp getリクエストを送る
        result_values = self.app.get("/app/records")

        self.assertEqual(result_values.status_code, 200)

    def test_working_get_records(self):
        # 指定パスにhttp getリクエストを送る
        result_values = self.app.get("/app/records/testid001")

        self.assertEqual(result_values.status_code, 200)

        result_dict = json.loads(result_values.data)
        for rec in result_dict.get("body"):
            self.assertEqual(rec.get("user_id"), "testid001")
            self.assertEqual(rec.get("dept_no"), "dept01")
            self.assertEqual(rec.get("user_name"), "testuser01")

