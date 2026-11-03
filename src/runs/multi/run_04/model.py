"""Class stubs rendered from runs/multi/run_04/model.json by src/generate/render_code.py; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from enum import Enum


class DpiMessageType(Enum):
    E_DPI = "E_DPI"
    T_DPI = "T_DPI"
    T_DPI_T = "T_DPI_T"
    T_DPI_S = "T_DPI_S"
    A_DPI = "A_DPI"


class FlightOperationalStatus(Enum):
    INITIATED = "INITIATED"
    AIRBORNE = "AIRBORNE"
    FIR = "FIR"
    FINAL = "FINAL"
    LANDED = "LANDED"
    IN_BLOCK = "IN_BLOCK"
    SEQUENCED = "SEQUENCED"
    BOARDING = "BOARDING"
    READY = "READY"
    OFF_BLOCK = "OFF_BLOCK"
    DEPARTED_TAKE_OFF = "DEPARTED_TAKE_OFF"


class TakeOffNotificationType(Enum):
    FSA = "FSA"
    MVT = "MVT"
    AIRBORNE = "AIRBORNE"


class TimePrefix(Enum):
    SCHEDULED = "SCHEDULED"
    ESTIMATED = "ESTIMATED"
    TARGET = "TARGET"
    ACTUAL = "ACTUAL"
    CALCULATED = "CALCULATED"


@dataclass
class AcarsSystem:
    """The ACARS system fitted to equipped aircraft that reports actual times such as landing, in-block, off-block, and take-off.

    Package Systems, stereotype boundary, milestones [6, 7, 15, 16].

    Relationship: association 'reports ALDT' -> LandingTime [*]

    Relationship: association 'reports AIBT' -> InBlockTime [*]

    Relationship: association 'reports AOBT' -> OffBlockTime [*]

    Relationship: association 'reports ATOT' -> TakeOffTime [*]
    """
    pass


@dataclass
class Aerodrome:
    """An airport, whether the departure, destination, or outstation aerodrome, involved in a flight's origin or destination.

    Package Flights, stereotype entity, milestones [1, 3].
    """
    pass


@dataclass
class AirTrafficControlUnit:
    """Any ATC unit (Area Control Centre, Approach Control, Tower, or ATS unit) that receives the flight plan, detects the flight, or issues approvals.

    Package Stakeholders, stereotype entity, milestones [1, 2, 4, 5, 9, 10, 12, 13, 14, 16].

    Relationship: association 'receives' -> FlightPlan [*]
    """
    pass


@dataclass
class Aircraft:
    """The physical aircraft operating a flight, identified by type and registration, which may be updated from the flight plan.

    Package Flights, stereotype entity, milestones [1].
    """
    registration: str | None = None
    type: str | None = None


@dataclass
class AircraftOperator:
    """The airline or operator responsible for a flight, submitting the ATC flight plan and providing TOBT and related estimates.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13].

    Relationship: association 'submits' -> FlightPlan [1..*]

    Relationship: association 'provides registration and type data for' -> Aircraft [*]

    Relationship: association 'manages' -> TurnRound [*]
    """

    def provideFlightPlanData(self, sobt: datetime, aircraftRegistration: str, firstDestination: str) -> None:
        """The AO must provide correct information before the first E-DPI message, in order to feed Network Operations with consistent SOBT, aircraft registration, and first destination data, as early in time as possible."""
        raise NotImplementedError


@dataclass
class AircraftReadyMilestone:
    """Milestone 12: informs partners of the Actual Ready Time and alerts AO/GH if TOBT has passed without an ARDT or ready status message.

    Package Milestones, stereotype control, milestones [12].

    Relationship: dependency 'informs partners of readiness for' -> Flight

    Relationship: dependency 'expects' -> ReadyStatusMessage

    Relationship: dependency 'is triggered by input to' -> AirportCdmPlatform
    """

    def informPartnersOfArdt(self, ardt: datetime) -> None:
        """Informs all relevant Airport CDM Partners of Actual Ready Time (ARDT) in the Airport CDM Platform and that the aircraft is ready for start up / push-back."""
        raise NotImplementedError

    def checkReadyStatusReceived(self, tobt: datetime, tolerance: timedelta) -> bool:
        """At TOBT + tolerance the AO/GH are informed that TOBT has passed and there has not been a ready status message yet."""
        raise NotImplementedError


@dataclass
class AirportCdmPlatform:
    """The Airport CDM Platform that is initiated per flight, processes all available flight information, computes updated times, and triggers the DPI process and partner notifications.

    Package Systems, stereotype control, milestones [1, 2, 4, 12, 13, 14, 15].

    Relationship: dependency 'initiates for' -> Flight

    Relationship: dependency 'calculates TOBT automatically' -> OffBlockTime
    """

    def calculateTobtAutomatically(self, eldt: datetime) -> datetime:
        """Update of the ELDT can trigger a new TOBT to be entered by the AO/GH, or calculated automatically by the Airport CDM Platform."""
        raise NotImplementedError

    def initiateForFlight(self, flight: Flight) -> None:
        """The Airport CDM Platform is initiated for this flight, and all available information is processed."""
        raise NotImplementedError


@dataclass
class AirportSlot:
    """The airport slot allocated to a flight at a coordinated airport, against which the ATC flight plan and airport flight data are checked for consistency.

    Package Flights, stereotype entity, milestones [1].
    """
    pass


@dataclass
class AtcSystem:
    """The ATC system that provides radar/system-derived times (ALDT, TSAT context) and calculates EXOT based on traffic load, gate/stand location, runway, and holding position.

    Package Systems, stereotype boundary, milestones [4, 5, 6, 9].

    Relationship: association 'calculates EXOT' -> TaxiTime [*]

    Relationship: association 'provides ALDT' -> LandingTime [*]

    Relationship: association 'provides AIBT' -> InBlockTime [*]

    Relationship: association 'provides AOBT' -> OffBlockTime [*]

    Relationship: association 'provides ATOT' -> TakeOffTime [*]
    """

    def calculateExot(self, tobt: datetime, trafficLoad: str, gateStandLocation: str, runwayInUse: str, holdingPositionWait: timedelta) -> timedelta:
        """Following the receipt of the TOBT, the ATC system will calculate and provide the Estimated Taxi-Out Time (EXOT) based on the predicted traffic load, gate/stand location, runway in use, and waiting period at the Holding Position."""
        raise NotImplementedError


@dataclass
class AutomatedDockingSystem:
    """An automated docking or ground surveillance system (e.g. A-SMGCS) that detects in-block, off-block, or take-off events.

    Package Systems, stereotype boundary, milestones [7, 15, 16].

    Relationship: association 'detects AIBT' -> InBlockTime [*]

    Relationship: association 'detects AOBT' -> OffBlockTime [*]
    """
    pass


@dataclass
class BoardingStartsMilestone:
    """Milestone 11: informs partners of the Actual Start Boarding Time and checks whether boarding starts in time to respect TOBT.

    Package Milestones, stereotype control, milestones [11].

    Relationship: dependency 'informs partners of boarding for' -> Flight

    Relationship: dependency 'reads boarding status from' -> PassengerInformationSystem
    """
    triggerOffset: timedelta | None = None

    def informPartnersOfAsbt(self, asbt: datetime) -> None:
        """Informs all relevant Airport CDM Partners of Actual Start Boarding Time (ASBT) when it occurs."""
        raise NotImplementedError

    def checkBoardingStatus(self, asbt: datetime, tobt: datetime) -> bool:
        """At a certain time before TOBT (local variable e.g. corresponding to aircraft type) a check shall be performed to check the boarding status, and inform the AO/GH in case TOBT needs to be updated."""
        raise NotImplementedError


@dataclass
class BoardingTime:
    """The actual start boarding time (ASBT) at which the gate opens for passengers to board.

    Package Timings, stereotype entity, milestones [11].
    """
    value: datetime | None = None
    originator: str | None = None
    timeOfUpdate: datetime | None = None
    accuracy: timedelta | None = None


@dataclass
class DepartureClearanceMessage:
    """The DCL message or voice communication by which flight crew requests start-up.

    Package Messages, stereotype boundary, milestones [14].
    """
    pass


@dataclass
class DpiMessage:
    """A Departure Planning Information message (E-DPI, T-DPI, T-DPI-t, T-DPI-s, or A-DPI) sent to Network Operations to convey updated flight time estimates.

    Package Messages, stereotype boundary, milestones [1, 2, 3, 10, 15].
    """
    type: DpiMessageType | None = None

    def canBeSent(self, informationProvided: bool, isConsistent: bool) -> bool:
        """The E-DPI message should not be sent if no or inconsistent information is provided."""
        raise NotImplementedError


@dataclass
class EtfmsSystem:
    """The Network Operations system (ETFMS) that monitors a flight's progress within 3 hours flying time of the destination and issues Flight Update Messages.

    Package Systems, stereotype boundary, milestones [3].

    Relationship: dependency 'monitors progress of' -> Flight

    Relationship: dependency 'sends' -> FlightUpdateMessage
    """

    def monitorProgressAndSendFum(self, flight: Flight) -> FlightUpdateMessage:
        """If the flight is within 3hrs flying time of the destination airport the Network Operations monitors progress of the flight using the ETFMS and sends a Flight Update Message (FUM) that provides updates of the flight's progress."""
        raise NotImplementedError


