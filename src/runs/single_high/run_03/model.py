"""Class stubs rendered from runs/single_high/run_03/model.json by src/generate/render_code.py; do not edit by hand."""
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


class FlightDirection(Enum):
    ARRIVAL = "ARRIVAL"
    DEPARTURE = "DEPARTURE"


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


class MovementMessageType(Enum):
    FSA = "FSA"
    MVT = "MVT"


class TimePrefix(Enum):
    SCHEDULED = "Scheduled"
    ESTIMATED = "Estimated"
    TARGET = "Target"
    ACTUAL = "Actual"
    CALCULATED = "Calculated"


@dataclass
class ACARS:
    """The aircraft communications addressing and reporting system that reports ON/OFF/IN/OUT times from equipped aircraft.

    Package Systems, stereotype boundary, milestones [6, 7, 8, 15, 16].

    Relationship: dependency 'reports times for' -> Flight
    """

    def reportTime(self, flight: Flight, eventType: str, time: datetime) -> None:
        """ACARS equipped aircraft report times such as landing (ALDT, ACARS=ON), in-block (AIBT, ACARS=IN), off-block (AOBT, ACARS=OUT), and take-off (ATOT, ACARS=OFF)."""
        raise NotImplementedError


@dataclass
class ATCSystem:
    """The ATC/radar system (including A-SMGCS, Tower FDPS, and radar) that detects the flight and provides its actual times.

    Package Systems, stereotype boundary, milestones [3, 4, 5, 6, 9, 16].

    Relationship: dependency 'detects/reports times for' -> Flight

    Relationship: dependency 'calculates' -> TaxiOutTime
    """

    def detectFlight(self, flight: Flight) -> None:
        """The radar system detects a flight based upon the assigned SSR code when it crosses a defined FIR/ATC boundary, range/position, or level (milestones 4,5)."""
        raise NotImplementedError

    def provideAtot(self, flight: Flight, time: datetime) -> None:
        """Provides ATOT after take off from outstation (milestone 3)."""
        raise NotImplementedError

    def provideAldt(self, flight: Flight, time: datetime) -> None:
        """Provides ALDT, the time an aircraft touches down (milestone 6)."""
        raise NotImplementedError

    def calculateExot(self, flight: Flight) -> timedelta:
        """Following receipt of TOBT, calculates and provides the Estimated Taxi-Out Time (EXOT) based on predicted traffic load, gate/stand location, runway in use, and waiting period at the Holding Position (milestone 9)."""
        raise NotImplementedError

    def detectTakeOff(self, flight: Flight) -> None:
        """Detects take off, triggered by Tower FDPS, A-SMGCS/Radar detection or ACARS (milestone 16)."""
        raise NotImplementedError


@dataclass
class ATCUnit:
    """The air traffic control unit(s), including the departure aerodrome's ATC, that receive the ATC Flight Plan and issue TSAT and start-up approval.

    Package Stakeholders, stereotype entity, milestones [1, 9, 10, 13, 14].

    Relationship: association 'receives' -> AtcFlightPlan [*]
    """
    unitName: str | None = None

    def receiveFlightPlan(self, flightPlan: AtcFlightPlan) -> None:
        """All involved ATC units receive the flight plan, including departure and destination aerodromes (milestone 1)."""
        raise NotImplementedError


@dataclass
class Aircraft:
    """The physical aircraft that operates a flight, identified by registration and type.

    Package Flights, stereotype entity, milestones [1, 4].
    """
    registration: str | None = None
    type: str | None = None

    def updateType(self, newType: str) -> None:
        """The flight plan may be used to update certain information such as type of aircraft (milestone 1)."""
        raise NotImplementedError


