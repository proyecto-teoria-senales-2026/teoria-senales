from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

from pypdf import PdfReader
from teoria_senales.reports.pdf_verifier import verify_pdf_against_repository


ROOT = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def test_all_student_guides_are_integrated(self):
        expected = {
            f"Guia_del_estudiante_{exercise}.pdf"
            for exercise in ("C-1-1", "C-1-2", "C-1-3", "C-1-4", "C-3-3")
        }
        self.assertEqual({path.name for path in (ROOT / "docs" / "guias").iterdir()}, expected)

    def test_pdf_guides_contain_mathematical_formulation(self):
        for guide in sorted((ROOT / "docs" / "guias").glob("*.pdf")):
            with self.subTest(guide=guide.name):
                text = "\n".join(page.extract_text() or "" for page in PdfReader(guide).pages)
                self.assertIn("Formulación matemática que debe aplicar", text)

    def test_no_teacher_guides_in_student_application(self):
        self.assertFalse(any((ROOT / "docs" / "guias").glob("*docente*")))

    def test_no_old_duplicate_guide(self):
        self.assertFalse((ROOT / "docs" / "guias" / "Guia_Estudiante_C1-1.docx").exists())
        self.assertFalse(any((ROOT / "docs" / "guias").glob("*.docx")))

    def test_guides_have_three_pages_and_complete_authorship(self):
        expected_authors = "Juan Esteban Rengifo Segura; Julián Felipe Montaña Aguilar"
        for guide in sorted((ROOT / "docs" / "guias").glob("*.pdf")):
            with self.subTest(guide=guide.name):
                reader = PdfReader(guide)
                self.assertEqual(len(reader.pages), 3)
                self.assertEqual(reader.metadata.author, expected_authors)

    def test_institutional_header_asset_exists(self):
        header = (
            ROOT
            / "src"
            / "teoria_senales"
            / "assets"
            / "encabezado_institucional.png"
        )
        self.assertTrue(header.is_file())
        self.assertGreater(header.stat().st_size, 10_000)

    def test_all_streamlit_pages_render_institutional_header(self):
        entrypoints = [ROOT / "app.py", *sorted((ROOT / "pages").glob("*.py"))]
        expected_render = 'st.image(str(HEADER_IMAGE), width="stretch")'
        for entrypoint in entrypoints:
            with self.subTest(entrypoint=entrypoint.relative_to(ROOT)):
                source = entrypoint.read_text(encoding="utf-8")
                self.assertIn("HEADER_IMAGE =", source)
                self.assertIn(expected_render, source)

    def test_rendered_guides_have_no_left_margin_artifact(self):
        renderer = shutil.which("pdftoppm")
        self.assertIsNotNone(renderer, "pdftoppm es obligatorio para el QA visual")
        for guide in sorted((ROOT / "docs" / "guias").glob("*.pdf")):
            with self.subTest(guide=guide.name), tempfile.TemporaryDirectory() as temp_dir:
                prefix = Path(temp_dir) / "page"
                subprocess.run(
                    [renderer, "-png", "-r", "150", str(guide), str(prefix)],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                )
                pages = sorted(Path(temp_dir).glob("page-*.png"))
                self.assertEqual(len(pages), 3)
                from PIL import Image

                for page in pages:
                    image = Image.open(page).convert("RGB")
                    forbidden = [
                        (x, y)
                        for y in range(205, 236)
                        for x in range(0, 25)
                        if max(image.getpixel((x, y))) < 245
                    ]
                    self.assertEqual(
                        forbidden,
                        [],
                        msg=f"Artefacto en margen izquierdo de {guide.name}, {page.name}",
                    )

    def test_single_application_launcher(self):
        self.assertTrue((ROOT / "INICIAR_APLICACION.bat").is_file())
        self.assertFalse((ROOT / "INICIAR_C3-3.bat").exists())

    def test_documented_test_runner_exists(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("python run_tests.py", readme)
        self.assertTrue((ROOT / "run_tests.py").is_file())

    def test_microphone_and_python_requirements_are_consistent(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        quick_start = (ROOT / "INSTRUCCIONES_RAPIDAS.md").read_text(encoding="utf-8")
        launcher = (ROOT / "INICIAR_APLICACION.bat").read_text(
            encoding="utf-8", errors="ignore"
        )
        current_status = (ROOT / "docs" / "estado_actual.md").read_text(
            encoding="utf-8"
        )
        architecture = (ROOT / "docs" / "arquitectura.md").read_text(
            encoding="utf-8"
        )

        for document in (readme, quick_start, launcher):
            self.assertIn("Python 3.12 o 3.13", document)
            self.assertNotIn("Python 3.11", document)

        self.assertIn("El uso del micrófono ya está aprobado", current_status)
        self.assertIn("micrófono desde la interfaz Streamlit", architecture)
        self.assertNotIn(
            "Uso de archivo de audio, micrófono o ambas alternativas",
            current_status,
        )
        self.assertNotIn("cuando se valide su mecanismo", architecture)

    def test_demo_report_is_current_and_encrypted(self):
        report = PdfReader(ROOT / "docs" / "evidencias" / "reporte_demostracion_C3-3.pdf")
        self.assertTrue(report.is_encrypted)
        self.assertNotEqual(report.decrypt(""), 0)
        self.assertEqual(report.metadata.title, "Reporte docente - C-3-3")

    def test_verifier_accepts_original_and_rejects_altered_copy(self):
        evidence = ROOT / "docs" / "evidencias" / "verificacion"
        valid = verify_pdf_against_repository(
            (evidence / "reporte_original_valido_C-3-3.pdf").read_bytes(), evidence
        )
        altered = verify_pdf_against_repository(
            (evidence / "reporte_copia_alterada_C-3-3.pdf").read_bytes(), evidence
        )
        self.assertEqual(valid.status, "VÁLIDO")
        self.assertTrue(valid.valid)
        self.assertEqual(altered.status, "ALTERADO O NO VÁLIDO")
        self.assertFalse(altered.valid)

    def test_github_actions_runs_qa(self):
        workflow = ROOT / ".github" / "workflows" / "qa.yml"
        self.assertTrue(workflow.is_file())
        self.assertIn("python run_tests.py", workflow.read_text(encoding="utf-8"))

    def test_readme_links_exist(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        links = re.findall(r"\]\(([^)]+)\)", readme)
        missing = [link for link in links if not (ROOT / link).exists()]
        self.assertEqual(missing, [])

    def test_visible_access_link_uses_approved_id(self):
        app = (ROOT / "app.py").read_text(encoding="utf-8")
        self.assertIn('label="Abrir C-1-1', app)
        self.assertNotIn('label="Abrir C1-1', app)

    def test_no_ai_branding_in_text_sources(self):
        # Construir los términos desde códigos evita incorporar las propias
        # marcas buscadas como texto visible dentro del paquete distribuido.
        encoded_terms = (
            (111, 112, 101, 110, 97, 105),
            (99, 104, 97, 116, 103, 112, 116),
            (99, 111, 112, 105, 108, 111, 116),
            (103, 101, 109, 105, 110, 105),
            (99, 108, 97, 117, 100, 101),
            (97, 110, 116, 104, 114, 111, 112, 105, 99),
        )
        forbidden_terms = tuple("".join(map(chr, item)) for item in encoded_terms)
        findings = []
        for path in ROOT.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".py", ".md", ".txt", ".bat"}:
                content = path.read_text(encoding="utf-8", errors="ignore").casefold()
                if any(term in content for term in forbidden_terms):
                    findings.append(str(path.relative_to(ROOT)))
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
