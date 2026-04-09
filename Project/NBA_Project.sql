-- Create the database
CREATE DATABASE IF NOT EXISTS NBA_Project;
USE NBA_Project;

-- ============================
-- TEAMS TABLE
-- ============================
CREATE TABLE Teams (
    TeamID INT AUTO_INCREMENT PRIMARY KEY,
    TeamName VARCHAR(100) NOT NULL,
    City VARCHAR(100) NOT NULL
);

-- ============================
-- PLAYERS TABLE
-- ============================
CREATE TABLE Players (
    PlayerID INT AUTO_INCREMENT PRIMARY KEY,
    PlayerName VARCHAR(100) NOT NULL,
    Position VARCHAR(20),
    TeamID INT,
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

-- ============================
-- PLAYER STATS TABLE
-- ============================
CREATE TABLE PlayerStats (
    StatID INT AUTO_INCREMENT PRIMARY KEY,
    PlayerID INT NOT NULL,
    GamesPlayed INT,
    Points INT,
    Assists INT,
    Rebounds INT,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);