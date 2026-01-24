SELECT      i.Name, v.Value
FROM        METADATAITEMS i
INNER JOIN  METADATAVALUES v ON v.metadata_item_id = i.id
WHERE       v.game_id = $GAME_ID;
