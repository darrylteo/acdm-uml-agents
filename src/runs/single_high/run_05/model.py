"""Class stubs rendered from runs/single_high/run_05/model.json by src/generate/render_code.py; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from enum import Enum


class DPIMessageType(Enum):
    E_DPI = "E-DPI"
    T_DPI = "T-DPI"
    T_DPI_T = "T-DPI-t"
    T_DPI_S = "T-DPI-s"
    A_DPI = "A-DPI"


class FlightDirection(Enum):
    ARRIVAL = "Arrival"
    DEPARTURE = "Departure"


class FlightStatus(Enum):
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


class TaxiDirection(Enum):
    OUT = "Out"
    IN = "In"


class TimePrefix(Enum):
    SCHEDULED = "Scheduled"
    ESTIMATED = "Estimated"
    TARGET = "Target"
    ACTUAL = "Actual"
    CALCULATED = "Calculated"


@dataclass
class ACARS:
    """The aircraft communications addressing and reporting system that reports landing, in-block, off-block and take-off events for equipped aircraft.

    Package Systems, stereotype boundary, milestones [6, 7, 15, 16].

    Relationship: dependency 'reports movement events for' -> Flight
    """

    def reportMovementEvent(self, flight: Flight, eventCode: str) -> TimeQuantity:
        """Reports ACARS ON/IN/OUT/OFF events corresponding to ALDT, AIBT, AOBT and ATOT (milestones 6, 7, 15, 16)."""
        raise NotImplementedError


@dataclass
class ATCSystem:
    """The ATC technical system (including radar and A-SMGCS) that detects a flight's position and calculates the Estimated Taxi-Out Time.

    Package Systems, stereotype boundary, milestones [4, 5, 9, 16].

    Relationship: dependency 'calculates EXOT' -> TaxiTime

    Relationship: dependency 'detects' -> Flight
    """

    def calculateEXOT(self, flight: Flight, tobt: OffBlockTime) -> TaxiTime:
        """Following receipt of TOBT, the ATC system calculates and provides the Estimated Taxi-Out Time (EXOT) based on predicted traffic load, gate/stand location, runway in use, and waiting period at the Holding Position (milestone 9)."""
        raise NotImplementedError

    def detectFlight(self, flight: Flight) -> None:
        """Detects the flight by radar in FIR, TMA, or on Final Approach, or via A-SMGCS/Radar at take-off (milestones 4, 5, 16)."""
        raise NotImplementedError


@dataclass
class AirTrafficControl:
    """The air traffic control organisation, including ACC, Approach Control Unit and Tower units, that issues TSAT, approves start-up, and sequences departing flights.

    Package Stakeholders, stereotype entity, milestones [1, 4, 5, 9, 10, 12, 13, 14, 16].

    Relationship: dependency 'issues' -> StartUpApprovalTime
    """
    unitType: str | None = None

    def issueTSAT(self, flight: Flight) -> StartUpApprovalTime:
        """ATC issues the Target Start Up Approval Time, t minutes before EOBT, a locally agreed parameter (milestone 10)."""
        raise NotImplementedError

    def approveStartUp(self, flight: Flight) -> StartUpApprovalTime:
        """ATC provides the Actual start up Approval Time (ASAT), the time an aircraft receives its start up approval (milestone 14)."""
        raise NotImplementedError

    def confirmTSATToPilot(self, flight: Flight) -> None:
        """ATC confirms TSAT to the pilot in order to maintain the aircraft in the pre-departure sequence (milestone 13)."""
        raise NotImplementedError

    def refinePreDepartureSequence(self, flight: Flight) -> None:
        """ATC refines the pre-departure sequence once the pilot requests start up just before TSAT (milestone 12)."""
        raise NotImplementedError

    def resequenceFlight(self, flight: Flight) -> None:
        """If start-up approval is not granted at TSAT+tolerance, all partners are informed and the flight will be re-sequenced (milestone 14)."""
        raise NotImplementedError


@dataclass
class Message:
    """A message exchanged between stakeholders and systems in the Airport CDM process.

    Package Messages, stereotype boundary, milestones [1, 2, 3, 10, 11, 12, 15, 16].
    """
    sender: str | None = None
    recipient: str | None = None
    sentTime: datetime | None = None
    content: str | None = None


@dataclass
class AirborneMessage(Message):
    """The message generated when the aircraft becomes airborne.

    Package Messages, stereotype boundary, milestones [16].
    """
    takeOffTime: TakeOffTime | None = None


@dataclass
class Aircraft:
    """The physical aircraft that operates a flight, identified by registration and type.

    Package Flights, stereotype entity, milestones [1].
    """
    registration: str | None = None
    type: str | None = None


@dataclass
class TurnRoundOperator:
    """A joint role, referred to throughout the document as AO/GH, that manages the aircraft turn-round and provides TOBT-related updates to the Airport CDM process.

    Package Stakeholders, stereotype entity, milestones [1, 4, 5, 6, 7, 8, 9, 10, 12].

    Relationship: dependency 'provides TOBT' -> OffBlockTime
    """
    name: str | None = None

    def provideTOBT(self, flight: Flight, time: datetime) -> OffBlockTime:
        """AO/GH provides or inserts a TOBT value, as referenced across milestones 4-9."""
        raise NotImplementedError

    def updateTOBT(self, flight: Flight) -> None:
        """TOBT is updated automatically or inserted manually by the Aircraft Operator/Ground Handler, calculated on the basis of the defined or estimated turn-round period for the departing flight (milestones 6, 7, 8)."""
        raise NotImplementedError

    def confirmFinalTOBT(self, flight: Flight) -> OffBlockTime:
        """The time at which the AO/GH provide their most accurate TOBT taking into account the operational situation, at t minutes before EOBT (milestone 9)."""
        raise NotImplementedError

    def manageTurnRoundProcess(self, flight: Flight) -> None:
        """The AO/GH, in coordination with the aircrew, manages the turn-round process accordingly once TOBT/TSAT is stable (milestones 9, 10)."""
        raise NotImplementedError

    def recordActualCommenceGroundHandling(self, flight: Flight) -> GroundHandlingTime:
        """AO/GH provides the Actual Commence of Ground Handling time (ACGT) (milestone 8)."""
        raise NotImplementedError

    def recordAircraftReady(self, flight: Flight) -> ReadyTime:
        """AO/GH provides the Actual Ready Time (ARDT) when doors are closed and the aircraft is ready to taxi (milestone 12)."""
        raise NotImplementedError


@dataclass
class AircraftOperator(TurnRoundOperator):
    """The airline that submits the ATC Flight Plan and integrates its own strategy to compute the TOBT for a flight.

    Package Stakeholders, stereotype entity, milestones [1, 9].

    Relationship: dependency 'submits' -> FlightPlan
    """

    def submitATCFlightPlan(self, flightPlan: FlightPlan) -> None:
        """The ATC Flight Plan is submitted by the Aircraft Operator (milestone 1)."""
        raise NotImplementedError

    def integrateOwnStrategyForTOBT(self, flight: Flight) -> None:
        """Emphasis is put on the need for the Aircraft Operator to integrate his own strategy to compute a TOBT related to the flight (milestone 9)."""
        raise NotImplementedError


@dataclass
class Milestone:
    """One of the sixteen defined events of the Airport CDM process, each with its own trigger, timing rule, effect, and procedure.

    Package Milestones, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    milestoneNumber: int | None = None
    name: str | None = None
    definition: str | None = None
    trigger: str | None = None
    dataQualityAccuracy: str | None = None
    resultingStatus: FlightStatus | None = None

    def changeOperationalStatus(self, flight: Flight) -> None:
        """Sets the flight's status to the milestone's resultingStatus, as stated in each milestone's 'Operational Status (changes to)' field."""
        raise NotImplementedError


