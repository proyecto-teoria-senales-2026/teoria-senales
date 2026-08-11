from pathlib import Path
import re
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def test_all_student_guides_are_integrated(self):
        expected = {
            f"Guia_del_estudiante_{exercise}.{extension}"
            for exercise in ("C-1-1", "C-1-2", "C-1-3", "C-1-4", "C-3-3")
            for extension in ("docx", "pdf")
        }
        self.assertEqual({path.name for path in (ROOT / "docs" / "guias").iterdir()}, expected)

    def test_word_guides_contain_native_equations(self):
        for guide in sorted((ROOT / "docs" / "guias").glob("*.docx")):
            with self.subTest(guide=guide.name), zipfile.ZipFile(guide) as archive:
                document_xml = archive.read("word/document.xml")
                self.assertIn(b"<m:oMath", document_xml)

    def test_no_teacher_guides_in_student_application(self):
        self.assertFalse(any((ROOT / "docs" / "guias").glob("*docente*")))

    def test_no_old_duplicate_guide(self):
        self.assertFalse((ROOT / "docs" / "guias" / "Guia_Estudiante_C1-1.docx").exists())

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
        forbidden = re.compile(r"openai|chatgpt|generad[oa] por ia|marca de agua.*ia", re.IGNORECASE)
        findings = []
        for path in ROOT.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".py", ".md", ".txt", ".bat"}:
                if path.is_relative_to(ROOT / "tests"):
                    continue
                if forbidden.search(path.read_text(encoding="utf-8", errors="ignore")):
                    findings.append(str(path.relative_to(ROOT)))
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
