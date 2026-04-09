SELECT 
    p.PlayerName,
    s.Points,
    s.Assists,
    s.Rebounds,
    s.Steals,
    s.Blocks,
    s.Turnovers,
    s.TwoPtPct,
    s.ThreePtPct
FROM PlayerStats s
JOIN Players p USING (PlayerID)
ORDER BY s.Points DESC
LIMIT 100;