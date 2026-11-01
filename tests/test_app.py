"""Regression tests for the public HTTP API, using only unittest and Flask."""

import unittest

from app import create_app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

    def test_seeded_items(self):
        response = self.client.get("/items")
        self.assertEqual(response.json["count"], 2)
        self.assertEqual(response.json["items"][0]["id"], 1)

    def test_filter_by_category(self):
        self.client.post("/add-item", json={"name": "Demo", "category": "project"})
        response = self.client.get("/items?category=project")
        self.assertEqual(response.json["count"], 1)
        self.assertEqual(response.json["items"][0]["name"], "Demo")

    def test_get_item_and_missing_item(self):
        self.assertEqual(self.client.get("/items/1").json["name"], "Python Basics")
        self.assertEqual(self.client.get("/items/999").status_code, 404)

    def test_create_item_trims_text_and_returns_new_id(self):
        response = self.client.post("/add-item", json={"name": "  Flask  ", "category": "  demo "})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["item"], {"id": 3, "name": "Flask", "category": "demo"})
        self.assertEqual(self.client.get("/items").json["count"], 3)

    def test_non_json_content_type_rejected(self):
        response = self.client.post("/add-item", data="name=test")
        self.assertEqual(response.status_code, 415)

    def test_malformed_json_rejected(self):
        response = self.client.post("/add-item", data="{", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_non_object_json_rejected(self):
        response = self.client.post("/add-item", json=["test"])
        self.assertEqual(response.status_code, 400)

    def test_empty_wrong_type_and_oversized_fields_rejected(self):
        for body in ({"name": " ", "category": "demo"},
                     {"name": 2, "category": "demo"},
                     {"name": "a" * 101, "category": "demo"},
                     {"name": "demo"}):
            with self.subTest(body=body):
                self.assertEqual(self.client.post("/add-item", json=body).status_code, 400)

    def test_isolated_app_instances(self):
        self.client.post("/add-item", json={"name": "first", "category": "test"})
        self.assertEqual(create_app().test_client().get("/items").json["count"], 2)


if __name__ == "__main__":
    unittest.main()
