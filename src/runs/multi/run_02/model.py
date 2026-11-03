"""Class stubs rendered from runs/multi/run_02/model.json by src/generate/render_code.py; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from enum import Enum


class DpiMessageType(Enum):
    E_DPI = "E-DPI"
    T_DPI = "T-DPI"
    T_DPI_T = "T-DPI-t"
    T_DPI_S = "T-DPI-s"
    A_DPI = "A-DPI"


class FlightOperationalStatus(Enum):
    INITIATED = "INITIATED"
    REGULATED = "REGULATED"
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


class TimeQuantityPrefix(Enum):
    SCHEDULED = "Scheduled"
    ESTIMATED = "Estimated"
    TARGET = "Target"
    ACTUAL = "Actual"
    CALCULATED = "Calculated"


@dataclass
class AcarsSystem:
    """The aircraft's ACARS reporting system that provides landing, in-block, off-block, and take-off events directly from the aircraft.

    Package Systems, stereotype boundary, milestones [6, 7, 15, 16].
    """
    pass


@dataclass
class AirportCdmPartner:
    """A generic party in the Airport CDM process that originates or receives flight information and notifications.

    Package Stakeholders, stereotype entity, milestones [1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    pass


@dataclass
class AirTrafficControlUnit(AirportCdmPartner):
    """An air traffic control body, including the tower, Area Control Centre, and Approach Control Unit, that manages the flight's sequencing and clearances.

    Package Stakeholders, stereotype entity, milestones [1, 2, 4, 5, 9, 10, 12, 13, 14, 16].

    Relationship: association 'receives' -> FlightPlan [*]

    Relationship: association 'issues TSAT' -> TsatIssued

    Relationship: association 'confirms TSAT' -> StartUpRequested

    Relationship: association 'approves start up' -> StartUpApproved

    Relationship: association 'refines pre-departure sequence' -> AircraftReady

    Relationship: association 'detects' -> LocalRadarUpdate

    Relationship: association 'detects' -> FinalApproach

    Relationship: association 'detects' -> TakeOff
    """
    pass


@dataclass
class AirborneMessage:
    """The message generated on take-off confirming the flight is airborne and removing it from the departure sequence.

    Package Messages, stereotype boundary, milestones [16].
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
class AircraftOperator(AirportCdmPartner):
    """The airline or its representative that submits the ATC Flight Plan and provides TOBT and other flight estimates.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 13].

    Relationship: association 'submits' -> FlightPlan [1..*]

    Relationship: association 'provides TOBT' -> Landed

    Relationship: association 'provides TOBT' -> InBlock

    Relationship: association 'provides TOBT' -> GroundHandlingStarted

    Relationship: association 'confirms TOBT' -> FinalConfirmationOfTobt
    """

    def provideFlightData(self, sobt: datetime, aircraftRegistration: str, firstDestination: str) -> None:
        """The AO must provide correct information before the first E-DPI message, in order to feed Network Operations with consistent SOBT, aircraft registration, and first destination data, as early in time as possible."""
        raise NotImplementedError


@dataclass
class AircraftReady:
    """Milestone 12: informs partners of Actual Ready Time and alerts the AO/GH if TOBT has passed without a ready status being received.

    Package Milestones, stereotype control, milestones [12].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'uses' -> AirportCdmPlatform

    Relationship: dependency 'checks for' -> ReadyStatusMessage
    """
    readyTolerance: timedelta | None = None

    def informArdt(self, flight: Flight, ardt: datetime) -> None:
        """Informs all relevant Airport CDM Partners of Actual Ready Time (ARDT) in the Airport CDM Platform and that the aircraft is ready for start up/push-back."""
        raise NotImplementedError

    def checkReadyStatusReceived(self, flight: Flight) -> bool:
        """Informs the AO/GH that TOBT has passed and the Airport CDM Platform has not yet received ARDT or Ready Status (RDY); at TOBT + tolerance the AO/GH are informed that TOBT has passed and there has not been a ready status message yet."""
        raise NotImplementedError


@dataclass
class AirportCdmPlatform:
    """The central Airport CDM system that holds flight information, performs consistency checks, computes and updates time estimates, and triggers notifications throughout the process.

    Package Systems, stereotype control, milestones [1, 2, 4, 9, 10, 11, 12, 13, 14, 15].
    """

    def markRegulated(self, flight: Flight) -> None:
        """Marks appropriate fields as REGULATED and updates ETOT/TTOT/CTOT."""
        raise NotImplementedError

    def calculateTobtFromEldt(self, flight: Flight, eldt: LandingTime) -> datetime:
        """Update of the ELDT can trigger a new TOBT to be entered by the AO/GH, or calculated automatically by the Airport CDM Platform."""
        raise NotImplementedError


@dataclass
class AirportSlot:
    """The airport slot programme entry against which the ATC Flight Plan's consistency is checked.

    Package Flights, stereotype entity, milestones [1].
    """
    slotTime: datetime | None = None


@dataclass
class AtcSystem:
    """The ATC ground system that calculates the Estimated Taxi-Out Time based on traffic load, stand/gate location, runway in use, and holding position wait.

    Package Systems, stereotype boundary, milestones [9].
    """

    def calculateExot(self, flight: Flight) -> timedelta:
        """Following the receipt of the TOBT, the ATC system calculates and provides the Estimated Taxi-Out Time (EXOT) based on the predicted traffic load, gate/stand location, runway in use, and waiting period at the Holding Position, etc."""
        raise NotImplementedError


@dataclass
class BoardingStarts:
    """Milestone 11: informs partners of Actual Start Boarding Time and checks whether boarding starts in time to respect TOBT.

    Package Milestones, stereotype control, milestones [11].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'uses' -> AirportCdmPlatform

    Relationship: dependency 'distinguished from' -> FidsSystem
    """
    boardingCheckOffset: timedelta | None = None

    def informAsbt(self, flight: Flight, asbt: datetime) -> None:
        """Informs all relevant Airport CDM Partners of Actual Start Boarding Time (ASBT) when it occurs."""
        raise NotImplementedError

    def checkBoardingStatus(self, flight: Flight) -> bool:
        """Checks whether boarding starts in time to respect TOBT and informs the AO/GH in case TOBT needs to be updated; at a certain time before TOBT (local variable e.g. corresponding to aircraft type) a check shall be performed to check the boarding status."""
        raise NotImplementedError


@dataclass
class TimeQuantity:
    """A general time value describing a flight's progress toward or through a milestone event, carrying its prefix, origin, accuracy, and successive updates.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'originated by' -> AirportCdmPartner [1]
    """
    value: datetime | None = None
    prefix: TimeQuantityPrefix | None = None
    originator: AirportCdmPartner | None = None
    recordedAt: datetime | None = None
    accuracy: timedelta | None = None


@dataclass
class BoardingTime(TimeQuantity):
    """The actual time passengers start boarding the aircraft (ASBT).

    Package Timings, stereotype entity, milestones [11].
    """
    pass


@dataclass
class DepartureClearanceMessage:
    """The voice or DCL message by which flight crew request start-up approval.

    Package Messages, stereotype boundary, milestones [14].
    """
    pass


@dataclass
class DpiMessage:
    """A Departure Planning Information message (E-DPI, T-DPI, T-DPI-t, T-DPI-s, or A-DPI) sent to Network Operations to convey flight time estimates.

    Package Messages, stereotype boundary, milestones [1, 2, 3, 10, 15].

    Relationship: association 'sent to' -> NetworkOperations [1]
    """
    messageType: DpiMessageType | None = None


@dataclass
class DpiProcess:
    """The process that commences correct DPI messaging with Network Operations when implemented.

    Package Systems, stereotype control, milestones [1].

    Relationship: dependency 'commences messaging with' -> NetworkOperations

    Relationship: association 'sends' -> DpiMessage [*]
    """

    def commenceMessaging(self, flight: Flight) -> None:
        """The DPI process commences the correct messaging with Network Operations (if implemented)."""
        raise NotImplementedError

    def canSendEDpi(self, flightPlan: FlightPlan) -> bool:
        """The E-DPI message should not be sent if no or inconsistent information is provided."""
        raise NotImplementedError


@dataclass
class EobtMinus2Hours:
    """Milestone 2: checks flight estimates against the ATC Flight Plan at EOBT-2 hours, issues CTOT for regulated flights, and informs Network Operations via the first T-DPI message.

    Package Milestones, stereotype control, milestones [2].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'uses' -> AirportCdmPlatform

    Relationship: association 'sends' -> DpiMessage [1]

    Relationship: association 'informs' -> NetworkOperations
    """
    ctotIssuanceOffset: timedelta | None = None

    def checkEstimatesConsistency(self, flight: Flight) -> bool:
        """Checks (before or after take off from outstation) whether AO/GH flight estimates are consistent with the ATC Flight Plan and informs Network Operations about the updated take off time estimate, using a T-DPI Message; this check shall be performed to verify feasibility of the ATC Flight Plan estimated off block time at EOBT-2 hrs."""
        raise NotImplementedError

    def informFirstTdpi(self, flight: Flight) -> None:
        """At EOBT-2 hrs Network Operations is informed through the first T-DPI message."""
        raise NotImplementedError

    def calculateTtot(self, eibt: datetime, mttt: timedelta, exot: timedelta, eobt: datetime, tobt: datetime) -> datetime:
        """Calculation basis for the TTOT shall take into account EIBT+MTTT+EXOT, if later than EOBT+EXOT. In the case of manual input of TOBT, this estimate will override the EIBT+MTTT estimate, hence TTOT equals TOBT+EXOT."""
        raise NotImplementedError

    def updateInboundEldt(self, flight: Flight, fum: FlightUpdateMessage) -> None:
        """For inbound flights, ELDT is updated based on information provided by the FUM messages, taking into account the actual progress of the flight."""
        raise NotImplementedError


@dataclass
class EtfmsSystem:
    """The Enhanced Tactical Flow Management System used by Network Operations to monitor flight progress and generate Flight Update Messages.

    Package Systems, stereotype boundary, milestones [3].
    """
    pass


@dataclass
class FidsSystem:
    """The flight information display and public address system used to pre-call passengers, distinct from the physical start of boarding.

    Package Systems, stereotype boundary, milestones [11].
    """
    pass


@dataclass
class TobtFeasibilityCheckMilestone:
    """A common superclass for the milestone processes (radar update, final approach, landed, in-block, ground handling started, final TOBT confirmation) that check the AO/GH TOBT against the ATC Flight Plan and inform Network Operations when TTOT changes beyond the agreed tolerance.

    Package Milestones, stereotype control, milestones [4, 5, 6, 7, 8, 9].

    Relationship: association 'informs' -> NetworkOperations
    """
    ttotTolerance: timedelta | None = None

    def checkTobtConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan; performed to verify feasibility of the ATC Flight Plan given the updated TOBT or ATC Flight Plan."""
        raise NotImplementedError

    def informNetworkOperationsIfTtotChanged(self, flight: Flight) -> None:
        """Network Operations is informed when the TTOT changes by more than the agreed TTOT tolerance; the TTOT tolerance is respected before Network Operations is informed of updated TTOT."""
        raise NotImplementedError


