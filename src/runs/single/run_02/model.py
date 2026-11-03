"""Class stubs rendered from runs/single/run_02/model.json by src/generate/render_code.py; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from enum import Enum


class DpiType(Enum):
    E_DPI = "E-DPI"
    T_DPI = "T-DPI"
    T_DPI_T = "T-DPI-t"
    T_DPI_S = "T-DPI-s"
    A_DPI = "A-DPI"


class EventType(Enum):
    OFF_BLOCK = "Off-Block"
    IN_BLOCK = "In-Block"
    LANDING = "Landing"
    TAKE_OFF = "Take-Off"
    START_UP_APPROVAL = "Start-Up Approval"
    TAKE_OFF_OUTSTATION = "Take-Off Outstation"
    GROUND_HANDLING_START = "Ground Handling Start"
    START_BOARDING = "Start Boarding"
    READY = "Ready"
    START_UP_REQUEST = "Start-Up Request"


class FlightDirection(Enum):
    ARRIVAL = "Arrival"
    DEPARTURE = "Departure"


class OperationalStatus(Enum):
    INITIATED = "INITIATED"
    REGULATED = "REGULATED"
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


class PrefixType(Enum):
    SCHEDULED = "Scheduled"
    ESTIMATED = "Estimated"
    TARGET = "Target"
    ACTUAL = "Actual"
    CALCULATED = "Calculated"


@dataclass
class Acars:
    """The ACARS system aboard equipped aircraft that provides actual time events (ON, IN, OUT, OFF) such as ALDT, AIBT, AOBT and ATOT.

    Package Systems, stereotype boundary, milestones [6, 7, 15, 16].

    Relationship: dependency 'provides actual times' -> TimeQuantity
    """
    pass


@dataclass
class AirportCdmPartner:
    """A generic party involved in the Airport CDM process that originates or receives flight information and is informed of milestone events.

    Package Stakeholders, stereotype entity, milestones [1, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    name: str | None = None
    role: str | None = None


@dataclass
class AirTrafficControl(AirportCdmPartner):
    """The air traffic control unit (including Area Control Centre/Approach Control Unit and Tower) that issues TSAT, TWR instructions, and start-up approvals, and detects flights via radar/A-SMGCS/FDPS.

    Package Stakeholders, stereotype entity, milestones [2, 4, 5, 9, 10, 12, 13, 14, 16].
    """
    unitType: str | None = None


@dataclass
class Aircraft:
    """The physical aircraft operating a flight, identified by registration and type.

    Package Flights, stereotype entity, milestones [1].
    """
    registration: str | None = None
    type: str | None = None


@dataclass
class AircraftOperator(AirportCdmPartner):
    """The airline or operator that submits the ATC flight plan, provides TOBT and turn-round information, and manages the aircraft's turn-round.

    Package Stakeholders, stereotype entity, milestones [1, 3, 4, 5, 6, 7, 8, 9, 11, 12].

    Relationship: dependency 'submits' -> AtcFlightPlan
    """

    def submitAtcFlightPlan(self, flightPlan: AtcFlightPlan) -> None:
        """The ATC Flight Plan is submitted by the Aircraft Operator and distributed by the IFPS (M1)."""
        raise NotImplementedError

    def provideTobt(self, flight: Flight, tobt: TimeQuantity) -> None:
        """The Aircraft Operator/Ground Handler provides the most accurate TOBT taking into account the operational situation, integrating their own strategy (M9)."""
        raise NotImplementedError


@dataclass
class Milestone:
    """A superclass for the sixteen CDM milestone events, each with a definition, timing rule, trigger, effect, and procedure that changes the flight's operational status.

    Package Milestones, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'tracks progress of' -> Flight [1]

    Relationship: dependency 'executed within' -> AirportCdmPlatform
    """
    milestoneNumber: int | None = None
    definition: str | None = None
    timingRule: str | None = None
    dataQuality: str | None = None
    trigger: str | None = None
    operationalStatusChange: OperationalStatus | None = None


@dataclass
class AircraftReady(Milestone):
    """Milestone 12: all doors closed, boarding bridge removed, push back vehicle connected; the aircraft is ready to taxi (ARDT).

    Package Milestones, stereotype control, milestones [12].
    """

    def recordArdt(self, flight: Flight) -> TimeQuantity:
        """Informs all relevant Airport CDM Partners of the Actual Ready Time (ARDT) in the Airport CDM Platform, confirming the aircraft is ready for start up/push-back."""
        raise NotImplementedError

    def checkReadyStatusReceived(self, flight: Flight, tolerance: timedelta) -> bool:
        """At TOBT+tolerance, informs the AO/GH that TOBT has passed and no ARDT or Ready Status (RDY) has been received."""
        raise NotImplementedError


@dataclass
class AirportCdmPlatform:
    """The Airport CDM Platform system that is initiated per flight, processes available information, computes and records time quantities, marks status fields, and informs Airport CDM Partners at each milestone.

    Package Systems, stereotype control, milestones [1, 2, 4, 10, 11, 12, 13, 14, 15].

    Relationship: dependency 'sends' -> DpiMessage

    Relationship: dependency 'triggers' -> FsaMessage

    Relationship: dependency 'triggers' -> MvtMessage

    Relationship: association 'processes' -> Flight [*]
    """

    def initiateForFlight(self, flight: Flight) -> None:
        """Initiated for the flight and processes all available information (M1)."""
        raise NotImplementedError

    def markAsRegulated(self, flight: Flight) -> None:
        """Marks appropriate fields as REGULATED for a flight that receives a CTOT (M2)."""
        raise NotImplementedError

    def calculateTobtAutomatically(self, flight: Flight) -> TimeQuantity:
        """A new TOBT can be calculated automatically by the Airport CDM Platform following an ELDT update (M4)."""
        raise NotImplementedError

    def informPartners(self, flight: Flight, eventType: EventType) -> None:
        """Informs all relevant Airport CDM Partners of an actual time event (ASBT, ARDT, ASRT, ASAT, AOBT, ATOT) as it occurs (M11-16)."""
        raise NotImplementedError


@dataclass
class AirportSlot:
    """The airport slot programme entry that the ATC Flight Plan must correspond to, used to initiate the outbound flight at coordinated airports.

    Package Flights, stereotype entity, milestones [1].
    """
    sobt: TimeQuantity | None = None
    slotProgramme: str | None = None


@dataclass
class AtcFlightPlan:
    """The ICAO flight plan submitted to ATC for a flight, distributed by the IFPS, and checked for consistency with the airport slot and flight data.

    Package Flights, stereotype entity, milestones [1, 2, 3].
    """
    eobt: TimeQuantity | None = None
    estimatedElapsedTime: timedelta | None = None
    departureAerodrome: str | None = None
    destinationAerodrome: str | None = None
    isRepetitive: bool | None = None


@dataclass
class AtcFlightPlanActivated(Milestone):
    """Milestone 1: the ICAO flight plan is submitted to ATC and the Airport CDM Platform is initiated for the flight.

    Package Milestones, stereotype control, milestones [1].
    """

    def checkConsistency(self, flightPlan: AtcFlightPlan, slot: AirportSlot, flight: Flight) -> bool:
        """Checks consistency between the ATC Flight Plan, Airport Slot and Airport flight data before the first E-DPI is sent."""
        raise NotImplementedError

    def sendFirstEdpi(self, flight: Flight) -> None:
        """Confirms the flight to Network Operations via the first E-DPI message with consistent SOBT, aircraft registration and first destination data; not sent if information is missing or inconsistent."""
        raise NotImplementedError

    def updateEldtEibtEtot(self, flight: Flight) -> None:
        """ELDT and EIBT updated for an arrival; EOBT and ETOT updated for a departure."""
        raise NotImplementedError


@dataclass
class AtcSystem:
    """The ATC technical system(s) (radar, A-SMGCS, Tower FDPS) that detect flight events and provide time quantities such as ATOT, ALDT and TSAT.

    Package Systems, stereotype boundary, milestones [3, 4, 5, 6, 9, 10, 16].

    Relationship: dependency 'provides actual/target times' -> TimeQuantity
    """
    pass


@dataclass
class BoardingStarts(Milestone):
    """Milestone 11: the gate is opened for passengers to physically start boarding.

    Package Milestones, stereotype control, milestones [11].
    """

    def recordAsbt(self, flight: Flight) -> TimeQuantity:
        """Informs all relevant Airport CDM Partners of the Actual Start Boarding Time (ASBT) when it occurs."""
        raise NotImplementedError

    def checkBoardingStatus(self, flight: Flight, minutesBeforeTobt: int) -> bool:
        """At a locally defined time before TOBT, checks the boarding status and informs the AO/GH if TOBT needs updating."""
        raise NotImplementedError


@dataclass
class DpiMessage:
    """A Departure Planning Information message sent by the Airport CDM Platform to Network Operations to communicate flight time estimates.

    Package Messages, stereotype boundary, milestones [1, 2, 3, 10, 15].
    """
    type: DpiType | None = None
    timestamp: datetime | None = None


@dataclass
class Eobt2hrCheck(Milestone):
    """Milestone 2: at EOBT-2 hr regulated flights receive a CTOT and estimates are checked against the ATC Flight Plan.

    Package Milestones, stereotype control, milestones [2].
    """

    def checkFlightEstimatesConsistency(self, flight: Flight) -> bool:
        """Checks whether AO/GH flight estimates are consistent with the ATC Flight Plan to verify feasibility of the estimated off-block time at EOBT-2 hr."""
        raise NotImplementedError

    def sendTDpi(self, flight: Flight) -> None:
        """Informs Network Operations about the updated take off time estimate using a T-DPI message at EOBT-2 hrs."""
        raise NotImplementedError

    def markAsRegulated(self, flight: Flight) -> None:
        """Marks appropriate fields as REGULATED when the flight receives a CTOT."""
        raise NotImplementedError


@dataclass
class EtfmsSystem:
    """The system used by Network Operations to monitor flight progress and issue Flight Update Messages.

    Package Systems, stereotype boundary, milestones [3].

    Relationship: dependency 'sends' -> FumMessage
    """
    pass


@dataclass
class FinalApproach(Milestone):
    """Milestone 5: the flight enters the Final Approach phase, prompting a further TOBT/ELDT update, typically 2 to 5 minutes from landing.

    Package Milestones, stereotype control, milestones [5].
    """

    def commenceTobtProcess(self, flight: Flight) -> None:
        """Commences the TOBT process and checks whether the AO/GH TOBT is consistent with the ATC Flight Plan."""
        raise NotImplementedError

    def informNetworkOperationsIfTtotExceedsTolerance(self, flight: Flight) -> None:
        """Network Operations is informed when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class FinalConfirmationOfTobt(Milestone):
    """Milestone 9: the time at which the Aircraft Operator/Ground Handler provides its most accurate TOBT, t minutes before EOBT.

    Package Milestones, stereotype control, milestones [9].
    """

    def confirmTobt(self, flight: Flight, tMinutesBeforeEobt: int) -> None:
        """Checks TOBT quality at a predefined local time before TSAT issue, triggered by a new TOBT or TTOT update; no need to reconfirm if manually modified before."""
        raise NotImplementedError

    def calculateExot(self, flight: Flight) -> timedelta:
        """Following receipt of TOBT, the ATC system calculates and provides the Estimated Taxi-Out Time (EXOT) based on predicted traffic load, gate/stand location, runway in use, and waiting period at the holding position."""
        raise NotImplementedError


@dataclass
class Flight:
    """A single flight (arrival or departure) that is tracked through the CDM milestones with its operational status and time quantities.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'operates with' -> Aircraft [1]

    Relationship: association 'described by' -> AtcFlightPlan [1]

    Relationship: association 'corresponds to' -> AirportSlot [0..1]

    Relationship: aggregation 'records' -> TimeQuantity [1..*]
    """
    flightId: str | None = None
    direction: FlightDirection | None = None
    operationalStatus: OperationalStatus | None = None
    isRegulated: bool | None = None
    timeQuantities: TimeQuantity | None = None


@dataclass
class FsaMessage:
    """An airborne/FSA message sent on take off.

    Package Messages, stereotype boundary, milestones [16].
    """
    timestamp: datetime | None = None


@dataclass
class FumMessage:
    """A Flight Update Message sent by Network Operations providing updates of a flight's progress used to update ELDT.

    Package Messages, stereotype boundary, milestones [2, 3].
    """
    timestamp: datetime | None = None


@dataclass
class GroundHandler(AirportCdmPartner):
    """The party that manages ground handling operations for the flight and coordinates with the Aircraft Operator on TOBT and turn-round.

    Package Stakeholders, stereotype entity, milestones [6, 7, 8, 9, 11, 12].
    """
    pass


@dataclass
class GroundHandlingStarted(Milestone):
    """Milestone 8: ACGT, the commencement of ground handling operations, triggers an update of TOBT for flights first of the day or long-parked.

    Package Milestones, stereotype control, milestones [8].
    """

    def checkTobtConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT."""
        raise NotImplementedError

    def updateTobtFromTurnround(self, flight: Flight, mttt: timedelta) -> None:
        """TOBT is updated automatically or manually, calculated on the basis of the estimated turn-round period for the departing flight."""
        raise NotImplementedError


@dataclass
class Ifps:
    """The system that distributes the submitted ATC Flight Plan to all involved ATC units.

    Package Systems, stereotype boundary, milestones [1].

    Relationship: dependency 'distributes' -> AtcFlightPlan
    """
    pass


@dataclass
class InBlockMilestone(Milestone):
    """Milestone 7: AIBT, the actual in-block time, triggers an update of downstream TOBT and TTOT estimates.

    Package Milestones, stereotype control, milestones [7].
    """

    def checkTobtConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT."""
        raise NotImplementedError

    def updateTobtTtotFromTurnround(self, flight: Flight, mttt: timedelta) -> None:
        """TOBT and TTOT are updated automatically or manually, calculated on the basis of the estimated turn-round period for the departing flight."""
        raise NotImplementedError


@dataclass
class Landed(Milestone):
    """Milestone 6: ALDT, the actual landing time, triggers an update of downstream TOBT, TTOT and EIBT estimates.

    Package Milestones, stereotype control, milestones [6].
    """

    def checkTobtConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT/ATC Flight Plan."""
        raise NotImplementedError

    def updateEibtFromAldt(self, flight: Flight, exit: timedelta) -> datetime:
        """EIBT can be updated according to ALDT+EXIT."""
        raise NotImplementedError

    def informNetworkOperationsIfTtotExceedsTolerance(self, flight: Flight) -> None:
        """A TTOT tolerance is respected before Network Operations is informed of the updated TTOT."""
        raise NotImplementedError


@dataclass
class LocalRadarUpdate(Milestone):
    """Milestone 4: the flight enters the FIR or local airspace of the destination airport, triggering a TOBT/ELDT update.

    Package Milestones, stereotype control, milestones [4].
    """

    def commenceTobtProcess(self, flight: Flight) -> None:
        """Commences the TOBT process and checks whether the AO/GH TOBT is consistent with the ATC Flight Plan."""
        raise NotImplementedError

    def informNetworkOperationsIfTtotExceedsTolerance(self, flight: Flight) -> None:
        """Network Operations is informed when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class MvtMessage:
    """A movement (MVT) message sent on take off.

    Package Messages, stereotype boundary, milestones [16].
    """
    timestamp: datetime | None = None


@dataclass
class NetworkOperations(AirportCdmPartner):
    """The network management function that issues CTOT, distributes flight plans, monitors flight progress via ETFMS, and receives DPI/FUM messages.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15].

    Relationship: dependency 'monitors flight progress with' -> EtfmsSystem

    Relationship: association 'receives' -> DpiMessage [*]
    """

    def issueCtot(self, flight: Flight) -> TimeQuantity:
        """The CTOT is issued by Network Operations at EOBT-2 hr if the flight is regulated (M2)."""
        raise NotImplementedError


@dataclass
class OffBlockMilestone(Milestone):
    """Milestone 15: AOBT, the time the aircraft pushes back/vacates the parking position.

    Package Milestones, stereotype control, milestones [15].
    """

    def recordAobt(self, flight: Flight) -> TimeQuantity:
        """Informs all relevant Airport CDM Partners of the Actual Off-Block Time (AOBT), confirming push-back/taxi has commenced."""
        raise NotImplementedError

    def sendADpi(self, flight: Flight) -> None:
        """AOBT always triggers an A-DPI message to Network Operations, or at a defined time prior to TTOT in case of remote holding."""
        raise NotImplementedError

    def checkTtotToleranceAndInform(self, flight: Flight) -> bool:
        """After the first A-DPI is sent, checks TTOT updates against the TTOT tolerance before Network Operations is informed with a new A-DPI of the updated TTOT."""
        raise NotImplementedError


@dataclass
class StandGateManagement(AirportCdmPartner):
    """The party responsible for stand and gate allocation decisions that depend on accurate ELDT and EIBT.

    Package Stakeholders, stereotype entity, milestones [4].
    """
    pass


@dataclass
class StartUpApproved(Milestone):
    """Milestone 14: ATC grants start up approval to the aircraft (ASAT).

    Package Milestones, stereotype control, milestones [14].
    """

    def recordAsat(self, flight: Flight) -> TimeQuantity:
        """Informs all relevant Airport CDM Partners of the Actual Start-up Approval Time (ASAT), confirming the aircraft has received start up approval/push-back clearance."""
        raise NotImplementedError

    def checkAsatAgainstTsat(self, flight: Flight, tolerance: timedelta) -> bool:
        """Checks if ASAT is in accordance with TSAT; if start up approval is not granted at TSAT+tolerance, all relevant partners are informed and the flight is re-sequenced."""
        raise NotImplementedError


@dataclass
class StartUpRequested(Milestone):
    """Milestone 13: the time that start up is requested by the pilot via ATC (ASRT).

    Package Milestones, stereotype control, milestones [13].
    """

    def recordAsrt(self, flight: Flight) -> TimeQuantity:
        """Informs all relevant Airport CDM Partners of the Actual Start-up Request Time (ASRT) when it occurs."""
        raise NotImplementedError

    def checkStartUpRequestedWithinTolerance(self, flight: Flight, tolerance: timedelta) -> bool:
        """Alerts all relevant partners when no start up has been requested inside the locally agreed TSAT tolerance window; if not made by TSAT+tolerance, AO/GH is informed and should update TOBT."""
        raise NotImplementedError


@dataclass
class TakeOffFromOutstation(Milestone):
    """Milestone 3: the ATOT from the outstation (ADEP) is recorded and used to update ELDT and downstream estimates.

    Package Milestones, stereotype control, milestones [3].
    """

    def checkLandingEstimateConsistency(self, flight: Flight) -> bool:
        """Checks whether AO/GH estimated landing time after take off from outstation is consistent with the outbound ATC Flight Plan."""
        raise NotImplementedError

    def sendTDpiT(self, flight: Flight) -> None:
        """Informs Network Operations about the updated take off time estimate using a T-DPI-t message; a TTOT tolerance of 5 minutes is respected first."""
        raise NotImplementedError


@dataclass
class TakeOffMilestone(Milestone):
    """Milestone 16: ATOT, the actual take off time, ending the departure sequence for the flight.

    Package Milestones, stereotype control, milestones [16].
    """

    def recordAtot(self, flight: Flight) -> TimeQuantity:
        """Informs all relevant Airport CDM Partners about the actual take off, triggered by Tower FDPS, A-SMGCS/Radar detection or ACARS."""
        raise NotImplementedError

    def sendFsaAndMvtMessages(self, flight: Flight) -> None:
        """FSA and MVT messages are sent on take off."""
        raise NotImplementedError

    def removeFromDepartureSequence(self, flight: Flight) -> None:
        """An airborne message is generated and the flight is removed from the departure sequence."""
        raise NotImplementedError


@dataclass
class TimeQuantity:
    """A single dated value of a named time quantity (identified by prefix and event) for a flight, recorded with its originator, accuracy and update time; every successive value is kept rather than overwritten.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    prefixType: PrefixType | None = None
    eventType: EventType | None = None
    value: datetime | None = None
    originator: str | None = None
    accuracy: str | None = None
    tolerance: timedelta | None = None
    recordedAt: datetime | None = None

    def update(self, newValue: datetime, originator: str, timestamp: datetime) -> TimeQuantity:
        """Appends a new successive value for this time quantity rather than overwriting the previous one, so the turn-round can be analysed afterwards."""
        raise NotImplementedError

    def calculateEldtFromAtot(self, atot: TimeQuantity, estimatedElapsedTime: timedelta) -> datetime:
        """Using the ATOT, ELDT is calculated using the Estimated Elapsed Time on the FPL (M3)."""
        raise NotImplementedError

    def calculateEibt(self, landingTime: TimeQuantity, exit: timedelta) -> datetime:
        """EIBT is computed using the ELDT/ALDT and the estimated taxi-in time (EXIT) (M4, M6)."""
        raise NotImplementedError

    def calculateTtot(self, eibt: TimeQuantity, mttt: timedelta, exot: timedelta, eobt: TimeQuantity, tobt: TimeQuantity) -> datetime:
        """Calculation basis for TTOT takes into account EIBT+MTTT+EXOT, if later than EOBT+EXOT; if TOBT is manually input it overrides the EIBT+MTTT estimate, so TTOT equals TOBT+EXOT (M2, M3)."""
        raise NotImplementedError

    def checkTtotToleranceExceeded(self, newTtot: datetime, tolerance: timedelta) -> bool:
        """Checks whether TTOT has changed by more than the agreed TTOT tolerance, in which case Network Operations must be informed (M4-M10, M15)."""
        raise NotImplementedError


@dataclass
class TsatIssued(Milestone):
    """Milestone 10: ATC issues the Target Start Up Approval Time, stabilising the flight into the pre-departure sequence.

    Package Milestones, stereotype control, milestones [10].
    """

    def issueTsat(self, flight: Flight) -> TimeQuantity:
        """Informs all relevant partners of the TSAT allocated to the flight; Network Operations is informed by a T-DPI-s for non-regulated flights."""
        raise NotImplementedError

    def checkTobtUpdateCount(self, flight: Flight, threshold: int) -> bool:
        """Checks whether the number of TOBT updates exceeds a locally defined tolerance after TSAT has been issued; if exceeded the TOBT input is processed per local procedure."""
        raise NotImplementedError


@dataclass
class TurnRound:
    """The aircraft turn-round comprising a related arriving and departing flight, described by a defined turn-round period.

    Package Flights, stereotype entity, milestones [1, 6, 7, 8].

    Relationship: aggregation 'comprises arrival and departure flight' -> Flight [2]
    """
    mttt: timedelta | None = None
