import mysql.connector

def main():
    # 1. Connect to your MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # <-- your MySQL username (usually "root"))
        password="",  # <-- Enter your MySQL password
        database="NBA_Project"
    )

    cursor = connection.cursor()

    # 2. Write a SQL query
    query = """
        SELECT 
            Players.PlayerName,
            PlayerStats.Points,
            PlayerStats.Assists,
            PlayerStats.Rebounds,
            PlayerStats.Steals,
            PlayerStats.Blocks,
            PlayerStats.Turnovers,
            PlayerStats.TwoPtPct,
            PlayerStats.ThreePtPct
        FROM PlayerStats
        JOIN Players ON PlayerStats.PlayerID = Players.PlayerID
        ORDER BY PlayerStats.Points DESC
        LIMIT 10;
    """

    # 3. Execute the query
    cursor.execute(query)

    # 4. Fetch results
    results = cursor.fetchall()

    # 5. Print results to the command line
    print("\nTop 10 NBA Scorers 2024-2025 (with full stats):\n")
    for row in results:
        name, pts, ast, reb, stl, blk, tov, two, three = row
        print(f"{name:25} | PTS: {pts:4} | AST: {ast:4} | REB: {reb:4} | "
              f"STL: {stl:4} | BLK: {blk:4} | TOV: {tov:4} | "
              f"2P%: {two:.3f} | 3P%: {three:.3f}")

    # 6. Close connection
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()