from datetime import timedelta, datetime, UTC
from pathlib import Path
from typing import Dict

import jwt
from pydantic import BaseModel

from backend.src.config.settings import settings


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = 'Bearer'


class AuthJWT:
    private_key_path: Path = settings.jwt.private_key
    public_key_path: Path = settings.jwt.public_key
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    TOKEN_TYPE_FIELD = 'type'
    ACCESS_TOKEN_TYPE = 'access'
    REFRESH_TOKEN_TYPE = 'refresh'

    def encode_jwt(
            self,
            payload: dict,
            expire_timedelta: timedelta | None = None,
    ) -> str:
        private_key = self.private_key_path.read_text()
        to_encode = payload.copy()
        now = datetime.now(UTC)
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update(exp=expire, iat=now)
        encoded = jwt.encode(to_encode, private_key, algorithm=self.algorithm)
        return encoded

    def decode_jwt(
            self,
            token: str | bytes,
    ) -> Dict:
        public_key: str = self.public_key_path.read_text()
        decoded = jwt.decode(token, public_key, algorithms=[self.algorithm])
        return decoded

    def create_jwt(
            self,
            token_type: str,
            token_data: dict,
            expire_timedelta: timedelta | None = None,
    ) -> str:
        jwt_payload = {self.TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)
        if jwt_payload.get('sub'):
            jwt_payload['sub'] = str(token_data['sub'])
        return self.encode_jwt(
            payload=jwt_payload,
            expire_timedelta=expire_timedelta
        )

    def create_access_token(self, payload: dict) -> str:
        return self.create_jwt(
            token_type=self.ACCESS_TOKEN_TYPE,
            token_data=payload
        )

    def create_refresh_token(self, payload: dict) -> str:
        return self.create_jwt(
            token_type=self.REFRESH_TOKEN_TYPE,
            token_data=payload,
            expire_timedelta=timedelta(days=self.refresh_token_expire_days)
        )

    def token_refresh(self, refresh_token: str) -> tuple[str, str] | tuple[None, None]:
        try:
            decoded_refresh_token = self.decode_jwt(refresh_token)
            access_token = self.create_access_token(decoded_refresh_token)
            refresh_token = self.create_refresh_token(decoded_refresh_token)
            return access_token, refresh_token
        except Exception as e:
            print(f'error:{e}')
            return None, None


jwt_token = AuthJWT()