@dataclass
class AircraftReadyMilestone(Milestone):
    """Milestone 12: the time when all doors are closed, boarding bridge removed, push-back vehicle connected, ready to taxi upon TWR instructions (ARDT).

    Package Milestones, stereotype control, milestones [12].

    Relationship: association 'records' -> ReadyTime [1]
    """
    readyTolerance: timedelta | None = None

    def informPartnersOfARDT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of ARDT in the Airport CDM Platform and that the aircraft is ready for start-up/push-back."""
        raise NotImplementedError

    def checkReadyStatusReceived(self, flight: Flight) -> bool:
        """At TOBT+tolerance, checks and informs the AO/GH that TOBT has passed and the Airport CDM Platform has not yet received ARDT or Ready Status (RDY)."""
        raise NotImplementedError


@dataclass
class Airport:
    """An aerodrome involved in a flight, either as departure (including as an outstation) or destination, which may or may not be schedule-coordinated.

    Package Flights, stereotype entity, milestones [1, 3].

    Relationship: dependency 'provides ATOT' -> TakeOffTime
    """
    icaoCode: str | None = None
    coordinated: bool | None = None

    def provideActualTakeOffTime(self, flight: Flight) -> TakeOffTime:
        """The outstation (ADEP) provides ATOT to the Network Operations and Aircraft Operator (milestone 3)."""
        raise NotImplementedError


@dataclass
class AirportCDMPlatform:
    """The Airport CDM Platform that is initiated for each flight, processes all available flight information, and performs the ACISP actions defined for each milestone.

    Package Systems, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 16].

    Relationship: association 'processes' -> Flight [*]

    Relationship: dependency 'sends' -> Message

    Relationship: dependency 'performs the ACISP action for' -> Milestone
    """

    def initiatePlatformForFlight(self, flight: Flight) -> None:
        """The Airport CDM Platform is initiated for the flight and all available information is processed (milestone 1)."""
        raise NotImplementedError

    def updateArrivalEstimates(self, flight: Flight) -> None:
        """ELDT and EIBT updated for an arrival (milestone 1 ACISP action)."""
        raise NotImplementedError

    def updateDepartureEstimates(self, flight: Flight) -> None:
        """EOBT and ETOT updated for a departure (milestone 1 ACISP action)."""
        raise NotImplementedError

    def commenceDPIProcess(self, flight: Flight) -> None:
        """The DPI process commences the correct messaging with Network Operations, if implemented (milestone 1)."""
        raise NotImplementedError

    def updateETOTTTOTCTOT(self, flight: Flight) -> None:
        """ETOT/TTOT/CTOT updated (milestone 2 ACISP action)."""
        raise NotImplementedError

    def markAsRegulated(self, flight: Flight) -> None:
        """Marks appropriate fields as REGULATED for a flight that has received a CTOT (milestone 2 ACISP action)."""
        raise NotImplementedError

    def updateELDTEIBTTOBTTTOT(self, flight: Flight) -> None:
        """ELDT, EIBT, TOBT and TTOT updated (ACISP action common to milestones 3, 4 and 5)."""
        raise NotImplementedError

    def updateFromALDT(self, flight: Flight) -> None:
        """ELDT changes to ALDT; EIBT, TOBT and TTOT updated (milestone 6 ACISP action)."""
        raise NotImplementedError

    def updateFromAIBT(self, flight: Flight) -> None:
        """EIBT changes to AIBT; TOBT and TTOT updated (milestone 7 ACISP action)."""
        raise NotImplementedError

    def updateFromACGT(self, flight: Flight) -> None:
        """ETTT/TOBT, TTOT updated (milestone 8 ACISP action)."""
        raise NotImplementedError

    def recordTOBTConfirmation(self, flight: Flight) -> None:
        """Triggered by a new TOBT or TTOT update; no need to confirm an existing TOBT if it has been manually modified before (milestone 9 ACISP action)."""
        raise NotImplementedError

    def updateTTOTAfterTSAT(self, flight: Flight) -> None:
        """TTOT updated (milestone 10 ACISP action)."""
        raise NotImplementedError

    def recordAOBT(self, flight: Flight) -> None:
        """AOBT recorded (milestone 15 ACISP action)."""
        raise NotImplementedError

    def recordATOT(self, flight: Flight) -> None:
        """ATOT recorded (milestone 16 ACISP action)."""
        raise NotImplementedError


@dataclass
class AirportSlot:
    """The airport slot allocated to a flight under the airport slot programme, against which the ATC Flight Plan must be consistent.

    Package Flights, stereotype entity, milestones [1].

    Relationship: association 'at' -> Airport [1]
    """
    slotTime: datetime | None = None
    aerodrome: str | None = None


@dataclass
class AutomatedDockingSystem:
    """An automated docking system that can provide AIBT and AOBT.

    Package Systems, stereotype boundary, milestones [7, 15].

    Relationship: dependency 'reports movement events for' -> Flight
    """

    def detectInBlockOrOffBlock(self, flight: Flight) -> TimeQuantity:
        """Provides AIBT or AOBT for a flight via automated docking detection (milestones 7, 15)."""
        raise NotImplementedError


@dataclass
class BoardingStartsMilestone(Milestone):
    """Milestone 11: the gate is open for passengers to physically start boarding.

    Package Milestones, stereotype control, milestones [11].

    Relationship: association 'records' -> BoardingTime [1]
    """
    checkOffsetMinutes: timedelta | None = None

    def informPartnersOfASBT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of the Actual Start Boarding Time (ASBT) when it occurs."""
        raise NotImplementedError

    def checkBoardingStatus(self, flight: Flight) -> bool:
        """At a certain local-variable time before TOBT, checks whether boarding starts in time to respect TOBT, and informs AO/GH in case TOBT needs to be updated."""
        raise NotImplementedError


