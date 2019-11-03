import unittest

from src.render import render


class RenderTestCase(unittest.TestCase):
    
    def test_render(self):
        measurements = [
            {
                'location': 'St. James',
                'measurement': 4,
                'coordinates': [45, 46]
            },
            {
                'location': 'St. Boniface',
                'measurement': 6,
                'coordinates': [47, 48]
            }
        ]

        html = render(measurements, "src/templates/")
        self.assertIn('addMarker("45", "46", "St. James", "4");', html)
        self.assertIn('addMarker("47", "48", "St. Boniface", "6")', html)

if __name__ == '__main__':
    unittest.main()