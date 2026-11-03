"""Class stubs rendered from runs/single_high/run_01/model.json by src/generate/render_code.py; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from enum import Enum


class DPIType(Enum):
    E_DPI = "E-DPI"
    T_DPI = "T-DPI"
    T_DPI_T = "T-DPI-t"
    T_DPI_S = "T-DPI-s"
    A_DPI = "A-DPI"


class FlightDirection(Enum):
    ARRIVAL = "Arrival"
    DEPARTURE = "Departure"


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
    DEPARTED_TAKE_OFF = "DEPARTED / TAKE OFF"


class FlightPlanType(Enum):
    STANDARD = "Standard"
    RFPL = "RFPL"


class SlotCoordinationStatus(Enum):
    COORDINATED = "Coordinated"
    NON_COORDINATED = "Non-Coordinated"


class TimePrefix(Enum):
    SCHEDULED = "Scheduled"
    ESTIMATED = "Estimated"
    TARGET = "Target"
    ACTUAL = "Actual"
    CALCULATED = "Calculated"


@dataclass
class ACARS:
    """The aircraft's ACARS system that reports ON/OFF/OUT/IN events, providing ATOT, ALDT, AIBT, and AOBT.

    Package Systems, stereotype boundary, milestones [6, 7, 15, 16].

    Relationship: dependency 'reports times for' -> Flight
    """
    pass


@dataclass
class ATCFlightPlan:
    """The ICAO flight plan submitted to ATC and distributed by IFPS, describing the flight's aerodromes and estimates, corresponding to the airport slot programme.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9].

    Relationship: association 'submitted by' -> AircraftOperator [1]

    Relationship: dependency 'distributed by' -> IFPS
    """
    type: FlightPlanType | None = None
    departureAerodrome: str | None = None
    destinationAerodrome: str | None = None
    sobt: OffBlockTime | None = None


@dataclass
class ATCSystem:
    """The ATC/radar system, including A-SMGCS and Tower FDPS, that detects a flight crossing FIR/TMA boundaries or levels using its assigned SSR code, and provides ALDT, AIBT, AOBT, and ATOT.

    Package Systems, stereotype boundary, milestones [3, 4, 5, 6, 7, 15, 16].

    Relationship: dependency 'detects / reports times for' -> Flight
    """

    def detectFlight(self, flight: Flight) -> datetime:
        """Detects a flight based upon the assigned SSR code when it crosses a defined FIR/ATC boundary (milestone 4) or a defined range/position or level on Final Approach (milestone 5)."""
        raise NotImplementedError


@dataclass
class Stakeholder:
    """A party that takes part in the CDM process and originates or receives flight information.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    name: str | None = None


@dataclass
class AirTrafficControl(Stakeholder):
    """The air traffic control units (ATS units, Area Control Centre, Approach Control Unit, Tower) that provide radar detection, issue TSAT/start-up approval, and manage the pre-departure sequence.

    Package Stakeholders, stereotype entity, milestones [1, 4, 5, 9, 10, 12, 13, 14, 15, 16].

    Relationship: dependency 'issues TSAT / approves ASAT' -> StartUpApprovalTime

    Relationship: dependency 'calculates EXOT for' -> TaxiOutTime
    """

    def issueTSAT(self, flight: Flight, t: timedelta) -> datetime:
        """ATC issues the Target Start Up Approval Time t minutes before EOBT, a locally agreed parameter (milestone 10)."""
        raise NotImplementedError

    def approveStartUp(self, flight: Flight) -> None:
        """ATC gives the aircraft its start up approval / push-back clearance (milestone 14)."""
        raise NotImplementedError

    def establishPushBackSequence(self, flight: Flight) -> None:
        """An accurate TOBT at EOBT-t minutes is a pre-requisite for ATC to establish a push back / pre-departure sequence (milestone 9)."""
        raise NotImplementedError

    def calculateEXOT(self, flight: Flight) -> timedelta:
        """Following receipt of TOBT, the ATC system calculates and provides the Estimated Taxi-Out Time based on the predicted traffic load, gate/stand location, runway in use, and waiting period at the Holding Position (milestone 9)."""
        raise NotImplementedError

    def refineSequence(self, flight: Flight) -> None:
        """ATC refines the pre-departure sequence once the aircraft is ready (milestone 12)."""
        raise NotImplementedError

    def confirmTSATToPilot(self, flight: Flight) -> None:
        """ATC confirms TSAT to the pilot in order to maintain the aircraft in the pre-departure sequence (milestone 13)."""
        raise NotImplementedError

    def reSequenceFlight(self, flight: Flight) -> None:
        """If start-up approval is not granted at TSAT+tolerance, the flight is re-sequenced (milestone 14)."""
        raise NotImplementedError