@dataclass
class TimeQuantity:
    """A time value describing a flight's progress, named by a prefix (Scheduled, Estimated, Target, Actual, Calculated) and an event, keeping every successive value with its originator and time of update.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    prefix: TimePrefix | None = None
    value: datetime | None = None
    originator: str | None = None
    accuracy: str | None = None
    recordedAt: datetime | None = None


@dataclass
class BoardingTime(TimeQuantity):
    """The Actual Start Boarding Time (ASBT), the time the gate opens for passengers to physically start boarding.

    Package Timings, stereotype entity, milestones [11].
    """
    pass


@dataclass
class DPIMessage(Message):
    """A Departure Planning Information message sent to Network Operations, of type E-DPI, T-DPI, T-DPI-t, T-DPI-s, or A-DPI.

    Package Messages, stereotype boundary, milestones [1, 2, 3, 10, 15].
    """
    dpiType: DPIMessageType | None = None
    sobt: str | None = None
    aircraftRegistration: str | None = None
    firstDestination: str | None = None


@dataclass
class EOBTMinus2HourMilestone(Milestone):
    """Milestone 2: at EOBT-2hr regulated flights receive a CTOT and Network Operations is informed of the updated take-off estimate.

    Package Milestones, stereotype control, milestones [2].

    Relationship: association 'records CTOT/TTOT for' -> TakeOffTime [1]
    """

    def checkFlightEstimatesConsistency(self, flight: Flight) -> bool:
        """Checks, before or after take-off from outstation, whether AO/GH flight estimates are consistent with the ATC Flight Plan, verifying feasibility at EOBT-2hrs."""
        raise NotImplementedError

    def sendTDPI(self, flight: Flight) -> DPIMessage:
        """Informs Network Operations at EOBT-2hrs about the updated take-off time estimate using a T-DPI message."""
        raise NotImplementedError

    def calculateTTOT(self, eibt: InBlockTime, mttt: MinimumTurnRoundTime, exot: TaxiTime, eobt: OffBlockTime, tobt: OffBlockTime) -> TakeOffTime:
        """Calculation basis for TTOT takes into account EIBT+MTTT+EXOT if later than EOBT+EXOT; if TOBT is manually input it overrides the EIBT+MTTT estimate, so TTOT equals TOBT+EXOT."""
        raise NotImplementedError

    def updateELDTFromFUM(self, flight: Flight, fum: FlightUpdateMessage) -> LandingTime:
        """For inbound flights, ELDT is updated based on information provided by FUM messages, taking into account the actual progress of the flight."""
        raise NotImplementedError


@dataclass
class ETFMS:
    """The Network Operations system used to monitor a flight's progress and send Flight Update Messages.

    Package Systems, stereotype boundary, milestones [2, 3].

    Relationship: dependency 'monitors progress of' -> Flight
    """

    def monitorFlightProgress(self, flight: Flight) -> None:
        """Network Operations monitors progress of the flight using the ETFMS when within 3hrs flying time of the destination airport (milestone 3)."""
        raise NotImplementedError

    def sendFUM(self, flight: Flight) -> FlightUpdateMessage:
        """Sends a Flight Update Message (FUM) that provides updates of the flight's progress (milestones 2, 3)."""
        raise NotImplementedError


