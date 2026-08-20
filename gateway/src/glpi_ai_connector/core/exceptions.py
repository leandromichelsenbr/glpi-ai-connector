class GLPIError(RuntimeError):
    """Erro retornado ou detectado na integração com o GLPI."""


class GLPIAuthenticationError(GLPIError):
    """Falha de autenticação ou criação da sessão GLPI."""
