from database.conexao import ConexaoMySQL
from models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash

class BancoDados:    
    @staticmethod
    def _get_cursor():
        conexao = ConexaoMySQL().conectar()
        if conexao:
            return conexao.cursor(dictionary=True), conexao
        return None, None

    @staticmethod
    def autenticar_usuario(email, senha_fornecida):
        """
        Busca e autentica o usuário no banco de dados usando validação de Hash.
        """
        cursor, _ = BancoDados._get_cursor()
        if not cursor: return None
        
        cursor.execute("SELECT * FROM usuarios WHERE email = %s LIMIT 1", (email,))
        r = cursor.fetchone()
        cursor.close()
        
        # se encontrou o usuário e o hash da senha bater
        if r and check_password_hash(r['senha'], senha_fornecida):
            return Usuario(
                nome=r.get('nome', 'Aluno'),
                curso=r.get('curso', ''),
                carga_horaria_total=r.get('carga_horaria_total', 0),
                semestres_totais=r.get('semestres_totais', 0),
                ira=r.get('ira', 0.0),
                semestres_cursados=r.get('semestres_cursados', 0),
                id=r.get('id')
            )
        return None

    @staticmethod
    def registrar_usuario(nome, email, senha_plana):
        """
        Insere um novo usuário no banco de dados com senha criptografada.
        """
        cursor, conexao = BancoDados._get_cursor()
        if not cursor: return False
        
        senha_hash = generate_password_hash(senha_plana)
        
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha, curso, carga_horaria_total, semestres_totais, ira, semestres_cursados) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (nome, email, senha_hash, '', 0, 0, 0.0, 0)
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
    def redefinir_senha(email, nova_senha_plana):
        """
        Atualiza a senha do usuário, garantindo a criptografia da nova senha.
        """
        cursor, conexao = BancoDados._get_cursor()
        if not cursor: return False
        
        nova_senha_hash = generate_password_hash(nova_senha_plana)
        
        try:
            cursor.execute("UPDATE usuarios SET senha = %s WHERE email = %s", (nova_senha_hash, email))
            conexao.commit()
            sucesso = cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao redefinir senha: {e}")
            sucesso = False
        finally:
            cursor.close()
            
        return sucesso
