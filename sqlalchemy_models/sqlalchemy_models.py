from sqlalchemy import (
    Column,
    String,
    Integer,
    BigInteger,
    Boolean,
    Float,
    Text,
    ForeignKey,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Table: matches
class Matches(Base):
    __tablename__ = "matches"
    match_id = Column(Text, primary_key=True)
    map_id = Column(Text)
    game_pod_id = Column(Text)
    game_loop_zone = Column(Text)
    game_server_address = Column(Text)
    game_version = Column(Text)
    game_length_millis = Column(BigInteger)
    game_start_millis = Column(BigInteger)
    provisioning_flow_id = Column(Text)
    is_completed = Column(Boolean)
    custom_game_name = Column(Text)
    force_post_processing = Column(Boolean)
    queue_id = Column(Text)
    game_mode = Column(Text)
    is_ranked = Column(Boolean)
    is_match_sampled = Column(Boolean)
    season_id = Column(Text)
    completion_state = Column(Text)
    platform_type = Column(Text)
    should_match_disable_penalties = Column(Boolean)
    region = Column(Text)


# Table: premier_match_info
class PremierMatchInfo(Base):
    __tablename__ = "premier_match_info"
    match_id = Column(Text, ForeignKey("matches.match_id"), primary_key=True)
    premier_season_id = Column(Text)
    premier_event_id = Column(Text)


# Table: party_rr_penalties
class PartyRRPenalties(Base):
    __tablename__ = "party_rr_penalties"
    match_id = Column(Text, ForeignKey("matches.match_id"))
    party_id = Column(Text)
    penalty_value = Column(Float)
    __table_args__ = (
        PrimaryKeyConstraint("match_id", "party_id", name="party_rr_penalties_pk"),
    )


# Table: coaches
class Coaches(Base):
    __tablename__ = "coaches"
    match_id = Column(Text, ForeignKey("matches.match_id"))
    coach = Column(Text)
    __table_args__ = (
        PrimaryKeyConstraint("match_id", "coach", name="coaches_pk"),
    )


# Table: kills
class Kills(Base):
    __tablename__ = "kills"
    kill_id = Column(BigInteger, primary_key=True, autoincrement=True)
    match_id = Column(Text, ForeignKey("matches.match_id"))
    game_time = Column(Integer)
    round_time = Column(Integer)
    round_num = Column(Integer)
    killer = Column(Text)
    victim = Column(Text)
    __table_args__ = (
        PrimaryKeyConstraint("kill_id", name="kills_pk"),
    )


# Table: kill_victim_locations
class KillVictimLocations(Base):
    __tablename__ = "kill_victim_locations"
    kill_id = Column(BigInteger)
    match_id = Column(Text)
    x = Column(Integer)
    y = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint("kill_id", "match_id", name="kill_victim_locations_pk"),
        ForeignKeyConstraint(
            ["kill_id"],
            ["kills.kill_id"],
            name="fk_kill_victim_locations_kills",
        ),
    )


# Table: kill_assistants
class KillAssistants(Base):
    __tablename__ = "kill_assistants"
    kill_id = Column(BigInteger)
    match_id = Column(Text)
    assistant = Column(Text)
    __table_args__ = (
        PrimaryKeyConstraint("kill_id", "assistant", name="kill_assistants_pk"),
        ForeignKeyConstraint(
            ["kill_id"],
            ["kills.kill_id"],
            name="fk_kill_assistants_kills",
        ),
    )


# Table: kill_player_locations
class KillPlayerLocations(Base):
    __tablename__ = "kill_player_locations"
    kill_id = Column(BigInteger)
    match_id = Column(Text)
    subject = Column(Text)
    view_radians = Column(Float)
    x = Column(Integer)
    y = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint("kill_id", "subject", name="kill_player_locations_pk"),
        ForeignKeyConstraint(
            ["kill_id"],
            ["kills.kill_id"],
            name="fk_kill_player_locations_kills",
        ),
    )


# Table: kill_finishing_damage
class KillFinishingDamage(Base):
    __tablename__ = "kill_finishing_damage"
    kill_id = Column(BigInteger, primary_key=True)
    match_id = Column(Text, ForeignKey("matches.match_id"))
    damage_type = Column(Text)
    damage_item = Column(Text)
    is_secondary_fire_mode = Column(Boolean)


