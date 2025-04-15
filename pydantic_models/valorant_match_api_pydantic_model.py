# generated by datamodel-codegen:
#   filename:  67be264e22f58af17bd8a42a.json
#   timestamp: 2025-03-05T12:23:29+00:00

from __future__ import annotations

from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field


class BasicMovement(BaseModel):
    idleTimeMillis: int
    objectiveCompleteTimeMillis: int


class BasicGunSkill(BaseModel):
    idleTimeMillis: int
    objectiveCompleteTimeMillis: int


class AdaptiveBots(BaseModel):
    idleTimeMillis: int
    objectiveCompleteTimeMillis: int
    adaptiveBotAverageDurationMillisAllAttempts: int
    adaptiveBotAverageDurationMillisFirstAttempt: int
    killDetailsFirstAttempt: None


class Ability(BaseModel):
    idleTimeMillis: int
    objectiveCompleteTimeMillis: int


class BombPlant(BaseModel):
    idleTimeMillis: int
    objectiveCompleteTimeMillis: int


class DefendBombSite(BaseModel):
    idleTimeMillis: int
    objectiveCompleteTimeMillis: int
    success: bool


class SettingStatus(BaseModel):
    isMouseSensitivityDefault: bool
    isCrosshairDefault: bool


class NewPlayerExperienceDetails(BaseModel):
    basicMovement: BasicMovement
    basicGunSkill: BasicGunSkill
    adaptiveBots: AdaptiveBots
    ability: Ability
    bombPlant: BombPlant
    defendBombSite: DefendBombSite
    settingStatus: SettingStatus
    versionString: str



class XpModification(BaseModel):
    Value: float
    ID: str

class RoundDamageItem(BaseModel):
    round: int
    receiver: str
    damage: int


class PlatformInfo(BaseModel):
    platformType: str
    platformOS: str
    platformOSVersion: str
    platformChipset: str
    platformDevice: str

class matchAbilityCasts(BaseModel):
    """
    Represents the number of times each type of ability was cast during a match.
    This includes grenade casts, two other abilities, and ultimate casts.
    Each attribute is optional and may not be present if the ability was not used.
    """
    grenadeCasts: Optional[int]
    ability1Casts: Optional[int]
    ability2Casts: Optional[int]
    ultimateCasts: Optional[int]

class playerMatchStats(BaseModel):
    """
    Represents the statistics of a player for an entire match.
    This includes the player's score, number of rounds played, kills, deaths, assists,
    total playtime in milliseconds, and the ability casts during the match.
    """
    score: int
    roundsPlayed: int
    kills: int
    deaths: int
    assists: int
    playtimeMillis: int
    abilityCasts: Optional[matchAbilityCasts] #The ability casts for the entire match

class BehaviorFactors(BaseModel):
    """
    Represents various behavioral factors of a player during a match.
    These factors include metrics such as the number of rounds the player was AFK,
    the number of collisions, communication rating recovery, damage participation,
    friendly fire incidents (both incoming and outgoing), mouse movement, self-inflicted damage,
    and the number of rounds the player stayed in spawn.
    """
    afkRounds: float
    collisions: float
    commsRatingRecovery: int
    damageParticipationOutgoing: int
    friendlyFireIncoming: float
    friendlyFireOutgoing: float
    mouseMovement: int
    selfDamage: float
    stayedInSpawnRounds: float

class Player(BaseModel):
    """
    Represents a player in a Valorant match.
    This includes the player's unique identifier, game name, tag line, platform information,
    team and party identifiers, character used, match statistics, round damage details,
    competitive tier, observer status, player card and title, preferred level border,
    account level, session playtime, experience details, and behavior factors.
    """
    subject: str
    gameName: str
    tagLine: str
    platformInfo: PlatformInfo
    teamId: str
    partyId: str
    characterId: str
    stats: playerMatchStats #The player's stats for the entire match
    roundDamage: Optional[List[RoundDamageItem]]
    competitiveTier: int
    isObserver: bool
    playerCard: str
    playerTitle: str
    preferredLevelBorder: Optional[str]
    accountLevel: int
    sessionPlaytimeMinutes: Optional[int]
    xpModifications: Optional[List[XpModification]]
    behaviorFactors: Optional[BehaviorFactors]
    newPlayerExperienceDetails: NewPlayerExperienceDetails

