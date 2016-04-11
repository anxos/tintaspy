import unittest
import harmonies


# test color string format

class ColorTestCase(unittest.TestCase):
    def test_lengthOne(self):
        self.assertTrue(harmonies.isColor("#ffffff"))

    def test_lengthTwo(self):
        self.assertFalse(harmonies.isColor("#fff"))

    def test_lengthThree(self):
        self.assertFalse(harmonies.isColor("#fffffffffffff"))

    def test_characterSet(self):
        self.assertFalse(harmonies.isColor("#ffxxxx"))

    def test_startSet(self):
        self.assertFalse(harmonies.isColor("fffffff"))

    def test_charSet(self):
        self.assertTrue(harmonies.isColor("#2BD9D9"))


class TupleTestCase(unittest.TestCase):
    def test_white(self):
        self.assertEqual(harmonies.hexToTuple("#ffffff"), (255, 255, 255))

    def test_black(self):
        self.assertEqual(harmonies.hexToTuple("#000000"), (0, 0, 0))

    def test_red(self):
        self.assertEqual(harmonies.hexToTuple("#ff0000"), (255, 0, 0))

    def test_some_cyan(self):
        self.assertEqual(harmonies.hexToTuple("#2BD9D9"), (43, 217, 217))


class SimpleColorConversionTestCase(unittest.TestCase):
    def test_white(self):
        self.assertAlmostEqual(harmonies.rgbRelative((255, 255, 255)), (1, 1, 1), places=4)

    def test_black(self):
        self.assertAlmostEqual(harmonies.rgbRelative((0, 0, 0)), (0, 0, 0), places=4)

    def test_red(self):
        self.assertAlmostEqual(harmonies.rgbRelative((255, 0, 0)), (1, 0, 0), places=4)

    def text_some_cyan(self):
        self.assertAlmostEqual(harmonies.rgbRelative((43, 217, 217)), (0.17, 0.85, 0.85), places=4)

    def test_white_rel(self):
        self.assertEqual(harmonies.rgbAbsolute((1, 1, 1.0)), (255, 255, 255))

    def test_some_cyan_rel(self):
        self.assertEqual(harmonies.rgbAbsolute((0.17, 0.85, 0.85)), (43, 217, 217))

    def test_white_hsl(self):
        self.assertEqual(harmonies.hslAbsolute((0, 0, 1.0)), (0, 0, 100))

    def test_some_cyan_hsl(self):
        self.assertEqual(harmonies.hslAbsolute((0.5, 0.8, 0.85)), (180, 80, 85))

    def test_white_hsl_rel(self):
        self.assertAlmostEqual(harmonies.hslRelative((0, 0, 100)), (0, 0, 1), places=4)

    def test_some_cyan_hsl_rel(self):
        self.assertAlmostEqual(harmonies.hslRelative((180, 80, 85)), (0.5, 0.8, 0.85), places=4)


class ConversionsTestCase(unittest.TestCase):
    def test_white_hex(self):
        self.assertEqual(harmonies.hexColor((255, 255, 255)), "#ffffff")

    def test_some_cyan_hex(self):
        self.assertEqual(harmonies.hexColor((43, 217, 217)), "#2bd9d9")

    def test_white_to_hsl(self):
        self.assertAlmostEqual(harmonies.rgbToHsl((255, 255, 255)), (0, 0, 100), places=2)

    def test_red_to_hsl(self):
        self.assertAlmostEqual(harmonies.rgbToHsl((255, 0, 0)), (0, 100, 50), places=2)

    def test_some_cyan_to_hsl(self):
        self.assertAlmostEqual(harmonies.rgbToHsl((43, 217, 217)), (180, 69.6, 51), places=2)

    def test_some_orange_to_hsl(self):
        self.assertAlmostEqual(harmonies.rgbToHsl((217, 130, 43)), (30, 69.6, 51), places=2)

    def test_white_to_rgb(self):
        self.assertEqual(harmonies.hslToRgb((0, 0, 100)), (255, 255, 255))

    def test_red_to_rgb(self):
        self.assertEqual(harmonies.hslToRgb((0, 100, 50)), (255, 0, 0))

    def test_some_cyan_to_rgb(self):
        self.assertEqual(harmonies.hslToRgb((180, 69.6, 51)), (43, 217, 217))

    def test_some_orange_to_rgb(self):
        self.assertEqual(harmonies.hslToRgb((30, 69.6, 51)), (217, 130, 43))


class HarmoniesTestCase(unittest.TestCase):
    def test_complementary_cyan(self):
        self.assertAlmostEqual(harmonies.complementary((180, 69.6, 51)), (0, 69.6, 51), places=2)

    def test_complementary_orange(self):
        self.assertAlmostEqual(harmonies.complementary((30, 69.6, 51)), (210, 69.6, 51), places=2)

    def test_split_complementary_orange(self):
        self.assertEqual(harmonies.splitComplementary((30, 69.6, 51)), ((180, 69.6, 51), (240, 69.6, 51)))


if __name__ == '__main__':
    unittest.main()
