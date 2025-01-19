CREATE DATABASE music_management;
USE music_management;

CREATE TABLE Albums (
    album_title VARCHAR(50) PRIMARY KEY,
    artist VARCHAR(100)
);

ALTER TABLE Albums DROP album_duration;
CREATE TABLE Tracks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    track_title VARCHAR(50),
    mp3_file VARCHAR(50),
    duration VARCHAR(10),
    album_title VARCHAR(50),
    FOREIGN KEY (album_title) REFERENCES Albums(album_title) ON DELETE CASCADE
);

CREATE INDEX idx_album_title ON Tracks (album_title);
CREATE INDEX idx_album_title_track_title ON Tracks (album_title, track_title);

INSERT INTO Albums (album_title, artist, album_duration) VALUES
    ('Album 1', 'Artist 1', '00:41:25'),
    ('Album 2', 'Artist 2', '00:40:25'),
    ('Album 3', 'Artist 3', '00:57:25'),
    ('Album 4', 'Artist 4', '00:50:10'),
    ('Album 5', 'Artist 5', '01:00:45');
    
INSERT INTO Tracks (track_title, mp3_file, duration, album_title) VALUES
    ('Track 1', 'track1.mp3', '04:30', 'Album 1'),
    ('Track 2', 'track2.mp3', '03:45', 'Album 1'),
    ('Track 3', 'track3.mp3', '04:00', 'Album 1'),
    ('Track 4', 'track4.mp3', '05:15', 'Album 1'),
    ('Track 5', 'track5.mp3', '04:20', 'Album 1'),
    ('Track 6', 'track6.mp3', '03:40', 'Album 1'),
    ('Track 7', 'track7.mp3', '03:50', 'Album 1'),
    ('Track 8', 'track8.mp3', '04:10', 'Album 1'),
    ('Track 9', 'track9.mp3', '04:00', 'Album 1'),
    ('Track 10', 'track10.mp3', '03:55', 'Album 1');

INSERT INTO Tracks (track_title, mp3_file, duration, album_title) VALUES
    ('Track 1', 'track1.mp3', '04:00', 'Album 2'),
    ('Track 2', 'track2.mp3', '03:50', 'Album 2'),
    ('Track 3', 'track3.mp3', '04:10', 'Album 2'),
    ('Track 4', 'track4.mp3', '04:20', 'Album 2'),
    ('Track 5', 'track5.mp3', '03:45', 'Album 2'),
    ('Track 6', 'track6.mp3', '03:55', 'Album 2'),
    ('Track 7', 'track7.mp3', '04:30', 'Album 2'),
    ('Track 8', 'track8.mp3', '03:40', 'Album 2'),
    ('Track 9', 'track9.mp3', '04:00', 'Album 2'),
    ('Track 10', 'track10.mp3', '04:15', 'Album 2');

INSERT INTO Tracks (track_title, mp3_file, duration, album_title) VALUES
    ('Track 1', 'track1.mp3', '06:00', 'Album 3'),
    ('Track 2', 'track2.mp3', '05:30', 'Album 3'),
    ('Track 3', 'track3.mp3', '05:00', 'Album 3'),
    ('Track 4', 'track4.mp3', '05:45', 'Album 3'),
    ('Track 5', 'track5.mp3', '06:10', 'Album 3'),
    ('Track 6', 'track6.mp3', '05:20', 'Album 3'),
    ('Track 7', 'track7.mp3', '05:35', 'Album 3'),
    ('Track 8', 'track8.mp3', '06:15', 'Album 3'),
    ('Track 9', 'track9.mp3', '05:50', 'Album 3'),
    ('Track 10', 'track10.mp3', '06:00', 'Album 3');

INSERT INTO Tracks (track_title, mp3_file, duration, album_title) VALUES
    ('Track 1', 'track1.mp3', '05:30', 'Album 4'),
    ('Track 2', 'track2.mp3', '05:00', 'Album 4'),
    ('Track 3', 'track3.mp3', '04:40', 'Album 4'),
    ('Track 4', 'track4.mp3', '05:10', 'Album 4'),
    ('Track 5', 'track5.mp3', '04:30', 'Album 4'),
    ('Track 6', 'track6.mp3', '05:00', 'Album 4'),
    ('Track 7', 'track7.mp3', '05:20', 'Album 4'),
    ('Track 8', 'track8.mp3', '05:15', 'Album 4'),
    ('Track 9', 'track9.mp3', '04:45', 'Album 4'),
    ('Track 10', 'track10.mp3', '05:00', 'Album 4');

INSERT INTO Tracks (track_title, mp3_file, duration, album_title) VALUES
    ('Track 1', 'track1.mp3', '06:20', 'Album 5'),
    ('Track 2', 'track2.mp3', '06:00', 'Album 5'),
    ('Track 3', 'track3.mp3', '05:40', 'Album 5'),
    ('Track 4', 'track4.mp3', '06:10', 'Album 5'),
    ('Track 5', 'track5.mp3', '05:55', 'Album 5'),
    ('Track 6', 'track6.mp3', '06:00', 'Album 5'),
    ('Track 7', 'track7.mp3', '06:15', 'Album 5'),
    ('Track 8', 'track8.mp3', '06:10', 'Album 5'),
    ('Track 9', 'track9.mp3', '05:45', 'Album 5'),
    ('Track 10', 'track10.mp3', '06:30', 'Album 5');
