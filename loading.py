import json
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import your SQLAlchemy ORM models.
# For example, assuming you defined ORM classes for each table in models.py:
from sqlalchemy_models.sqlalchemy_models import (
    Matches, PremierMatchInfo, PartyRRPenalties, Coaches, Kills, KillVictimLocations,
    KillAssistants, KillPlayerLocations, KillFinishingDamage, Players, PlayerPlatformInfo,
    PlayerMatchStats, PlayerXPModifications, PlayerBehaviorFactors,
    CompleteNewPlayerExperienceDetails, RoundResults, RoundPlantPlayerLocations,
    RoundDefusePlayerLocations, RoundPlayerStats, PlayerRoundDamage, RoundEconomy,
    RoundAbilityEffects, Teams
)

# Import the validated Pydantic model
from pydantic_models.valorant_match_api_pydantic_model import ValorantMatchAPIModel


def update_matches(session, validated_data: ValorantMatchAPIModel):

    logger.info("Updating matches with match_id: %s", validated_data.matchInfo.matchId)
    mi = validated_data.matchInfo
    match_row = Matches(
        match_id=mi.matchId,
        map_id=mi.mapId,
        game_pod_id=mi.gamePodId,
        game_loop_zone=mi.gameLoopZone,
        game_server_address=mi.gameServerAddress,
        game_version=mi.gameVersion,
        game_length_millis=mi.gameLengthMillis,
        game_start_millis=mi.gameStartMillis,
        provisioning_flow_id=mi.provisioningFlowID,
        is_completed=mi.isCompleted,
        custom_game_name=mi.customGameName,
        force_post_processing=mi.forcePostProcessing,
        queue_id=mi.queueID,
        game_mode=mi.gameMode,
        is_ranked=mi.isRanked,
        is_match_sampled=mi.isMatchSampled,
        season_id=mi.seasonId,
        completion_state=mi.completionState,
        platform_type=mi.platformType,
        should_match_disable_penalties=mi.shouldMatchDisablePenalties,
        region=validated_data.region if validated_data.region is not None else ""
    )
    session.add(match_row)
    session.flush() #Get the match_id which serves as foreign key
    # session.commit()
    logger.info("Match data added to the session for match_id: %s", mi.matchId)

def update_premier_match_info(session, validated_data: ValorantMatchAPIModel):
    logger.info("Updating premier match info for match_id: %s", validated_data.matchInfo.matchId)
    
    pmi = validated_data.matchInfo.premierMatchInfo
    pmi_row = PremierMatchInfo(
        match_id=validated_data.matchInfo.matchId,
        premier_season_id=pmi.premierSeasonId,
        premier_event_id=pmi.premierEventId
    )
    session.add(pmi_row)
    # session.commit()
    logger.info("Premier match info added to the session for match_id: %s", validated_data.matchInfo.matchId)

def update_party_rr_penalties(session, validated_data: ValorantMatchAPIModel):
    logger.info("Updating party RR penalties for match_id: %s", validated_data.matchInfo.matchId)
    penalties = validated_data.matchInfo.partyRRPenalties
    for party_id, penalty_value in penalties.items():
        logger.debug("Adding penalty for party_id: %s with penalty_value: %s", party_id, penalty_value)
        penalty_row = PartyRRPenalties(
            match_id=validated_data.matchInfo.matchId,
            party_id=party_id,
            penalty_value=penalty_value
        )
        session.add(penalty_row)
    # session.commit()
    logger.info("Party RR penalties added to the session for match_id: %s", validated_data.matchInfo.matchId)

def update_coaches(session, validated_data: ValorantMatchAPIModel):
    logger.info("Updating coaches for match_id: %s", validated_data.matchInfo.matchId)
    
    if validated_data.coaches != []:
        # Assuming coaches is a list of strings.
        for coach in validated_data.coaches:
            logger.debug("Adding coach: %s", coach)
            coach_row = Coaches(
                match_id=validated_data.matchInfo.matchId,
                coach=coach
            )
            session.add(coach_row)
        session.commit()
        logger.info("Coaches added to the session for match_id: %s", validated_data.matchInfo.matchId)

