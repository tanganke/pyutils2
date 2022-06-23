import unittest
from pyutils.quantum.qubit import from_bloch_sphere, to_bloch_sphere


class TestBlochSphere(unittest.TestCase):

    def test_bloch_shpere(self):
        qubit = from_bloch_sphere(0, 0)
        print(qubit)
        print(to_bloch_sphere(*qubit))


if __name__ == '__main__':
    unittest.main()
