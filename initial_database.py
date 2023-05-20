from common import execute_command

# run this script once to initialize sqlite database

execute_command("drop table if exists uploadedfiles")
execute_command("drop table if exists runs")
execute_command("drop table if exists rankings")
execute_command("drop table if exists gameplay")

execute_command("create table uploadedfiles(bot text, userpass text)")

# insert default bots like they are uploaded
execute_command("insert into uploadedfiles values ('dummy', 'admin')")
execute_command("insert into uploadedfiles values ('dummy5', 'admin')")
execute_command("insert into uploadedfiles values ('dummy_fail', 'admin')")

execute_command(
    "create table runs("
        "bot1 text, "
        "bot2 text, "
        "map text, "
        "added timestmap, "
        "runtime timestamp, "
        "run bool, "
        "score1 int, "
        "score2 int, "
        "primary key (bot1, bot2, map))")

execute_command(
    "create table rankings(bot text primary key, wins int, loses int, score int, rank float)")

execute_command(
    "create table gameplay("
        "bot1 text,"
        "bot2 text,"
        "map text,"
        "turn integer,"
        "state text, "
        "primary key (bot1, bot2, map, turn))"
)