@dataclass
class GroundOperationsPartner:
    """The Aircraft Operator or Ground Handler, referred to jointly as AO/GH, who manages the turn-round process and provides the flight's operational time estimates.

    Package Stakeholders, stereotype entity, milestones [1, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15].

    Relationship: association 'manages turn-round for' -> Flight [*]

    Relationship: association 'provides manual input to' -> AirportCDMPlatform [1]
    """
    partnerId: str | None = None

    def provideTobt(self, flight: Flight, tobt: datetime) -> None:
        """AO/GH provide TOBT, updated automatically or inserted manually, calculated on the basis of the defined/estimated turn-round period for the departing flight (milestones 4,6,7,8)."""
        raise NotImplementedError

    def confirmFinalTobt(self, flight: Flight) -> None:
        """AO/GH provide their most accurate TOBT, taking into account the operational situation, t minutes before EOBT (milestone 9)."""
        raise NotImplementedError

    def manageTurnRound(self, flight: Flight) -> None:
        """AO/GH, in coordination with the aircrew, manage the turn-round process accordingly once TOBT/TSAT is established (milestones 9,10)."""
        raise NotImplementedError

    def provideReadyStatus(self, flight: Flight, time: datetime) -> None:
        """AO/GH provide Actual Ready Time (ARDT) confirming that all doors are closed, boarding bridge removed, push back vehicle connected, ready to taxi (milestone 12)."""
        raise NotImplementedError


@dataclass
class AircraftOperator(GroundOperationsPartner):
    """The airline that operates the flight and submits the ATC Flight Plan.

    Package Stakeholders, stereotype entity, milestones [1, 4, 6, 7, 8, 9].

    Relationship: dependency 'submits' -> AtcFlightPlan
    """

    def submitAtcFlightPlan(self, flightPlan: AtcFlightPlan) -> None:
        """The ATC Flight Plan is submitted by the Aircraft Operator and distributed by the IFPS (milestone 1)."""
        raise NotImplementedError


@dataclass
class Milestone:
    """An abstract CDM process event with its trigger, timing rule, effect, procedure, and the flight status it produces.

    Package Milestones, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'applies to' -> Flight [1]
    """
    milestoneName: str | None = None
    definition: str | None = None
    trigger: str | None = None
    timingRule: str | None = None
    effect: str | None = None
    newStatus: FlightStatus | None = None

    def applyStatusChange(self, flight: Flight) -> None:
        """Changes the flight's operational status to newStatus on occurrence of this milestone."""
        raise NotImplementedError


