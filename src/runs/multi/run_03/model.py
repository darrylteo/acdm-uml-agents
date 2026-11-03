"""Class stubs rendered from runs/multi/run_03/model.json by src/generate/render_code.py; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from enum import Enum


class AirportCoordinationStatus(Enum):
    COORDINATED = "Coordinated"
    NON_COORDINATED = "NonCoordinated"


class DpiMessageType(Enum):
    E_DPI = "E-DPI"
    T_DPI = "T-DPI"
    T_DPI_T = "T-DPI-t"
    T_DPI_S = "T-DPI-s"
    A_DPI = "A-DPI"


class DurationKind(Enum):
    EXOT = "EXOT"
    EXIT = "EXIT"
    MTTT = "MTTT"
    ETTT = "ETTT"
    ESTIMATED_ELAPSED_TIME = "EstimatedElapsedTime"


class FlightOperationalStatus(Enum):
    INITIATED = "INITIATED"
    AIRBORNE = "AIRBORNE"
    FIR = "FIR"
    FINAL = "FINAL"
    LANDED = "LANDED"
    IN_BLOCK = "IN-BLOCK"
    SEQUENCED = "SEQUENCED"
    BOARDING = "BOARDING"
    READY = "READY"
    OFF_BLOCK = "OFF-BLOCK"
    DEPARTED_TAKE_OFF = "DEPARTED/TAKE OFF"


class MovementMessageType(Enum):
    FSA = "FSA"
    MVT = "MVT"
    AIRBORNE = "Airborne"


class StartUpRequestMethod(Enum):
    VOICE = "Voice"
    DCL = "DCL"


class TimePrefix(Enum):
    SCHEDULED = "Scheduled"
    ESTIMATED = "Estimated"
    TARGET = "Target"
    ACTUAL = "Actual"
    CALCULATED = "Calculated"


@dataclass
class Acars:
    """The aircraft communications addressing and reporting system that provides landing, in-block, off-block and take-off times for equipped aircraft.

    Package Systems, stereotype boundary, milestones [6, 7, 15, 16].
    """
    pass


@dataclass
class AirportCdmPartner:
    """A generalization of any party participating in the Airport CDM process that originates or receives flight information and is informed by milestone procedures.

    Package Stakeholders, stereotype entity, milestones [9, 10, 11, 12, 13, 14, 15, 16].
    """
    pass


@dataclass
class AirTrafficControl(AirportCdmPartner):
    """The air traffic control units (Area Control Centre, Approach Control, Tower) that manage flight plans, sequencing and start-up approvals.

    Package Stakeholders, stereotype entity, milestones [1, 4, 5, 9, 10, 12, 13, 14, 15, 16].

    Relationship: association 'issues TSAT' -> StartUpApprovalTime [*]
    """

    def issueTsat(self, flight: Flight) -> StartUpApprovalTime:
        """ATC issues the Target Start Up Approval Time t-minutes before EOBT, where t is a parameter agreed locally."""
        raise NotImplementedError


@dataclass
class Aircraft:
    """The physical aircraft performing a flight, identified by type and registration, which may be updated from the ATC Flight Plan.

    Package Flights, stereotype entity, milestones [1].
    """
    aircraftType: str | None = None
    registration: str | None = None


@dataclass
class AircraftOperator(AirportCdmPartner):
    """The airline or operator that submits the ATC Flight Plan, provides TOBT and turn-round estimates, and manages the aircraft's turn-round.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12].

    Relationship: association 'submits' -> AtcFlightPlan [*]

    Relationship: association 'sends' -> ReadyStatusMessage [*]
    """

    def provideFinalTobt(self, flight: Flight) -> OffBlockTime:
        """The Aircraft Operator or Ground Handler provide their most accurate TOBT taking into account the operational situation."""
        raise NotImplementedError


@dataclass
class Milestone:
    """An abstract representation of one of the sixteen defined events in the CDM process, each with its own trigger, timing rule, effect and procedure.

    Package Milestones, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'concerns' -> Flight [1]
    """
    milestoneNumber: int | None = None
    resultingStatus: FlightOperationalStatus | None = None


@dataclass
class AircraftReady(Milestone):
    """The milestone at which the aircraft is ready for start-up and push-back, informing partners and checking against TOBT.

    Package Milestones, stereotype control, milestones [12].
    """

    def notifyActualReadyTime(self, ardt: ReadyTime) -> None:
        """To inform all relevant Airport CDM Partners of Actual Ready Time (ARDT) in the Airport CDM Platform and that the aircraft is ready for start up / push-back."""
        raise NotImplementedError

    def checkReadyStatusReceived(self, tobt: OffBlockTime, tolerance: timedelta) -> bool:
        """At TOBT + tolerance the AO/GH are informed that TOBT has passed and the Airport CDM Platform has not yet received ARDT or Ready Status (RDY)."""
        raise NotImplementedError


@dataclass
class AirportCdmPlatform:
    """The central CDM system that is initiated for each flight, processes available information, and performs the Action on CDM Operation updates and partner notifications described at each milestone.

    Package Systems, stereotype boundary, milestones [1, 2, 4, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'sends/receives' -> DpiMessage [*]

    Relationship: association 'initiated for / holds' -> Flight [*]
    """

    def commenceDpiProcess(self, flight: Flight) -> None:
        """The DPI process commences the correct messaging with Network Operations (if implemented)."""
        raise NotImplementedError


@dataclass
class AirportFlightData:
    """The locally held airport data describing a flight that must be consistent with the ATC Flight Plan and Airport Slot before the first E-DPI is sent.

    Package Flights, stereotype entity, milestones [1].

    Relationship: association 'describes' -> Flight [1]
    """
    pass


@dataclass
class AirportSlot:
    """The airport slot allocated under the airport slot programme against which the ATC Flight Plan and flight data are checked for consistency.

    Package Flights, stereotype entity, milestones [1].
    """
    allocatedTime: datetime | None = None
    coordinationStatus: AirportCoordinationStatus | None = None


@dataclass
class AtcFlightPlan:
    """The ICAO flight plan, including repetitive flight plans, submitted by the Aircraft Operator and distributed by the IFPS to ATC units.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 6, 9].

    Relationship: association 'checked for consistency with' -> AirportSlot [1]

    Relationship: association 'checked for consistency with' -> AirportFlightData [1]
    """
    isRepetitive: bool | None = None
    firstDestination: str | None = None


@dataclass
class AtcFlightPlanActivation(Milestone):
    """The milestone at which the ATC Flight Plan is submitted and the Airport CDM Platform is initiated for the flight.

    Package Milestones, stereotype control, milestones [1].

    Relationship: dependency 'initiates' -> AirportCdmPlatform
    """

    def checkConsistency(self, atcFlightPlan: AtcFlightPlan, airportSlot: AirportSlot, airportFlightData: AirportFlightData) -> bool:
        """This check shall be performed to verify the consistency between the ATC Flight Plan, Airport Slot and Airport flight data before the first E-DPI is sent."""
        raise NotImplementedError

    def validateDataBeforeFirstEdpi(self, sobt: OffBlockTime, aircraftRegistration: str, firstDestination: str) -> bool:
        """The AO must provide correct information before this first E-DPI message, in order to feed Network Operations with consistent SOBT, aircraft registration, and first destination data, as early in time as possible. The E-DPI message should not be sent if no or inconsistent information is provided."""
        raise NotImplementedError

    def initiateOutboundFlight(self, flightPlan: AtcFlightPlan) -> Flight:
        """For non coordinated airports, the flight plan is used to initiate the outbound flight."""
        raise NotImplementedError

    def checkFlightReadiness(self, actualReadyTime: datetime, eobt: OffBlockTime) -> bool:
        """The flight is ready not later than 15 minutes after the planned EOBT."""
        raise NotImplementedError


@dataclass
class AtcSystem:
    """The ATC system, including Tower FDPS, that provides landing, in-block and off-block times and calculates EXOT.

    Package Systems, stereotype boundary, milestones [1, 4, 6, 7, 9, 15, 16].

    Relationship: association 'calculates EXOT' -> DurationEstimate [*]
    """

    def calculateExot(self, trafficLoad: str, gateStandLocation: str, runwayInUse: str, holdingPositionWaitPeriod: timedelta) -> DurationEstimate:
        """Following the receipt of the TOBT, the ATC system will calculate and provide the Estimated Taxi-Out Time (EXOT) based on the predicted traffic load, gate/stand location, runway in use, and waiting period at the Holding Position, etc."""
        raise NotImplementedError


@dataclass
class AutomatedDockingSystem:
    """An automated system that detects an aircraft's arrival in-block or departure off-block.

    Package Systems, stereotype boundary, milestones [7, 15].
    """
    pass


@dataclass
class BoardingStarts(Milestone):
    """The milestone at which boarding of passengers physically starts, used to check whether TOBT will be respected.

    Package Milestones, stereotype control, milestones [11].
    """

    def notifyActualStartBoardingTime(self, asbt: StartBoardingTime) -> None:
        """To inform all relevant Airport CDM Partners of Actual Start Boarding Time (ASBT) when it occurs."""
        raise NotImplementedError

    def checkBoardingStatus(self, asbt: StartBoardingTime, tobt: OffBlockTime) -> bool:
        """At a certain time before TOBT (local variable e.g. corresponding to aircraft type) a check shall be performed to check the boarding status, whether boarding starts in time to respect TOBT, and inform the AO/GH in case TOBT needs to be updated."""
        raise NotImplementedError


@dataclass
class DpiMessage:
    """A Departure Planning Information message exchanged with Network Operations at defined milestones, distinguished by its type (E-DPI, T-DPI, T-DPI-t, T-DPI-s, A-DPI).

    Package Messages, stereotype boundary, milestones [1, 2, 3, 10, 15].
    """
    messageType: DpiMessageType | None = None
    sobt: OffBlockTime | None = None
    aircraftRegistration: str | None = None
    firstDestination: str | None = None


@dataclass
class DurationEstimate:
    """A duration used to calculate other time quantities, such as estimated taxi-out time (EXOT), estimated taxi-in time (EXIT), minimum turn-round time (MTTT), estimated turn-round time (ETTT), or the flight plan's estimated elapsed time.

    Package Timings, stereotype entity, milestones [2, 3, 4, 6, 8, 9].
    """
    value: timedelta | None = None
    kind: DurationKind | None = None


@dataclass
class EobtMinusTwoHourCheck(Milestone):
    """The milestone at EOBT-2 hours at which regulated flights receive a CTOT and Network Operations is informed by the first T-DPI message.

    Package Milestones, stereotype control, milestones [2].
    """

    def checkFeasibility(self, flightEstimates: TakeOffTime, atcFlightPlan: AtcFlightPlan) -> bool:
        """This check shall be performed to verify feasibility of the ATC Flight Plan estimated off block time at EOBT-2 hrs, by checking whether AO/GH flight estimates are consistent with the ATC Flight Plan."""
        raise NotImplementedError

    def informNetworkOperationsViaFirstTdpi(self, flight: Flight) -> None:
        """At EOBT-2 hrs Network Operations is informed through the first T-DPI message about the updated take off time estimate."""
        raise NotImplementedError

    def calculateTtot(self, eibt: InBlockTime, mttt: DurationEstimate, exot: DurationEstimate, eobt: OffBlockTime, tobt: OffBlockTime) -> datetime:
        """Calculation basis for the TTOT shall take into account EIBT+MTTT+EXOT, if later than EOBT+EXOT. In the case of manual input of TOBT, this estimate will override the EIBT+MTTT estimate, hence TTOT equals TOBT+EXOT."""
        raise NotImplementedError

    def updateEldtFromFum(self, fumMessage: FlightUpdateMessage) -> datetime:
        """For inbound flights, ELDT is updated based on information provided by the FUM messages, taking into account the actual progress of the flight."""
        raise NotImplementedError

    def markFieldsAsRegulated(self, flight: Flight) -> None:
        """Mark appropriate fields as REGULATED."""
        raise NotImplementedError


@dataclass
class Etfms:
    """The Network Operations system that monitors a flight's progress and generates Flight Update Messages when the flight is within three hours of the destination.

    Package Systems, stereotype boundary, milestones [3].

    Relationship: dependency 'generates' -> FlightUpdateMessage
    """

    def monitorFlightProgress(self, flight: Flight) -> None:
        """If the flight is within 3hrs flying time of the destination airport the Network Operations monitors progress of the flight using the ETFMS."""
        raise NotImplementedError

    def sendFum(self, flight: Flight) -> FlightUpdateMessage:
        """Network Operations sends a Flight Update Message (FUM) that provides updates of the flight's progress."""
        raise NotImplementedError


