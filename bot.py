import logging
import random
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Import your cases
from cases import MEDICAL_CASES

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Read bot token
with open('bot_token.txt', 'r') as f:
    BOT_TOKEN = f.read().strip()

# Store user games
user_games = {}

def get_daily_case():
    """Get the same case for all users each day"""
    # Use today's date to seed random (same for all users)
    random.seed(datetime.now().strftime("%Y-%m-%d"))
    case_key = random.choice(list(MEDICAL_CASES.keys()))
    return MEDICAL_CASES[case_key]

def evaluate_guess(guess, diagnosis):
    """Wordle-style evaluation"""
    guess = guess.upper()
    diagnosis = diagnosis.upper()
    
    result = []
    
    # Check each letter
    for i in range(len(guess)):
        if i >= len(diagnosis):
            result.append('🟥')  # Extra letters are wrong
        elif guess[i] == diagnosis[i]:
            result.append('🟩')  # Correct letter in correct position
        elif guess[i] in diagnosis:
            result.append('🟨')  # Correct letter in wrong position
        else:
            result.append('🟥')  # Wrong letter
    
    return ' '.join(result)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # Get today's case (same for all users)
    case = get_daily_case()
    
    # Initialize user game
    user_games[user_id] = {
        'case': case,
        'attempts': 0,
        'diagnosis': case['diagnosis'],
        'started_at': datetime.now()
    }
    
    welcome_text = f"""
🏥 DAILY DIAGNOSIS WORDLE 🏥

{case['case_text']}

🎯 GUESS THE DIAGNOSIS!
• You have 6 attempts
• Type the full diagnosis name
• Get color feedback: 🟩🟨🟥

Enter your first guess:
    """
    
    await update.message.reply_text(welcome_text)

async def handle_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    guess = update.message.text.strip().upper()
    
    # Check if user has an active game
    if user_id not in user_games:
        await update.message.reply_text("Please start a game with /start first!")
        return
    
    game = user_games[user_id]
    game['attempts'] += 1
    
    # Evaluate the guess
    feedback = evaluate_guess(guess, game['diagnosis'])
    
    result_text = f"""
🎯 Attempt {game['attempts']}/6

Your guess: {guess}
Feedback: {feedback}

{game['diagnosis']}  # Show the target word with feedback
    """
    
    # Check if won
    if guess == game['diagnosis']:
        victory_text = f"""
🎉 CONGRATULATIONS! 🎉

You correctly diagnosed: {game['diagnosis']}
Attempts: {game['attempts']}/6

Well done, Doctor! 🏥

Play again tomorrow for a new case!
        """
        del user_games[user_id]  # End game
        await update.message.reply_text(victory_text)
    
    # Check if lost
    elif game['attempts'] >= 6:
        game_over_text = f"""
💡 GAME OVER

The correct diagnosis was: {game['diagnosis']}

Better luck tomorrow! New case in 24 hours.
        """
        del user_games[user_id]  # End game
        await update.message.reply_text(game_over_text)
    
    else:
        await update.message.reply_text(result_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🆘 MEDICAL DIAGNOSIS WORDLE - HELP

🎮 HOW TO PLAY:
1. Use /start to begin daily case
2. Read the medical case presentation
3. Guess the full diagnosis name
4. Get color feedback on your guess
5. You have 6 attempts

🎯 COLOR MEANING:
🟩 = Correct letter in correct position
🟨 = Correct letter in wrong position  
🟥 = Incorrect letter

📝 EXAMPLE:
If diagnosis is "DIABETES MELLITUS"
Guess: "DIABETES INSULIN"
Feedback: 🟩🟩🟩🟩🟩🟩🟩 🟥🟥🟥🟥🟥🟥

🔄 DAILY RESET:
• New case every 24 hours
• Same case for all players
    """
    await update.message.reply_text(help_text)

def main():
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_guess))
    
    print("🟢 Medical Diagnosis Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()