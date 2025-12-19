from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required


def create_tokens(identity: dict):
    """Create access and refresh tokens.

    For compatibility and to satisfy JWT subject constraints, we set the token
    identity (sub) to the user's id as a string and attach role/email as additional claims.
    """
    sub = str(identity.get("user_id"))
    additional = {"role": identity.get("role"), "email": identity.get("email")}
    access = create_access_token(identity=sub, additional_claims=additional)
    refresh = create_refresh_token(identity=sub, additional_claims=additional)
    return {"access_token": access, "refresh_token": refresh}


def protected(fn):
    # Simple wrapper that enforces JWT presence; use flask_jwt_extended decorators as well
    return jwt_required()(fn)
