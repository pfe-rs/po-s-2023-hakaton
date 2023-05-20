from common import execute_command
import sys

bot = sys.argv[1]

print("removing bot ", bot)

execute_command("delete from runs where bot1 = ? or bot2 = ?", (bot, bot))

execute_command("delete from rankings where bot = ?", (bot,))
