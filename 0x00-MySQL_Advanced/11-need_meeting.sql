-- Creates a view that lists students who need a meeting
-- Criteria: score < 80 AND (no last_meeting OR last_meeting was over a month ago)

DROP VIEW IF EXISTS need_meeting;

CREATE VIEW need_meeting AS
SELECT name
FROM students
WHERE score < 80
  AND (
        last_meeting IS NULL
        OR last_meeting < CURDATE() - INTERVAL 1 MONTH
);