@dataclass
class TobtCheckMilestone:
    """The common TOBT-feasibility check and TTOT-tolerance notification performed at each milestone from Local Radar Update through Final Confirmation of the TOBT: verify that TOBT is consistent with the ATC Flight Plan and inform Network Operations when TTOT changes by more than the agreed tolerance.

    Package Milestones, stereotype control, milestones [4, 5, 6, 7, 8, 9].
    """

    def checkTobtConsistency(self, tobt: datetime, atcFlightPlan: FlightPlan) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan; shall be performed to verify feasibility of the ATC Flight Plan given the updated TOBT (milestones 4-9)."""
        raise NotImplementedError

    def informNetworkOperationsOfTtotChange(self, newTtot: datetime, tolerance: timedelta) -> None:
        """Network Operations is informed when the TTOT changes by more than the agreed TTOT tolerance (milestones 4-9)."""
        raise NotImplementedError


@dataclass
class FinalApproachMilestone(TobtCheckMilestone):
    """Milestone 5: commences the TOBT process on radar detection of the flight on final approach.

    Package Milestones, stereotype control, milestones [5].

    Relationship: dependency 'commences TOBT process for' -> Flight

    Relationship: dependency 'checks TOBT against' -> FlightPlan

    Relationship: dependency 'informs of TTOT change' -> NetworkOperations

    Relationship: dependency 'triggered by' -> RadarSystem
    """

    def commenceTobtProcess(self, flight: Flight) -> None:
        """Commences the TOBT process; triggered by the detection of the flight by radar in either FIR, TMA, or on Final Approach."""
        raise NotImplementedError


@dataclass
class FinalTobtConfirmationMilestone(TobtCheckMilestone):
    """Milestone 9: checks that the AO/GH's most accurate TOBT, provided t minutes before EOBT, is consistent with the ATC Flight Plan prior to TSAT issue.

    Package Milestones, stereotype control, milestones [9].

    Relationship: dependency 'confirms TOBT for' -> Flight

    Relationship: dependency 'checks feasibility against' -> FlightPlan

    Relationship: dependency 'informs of TTOT change' -> NetworkOperations

    Relationship: dependency 'triggers EXOT calculation by' -> AtcSystem

    Relationship: dependency 'is constantly applicable in' -> AirportCdmPlatform
    """
    localParameterT: timedelta | None = None

    def confirmTobt(self, tobt: datetime, wasManuallyModified: bool) -> bool:
        """Triggered by a new TOBT or TTOT update; no need to confirm an existing TOBT if it has been manually modified before."""
        raise NotImplementedError


@dataclass
class Flight:
    """A single scheduled arrival or departure operation of an aircraft, carrying an operational status that changes at each milestone.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'operated with' -> Aircraft [1]

    Relationship: association 'described by' -> FlightPlan [1]

    Relationship: composition 'has off-block time history' -> OffBlockTime [0..*]

    Relationship: composition 'has landing time history' -> LandingTime [0..*]

    Relationship: composition 'has in-block time history' -> InBlockTime [0..*]

    Relationship: composition 'has take-off time history' -> TakeOffTime [0..*]

    Relationship: composition 'has start-up approval time history' -> StartUpApprovalTime [0..*]

    Relationship: composition 'has start-up request time' -> StartUpRequestTime [0..1]

    Relationship: composition 'has ready time' -> ReadyTime [0..1]

    Relationship: composition 'has boarding time' -> BoardingTime [0..1]

    Relationship: composition 'has ground handling time' -> GroundHandlingTime [0..1]

    Relationship: aggregation 'has estimated taxi times' -> TaxiTime [0..2]

    Relationship: aggregation 'uses minimum turn-round time' -> MinimumTurnRoundTime [0..1]
    """
    operationalStatus: FlightOperationalStatus | None = None
    regulated: bool | None = None


@dataclass
class FlightCrew:
    """The pilot and aircrew who request start-up, coordinate boarding and turn-round management, and receive TSAT confirmation.

    Package Stakeholders, stereotype entity, milestones [9, 12, 13, 14].

    Relationship: association 'requests start-up' -> StartUpRequestTime [0..1]

    Relationship: association 'sends' -> DepartureClearanceMessage [0..1]
    """
    pass


@dataclass
class FlightPlan:
    """The ICAO ATC flight plan submitted for a flight, possibly as part of a repetitive flight plan (RFPL), describing departure and destination aerodromes.

    Package Flights, stereotype entity, milestones [1, 3].

    Relationship: association 'corresponds to' -> AirportSlot [0..1]

    Relationship: association 'departure aerodrome' -> Aerodrome [1]

    Relationship: association 'destination aerodrome' -> Aerodrome [1]
    """
    isRepetitive: bool | None = None
    estimatedElapsedTime: timedelta | None = None


@dataclass
class FlightPlanActivationMilestone:
    """Milestone 1: checks consistency between the ATC Flight Plan, airport slot, and airport flight data, and confirms the flight to Network Operations before the first E-DPI.

    Package Milestones, stereotype control, milestones [1].

    Relationship: dependency 'initiates and updates status of' -> Flight

    Relationship: dependency 'checks consistency of' -> FlightPlan

    Relationship: dependency 'checks consistency against' -> AirportSlot

    Relationship: dependency 'checks consistency of' -> Aircraft

    Relationship: dependency 'confirms flight to' -> NetworkOperations

    Relationship: dependency 'commences on' -> AirportCdmPlatform
    """
    triggerOffset: timedelta | None = None

    def checkConsistency(self, atcFlightPlan: FlightPlan, airportSlot: AirportSlot, aircraft: Aircraft) -> bool:
        """Checks consistency between ATC Flight Plan, Airport Slot and Airport flight data; shall be performed to verify this consistency before the first E-DPI is sent."""
        raise NotImplementedError

    def confirmFlightToNetworkOperations(self, flight: Flight) -> None:
        """Confirms the flight to the Network Operations and allows further local processing of the flight."""
        raise NotImplementedError

    def triggerOnActivationOrResubmission(self, eobt: datetime, isNewOrLateSubmission: bool) -> None:
        """Process is triggered by the first activation of the ATC Flight Plan (earliest EOBT-3 hr), or new or late submissions of the ATC Flight Plan, after cancellation or revised EOBT."""
        raise NotImplementedError

    def updateArrivalOrDepartureTimings(self, flight: Flight) -> None:
        """ELDT and EIBT updated for an arrival; EOBT and ETOT updated for a departure."""
        raise NotImplementedError


@dataclass
class FlightUpdateMessage:
    """The FUM sent by Network Operations providing updates of a flight's progress used to update ELDT.

    Package Messages, stereotype boundary, milestones [2, 3].
    """
    pass


@dataclass
class GroundHandler:
    """The party performing turn-round and ground handling operations on behalf of, or alongside, the Aircraft Operator.

    Package Stakeholders, stereotype entity, milestones [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13].

    Relationship: association 'manages' -> TurnRound [*]
    """
    pass


@dataclass
class GroundHandlingStartedMilestone(TobtCheckMilestone):
    """Milestone 8: on ACGT, for first-of-day or long-parked flights, updates the TOBT for the departing flight based on the turn-round period.

    Package Milestones, stereotype control, milestones [8].

    Relationship: dependency 'checks TOBT for' -> Flight

    Relationship: dependency 'checks feasibility against' -> FlightPlan

    Relationship: dependency 'informs of TTOT change' -> NetworkOperations

    Relationship: dependency 'uses turn-round period to update TOBT' -> TurnRound
    """

    def triggerTobtUpdateFromAcgt(self, acgt: datetime, turnRoundPeriod: timedelta) -> None:
        """The occurrence of ACGT triggers an update of downstream estimates: TOBT is updated automatically or inserted manually by the Aircraft Operator/Ground Handler, calculated on the basis of the estimated turn-round period for the departing flight."""
        raise NotImplementedError


@dataclass
class GroundHandlingTime:
    """The actual commence of ground handling time (ACGT), applicable to first-of-day or long-parked flights.

    Package Timings, stereotype entity, milestones [7, 8].
    """
    value: datetime | None = None
    originator: str | None = None
    timeOfUpdate: datetime | None = None
    accuracy: timedelta | None = None


@dataclass
class Ifps:
    """The Integrated Initial Flight Plan Processing System that distributes the submitted ATC flight plan to all involved ATC units.

    Package Stakeholders, stereotype entity, milestones [1].

    Relationship: association 'distributes flight plan to' -> AirTrafficControlUnit [*]

    Relationship: dependency 'distributes' -> FlightPlan
    """

    def distributeFlightPlan(self, flightPlan: FlightPlan) -> None:
        """The ATC Flight Plan is submitted by the Aircraft Operator and distributed by the IFPS; all involved ATC units receive the flight plan, including departure and destination aerodromes."""
        raise NotImplementedError


@dataclass
class InBlockMilestone(TobtCheckMilestone):
    """Milestone 7: on AIBT, updates downstream time estimates for the departing flight based on the turn-round period.

    Package Milestones, stereotype control, milestones [7].

    Relationship: dependency 'checks TOBT for' -> Flight

    Relationship: dependency 'checks feasibility against' -> FlightPlan

    Relationship: dependency 'informs of TTOT change' -> NetworkOperations

    Relationship: dependency 'uses turn-round period to update TOBT' -> TurnRound
    """

    def triggerDownstreamUpdatesFromAibt(self, aibt: datetime, turnRoundPeriod: timedelta) -> None:
        """The occurrence of AIBT should trigger an update of downstream estimates: TOBT and TTOT are updated automatically or inserted manually by the Aircraft Operator/Ground Handler, calculated on the basis of the estimated turn-round period for the departing flight."""
        raise NotImplementedError


@dataclass
class InBlockTime:
    """A time quantity for the in-block event (EIBT or AIBT), recorded with its prefix, origin, and time of update.

    Package Timings, stereotype entity, milestones [1, 3, 4, 6, 7].
    """
    prefix: TimePrefix | None = None
    value: datetime | None = None
    originator: str | None = None
    timeOfUpdate: datetime | None = None
    accuracy: timedelta | None = None

    def calculateFromEldt(self, eldt: datetime, exit: timedelta) -> datetime:
        """An estimated in-block time (EIBT) is computed using the ELDT and the estimated taxi-in time."""
        raise NotImplementedError

    def calculateFromAldt(self, aldt: datetime, exit: timedelta) -> datetime:
        """The EIBT can be updated according to the ALDT + EXIT."""
        raise NotImplementedError


@dataclass
class LandedMilestone(TobtCheckMilestone):
    """Milestone 6: on ALDT, updates downstream time estimates for the departing flight based on the turn-round period.

    Package Milestones, stereotype control, milestones [6].

    Relationship: dependency 'checks TOBT for' -> Flight

    Relationship: dependency 'checks feasibility against' -> FlightPlan

    Relationship: dependency 'informs of TTOT change' -> NetworkOperations

    Relationship: dependency 'uses turn-round period to update TOBT' -> TurnRound
    """

    def triggerDownstreamUpdatesFromAldt(self, aldt: datetime, turnRoundPeriod: timedelta) -> None:
        """The occurrence of ALDT triggers an update of downstream estimates: TOBT and TTOT are updated automatically or inserted manually by the Aircraft Operator/Ground Handler, calculated on the basis of the defined turn-round period for the departing flight."""
        raise NotImplementedError


@dataclass
class LandingTime:
    """A time quantity for the landing event (ELDT or ALDT), recorded with its prefix, origin, and time of update.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6].

    Relationship: dependency 'updates from' -> FlightUpdateMessage
    """
    prefix: TimePrefix | None = None
    value: datetime | None = None
    originator: str | None = None
    timeOfUpdate: datetime | None = None
    accuracy: timedelta | None = None

    def updateFromFum(self, fum: FlightUpdateMessage) -> None:
        """For inbound flights, ELDT is updated based on information provided by the FUM messages, taking into account the actual progress of the flight."""
        raise NotImplementedError

    def calculateFromAtot(self, atot: datetime, estimatedElapsedTime: timedelta) -> datetime:
        """If the departure airport is more than 3hrs flying time from the destination airport, an ELDT can be calculated by using the ATOT and the Estimated Elapsed Time on the FPL."""
        raise NotImplementedError


@dataclass
class LocalRadarUpdateMilestone(TobtCheckMilestone):
    """Milestone 4: commences the TOBT process on radar detection of the flight in the FIR, checking TOBT feasibility and TTOT tolerance, and constrains stand/gate changes near ELDT.

    Package Milestones, stereotype control, milestones [4].

    Relationship: dependency 'commences TOBT process for' -> Flight

    Relationship: dependency 'checks TOBT against' -> FlightPlan

    Relationship: dependency 'informs of TTOT change' -> NetworkOperations

    Relationship: dependency 'triggered by' -> RadarSystem

    Relationship: dependency 'runs within' -> AirportCdmPlatform
    """

    def commenceTobtProcess(self, flight: Flight) -> None:
        """Commences the TOBT process; triggered by the detection of the flight by radar in either FIR, TMA, or on Final Approach."""
        raise NotImplementedError

    def checkStandGateChangeAllowed(self, eldt: datetime, exit: timedelta) -> bool:
        """Taking into account the taxi-in time (EXIT), any change to a stand or gate is not preferred after ELDT-30'."""
        raise NotImplementedError


