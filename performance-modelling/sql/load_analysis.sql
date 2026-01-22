SELECT      m.game_id,
            ae.name as "engine",
            0 as "depth",
            m.halfmove,
            m.san,
            a.previous_score,
            a.score,
            a.cpl,
            a.win_percent,
            a.accuracy,
            a.evaluation,
            a.annotation
FROM        MOVES m
INNER JOIN  ANALYSIS a ON a.Move_Id = m.Id
INNER JOIN  ANALYSISENGINES ae ON ae.Id = a.Analysis_Engine_Id
WHERE       m.Game_Id = $GAME_ID
AND         ae.Name LIKE '%$ENGINE%';
