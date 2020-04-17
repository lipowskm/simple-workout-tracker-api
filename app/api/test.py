from fastapi import HTTPException

from fastapi import APIRouter, Depends
from pydantic import EmailStr
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE

from app.models.user import User as DBUser
from app.api.utils.security import get_current_active_superuser, get_current_user
from app.schemas.msg import Msg
from app.schemas.user import User
from app.utils.email import send_test_email

router = APIRouter()


@router.post("/test-email",
             response_model=Msg,
             status_code=201,
             dependencies=[Depends(get_current_active_superuser)])
def test_email(
    email: EmailStr
):
    """
    Send test email to given email address
    """
    response = send_test_email(email=email)
    if response.status_code != 250:
        raise HTTPException(
            status_code=HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error while trying to send email, please try again",
        )
    return {"msg": "Test email sent"}


@router.post("/test-token",
             tags=["tests"],
             response_model=User,
             dependencies=[Depends(get_current_user)])
def test_token(current_user: DBUser = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user