@dataclass
class AircraftReady(Milestone):
    """Milestone 12: the time when all doors are closed, boarding bridge removed, push back vehicle connected, ready to taxi (ARDT).

    Package Milestones, stereotype control, milestones [12].
    """

    def informPartnersOfArdt(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of Actual Ready Time (ARDT) or Ready Status (RDY) that the aircraft is ready for start up/push-back."""
        raise NotImplementedError

    def checkReadyStatusReceived(self, flight: Flight) -> bool:
        """At TOBT + tolerance, checks whether ARDT or Ready Status has been received and informs the AO/GH if TOBT has passed without it."""
        raise NotImplementedError

    def refinePreDepartureSequence(self, flight: Flight) -> None:
        """ATC refines the pre-departure sequence once the aircraft is ready."""
        raise NotImplementedError


@dataclass
class AirportCDMPlatform:
    """The Airport CDM Platform that is initiated per flight, processes all available flight information, and performs the CDM actions recorded at each milestone.

    Package Systems, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 16].

    Relationship: association 'holds data for' -> Flight [*]

    Relationship: dependency 'sends' -> DpiMessage

    Relationship: dependency 'generates' -> MovementMessage
    """
    platformId: str | None = None

    def initiatePlatform(self, flight: Flight) -> None:
        """The Airport CDM Platform is initiated for this flight, and all available information is processed (milestone 1)."""
        raise NotImplementedError

    def updateArrivalEstimates(self, flight: Flight) -> None:
        """ELDT and EIBT updated for an arrival (milestone 1)."""
        raise NotImplementedError

    def updateDepartureEstimates(self, flight: Flight) -> None:
        """EOBT and ETOT updated for a departure (milestone 1)."""
        raise NotImplementedError

    def commenceDpiProcess(self, flight: Flight) -> None:
        """The DPI process commences with Network Operations, if implemented (milestone 1)."""
        raise NotImplementedError

    def updateEtotTtotCtot(self, flight: Flight) -> None:
        """ETOT/TTOT/CTOT updated (milestone 2)."""
        raise NotImplementedError

    def markRegulated(self, flight: Flight) -> None:
        """Marks appropriate fields as REGULATED (milestone 2)."""
        raise NotImplementedError

    def updateEldtEibtTobtTtot(self, flight: Flight) -> None:
        """ELDT, EIBT, TOBT and TTOT updated (milestones 3,4,5)."""
        raise NotImplementedError

    def updateAldtEibtTobtTtot(self, flight: Flight) -> None:
        """ELDT changes to ALDT, EIBT, TOBT and TTOT updated (milestone 6)."""
        raise NotImplementedError

    def updateAibtTobtTtot(self, flight: Flight) -> None:
        """EIBT changes to AIBT, TOBT and TTOT updated (milestone 7)."""
        raise NotImplementedError

    def updateEtttTobtTtot(self, flight: Flight) -> None:
        """ETTT/TOBT, TTOT updated (milestone 8)."""
        raise NotImplementedError

    def evaluateTobtConfirmationNeeded(self, flight: Flight) -> bool:
        """Triggered by a new TOBT or TTOT update; no need to confirm an existing TOBT if it has been manually modified before (milestone 9)."""
        raise NotImplementedError

    def addToPreDepartureSequence(self, flight: Flight) -> None:
        """The flight is introduced into the pre-departure sequence following receipt of TOBT (milestone 9)."""
        raise NotImplementedError

    def updateTtot(self, flight: Flight) -> None:
        """TTOT updated (milestone 10)."""
        raise NotImplementedError

    def stabiliseInPreDepartureSequence(self, flight: Flight) -> None:
        """The flight is stabilised into the pre-departure sequence once TSAT is issued (milestone 10)."""
        raise NotImplementedError

    def recordAobt(self, flight: Flight, time: datetime) -> None:
        """AOBT recorded (milestone 15)."""
        raise NotImplementedError

    def recordAtot(self, flight: Flight, time: datetime) -> None:
        """ATOT recorded (milestone 16)."""
        raise NotImplementedError


@dataclass
class AirportFlightData:
    """The airport's own flight data record, checked for consistency with the ATC Flight Plan and Airport Slot, and used to initiate the outbound flight at non-coordinated airports.

    Package Flights, stereotype entity, milestones [1].
    """
    dataReference: str | None = None


@dataclass
class AirportSlot:
    """The airport slot programme entry that the ATC Flight Plan must correspond to.

    Package Flights, stereotype entity, milestones [1].
    """
    slotProgrammeReference: str | None = None
    scheduledTime: datetime | None = None


@dataclass
class AtcFlightPlan:
    """The ICAO flight plan submitted to ATC for a flight, distributed by the IFPS to involved ATC units.

    Package Flights, stereotype entity, milestones [1].

    Relationship: dependency 'corresponds to' -> AirportSlot

    Relationship: dependency 'checked for consistency with' -> AirportFlightData
    """
    sobt: datetime | None = None
    departureAerodrome: str | None = None
    destinationAerodrome: str | None = None
    aircraftRegistration: str | None = None
    isRepetitive: bool | None = None


@dataclass
class BoardingStarts(Milestone):
    """Milestone 11: the gate is open for passengers to physically start boarding.

    Package Milestones, stereotype control, milestones [11].
    """

    def informPartnersOfAsbt(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of Actual Start Boarding Time (ASBT) when it occurs."""
        raise NotImplementedError

    def checkBoardingStatus(self, flight: Flight) -> bool:
        """At a locally defined time before TOBT, checks whether boarding starts in time to respect TOBT and informs the AO/GH in case TOBT needs to be updated."""
        raise NotImplementedError