@dataclass
class FinalApproach(Milestone):
    """The milestone at which the flight enters final approach at the destination, triggering a new TOBT determination.

    Package Milestones, stereotype control, milestones [5].
    """

    def triggerTobtUpdate(self, eldt: LandingTime) -> None:
        """Update of the ELDT to determine a new TOBT."""
        raise NotImplementedError

    def checkFeasibility(self, tobt: OffBlockTime, atcFlightPlan: AtcFlightPlan) -> bool:
        """This process commences the TOBT process and checks whether the AO/GH TOBT is consistent with the ATC Flight Plan; this check shall be performed to verify feasibility of the ATC Flight Plan given the up-dated TOBT."""
        raise NotImplementedError

    def notifyNetworkOperationsIfToleranceExceeded(self, newTtot: TakeOffTime, oldTtot: TakeOffTime) -> None:
        """Network Operations is informed when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class FinalConfirmationOfTobt(Milestone):
    """The milestone at which the Aircraft Operator or Ground Handler provides their most accurate TOBT ahead of TSAT issue.

    Package Milestones, stereotype control, milestones [9].
    """

    def checkFeasibility(self, tobt: OffBlockTime, atcFlightPlan: AtcFlightPlan) -> bool:
        """This check should be performed at a predefined time (local parameter) to confirm TOBT prior to TSAT issue and verify feasibility of the ATC Flight Plan estimates given the updated TOBT, by checking whether the AO/GH TOBT is consistent with the ATC Flight Plan."""
        raise NotImplementedError

    def notifyNetworkOperationsIfToleranceExceeded(self, newTtot: TakeOffTime, oldTtot: TakeOffTime) -> None:
        """Network Operations is informed when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError

    def introduceIntoPredepartureSequence(self, flight: Flight) -> None:
        """The flight is introduced into the pre-departure sequence."""
        raise NotImplementedError

    def requiresConfirmation(self, tobt: OffBlockTime, manuallyModified: bool) -> bool:
        """No need to confirm an existing TOBT if it has been manually modified before."""
        raise NotImplementedError