@dataclass
class ElapsedTime(TimeQuantity):
    """The Estimated Elapsed Time given on the ATC Flight Plan, used with ATOT to calculate ELDT.

    Package Timings, stereotype entity, milestones [3].
    """
    pass


@dataclass
class FinalApproachMilestone(Milestone):
    """Milestone 5: the flight enters the Final Approach phase at the destination airport, updating ELDT and commencing the TOBT process.

    Package Milestones, stereotype control, milestones [5].

    Relationship: association 'records' -> LandingTime [1]
    """

    def commenceTOBTProcess(self, flight: Flight) -> None:
        """Commences the TOBT process and checks whether the AO/GH TOBT is consistent with the ATC Flight Plan."""
        raise NotImplementedError

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Verifies feasibility of the ATC Flight Plan given the updated TOBT."""
        raise NotImplementedError

    def notifyNetworkOperationsIfTTOTChange(self, flight: Flight) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class FinalTOBTConfirmationMilestone(Milestone):
    """Milestone 9: the time at which the AO/GH provide their most accurate TOBT taking into account the operational situation, t minutes before EOBT.

    Package Milestones, stereotype control, milestones [9].

    Relationship: association 'records' -> OffBlockTime [1]
    """
    confirmationOffsetMinutes: timedelta | None = None

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan."""
        raise NotImplementedError

    def notifyNetworkOperationsIfTTOTChange(self, flight: Flight) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError

    def confirmTOBT(self, flight: Flight) -> bool:
        """Performed at a predefined local-parameter time to confirm TOBT prior to TSAT issue and verify feasibility of the ATC Flight Plan estimates; no need to confirm an existing TOBT if it has been manually modified before."""
        raise NotImplementedError

    def introduceFlightIntoPreDepartureSequence(self, flight: Flight) -> None:
        """The flight is introduced into the pre-departure sequence once TOBT is confirmed."""
        raise NotImplementedError


