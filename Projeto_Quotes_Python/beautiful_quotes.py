import requests
from bs4 import BeautifulSoup
from conexao_ora import conectar_oracle
 
def coletar_e_salvar_citacoes():
    url = 'https://toscrape.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
 
    quotes_elements = soup.find_all('span', class_='text')
    author_elements = soup.find_all('small', class_='author')
 
    # Captura a senha no escopo principal para o input funcionar corretamente
    senha = input('Informe a senha do banco de dados para iniciar a raspagem: ')
    conn = conectar_oracle(password=senha)
    
    if not conn:
        print("Operação cancelada devido a falha na conexão com o banco.")
        return

    cursor = None
    try:
        cursor = conn.cursor()
        
        # Garante o mapeamento correto linha a linha
        for q, a in zip(quotes_elements, author_elements):
            texto = q.get_text()
            autor = a.get_text()
            
            cursor.execute(
                "INSERT INTO quote (quote_text, author_name) VALUES (:1, :2)",
                (texto, autor)
            )
        
        conn.commit()
        print("Todas as citações do site foram inseridas com sucesso no banco de dados!")
        
    except Exception as e:
        print(f"Erro ao salvar dados no Oracle: {e}")
        conn.rollback()
    finally:
        # Fecha os recursos de forma segura apenas se foram abertos
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    coletar_e_salvar_citacoes()