# Table: players
class Players(Base):
    __tablename__ = "players"
    match_id = Column(Text, ForeignKey("matches.match_id"))
    subject = Column(Text)
    game_name = Column(Text)
    tag_line = Column(Text)
    team_id = Column(Text)
    party_id = Column(Text)
    character_id = Column(Text)
    competitive_tier = Column(Integer)
    is_observer = Column(Boolean)
    player_card = Column(Text)
    player_title = Column(Text)
    preferred_level_border = Column(Text)
    account_level = Column(Integer)
    session_playtime_minutes = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint("match_id", "subject", name="players_pk"),
    )


# Table: player_platform_info
class PlayerPlatformInfo(Base):
    __tablename__ = "player_platform_info"
    match_id = Column(Text, ForeignKey("matches.match_id"))
    subject = Column(Text)
    platform_type = Column(Text)
    platform_os = Column(Text)
    platform_os_version = Column(Text)
    platform_chipset = Column(Text)
    platform_device = Column(Text)
    __table_args__ = (
        PrimaryKeyConstraint("match_id", "subject", name="player_platform_info_pk"),
    )


# Table: player_match_stats
class PlayerMatchStats(Base):
    __tablename__ = "player_match_stats"
    match_id = Column(Text, ForeignKey("matches.match_id"))
    subject = Column(Text)
    score = Column(Integer)
    rounds_played = Column(Integer)
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)
    playtime_millis = Column(Integer)
    match_grenade_casts = Column(Integer)
    match_ability1_casts = Column(Integer)
    match_ability2_casts = Column(Integer)
    match_ultimate_casts = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint("match_id", "subject", name="player_match_stats_pk"),
    )


# Table: player_xp_modifications
class PlayerXPModifications(Base):
    __tablename__ = "player_xp_modifications"
    match_id = Column(Text, ForeignKey("matches.match_id"))
    subject = Column(Text)
    modification_id = Column(Text)
    value = Column(Float)
    __table_args__ = (
        PrimaryKeyConstraint("match_id", "subject", "modification_id", name="player_xp_modifications_pk"),
    )


# Table: player_behavior_factors
class PlayerBehaviorFactors(Base):
    __tablename__ = "player_behavior_factors"
    match_id = Column(Text, ForeignKey("matches.match_id"))
    subject = Column(Text)
    afk_rounds = Column(Float)
    collisions = Column(Float)
    comms_rating_recovery = Column(Integer)
    damage_participation_outgoing = Column(Integer)
    friendly_fire_incoming = Column(Integer)
    friendly_fire_outgoing = Column(Integer)
    mouse_movement = Column(Integer)
    self_damage = Column(Float)
    stayed_in_spawn_rounds = Column(Float)
    __table_args__ = (
        PrimaryKeyConstraint("match_id", "subject", name="player_behavior_factors_pk"),
    )


# Table: complete_new_player_experience_details
class CompleteNewPlayerExperienceDetails(Base):
    __tablename__ = "complete_new_player_experience_details"
    # Note: Here the PK is only subject.
    subject = Column(Text, primary_key=True)
    version_string = Column(Text)
    basic_movement_idle_time_millis = Column(Integer)
    basic_movement_objective_complete_time_millis = Column(Integer)
    basic_gun_skill_idle_time_millis = Column(Integer)
    basic_gun_skill_objective_complete_time_millis = Column(Integer)
    adaptive_bots_idle_time_millis = Column(Integer)
    adaptive_bots_objective_complete_time_millis = Column(Integer)
    adaptive_bot_avg_duration_all_attempts = Column(Integer)
    adaptive_bot_avg_duration_first_attempt = Column(Integer)
    kill_details_first_attempt = Column(Text)
    ability_idle_time_millis = Column(Integer)
    ability_objective_complete_time_millis = Column(Integer)
    bomb_plant_idle_time_millis = Column(Integer)
    bomb_plant_objective_complete_time_millis = Column(Integer)
    defend_bomb_site_idle_time_millis = Column(Integer)
    defend_bomb_site_objective_complete_time_millis = Column(Integer)
    defend_bomb_site_success = Column(Boolean)
    setting_status_is_mouse_sensitivity_default = Column(Boolean)
    setting_status_is_crosshair_default = Column(Boolean)