@dataclass
class TimeQuantity:
    """An abstract time quantity describing a flight's progress, whose successive scheduled, estimated, target, actual, or calculated values are all kept rather than overwritten.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: composition 'records' -> TimeValue [1..*]
    """
    values: TimeValue | None = None

    def appendValue(self, prefix: TimePrefix, dateTime: datetime, originator: str) -> None:
        """Records a new value of this time quantity with its originator and time of update; an update appends rather than overwrites."""
        raise NotImplementedError


@dataclass
class BoardingTime(TimeQuantity):
    """The Actual Start Boarding Time (ASBT), when the gate opens for passengers to physically start boarding.

    Package Timings, stereotype entity, milestones [11].
    """
    boardingCheckOffset: timedelta | None = None


@dataclass
class DpiMessage:
    """A Departure Planning Information message sent by the Airport CDM Platform to Network Operations at various milestones.

    Package Messages, stereotype boundary, milestones [1, 2, 3, 10, 15].
    """
    type: DpiType | None = None
    sender: str | None = None
    ttotValue: datetime | None = None
    timestamp: datetime | None = None


@dataclass
class ETFMS:
    """The system Network Operations uses to monitor the progress of a flight and generate Flight Update Messages.

    Package Systems, stereotype boundary, milestones [3].

    Relationship: association 'used by' -> NetworkOperations [1]
    """

    def provideFlightUpdate(self, flight: Flight) -> FlightUpdateMessage:
        """Network Operations monitors progress of the flight using the ETFMS and sends a Flight Update Message (FUM) that provides updates of the flight's progress, when within 3hrs flying time of destination."""
        raise NotImplementedError


