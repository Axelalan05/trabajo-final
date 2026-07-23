from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator

token_generator = PasswordResetTokenGenerator()


def generate_reset_token(user):
    """Genera un token usando el PasswordResetTokenGenerator de Django."""
    return token_generator.make_token(user)


def check_reset_token(user, token):
    """Verifica que el token sea válido y no haya expirado.
    
    Django internamente usa el uid, el password hash del usuario y
    el timestamp de creación. Al cambiar la contraseña con set_password(),
    el hash cambia y el token queda automáticamente invalidado.
    """
    return token_generator.check_token(user, token)


def send_reset_email(user, request=None):
    """
    Envía el correo de recuperación mediante Resend.
    Retorna (success: bool, token: str | None).
    """
    token = generate_reset_token(user)
    uid = user.pk

    reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"

    subject = "Recuperación de contraseña - GameVault"

    html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: system-ui, 'Segoe UI', Roboto, sans-serif; background-color: #121366; color: #FFFFFF; padding: 40px; margin: 0;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #080933; border-radius: 12px; padding: 40px; border: 1px solid rgba(255,255,255,0.10);">
        <div style="text-align: center; margin-bottom: 8px;">
            <span style="font-size: 28px; font-weight: bold; color: #68F99F;">GameVault</span>
        </div>
        <h2 style="color: #FFFFFF; text-align: center; font-weight: 600; margin-top: 0;">Recuperación de contraseña</h2>
        <p style="color: #CCCCCC; text-align: center; font-size: 15px; line-height: 1.6; margin-bottom: 28px;">
            Hola <strong style="color: #FFFFFF;">{user.username}</strong>, recibiste este correo porque solicitaste restablecer tu contraseña.
        </p>
        <div style="text-align: center; margin: 32px 0;">
            <a href="{reset_url}"
               style="display: inline-block; background-color: #68F99F; color: #121366; text-decoration: none;
                      padding: 14px 36px; border-radius: 8px; font-size: 16px; font-weight: bold;">
                Restablecer contraseña
            </a>
        </div>
        <p style="color: #B0B0B0; text-align: center; font-size: 13px;">
            Este enlace expira en 1 hora. Si no solicitaste este cambio, ignorá este mensaje.
        </p>
        <p style="color: #666; text-align: center; font-size: 11px; margin-top: 28px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 20px;">
            Si el botón no funciona, copiá y pegá este enlace en tu navegador:<br>
            <span style="color: #68F99F; word-break: break-all;">{reset_url}</span>
        </p>
    </div>
</body>
</html>
"""

    try:
        import resend

        resend.api_key = settings.RESEND_API_KEY

        params = {
            "from": settings.RESEND_FROM_EMAIL,
            "to": [user.email],
            "subject": subject,
            "html": html_message,
        }

        resend.Emails.send(params)
        return True, token
    except Exception as e:
        print(f"Error al enviar email con Resend: {e}")
        return False, token

def send_verification_email(username, email, uid, token, request=None):
    """
    Envía el correo de verificación de registro mediante Resend.
    """
    verify_url = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}"

    subject = "Confirmá tu registro - GameVault"

    html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: system-ui, 'Segoe UI', Roboto, sans-serif; background-color: #121366; color: #FFFFFF; padding: 40px; margin: 0;">
    <div style="max-width: 600px; margin: 0 auto; background-color: #080933; border-radius: 12px; padding: 40px; border: 1px solid rgba(255,255,255,0.10);">
        <div style="text-align: center; margin-bottom: 8px;">
            <span style="font-size: 28px; font-weight: bold; color: #68F99F;">GameVault</span>
        </div>
        <h2 style="color: #FFFFFF; text-align: center; font-weight: 600; margin-top: 0;">Confirmá tu registro</h2>
        <p style="color: #CCCCCC; text-align: center; font-size: 15px; line-height: 1.6; margin-bottom: 28px;">
            Hola <strong style="color: #FFFFFF;">{username}</strong>, hacé clic en el botón para confirmar tu cuenta en GameVault.
        </p>
        <div style="text-align: center; margin: 32px 0;">
            <a href="{verify_url}"
               style="display: inline-block; background-color: #68F99F; color: #121366; text-decoration: none;
                      padding: 14px 36px; border-radius: 8px; font-size: 16px; font-weight: bold;">
                Confirmar registro
            </a>
        </div>
        <p style="color: #B0B0B0; text-align: center; font-size: 13px; margin-top: 24px;">
            Si no solicitaste este registro, ignorá este mensaje.
        </p>
        <p style="color: #666; text-align: center; font-size: 11px; margin-top: 28px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 20px;">
            Si el botón no funciona, copiá y pegá este enlace en tu navegador:<br>
            <span style="color: #68F99F; word-break: break-all;">{verify_url}</span>
        </p>
    </div>
</body>
</html>
"""

    try:
        import resend

        resend.api_key = settings.RESEND_API_KEY

        params = {
            "from": settings.RESEND_FROM_EMAIL,
            "to": [email],
            "subject": subject,
            "html": html_message,
        }

        resend.Emails.send(params)
        return True
    except Exception as e:
        print(f"Error al enviar email de verificación con Resend: {e}")
        return False