@dataclass
class FinalApproach(TobtFeasibilityCheckMilestone):
    """Milestone 5: on entering final approach, commences the TOBT process and updates ELDT-based estimates.

    Package Milestones, stereotype control, milestones [5].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'triggered by' -> SurveillanceSystem
    """
    finalApproachWindow: timedelta | None = None

    def commenceTobtProcess(self, flight: Flight) -> None:
        """Commences the TOBT process and checks whether the AO/GH TOBT is consistent with the ATC Flight Plan."""
        raise NotImplementedError


@dataclass
class FinalConfirmationOfTobt(TobtFeasibilityCheckMilestone):
    """Milestone 9: at a locally agreed time before EOBT, confirms the AO/GH's most accurate TOBT and triggers ATC calculation of EXOT.

    Package Milestones, stereotype control, milestones [9].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'uses' -> AirportCdmPlatform

    Relationship: dependency 'requests EXOT from' -> AtcSystem

    Relationship: dependency 'shares EOBT with' -> StandGateManagement
    """
    confirmationOffset: timedelta | None = None

    def confirmTobt(self, flight: Flight, tobt: datetime) -> None:
        """The Aircraft Operator/Ground Handler provides their most accurate TOBT taking into account the operational situation, t minutes before EOBT (t is a parameter time agreed locally)."""
        raise NotImplementedError

    def introduceToPreDepartureSequence(self, flight: Flight) -> None:
        """The flight is introduced into the pre-departure sequence."""
        raise NotImplementedError

    def needsConfirmation(self, tobt: datetime) -> bool:
        """This process is triggered by a new TOBT or TTOT update. There is no need to confirm an existing TOBT if it has been manually modified before."""
        raise NotImplementedError


