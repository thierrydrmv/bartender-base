from django.template.loader import render_to_string
from django.test import SimpleTestCase, TestCase, override_settings


class ErrorPageTests(TestCase):
    @override_settings(DEBUG=False)
    def test_404_page(self):
        response = self.client.get("/pagina-que-nao-existe/")

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")
        self.assertContains(
            response,
            "Página não encontrada",
            status_code=404,
        )


class ServerErrorTemplateTests(SimpleTestCase):
    def test_500_template_can_be_rendered(self):
        content = render_to_string("500.html")

        self.assertIn("Erro 500", content)
        self.assertIn("Algo não saiu como esperado", content)