@dataclass
class MinimumTurnRoundTime:
    """The minimum turn-round time (MTTT) defined for an aircraft type, used as a calculation basis for TTOT.

    Package Timings, stereotype entity, milestones [2, 3].
    """
    duration: timedelta | None = None


@dataclass
class NetworkOperations:
    """The network management function that issues CTOT, receives DPI messages, and monitors flight progress via ETFMS/FUM.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15].

    Relationship: association 'monitors flight progress via' -> EtfmsSystem [1]

    Relationship: association 'issues CTOT' -> TakeOffTime [*]

    Relationship: dependency 'issues CTOT for' -> Flight

    Relationship: dependency 'receives' -> DpiMessage
    """

    def issueCtot(self, flight: Flight, eobt: datetime) -> datetime:
        """The CTOT is issued by the Network Operations and sent to relevant ATS units as well as the departure aerodrome; if the flight is regulated, a CTOT is issued at EOBT-2h."""
        raise NotImplementedError


@dataclass
class OffBlockMilestone:
    """Milestone 15: informs partners of the Actual Off-Block Time, updates TTOT considering EXOT, and triggers an A-DPI message to Network Operations.

    Package Milestones, stereotype control, milestones [15].

    Relationship: dependency 'informs partners of off-block for' -> Flight

    Relationship: dependency 'informs via A-DPI' -> NetworkOperations

    Relationship: dependency 'sends' -> DpiMessage

    Relationship: dependency 'records in' -> AirportCdmPlatform
    """

    def informPartnersOfAobt(self, aobt: datetime) -> None:
        """Informs all relevant Airport CDM Partners of Actual Off-Block Time (AOBT) in the Airport CDM Platform and that the aircraft has commenced push-back / taxi from parking position."""
        raise NotImplementedError

    def updateTtotConsideringExot(self, exot: timedelta) -> datetime:
        """TTOT updated considering the EXOT."""
        raise NotImplementedError

    def sendADpi(self, flight: Flight, isRemoteHolding: bool) -> None:
        """AOBT always triggers an A-DPI message to Network Operations or, in the case of remote holding, at a defined time prior to TTOT."""
        raise NotImplementedError

    def checkTtotToleranceAndSendADpi(self, newTtot: datetime, tolerance: timedelta) -> None:
        """After a first A-DPI is sent this check shall be performed to check TTOT updates against the TTOT tolerance before Network Operations is informed, with a new A-DPI, of the updated TTOT."""
        raise NotImplementedError


