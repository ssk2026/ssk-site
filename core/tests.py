from django.test import SimpleTestCase
from django.urls import reverse
from unittest.mock import patch

from .content import load_events, load_notices, load_papers


class PublicSiteTests(SimpleTestCase):
    def test_home_starts_with_doctype_without_bom(self):
        response = self.client.get(reverse("home"))
        self.assertNotIn(b"\xef\xbb\xbf", response.content[:16])
        self.assertTrue(response.content.lstrip().startswith(b"<!DOCTYPE html>"))

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
        self.assertEqual(len(load_papers()), 1)

    def test_event_list_and_detail_use_json_content(self):
        list_response = self.client.get(reverse("events"))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, "생성형 AI 기술의 현재와 미래")

        detail_response = self.client.get(reverse("event_detail", args=[4]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, "The Present and Future")

    def test_contact_page_has_email_submission_form(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'action="/api/contact"')
        self.assertContains(response, 'name="email"')
        self.assertContains(response, 'name="message"')
        self.assertContains(response, 'name="consent"')
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

    def test_unpublished_content_is_hidden(self):
        self.assertTrue(all(item.get("published", True) for item in load_events()))
        self.assertTrue(all(item.get("published", True) for item in load_papers()))

    @patch("core.views.load_notices")
    def test_static_notice_rows_have_search_metadata(self, mocked_load_notices):
        mocked_load_notices.return_value = [
            {
                "slug": "sample-notice",
                "title": "테스트 공지",
                "author": "관리자",
                "created_at": "2026-10-21",
                "content_html": "<p>공지 본문</p>",
            }
        ]
        response = self.client.get(reverse("notice_list"), {"_static": "1"})
        self.assertContains(response, "data-static-item", count=1)
        self.assertContains(response, 'data-search-title="테스트 공지"')
