SELECT      g.Id,
            CASE wp.Name WHEN '$NAME' THEN 'White' ELSE 'Black' END AS "Colour"
FROM        GAMES g
INNER JOIN  PLAYERS wp ON wp.id = g.white_player_id
INNER JOIN  PLAYERS bp ON bp.id = g.black_player_id
WHERE       wp.Name = '$NAME'
OR          bp.Name = '$NAME';