class PremierMatchInfo(BaseModel):
    premierSeasonId: None
    premierEventId: None


class MatchInfo(BaseModel):
    matchId: str
    mapId: str
    gamePodId: str
    gameLoopZone: str
    gameServerAddress: str
    gameVersion: str
    gameLengthMillis: int
    gameStartMillis: int
    provisioningFlowID: str
    isCompleted: bool
    customGameName: str
    forcePostProcessing: bool
    queueID: str
    gameMode: str
    isRanked: bool
    isMatchSampled: bool
    seasonId: str
    completionState: str
    platformType: str
    premierMatchInfo: PremierMatchInfo
    partyRRPenalties: Dict[str, float]
    shouldMatchDisablePenalties: bool

class Location(BaseModel):
    x: int
    y: int


class DetailedPlayerLocation(BaseModel):
    """
    Location of player along with viewRadians
    """
    subject: str
    viewRadians: float
    location: Location


class DetailedRoundDamageItem(BaseModel):
    receiver: str
    damage: int
    legshots: int
    bodyshots: int
    headshots: int


class RoundAbilityCasts(BaseModel):
    """
    RoundAbilityCasts represents the number of effects caused by different abilities during a round.
    It includes optional counts for grenade effects, two other abilities, and ultimate effects.
    """
    grenadeEffects: Optional[int]
    ability1Effects: Optional[int]
    ability2Effects: Optional[int]
    ultimateEffects: Optional[int]


class FinishingDamage(BaseModel):
    damageType: Optional[str] = Field(default='NA')
    damageItem: str
    isSecondaryFireMode: bool


class roundKill(BaseModel):
    """
    Represents a kill event in a Valorant match. 
    This includes details such as the game time and round time when the kill occurred,
    the killer and victim's identifiers, the victim's location,
    any assistants involved in the kill, the locations of players at the time of the kill,
    and the finishing damage details.
    """
    gameTime: int
    roundTime: int
    killer: Optional[str] #Can be None in the cases where the victim dies due to other reasons like Fall, Explosion etc. Hence the Optional[str]
    victim: str
    victimLocation: Location 
    assistants: List[str]
    playerLocations: List[DetailedPlayerLocation] #Remaining (still alive) Player locations at the time of the kill
    finishingDamage: FinishingDamage

class RoundPlayerStat(BaseModel):
    subject: str
    kills: List[roundKill] #The list of kills in that round
    damage: List[DetailedRoundDamageItem]
    score: int
    economy: Economy
    ability: RoundAbilityCasts  #The abilities cast in that round
    wasAfk: bool
    wasPenalized: bool
    stayedInSpawn: bool

class Economy(BaseModel):
    loadoutValue: int
    weapon: Optional[str]
    armor: Optional[str]
    remaining: int
    spent: int

class RoundPlayerEconomy(Economy):
    """
    Extends Economy class by adding subject (player) id
    """
    subject: str

class PlayerScore(BaseModel):
    subject: str
    score: int

class RoundResult(BaseModel):
    roundNum: int
    roundResult: str
    roundCeremony: str
    winningTeam: str
    bombPlanter: Optional[str]
    bombDefuser: Optional[str]
    plantRoundTime: int
    plantPlayerLocations: Optional[List[DetailedPlayerLocation]]
    plantLocation: Location
    plantSite: Optional[str]
    defuseRoundTime: int
    defusePlayerLocations: Optional[List[DetailedPlayerLocation]]
    defuseLocation: Location
    playerStats: List[RoundPlayerStat]
    roundResultCode: str
    playerEconomies: Optional[List[RoundPlayerEconomy]] #Also present as a part of the RoundPlayerStat
    playerScores: Optional[List[PlayerScore]]

class RoundKillWithRoundNumber(roundKill):
    """
    Extends the roundKill class and adds the round number
    """
    round: int

class Team(BaseModel):
    teamId: str
    won: bool
    roundsPlayed: int
    roundsWon: int
    numPoints: int
    rosterInfo: None

class ValorantMatchAPIModel(BaseModel):
    field_id: str = Field(..., alias='_id')
    matchInfo: MatchInfo
    coaches: List
    kills: List[RoundKillWithRoundNumber]
    players: List[Player]
    region: Optional[Any]
    roundResults: List[RoundResult]
    teams: List[Team]
