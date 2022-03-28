import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(10)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)
    
    def test_kortin_saldo_oikein(self):
        self.assertEqual(self.maksukortti.saldo, 10)
    
    def test_rahan_lataaminen_toimii_oikein(self):
        self.maksukortti.lataa_rahaa(10)
        self.assertAlmostEqual(self.maksukortti.saldo, 20)
    
    def test_rahan_ottaminen_toimii_oikein(self):
        self.assertTrue(self.maksukortti.ota_rahaa(5))
        self.assertEqual(self.maksukortti.saldo, 5)
        self.assertFalse(self.maksukortti.ota_rahaa(10))
        self.assertEqual(self.maksukortti.saldo, 5)
    
    def test_saldon_tulostaminen(self):
        self.assertEqual(str(self.maksukortti), "saldo: 0.1")
