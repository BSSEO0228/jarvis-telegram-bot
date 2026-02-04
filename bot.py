import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 자비스 온라인!\n코인 тик커(BTC, SUI, ENS)를 보내봐.")

async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip().upper()
    await update.message.reply_text(f"📌 입력 확인: {text}\n(다음 단계에서 시세/지표 붙일 예정)")

def main():
    if not TOKEN:
        raise RuntimeError("환경변수 TELEGRAM_TOKEN 이 설정되지 않았음")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    # ✅ Railway 같은 환경에서 '안 죽게' 만드는 폴링 옵션
    app.run_polling(
        drop_pending_updates=True,
        poll_interval=2.0,
        timeout=30,
        read_timeout=30,
        write_timeout=30,
        connect_timeout=30,
        allowed_updates=Update.ALL_TYPES,
    )

if __name__ == "__main__":
    main()