@dataclass
class FinalApproach(Milestone):
    """Milestone 5: the flight enters the Final Approach phase at the destination airport, typically 2 to 5 minutes from landing.

    Package Milestones, stereotype control, milestones [5].
    """

    def commenceTobtProcess(self, flight: Flight) -> None:
        """Commences the TOBT process on detection of the flight on Final Approach."""
        raise NotImplementedError

    def checkTobtConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT."""
        raise NotImplementedError

    def informNetworkOperationsIfTtotExceedsTolerance(self, flight: Flight) -> DpiMessage:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class FinalTobtConfirmation(Milestone):
    """Milestone 9: the time at which the AO/GH provide their most accurate TOBT, t minutes before EOBT.

    Package Milestones, stereotype control, milestones [9].
    """

    def checkTobtConsistency(self, flight: Flight) -> bool:
        """Performed at a predefined local time (t minutes before EOBT) to confirm TOBT prior to TSAT issue and verify feasibility of the ATC Flight Plan estimates."""
        raise NotImplementedError

    def informNetworkOperationsIfTtotExceedsTolerance(self, flight: Flight) -> DpiMessage:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class Flight:
    """An arriving or departing flight leg of a turn-round, tracked through the milestones with its operational status and time quantities.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'described by' -> AtcFlightPlan [1]

    Relationship: association 'has' -> AirportFlightData [1]

    Relationship: association 'operates' -> Aircraft [1]

    Relationship: composition 'has' -> OffBlockTime [1]

    Relationship: composition 'has' -> InBlockTime [1]

    Relationship: composition 'has' -> LandingTime [1]

    Relationship: composition 'has' -> TakeOffTime [1]

    Relationship: composition 'has' -> TaxiOutTime [1]

    Relationship: composition 'has' -> TaxiInTime [1]

    Relationship: composition 'has' -> TurnroundTime [1]

    Relationship: composition 'has' -> GroundHandlingTime [1]

    Relationship: composition 'has' -> BoardingTime [1]

    Relationship: composition 'has' -> ReadyTime [1]

    Relationship: composition 'has' -> StartUpRequestTime [1]

    Relationship: composition 'has' -> StartUpApprovalTime [1]
    """
    flightId: str | None = None
    direction: FlightDirection | None = None
    status: FlightStatus | None = None
    regulated: bool | None = None
    offBlockTime: OffBlockTime | None = None
    inBlockTime: InBlockTime | None = None
    landingTime: LandingTime | None = None
    takeOffTime: TakeOffTime | None = None
    taxiOutTime: TaxiOutTime | None = None
    taxiInTime: TaxiInTime | None = None
    turnroundTimeEstimate: TurnroundTime | None = None
    groundHandlingTime: GroundHandlingTime | None = None
    boardingTime: BoardingTime | None = None
    readyTime: ReadyTime | None = None
    startUpRequestTime: StartUpRequestTime | None = None
    startUpApprovalTime: StartUpApprovalTime | None = None


@dataclass
class FlightCrew:
    """The pilot and aircrew who request start-up and operate the aircraft during the turn-round.

    Package Stakeholders, stereotype entity, milestones [12, 14].

    Relationship: association 'operates' -> Flight [1]
    """

    def requestStartUp(self, flight: Flight) -> None:
        """The pilot requests start up just before TSAT, following coordination with the Ground Handler, by voice or DCL (milestones 12,14)."""
        raise NotImplementedError


@dataclass
class FlightPlanActivated(Milestone):
    """Milestone 1: the ICAO flight plan is submitted to ATC and the Airport CDM Platform is initiated for the flight.

    Package Milestones, stereotype control, milestones [1].

    Relationship: dependency 'checks consistency of' -> AtcFlightPlan

    Relationship: dependency 'checks consistency of' -> AirportSlot

    Relationship: dependency 'checks consistency of' -> AirportFlightData

    Relationship: dependency 'sends' -> DpiMessage
    """

    def checkFlightPlanConsistency(self, flight: Flight, flightPlan: AtcFlightPlan, slot: AirportSlot, airportData: AirportFlightData) -> bool:
        """Checks consistency between the ATC Flight Plan, Airport Slot, and Airport flight data before the first E-DPI is sent."""
        raise NotImplementedError

    def confirmFlightToNetworkOperations(self, flight: Flight) -> None:
        """Confirms the flight to Network Operations and allows further local processing of the flight."""
        raise NotImplementedError

    def sendFirstEdpi(self, flight: Flight) -> DpiMessage:
        """Sends the first E-DPI message with consistent SOBT, aircraft registration and first destination data once the AO has provided correct information; the E-DPI should not be sent if no or inconsistent information is provided. Triggered by first activation of the ATC Flight Plan (earliest EOBT-3hr), or new/late submissions after cancellation or revised EOBT."""
        raise NotImplementedError


@dataclass
class FlightUpdateMessage:
    """The Flight Update Message (FUM) sent by Network Operations via the ETFMS to provide updates of a flight's progress.

    Package Messages, stereotype boundary, milestones [2, 3].
    """
    eldtValue: datetime | None = None
    timestamp: datetime | None = None
    sender: str | None = None


@dataclass
class GroundHandler(GroundOperationsPartner):
    """The party that performs ground handling operations for the flight, jointly with the Aircraft Operator referred to as AO/GH.

    Package Stakeholders, stereotype entity, milestones [4, 6, 7, 8, 9].
    """
    pass


@dataclass
class GroundHandlingStarted(Milestone):
    """Milestone 8: ACGT, the commencement of ground handling operations, specific to first-of-day or long-parked flights.

    Package Milestones, stereotype control, milestones [8].
    """

    def checkTobtConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT or ATC Flight Plan, triggered by Actual Commence of Ground Handling (ACGT)."""
        raise NotImplementedError

    def informNetworkOperationsIfTtotExceedsTolerance(self, flight: Flight) -> DpiMessage:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class GroundHandlingTime(TimeQuantity):
    """The Actual Commencement of Ground Handling Time (ACGT), specific to first-of-day or long-parked flights.

    Package Timings, stereotype entity, milestones [8].
    """
    pass


