-- SELECT pg_size_pretty(pg_database_size('valorant_match_data'));

-- SELECT pg_size_pretty(pg_table_size('public.matches'));
-- SELECT pg_size_pretty(pg_table_size('public.complete_new_player_experience_details'));

-- select * from public.matches

-- select * from pg_stats where tablename= 'complete_new_player_experience_details'

select * from round_results


select * from public.kill_player_locations limit 100

select count(distinct(kill_id)) from public.kill_player_locations

SELECT
  table_name,
  pg_size_pretty(pg_table_size('public.' || table_name)) AS table_size
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY pg_table_size('public.' || table_name) DESC;


SELECT subject, COUNT(match_id) FROM players 
where match_id in 
(select match_id from public.matches
where date(to_timestamp (game_start_millis/1000))= '2025-02-24')
group by subject
order by count desc


select match_id from public.players where subject='3043bc0c-2d2a-5ace-85bb-5f5e8929849a'

select * from public.premier_match_info where premier_season_id is not NULL

select * from pg_stats where tablename= 'complete_new_player_experience_details'