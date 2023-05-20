from common import execute_command, execute_query

def printList(name, list):
    print(name)
    for l in list:
        print("  ", l)

def printTable(name):
    results = execute_query(f"select * from {name}")
    printList(name, results)

printTable("uploadedfiles")
printTable("runs")
printTable("rankings")
# printTable("gameplay")

# execute_command("delete from uploadedfiles")
# execute_command("delete from runs")
# execute_command("delete from rankings")
# execute_command("delete from gameplay")