@dataclass
class Flight:
    """A single scheduled arrival or departure operation of an aircraft, tracked through the sixteen milestones with its operational status and time quantities.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'described by' -> FlightPlan [1]

    Relationship: association 'operated by' -> Aircraft [1]

    Relationship: composition 'has' -> OffBlockTime [0..*]

    Relationship: composition 'has' -> LandingTime [0..*]

    Relationship: composition 'has' -> InBlockTime [0..*]

    Relationship: composition 'has' -> TakeOffTime [0..*]

    Relationship: composition 'has' -> StartUpApprovalTime [0..*]

    Relationship: composition 'has' -> StartUpRequestTime [0..*]

    Relationship: composition 'has' -> ReadyTime [0..*]

    Relationship: composition 'has' -> BoardingTime [0..*]

    Relationship: composition 'has' -> GroundHandlingTime [0..*]

    Relationship: composition 'has' -> TaxiOutTime [0..*]

    Relationship: composition 'has' -> TaxiInTime [0..*]

    Relationship: composition 'has' -> TurnRoundTime [0..*]
    """
    operationalStatus: FlightOperationalStatus | None = None
    ssrCode: str | None = None


@dataclass
class FlightCrew(AirportCdmPartner):
    """The pilot and crew who request start-up approval and coordinate the turn-round with the ground handler.

    Package Stakeholders, stereotype entity, milestones [12, 13, 14].

    Relationship: association 'sends' -> DepartureClearanceMessage [0..1]

    Relationship: association 'requests start up' -> StartUpRequested

    Relationship: association 'coordinates with' -> GroundHandler
    """
    pass