# Table: round_results
class RoundResults(Base):
    __tablename__ = "round_results"
    match_id = Column(Text, ForeignKey("matches.match_id"))
    round_num = Column(Integer)
    round_result = Column(Text)
    round_ceremony = Column(Text)
    winning_team = Column(Text)
    bomb_planter = Column(Text)
    bomb_defuser = Column(Text)
    plant_round_time = Column(Integer)
    plant_site = Column(Text)
    defuse_round_time = Column(Integer)
    round_result_code = Column(Text)
    round_plant_location_x = Column(Integer)
    round_plant_location_y = Column(Integer)
    round_defuse_location_x = Column(Integer)
    round_defuse_location_y = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint("match_id", "round_num", name="round_results_pk"),
    )


# Table: round_plant_player_locations
class RoundPlantPlayerLocations(Base):
    __tablename__ = "round_plant_player_locations"
    match_id = Column(Text, ForeignKey("matches.match_id"))
    round_num = Column(Integer)
    subject = Column(Text)
    view_radians = Column(Float)
    location_x = Column(Integer)
    location_y = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint("match_id", "round_num", "subject", name="round_plant_player_locations_pk"),
    )


# Table: round_defuse_player_locations
class RoundDefusePlayerLocations(Base):
    __tablename__ = "round_defuse_player_locations"
    match_id = Column(Text, ForeignKey("matches.match_id"))
    round_num = Column(Integer)
    subject = Column(Text)
    view_radians = Column(Float)
    location_x = Column(Integer)
    location_y = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint("match_id", "round_num", "subject", name="round_defuse_player_locations_pk"),
    )


# Table: round_player_stats
class RoundPlayerStats(Base):
    __tablename__ = "round_player_stats"
    match_id = Column(Text, ForeignKey("matches.match_id"))
    round_num = Column(Integer)
    subject = Column(Text)
    score = Column(Integer)
    was_afk = Column(Boolean)
    was_penalized = Column(Boolean)
    stayed_in_spawn = Column(Boolean)
    __table_args__ = (
        PrimaryKeyConstraint("match_id", "round_num", "subject", name="round_player_stats_pk"),
    )


# Table: player_round_damage
class PlayerRoundDamage(Base):
    __tablename__ = "player_round_damage"
    player_round_damage_id = Column(BigInteger, primary_key=True, autoincrement=True)
    match_id = Column(Text, ForeignKey("matches.match_id"))
    round_num = Column(Integer)
    subject = Column(Text)
    receiver = Column(Text)
    damage = Column(Integer)
    legshots = Column(Integer)
    bodyshots = Column(Integer)
    headshots = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint("player_round_damage_id", name="player_round_damage_pk"),
    )


# Table: round_economy
class RoundEconomy(Base):
    __tablename__ = "round_economy"
    match_id = Column(Text, ForeignKey("matches.match_id"))
    round_num = Column(Integer)
    subject = Column(Text)
    loadout_value = Column(Integer)
    weapon = Column(Text)
    armor = Column(Text)
    remaining = Column(Integer)
    spent = Column(Integer)
    __table_args__ = (
        PrimaryKeyConstraint("match_id", "round_num", "subject", name="round_economy_pk"),
    )


# Table: round_ability_effects
class RoundAbilityEffects(Base):
    __tablename__ = "round_ability_effects"
    match_id = Column(Text, ForeignKey("matches.match_id"))
    round_num = Column(Integer)
    subject = Column(Text)
    grenade_effects = Column(Text)
    ability1_effects = Column(Text)
    ability2_effects = Column(Text)
    ultimate_effects = Column(Text)
    __table_args__ = (
        PrimaryKeyConstraint("match_id", "round_num", "subject", name="round_ability_effects_pk"),
    )


# Table: teams
class Teams(Base):
    __tablename__ = "teams"
    match_id = Column(Text, ForeignKey("matches.match_id"))
    team_id = Column(Text)
    won = Column(Boolean)
    rounds_played = Column(Integer)
    rounds_won = Column(Integer)
    num_points = Column(Integer)
    roster_info = Column(Text)
    __table_args__ = (
        PrimaryKeyConstraint("match_id", "team_id", name="teams_pk"),
    )