def update_kills(session, validated_data: ValorantMatchAPIModel):
    logger.info("Updating kills for match_id: %s", validated_data.matchInfo.matchId)
    for kill in validated_data.kills:
        logger.debug("Processing kill with game_time: %s, round_time: %s", kill.gameTime, kill.roundTime)
        kill_row = Kills(
            match_id=validated_data.matchInfo.matchId,
            game_time=kill.gameTime,
            round_time=kill.roundTime,
            round_num=getattr(kill, "round", None),
            killer=kill.killer if kill.killer is not None else "",
            victim=kill.victim
        )
        session.add(kill_row)
        session.flush()  # flush to obtain kill_row.kill_id
        logger.debug("Kill added with kill_id: %s", kill_row.kill_id)
        
        # Insert kill victim location
        kvl = KillVictimLocations(
            kill_id=kill_row.kill_id,
            match_id=validated_data.matchInfo.matchId,
            x=kill.victimLocation.x,
            y=kill.victimLocation.y
        )
        session.add(kvl)
        logger.debug("Kill victim location added for kill_id: %s", kill_row.kill_id)
        
        # Insert kill assistants
        for assistant in kill.assistants:
            logger.debug("Adding assistant: %s for kill_id: %s", assistant, kill_row.kill_id)
            ka = KillAssistants(
                kill_id=kill_row.kill_id,
                match_id=validated_data.matchInfo.matchId,
                assistant=assistant
            )
            session.add(ka)
        
        # Insert kill player locations
        for ploc in kill.playerLocations:
            logger.debug("Adding player location for subject: %s, kill_id: %s", ploc.subject, kill_row.kill_id)
            kpl = KillPlayerLocations(
                kill_id=kill_row.kill_id,
                match_id=validated_data.matchInfo.matchId,
                subject=ploc.subject,
                view_radians=ploc.viewRadians,
                x=ploc.location.x,
                y=ploc.location.y
            )
            session.add(kpl)
        
        # Insert kill finishing damage
        fd = kill.finishingDamage
        logger.debug("Adding finishing damage for kill_id: %s", kill_row.kill_id)
        kfd = KillFinishingDamage(
            kill_id=kill_row.kill_id,
            match_id=validated_data.matchInfo.matchId,
            damage_type=fd.damageType,
            damage_item=fd.damageItem,
            is_secondary_fire_mode=fd.isSecondaryFireMode
        )
        session.add(kfd)
    # session.commit()
    logger.info("Kills updated for match_id: %s", validated_data.matchInfo.matchId)