@dataclass
class Flight:
    """A single arrival or departure operation of an aircraft, tracked through the sixteen milestones of the Airport CDM process.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'operated by' -> Aircraft [1]

    Relationship: association 'departs from' -> Airport [1]

    Relationship: association 'destined to' -> Airport [1]

    Relationship: association 'progresses through' -> Milestone [*]

    Relationship: aggregation 'records history of' -> OffBlockTime [0..*]

    Relationship: aggregation 'records history of' -> InBlockTime [0..*]

    Relationship: aggregation 'records history of' -> LandingTime [0..*]

    Relationship: aggregation 'records history of' -> TakeOffTime [0..*]

    Relationship: aggregation 'records history of' -> StartUpApprovalTime [0..*]

    Relationship: aggregation 'records history of' -> TaxiTime [0..*]

    Relationship: aggregation 'records history of' -> MinimumTurnRoundTime [0..*]

    Relationship: aggregation 'records history of' -> GroundHandlingTime [0..*]

    Relationship: aggregation 'records history of' -> BoardingTime [0..*]

    Relationship: aggregation 'records history of' -> ReadyTime [0..*]

    Relationship: aggregation 'records history of' -> StartUpRequestTime [0..*]

    Relationship: aggregation 'records history of' -> ElapsedTime [0..*]
    """
    aircraftRegistration: str | None = None
    aircraftType: str | None = None
    direction: FlightDirection | None = None
    status: FlightStatus | None = None
    regulated: bool | None = None


@dataclass
class FlightPlan:
    """The ICAO ATC Flight Plan submitted for a flight, possibly a repetitive flight plan (RFPL) covering daily or weekly flights.

    Package Flights, stereotype entity, milestones [1].

    Relationship: association 'describes' -> Flight [1]

    Relationship: association 'corresponds to' -> AirportSlot [0..1]
    """
    repetitive: bool | None = None
    submissionTime: datetime | None = None
    departureAerodrome: str | None = None
    destinationAerodrome: str | None = None


@dataclass
class FlightPlanActivatedMilestone(Milestone):
    """Milestone 1: the ICAO flight plan is submitted to ATC and the Airport CDM Platform is initiated for the flight.

    Package Milestones, stereotype control, milestones [1].
    """

    def checkConsistency(self, flightPlan: FlightPlan, airportSlot: AirportSlot, flight: Flight) -> bool:
        """Checks consistency between the ATC Flight Plan, Airport Slot and Airport flight data before the first E-DPI is sent."""
        raise NotImplementedError

    def confirmFlightToNetworkOperations(self, flight: Flight) -> None:
        """Confirms the flight to Network Operations and allows further local processing of the flight."""
        raise NotImplementedError

    def sendFirstEDPI(self, flight: Flight) -> DPIMessage:
        """Sends the first E-DPI with consistent SOBT, aircraft registration and first destination data; not sent if information is missing or inconsistent, triggered by first activation of the flight plan (earliest EOBT-3hr) or new/late submissions after cancellation or revised EOBT."""
        raise NotImplementedError

    def checkFlightReadyDeadline(self, flight: Flight) -> bool:
        """Checks that the flight is ready not later than 15 minutes after the planned EOBT."""
        raise NotImplementedError


@dataclass
class FlightStatusAdvisoryMessage(Message):
    """An FSA message sent at take-off advising of the flight's status.

    Package Messages, stereotype boundary, milestones [16].
    """
    status: FlightStatus | None = None


@dataclass
class FlightUpdateMessage(Message):
    """A Flight Update Message (FUM) sent by Network Operations providing updates of a flight's progress.

    Package Messages, stereotype boundary, milestones [2, 3].
    """
    updatedELDT: LandingTime | None = None


@dataclass
class GroundHandler(TurnRoundOperator):
    """The ground handling organisation that carries out turn-round operations for a flight, jointly referred to with the Aircraft Operator as AO/GH.

    Package Stakeholders, stereotype entity, milestones [1, 8, 12].
    """
    pass


