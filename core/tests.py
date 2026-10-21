from django.test import SimpleTestCase
from django.urls import reverse

from .content import load_events, load_notices


class PublicSiteTests(SimpleTestCase):
    def test_json_content_is_valid(self):
        self.assertEqual(len(load_events("event")), 5)
        briefings = load_events("briefing")
        self.assertEqual(len(briefings), 3)
        self.assertEqual(
            [item["event_date"] for item in briefings],
            sorted((item["event_date"] for item in briefings), reverse=True),
        )
        self.assertEqual(briefings[-1]["id"], 9)
        self.assertEqual(load_notices(), [])

    def test_event_list_and_detail_use_json_content(self):
        list_response = self.client.get(reverse("events"))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, "생성형 AI 기술의 현재와 미래")

        detail_response = self.client.get(reverse("event_detail", args=[4]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "The Present and Future")

    def test_contact_page_has_no_submission_form(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "<form")
        self.assertContains(response, "mailto:psych.law.du@gmail.com")

    def test_admin_and_login_routes_are_not_exposed(self):
        self.assertEqual(self.client.get("/admin/").status_code, 404)
        self.assertEqual(self.client.get("/login/").status_code, 404)
        self.assertEqual(self.client.get("/events/create/").status_code, 404)

    def test_static_export_lists_include_all_items_and_client_controls(self):
        response = self.client.get(reverse("events"), {"_static": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "data-static-list")
        self.assertContains(response, "data-static-item", count=5)
        self.assertContains(response, "js/static-list.js")

        briefing_response = self.client.get(
            reverse("performance_briefing"), {"_static": "1"}
        )
        self.assertContains(briefing_response, "data-static-item", count=3)
