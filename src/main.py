from datetime import datetime, timedelta
import os
import time
import config
from image_downloader import verificar_imagem_disponivel, baixar_e_salvar_imagem, construir_url
from email_sender import enviar_email_comparacao

def main():
    """
    Função principal que executa o processo de verificação e envio de emails de comparação de mapas.

    Verifica se os mapas das horas especificadas estão disponíveis, baixa e salva as imagens,
    e envia um email de comparação se o mapa atual e o mapa anterior estiverem disponíveis.
    """
    horas = ["00", "06", "12", "18"]
    emails_destino = config.EMAIL_RECIPIENTS
    imagens_enviadas = set()
    os.makedirs(config.MAPS_DIR, exist_ok=True)

    def verificar_e_baixar_imagem(data, hora):
        """
        Verifica se a imagem do mapa está disponível e baixa se ainda não existir localmente.

        Args:
            data (datetime): A data para a qual verificar e baixar a imagem.
            hora (str): A hora para a qual verificar e baixar a imagem.

        Returns:
            str: O caminho da imagem baixada se disponível e baixada com sucesso, caso contrário, None.
        """
        data_str = data.strftime('%Y%m%d')
        caminho_imagem_atual = os.path.join(config.MAPS_DIR, f"map_{data_str}_{hora}.png")
        if not os.path.exists(caminho_imagem_atual):
            url_atual = construir_url(data, hora)
            if verificar_imagem_disponivel(url_atual) and baixar_e_salvar_imagem(url_atual, caminho_imagem_atual):
                return caminho_imagem_atual
            else:
                print(f"Mapa ainda indisponível: {url_atual}")
                return None
        else:
            print(f"Mapa já existe: {caminho_imagem_atual}")
            return None  # Retorna None se o mapa já existe

    def enviar_email_comparacao_mapa(data_atual, hora_atual):
        """
        Envia um email de comparação de mapas se ambos, o mapa atual e o anterior, estiverem disponíveis.

        Args:
            data_atual (datetime): A data atual para a qual verificar e enviar a comparação.
            hora_atual (str): A hora atual para a qual verificar e enviar a comparação.

        Returns:
            None
        """
        if hora_atual == "00":
            data_anterior = data_atual - timedelta(days=1)
            hora_anterior = "18"
        else:
            data_anterior = data_atual
            hora_anterior = horas[horas.index(hora_atual) - 1]

        caminho_imagem_atual = verificar_e_baixar_imagem(data_atual, hora_atual)
        if not caminho_imagem_atual:
            return  # Não envia o email se o mapa atual já existe

        caminho_imagem_anterior = os.path.join(config.MAPS_DIR, f"map_{data_anterior.strftime('%Y%m%d')}_{hora_anterior}.png")

        if os.path.exists(caminho_imagem_anterior):
            identificador = f"{data_atual.strftime('%Y%m%d')}_{hora_atual}"
            if identificador not in imagens_enviadas:
                enviar_email_comparacao(caminho_imagem_anterior, caminho_imagem_atual, emails_destino, hora_atual, config)
                print(f"Comparação de mapas enviada: {caminho_imagem_anterior} vs {caminho_imagem_atual}")
                imagens_enviadas.add(identificador)

    while True:
        for hora in horas:
            enviar_email_comparacao_mapa(datetime.utcnow(), hora)
        print(f"Aguardando 5 minutos antes da próxima tentativa...")
        time.sleep(300)  # Aguarda 5 minutos antes de tentar novamente

if __name__ == "__main__":
    main()