@dataclass
class GroundHandlingStartedMilestone(Milestone):
    """Milestone 8: commencement of ground handling operations (ACGT) triggers an update of downstream estimates, specific to first-of-day or long-parked flights.

    Package Milestones, stereotype control, milestones [8].

    Relationship: association 'records' -> GroundHandlingTime [1]
    """

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan, verifying feasibility given the updated TOBT or ATC Flight Plan."""
        raise NotImplementedError

    def notifyNetworkOperationsIfTTOTChange(self, flight: Flight) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError

    def updateTOBT(self, flight: Flight) -> None:
        """TOBT is updated automatically or inserted manually by the AO/GH, calculated on the basis of the estimated turn-round period for the departing flight."""
        raise NotImplementedError


@dataclass
class GroundHandlingTime(TimeQuantity):
    """The Actual Commence of Ground Handling time (ACGT), specific to flights that are the first operation of the day or have been long-term parked.

    Package Timings, stereotype entity, milestones [7, 8].
    """
    pass


@dataclass
class IFPS:
    """The system/organisation that distributes the submitted ATC Flight Plan to all involved ATC units.

    Package Stakeholders, stereotype entity, milestones [1].

    Relationship: dependency 'distributes' -> FlightPlan

    Relationship: dependency 'distributes flight plan to' -> AirTrafficControl
    """

    def distributeFlightPlan(self, flightPlan: FlightPlan) -> None:
        """The ATC Flight Plan is distributed by the IFPS so that all involved ATC units, including departure and destination aerodromes, receive it (milestone 1)."""
        raise NotImplementedError


@dataclass
class InBlockMilestone(Milestone):
    """Milestone 7: AIBT, the actual in-block time, triggers an update of downstream estimates.

    Package Milestones, stereotype control, milestones [7].

    Relationship: association 'records' -> InBlockTime [1]
    """

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan, verifying feasibility given the updated TOBT or ATC Flight Plan."""
        raise NotImplementedError

    def notifyNetworkOperationsIfTTOTChange(self, flight: Flight) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError

    def updateTOBTAndTTOT(self, flight: Flight) -> None:
        """TOBT and TTOT are updated automatically or inserted manually by the AO/GH, calculated on the basis of the estimated turn-round period for the departing flight."""
        raise NotImplementedError


@dataclass
class InBlockTime(TimeQuantity):
    """The in-block time quantity of a flight, covering EIBT and AIBT values distinguished by prefix.

    Package Timings, stereotype entity, milestones [1, 2, 4, 5, 6, 7].
    """
    pass


@dataclass
class LandedMilestone(Milestone):
    """Milestone 6: ALDT, the actual landing time, triggers an update of downstream estimates.

    Package Milestones, stereotype control, milestones [6].

    Relationship: association 'records' -> LandingTime [1]
    """

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan, verifying feasibility given the updated TOBT or ATC Flight Plan."""
        raise NotImplementedError

    def notifyNetworkOperationsIfTTOTChange(self, flight: Flight) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError

    def updateTOBTAndTTOT(self, flight: Flight) -> None:
        """TOBT and TTOT are updated automatically or inserted manually by the AO/GH, calculated on the basis of the defined turn-round period for the departing flight."""
        raise NotImplementedError

    def calculateEIBT(self, aldt: LandingTime, exit: TaxiTime) -> InBlockTime:
        """The EIBT can be updated according to the ALDT+EXIT."""
        raise NotImplementedError


@dataclass
class LandingTime(TimeQuantity):
    """The landing time quantity of a flight, covering ELDT and ALDT values distinguished by prefix.

    Package Timings, stereotype entity, milestones [1, 3, 4, 5, 6].
    """
    pass


@dataclass
class LocalRadarUpdateMilestone(Milestone):
    """Milestone 4: the flight enters the FIR or local airspace of the destination airport, updating ELDT and commencing the TOBT process.

    Package Milestones, stereotype control, milestones [4].

    Relationship: association 'records' -> LandingTime [1]
    """
    standGateChangeCutoff: timedelta | None = None

    def commenceTOBTProcess(self, flight: Flight) -> None:
        """Commences the TOBT process and checks whether the AO/GH TOBT is consistent with the ATC Flight Plan."""
        raise NotImplementedError

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Verifies feasibility of the ATC Flight Plan given the updated TOBT."""
        raise NotImplementedError

    def notifyNetworkOperationsIfTTOTChange(self, flight: Flight) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError

    def calculateEIBT(self, eldt: LandingTime, exit: TaxiTime) -> InBlockTime:
        """An estimated in-block time (EIBT) is computed using the ELDT and the estimated taxi-in time."""
        raise NotImplementedError

    def checkStandGateChangeAllowed(self, eldt: LandingTime, currentTime: datetime) -> bool:
        """Checks that any change to a stand or gate is not made after ELDT-30 minutes, taking into account the taxi-in time (EXIT)."""
        raise NotImplementedError


@dataclass
class MinimumTurnRoundTime(TimeQuantity):
    """The minimum/estimated turn-round time (MTTT) used to calculate downstream TOBT and TTOT for a departing flight.

    Package Timings, stereotype entity, milestones [2, 3, 6, 7, 8].
    """
    pass


