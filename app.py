import g4f
from datetime import datetime
import time

def salvar_conversa(mensagens):
    """Salva o histórico da conversa em um arquivo de texto"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"conversa_{timestamp}.txt", "w", encoding="utf-8") as f:
        for msg in mensagens:
            f.write(f"{msg['role']}: {msg['content']}\n")

def chat_ia():
    print("=== Chat com IA ===")
    print("Digite 'sair' para encerrar ou 'salvar' para guardar a conversa")
    print("--------------------")

    mensagens = []
    system_msg = {
        "role": "system",
        "content": "Você é um assistente virtual prestativo. Responda sempre em português do Brasil de forma clara e objetiva."
    }
    mensagens.append(system_msg)

    providers_to_try = [
        ('FreeGpt', g4f.Provider.FreeGpt),
        ('You', g4f.Provider.You),
        ('ChatAnywhere', g4f.Provider.ChatAnywhere)
    ]

    while True:
        user_input = input("\nVocê: ").strip()
        
        if user_input.lower() == "sair":
            if mensagens:
                salvar = input("\nDeseja salvar a conversa? (s/n): ").lower()
                if salvar == 's':
                    salvar_conversa(mensagens)
                    print("Conversa salva!")
            print("\nAté logo!")
            break
            
        if user_input.lower() == "salvar":
            salvar_conversa(mensagens)
            print("Conversa salva!")
            continue
            
        mensagens.append({"role": "user", "content": user_input})
        
        response = None
        for provider_name, provider in providers_to_try:
            try:
                print(f"\nTentando com {provider_name}...")
                time.sleep(5)  # Pausa de 5 segundos para evitar bloqueios
                response = g4f.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    provider=provider,
                    messages=mensagens,
                    stream=False
                )
                
                mensagens.append({"role": "assistant", "content": response})
                
                print("\nIA:", response)
                break
            except Exception as e:
                error_msg = str(e)
                print(f"\nErro ao comunicar com {provider_name}: {error_msg}")
                if "Unusual activity" in error_msg:
                    print("Acesso bloqueado temporariamente. Tentando com o próximo provedor.")
                else:
                    print("Tentando com o próximo provedor.")
                continue

        if response is None:
            print("\nNão foi possível obter uma resposta da IA. Tente novamente mais tarde.")

def main():
    try:
        chat_ia()
    except KeyboardInterrupt:
        print("\n\nChat encerrado pelo usuário.")
    except Exception as e:
        print(f"\nErro inesperado: {str(e)}")

if __name__ == "__main__":
    main()