@dataclass
class OffBlockTime:
    """A time quantity for the off-block event (SOBT, EOBT, TOBT, or AOBT), recorded with its prefix, origin, and time of update; every successive value is kept.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15].
    """
    prefix: TimePrefix | None = None
    value: datetime | None = None
    originator: str | None = None
    timeOfUpdate: datetime | None = None
    accuracy: timedelta | None = None


@dataclass
class PassengerInformationSystem:
    """The airport system, flight information display system (FIDS), or public address system used to inform passengers of boarding.

    Package Systems, stereotype boundary, milestones [11].

    Relationship: association 'records boarding start' -> BoardingTime [*]
    """
    pass


@dataclass
class RadarSystem:
    """The radar system that detects a flight by its assigned SSR code when it crosses a FIR/ATC boundary, a defined range/position, or a predetermined level.

    Package Systems, stereotype boundary, milestones [4, 5].

    Relationship: association 'detects' -> Flight [*]
    """

    def detectFlight(self, ssrCode: str, boundaryOrPositionOrLevel: str) -> None:
        """The radar system is able to detect a flight based upon the assigned SSR code when the flight crosses a defined FIR/ATC boundary (milestone 4), or crosses either a defined range/position or passes/leaves a predetermined level (milestone 5)."""
        raise NotImplementedError