@dataclass
class FlightPlan:
    """The ICAO/ATC Flight Plan submitted by the Aircraft Operator, possibly a repetitive flight plan, describing departure and destination aerodromes and other flight data.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 6, 7, 8, 9].

    Relationship: association 'checked against' -> AirportSlot [0..1]

    Relationship: dependency 'updates type/registration of' -> Aircraft
    """
    departureAerodrome: str | None = None
    destinationAerodrome: str | None = None
    isRepetitive: bool | None = None


@dataclass
class FlightPlanActivation:
    """Milestone 1: processes the activated ATC Flight Plan, checks its consistency with the Airport Slot and airport flight data, and confirms the flight for further processing.

    Package Milestones, stereotype control, milestones [1].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'initiates' -> AirportCdmPlatform

    Relationship: association 'sends' -> DpiMessage [1]

    Relationship: association 'confirms flight to' -> NetworkOperations
    """
    activationOffset: timedelta | None = None
    readinessOffset: timedelta | None = None

    def checkConsistency(self, flightPlan: FlightPlan, airportSlot: AirportSlot, flight: Flight) -> bool:
        """Checks consistency between the ATC Flight Plan, Airport Slot and Airport flight data before the first E-DPI is sent, and then confirms the flight to the Network Operations and allows further local processing of the flight."""
        raise NotImplementedError

    def activate(self, flightPlan: FlightPlan) -> None:
        """Triggered by the first activation of the ATC Flight Plan (earliest EOBT-3 hr), or by new or late submissions of the ATC Flight Plan, after cancellation or revised EOBT."""
        raise NotImplementedError

    def updateTimingsOnActivation(self, flight: Flight) -> None:
        """For an arrival, ELDT and EIBT are updated; for a departure, EOBT and ETOT are updated."""
        raise NotImplementedError

    def checkFlightReady(self, flight: Flight, plannedEobt: datetime) -> bool:
        """The flight is ready not later than 15 minutes after the planned EOBT."""
        raise NotImplementedError


@dataclass
class FlightStatusMessage:
    """The FSA message sent on actual take-off to inform relevant systems of the flight's status.

    Package Messages, stereotype boundary, milestones [16].
    """
    pass