@dataclass
class IFPS:
    """The Integrated Initial Flight Plan Processing System that distributes the ATC Flight Plan to all involved ATC units.

    Package Systems, stereotype boundary, milestones [1].

    Relationship: dependency 'distributes' -> AtcFlightPlan
    """

    def distributeFlightPlan(self, flightPlan: AtcFlightPlan, atcUnit: ATCUnit) -> None:
        """Distributes the ATC Flight Plan so that all involved ATC units receive it, including departure and destination aerodromes."""
        raise NotImplementedError


@dataclass
class InBlock(Milestone):
    """Milestone 7: AIBT, the time the aircraft arrives in-blocks.

    Package Milestones, stereotype control, milestones [7].
    """

    def checkTobtConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT or ATC Flight Plan, triggered by Actual In Blocks Time (AIBT)."""
        raise NotImplementedError

    def informNetworkOperationsIfTtotExceedsTolerance(self, flight: Flight) -> DpiMessage:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class InBlockTime(TimeQuantity):
    """The event of the aircraft arriving in-blocks, kept as EIBT and AIBT values.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7].
    """
    pass


@dataclass
class Landed(Milestone):
    """Milestone 6: ALDT, the time the aircraft touches down on the runway.

    Package Milestones, stereotype control, milestones [6].
    """

    def checkTobtConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT or ATC Flight Plan, triggered by Actual Landing Time (ALDT)."""
        raise NotImplementedError

    def informNetworkOperationsIfTtotExceedsTolerance(self, flight: Flight) -> DpiMessage:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class LandingTime(TimeQuantity):
    """The event of the aircraft touching down, kept as ELDT and ALDT values.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6].
    """
    pass


@dataclass
class LocalRadarUpdate(Milestone):
    """Milestone 4: the flight enters the FIR or local airspace of the destination airport, detected by radar based on SSR code.

    Package Milestones, stereotype control, milestones [4].
    """

    def commenceTobtProcess(self, flight: Flight) -> None:
        """Commences the TOBT process on detection of the flight by radar in FIR, TMA, or on Final Approach."""
        raise NotImplementedError

    def checkTobtConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT."""
        raise NotImplementedError

    def informNetworkOperationsIfTtotExceedsTolerance(self, flight: Flight) -> DpiMessage:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class MovementMessage:
    """The FSA or MVT movement message sent when a flight takes off.

    Package Messages, stereotype boundary, milestones [16].
    """
    type: MovementMessageType | None = None
    timestamp: datetime | None = None


@dataclass
class NetworkOperations:
    """The party (Network Manager operations) that issues CTOT, monitors regulated flights, and receives DPI and update messages from the airport.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 10, 15].

    Relationship: association 'regulates/monitors' -> Flight [*]

    Relationship: dependency 'receives' -> DpiMessage

    Relationship: dependency 'sends' -> FlightUpdateMessage

    Relationship: dependency 'issues CTOT for' -> TakeOffTime
    """
    name: str | None = None

    def issueCtot(self, flight: Flight) -> datetime:
        """CTOT is issued by Network Operations at EOBT-2hr for regulated flights and sent to relevant ATS units and the departure aerodrome; CTOT flights usually have priority over unregulated flights (milestone 2)."""
        raise NotImplementedError

    def monitorFlightProgress(self, flight: Flight) -> None:
        """Network Operations monitors progress of the flight using the ETFMS and sends a Flight Update Message when the flight is within 3hrs flying time of the destination (milestone 3)."""
        raise NotImplementedError

    def receiveDpiMessage(self, message: DpiMessage) -> None:
        """Network Operations receives DPI messages from the Airport CDM Platform (milestones 1,2,3,10,15)."""
        raise NotImplementedError


@dataclass
class OffBlock(Milestone):
    """Milestone 15: AOBT, the time the aircraft pushes back/vacates the parking position.

    Package Milestones, stereotype control, milestones [15].

    Relationship: dependency 'sends' -> DpiMessage
    """

    def informPartnersOfAobt(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of Actual Off-Block Time (AOBT) and that the aircraft has commenced push-back/taxi; AOBT always triggers an A-DPI message to Network Operations, or at a defined time prior to TTOT in case of remote holding."""
        raise NotImplementedError

    def checkTtotChangeAgainstTolerance(self, flight: Flight) -> bool:
        """After the first A-DPI is sent, checks TTOT updates against the TTOT tolerance before Network Operations is informed, with a new A-DPI, of the updated TTOT."""
        raise NotImplementedError