def update_players(session, validated_data: ValorantMatchAPIModel):

    logger.info("Updating Players for match_id: %s", validated_data.matchInfo.matchId)
    for player in validated_data.players:
        logger.debug("Processing player: %s", player.subject)
        player_row = Players(
            match_id=validated_data.matchInfo.matchId,
            subject=player.subject,
            game_name=player.gameName,
            tag_line=player.tagLine,
            team_id=player.teamId,
            party_id=player.partyId,
            character_id=player.characterId,
            competitive_tier=player.competitiveTier,
            is_observer=player.isObserver,
            player_card=player.playerCard,
            player_title=player.playerTitle,
            preferred_level_border=player.preferredLevelBorder or "",
            account_level=player.accountLevel,
            session_playtime_minutes=player.sessionPlaytimeMinutes if player.sessionPlaytimeMinutes is not None else 0
        )
        session.add(player_row)
        session.flush()
        logger.debug("Player added with subject: %s", player.subject)
        
        # Insert player_platform_info
        ppi = player.platformInfo
        platform_row = PlayerPlatformInfo(
            match_id=validated_data.matchInfo.matchId,
            subject=player.subject,
            platform_type=ppi.platformType,
            platform_os=ppi.platformOS,
            platform_os_version=ppi.platformOSVersion,
            platform_chipset=ppi.platformChipset,
            platform_device=ppi.platformDevice
        )
        session.add(platform_row)
        logger.debug("Player platform info added for subject: %s", player.subject)
        
        # Insert player_match_stats
        pms = player.stats
        ac = pms.abilityCasts
        stats_row = PlayerMatchStats(
            match_id=validated_data.matchInfo.matchId,
            subject=player.subject,
            score=pms.score,
            rounds_played=pms.roundsPlayed,
            kills=pms.kills,
            deaths=pms.deaths,
            assists=pms.assists,
            playtime_millis=pms.playtimeMillis,
            match_grenade_casts=ac.grenadeCasts or 0,
            match_ability1_casts=ac.ability1Casts or 0,
            match_ability2_casts=ac.ability2Casts or 0,
            match_ultimate_casts=ac.ultimateCasts or 0
        )
        session.add(stats_row)
        logger.debug("Player match stats added for subject: %s", player.subject)
        
        # Insert player_xp_modifications
        if player.xpModifications:
            for mod in player.xpModifications:
                xp_row = PlayerXPModifications(
                    match_id=validated_data.matchInfo.matchId,
                    subject=player.subject,
                    modification_id=mod.ID,
                    value=mod.Value
                )
                session.add(xp_row)
                logger.debug("XP modification added for subject: %s, modification_id: %s", player.subject, mod.ID)
        
        # Insert player_behavior_factors
        pb = player.behaviorFactors
        behavior_row = PlayerBehaviorFactors(
            match_id=validated_data.matchInfo.matchId,
            subject=player.subject,
            afk_rounds=pb.afkRounds,
            collisions=pb.collisions,
            comms_rating_recovery=pb.commsRatingRecovery,
            damage_participation_outgoing=pb.damageParticipationOutgoing,
            friendly_fire_incoming=pb.friendlyFireIncoming,
            friendly_fire_outgoing=pb.friendlyFireOutgoing,
            mouse_movement=pb.mouseMovement,
            self_damage=pb.selfDamage,
            stayed_in_spawn_rounds=pb.stayedInSpawnRounds
        )
        session.add(behavior_row)
        logger.debug("Player behavior factors added for subject: %s", player.subject)
        
        # Insert combined new player experience details
        npe = player.newPlayerExperienceDetails
        
        # complete_npe = CompleteNewPlayerExperienceDetails(
        #     subject=player.subject,
        #     version_string=npe.versionString,
        #     basic_movement_idle_time_millis=npe.basicMovement.idleTimeMillis,
        #     basic_movement_objective_complete_time_millis=npe.basicMovement.objectiveCompleteTimeMillis,
        #     basic_gun_skill_idle_time_millis=npe.basicGunSkill.idleTimeMillis,
        #     basic_gun_skill_objective_complete_time_millis=npe.basicGunSkill.objectiveCompleteTimeMillis,
        #     adaptive_bots_idle_time_millis=npe.adaptiveBots.idleTimeMillis,
        #     adaptive_bots_objective_complete_time_millis=npe.adaptiveBots.objectiveCompleteTimeMillis,
        #     adaptive_bot_avg_duration_all_attempts=npe.adaptiveBots.adaptiveBotAverageDurationMillisAllAttempts,
        #     adaptive_bot_avg_duration_first_attempt=npe.adaptiveBots.adaptiveBotAverageDurationMillisFirstAttempt,
        #     kill_details_first_attempt=npe.adaptiveBots.killDetailsFirstAttempt,
        #     ability_idle_time_millis=npe.ability.idleTimeMillis,
        #     ability_objective_complete_time_millis=npe.ability.objectiveCompleteTimeMillis,
        #     bomb_plant_idle_time_millis=npe.bombPlant.idleTimeMillis,
        #     bomb_plant_objective_complete_time_millis=npe.bombPlant.objectiveCompleteTimeMillis,
        #     defend_bomb_site_idle_time_millis=npe.defendBombSite.idleTimeMillis,
        #     defend_bomb_site_objective_complete_time_millis=npe.defendBombSite.objectiveCompleteTimeMillis,
        #     defend_bomb_site_success=npe.defendBombSite.success,
        #     setting_status_is_mouse_sensitivity_default=npe.settingStatus.isMouseSensitivityDefault,
        #     setting_status_is_crosshair_default=npe.settingStatus.isCrosshairDefault
        # )

        #The subject might repeat across matches. Since multiple matches are loaded together parallelly on separate threads, 
        # race conditions can lead to primary key violations on this table 
        # i.e. if a parallel thread has loaded the same subject into the database before the current thread. 
        #A regular session.add() would lead to primary key violations. 
        #Hence making use of postgres' on conflict do nothing to avoid errors.
        #While inserting, if a primary key conflict is found, it will not do anything
        complete_npe = insert(CompleteNewPlayerExperienceDetails).values(
        subject=player.subject,
        version_string=npe.versionString,
        basic_movement_idle_time_millis=npe.basicMovement.idleTimeMillis,
        basic_movement_objective_complete_time_millis=npe.basicMovement.objectiveCompleteTimeMillis,
        basic_gun_skill_idle_time_millis=npe.basicGunSkill.idleTimeMillis,
        basic_gun_skill_objective_complete_time_millis=npe.basicGunSkill.objectiveCompleteTimeMillis,
        adaptive_bots_idle_time_millis=npe.adaptiveBots.idleTimeMillis,
        adaptive_bots_objective_complete_time_millis=npe.adaptiveBots.objectiveCompleteTimeMillis,
        adaptive_bot_avg_duration_all_attempts=npe.adaptiveBots.adaptiveBotAverageDurationMillisAllAttempts,
        adaptive_bot_avg_duration_first_attempt=npe.adaptiveBots.adaptiveBotAverageDurationMillisFirstAttempt,
        kill_details_first_attempt=npe.adaptiveBots.killDetailsFirstAttempt,
        ability_idle_time_millis=npe.ability.idleTimeMillis,
        ability_objective_complete_time_millis=npe.ability.objectiveCompleteTimeMillis,
        bomb_plant_idle_time_millis=npe.bombPlant.idleTimeMillis,
        bomb_plant_objective_complete_time_millis=npe.bombPlant.objectiveCompleteTimeMillis,
        defend_bomb_site_idle_time_millis=npe.defendBombSite.idleTimeMillis,
        defend_bomb_site_objective_complete_time_millis=npe.defendBombSite.objectiveCompleteTimeMillis,
        defend_bomb_site_success=npe.defendBombSite.success,
        setting_status_is_mouse_sensitivity_default=npe.settingStatus.isMouseSensitivityDefault,
        setting_status_is_crosshair_default=npe.settingStatus.isCrosshairDefault
    ).on_conflict_do_nothing(index_elements=["subject"])  
        
        
        session.execute(complete_npe)
        session.flush() #Check that any new primary keys generated during the session are updated.
        
        #New player experience details would only happen once per subject presumably. 
        # Therefore do not insert if the entity already exists.
        
    #     existing_npe = session.query(CompleteNewPlayerExperienceDetails).filter_by(subject=player.subject).first() #Check if the entity exists
    #     if existing_npe is None:
    #         try:
    #             # session.merge(complete_npe) #Using session.merge instead of session.add because in this particular table, race conditions with other threads often lead to primary key violations despite checks. session.merge causes an upsert, thereby bypassing primary key violations
    #             session.execute(stmt)
    #             session.flush() #Sending changes to the database (without committing) so that the primary key field can be updated and violations can be checked.
    #             logger.debug("New player experience details added for subject: %s", player.subject)
    #         except IntegrityError as e:
    #             if 'violates unique constraint' in str(e.orig):
    #                 logger.debug("Primary key violation for new player experience details, subject: %s", player.subject)
    #             else:
    #                 logger.debug(f"Insertion issue into new player experience details: {e}")
    #     else:
    #         logger.debug("New player experience details already exist for subject: %s", player.subject)
    # # session.commit()
    logger.info("Players updated for match_id: %s", validated_data.matchInfo.matchId)

