from django.template.loader import render_to_string
from django.test import SimpleTestCase


class ErrorPageTests(SimpleTestCase):
    def test_500_template_can_be_rendered(self):
        content = render_to_string("500.html")

        self.assertIn("Erro 500", content)
        self.assertIn("Algo não saiu como esperado", content)