@dataclass
class FlightUpdateMessage:
    """The FUM sent by Network Operations providing updates of an inbound flight's progress toward the destination.

    Package Messages, stereotype boundary, milestones [2, 3].
    """
    pass


@dataclass
class GroundHandler(AirportCdmPartner):
    """The party that performs and reports ground handling operations and turn-round estimates on behalf of the aircraft operator.

    Package Stakeholders, stereotype entity, milestones [6, 7, 8, 9, 10, 11, 12, 13].

    Relationship: association 'provides TOBT' -> Landed

    Relationship: association 'provides TOBT' -> InBlock

    Relationship: association 'provides TOBT' -> GroundHandlingStarted

    Relationship: association 'confirms TOBT' -> FinalConfirmationOfTobt

    Relationship: association 'manages turn-round' -> TsatIssued

    Relationship: association 'reports boarding' -> BoardingStarts

    Relationship: association 'reports ready' -> AircraftReady

    Relationship: association 'requests start up' -> StartUpRequested
    """
    pass


@dataclass
class GroundHandlingStarted(TobtFeasibilityCheckMilestone):
    """Milestone 8: on commencement of ground handling (ACGT), updates TOBT/TTOT based on the estimated turn-round period.

    Package Milestones, stereotype control, milestones [8].

    Relationship: association 'processes' -> Flight [1]
    """

    def updateTobt(self, flight: Flight) -> None:
        """The occurrence of ACGT triggers an update of downstream estimates: TOBT is updated automatically or inserted manually by the Aircraft Operator/Ground Handler, calculated on the basis of the estimated turn-round period for the departing flight."""
        raise NotImplementedError


@dataclass
class GroundHandlingTime(TimeQuantity):
    """The actual time ground handling operations commence for a flight (ACGT).

    Package Timings, stereotype entity, milestones [8].
    """
    pass


@dataclass
class Ifps(AirportCdmPartner):
    """The Integrated Initial Flight Plan Processing System party that distributes the submitted ATC Flight Plan to involved ATC units.

    Package Stakeholders, stereotype entity, milestones [1].

    Relationship: dependency 'distributes' -> FlightPlan
    """
    pass


@dataclass
class InBlock(TobtFeasibilityCheckMilestone):
    """Milestone 7: on actual in-block (AIBT), updates TOBT and TTOT based on the estimated turn-round period.

    Package Milestones, stereotype control, milestones [7].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'triggered by' -> SurveillanceSystem

    Relationship: dependency 'triggered by' -> AcarsSystem
    """

    def updateDownstreamEstimates(self, flight: Flight) -> None:
        """The occurrence of AIBT should trigger an update of downstream estimates: TOBT and TTOT are updated automatically or inserted manually by the Aircraft Operator/Ground Handler, calculated on the basis of the estimated turn-round period for the departing flight."""
        raise NotImplementedError


@dataclass
class InBlockTime(TimeQuantity):
    """The estimated or actual time an aircraft arrives in-blocks (EIBT, AIBT).

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 6, 7].
    """
    pass


@dataclass
class Landed(TobtFeasibilityCheckMilestone):
    """Milestone 6: on actual landing (ALDT), updates TOBT, TTOT and EIBT.

    Package Milestones, stereotype control, milestones [6].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'triggered by' -> SurveillanceSystem

    Relationship: dependency 'triggered by' -> AcarsSystem
    """

    def updateDownstreamEstimates(self, flight: Flight) -> None:
        """The occurrence of ALDT triggers an update of downstream estimates: TOBT and TTOT are updated automatically or inserted manually by the Aircraft Operator/Ground Handler, calculated on the basis of the defined turn-round period for the departing flight."""
        raise NotImplementedError

    def calculateEibt(self, aldt: datetime, exit: timedelta) -> datetime:
        """The EIBT can be updated according to the ALDT+EXIT."""
        raise NotImplementedError


@dataclass
class LandingTime(TimeQuantity):
    """The estimated or actual time an aircraft touches down (ELDT, ALDT).

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6].
    """
    pass