@dataclass
class OffBlockTime(TimeQuantity):
    """The event of the aircraft leaving the parking position, kept as SOBT, EOBT, TOBT and AOBT values.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 15].
    """
    tobtUpdateThreshold: int | None = None


@dataclass
class ReadyTime(TimeQuantity):
    """The Actual Ready Time (ARDT), when all doors are closed, boarding bridge removed, push back vehicle connected.

    Package Timings, stereotype entity, milestones [12].
    """
    readyTolerance: timedelta | None = None


@dataclass
class RegulationCheck(Milestone):
    """Milestone 2 (EOBT-2hr): most flights are known in the Airport CDM Platform and regulated flights receive a CTOT from Network Operations.

    Package Milestones, stereotype control, milestones [2].

    Relationship: dependency 'sends' -> DpiMessage
    """

    def checkFlightEstimatesConsistency(self, flight: Flight) -> bool:
        """Checks whether AO/GH flight estimates are consistent with the ATC Flight Plan, to verify feasibility of the estimated off block time at EOBT-2hrs."""
        raise NotImplementedError

    def informNetworkOperationsOfTtot(self, flight: Flight) -> DpiMessage:
        """Informs Network Operations about the updated take off time estimate using a T-DPI message at EOBT-2hrs."""
        raise NotImplementedError

    def calculateTtot(self, eibt: datetime, mttt: timedelta, exot: timedelta, eobt: datetime, tobt: datetime) -> datetime:
        """Calculation basis for TTOT is EIBT+MTTT+EXOT, if later than EOBT+EXOT. In case of manual TOBT input, this overrides the EIBT+MTTT estimate, hence TTOT equals TOBT+EXOT."""
        raise NotImplementedError


@dataclass
class StartUpApprovalTime(TimeQuantity):
    """The event of the aircraft's start-up approval, kept as TSAT and ASAT values.

    Package Timings, stereotype entity, milestones [10, 14].
    """
    tsatTolerance: timedelta | None = None