@dataclass
class Flight:
    """A single scheduled arriving or departing movement of an aircraft, carrying its operational status and the time quantities that describe its progress.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'performed by' -> Aircraft [1]

    Relationship: association 'described by' -> AtcFlightPlan [1]

    Relationship: composition 'off-block time history' -> OffBlockTime [0..*]

    Relationship: composition 'in-block time history' -> InBlockTime [0..*]

    Relationship: composition 'landing time history' -> LandingTime [0..*]

    Relationship: composition 'take-off time history' -> TakeOffTime [0..*]

    Relationship: composition 'start-up approval time history' -> StartUpApprovalTime [0..*]

    Relationship: composition 'actual start boarding time' -> StartBoardingTime [0..1]

    Relationship: composition 'actual ready time' -> ReadyTime [0..1]

    Relationship: composition 'actual start-up request time' -> StartUpRequestTime [0..1]
    """
    operationalStatus: FlightOperationalStatus | None = None
    isRegulated: bool | None = None

    def updateOperationalStatus(self, newStatus: FlightOperationalStatus) -> None:
        """The flight's operational status changes to the status recorded at each milestone (e.g. INITIATED, AIRBORNE, FIR, FINAL, LANDED, IN-BLOCK, SEQUENCED, BOARDING, READY, OFF-BLOCK, DEPARTED/TAKE OFF)."""
        raise NotImplementedError


