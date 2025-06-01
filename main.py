from shared import build_rag_chain
from telegram_bot import main as telegram_bot_main
import logging

logger = logging.getLogger(__name__)

def main():
    try:
        mode = input("Choose mode (cli/telegram): ").strip().lower()
        if mode == "cli":
            query_chain = build_rag_chain()
            print("Enhanced RAG system is ready. Type your query below:")
            while True:
                query = input(">> ")
                if query.lower() in ["exit", "quit"]:
                    print("\nExiting the RAG system.")
                    break
                
                result = query_chain(query)  
                print(result)
        elif mode == "telegram":
            telegram_bot_main()
        else:
            print("Invalid mode. Please choose 'cli' or 'telegram'.")
    except KeyboardInterrupt:
        print("\nExiting the RAG system.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print("An error occurred. Please check the logs for details.")


if __name__ == "__main__":
    main()