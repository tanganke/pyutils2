import numpy as np
import math

__all__ = ['from_bloch_sphere', 'to_bloch_sphere',
           'I', 'X', 'Y', 'Z',
           'Rx', 'Ry', 'Rz',
           ]


def from_bloch_sphere(theta, phi):
    """
    Returns a qubit with the given Bloch sphere coordinates.

    Args:
        theta (float)
        phi (float)

    Returns:
        Tuple[float, complex]
    """

    return (np.cos(theta / 2),
            np.sin(theta / 2) * np.exp(1j * phi))


def to_bloch_sphere(c0, c1, eps=1e-4):
    R"""
    Returns the Bloch sphere coordinates of qubit c0|0>+c1|1>.

    Args:
        c0 (complex)
        c1 (complex)

    Returns:
        Tuple[float, float]
    """
    r0 = np.abs(c0)
    r1 = np.abs(c1)
    assert np.abs(r0 * r0 + r1 * r1 - 1) <= eps, \
        "c0|0>+c1|1> is not a valid qubit"

    phi0 = np.angle(c0)
    phi1 = np.angle(c1)

    theta = 2 * np.arccos(r0)
    phi = phi1 - phi0
    phi = phi - 2 * np.pi * np.floor(phi / np.pi)

    return (theta, phi)


I = np.array([[1, 0], [0, 1]], dtype=np.float)
X = np.array([[0, 1], [1, 0]], dtype=np.float)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex)
Z = np.array([[1, 0], [0, -1]], dtype=np.float)


def Rx(theta):
    return np.cos(theta / 2) * I - 1j * np.sin(theta / 2) * X


def Ry(theta):
    return np.cos(theta / 2) * I - 1j * np.sin(theta / 2) * Y


def Rz(theta):
    return np.cos(theta / 2) * I - 1j * np.sin(theta / 2) * Z
