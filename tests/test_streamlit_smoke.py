from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


class StreamlitSmokeTests(unittest.TestCase):
    def _run(self, relative_path):
        app = AppTest.from_file(str(ROOT / relative_path), default_timeout=15)
        app.run()
        self.assertEqual(list(app.exception), [], msg=f"Excepciones al abrir {relative_path}")
        return app

    def _assert_institutional_header_is_rendered(self, app, relative_path):
        images = app.get("image")
        self.assertGreaterEqual(
            len(images),
            1,
            msg=f"No se renderizó el encabezado institucional en {relative_path}",
        )

    def test_application_entrypoint(self):
        app = self._run("app.py")
        self.assertTrue(
            any("Señales fundamentales" in title.value for title in app.title)
        )
        self._assert_institutional_header_is_rendered(app, "app.py")

    def test_c3_3_page(self):
        app = self._run("pages/05_C3_3.py")
        self.assertTrue(any("Convolución" in title.value for title in app.title))
        self._assert_institutional_header_is_rendered(app, "pages/05_C3_3.py")

    def test_c1_1_page(self):
        app = self._run("pages/01_C1_1.py")
        self._assert_institutional_header_is_rendered(app, "pages/01_C1_1.py")

    def test_c1_2_page(self):
        app = self._run("pages/02_C1_2.py")
        self._assert_institutional_header_is_rendered(app, "pages/02_C1_2.py")

    def test_c1_3_page(self):
        app = self._run("pages/03_C1_3.py")
        self._assert_institutional_header_is_rendered(app, "pages/03_C1_3.py")

    def test_c1_4_page(self):
        app = self._run("pages/04_C1_4.py")
        self._assert_institutional_header_is_rendered(app, "pages/04_C1_4.py")


if __name__ == "__main__":
    unittest.main()
