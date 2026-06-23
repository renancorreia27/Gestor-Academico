from database.conexao import ConexaoMySQL
from models import Usuario, Semestre, Materia, Nota
from werkzeug.security import generate_password_hash, check_password_hash

class BancoDados:    
    @staticmethod
    def inicializar_banco():
        """Cria as tabelas necessárias caso elas não existam."""
        cursor, conexao = BancoDados._get_cursor()
        if not cursor: return
        
        try:
            try:
                cursor.execute("ALTER TABLE usuarios ADD COLUMN instituicao VARCHAR(255) DEFAULT ''")
            except Exception:
                pass
            try:
                cursor.execute("ALTER TABLE usuarios ADD COLUMN meta_ira DECIMAL(5,2) DEFAULT 0.0")
            except Exception:
                pass
            
            # Tabela de Semestres
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS semestres (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    usuario_id INT NOT NULL,
                    nome VARCHAR(255) NOT NULL,
                    situacao VARCHAR(255) DEFAULT 'Não Iniciado',
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
                )
            """)
            
            # Tabela de Materias
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS materias (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    semestre_id INT NOT NULL,
                    nome VARCHAR(255) NOT NULL,
                    carga_horaria INT DEFAULT 0,
                    media DECIMAL(5, 2) DEFAULT 0.0,
                    faltas INT DEFAULT 0,
                    max_faltas INT DEFAULT 20,
                    media_necessaria DECIMAL(5, 2) DEFAULT 7.0,
                    FOREIGN KEY (semestre_id) REFERENCES semestres(id) ON DELETE CASCADE
                )
            """)
            
            # Tabela de Notas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    materia_id INT NOT NULL,
                    valor DECIMAL(5, 2) NOT NULL,
                    peso DECIMAL(5, 2) NOT NULL,
                    FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE
                )
            """)
            
            conexao.commit()
        except Exception as e:
            print(f"Erro ao inicializar banco: {e}")
        finally:
            cursor.close()

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
                id=r.get('id'),
                instituicao=r.get('instituicao', ''),
                meta_ira=float(r.get('meta_ira', 0.0)) if r.get('meta_ira') else 0.0
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
            cursor.execute(
                "UPDATE usuarios SET senha = %s WHERE email = %s",
                (nova_senha_hash, email)
            )
            conexao.commit()
            sucesso = cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao redefinir senha: {e}")
            sucesso = False
        finally:
            cursor.close()
            
        return sucesso

    @staticmethod
    def obter_usuario(usuario_id):
        cursor, _ = BancoDados._get_cursor()
        if not cursor: return None
        
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))
        r = cursor.fetchone()
        cursor.close()
        
        if r:
            return Usuario(
                nome=r.get('nome', 'Aluno'),
                curso=r.get('curso', ''),
                carga_horaria_total=r.get('carga_horaria_total', 0),
                semestres_totais=r.get('semestres_totais', 0),
                ira=r.get('ira', 0.0),
                semestres_cursados=r.get('semestres_cursados', 0),
                id=r.get('id'),
                instituicao=r.get('instituicao', ''),
                meta_ira=float(r.get('meta_ira', 0.0)) if r.get('meta_ira') else 0.0
            )
        return None

    @staticmethod
    def atualizar_perfil(usuario_id, instituicao, curso, semestres_totais, carga_horaria_total, meta_ira):
        cursor, conexao = BancoDados._get_cursor()
        if not cursor: return False
        
        try:
            cursor.execute(
                """UPDATE usuarios 
                   SET instituicao=%s, curso=%s, semestres_totais=%s, carga_horaria_total=%s, meta_ira=%s
                   WHERE id=%s""",
                (instituicao, curso, semestres_totais, carga_horaria_total, meta_ira, usuario_id)
            )
            conexao.commit()
            sucesso = True
        except Exception as e:
            print(f"Erro ao atualizar perfil: {e}")
            sucesso = False
        finally:
            cursor.close()
        return sucesso

    # --- DAOs para Semestres ---

    @staticmethod
    def listar_semestres(usuario_id):
        cursor, _ = BancoDados._get_cursor()
        if not cursor: return []
        
        cursor.execute("SELECT * FROM semestres WHERE usuario_id = %s", (usuario_id,))
        resultados = cursor.fetchall()
        cursor.close()
        
        return [Semestre(nome=r['nome'], situacao=r['situacao'], id=r['id']) for r in resultados]

    @staticmethod
    def criar_semestre(usuario_id, nome, situacao="Não Iniciado"):
        cursor, conexao = BancoDados._get_cursor()
        if not cursor: return False
        
        try:
            cursor.execute(
                "INSERT INTO semestres (usuario_id, nome, situacao) VALUES (%s, %s, %s)",
                (usuario_id, nome, situacao)
            )
            conexao.commit()
            sucesso = cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao criar semestre: {e}")
            sucesso = False
        finally:
            cursor.close()
        return sucesso

    @staticmethod
    def deletar_semestre(semestre_id):
        cursor, conexao = BancoDados._get_cursor()
        if not cursor: return False
        
        try:
            cursor.execute("DELETE FROM semestres WHERE id = %s", (semestre_id,))
            conexao.commit()
            sucesso = cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao deletar semestre: {e}")
            sucesso = False
        finally:
            cursor.close()
        return sucesso

    # --- DAOs para Matérias ---

    @staticmethod
    def atualizar_status_semestre(semestre_id, situacao):
        cursor, conn = BancoDados._get_cursor()
        if not cursor: return
        cursor.execute("UPDATE semestres SET situacao = %s WHERE id = %s", (situacao, semestre_id))
        conn.commit()
        cursor.close()

    @staticmethod
    def calcular_ira_geral(usuario_id):
        cursor, conn = BancoDados._get_cursor()
        if not cursor: return 0.0
        query = """
            SELECT m.media, m.carga_horaria 
            FROM materias m
            JOIN semestres s ON m.semestre_id = s.id
            WHERE s.usuario_id = %s
        """
        cursor.execute(query, (usuario_id,))
        materias = cursor.fetchall()
        cursor.close()
        
        total_produto = 0
        total_carga = 0
        for m in materias:
            total_produto += m['media'] * m['carga_horaria']
            total_carga += m['carga_horaria']
        
        if total_carga == 0:
            return 0.0
        return total_produto / total_carga

    @staticmethod
    def listar_materias(semestre_id):
        cursor, _ = BancoDados._get_cursor()
        if not cursor: return []
        
        cursor.execute("SELECT * FROM materias WHERE semestre_id = %s", (semestre_id,))
        resultados = cursor.fetchall()
        
        materias = []
        for r in resultados:
            mat = Materia(
                nome=r['nome'],
                semestre='', # Será preenchido na view se necessário
                carga_horaria=r['carga_horaria'],
                media=float(r['media']),
                faltas=r['faltas'],
                max_faltas=r['max_faltas'],
                media_necessaria=float(r['media_necessaria']),
                id=r['id'],
                semestre_id=r['semestre_id']
            )
            
            # Buscar as notas da matéria
            cursor.execute("SELECT * FROM notas WHERE materia_id = %s", (mat.id,))
            notas_db = cursor.fetchall()
            for n in notas_db:
                mat.notas.append(Nota(float(n['valor']), float(n['peso'])))
            
            materias.append(mat)
            
        cursor.close()
        return materias

    @staticmethod
    def adicionar_materia(semestre_id, nome, carga_horaria, max_faltas, media_necessaria):
        cursor, conexao = BancoDados._get_cursor()
        if not cursor: return False
        
        try:
            cursor.execute(
                "INSERT INTO materias (semestre_id, nome, carga_horaria, max_faltas, media_necessaria) VALUES (%s, %s, %s, %s, %s)",
                (semestre_id, nome, carga_horaria, max_faltas, media_necessaria)
            )
            conexao.commit()
            sucesso = cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao adicionar matéria: {e}")
            sucesso = False
        finally:
            cursor.close()
        return sucesso

    @staticmethod
    def excluir_materia(materia_id):
        cursor, conn = BancoDados._get_cursor()
        if not cursor: return
        cursor.execute("DELETE FROM materias WHERE id = %s", (materia_id,))
        conn.commit()
        cursor.close()

    @staticmethod
    def editar_materia(materia_id, nome, carga_horaria, max_faltas, media_necessaria):
        cursor, conexao = BancoDados._get_cursor()
        if not cursor: return False
        
        try:
            cursor.execute(
                "UPDATE materias SET nome=%s, carga_horaria=%s, max_faltas=%s, media_necessaria=%s WHERE id=%s",
                (nome, carga_horaria, max_faltas, media_necessaria, materia_id)
            )
            conexao.commit()
            sucesso = cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao editar matéria: {e}")
            sucesso = False
        finally:
            cursor.close()
        return sucesso

    @staticmethod
    def deletar_materia(materia_id):
        cursor, conexao = BancoDados._get_cursor()
        if not cursor: return False
        
        try:
            cursor.execute("DELETE FROM materias WHERE id = %s", (materia_id,))
            conexao.commit()
            sucesso = cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao deletar matéria: {e}")
            sucesso = False
        finally:
            cursor.close()
        return sucesso

    @staticmethod
    def adicionar_falta(materia_id, qtd):
        cursor, conexao = BancoDados._get_cursor()
        if not cursor: return False
        
        try:
            cursor.execute("UPDATE materias SET faltas = faltas + %s WHERE id = %s", (qtd, materia_id))
            conexao.commit()
            sucesso = cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao adicionar falta: {e}")
            sucesso = False
        finally:
            cursor.close()
        return sucesso

    @staticmethod
    def adicionar_nota(materia_id, valor, peso):
        cursor, conexao = BancoDados._get_cursor()
        if not cursor: return False
        
        try:
            cursor.execute("INSERT INTO notas (materia_id, valor, peso) VALUES (%s, %s, %s)", (materia_id, valor, peso))
            conexao.commit()
            sucesso = cursor.rowcount > 0
            
            # Recalcular média (simplificado, mas ideal seria no banco ou classe)
            cursor.execute("SELECT * FROM notas WHERE materia_id = %s", (materia_id,))
            notas = cursor.fetchall()
            soma_pesos = sum(float(n['peso']) for n in notas)
            if soma_pesos > 0:
                soma_ponderada = sum(float(n['valor']) * float(n['peso']) for n in notas)
                media = soma_ponderada / soma_pesos
                cursor.execute("UPDATE materias SET media = %s WHERE id = %s", (media, materia_id))
                conexao.commit()
            
        except Exception as e:
            print(f"Erro ao adicionar nota: {e}")
            sucesso = False
        finally:
            cursor.close()
        return sucesso
