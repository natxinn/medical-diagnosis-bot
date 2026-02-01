import logging
import os
import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Import your cases
from cases import MEDICAL_CASES

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Read bot token from environment variable (for Railway) or file
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    try:
        with open('bot_token.txt', 'r') as f:
            BOT_TOKEN = f.read().strip()
    except:
        logger.error("No BOT_TOKEN found in environment or file")

# Store user games and leaderboard
user_games = {}
leaderboard = {}

def get_weekly_case():
    """Get cases in persistent sequential order - tied to calendar"""
    # Calculate the start of this week (Monday)
    now = datetime.now()
    days_since_monday = now.weekday()  # 0=Monday, 1=Tuesday, etc.
    start_of_week = now - timedelta(days=days_since_monday)
    
    # Get all case keys
    all_cases = list(MEDICAL_CASES.keys())
    if not all_cases:
        logger.error("No medical cases found!")
        return None
    
    # Use fixed reference date for consistent sequencing
    # This ensures order persists through code updates and server restarts
    reference_date = datetime(2024, 1, 1)  # Fixed anchor point
    weeks_since_reference = (start_of_week - reference_date).days // 7
    
    # Calculate which case to show this week
    case_index = weeks_since_reference % len(all_cases)
    
    case_key = all_cases[case_index]
    logger.info(f"Week starting {start_of_week.strftime('%Y-%m-%d')}: Showing case {case_index + 1}/{len(all_cases)} - {case_key}")
    return MEDICAL_CASES[case_key]

def evaluate_guess(guess, diagnosis):
    """Wordle-style evaluation - NOT case sensitive"""
    guess = guess.upper()  # Convert to uppercase for comparison
    diagnosis = diagnosis.upper()
    
    result = []
    
    for i in range(len(guess)):
        if i >= len(diagnosis):
            result.append('🟥')
        elif guess[i] == diagnosis[i]:
            result.append('🟩')
        elif guess[i] in diagnosis:
            result.append('🟨')
        else:
            result.append('🟥')
    
    # REMOVE SPACES between boxes - join without spaces
    return ''.join(result)

def update_leaderboard(user_id, username, attempts, won=True):
    """Update weekly leaderboard"""
    now = datetime.now()
    days_since_monday = now.weekday()
    start_of_week = now - timedelta(days=days_since_monday)
    week_key = start_of_week.strftime("%Y-%m-%d")
    
    if week_key not in leaderboard:
        leaderboard[week_key] = {}
    
    if user_id not in leaderboard[week_key]:
        leaderboard[week_key][user_id] = {
            'username': username,
            'attempts': attempts if won else 6,
            'won': won,
            'timestamp': datetime.now()
        }
    elif won and attempts < leaderboard[week_key][user_id]['attempts']:
        # Update if they won with fewer attempts
        leaderboard[week_key][user_id]['attempts'] = attempts
        leaderboard[week_key][user_id]['won'] = True
        leaderboard[week_key][user_id]['timestamp'] = datetime.now()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    case = get_weekly_case()
    if not case:
        await update.message.reply_text("❌ Medical cases are currently unavailable. Please try again later.")
        return
    
    user_games[user_id] = {
        'case': case,
        'attempts': 0,
        'diagnosis': case['diagnosis'],
        'started_at': datetime.now()
    }
    
    # Calculate letter count for this week's diagnosis
    letter_count = len(case['diagnosis'])
    
    welcome_text = f"""
🏥 *BIWEEKLY CLINICLE CASE* 🏥

{case['case_text']}

🎯 *GUESS THE DIAGNOSIS!*
• The answer has {letter_count} letters
• You have 6 attempts
• Type the full diagnosis name
• NOT case sensitive - "diabetes" works!
• Get color feedback: 🟩🟨🟥

📊 Use /leaderboard to see case rankings!
/help to find out how to play!

Enter your first guess:
    """
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def handle_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    guess = update.message.text.strip()  # Don't convert to upper yet
    
    if user_id not in user_games:
        await update.message.reply_text("Please start a game with /start first!")
        return
    
    game = user_games[user_id]
    game['attempts'] += 1
    
    # Case insensitive comparison
    feedback = evaluate_guess(guess, game['diagnosis'])
    
    result_text = f"""
🎯 *Attempt {game['attempts']}/6*

Your guess: {guess}
Feedback: {feedback}
    """
    
    # Case insensitive win condition
    if guess.upper() == game['diagnosis'].upper():
        update_leaderboard(user_id, user.username or user.first_name, game['attempts'], won=True)
        
        victory_text = f"""
🎉 *CONGRATULATIONS!* 🎉

You correctly diagnosed: *{game['diagnosis']}*
Attempts: {game['attempts']}/6

🏆 Added to the leaderboard!
Use /leaderboard to see rankings.

        """
        del user_games[user_id]
        await update.message.reply_text(victory_text, parse_mode='Markdown')
    
    elif game['attempts'] >= 6:
        update_leaderboard(user_id, user.username or user.first_name, game['attempts'], won=False)
        
        game_over_text = f"""
💡 *GAME OVER*

The correct diagnosis was: *{game['diagnosis']}*

Better luck next time! 
        """
        del user_games[user_id]
        await update.message.reply_text(game_over_text, parse_mode='Markdown')
    
    else:
        await update.message.reply_text(result_text, parse_mode='Markdown')

