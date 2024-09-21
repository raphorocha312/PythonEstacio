import csv
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Função para ler os dados do arquivo CSV
def ler_boletos(arquivo):
    boletos = []
    with open(arquivo, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            boletos.append(row)
    return boletos

# Função para enviar email
def enviar_email(destinatario, assunto, corpo):
    remetente = "seu_email@example.com"  # Coloque seu email aqui
    senha = "sua_senha"  # Coloque sua senha aqui

    # Configurações do servidor SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remetente, senha)

    # Criar mensagem
    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = assunto
    mensagem.attach(MIMEText(corpo, 'plain'))

    # Enviar email
    server.send_message(mensagem)
    server.quit()

# Função para verificar vencimentos e enviar lembretes
def verificar_vencimentos(boletos):
    hoje = datetime.now()
    for boleto in boletos:
        data_vencimento = datetime.strptime(boleto['data_vencimento'], '%Y-%m-%d')
        if hoje > data_vencimento and not boleto['pago'].lower() == 'sim':
            enviar_email(boleto['email'], f'Lembrete: Vencimento de {boleto["descricao"]}', 
                          f'Você tem um boleto vencido: {boleto["descricao"]} no valor de {boleto["valor"]}.')
        elif hoje + timedelta(days=3) >= data_vencimento and not boleto['pago'].lower() == 'sim':
            enviar_email(boleto['email'], f'Pagamento próximo: {boleto["descricao"]}', 
                          f'Lembrete: O boleto {boleto["descricao"]} vencerá em 3 dias. Valor: {boleto["valor"]}.')

# Função principal
def main():
    boletos = ler_boletos('boletos.csv')
    verificar_vencimentos(boletos)

if __name__ == "__main__":
    main()