@dataclass
class ReadyStatusMessage:
    """The RDY message confirming that the aircraft is ready and follows the indicated TOBT.

    Package Messages, stereotype boundary, milestones [12].
    """
    pass


@dataclass
class ReadyTime:
    """The actual time at which the aircraft is ready for start-up/push-back (ARDT), recorded with its origin and time of update.

    Package Timings, stereotype entity, milestones [12].
    """
    value: datetime | None = None
    originator: str | None = None
    timeOfUpdate: datetime | None = None
    accuracy: timedelta | None = None
    tolerance: timedelta | None = None


@dataclass
class TtotCalculationMilestone:
    """The common TTOT calculation rule shared by the EOBT-2hr check and the take-off-from-outstation check: TTOT is based on EIBT+MTTT+EXOT (or EOBT+EXOT if later), overridden by TOBT+EXOT once TOBT is available.

    Package Milestones, stereotype control, milestones [2, 3].
    """

    def calculateTtot(self, eibt: datetime, mttt: timedelta, exot: timedelta, eobt: datetime, tobt: datetime) -> datetime:
        """Calculation basis for the TTOT takes into account EIBT+MTTT+EXOT, compared against EOBT+EXOT (the later of the two applies); in the case of manual input of TOBT, or once TOBT is available, this prediction overrides the EIBT+MTTT estimate, hence TTOT equals TOBT+EXOT (milestones 2 and 3)."""
        raise NotImplementedError