@dataclass
class MovementMessage(Message):
    """An MVT message sent at take-off reporting the aircraft's movement.

    Package Messages, stereotype boundary, milestones [16].
    """
    eventType: str | None = None


@dataclass
class NetworkOperations:
    """The network management function that issues CTOT for regulated flights, monitors flight progress, and receives DPI messages from the Airport CDM Platform.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 15].

    Relationship: association 'issues CTOT for' -> Flight [*]

    Relationship: dependency 'issues CTOT' -> TakeOffTime

    Relationship: dependency 'sends' -> FlightUpdateMessage
    """

    def issueCTOT(self, flight: Flight) -> TakeOffTime:
        """The CTOT is issued by Network Operations and sent to relevant ATS units and the departure aerodrome, at EOBT-2h if the flight is regulated (milestone 2)."""
        raise NotImplementedError


@dataclass
class OffBlockMilestone(Milestone):
    """Milestone 15: AOBT, the actual time the aircraft pushes back/vacates the parking position.

    Package Milestones, stereotype control, milestones [15].

    Relationship: association 'records' -> OffBlockTime [1]
    """

    def informPartnersOfAOBT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of AOBT in the Airport CDM Platform and that the aircraft has commenced push-back/taxi from the parking position."""
        raise NotImplementedError

    def sendADPI(self, flight: Flight) -> DPIMessage:
        """AOBT always triggers an A-DPI message to Network Operations, or in the case of remote holding at a defined time prior to TTOT."""
        raise NotImplementedError

    def checkTTOTChangeAndNotify(self, flight: Flight) -> None:
        """After the first A-DPI is sent, checks TTOT updates against the TTOT tolerance before Network Operations is informed, with a new A-DPI, of the updated TTOT."""
        raise NotImplementedError


@dataclass
class OffBlockTime(TimeQuantity):
    """The off-block time quantity of a flight, covering SOBT, EOBT, TOBT and AOBT values distinguished by prefix.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 15].
    """
    pass


@dataclass
class Pilot:
    """The aircrew member who requests start-up approval from ATC ahead of TSAT.

    Package Stakeholders, stereotype entity, milestones [12, 13].

    Relationship: association 'requests start-up from' -> AirTrafficControl [1]
    """

    def requestStartUp(self, flight: Flight) -> None:
        """The pilot requests start up just before TSAT, following coordination with the Ground Handler (milestone 12), triggering ATC's start-up request handling (milestone 13)."""
        raise NotImplementedError


@dataclass
class ReadyStatusMessage(Message):
    """A Ready Status (RDY) message indicating the aircraft is ready for start-up/push-back.

    Package Messages, stereotype boundary, milestones [12].
    """
    ready: bool | None = None


@dataclass
class ReadyTime(TimeQuantity):
    """The Actual Ready Time (ARDT), the time all doors are closed and the aircraft is ready to taxi upon TWR instruction.

    Package Timings, stereotype entity, milestones [12].
    """
    pass


@dataclass
class StartUpApprovalTime(TimeQuantity):
    """The start-up approval time quantity of a flight, covering TSAT and ASAT values distinguished by prefix.

    Package Timings, stereotype entity, milestones [9, 10, 13, 14].
    """
    pass


@dataclass
class StartUpApprovedMilestone(Milestone):
    """Milestone 14: ASAT, the actual time an aircraft receives its start-up approval.

    Package Milestones, stereotype control, milestones [14].

    Relationship: association 'records' -> StartUpApprovalTime [1]
    """
    startUpTolerance: timedelta | None = None

    def informPartnersOfASAT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of ASAT in the Airport CDM Platform and that the aircraft has received start-up approval/push-back clearance."""
        raise NotImplementedError

    def checkASATAgainstTSAT(self, flight: Flight) -> bool:
        """Checks if ASAT is in accordance with TSAT and alerts all relevant Airport CDM Partners when no start-up has been granted at TSAT+tolerance; the flight will be re-sequenced."""
        raise NotImplementedError


@dataclass
class StartUpRequestTime(TimeQuantity):
    """The Actual Start-up Request Time (ASRT), the time start-up is requested.

    Package Timings, stereotype entity, milestones [13].
    """
    pass


@dataclass
class StartUpRequestedMilestone(Milestone):
    """Milestone 13: the time that start-up is requested (ASRT), based on pilot request to ATC.

    Package Milestones, stereotype control, milestones [13].

    Relationship: association 'records' -> StartUpRequestTime [1]
    """
    tsatTolerance: timedelta | None = None

    def informPartnersOfASRT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of the Actual Start-up Request Time (ASRT) in the Airport CDM Platform when it occurs."""
        raise NotImplementedError

    def alertIfNoStartUpRequested(self, flight: Flight) -> None:
        """If the start-up request is not made by TSAT+tolerance, alerts all relevant Airport CDM Partners and informs the AO/GH that no start-up has been requested and TOBT should be updated."""
        raise NotImplementedError