@dataclass
class StartUpApproved(Milestone):
    """Milestone 14: ASAT, the time an aircraft receives its start-up approval.

    Package Milestones, stereotype control, milestones [14].
    """

    def informPartnersOfAsat(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of Actual start up approval Time (ASAT) and that the aircraft has received start up/push-back clearance."""
        raise NotImplementedError

    def checkAsatAgainstTsat(self, flight: Flight) -> bool:
        """Checks if ASAT is in accordance with TSAT and alerts all relevant partners when no start-up has been granted at TSAT + tolerance; the flight will be re-sequenced."""
        raise NotImplementedError


@dataclass
class StartUpRequestTime(TimeQuantity):
    """The Actual Start-up Request Time (ASRT), when start-up is requested by the pilot.

    Package Timings, stereotype entity, milestones [13].
    """
    pass


@dataclass
class StartUpRequested(Milestone):
    """Milestone 13: the time that start up is requested (ASRT), based on pilot request.

    Package Milestones, stereotype control, milestones [13].
    """

    def informPartnersOfAsrt(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of Actual Start up Request Time (ASRT) when it occurs."""
        raise NotImplementedError

    def checkStartUpRequestedInTime(self, flight: Flight) -> bool:
        """Alerts all relevant Airport CDM Partners when no start-up has been requested inside the locally agreed TSAT tolerance window; if not requested by TSAT + tolerance the AO/GH is informed and should update TOBT."""
        raise NotImplementedError


@dataclass
class TakeOff(Milestone):
    """Milestone 16: ATOT, the time an aircraft takes off from the runway.

    Package Milestones, stereotype control, milestones [16].

    Relationship: dependency 'generates' -> MovementMessage
    """

    def informPartnersOfTakeOff(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners about the actual take off; an airborne message is generated and the flight is removed from the departure sequence. Triggered by Tower FDPS, A-SMGCS/Radar detection, or ACARS."""
        raise NotImplementedError


@dataclass
class TakeOffFromOutstation(Milestone):
    """Milestone 3: the ATOT from the outstation (ADEP) is provided to Network Operations and the Aircraft Operator.

    Package Milestones, stereotype control, milestones [3].

    Relationship: dependency 'sends' -> DpiMessage
    """

    def checkLandingEstimateConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH estimated landing time after take off from outstation is consistent with the outbound ATC Flight Plan."""
        raise NotImplementedError

    def informNetworkOperationsTdpiT(self, flight: Flight) -> DpiMessage:
        """Informs Network Operations of updated take off time estimates using a T-DPI-t message when needed; a TTOT tolerance of 5 minutes is respected before informing."""
        raise NotImplementedError

    def calculateTtot(self, eibt: datetime, mttt: timedelta, exot: timedelta, eobt: datetime, tobt: datetime) -> datetime:
        """Calculation basis for TTOT is EIBT+MTTT+EXOT. If EOBT is later than EIBT+MTTT, TTOT equals EOBT+EXOT. If TOBT is available it overrules the EIBT+MTTT estimate, so TTOT equals TOBT+EXOT."""
        raise NotImplementedError


@dataclass
class TakeOffTime(TimeQuantity):
    """The event of the aircraft taking off, kept as ETOT, TTOT, CTOT, and ATOT values.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 16].
    """
    ttotTolerance: timedelta | None = None


@dataclass
class TaxiInTime(TimeQuantity):
    """The Estimated Taxi-In Time (EXIT), used with ELDT to compute EIBT.

    Package Timings, stereotype entity, milestones [4, 6].
    """
    pass


@dataclass
class TaxiOutTime(TimeQuantity):
    """The Estimated Taxi-Out Time (EXOT), calculated by the ATC system based on predicted traffic load, gate/stand location, runway in use, and waiting period at the Holding Position.

    Package Timings, stereotype entity, milestones [2, 3, 9].
    """
    pass


@dataclass
class TimeValue:
    """One recorded value of a time quantity, with the prefix that identifies its kind, its originator, and its accuracy.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    prefix: TimePrefix | None = None
    dateTime: datetime | None = None
    originator: str | None = None
    accuracy: str | None = None
    timeOfUpdate: datetime | None = None


@dataclass
class TsatIssued(Milestone):
    """Milestone 10: the time ATC issues the Target Start Up Approval Time (TSAT).

    Package Milestones, stereotype control, milestones [10].

    Relationship: dependency 'sends' -> DpiMessage
    """

    def informPartnersOfTsat(self, flight: Flight) -> None:
        """Informs all relevant partners of the TSAT allocated to the flight; Network Operations is informed by a T-DPI-s for non-regulated flights."""
        raise NotImplementedError

    def checkTobtUpdateCount(self, flight: Flight) -> bool:
        """Checks whether the number of TOBT updates after TSAT has been issued exceeds a locally defined tolerance; if exceeded, TOBT input should be processed according to local procedure."""
        raise NotImplementedError


@dataclass
class TurnRound:
    """The aircraft turn-round that normally includes an arriving and a departing flight, each with a related flight plan.

    Package Flights, stereotype entity, milestones [1].

    Relationship: association 'arrival' -> Flight [1]

    Relationship: association 'departure' -> Flight [0..1]
    """
    turnRoundId: str | None = None


@dataclass
class TurnroundTime(TimeQuantity):
    """The estimated or minimum turn-round period (MTTT) used as basis for TOBT and TTOT calculation.

    Package Timings, stereotype entity, milestones [2, 3, 6, 7, 8].
    """
    minimumTurnRoundTime: timedelta | None = None