@dataclass
class RegulationCheckMilestone(TtotCalculationMilestone):
    """Milestone 2 (EOBT-2hr): checks AO/GH flight estimates against the ATC Flight Plan, determines CTOT for regulated flights, and informs Network Operations via a T-DPI message.

    Package Milestones, stereotype control, milestones [2].

    Relationship: dependency 'checks and marks regulated' -> Flight

    Relationship: dependency 'checks estimates against' -> FlightPlan

    Relationship: dependency 'informs via T-DPI' -> NetworkOperations

    Relationship: dependency 'sends' -> DpiMessage

    Relationship: dependency 'runs within' -> AirportCdmPlatform
    """
    triggerOffset: timedelta | None = None

    def checkFlightEstimatesConsistency(self, estimates: str, atcFlightPlan: FlightPlan) -> bool:
        """Checks (before or after take off from outstation) whether AO/GH flight estimates are consistent with the ATC Flight Plan; shall be performed to verify feasibility of the ATC Flight Plan estimated off block time at EOBT-2 hrs."""
        raise NotImplementedError

    def informNetworkOperationsViaTDpi(self, flight: Flight) -> None:
        """At EOBT-2 hrs Network Operations is informed through the first T-DPI message about the updated take off time estimate."""
        raise NotImplementedError

    def markFieldsAsRegulated(self, flight: Flight) -> None:
        """Marks appropriate fields as REGULATED for a flight that has received a CTOT, setting the flight's regulated attribute."""
        raise NotImplementedError