@dataclass
class Message:
    """A message exchanged between stakeholders and systems in the CDM process.

    Package Messages, stereotype boundary, milestones [1, 2, 3, 10, 15, 16].

    Relationship: association 'exchanged with' -> Stakeholder [1..*]
    """
    sender: str | None = None
    timestamp: datetime | None = None
    content: str | None = None


@dataclass
class AirborneMessage(Message):
    """The airborne message generated when the flight departs, after which the flight is removed from the departure sequence.

    Package Messages, stereotype boundary, milestones [16].
    """
    pass


@dataclass
class Aircraft:
    """The aircraft assigned to operate the flight, whose type may be updated from the flight plan.

    Package Flights, stereotype entity, milestones [1].
    """
    registration: str | None = None
    aircraftType: str | None = None


@dataclass
class AircraftOperator(Stakeholder):
    """The airline (AO) responsible for operating the flight, submitting the ATC Flight Plan, and providing TOBT and other turn-round estimates.

    Package Stakeholders, stereotype entity, milestones [1, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14].

    Relationship: dependency 'provides TOBT' -> OffBlockTime
    """

    def provideTOBT(self, flight: Flight, value: datetime) -> None:
        """The AO/GH provides the TOBT, calculated on the basis of the estimated/defined turn-round period, updated automatically or inserted manually (milestones 6,7,8)."""
        raise NotImplementedError

    def computeTOBTStrategy(self, flight: Flight) -> datetime:
        """The Aircraft Operator integrates his own strategy to compute a TOBT related to the flight, providing the most accurate TOBT taking into account the operational situation (milestone 9)."""
        raise NotImplementedError


