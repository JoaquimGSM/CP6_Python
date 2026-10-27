import oracledb
import os

def conectar_oracle(password=None):
    user = "rm572208"
    dsn = "://fiap.com.br:1521/orcl"
    
    # Se não for passada por parâmetro, pede no terminal
    if not password:
        password = os.environ.get("ORACLE_DB_PASSWORD") or input('Informe sua senha do banco Oracle: ')
        
    try:
        conn = oracledb.connect(user=user, dsn=dsn, password=password)
        print('Conexão estabelecida com sucesso!')
        return conn
    except Exception as e:
        print(f'Erro ao conectar ao Oracle: {e}')
        return None
    
def testar_conexao():
    conn = conectar_oracle()
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT sysdate FROM dual') 
        resultado = cursor.fetchone()
        print(f'Teste ok: {resultado[0]}')
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print('Iniciando teste de conexão isolado...')
    testar_conexao()