@dataclass
class LocalRadarUpdate(TobtFeasibilityCheckMilestone):
    """Milestone 4: on radar detection at the FIR boundary, commences the TOBT process and updates ELDT/EIBT/TOBT/TTOT.

    Package Milestones, stereotype control, milestones [4].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'uses' -> AirportCdmPlatform

    Relationship: dependency 'triggered by' -> SurveillanceSystem

    Relationship: dependency 'affects stand/gate decisions' -> StandGateManagement
    """
    standGateChangeCutoff: timedelta | None = None

    def commenceTobtProcess(self, flight: Flight) -> None:
        """Commences the TOBT process and checks whether the AO/GH TOBT is consistent with the ATC Flight Plan."""
        raise NotImplementedError

    def calculateEibt(self, eldt: datetime, exit: timedelta) -> datetime:
        """An estimated in-block time (EIBT) is computed using the ELDT and the estimated taxi-in time."""
        raise NotImplementedError

    def checkStandGateChangeAllowed(self, eldt: datetime, exit: timedelta, now: datetime) -> bool:
        """Taking into account the taxi-in time (EXIT), any change to a stand or gate is not preferred after ELDT-30'."""
        raise NotImplementedError


@dataclass
class MovementMessage:
    """The MVT message sent on actual take-off reporting the aircraft's movement.

    Package Messages, stereotype boundary, milestones [16].
    """
    pass


@dataclass
class NetworkOperations(AirportCdmPartner):
    """The network management party that issues CTOT, monitors flight progress via ETFMS/FUM, and receives DPI messages.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15].

    Relationship: association 'sends' -> FlightUpdateMessage [*]

    Relationship: dependency 'uses' -> EtfmsSystem
    """

    def issueCtot(self, flight: Flight) -> TakeOffTime:
        """The Network Operations issues the CTOT and sends it to relevant ATS units as well as the departure aerodrome. If the flight is regulated, a CTOT is issued at EOBT-2h."""
        raise NotImplementedError

    def monitorFlightProgress(self, flight: Flight) -> None:
        """If the flight is within 3hrs flying time of the destination airport the Network Operations monitors progress of the flight using the ETFMS and sends a Flight Update Message (FUM) that provides updates of the flight's progress."""
        raise NotImplementedError


@dataclass
class OffBlock:
    """Milestone 15: informs partners of Actual Off-Block Time, triggers an A-DPI message, and checks TTOT changes against tolerance before informing Network Operations.

    Package Milestones, stereotype control, milestones [15].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'uses' -> AirportCdmPlatform

    Relationship: association 'sends' -> DpiMessage [1..*]

    Relationship: association 'informs' -> NetworkOperations

    Relationship: dependency 'triggered by' -> SurveillanceSystem

    Relationship: dependency 'triggered by' -> AcarsSystem
    """
    ttotTolerance: timedelta | None = None

    def informAobt(self, flight: Flight, aobt: datetime) -> None:
        """Informs all relevant Airport CDM Partners of Actual Off-Block Time (AOBT) in the Airport CDM Platform and that the aircraft has commenced push-back/taxi from parking position when it occurs. AOBT always triggers an A-DPI message to Network Operations, or in the case of remote holding at a defined time prior to TTOT."""
        raise NotImplementedError

    def checkTtotChange(self, flight: Flight) -> bool:
        """Checks if TTOT changes by more than the agreed tolerance and informs Network Operations; after a first A-DPI is sent this check shall be performed to check TTOT updates against the TTOT tolerance before Network Operations is informed, with a new A-DPI, of the updated TTOT."""
        raise NotImplementedError

    def calculateTtot(self, aobt: datetime, exot: timedelta) -> datetime:
        """TTOT updated considering the EXOT."""
        raise NotImplementedError


@dataclass
class OffBlockTime(TimeQuantity):
    """The scheduled, estimated, target, or actual time an aircraft leaves its parking position (SOBT, EOBT, TOBT, AOBT).

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 6, 7, 8, 9, 10, 15].
    """
    pass


@dataclass
class ReadyStatusMessage:
    """The RDY message confirming that an aircraft is ready for start-up and push-back.

    Package Messages, stereotype boundary, milestones [12].
    """
    pass


@dataclass
class ReadyTime(TimeQuantity):
    """The actual time an aircraft is ready for start-up and push-back, with all doors closed and equipment removed (ARDT).

    Package Timings, stereotype entity, milestones [12].
    """
    pass


