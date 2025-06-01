import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from shared import build_rag_chain

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I'm your assistant. Ask me anything!")

async def handle_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.message.text
    try:
        query_chain = build_rag_chain()
        result = query_chain(query)
        await update.message.reply_text(result)
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        await update.message.reply_text("An error occurred. Please try again later.")

def main():
    application = ApplicationBuilder().token("7945089308:AAHhiXGDA8I7yXL38XcSOIYFOYmG9De-umw").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_query))

    logger.info("Telegram bot is running...")
    application.run_polling()