def update_round_results(session, validated_data: ValorantMatchAPIModel):
    logger.info("Committing round results for match_id: %s", validated_data.matchInfo.matchId)

    for rr in validated_data.roundResults:
        rr_row = RoundResults(
            match_id=validated_data.matchInfo.matchId,
            round_num=rr.roundNum,
            round_result=rr.roundResult,
            round_ceremony=rr.roundCeremony,
            winning_team=rr.winningTeam,
            bomb_planter=rr.bombPlanter or "",
            bomb_defuser=rr.bombDefuser or "",
            plant_round_time=rr.plantRoundTime,
            plant_site=rr.plantSite or "",
            defuse_round_time=rr.defuseRoundTime,
            round_result_code=rr.roundResultCode,
            round_plant_location_x=rr.plantLocation.x,
            round_plant_location_y=rr.plantLocation.y,
            round_defuse_location_x=rr.defuseLocation.x,
            round_defuse_location_y=rr.defuseLocation.y
        )
        session.add(rr_row)
        logger.debug("Round result added for match_id: %s, round_num: %s", validated_data.matchInfo.matchId, rr.roundNum)
        session.flush()  # flush to obtain round_results for foreign keys

        # Insert round plant player locations (if present)
        if rr.plantPlayerLocations:
            for ppl in rr.plantPlayerLocations:
                rpp = RoundPlantPlayerLocations(
                    match_id=validated_data.matchInfo.matchId,
                    round_num=rr.roundNum,
                    subject=ppl.subject,
                    view_radians=ppl.viewRadians,
                    location_x=ppl.location.x,
                    location_y=ppl.location.y
                )
                session.add(rpp)
                logger.debug("Round plant player location added for subject: %s, round_num: %s", ppl.subject, rr.roundNum)
        
        # Insert round defuse player locations (if present)
        if rr.defusePlayerLocations:
            for dpl in rr.defusePlayerLocations:
                rdpl = RoundDefusePlayerLocations(
                    match_id=validated_data.matchInfo.matchId,
                    round_num=rr.roundNum,
                    subject=dpl.subject,
                    view_radians=dpl.viewRadians,
                    location_x=dpl.location.x,
                    location_y=dpl.location.y
                )
                session.add(rdpl)
                logger.debug("Round defuse player location added for subject: %s, round_num: %s", dpl.subject, rr.roundNum)
        
        # Insert round player stats and nested tables
        for rps in rr.playerStats:
            rps_row = RoundPlayerStats(
                match_id=validated_data.matchInfo.matchId,
                round_num=rr.roundNum,
                subject=rps.subject,
                score=rps.score,
                was_afk=rps.wasAfk,
                was_penalized=rps.wasPenalized,
                stayed_in_spawn=rps.stayedInSpawn
            )
            session.add(rps_row)
            logger.debug("Round player stats added for subject: %s, round_num: %s", rps.subject, rr.roundNum)
            session.flush()  # to obtain round player stats key

            # Insert round player damage
            for dmg in rps.damage:
                prd = PlayerRoundDamage(
                    match_id=validated_data.matchInfo.matchId,
                    round_num=rr.roundNum,
                    subject=rps.subject,
                    receiver=dmg.receiver,
                    damage=dmg.damage,
                    legshots=dmg.legshots,
                    bodyshots=dmg.bodyshots,
                    headshots=dmg.headshots
                )
                session.add(prd)
                logger.debug("Player round damage added for subject: %s, receiver: %s, round_num: %s", rps.subject, dmg.receiver, rr.roundNum)
            
            # Insert round economy
            re_row = RoundEconomy(
                match_id=validated_data.matchInfo.matchId,
                round_num=rr.roundNum,
                subject=rps.subject,
                loadout_value=rps.economy.loadoutValue,
                weapon=rps.economy.weapon or "",
                armor=rps.economy.armor or "",
                remaining=rps.economy.remaining,
                spent=rps.economy.spent
            )
            session.add(re_row)
            logger.debug("Round economy added for subject: %s, round_num: %s", rps.subject, rr.roundNum)
            
            # Insert round ability effects
            rae = rps.ability
            rae_row = RoundAbilityEffects(
                match_id=validated_data.matchInfo.matchId,
                round_num=rr.roundNum,
                subject=rps.subject,
                grenade_effects=rae.grenadeEffects if rae.grenadeEffects is not None else 0,
                ability1_effects=rae.ability1Effects if rae.ability1Effects is not None else 0,
                ability2_effects=rae.ability2Effects if rae.ability2Effects is not None else 0,
                ultimate_effects=rae.ultimateEffects if rae.ultimateEffects is not None else 0
            )
            session.add(rae_row)
            logger.debug("Round ability effects added for subject: %s, round_num: %s", rps.subject, rr.roundNum)

        # session.commit()
    logger.info("Round results committed for match_id: %s", validated_data.matchInfo.matchId)