async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show weekly leaderboard"""
    now = datetime.now()
    days_since_monday = now.weekday()
    start_of_week = now - timedelta(days=days_since_monday)
    week_key = start_of_week.strftime("%Y-%m-%d")
    
    if week_key not in leaderboard or not leaderboard[week_key]:
        await update.message.reply_text("🏆 No leaderboard data for this week yet. Be the first to play!")
        return
    
    # Get current week's leaderboard
    week_data = leaderboard[week_key]
    
    # Sort by attempts (fewer = better) and then by timestamp
    sorted_players = sorted(
        week_data.items(),
        key=lambda x: (x[1]['attempts'] if x[1]['won'] else 999, x[1]['timestamp'])
    )
    
    leaderboard_text = f"🏆 *LEADERBOARD* 🏆\n"
    leaderboard_text += f"*Week starting {start_of_week.strftime('%b %d')}*\n\n"
    
    for i, (user_id, data) in enumerate(sorted_players[:10], 1):  # Top 10
        status = "✅" if data['won'] else "❌"
        username = data['username'] or f"Player {i}"
        leaderboard_text += f"{i}. {username} {status}\n"
        leaderboard_text += f"   Attempts: {data['attempts']}/6\n\n"
    
    leaderboard_text += "🔄 Resets after every case"
    
    await update.message.reply_text(leaderboard_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🆘 *BIWEEKLY CLINICLE CASE - HELP*

🎮 *HOW TO PLAY*:
1. Use /start to begin case
2. Read the medical case presentation
3. Guess the full diagnosis name
4. NOT case sensitive - type naturally!
5. Get color feedback on your guess
6. You have 6 attempts

🎯 *COLOR MEANING*:
🟩 = Correct letter in correct position
🟨 = Correct letter in wrong position  
🟥 = Incorrect letter

📏 *ANSWER LENGTH*:
• Each case shows how many letters in the answer

🏆 *LEADERBOARD*:
• Use /leaderboard to see rankings
• Fewer attempts = better ranking
• Resets every 2 weeks

🔄 *BIWEEKLY RESET*:
• New case drops on Monday
• Same case for all players all week
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

def main():
    if not BOT_TOKEN:
        logger.error("No BOT_TOKEN provided. Bot cannot start.")
        return
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("leaderboard", leaderboard_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_guess))
    
    logger.info("🟢 Medical Diagnosis Bot is starting...")
    logger.info(f"📅 Today's date: {datetime.now().strftime('%Y-%m-%d')}")
    logger.info(f"🏥 Available cases: {len(MEDICAL_CASES)}")
    application.run_polling()

if __name__ == '__main__':
    main()