@dataclass
class StandGateManagement:
    """The stakeholder responsible for stand and gate allocation, sharing EOBT and reacting to stand/gate change decisions.

    Package Stakeholders, stereotype entity, milestones [4, 9].

    Relationship: association 'manages stand/gate for' -> Flight [*]

    Relationship: association 'shares EOBT with' -> OffBlockTime [*]
    """
    pass


@dataclass
class StartUpApprovalTime:
    """A time quantity for the start-up approval event (TSAT or ASAT), recorded with its prefix, origin, and time of update.

    Package Timings, stereotype entity, milestones [9, 10, 12, 13, 14].
    """
    prefix: TimePrefix | None = None
    value: datetime | None = None
    originator: str | None = None
    timeOfUpdate: datetime | None = None
    accuracy: timedelta | None = None
    tolerance: timedelta | None = None


@dataclass
class StartUpApprovedMilestone:
    """Milestone 14: informs partners of the Actual Start-Up Approval Time and checks and alerts if approval is not aligned with or granted by TSAT tolerance.

    Package Milestones, stereotype control, milestones [14].

    Relationship: dependency 'resequences' -> Flight

    Relationship: dependency 'triggered by' -> DepartureClearanceMessage

    Relationship: dependency 'records in' -> AirportCdmPlatform
    """

    def informPartnersOfAsat(self, asat: datetime) -> None:
        """Informs all relevant Airport CDM Partners of Actual start up approval Time (ASAT) in the Airport CDM Platform and that the aircraft has received start up approval / push-back clearance."""
        raise NotImplementedError

    def checkAsatAgainstTsat(self, asat: datetime, tsat: datetime, tolerance: timedelta) -> bool:
        """Checks if ASAT is in accordance to TSAT and alerts all relevant Airport CDM Partners when no start up has been granted; in case the start up approval is not granted at TSAT + tolerance, all relevant partners should be informed."""
        raise NotImplementedError

    def resequenceFlight(self, flight: Flight) -> None:
        """The flight will be re-sequenced when start up approval is not granted at TSAT + tolerance."""
        raise NotImplementedError


@dataclass
class StartUpRequestTime:
    """The actual time at which start-up is requested (ASRT), recorded with its origin and time of update.

    Package Timings, stereotype entity, milestones [13].
    """
    value: datetime | None = None
    originator: str | None = None
    timeOfUpdate: datetime | None = None
    accuracy: timedelta | None = None
    toleranceWindow: timedelta | None = None


@dataclass
class StartUpRequestedMilestone:
    """Milestone 13: informs partners of the Actual Start-Up Request Time and alerts partners if no start-up request is made within the TSAT tolerance window.

    Package Milestones, stereotype control, milestones [13].

    Relationship: dependency 'informs partners of start-up request for' -> Flight

    Relationship: dependency 'triggered by request from' -> FlightCrew

    Relationship: dependency 'records in' -> AirportCdmPlatform
    """

    def informPartnersOfAsrt(self, asrt: datetime) -> None:
        """Informs all relevant Airport CDM Partners of Actual Start up Request Time (ASRT) in the Airport CDM Platform."""
        raise NotImplementedError

    def checkStartUpRequestedWithinTolerance(self, tsat: datetime, tolerance: timedelta) -> bool:
        """If the start up request is not made by TSAT + tolerance, the AO/GH is informed that no start up has been requested, and should update TOBT."""
        raise NotImplementedError


