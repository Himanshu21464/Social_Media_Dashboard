-- ------------------Standardize the video duration of Twitch -------------------
-- Step 1: Add a new column with the desired datatype
use twitch;
ALTER TABLE twitch_videos
ADD COLUMN new_duration TIME;

-- Step 2: Update the new column with the formatted durations
UPDATE twitch_videos
SET new_duration = CASE
    WHEN duration REGEXP '^[0-9]+h[0-9]+m[0-9]+s$' THEN TIME_FORMAT(
        CONCAT(
            SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'h', 1), 'h', -1),
            ':',
            SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'm', 1), 'h', -1),
            ':',
            SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 's', 1), 'm', -1)
        ),
        '%H:%i:%s'
    )
    WHEN duration REGEXP '^[0-9]+m[0-9]+s$' THEN TIME_FORMAT(
        CONCAT(
            '00:',
            SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 'm', 1), 'm', -1),
            ':',
            SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 's', 1), 'm', -1)
        ),
        '%H:%i:%s'
    )
    WHEN duration REGEXP '^[0-9]+s$' THEN TIME_FORMAT(
        CONCAT(
            '00:00:',
            SUBSTRING_INDEX(SUBSTRING_INDEX(duration, 's', 1), 's', -1)
        ),
        '%H:%i:%s'
    )
    ELSE duration
END;

select * from twitch_videos;
-- Step 3: Drop the old column (if needed)
ALTER TABLE twitch_videos
DROP COLUMN duration;

-- Step 4: Rename the new column to the original column name
ALTER TABLE twitch_videos
CHANGE COLUMN new_duration duration TIME;

-- ---------------Standardize the video duration of Dailymotion -----------------

-- Step 1: Add a new column with the desired datatype
use dailymotion;
ALTER TABLE dailymotion_videos
ADD COLUMN new_duration TIME;

-- Step 2: Update the new column with the formatted durations
UPDATE dailymotion_videos
SET new_duration = SEC_TO_TIME(duration);

-- Step 3: Drop the old column (if needed)
ALTER TABLE dailymotion_videos
DROP COLUMN duration;

-- Step 4: Rename the new column to the original column name
ALTER TABLE dailymotion_videos
CHANGE COLUMN new_duration duration TIME;


