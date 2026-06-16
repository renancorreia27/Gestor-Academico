from database.conexao import ConexaoMySQL
from models import Usuario

class BancoDados:    
    @staticmethod
    def _get_cursor():
        conexao = ConexaoMySQL().conectar()
        if conexao:
            return conexao.cursor(dictionary=True), conexao
        return None, None

    @staticmethod
    def autenticar_usuario(email, senha):
        """
        Busca e autentica o usuário no banco de dados para o login.
        """
        cursor, _ = BancoDados._get_cursor()
        if not cursor: return None
        
        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s LIMIT 1", (email, senha))
        r = cursor.fetchone()
        cursor.close()
        
        if r:
            return Usuario(
                nome=r.get('nome', 'Aluno'),
                curso=r.get('curso', ''),
                carga_horaria_total=r.get('carga_horaria_total', 0),
                semestres_totais=r.get('semestres_totais', 0),
                iea=r.get('iea', 0.0),
                semestres_cursados=r.get('semestres_cursados', 0),
                id=r.get('id')
            )
        return None

    @staticmethod
    def registrar_usuario(nome, email, senha):
        """
        Insere um novo usuário no banco de dados.
        """
        cursor, conexao = BancoDados._get_cursor()
        if not cursor: return False
        
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha, curso, carga_horaria_total, semestres_totais, iea, semestres_cursados) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (nome, email, senha, '', 0, 0, 0.0, 0)
            )
            conexao.commit()
            sucesso = cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao registrar: {e}")
            sucesso = False
        finally:
            cursor.close()
            
        return sucesso

    @staticmethod
    def redefinir_senha(email, nova_senha):
        """
        Atualiza a senha do usuário com base no email.
        """
        cursor, conexao = BancoDados._get_cursor()
        if not cursor: return False
        
        try:
            cursor.execute("UPDATE usuarios SET senha = %s WHERE email = %s", (nova_senha, email))
            conexao.commit()
            sucesso = cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao redefinir senha: {e}")
            sucesso = False
        finally:
            cursor.close()
            
        return sucesso
