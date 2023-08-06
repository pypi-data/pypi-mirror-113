import math

import jax

import jax.numpy as jnp


def matrix2angles(R):
    r"""conversion from matrix to angles
    Parameters. Derived from https://www.geometrictools.com/Documentation/EulerAngles.pdf 2.12
    ----------
    R : `jax.array`
        matrices of shape :math:`(..., 3, 3)`
    Returns
    -------
    alpha : `jax.array`
        tensor of shape :math:`(...)`
    beta : `jax.array`
        tensor of shape :math:`(...)`
    gamma : `jax.array`
        tensor of shape :math:`(...)`
    """
    alpha = jnp.arctan2(R[...,1,2],R[...,0,2])
    beta = jnp.arccos(R[...,2,2])
    gamma = jnp.arctan2(R[...,2,1],-R[...,2,0])
    return alpha,beta,gamma  # z,y,z' convention
    
def angles2matrix(alpha,beta,gamma):
    r"""conversion from angles to matrix
    Parameters
    ----------
    alpha : `jax.array`
        tensor of shape :math:`(...)`
    beta : `jax.array`
        tensor of shape :math:`(...)`
    gamma : `jax.array`
        tensor of shape :math:`(...)`
    Returns
    -------
    `jax.array`
        matrices of shape :math:`(..., 3, 3)`
    """
    
    alpha, beta, gamma = jax.numpy.broadcast_arrays(alpha, beta, gamma)
    
    return matrix_z(alpha) @ matrix_y(beta) @ matrix_z(gamma)


def matrix_x(angle):
    r"""matrix of rotation around X axis
    Parameters
    ----------
    angle : `jax.array`
        tensor of any shape :math:`(...)`
    Returns
    -------
    `jax.array`
        matrices of shape :math:`(..., 3, 3)`
    """
    c = jnp.cos(angle)
    s = jnp.sin(angle)
    o = jnp.ones(jnp.shape(angle))
    z = jnp.zeros(jnp.shape(angle))
    return jnp.stack([
        jnp.stack([o, z, z], axis=-1),
        jnp.stack([z, c, -s], axis=-1),
        jnp.stack([z, s, c], axis=-1),
    ], axis=-2)



def matrix_y(angle):
    r"""matrix of rotation around Y axis
    Parameters
    ----------
    angle : `jax.array
        tensor of any shape :math:`(...)`
    Returns
    -------
    `jax.array`
        matrices of shape :math:`(..., 3, 3)`
    """
    c = jnp.cos(angle)
    s = jnp.sin(angle)
    o = jnp.ones(jnp.shape(angle))
    z = jnp.zeros(jnp.shape(angle))
    return jnp.stack([
        jnp.stack([c, z, s], axis=-1),
        jnp.stack([z, o, z], axis=-1),
        jnp.stack([-s, z, c], axis=-1),
    ], axis=-2)

def matrix_z(angle):
    r"""matrix of rotation around Y axis
    Parameters
    ----------
    angle : `jax.array`
        tensor of any shape :math:`(...)`
    Returns
    -------
    `jax.array`
        matrices of shape :math:`(..., 3, 3)`
    """
    c = jnp.cos(angle)
    s = jnp.sin(angle)
    o = jnp.ones(jnp.shape(angle))
    z = jnp.zeros(jnp.shape(angle))
    return jnp.stack([
        jnp.stack([c, -s, z], axis=-1),
        jnp.stack([s, c, z], axis=-1),
        jnp.stack([z, z, o], axis=-1),
    ], axis=-2)