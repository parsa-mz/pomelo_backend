from fastapi import Depends, HTTPException, status

from core.dependencies.authenticate import auth_middleware



def ALLOW_ANY():
    """
    Access level: everyone
    """
    return True


def IS_AUTHENTICATED(user=Depends(auth_middleware)):
    """
    Access level: authenticated users
    """
    return user