@dataclass
class FlightCrew(AirportCdmPartner):
    """The pilot and aircrew who request and receive start-up approval and coordinate readiness with the Ground Handler.

    Package Stakeholders, stereotype entity, milestones [12, 13, 14].

    Relationship: association 'sends' -> StartUpRequestMessage [*]
    """
    pass


@dataclass
class FlightInformationDisplaySystem:
    """The airport system, including flight information display and public address systems, used to inform partners and pre-call passengers.

    Package Systems, stereotype boundary, milestones [11].
    """
    pass


@dataclass
class FlightUpdateMessage:
    """The FUM message sent by Network Operations that provides updates of an inbound flight's progress.

    Package Messages, stereotype boundary, milestones [2, 3].
    """
    pass


@dataclass
class GroundHandler(AirportCdmPartner):
    """The party that performs ground handling operations and, with the Aircraft Operator, provides turn-round times such as TOBT, ACGT and ARDT.

    Package Stakeholders, stereotype entity, milestones [4, 6, 7, 8, 9, 10, 11, 12].
    """

    def provideFinalTobt(self, flight: Flight) -> OffBlockTime:
        """The Aircraft Operator or Ground Handler provide their most accurate TOBT taking into account the operational situation."""
        raise NotImplementedError


@dataclass
class GroundHandlingStarted(Milestone):
    """The milestone at which ground handling commences (ACGT) for first-of-day or long-parked flights, triggering a TOBT update.

    Package Milestones, stereotype control, milestones [8].
    """

    def updateTobt(self, acgt: datetime, turnRoundPeriod: DurationEstimate) -> None:
        """The occurrence of ACGT triggers an update of downstream estimates: TOBT is updated automatically or inserted manually by the Aircraft Operator/Ground Handler, calculated on the basis of the estimated turn-round period for the departing flight."""
        raise NotImplementedError

    def checkFeasibility(self, tobt: OffBlockTime, atcFlightPlan: AtcFlightPlan) -> bool:
        """This check shall be performed to verify feasibility of the ATC Flight Plan given the updated TOBT or ATC Flight Plan, by checking whether the AO/GH TOBT is consistent with the ATC Flight Plan."""
        raise NotImplementedError

    def notifyNetworkOperationsIfToleranceExceeded(self, newTtot: TakeOffTime, oldTtot: TakeOffTime) -> None:
        """Network Operations is informed when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class Ifps:
    """The system that distributes the submitted ATC Flight Plan to all involved ATC units.

    Package Systems, stereotype boundary, milestones [1].

    Relationship: dependency 'distributes' -> AtcFlightPlan
    """
    pass


@dataclass
class InBlock(Milestone):
    """The milestone at which AIBT is recorded, triggering updates to TOBT and TTOT based on the estimated turn-round period.

    Package Milestones, stereotype control, milestones [7].
    """

    def updateTobtAndTtot(self, aibt: InBlockTime, turnRoundPeriod: DurationEstimate) -> None:
        """The occurrence of AIBT should trigger an update of downstream estimates: TOBT and TTOT are updated automatically or inserted manually by the Aircraft Operator/Ground Handler, calculated on the basis of the estimated turn-round period for the departing flight."""
        raise NotImplementedError

    def checkFeasibility(self, tobt: OffBlockTime, atcFlightPlan: AtcFlightPlan) -> bool:
        """This check shall be performed to verify feasibility of the ATC Flight Plan given the updated TOBT or ATC Flight Plan, by checking whether the AO/GH TOBT is consistent with the ATC Flight Plan."""
        raise NotImplementedError

    def notifyNetworkOperationsIfToleranceExceeded(self, newTtot: TakeOffTime, oldTtot: TakeOffTime) -> None:
        """Network Operations is informed when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class TimeQuantity:
    """An abstract time value describing a flight's progress, recorded with its prefix, originator and time of update, with every successive value kept rather than overwritten.

    Package Timings, stereotype entity, milestones [1, 2, 3].
    """
    value: datetime | None = None
    prefix: TimePrefix | None = None
    originator: str | None = None
    recordedAt: datetime | None = None

    def recordUpdate(self, newValue: datetime, originator: str, recordedAt: datetime) -> None:
        """Every successive value is kept, with its originator and time of update, so a turn-round can be analysed afterwards; an update appends rather than overwriting."""
        raise NotImplementedError