@dataclass
class StandGateManagement(AirportCdmPartner):
    """The party responsible for stand and gate allocation that shares EOBT information and is affected by stand/gate change decisions.

    Package Stakeholders, stereotype entity, milestones [4, 9].
    """
    pass


@dataclass
class StartUpApprovalTime(TimeQuantity):
    """The target or actual time an aircraft receives start-up approval (TSAT, ASAT).

    Package Timings, stereotype entity, milestones [10, 13, 14].
    """
    pass


@dataclass
class StartUpApproved:
    """Milestone 14: informs partners of Actual Start-up Approval Time and checks that it accords with TSAT, alerting partners and re-sequencing the flight if not granted in time.

    Package Milestones, stereotype control, milestones [14].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'uses' -> AirportCdmPlatform

    Relationship: dependency 'triggered by' -> DepartureClearanceMessage
    """
    tsatTolerance: timedelta | None = None

    def informAsat(self, flight: Flight, asat: datetime) -> None:
        """Informs all relevant Airport CDM Partners of Actual start up approval Time (ASAT) in the Airport CDM Platform and that the aircraft has received start up approval/push-back clearance when it occurs."""
        raise NotImplementedError

    def checkAsatAgainstTsat(self, flight: Flight) -> bool:
        """Checks if ASAT is in accordance with TSAT and alerts all relevant Airport CDM Partners when no start up has been granted; in case the start up approval is not granted at TSAT + tolerance, all relevant partners should be informed and the flight will be re-sequenced."""
        raise NotImplementedError


@dataclass
class StartUpRequestTime(TimeQuantity):
    """The actual time start-up is requested by the flight crew (ASRT).

    Package Timings, stereotype entity, milestones [13].
    """
    pass


@dataclass
class StartUpRequested:
    """Milestone 13: informs partners of Actual Start-up Request Time and alerts partners if no start-up request is made within the TSAT tolerance window.

    Package Milestones, stereotype control, milestones [13].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'uses' -> AirportCdmPlatform
    """
    tsatTolerance: timedelta | None = None

    def informAsrt(self, flight: Flight, asrt: datetime) -> None:
        """Informs all relevant Airport CDM Partners of Actual Start up Request Time (ASRT) in the Airport CDM Platform when it occurs."""
        raise NotImplementedError

    def checkStartUpRequested(self, flight: Flight) -> bool:
        """Alerts all relevant Airport CDM Partners when no start up has been requested inside the locally agreed TSAT tolerance window; if the start up request is not made by TSAT + tolerance, the AO/GH is informed that no start up has been requested, and should update TOBT."""
        raise NotImplementedError


@dataclass
class SurveillanceSystem:
    """A radar, A-SMGCS, or Tower FDPS detection system that identifies a flight's position by SSR code to trigger milestone events.

    Package Systems, stereotype boundary, milestones [4, 5, 6, 7, 15, 16].
    """

    def detectFlightAtFirBoundary(self, ssrCode: str) -> bool:
        """The radar system detects a flight based upon the assigned SSR code when the flight crosses a defined FIR/ATC boundary."""
        raise NotImplementedError

    def detectFinalApproach(self, ssrCode: str) -> bool:
        """The radar system detects a flight based upon the assigned SSR code and identifies when the flight crosses either a defined range/position or passes/leaves a predetermined level."""
        raise NotImplementedError


@dataclass
class TakeOff:
    """Milestone 16: informs partners of the actual take-off, sends FSA and MVT messages, and removes the flight from the departure sequence.

    Package Milestones, stereotype control, milestones [16].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'triggered by' -> SurveillanceSystem

    Relationship: dependency 'triggered by' -> AcarsSystem

    Relationship: association 'sends' -> FlightStatusMessage [1]

    Relationship: association 'sends' -> MovementMessage [1]

    Relationship: association 'generates' -> AirborneMessage [1]
    """

    def informTakeOff(self, flight: Flight, atot: datetime) -> None:
        """Informs all relevant Airport CDM Partners about the actual take off. An airborne message is generated and the flight is removed from the departure sequence."""
        raise NotImplementedError

    def sendFsaAndMvtMessages(self, flight: Flight) -> None:
        """FSA and MVT messages are sent."""
        raise NotImplementedError