def update_teams(session, validated_data: ValorantMatchAPIModel):
    logger.info("Updating teams for match_id: %s", validated_data.matchInfo.matchId)
    for team in validated_data.teams:
        logger.debug("Processing team_id: %s", team.teamId)
        team_row = Teams(
            match_id=validated_data.matchInfo.matchId,
            team_id=team.teamId,
            won=team.won,
            rounds_played=team.roundsPlayed,
            rounds_won=team.roundsWon,
            num_points=team.numPoints,
            roster_info=team.rosterInfo or ""
        )
        session.add(team_row)
        logger.debug("Team added for team_id: %s", team.teamId)
    # session.commit()
    logger.info("Teams updated for match_id: %s", validated_data.matchInfo.matchId)

def load_valorant_data_to_database(Session,validated_data):

    session = Session()
    # Setup the SQLAlchemy engine and session
    success_flag=0
    try:
        update_matches(session, validated_data)
        update_premier_match_info(session, validated_data)
        update_party_rr_penalties(session, validated_data)
        update_coaches(session, validated_data)
        update_kills(session, validated_data)
        update_players(session, validated_data)
        update_round_results(session, validated_data)
        update_teams(session, validated_data)
        success_flag=1
        logger.info("Data successfully loaded into the database.")
        
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error: {e}")

    finally:
        session.commit() #If there were no exceptions, commit everything to the database. If there was an exception, nothing will be committed
        session.close()
        
    
    return success_flag