@dataclass
class InBlockTime(TimeQuantity):
    """The estimated or actual value of the in-block event (EIBT, AIBT) for an arriving flight.

    Package Timings, stereotype entity, milestones [1, 3, 4, 6, 7].
    """
    accuracy: timedelta | None = None


@dataclass
class Landed(Milestone):
    """The milestone at which ALDT is recorded, triggering updates to TOBT, TTOT and EIBT.

    Package Milestones, stereotype control, milestones [6].
    """

    def updateTobtAndTtot(self, aldt: LandingTime, turnRoundPeriod: DurationEstimate) -> None:
        """The occurrence of ALDT triggers an update of downstream estimates: TOBT and TTOT are updated automatically or inserted manually by the Aircraft Operator/Ground Handler, calculated on the basis of the defined turn-round period for the departing flight."""
        raise NotImplementedError

    def calculateEibt(self, aldt: LandingTime, exit: DurationEstimate) -> datetime:
        """The EIBT can be updated according to the ALDT+EXIT."""
        raise NotImplementedError

    def checkFeasibility(self, tobt: OffBlockTime, atcFlightPlan: AtcFlightPlan) -> bool:
        """This check shall be performed to verify feasibility of the ATC Flight Plan given the updated TOBT or ATC Flight Plan, by checking whether the AO/GH TOBT is consistent with the ATC Flight Plan."""
        raise NotImplementedError

    def notifyNetworkOperationsIfToleranceExceeded(self, newTtot: TakeOffTime, oldTtot: TakeOffTime) -> None:
        """Network Operations is informed when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class LandingTime(TimeQuantity):
    """The estimated or actual value of the landing event (ELDT, ALDT) for an arriving flight.

    Package Timings, stereotype entity, milestones [1, 3, 4, 5, 6].
    """
    accuracy: timedelta | None = None


@dataclass
class LocalRadarUpdate(Milestone):
    """The milestone at which the flight is detected entering the FIR or local airspace, triggering a TOBT process and ELDT/EIBT update.

    Package Milestones, stereotype control, milestones [4].
    """

    def triggerTobtUpdate(self, eldt: LandingTime) -> None:
        """Update of the ELDT can trigger a new TOBT to be entered by the AO/GH, or calculated automatically by the Airport CDM Platform."""
        raise NotImplementedError

    def checkStandGateChangePreference(self, eldt: LandingTime, exit: DurationEstimate) -> bool:
        """Taking into account the taxi-in time (EXIT), any change to a stand or gate is not preferred after ELDT-30'."""
        raise NotImplementedError

    def calculateEibt(self, eldt: LandingTime, exit: DurationEstimate) -> datetime:
        """An estimated in-block time (EIBT) is computed using the ELDT and the estimated taxi-in time."""
        raise NotImplementedError

    def checkFeasibility(self, tobt: OffBlockTime, atcFlightPlan: AtcFlightPlan) -> bool:
        """This process commences the TOBT process and checks whether the AO/GH TOBT is consistent with the ATC Flight Plan; this check shall be performed to verify feasibility of the ATC Flight Plan given the up-dated TOBT."""
        raise NotImplementedError

    def notifyNetworkOperationsIfToleranceExceeded(self, newTtot: TakeOffTime, oldTtot: TakeOffTime) -> None:
        """Network Operations is informed when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class MovementMessage:
    """A message sent on actual take-off informing partners of the flight's movement, including FSA, MVT and the airborne message.

    Package Messages, stereotype boundary, milestones [16].
    """
    messageType: MovementMessageType | None = None


@dataclass
class NetworkOperations(AirportCdmPartner):
    """The network management function that issues CTOT, monitors flight progress via ETFMS, and is informed of updated estimates through DPI messages.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15].

    Relationship: association 'informed by' -> DpiMessage [*]

    Relationship: association 'sends' -> FlightUpdateMessage [*]

    Relationship: association 'issues CTOT' -> TakeOffTime [*]
    """

    def issueCtot(self, flight: Flight) -> TakeOffTime:
        """If the flight is regulated, a CTOT is issued by Network Operations at EOBT-2h."""
        raise NotImplementedError


@dataclass
class OffBlock(Milestone):
    """The milestone at which the aircraft pushes back, recorded as AOBT and always triggering an A-DPI message to Network Operations.

    Package Milestones, stereotype control, milestones [15].
    """

    def notifyActualOffBlockTime(self, aobt: OffBlockTime) -> None:
        """To inform all relevant Airport CDM Partners of Actual Off-Block Time (AOBT) in the Airport CDM Platform and that the aircraft has commenced push-back / taxi from parking position."""
        raise NotImplementedError

    def updateTtot(self, aobt: OffBlockTime, exot: DurationEstimate) -> datetime:
        """TTOT updated considering the EXOT."""
        raise NotImplementedError

    def checkTtotToleranceExceeded(self, newTtot: TakeOffTime, oldTtot: TakeOffTime) -> bool:
        """To check if TTOT changes by more than the agreed tolerance and inform Network Operations."""
        raise NotImplementedError

    def sendADpi(self, flight: Flight) -> None:
        """AOBT always triggers an A-DPI message to Network Operations or in the case of remote holding at a defined time prior to TTOT. After a first A-DPI is sent this check shall be performed to check TTOT updates against the TTOT tolerance before Network Operations is informed, with a new A-DPI, of the updated TTOT."""
        raise NotImplementedError


@dataclass
class OffBlockTime(TimeQuantity):
    """The scheduled, target or actual value of the off-block event (EOBT, TOBT, AOBT) for a flight.

    Package Timings, stereotype entity, milestones [1, 2, 4, 6, 7, 8, 9, 10, 12, 15].
    """
    accuracy: timedelta | None = None


@dataclass
class Outstation(AirportCdmPartner):
    """The departure aerodrome of the outbound flight when different from the airport of interest, which provides ATOT to Network Operations and the Aircraft Operator.

    Package Stakeholders, stereotype entity, milestones [3].

    Relationship: association 'provides ATOT for' -> Flight [*]

    Relationship: dependency 'provides ATOT to' -> NetworkOperations
    """

    def provideAtot(self, flight: Flight) -> TakeOffTime:
        """The outstation provides ATOT to the Network Operations and Aircraft Operator."""
        raise NotImplementedError


@dataclass
class ReadyStatusMessage:
    """The Ready Status (RDY) message confirming that a flight follows the indicated TOBT and is ready for start-up.

    Package Messages, stereotype boundary, milestones [12].
    """
    pass


@dataclass
class ReadyTime(TimeQuantity):
    """The actual time at which an aircraft is ready for start-up and push-back (ARDT).

    Package Timings, stereotype entity, milestones [12].
    """
    accuracy: timedelta | None = None
    tolerance: timedelta | None = None


@dataclass
class StandGateManagement(AirportCdmPartner):
    """The stakeholder responsible for stand and gate allocation decisions that depend on accurate ELDT and EOBT sharing.

    Package Stakeholders, stereotype entity, milestones [4, 9].

    Relationship: dependency 'decides stand/gate allocation based on' -> Flight
    """
    pass


@dataclass
class StartBoardingTime(TimeQuantity):
    """The actual time at which boarding of a flight starts (ASBT).

    Package Timings, stereotype entity, milestones [11].
    """
    accuracy: timedelta | None = None


@dataclass
class StartUpApprovalTime(TimeQuantity):
    """The target or actual value of the start-up approval event (TSAT, ASAT) for a departing flight.

    Package Timings, stereotype entity, milestones [9, 10, 14].
    """
    toleranceWindow: timedelta | None = None


@dataclass
class StartUpApproved(Milestone):
    """The milestone at which ATC grants start-up approval, checked against TSAT with resequencing if not granted in time.

    Package Milestones, stereotype control, milestones [14].
    """

    def notifyActualStartUpApprovalTime(self, asat: datetime) -> None:
        """To inform all relevant Airport CDM Partners of Actual start up approval Time (ASAT) in the Airport CDM Platform and that the aircraft has received start up approval / push-back clearance."""
        raise NotImplementedError

    def checkAsatAgainstTsat(self, asat: datetime, tsat: StartUpApprovalTime, tolerance: timedelta) -> bool:
        """A check shall be performed to check if ASAT is in accordance to TSAT and to alert all relevant Airport CDM Partners when no start up has been granted. In case the start up approval is not granted at TSAT + tolerance, all relevant partners should be informed."""
        raise NotImplementedError

    def resequenceFlight(self, flight: Flight) -> None:
        """The flight will be re-sequenced."""
        raise NotImplementedError


@dataclass
class StartUpRequestMessage:
    """The message by which the flight crew requests start-up, made by voice or DCL.

    Package Messages, stereotype boundary, milestones [14].
    """
    method: StartUpRequestMethod | None = None


@dataclass
class StartUpRequestTime(TimeQuantity):
    """The actual time at which start-up is requested by the flight crew (ASRT).

    Package Timings, stereotype entity, milestones [13].
    """
    accuracy: timedelta | None = None


@dataclass
class StartUpRequested(Milestone):
    """The milestone at which start-up is requested by the pilot, with an alert if no request is made within the TSAT tolerance window.

    Package Milestones, stereotype control, milestones [13].
    """

    def notifyActualStartUpRequestTime(self, asrt: StartUpRequestTime) -> None:
        """To inform all relevant Airport CDM Partners of Actual Start up Request Time (ASRT) in the Airport CDM Platform."""
        raise NotImplementedError

    def checkStartUpRequestedWithinTolerance(self, tsat: StartUpApprovalTime, tolerance: timedelta) -> bool:
        """To alert all relevant Airport CDM Partners when no start up has been requested inside the locally agreed TSAT tolerance window. If the start up request is not made by TSAT + tolerance, the AO/GH is informed that no start up has been requested, and should update TOBT."""
        raise NotImplementedError


@dataclass
class SurveillanceRadarSystem:
    """The radar system (including A-SMGCS) that detects a flight by its assigned SSR code when it crosses the FIR/ATC boundary or enters final approach.

    Package Systems, stereotype boundary, milestones [4, 5].
    """

    def detectFlightAtFirBoundary(self, ssrCode: str) -> None:
        """The radar system is able to detect a flight based upon the assigned SSR code when the flight crosses a defined FIR/ATC boundary."""
        raise NotImplementedError

    def detectFlightOnFinalApproach(self, ssrCode: str) -> None:
        """The radar system detects a flight based upon the assigned SSR code and identifies when the flight crosses either a defined range/position or passes/leaves a predetermined level."""
        raise NotImplementedError


@dataclass
class TakeOff(Milestone):
    """The milestone at which the aircraft takes off, recorded as ATOT, generating an airborne message and removing the flight from the departure sequence.

    Package Milestones, stereotype control, milestones [16].

    Relationship: association 'sends' -> MovementMessage [*]
    """

    def notifyActualTakeOff(self, atot: TakeOffTime) -> None:
        """To inform all relevant Airport CDM Partners about the actual take off."""
        raise NotImplementedError

    def generateAirborneMessage(self, flight: Flight) -> None:
        """An airborne message is generated and the flight is removed from the departure sequence."""
        raise NotImplementedError

    def sendFsaAndMvtMessages(self, flight: Flight) -> None:
        """FSA and MVT messages are sent."""
        raise NotImplementedError


@dataclass
class TakeOffFromOutstation(Milestone):
    """The milestone at which ATOT from the outstation is received and used to update ELDT and, when needed, inform Network Operations via a T-DPI-t message.

    Package Milestones, stereotype control, milestones [3].
    """

    def calculateEldtFromAtot(self, atot: TakeOffTime, estimatedElapsedTime: DurationEstimate) -> datetime:
        """If the departure airport is more than 3hrs flying time from the destination airport, using the ATOT an ELDT can be calculated by using the Estimated Elapsed Time on the FPL."""
        raise NotImplementedError

    def checkFeasibility(self, estimatedLandingTime: LandingTime, atcFlightPlan: AtcFlightPlan) -> bool:
        """This check shall be performed to verify feasibility of the ATC Flight Plan at take off from outstation, by checking whether the AO/GH estimated landing time is consistent with the outbound ATC Flight Plan."""
        raise NotImplementedError

    def calculateTtot(self, eibt: InBlockTime, mttt: DurationEstimate, exot: DurationEstimate, eobt: OffBlockTime, tobt: OffBlockTime) -> datetime:
        """Calculation basis for the TTOT shall take into account EIBT+MTTT+EXOT. In case EOBT is later than EIBT+MTTT, TTOT equals EOBT+EXOT. In the case where TOBT is available this prediction will overrule the EIBT+MTTT estimate, hence TTOT equals TOBT+EXOT."""
        raise NotImplementedError

    def notifyNetworkOperationsIfToleranceExceeded(self, newTtot: TakeOffTime, oldTtot: TakeOffTime) -> None:
        """A TTOT tolerance of 5 minutes is respected before Network Operations is informed of the updated TTOT using a T-DPI-t Message."""
        raise NotImplementedError


@dataclass
class TakeOffTime(TimeQuantity):
    """The estimated, target, calculated or actual value of the take-off event (ETOT, TTOT, CTOT, ATOT) for a departing flight.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 16].
    """
    accuracy: timedelta | None = None
    tolerance: timedelta | None = None


@dataclass
class TsatIssued(Milestone):
    """The milestone at which ATC issues the Target Start-Up Approval Time and checks the number of subsequent TOBT updates.

    Package Milestones, stereotype control, milestones [10].
    """

    def notifyPartnersOfTsat(self, tsat: StartUpApprovalTime) -> None:
        """To inform all relevant partners of the TSAT that has been allocated to the flight."""
        raise NotImplementedError

    def informNetworkOperationsViaTdpiS(self, flight: Flight) -> None:
        """The Network Operations is informed by a T-DPI-s for non regulated flights."""
        raise NotImplementedError

    def checkTobtUpdateCountExceedsTolerance(self, tobtUpdateCount: int, threshold: int) -> bool:
        """A check shall be performed to see the number of TOBT updates after TSAT has been issued. In case the number of TOBT updates exceeds a threshold, then the TOBT input should be processed according to local procedure."""
        raise NotImplementedError


@dataclass
class TurnRound:
    """The linked pair of an arriving and a departing flight of the same aircraft at an airport, over which the turn-round period is defined and analysed.

    Package Flights, stereotype entity, milestones [1, 4, 6, 7, 8].

    Relationship: aggregation 'comprises arriving and departing flight' -> Flight [2]

    Relationship: aggregation 'turn-round duration basis' -> DurationEstimate [0..*]
    """
    minimumTurnRoundTime: DurationEstimate | None = None
    estimatedTurnRoundTime: DurationEstimate | None = None