@dataclass
class TSATIssuedMilestone(Milestone):
    """Milestone 10: the time ATC issues the Target Start Up Approval Time.

    Package Milestones, stereotype control, milestones [10].

    Relationship: association 'records' -> StartUpApprovalTime [1]
    """
    issueOffsetMinutes: timedelta | None = None

    def informPartnersOfTSAT(self, flight: Flight) -> None:
        """Informs all relevant partners of the TSAT that has been allocated to the flight; no check is performed for this step."""
        raise NotImplementedError

    def sendTDPIs(self, flight: Flight) -> DPIMessage:
        """Network Operations is informed by a T-DPI-s for non-regulated flights."""
        raise NotImplementedError

    def checkTOBTUpdateCount(self, flight: Flight) -> bool:
        """Checks whether the number of TOBT updates after TSAT has been issued exceeds a locally defined tolerance; if exceeded, the TOBT input is processed according to local procedure."""
        raise NotImplementedError


@dataclass
class TakeOffFromOutstationMilestone(Milestone):
    """Milestone 3: the ATOT from the outstation (ADEP) is recorded and used to update landing and take-off estimates.

    Package Milestones, stereotype control, milestones [3].

    Relationship: association 'records' -> TakeOffTime [1]
    """
    ttotTolerance: timedelta | None = None

    def checkLandingEstimateConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH estimated landing time after take-off from outstation is consistent with the outbound ATC Flight Plan."""
        raise NotImplementedError

    def sendTDPIt(self, flight: Flight) -> DPIMessage:
        """Informs Network Operations about the updated take-off time estimates using a T-DPI-t message, respecting the 5-minute TTOT tolerance."""
        raise NotImplementedError

    def calculateTTOT(self, eibt: InBlockTime, mttt: MinimumTurnRoundTime, exot: TaxiTime, eobt: OffBlockTime, tobt: OffBlockTime) -> TakeOffTime:
        """TTOT takes into account EIBT+MTTT+EXOT; if EOBT is later than EIBT+MTTT, TTOT equals EOBT+EXOT; if TOBT is available it overrules the EIBT+MTTT estimate, so TTOT equals TOBT+EXOT."""
        raise NotImplementedError

    def calculateELDT(self, atot: TakeOffTime, elapsedTime: ElapsedTime) -> LandingTime:
        """If the departure airport is more than 3hrs flying time from the destination, ELDT is calculated using the ATOT and the Estimated Elapsed Time on the FPL."""
        raise NotImplementedError


@dataclass
class TakeOffMilestone(Milestone):
    """Milestone 16: ATOT, the actual time the aircraft takes off from the runway.

    Package Milestones, stereotype control, milestones [16].

    Relationship: association 'records' -> TakeOffTime [1]
    """

    def informPartnersOfATOT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners about the actual take-off."""
        raise NotImplementedError

    def generateAirborneMessage(self, flight: Flight) -> AirborneMessage:
        """An airborne message is generated, triggered by Tower FDPS, A-SMGCS/Radar detection or ACARS."""
        raise NotImplementedError

    def removeFromDepartureSequence(self, flight: Flight) -> None:
        """The flight is removed from the departure sequence."""
        raise NotImplementedError

    def sendFSAAndMVT(self, flight: Flight) -> None:
        """FSA and MVT messages are sent."""
        raise NotImplementedError


@dataclass
class TakeOffTime(TimeQuantity):
    """The take-off time quantity of a flight, covering ETOT, TTOT, CTOT and ATOT values distinguished by prefix.

    Package Timings, stereotype entity, milestones [1, 2, 3, 15, 16].
    """
    pass


@dataclass
class TaxiTime(TimeQuantity):
    """An estimated taxi time quantity of a flight, covering EXOT (taxi-out) and EXIT (taxi-in), distinguished by direction.

    Package Timings, stereotype entity, milestones [2, 3, 4, 6, 9].
    """
    direction: TaxiDirection | None = None


@dataclass
class TurnRound:
    """An aircraft turn-round normally comprising a related arriving and departing flight pair.

    Package Flights, stereotype entity, milestones [1].

    Relationship: aggregation 'arrival flight' -> Flight [0..1]

    Relationship: aggregation 'departure flight' -> Flight [0..1]

    Relationship: composition 'has' -> MinimumTurnRoundTime [0..1]
    """
    turnRoundId: str | None = None