@dataclass
class TakeOffFromOutstationMilestone(TtotCalculationMilestone):
    """Milestone 3: checks estimated landing times after take-off from the outstation against the outbound ATC Flight Plan and informs Network Operations via a T-DPI-t message.

    Package Milestones, stereotype control, milestones [3].

    Relationship: dependency 'checks estimates for' -> Flight

    Relationship: dependency 'checks consistency against outbound' -> FlightPlan

    Relationship: dependency 'informs via T-DPI-t' -> NetworkOperations

    Relationship: dependency 'sends' -> DpiMessage
    """

    def checkLandingEstimatesConsistency(self, estimatedLandingTime: datetime, outboundFlightPlan: FlightPlan) -> bool:
        """Checks whether the AO/GH estimated landing time after take off from outstation is consistent with the outbound ATC Flight Plan; shall be performed to verify feasibility of the ATC Flight Plan at take off from outstation."""
        raise NotImplementedError

    def informNetworkOperationsViaTDpiT(self, flight: Flight) -> None:
        """When needed, informs the Network Operations about the updated take off time estimates using a T-DPI-t Message; a TTOT tolerance of 5 minutes is respected before Network Operations is informed of the updated TTOT."""
        raise NotImplementedError


@dataclass
class TakeOffMilestone:
    """Milestone 16: informs partners of the actual take-off, generates an airborne message, sends FSA and MVT messages, and removes the flight from the departure sequence.

    Package Milestones, stereotype control, milestones [16].

    Relationship: dependency 'removes from departure sequence' -> Flight

    Relationship: dependency 'sends' -> TakeOffNotificationMessage

    Relationship: dependency 'triggered by' -> AcarsSystem

    Relationship: dependency 'triggered by' -> RadarSystem
    """

    def informPartnersOfTakeOff(self, atot: datetime) -> None:
        """Informs all relevant Airport CDM Partners about the actual take off."""
        raise NotImplementedError

    def generateAirborneMessageAndRemoveFromSequence(self, flight: Flight) -> None:
        """An airborne message is generated and the flight is removed from the departure sequence."""
        raise NotImplementedError

    def sendFsaAndMvt(self, flight: Flight) -> None:
        """FSA and MVT messages are sent."""
        raise NotImplementedError


@dataclass
class TakeOffNotificationMessage:
    """A notification message sent at take-off (FSA, MVT, or airborne message) informing partners and Network Operations of the actual take-off.

    Package Messages, stereotype boundary, milestones [16].
    """
    type: TakeOffNotificationType | None = None


@dataclass
class TakeOffTime:
    """A time quantity for the take-off event (ETOT, TTOT, CTOT, or ATOT), recorded with its prefix, origin, and time of update.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 16].
    """
    prefix: TimePrefix | None = None
    value: datetime | None = None
    originator: str | None = None
    timeOfUpdate: datetime | None = None
    accuracy: timedelta | None = None
    tolerance: timedelta | None = None


@dataclass
class TaxiTime:
    """An estimated taxi duration, either taxi-out (EXOT) or taxi-in (EXIT), used in the calculation of other time quantities.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 6, 9].
    """
    type: str | None = None
    duration: timedelta | None = None
    calculationBasis: str | None = None


@dataclass
class TsatIssuedMilestone:
    """Milestone 10: informs partners of the TSAT allocated to the flight and checks whether TOBT updates after TSAT issue exceed a locally defined tolerance.

    Package Milestones, stereotype control, milestones [10].

    Relationship: dependency 'informs partners of TSAT for' -> Flight

    Relationship: dependency 'informs via T-DPI-s' -> NetworkOperations

    Relationship: dependency 'sends' -> DpiMessage
    """
    localParameterT: timedelta | None = None

    def informPartnersOfTsat(self, tsat: datetime) -> None:
        """Informs all relevant partners of the TSAT that has been allocated to the flight."""
        raise NotImplementedError

    def informNetworkOperationsViaTDpiS(self, flight: Flight) -> None:
        """The Network Operations is informed by a T-DPI-s for non regulated flights."""
        raise NotImplementedError

    def checkTobtUpdateCountAfterTsat(self, updateCount: int, threshold: int) -> bool:
        """A check shall be performed to see the number of TOBT updates after TSAT has been issued. In case the number of TOBT updates exceeds a threshold, then the TOBT input should be processed according to local procedure."""
        raise NotImplementedError


@dataclass
class TurnRound:
    """The aircraft turn-round linking an arriving flight and its related departing flight, including the defined turn-round period.

    Package Flights, stereotype entity, milestones [1, 6, 7, 8].

    Relationship: aggregation 'arriving flight' -> Flight [1]

    Relationship: aggregation 'departing flight' -> Flight [1]
    """
    turnRoundPeriod: timedelta | None = None
