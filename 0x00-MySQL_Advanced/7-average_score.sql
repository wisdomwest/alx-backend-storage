-- creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student
-- An average score can be a decimal

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE av_score FLOAT;
    SET av_score = (SELECT AVG(score) FROM corrections AS x WHERE x.user_id=user_id);
    UPDATE users SET average_score = av_score WHERE id=user_id;
END
$$
DELIMITER ;
