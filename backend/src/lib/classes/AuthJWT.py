from datetime import timedelta, datetime, UTC
from typing import Dict, Optional

import jwt
from pydantic import BaseModel

from backend.src.config.settings import settings


class Token(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
    token_type: str = 'Bearer'


class AuthJWT:
    private_key: str = settings.jwt.private_key
    public_key: str = settings.jwt.public_key
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    TOKEN_TYPE_FIELD: str = 'type'
    ACCESS_TOKEN: str = 'access_token'
    REFRESH_TOKEN: str = 'refresh_token'

    def _encode_jwt(
            self,
            payload: dict,
            expire_timedelta: timedelta | None = None,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.now(UTC)
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update(exp=expire, iat=now)
        encoded = jwt.encode(to_encode, self.private_key, algorithm=self.algorithm)
        return encoded

    def decode_jwt(
            self,
            token: str | bytes,
    ) -> Dict:
        decoded = jwt.decode(token, self.public_key, algorithms=[self.algorithm])
        return decoded

    def _create_jwt(
            self,
            token_type: str,
            token_data: dict,
            expire_timedelta: timedelta | None = None,
    ) -> str:
        jwt_payload = {self.TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)
        if jwt_payload.get('sub'):
            jwt_payload['sub'] = str(token_data['sub'])
        return self._encode_jwt(
            payload=jwt_payload,
            expire_timedelta=expire_timedelta
        )

    def create_access_token(self, payload: dict) -> str:
        return self._create_jwt(
            token_type=self.ACCESS_TOKEN,
            token_data=payload
        )

    def create_refresh_token(self, payload: dict) -> str:
        return self._create_jwt(
            token_type=self.REFRESH_TOKEN,
            token_data=payload,
            expire_timedelta=timedelta(days=self.refresh_token_expire_days)
        )

    def token_refresh(self, refresh_token: str) -> Optional[Token]:
        try:
            decoded_refresh_token = self.decode_jwt(refresh_token)
            access_token = self.create_access_token(decoded_refresh_token)
            refresh_token = self.create_refresh_token(decoded_refresh_token)
            return Token(access_token=access_token, refresh_token=refresh_token)
        except Exception as e:
            print(f'error:{e}')
            return None


jwt_token = AuthJWT()
