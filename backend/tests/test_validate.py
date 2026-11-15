import unittest

from raye_site.validate import normalise_email, parse_lang, truthy


class EmailTests(unittest.TestCase):
    def test_accepts_and_normalises(self):
        self.assertEqual(normalise_email("  Marie.Tremblay@Exemple.QC.CA "),
                         "marie.tremblay@exemple.qc.ca")
        self.assertEqual(normalise_email("a+raye@x.io"), "a+raye@x.io")
        self.assertEqual(normalise_email("jean_luc-p.2@test.ca"), "jean_luc-p.2@test.ca")

    def test_idn_domain_becomes_ascii(self):
        self.assertEqual(normalise_email("jo@éxample.ca"), "jo@xn--xample-9ua.ca")

    def test_rejects_bad_shapes(self):
        bad = [
            "", "plain", "@x.ca", "a@", "a@b", "a@b.c", "a..b@x.ca", ".a@x.ca",
            "a.@x.ca", "a@-x.ca", "a@x-.ca", "a@x..ca", "a b@x.ca", "a@x.ca\r\nBcc: z@y.ca",
            "a@x.ca\n", "a\x00@x.ca", '"quoted"@x.ca', "a@[127.0.0.1]", "a@x.c4",
            "a@x.ca,b@y.ca", "a<b>@x.ca", "é@x.ca", None, 42,
            "o'neil@x.ca", "a=b@x.ca", "a!b@x.ca", "a{b}@x.ca", "a|b@x.ca", "a`b@x.ca",
            "a%b@x.ca", "a/b@x.ca", "-..a@x.ca",
        ]
        for value in bad:
            with self.subTest(value=value):
                self.assertIsNone(normalise_email(value))

    def test_length_caps(self):
        self.assertIsNone(normalise_email("a" * 65 + "@x.ca"))
        self.assertIsNotNone(normalise_email("a" * 64 + "@x.ca"))
        long_domain = ".".join(["b" * 60] * 5) + ".ca"
        self.assertIsNone(normalise_email("a@" + long_domain))
        self.assertIsNone(normalise_email("a@" + "b" * 64 + ".ca"))

    def test_idn_garbage_rejected(self):
        self.assertIsNone(normalise_email("a@ .ca"))


class LangTests(unittest.TestCase):
    def test_lang(self):
        self.assertEqual(parse_lang("en"), "en")
        self.assertEqual(parse_lang("EN"), "en")
        self.assertEqual(parse_lang("fr"), "fr")
        self.assertEqual(parse_lang("de"), "fr")
        self.assertEqual(parse_lang(None), "fr")
        self.assertEqual(parse_lang(["en"]), "fr")

    def test_truthy(self):
        for v in (True, "on", "1", "yes", "true", "oui"):
            self.assertTrue(truthy(v))
        for v in (False, None, "", "0", "no", "off", 1.5, [], "false"):
            self.assertFalse(truthy(v))


if __name__ == "__main__":
    unittest.main()
