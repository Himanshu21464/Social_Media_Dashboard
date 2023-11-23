USE dailymotion;
SELECT *FROM dailymotion_videos;

USE YouTube_Analytics;
SELECT *FROM YouTube;

use dailymotion;
SELECT *FROM dailymotion_videos;

use twitch;
select *from twitch_videos;

create database global_database;
use global_database;

CREATE VIEW social_media_Dashboard AS
SELECT
    'YouTube' AS Platform,
    Title AS Title,
    Description AS Description,
    Published AS Published_Date,
    Tag_Count AS Tag_Count,
    View_Count AS View_Count,
    like_Count AS Like_Count,
    Dislike_Count AS Dislike_Count,
    comment_Count AS Comment_Count,
    Reactions AS Reactions,
    Duration AS Duration,
    NULL AS username,  -- Placeholder for username
    NULL AS video_id,  -- Placeholder for video_id
    NULL AS url,      -- Placeholder for url
    NULL as Tags
FROM YouTube_Analytics.YouTube

UNION ALL

SELECT
    'DailyMotion' AS Platform,
    title AS Title,
    NULL AS Description,  -- Placeholder for Description
    created_time AS Published_Date,
    NULL AS Tag_Count,    -- Placeholder for Tag_Count
    views_total AS View_Count,
    likes_total AS Like_Count,
    NULL AS Dislike_Count,  -- Placeholder for Dislike_Count
    NULL AS Comment_Count,  -- Placeholder for Comment_Count
    rating as Reactions,
    duration as duration,
    tags AS Tags,
    NULL AS username,  -- Placeholder for username
    NULL AS video_id,  -- Placeholder for video_id
    NULL AS url       -- Placeholder for url
FROM dailymotion.dailymotion_videos

UNION ALL

SELECT
    'Twitch' AS Platform,
    title AS Title,
    description as Description,
    published_at as Published_Date,
    NULL AS Tag_Count,  -- Placeholder for Tag_Count
    views AS View_Count,
    NULL AS Like_Count,  -- Placeholder for Like_Count
    NULL AS Dislike_Count,  -- Placeholder for Dislike_Count
    NULL AS Comment_Count,  -- Placeholder for Comment_Count
    duration as duration,
    NULL AS Tags,  -- Placeholder for Tags
    url as url,
    username as username,
    video_id as video_id,
    NULL as Reactions
    
FROM twitch.twitch_videos;
select *from social_media_Dashboard;
