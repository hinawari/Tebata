import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Fungsi untuk membuat soal matematika
def generate_addition_question():
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    question = f"{num1} + {num2} = "
    answer = num1 + num2
    return question, answer

def generate_subtraction_question():
    num1 = random.randint(1, 20)
    num2 = random.randint(1, num1)
    question = f"{num1} - {num2} = "
    answer = num1 - num2
    return question, answer

def generate_multiplication_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    question = f"{num1} x {num2} = "
    answer = num1 * num2
    return question, answer

def generate_division_question():
    num2 = random.randint(1, 10)
    answer = random.randint(1, 10)
    num1 = num2 * answer
    question = f"{num1} ÷ {num2} = "
    return question, answer

# Handler untuk perintah /start
async def start(update: Update, context: CallbackContext):
    # Reset nyawa dan jawaban
    context.user_data["nyawa"] = 3
    context.user_data["answer"] = None

    # Tampilkan menu pilihan soal
    await tampilkan_menu(update, context)

# Fungsi untuk menampilkan menu pilihan soal
async def tampilkan_menu(update: Update, context: CallbackContext):
    keyboard = [["1. Penjumlahan", "2. Pengurangan"], ["3. Perkalian", "4. Pembagian"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Pilih jenis soal:",
        reply_markup=reply_markup
    )

# Handler untuk memproses pilihan pengguna
async def handle_choice(update: Update, context: CallbackContext):
    choice = update.message.text
    if choice.startswith("1"):
        question, answer = generate_addition_question()
    elif choice.startswith("2"):
        question, answer = generate_subtraction_question()
    elif choice.startswith("3"):
        question, answer = generate_multiplication_question()
    elif choice.startswith("4"):
        question, answer = generate_division_question()
    else:
        await update.message.reply_text("Pilihan tidak valid. Silakan coba lagi.")
        return

    # Simpan jawaban dan reset nyawa
    context.user_data["answer"] = answer
    context.user_data["nyawa"] = 3
    await update.message.reply_text(f"Soal: {question}")

# Handler untuk memeriksa jawaban pengguna
async def check_answer(update: Update, context: CallbackContext):
    user_answer = update.message.text
    correct_answer = context.user_data.get("answer")
    nyawa = context.user_data.get("nyawa", 3)

    if correct_answer is None:
        await update.message.reply_text("Silakan pilih jenis soal terlebih dahulu.")
        return

    try:
        user_answer = int(user_answer)
        if user_answer == correct_answer:
            await update.message.reply_text("Benar! 🎉")
            await tampilkan_menu(update, context)  # Kembali ke menu
        else:
            nyawa -= 1
            context.user_data["nyawa"] = nyawa
            if nyawa > 0:
                await update.message.reply_text(f"Salah. Sisa nyawa: {nyawa}")
            else:
                await update.message.reply_text(f"Kesempatan habis. Jawaban yang benar adalah {correct_answer}.")
                await tampilkan_menu(update, context)  # Kembali ke menu
    except ValueError:
        await update.message.reply_text("Masukkan angka yang valid.")

# Fungsi utama untuk menjalankan bot
def main():
    # Ganti 'TOKEN_BOT_ANDA' dengan token bot Anda
    application = Application.builder().token("7785505694:AAErZKqMaHWzn-vULVmyNVmlnl61ODMe32o").build()

    # Tambahkan handler untuk perintah /start
    application.add_handler(CommandHandler("start", start))

    # Tambahkan handler untuk memproses pilihan pengguna
    application.add_handler(MessageHandler(filters.Text(["1. Penjumlahan", "2. Pengurangan", "3. Perkalian", "4. Pembagian"]), handle_choice))

    # Tambahkan handler untuk memeriksa jawaban pengguna
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer))

    # Jalankan bot
    application.run_polling()

if __name__ == "__main__":
    main()