@dataclass
class TakeOffFromOutstation:
    """Milestone 3: on take off from the outstation, checks AO/GH landing estimates against the outbound flight plan and informs Network Operations of updated take-off time estimates via a T-DPI-t message.

    Package Milestones, stereotype control, milestones [3].

    Relationship: association 'processes' -> Flight [1]

    Relationship: association 'sends' -> DpiMessage [1]

    Relationship: association 'informs' -> NetworkOperations
    """
    ttotTolerance: timedelta | None = None
    flyingTimeThreshold: timedelta | None = None

    def calculateEldt(self, atot: datetime, estimatedElapsedTime: timedelta) -> datetime:
        """Using the ATOT an ELDT can be calculated by using the Estimated Elapsed Time on the FPL."""
        raise NotImplementedError

    def checkLandingEstimateConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH estimated landing time after take off from outstation are consistent with the outbound ATC Flight Plan, and when needed informs the Network Operations about the updated take off time estimates using a T-DPI-t Message; this check shall be performed to verify feasibility of the ATC Flight Plan at take off from outstation. A TTOT tolerance of 5 minutes is respected before Network Operations is informed of the updated TTOT."""
        raise NotImplementedError

    def calculateTtot(self, eibt: datetime, mttt: timedelta, exot: timedelta, eobt: datetime, tobt: datetime) -> datetime:
        """Calculation basis for the TTOT shall take into account EIBT+MTTT+EXOT. In case EOBT is later than EIBT+MTTT, TTOT equals EOBT+EXOT. In the case where TOBT is available this prediction will overrule the EIBT+MTTT estimate, hence TTOT equals TOBT+EXOT."""
        raise NotImplementedError


@dataclass
class TakeOffTime(TimeQuantity):
    """The estimated, target, calculated, or actual time an aircraft takes off (ETOT, TTOT, CTOT, ATOT).

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 15, 16].
    """
    pass


@dataclass
class TaxiInTime(TimeQuantity):
    """The estimated taxi-in time between landing and in-block used to compute EIBT (EXIT).

    Package Timings, stereotype entity, milestones [4, 6].
    """
    duration: timedelta | None = None


@dataclass
class TaxiOutTime(TimeQuantity):
    """The estimated taxi-out time between off-block and take-off, calculated by ATC based on traffic load, stand location, and runway in use (EXOT).

    Package Timings, stereotype entity, milestones [2, 3, 4, 9, 15].
    """
    duration: timedelta | None = None


@dataclass
class TsatIssued:
    """Milestone 10: informs partners of the allocated TSAT via T-DPI-s and checks whether the number of TOBT updates after TSAT exceeds a locally defined tolerance.

    Package Milestones, stereotype control, milestones [10].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'uses' -> AirportCdmPlatform

    Relationship: association 'sends' -> DpiMessage [1]

    Relationship: association 'informs' -> NetworkOperations
    """
    issuanceOffset: timedelta | None = None
    tobtUpdateThreshold: int | None = None

    def informTsat(self, flight: Flight, tsat: datetime) -> None:
        """ATC informs all relevant partners of the TSAT that has been allocated to the flight. The Network Operations is informed by a T-DPI-s for non regulated flights."""
        raise NotImplementedError

    def checkTobtUpdateCount(self, flight: Flight) -> bool:
        """Checks whether the number of TOBT updates exceeds a tolerance defined locally, after TSAT has been issued. In case the number of TOBT updates exceeds a threshold, then the TOBT input should be processed according to local procedure."""
        raise NotImplementedError


@dataclass
class TurnRound:
    """The aircraft turn-round linking an arriving flight and its related departing flight so that ground handling and estimates can be analysed together.

    Package Flights, stereotype entity, milestones [1, 4, 6, 7, 8, 9].

    Relationship: aggregation 'includes' -> Flight [2]
    """
    pass


@dataclass
class TurnRoundTime(TimeQuantity):
    """The minimum or estimated turn-round period used to calculate the departing flight's TOBT (MTTT, ETTT).

    Package Timings, stereotype entity, milestones [2, 3, 6, 7, 8].
    """
    duration: timedelta | None = None