@dataclass
class Milestone:
    """One of the sixteen defined events of the CDM turn-round process, each with a trigger, timing rule, effect, and procedure.

    Package Milestones, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: dependency 'acts on' -> Flight

    Relationship: dependency 'updates fields on' -> AirportCDMPlatform
    """
    definition: str | None = None
    trigger: str | None = None
    timingRule: str | None = None
    effect: str | None = None
    resultingStatus: FlightOperationalStatus | None = None

    def occur(self, flight: Flight, timestamp: datetime) -> None:
        """Records the occurrence of the milestone for the flight and changes its operational status."""
        raise NotImplementedError

    def informPartners(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners, a step stated under most milestones' procedures."""
        raise NotImplementedError


@dataclass
class AircraftReady(Milestone):
    """Milestone 12: the time when all doors are closed, boarding bridge removed, push back vehicle connected, ready to taxi upon reception of TWR instructions (ARDT).

    Package Milestones, stereotype control, milestones [12].
    """

    def recordARDT(self, flight: Flight, timestamp: datetime) -> None:
        """Informs all relevant Airport CDM Partners of Actual Ready Time and that the aircraft is ready for start up / push-back."""
        raise NotImplementedError

    def checkReadyStatusReceived(self, flight: Flight, tolerance: timedelta) -> bool:
        """At TOBT + tolerance, informs the AO/GH that TOBT has passed and the Airport CDM Platform has not yet received ARDT or Ready Status (RDY)."""
        raise NotImplementedError


@dataclass
class Aircrew(Stakeholder):
    """The flight crew (pilot) that requests start-up and coordinates with the Ground Handler.

    Package Stakeholders, stereotype entity, milestones [12, 13, 14].

    Relationship: dependency 'requests' -> StartUpRequestTime
    """

    def requestStartUp(self, flight: Flight) -> None:
        """The pilot requests start up just before TSAT, following coordination with the Ground Handler, by voice or DCL (milestones 12,13,14)."""
        raise NotImplementedError


@dataclass
class AirportCDMPlatform:
    """The central platform that is initiated for each flight, processes all available information, and holds the CDM operation actions performed at each milestone.

    Package Systems, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'initiated for / holds data of' -> Flight [0..*]
    """
    initiated: bool | None = None

    def initiateForFlight(self, flight: Flight) -> None:
        """The Airport CDM Platform is initiated for this flight, and all available information is processed (milestone 1)."""
        raise NotImplementedError

    def updateField(self, flight: Flight, fieldName: str, value: datetime) -> None:
        """Updates fields such as ELDT, EIBT, ETOT, TOBT, TTOT, AOBT, ATOT as listed under each milestone's Action on CDM Operation."""
        raise NotImplementedError

    def markFieldAsRegulated(self, flight: Flight) -> None:
        """Marks appropriate fields as REGULATED (milestone 2)."""
        raise NotImplementedError


@dataclass
class AirportFlightData:
    """The airport's own flight data record checked for consistency against the ATC Flight Plan and Airport Slot.

    Package Flights, stereotype entity, milestones [1].
    """
    gateStandAllocation: str | None = None


@dataclass
class AirportOperator(Stakeholder):
    """The airport authority / stand-gate management function responsible for the airport slot programme and airport flight data.

    Package Stakeholders, stereotype entity, milestones [1, 4].
    """
    pass


@dataclass
class AirportSlot:
    """The airport slot programme entry that the ATC Flight Plan must correspond to.

    Package Flights, stereotype entity, milestones [1].
    """
    coordinationStatus: SlotCoordinationStatus | None = None


@dataclass
class BoardingStarts(Milestone):
    """Milestone 11: the gate is open for passengers to physically start boarding.

    Package Milestones, stereotype control, milestones [11].
    """

    def recordASBT(self, flight: Flight, timestamp: datetime) -> None:
        """Informs all relevant Airport CDM Partners of the Actual Start Boarding Time when it occurs."""
        raise NotImplementedError

    def checkBoardingStatus(self, flight: Flight, minutesBeforeTOBT: timedelta) -> bool:
        """At a certain local time before TOBT (e.g. by aircraft type), checks whether boarding starts in time to respect TOBT and informs the AO/GH if TOBT needs to be updated."""
        raise NotImplementedError


@dataclass
class TimeQuantity:
    """A time value describing a flight's progress, carrying its prefix, origin, accuracy, and update time; every successive value is kept rather than overwritten so a turn-round can be analysed afterwards.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    value: datetime | None = None
    prefix: TimePrefix | None = None
    originator: str | None = None
    accuracy: str | None = None
    updateTime: datetime | None = None

    def recordValue(self, value: datetime, originator: str, timestamp: datetime) -> None:
        """Appends a new time value with its originator and time of update, rather than overwriting the previous value, so the turn-round can be analysed afterwards."""
        raise NotImplementedError


@dataclass
class BoardingTime(TimeQuantity):
    """The actual start boarding time (ASBT), when the gate opens for passengers to physically start boarding.

    Package Timings, stereotype entity, milestones [11].
    """
    pass


@dataclass
class DPIMessage(Message):
    """A Departure Planning Information message sent to Network Operations at defined points of the process.

    Package Messages, stereotype boundary, milestones [1, 2, 3, 10, 15].
    """
    dpiType: DPIType | None = None


@dataclass
class DPIProcess:
    """The messaging process that commences correct DPI messaging with Network Operations following flight plan activation.

    Package Systems, stereotype control, milestones [1].

    Relationship: dependency 'sends messages to' -> NetworkOperations
    """

    def commenceMessaging(self, flight: Flight) -> None:
        """The DPI process commences the correct messaging with Network Operations, if implemented (milestone 1)."""
        raise NotImplementedError


@dataclass
class EOBTMinus2Hours(Milestone):
    """Milestone 2: at EOBT-2hr most flights are known and all regulated flights receive a CTOT from Network Operations.

    Package Milestones, stereotype control, milestones [2].

    Relationship: dependency 'sends T-DPI' -> DPIMessage
    """

    def checkFlightEstimatesConsistency(self, flight: Flight) -> bool:
        """Checks whether AO/GH flight estimates are consistent with the ATC Flight Plan, before or after take-off from outstation, to verify feasibility of the estimated off-block time at EOBT-2hrs."""
        raise NotImplementedError

    def sendFirstTDPI(self, flight: Flight) -> None:
        """Informs Network Operations about the updated take-off time estimate using a T-DPI message at EOBT-2hrs."""
        raise NotImplementedError

    def markAsRegulated(self, flight: Flight) -> None:
        """Marks appropriate fields as REGULATED for a flight that has received a CTOT."""
        raise NotImplementedError


@dataclass
class ETFMS:
    """Network Operations' system used to monitor the progress of a flight within 3 hours flying time of the destination and to generate Flight Update Messages.

    Package Systems, stereotype boundary, milestones [3].

    Relationship: dependency 'generates' -> FUM
    """
    pass


@dataclass
class FSAMessage(Message):
    """The FSA message sent when a flight takes off.

    Package Messages, stereotype boundary, milestones [16].
    """
    pass


@dataclass
class FUM(Message):
    """The Flight Update Message sent by Network Operations providing updates of the flight's progress.

    Package Messages, stereotype boundary, milestones [2, 3].
    """
    pass


@dataclass
class FinalApproach(Milestone):
    """Milestone 5: the flight enters the Final Approach phase at the destination airport, usually 2 to 5 minutes from landing.

    Package Milestones, stereotype control, milestones [5].
    """

    def commenceTOBTProcess(self, flight: Flight) -> None:
        """Commences the TOBT process and checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated ELDT."""
        raise NotImplementedError

    def notifyNetworkOperationsIfTTOTChanges(self, flight: Flight, tolerance: timedelta) -> None:
        """Network Operations is informed when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class FinalConfirmationOfTOBT(Milestone):
    """Milestone 9: the time at which the Aircraft Operator or Ground Handler provide their most accurate TOBT, taking into account the operational situation.

    Package Milestones, stereotype control, milestones [9].
    """

    def confirmTOBT(self, flight: Flight, t: timedelta) -> None:
        """The AO/GH provide their most accurate TOBT t minutes before EOBT (t a locally agreed parameter), a pre-requisite for ATC to establish the pre-departure sequence prior to TSAT issue."""
        raise NotImplementedError

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan; performed at a predefined local time to confirm TOBT prior to TSAT issue."""
        raise NotImplementedError

    def notifyNetworkOperationsIfTTOTChanges(self, flight: Flight, tolerance: timedelta) -> None:
        """Network Operations is informed when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class Flight:
    """A single flight movement, arriving or departing, tracked through the sixteen milestones of the CDM turn-round process.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'described by' -> ATCFlightPlan [1]

    Relationship: association 'corresponds to' -> AirportSlot [0..1]

    Relationship: association 'operated by' -> Aircraft [1]

    Relationship: association 'has' -> AirportFlightData [1]

    Relationship: association 'has' -> OffBlockTime [0..*]

    Relationship: association 'has' -> InBlockTime [0..*]

    Relationship: association 'has' -> LandingTime [0..*]

    Relationship: association 'has' -> TakeOffTime [0..*]

    Relationship: association 'has' -> StartUpApprovalTime [0..*]

    Relationship: association 'has' -> StartUpRequestTime [0..1]

    Relationship: association 'has' -> ReadyTime [0..1]

    Relationship: association 'has' -> BoardingTime [0..1]

    Relationship: association 'has' -> GroundHandlingTime [0..1]

    Relationship: association 'has' -> TaxiOutTime [0..1]

    Relationship: association 'has' -> TaxiInTime [0..1]
    """
    aircraftRegistration: str | None = None
    direction: FlightDirection | None = None
    operationalStatus: FlightOperationalStatus | None = None
    regulated: bool | None = None
    flightReadyTime: timedelta | None = None

    def updateOperationalStatus(self, newStatus: FlightOperationalStatus) -> None:
        """Changes the flight's operational status as each milestone occurs."""
        raise NotImplementedError


@dataclass
class FlightPlanActivated(Milestone):
    """Milestone 1: the ICAO flight plan is submitted to ATC and the Airport CDM Platform is initiated for the flight.

    Package Milestones, stereotype control, milestones [1].

    Relationship: dependency 'sends E-DPI' -> DPIMessage
    """

    def checkConsistency(self, flightPlan: ATCFlightPlan, slot: AirportSlot, flightData: AirportFlightData) -> bool:
        """Checks consistency between the ATC Flight Plan, Airport Slot, and Airport flight data before the first E-DPI is sent."""
        raise NotImplementedError

    def confirmFlightToNetworkOperations(self, flight: Flight) -> None:
        """Confirms the flight to Network Operations and allows further local processing of the flight."""
        raise NotImplementedError

    def sendFirstEDPI(self, flight: Flight) -> None:
        """Feeds Network Operations with consistent SOBT, aircraft registration, and first destination data; the E-DPI message should not be sent if no or inconsistent information is provided."""
        raise NotImplementedError


@dataclass
class GroundHandler(Stakeholder):
    """The party (GH), possibly including dispatcher/supervisor roles, that manages the turn-round process in coordination with the aircrew and provides TOBT and ready status.

    Package Stakeholders, stereotype entity, milestones [6, 7, 8, 9, 10, 11, 12, 13].

    Relationship: dependency 'provides TOBT' -> OffBlockTime
    """

    def manageTurnRoundProcess(self, flight: Flight) -> None:
        """The Ground Handler, in coordination with the aircrew, manages the turn-round process following TOBT confirmation and TSAT issue (milestones 9,10)."""
        raise NotImplementedError


@dataclass
class GroundHandlingStarted(Milestone):
    """Milestone 8: commencement of ground handling operations (ACGT), specific to first-operation-of-day or long-term parked flights.

    Package Milestones, stereotype control, milestones [8].
    """

    def recordACGT(self, flight: Flight, timestamp: datetime) -> None:
        """ACGT triggers an update of downstream estimates: TOBT updated automatically or inserted manually by AO/GH, calculated on the basis of the estimated turn-round period."""
        raise NotImplementedError

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT or ATC Flight Plan."""
        raise NotImplementedError

    def notifyNetworkOperationsIfTTOTChanges(self, flight: Flight, tolerance: timedelta) -> None:
        """Network Operations is informed when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class GroundHandlingTime(TimeQuantity):
    """The actual commence ground handling time (ACGT); for a normal turn-round ACGT is considered to commence at AIBT, but this milestone applies specifically to first-operation-of-day or long-term parked flights.

    Package Timings, stereotype entity, milestones [7, 8].
    """
    pass


@dataclass
class IFPS:
    """The system that distributes the ATC Flight Plan to all involved ATC units, including departure and destination aerodromes.

    Package Systems, stereotype boundary, milestones [1].
    """
    pass


@dataclass
class InBlock(Milestone):
    """Milestone 7: AIBT, the time an aircraft arrives in-blocks.

    Package Milestones, stereotype control, milestones [7].
    """

    def recordAIBT(self, flight: Flight, timestamp: datetime) -> None:
        """AIBT triggers an update of downstream estimates: TOBT and TTOT updated automatically or inserted manually by AO/GH, calculated on the basis of the estimated turn-round period."""
        raise NotImplementedError

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT or ATC Flight Plan."""
        raise NotImplementedError

    def notifyNetworkOperationsIfTTOTChanges(self, flight: Flight, tolerance: timedelta) -> None:
        """Network Operations is informed when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class InBlockTime(TimeQuantity):
    """The estimated (EIBT) or actual (AIBT) in-block time of an arriving flight.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7].
    """

    def calculateEIBT(self, eldt: LandingTime, exit: TaxiInTime) -> datetime:
        """EIBT is computed using the ELDT and the estimated taxi-in time EXIT (milestone 4); EIBT can also be updated according to ALDT+EXIT (milestone 6)."""
        raise NotImplementedError


@dataclass
class Landed(Milestone):
    """Milestone 6: ALDT, the time an aircraft touches down on a runway.

    Package Milestones, stereotype control, milestones [6].
    """

    def recordALDT(self, flight: Flight, timestamp: datetime) -> None:
        """ALDT triggers an update of downstream estimates: TOBT and TTOT updated automatically or inserted manually by AO/GH, calculated on the basis of the defined turn-round period; EIBT updated according to ALDT+EXIT."""
        raise NotImplementedError

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT or ATC Flight Plan."""
        raise NotImplementedError

    def notifyNetworkOperationsIfTTOTChanges(self, flight: Flight, tolerance: timedelta) -> None:
        """Network Operations is informed when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class LandingTime(TimeQuantity):
    """The estimated (ELDT) or actual (ALDT) landing time of an arriving flight.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6].
    """

    def calculateELDT(self, atot: TakeOffTime, estimatedElapsedTime: timedelta) -> datetime:
        """Using the ATOT, an ELDT can be calculated by using the Estimated Elapsed Time on the FPL (milestone 3)."""
        raise NotImplementedError


@dataclass
class LocalRadarUpdate(Milestone):
    """Milestone 4: the flight enters the FIR or local airspace of the destination airport.

    Package Milestones, stereotype control, milestones [4].
    """

    def commenceTOBTProcess(self, flight: Flight) -> None:
        """Commences the TOBT process and checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated ELDT."""
        raise NotImplementedError

    def notifyNetworkOperationsIfTTOTChanges(self, flight: Flight, tolerance: timedelta) -> None:
        """Network Operations is informed when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError

    def restrictStandGateChange(self, flight: Flight) -> bool:
        """Taking into account EXIT, any change to a stand or gate is not preferred after ELDT-30'."""
        raise NotImplementedError


@dataclass
class MVTMessage(Message):
    """The movement message sent when a flight takes off.

    Package Messages, stereotype boundary, milestones [16].
    """
    pass


@dataclass
class NetworkOperations(Stakeholder):
    """The network operations function that issues CTOT for regulated flights, monitors flight progress, and receives DPI/FUM messages.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15].

    Relationship: association 'issues CTOT to' -> Flight [0..*]

    Relationship: dependency 'sends' -> FUM
    """

    def issueCTOT(self, flight: Flight) -> datetime:
        """If the flight is regulated, Network Operations issues a CTOT at EOBT-2h, sent to relevant ATS units and the departure aerodrome; CTOT flights usually have priority over unregulated flights (milestone 2)."""
        raise NotImplementedError

    def monitorFlightProgress(self, flight: Flight) -> None:
        """Within 3 hours flying time of the destination, Network Operations monitors progress of the flight using ETFMS and sends a Flight Update Message (milestone 3)."""
        raise NotImplementedError


@dataclass
class OffBlock(Milestone):
    """Milestone 15: AOBT, the time the aircraft pushes back / vacates the parking position.

    Package Milestones, stereotype control, milestones [15].

    Relationship: dependency 'sends A-DPI' -> DPIMessage
    """

    def recordAOBT(self, flight: Flight, timestamp: datetime) -> None:
        """Informs all relevant Airport CDM Partners of Actual Off-Block Time and that the aircraft has commenced push-back / taxi from parking position."""
        raise NotImplementedError

    def sendADPI(self, flight: Flight) -> None:
        """AOBT always triggers an A-DPI message to Network Operations, or in the case of remote holding at a defined time prior to TTOT."""
        raise NotImplementedError

    def checkTTOTChangeAndNotify(self, flight: Flight, tolerance: timedelta) -> None:
        """After the first A-DPI is sent, checks TTOT updates against the TTOT tolerance before informing Network Operations, with a new A-DPI, of the updated TTOT."""
        raise NotImplementedError


@dataclass
class OffBlockTime(TimeQuantity):
    """The scheduled (SOBT), estimated (EOBT), target (TOBT), or actual (AOBT) off-block time of a flight.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 6, 7, 8, 9, 10, 15].
    """
    toleranceWindow: timedelta | None = None


@dataclass
class ReadyTime(TimeQuantity):
    """The actual ready time (ARDT), when all doors are closed and the aircraft is ready to taxi upon reception of TWR instructions.

    Package Timings, stereotype entity, milestones [12].
    """
    pass


@dataclass
class StartUpApprovalTime(TimeQuantity):
    """The target (TSAT) or actual (ASAT) start-up approval time.

    Package Timings, stereotype entity, milestones [10, 14].
    """
    pass


@dataclass
class StartUpApproved(Milestone):
    """Milestone 14: ASAT, the time an aircraft receives its start up approval.

    Package Milestones, stereotype control, milestones [14].
    """

    def recordASAT(self, flight: Flight, timestamp: datetime) -> None:
        """Informs all relevant Airport CDM Partners of Actual start up approval Time and that the aircraft has received start up / push-back clearance."""
        raise NotImplementedError

    def checkASATAgainstTSAT(self, flight: Flight, tolerance: timedelta) -> bool:
        """Checks if ASAT is in accordance with TSAT; if start-up approval is not granted at TSAT + tolerance, all relevant partners are informed and the flight is re-sequenced."""
        raise NotImplementedError


@dataclass
class StartUpRequestTime(TimeQuantity):
    """The actual start-up request time (ASRT).

    Package Timings, stereotype entity, milestones [13].
    """
    pass


@dataclass
class StartUpRequested(Milestone):
    """Milestone 13: the time that start up is requested (ASRT), based on pilot request.

    Package Milestones, stereotype control, milestones [13].
    """

    def recordASRT(self, flight: Flight, timestamp: datetime) -> None:
        """Informs all relevant Airport CDM Partners of Actual Start-up Request Time when it occurs."""
        raise NotImplementedError

    def alertIfNoStartUpRequested(self, flight: Flight, tsatTolerance: timedelta) -> bool:
        """If the start-up request is not made by TSAT + tolerance, informs the AO/GH that no start-up has been requested, and that TOBT should be updated."""
        raise NotImplementedError


@dataclass
class TSATIssued(Milestone):
    """Milestone 10: the time ATC issues the Target Start Up Approval Time.

    Package Milestones, stereotype control, milestones [10].

    Relationship: dependency 'sends T-DPI-s' -> DPIMessage
    """

    def issueTSAT(self, flight: Flight, t: timedelta) -> None:
        """Informs all relevant partners of the TSAT allocated to the flight, t minutes before EOBT (a locally agreed parameter); stabilises the flight into the pre-departure sequence."""
        raise NotImplementedError

    def sendTDPIs(self, flight: Flight) -> None:
        """Network Operations is informed by a T-DPI-s for non-regulated flights."""
        raise NotImplementedError

    def checkTOBTUpdateCount(self, flight: Flight, threshold: int) -> bool:
        """Checks whether the number of TOBT updates after TSAT has been issued exceeds a locally defined threshold; if exceeded, the TOBT input is processed according to local procedure."""
        raise NotImplementedError


@dataclass
class TakeOff(Milestone):
    """Milestone 16: ATOT, the time an aircraft takes off from the runway.

    Package Milestones, stereotype control, milestones [16].

    Relationship: dependency 'sends' -> MVTMessage

    Relationship: dependency 'sends' -> FSAMessage

    Relationship: dependency 'generates' -> AirborneMessage
    """

    def recordATOT(self, flight: Flight, timestamp: datetime) -> None:
        """Informs all relevant Airport CDM Partners about the actual take off, triggered by Tower FDPS, A-SMGCS / Radar detection or ACARS."""
        raise NotImplementedError

    def generateAirborneMessage(self, flight: Flight) -> None:
        """An airborne message is generated and the flight is removed from the departure sequence."""
        raise NotImplementedError

    def sendFSAAndMVT(self, flight: Flight) -> None:
        """FSA and MVT messages are sent."""
        raise NotImplementedError


@dataclass
class TakeOffFromOutstation(Milestone):
    """Milestone 3: the ATOT from the outstation (ADEP).

    Package Milestones, stereotype control, milestones [3].

    Relationship: dependency 'sends T-DPI-t' -> DPIMessage
    """

    def checkLandingEstimateConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH estimated landing time after take-off from outstation is consistent with the outbound ATC Flight Plan."""
        raise NotImplementedError

    def sendTDPIt(self, flight: Flight) -> None:
        """When needed, informs Network Operations about updated take-off time estimates using a T-DPI-t message; a TTOT tolerance of 5 minutes is respected before informing."""
        raise NotImplementedError


@dataclass
class TakeOffTime(TimeQuantity):
    """The estimated (ETOT), target (TTOT), calculated (CTOT), or actual (ATOT) take-off time of a departing flight.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 16].
    """

    def calculateTTOT(self, eibt: InBlockTime, mttt: timedelta, exot: TaxiOutTime, eobt: OffBlockTime, tobt: OffBlockTime) -> datetime:
        """Calculation basis for TTOT takes into account EIBT+MTTT+EXOT, if later than EOBT+EXOT (milestone 2); in case EOBT is later than EIBT+MTTT, TTOT equals EOBT+EXOT (milestone 3); in the case of manual input of TOBT, this estimate overrides the EIBT+MTTT estimate, hence TTOT equals TOBT+EXOT (milestones 2,3)."""
        raise NotImplementedError


@dataclass
class TaxiInTime:
    """The estimated taxi-in time (EXIT) used to compute the estimated in-block time.

    Package Timings, stereotype entity, milestones [4, 6].
    """
    duration: timedelta | None = None


@dataclass
class TaxiOutTime:
    """The estimated taxi-out time (EXOT), calculated by ATC based on predicted traffic load, gate/stand location, runway in use, and waiting period at the Holding Position.

    Package Timings, stereotype entity, milestones [2, 3, 9].
    """
    duration: timedelta | None = None


@dataclass
class TurnRound:
    """The turn-round of an aircraft, which normally includes an arriving and a departing flight.

    Package Flights, stereotype entity, milestones [1, 4, 6, 7, 8].

    Relationship: aggregation 'includes' -> Flight [1..2]
    """
    minimumTurnRoundTime: timedelta | None = None
