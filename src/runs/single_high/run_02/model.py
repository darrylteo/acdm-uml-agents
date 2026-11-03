"""Class stubs rendered from runs/single_high/run_02/model.json by src/generate/render_code.py; do not edit by hand."""
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


class OperationalStatus(Enum):
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


class PrefixType(Enum):
    SCHEDULED = "Scheduled"
    ESTIMATED = "Estimated"
    TARGET = "Target"
    ACTUAL = "Actual"
    CALCULATED = "Calculated"


@dataclass
class ACARS:
    """The aircraft system that can automatically report actual times equivalent to ALDT, AIBT, AOBT and ATOT.

    Package Systems, stereotype boundary, milestones [6, 7, 15, 16].
    """

    def reportEvent(self, flight: Flight, eventType: str) -> datetime:
        """Reports an actual time (ACARS=ON at landing M6, IN at in-block M7, OUT at off-block M15, OFF at take-off M16), with an accuracy of +/- 1 minute."""
        raise NotImplementedError


@dataclass
class AirportCDMPartner:
    """An abstract party that takes part in the Airport CDM process and is informed of, or provides, milestone information.

    Package Stakeholders, stereotype entity, milestones [1, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    name: str | None = None


@dataclass
class ATCUnit(AirportCDMPartner):
    """An air traffic control unit (ACC, Approach Control, Tower, or ATS unit) that receives the flight plan, detects the flight, calculates EXOT, and issues TSAT/ASAT.

    Package Stakeholders, stereotype entity, milestones [1, 2, 4, 5, 9, 10, 12, 13, 14, 16].
    """
    unitRole: str | None = None

    def calculateEXOT(self, trafficLoad: str, gateStandLocation: str, runwayInUse: str, holdingPositionWait: timedelta) -> TaxiOutTime:
        """The ATC system calculates and provides the Estimated Taxi-Out Time based on the predicted traffic load, gate/stand location, runway in use, and waiting period at the Holding Position, following receipt of TOBT (M9)."""
        raise NotImplementedError

    def issueTSAT(self, flight: Flight, t: timedelta) -> StartUpApprovalTime:
        """ATC issues the Target Start-Up Approval Time, t minutes before EOBT, a locally agreed parameter (M10)."""
        raise NotImplementedError

    def approveStartUp(self, flight: Flight) -> StartUpApprovalTime:
        """ATC gives start-up approval (ASAT) following a pilot's request, on receipt of which the aircraft will start up, push back and taxi (M14)."""
        raise NotImplementedError

    def confirmTSATToPilot(self, flight: Flight) -> None:
        """ATC confirms TSAT to the pilot to maintain the aircraft in the pre-departure sequence and assure that a regulated flight can respect its CTOT (M13)."""
        raise NotImplementedError

    def detectFlight(self, flight: Flight) -> None:
        """Detects the flight based upon its assigned SSR code, when it crosses a defined FIR/ATC boundary (M4) or a defined range/position/level on final approach (M5)."""
        raise NotImplementedError


@dataclass
class AirborneMessage:
    """The airborne message generated when the aircraft takes off, after which the flight is removed from the departure sequence.

    Package Messages, stereotype boundary, milestones [16].
    """
    pass


@dataclass
class Aircraft:
    """The physical aircraft operating a flight, identified by type and registration.

    Package Flights, stereotype entity, milestones [1, 3].
    """
    registration: str | None = None
    aircraftType: str | None = None


@dataclass
class TurnRoundPartner(AirportCDMPartner):
    """The Aircraft Operator or Ground Handler (AO/GH), referred to jointly by the document, who together manage the turn-round and provide TOBT and related operational times.

    Package Stakeholders, stereotype entity, milestones [2, 3, 4, 5, 6, 7, 8, 9, 12].
    """

    def updateTOBT(self, flight: Flight, turnRoundPeriod: timedelta) -> OffBlockTime:
        """TOBT is updated automatically or inserted manually, calculated on the basis of the defined/estimated turn-round period for the departing flight (M3,6,7,8); manual input overrides the EIBT+MTTT estimate so TTOT equals TOBT+EXOT (M2,3)."""
        raise NotImplementedError

    def confirmFinalTOBT(self, flight: Flight, t: timedelta) -> OffBlockTime:
        """AO/GH provide their most accurate TOBT taking into account the operational situation, t minutes before EOBT, a locally agreed parameter (M9)."""
        raise NotImplementedError

    def reportGroundHandlingStart(self, flight: Flight) -> datetime:
        """Provides ACGT, the actual commencement of ground handling operations, for flights that are the first operation of the day or long-term parked (M8)."""
        raise NotImplementedError

    def reportAircraftReady(self, flight: Flight) -> ReadyTime:
        """Provides ARDT: all doors closed, boarding bridge removed, push back vehicle connected, ready to taxi immediately upon reception of TWR instructions (M12)."""
        raise NotImplementedError

    def manageTurnRound(self, flight: Flight) -> None:
        """In coordination with the aircrew, manages the turn-round process accordingly following TOBT confirmation and TSAT issue (M9,10)."""
        raise NotImplementedError


@dataclass
class AircraftOperator(TurnRoundPartner):
    """The airline operating the flight, responsible for submitting the ATC Flight Plan and, jointly with the Ground Handler, providing TOBT and turn-round data.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9].

    Relationship: association 'submits' -> AtcFlightPlan [*]
    """

    def submitAtcFlightPlan(self, flightPlan: AtcFlightPlan) -> None:
        """Submits the ICAO ATC Flight Plan, which is distributed by IFPS so all involved ATC units, including departure and destination aerodromes, receive it (M1)."""
        raise NotImplementedError

    def provideCorrectInformation(self, sobt: OffBlockTime, registration: str, firstDestination: str) -> None:
        """Must provide correct information before the first E-DPI message, feeding Network Operations with consistent SOBT, aircraft registration and first destination data as early in time as possible (M1)."""
        raise NotImplementedError


@dataclass
class Aircrew(AirportCDMPartner):
    """The flight crew (pilot) who requests start-up and coordinates with the Ground Handler during the turn-round.

    Package Stakeholders, stereotype entity, milestones [12, 13, 14].
    """

    def requestStartUp(self, flight: Flight) -> datetime:
        """The pilot requests start-up just before TSAT, following coordination with the Ground Handler, producing the Actual Start-up Request Time (M12,13)."""
        raise NotImplementedError


@dataclass
class AirportCDMPlatform:
    """The Airport CDM Platform, the technical system initiated for each flight that processes available information, computes estimates, and records the Actions on CDM Operation (ACISP) at each milestone.

    Package Systems, stereotype boundary, milestones [1, 2, 4, 15, 16].

    Relationship: association 'executes' -> Milestone [1..*]

    Relationship: association 'processes information for' -> Flight [*]
    """
    initiatedFlight: Flight | None = None

    def initiateForFlight(self, flight: Flight) -> None:
        """The Airport CDM Platform is initiated for this flight and all available information is processed (M1)."""
        raise NotImplementedError

    def computeTOBTAutomatically(self, flight: Flight) -> OffBlockTime:
        """TOBT is calculated automatically by the Airport CDM Platform, following an ELDT update (M4)."""
        raise NotImplementedError

    def recordAOBT(self, flight: Flight, aobt: datetime) -> None:
        """Records AOBT (M15)."""
        raise NotImplementedError

    def recordATOT(self, flight: Flight, atot: datetime) -> None:
        """Records ATOT (M16)."""
        raise NotImplementedError


@dataclass
class AirportSlot:
    """The airport slot allocated to the flight under the airport slot programme, with which the ATC Flight Plan must correspond.

    Package Flights, stereotype entity, milestones [1].
    """
    slotTime: datetime | None = None


@dataclass
class AirportSurveillanceSystem:
    """The radar, A-SMGCS or Tower FDPS system that detects a flight by its assigned SSR code crossing the FIR/ATC boundary, entering final approach, or taking off.

    Package Systems, stereotype boundary, milestones [4, 5, 16].
    """

    def detectFIRCrossing(self, flight: Flight) -> None:
        """Detects a flight based upon the assigned SSR code when it crosses a defined FIR/ATC boundary (M4)."""
        raise NotImplementedError

    def detectFinalApproach(self, flight: Flight) -> None:
        """Detects when the flight crosses a defined range/position or passes/leaves a predetermined level on final approach (M5)."""
        raise NotImplementedError

    def detectTakeOff(self, flight: Flight) -> None:
        """Detects take-off via Tower FDPS, A-SMGCS or Radar (M16)."""
        raise NotImplementedError


@dataclass
class AtcFlightPlan:
    """The ICAO flight plan submitted to ATC for a flight, distributed by IFPS, which may be a one-off submission or a repetitive flight plan (RFPL).

    Package Flights, stereotype entity, milestones [1].
    """
    isRepetitive: bool | None = None
    sobt: datetime | None = None
    destinationAerodrome: str | None = None
    departureAerodrome: str | None = None
    submissionTime: datetime | None = None

    def checkConsistency(self, slot: AirportSlot, flightData: Flight) -> bool:
        """Checks consistency between the ATC Flight Plan, Airport Slot and Airport flight data before the first E-DPI is sent (M1)."""
        raise NotImplementedError


@dataclass
class TimeQuantity:
    """A time quantity describing a flight's progress, named by a prefix (Scheduled, Estimated, Target, Actual, Calculated) and an event, with its origin, accuracy and tolerance; every successive value is kept.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    prefix: PrefixType | None = None
    value: datetime | None = None
    accuracy: str | None = None
    tolerance: timedelta | None = None
    originator: str | None = None
    timeOfUpdate: datetime | None = None

    def recordValue(self, value: datetime, originator: str) -> None:
        """Appends a new successive value with its originator and time of update rather than overwriting the previous value."""
        raise NotImplementedError


@dataclass
class BoardingTime(TimeQuantity):
    """The Actual Start Boarding Time (ASBT), when the gate opens for passengers to physically start boarding.

    Package Timings, stereotype entity, milestones [11].
    """
    pass


@dataclass
class DPIMessage:
    """A Departure Planning Information message (E-DPI, T-DPI, T-DPI-t, T-DPI-s or A-DPI) sent to Network Operations to inform of updated take-off time estimates.

    Package Messages, stereotype boundary, milestones [1, 2, 3, 10, 15].
    """
    type: DPIType | None = None
    sentAt: datetime | None = None

    def send(self, flight: Flight) -> None:
        """Sends the message to Network Operations."""
        raise NotImplementedError


@dataclass
class ETFMS:
    """The system Network Operations uses to monitor progress of a flight within 3 hrs flying time of the destination airport.

    Package Systems, stereotype boundary, milestones [3].
    """

    def monitorProgress(self, flight: Flight) -> None:
        """Monitors progress of the flight so that Network Operations can send a Flight Update Message providing updates of the flight's progress (M3)."""
        raise NotImplementedError


@dataclass
class FSAMessage:
    """The FSA message sent when the aircraft takes off.

    Package Messages, stereotype boundary, milestones [16].
    """
    pass


@dataclass
class Flight:
    """A single arrival or departure flight tracked through the CDM process from ATC Flight Plan activation to take-off, carrying its operational status and successive time estimates.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'described by' -> AtcFlightPlan [1]

    Relationship: association 'corresponds to' -> AirportSlot [0..1]

    Relationship: association 'operated by' -> Aircraft [1]

    Relationship: association 'records' -> OffBlockTime [1..*]

    Relationship: association 'records' -> InBlockTime [1..*]

    Relationship: association 'records' -> LandingTime [1..*]

    Relationship: association 'records' -> TakeOffTime [1..*]

    Relationship: association 'records' -> TaxiOutTime [1..*]

    Relationship: association 'records' -> TaxiInTime [1..*]

    Relationship: association 'records' -> StartUpApprovalTime [1..*]

    Relationship: association 'records' -> BoardingTime [0..*]

    Relationship: association 'records' -> ReadyTime [0..*]

    Relationship: association 'records' -> StartUpRequestTime [0..*]
    """
    flightId: str | None = None
    direction: str | None = None
    aircraftType: str | None = None
    registration: str | None = None
    operationalStatus: OperationalStatus | None = None
    isRegulated: bool | None = None
    offBlockTime: OffBlockTime | None = None
    inBlockTime: InBlockTime | None = None
    landingTime: LandingTime | None = None
    takeOffTime: TakeOffTime | None = None
    taxiOutTime: TaxiOutTime | None = None
    taxiInTime: TaxiInTime | None = None
    startUpApprovalTime: StartUpApprovalTime | None = None
    boardingTime: BoardingTime | None = None
    readyTime: ReadyTime | None = None
    startUpRequestTime: StartUpRequestTime | None = None

    def isReadyWithin15MinOfEOBT(self) -> bool:
        """The flight is ready not later than 15 minutes after the planned EOBT (M1)."""
        raise NotImplementedError


@dataclass
class FlightUpdateMessage:
    """The FUM sent by Network Operations, via ETFMS, that provides updates of a flight's progress and is used to update ELDT.

    Package Messages, stereotype boundary, milestones [2, 3].
    """
    progressData: str | None = None


@dataclass
class GroundHandler(TurnRoundPartner):
    """The ground handling company that carries out turn-round operations for the flight.

    Package Stakeholders, stereotype entity, milestones [3, 4, 5, 6, 7, 8, 9, 11, 12].
    """
    pass


@dataclass
class IFPS:
    """The system that distributes the submitted ATC Flight Plan to all involved ATC units.

    Package Systems, stereotype boundary, milestones [1].

    Relationship: dependency 'distributes' -> AtcFlightPlan
    """

    def distributeFlightPlan(self, flightPlan: AtcFlightPlan) -> None:
        """Distributes the ATC Flight Plan submitted by the Aircraft Operator so that all involved ATC units, including departure and destination aerodromes, receive it (M1)."""
        raise NotImplementedError


@dataclass
class InBlockTime(TimeQuantity):
    """The in-block time for the flight, held as EIBT or AIBT depending on its prefix.

    Package Timings, stereotype entity, milestones [1, 3, 4, 5, 6, 7].
    """

    def calculateEIBT(self, landingTime: LandingTime, exit: TaxiInTime) -> datetime:
        """EIBT is computed using the ELDT/ALDT and the estimated/actual taxi-in time EXIT (M4,6)."""
        raise NotImplementedError


@dataclass
class LandingTime(TimeQuantity):
    """The landing time for the flight, held as ELDT or ALDT depending on its prefix.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6].
    """

    def calculateELDT(self, atot: TakeOffTime, estimatedElapsedTime: timedelta) -> datetime:
        """ELDT is calculated using the ATOT and the Estimated Elapsed Time on the FPL (M3)."""
        raise NotImplementedError


@dataclass
class Milestone:
    """One of the sixteen defined events of the Airport CDM process, each with its trigger, timing rule, effect on operational status, and procedure.

    Package Milestones, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    name: str | None = None
    trigger: str | None = None
    timingRule: str | None = None
    effect: str | None = None
    operationalStatusChange: OperationalStatus | None = None


@dataclass
class M10TSATIssued(Milestone):
    """The milestone at which ATC issues the Target Start-Up Approval Time (TSAT), t minutes before EOBT.

    Package Milestones, stereotype control, milestones [10].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'sends T-DPI-s' -> DPIMessage
    """

    def informPartnersOfTSAT(self, flight: Flight) -> None:
        """Informs all relevant partners of the TSAT allocated to the flight; Network Operations is informed by a T-DPI-s for non-regulated flights (M10)."""
        raise NotImplementedError

    def checkTOBTUpdateCount(self, flight: Flight, threshold: int) -> bool:
        """Checks whether the number of TOBT updates after TSAT has been issued exceeds a locally defined tolerance; if exceeded the TOBT input is processed according to local procedure (M10)."""
        raise NotImplementedError


@dataclass
class M11BoardingStarts(Milestone):
    """The milestone at which the gate opens for passengers to physically start boarding (ASBT).

    Package Milestones, stereotype control, milestones [11].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'informs' -> AirportCDMPartner
    """

    def informPartnersOfASBT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of the Actual Start Boarding Time when it occurs (M11)."""
        raise NotImplementedError

    def checkBoardingStatus(self, flight: Flight, timeBeforeTOBT: timedelta) -> bool:
        """At a locally defined time before TOBT (e.g. corresponding to aircraft type), checks the boarding status and informs the AO/GH if TOBT needs updating (M11)."""
        raise NotImplementedError


@dataclass
class M12AircraftReady(Milestone):
    """The milestone at which the aircraft is ready for start-up/push-back (ARDT).

    Package Milestones, stereotype control, milestones [12].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'informs' -> AirportCDMPartner

    Relationship: dependency 'or RDY' -> ReadyStatusMessage
    """

    def informPartnersOfARDT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of ARDT or Ready Status (RDY) in the Airport CDM Platform, confirming that the flight follows the indicated TOBT (M12)."""
        raise NotImplementedError

    def alertIfNoReadyStatus(self, flight: Flight, tolerance: timedelta) -> None:
        """At TOBT + tolerance, informs the AO/GH that TOBT has passed and no ready status message has yet been received (M12)."""
        raise NotImplementedError


@dataclass
class M13StartUpRequested(Milestone):
    """The milestone at which start-up is requested (ASRT), based on the pilot's request to ATC.

    Package Milestones, stereotype control, milestones [13].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'informs' -> AirportCDMPartner
    """

    def informPartnersOfASRT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of the Actual Start-up Request Time when it occurs (M13)."""
        raise NotImplementedError

    def alertIfNoStartUpRequest(self, flight: Flight, tolerance: timedelta) -> None:
        """If the start-up request is not made by TSAT + tolerance, informs the AO/GH that no start-up has been requested and that TOBT should be updated (M13)."""
        raise NotImplementedError


@dataclass
class M14StartUpApproved(Milestone):
    """The milestone at which the aircraft receives its start-up approval (ASAT).

    Package Milestones, stereotype control, milestones [14].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'informs' -> AirportCDMPartner
    """

    def informPartnersOfASAT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of ASAT in the Airport CDM Platform, confirming that the aircraft has received start-up approval/push-back clearance (M14)."""
        raise NotImplementedError

    def checkASATAgainstTSAT(self, flight: Flight, tolerance: timedelta) -> bool:
        """Checks if ASAT is in accordance with TSAT; if start-up approval is not granted at TSAT + tolerance, all relevant partners are informed and the flight is re-sequenced (M14)."""
        raise NotImplementedError


@dataclass
class M15OffBlock(Milestone):
    """The milestone at which the aircraft pushes back/vacates the parking position (AOBT).

    Package Milestones, stereotype control, milestones [15].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'sends A-DPI' -> DPIMessage

    Relationship: dependency 'informs' -> NetworkOperations
    """

    def informPartnersOfAOBT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of AOBT in the Airport CDM Platform, that the aircraft has commenced push-back/taxi from the parking position (M15)."""
        raise NotImplementedError

    def sendADPI(self, flight: Flight) -> DPIMessage:
        """AOBT always triggers an A-DPI message to Network Operations, or in the case of remote holding, at a defined time prior to TTOT (M15)."""
        raise NotImplementedError

    def checkTTOTChangeAndInform(self, flight: Flight, tolerance: timedelta) -> None:
        """After the first A-DPI is sent, checks TTOT updates against the TTOT tolerance before Network Operations is informed, with a new A-DPI, of the updated TTOT (M15)."""
        raise NotImplementedError


@dataclass
class M16TakeOff(Milestone):
    """The milestone at which the aircraft takes off from the runway (ATOT).

    Package Milestones, stereotype control, milestones [16].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'sends' -> FSAMessage

    Relationship: dependency 'sends' -> MVTMessage

    Relationship: dependency 'generates' -> AirborneMessage

    Relationship: dependency 'detected by' -> AirportSurveillanceSystem

    Relationship: dependency 'provided by' -> ACARS
    """

    def informPartnersOfATOT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners about the actual take-off (M16)."""
        raise NotImplementedError

    def generateAirborneMessageAndRemoveFromSequence(self, flight: Flight) -> None:
        """Generates an airborne message and removes the flight from the departure sequence, triggered by Tower FDPS, A-SMGCS/Radar detection or ACARS (M16)."""
        raise NotImplementedError

    def sendFSAandMVT(self, flight: Flight) -> None:
        """Sends FSA and MVT messages (M16)."""
        raise NotImplementedError


@dataclass
class M1FlightPlanActivated(Milestone):
    """The milestone at which the ICAO flight plan is submitted to ATC and the Airport CDM Platform is initiated for the flight.

    Package Milestones, stereotype control, milestones [1].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'sends E-DPI' -> DPIMessage
    """

    def checkConsistency(self, flightPlan: AtcFlightPlan, slot: AirportSlot, flightData: Flight) -> bool:
        """Checks consistency between the ATC Flight Plan, Airport Slot and Airport flight data before the first E-DPI is sent, to confirm the flight to Network Operations and allow further local processing (M1)."""
        raise NotImplementedError

    def sendFirstEDPI(self, flight: Flight) -> DPIMessage:
        """Sends the first E-DPI message once correct SOBT, registration and first destination data are provided; should not be sent if information is missing or inconsistent; triggered by first activation of the flight plan (earliest EOBT-3hr) or new/late submissions after cancellation or revised EOBT (M1)."""
        raise NotImplementedError

    def updateArrivalEstimates(self, flight: Flight) -> None:
        """For an arrival, ELDT and EIBT are updated (M1)."""
        raise NotImplementedError

    def updateDepartureEstimates(self, flight: Flight) -> None:
        """For a departure, EOBT and ETOT are updated (M1)."""
        raise NotImplementedError

    def initiateOutboundFlight(self, flight: Flight) -> None:
        """For non-coordinated airports the flight plan is used to initiate the outbound flight; for coordinated airports the outbound flight is already known (M1)."""
        raise NotImplementedError


@dataclass
class M2EOBTMinus2h(Milestone):
    """The milestone at EOBT-2h at which most flights are known, regulated flights receive a CTOT, and Network Operations is informed of the updated take-off time estimate.

    Package Milestones, stereotype control, milestones [2].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'sends T-DPI' -> DPIMessage

    Relationship: dependency 'informs / CTOT issued by' -> NetworkOperations
    """

    def checkFlightEstimatesConsistency(self, flight: Flight) -> bool:
        """Checks, before or after take-off from outstation, whether AO/GH flight estimates are consistent with the ATC Flight Plan, verifying feasibility of EOBT at EOBT-2hrs (M2)."""
        raise NotImplementedError

    def sendFirstTDPI(self, flight: Flight) -> DPIMessage:
        """Informs Network Operations of the updated take-off time estimate via a first T-DPI message at EOBT-2hrs (M2)."""
        raise NotImplementedError

    def markRegulated(self, flight: Flight) -> None:
        """Marks appropriate fields as REGULATED for a flight that has received a CTOT (M2)."""
        raise NotImplementedError

    def updateInboundELDT(self, flight: Flight, fum: FlightUpdateMessage) -> None:
        """For inbound flights, ELDT is updated based on information provided by FUM messages, taking into account the actual progress of the flight (M2)."""
        raise NotImplementedError


@dataclass
class M3TakeOffFromOutstation(Milestone):
    """The milestone at which the ATOT from the outstation is recorded and used to check and update downstream estimates.

    Package Milestones, stereotype control, milestones [3].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'sends T-DPI-t' -> DPIMessage

    Relationship: dependency 'receives FUM' -> FlightUpdateMessage
    """

    def checkLandingEstimateConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH estimated landing time after take-off from outstation is consistent with the outbound ATC Flight Plan (M3)."""
        raise NotImplementedError

    def sendTDPIt(self, flight: Flight) -> DPIMessage:
        """Informs Network Operations about updated take-off time estimates using a T-DPI-t message when needed, respecting a TTOT tolerance of 5 minutes before informing (M3)."""
        raise NotImplementedError

    def receiveOutstationATOT(self, flight: Flight) -> TakeOffTime:
        """Records ATOT, received from either the Network Operations FUM or via the AO/GH, if the destination is more than 3 hrs flying time away (M3)."""
        raise NotImplementedError


@dataclass
class M4LocalRadarUpdate(Milestone):
    """The milestone at which the flight enters the FIR or local airspace of the destination airport, detected by radar via the assigned SSR code.

    Package Milestones, stereotype control, milestones [4].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'informs' -> NetworkOperations

    Relationship: dependency 'detected by' -> AirportSurveillanceSystem
    """

    def commenceTOBTProcess(self, flight: Flight) -> None:
        """Commences the TOBT process and checks whether the AO/GH TOBT is consistent with the ATC Flight Plan, given the updated ELDT (M4)."""
        raise NotImplementedError

    def informNetworkOperationsIfTTOTChange(self, flight: Flight, tolerance: timedelta) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance (M4)."""
        raise NotImplementedError

    def preventStandGateChangeAfterELDTMinus30(self, flight: Flight) -> bool:
        """Any change to a stand or gate is not preferred after ELDT-30', taking into account the taxi-in time EXIT, to decrease last-minute stand/gate changes (M4)."""
        raise NotImplementedError


@dataclass
class M5FinalApproach(Milestone):
    """The milestone at which the flight enters the Final Approach phase, detected by radar crossing a defined range/position or level.

    Package Milestones, stereotype control, milestones [5].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'detected by' -> AirportSurveillanceSystem

    Relationship: dependency 'informs' -> NetworkOperations
    """

    def commenceTOBTProcess(self, flight: Flight) -> None:
        """Commences the TOBT process and checks whether the AO/GH TOBT is consistent with the ATC Flight Plan, given the updated ELDT (M5)."""
        raise NotImplementedError

    def informNetworkOperationsIfTTOTChange(self, flight: Flight, tolerance: timedelta) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance (M5)."""
        raise NotImplementedError


@dataclass
class M6Landed(Milestone):
    """The milestone at which ALDT, the actual landing time, is recorded.

    Package Milestones, stereotype control, milestones [6].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'informs' -> NetworkOperations

    Relationship: dependency 'provided by' -> ACARS
    """

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT or ATC Flight Plan (M6)."""
        raise NotImplementedError

    def informNetworkOperationsIfTTOTChange(self, flight: Flight, tolerance: timedelta) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance (M6)."""
        raise NotImplementedError

    def updateELDTtoALDT(self, flight: Flight) -> None:
        """ELDT changes to ALDT on landing, triggering an update of downstream estimates TOBT and TTOT, and EIBT may be updated as ALDT+EXIT (M6)."""
        raise NotImplementedError


@dataclass
class M7InBlock(Milestone):
    """The milestone at which AIBT, the actual in-block time, is recorded.

    Package Milestones, stereotype control, milestones [7].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'provided by' -> ACARS

    Relationship: dependency 'informs' -> NetworkOperations
    """

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT or ATC Flight Plan (M7)."""
        raise NotImplementedError

    def informNetworkOperationsIfTTOTChange(self, flight: Flight, tolerance: timedelta) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance (M7)."""
        raise NotImplementedError

    def updateEIBTtoAIBT(self, flight: Flight) -> None:
        """EIBT changes to AIBT, triggering an update of downstream estimates TOBT and TTOT, calculated on the basis of the estimated turn-round period for the departing flight (M7)."""
        raise NotImplementedError


@dataclass
class M8GroundHandlingStarted(Milestone):
    """The milestone at which ground handling operations commence (ACGT), specific to flights that are the first operation of the day or have been long-term parked.

    Package Milestones, stereotype control, milestones [8].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'informs' -> NetworkOperations
    """

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT or ATC Flight Plan (M8)."""
        raise NotImplementedError

    def informNetworkOperationsIfTTOTChange(self, flight: Flight, tolerance: timedelta) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance (M8)."""
        raise NotImplementedError


@dataclass
class M9FinalConfirmationTOBT(Milestone):
    """The milestone at which the AO/GH provides its most accurate TOBT, t minutes before EOBT, prior to TSAT issue.

    Package Milestones, stereotype control, milestones [9].

    Relationship: association 'processes' -> Flight [1]

    Relationship: dependency 'EXOT calculated by' -> ATCUnit

    Relationship: dependency 'informs' -> NetworkOperations
    """

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """At a predefined local time, checks whether the AO/GH TOBT is consistent with the ATC Flight Plan, to confirm TOBT prior to TSAT issue (M9)."""
        raise NotImplementedError

    def informNetworkOperationsIfTTOTChange(self, flight: Flight, tolerance: timedelta) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance (M9)."""
        raise NotImplementedError

    def confirmTOBT(self, flight: Flight) -> bool:
        """Triggered by a new TOBT or TTOT update; no need to confirm an existing TOBT if it has already been manually modified before (M9)."""
        raise NotImplementedError


@dataclass
class MVTMessage:
    """The MVT message sent when the aircraft takes off.

    Package Messages, stereotype boundary, milestones [16].
    """
    pass


@dataclass
class MinimumTurnRoundTime(TimeQuantity):
    """The minimum/estimated turn-round period (MTTT) used as the basis for calculating TOBT and TTOT for a departing flight.

    Package Timings, stereotype entity, milestones [2, 3, 6, 7, 8].
    """
    pass


@dataclass
class NetworkOperations(AirportCDMPartner):
    """The network management function that issues CTOT, monitors flight progress via ETFMS, and is kept informed by DPI messages so ATC Flight Plan estimates stay consistent.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15].

    Relationship: dependency 'monitors flight progress using' -> ETFMS

    Relationship: dependency 'sends' -> FlightUpdateMessage
    """

    def issueCTOT(self, flight: Flight) -> TakeOffTime:
        """Issues the CTOT, sent to relevant ATS units and the departure aerodrome, for regulated flights at EOBT-2h (M2)."""
        raise NotImplementedError

    def monitorFlightProgress(self, flight: Flight) -> None:
        """Monitors progress of the flight using the ETFMS and sends a Flight Update Message providing updates of the flight's progress, when within 3 hrs flying time of the destination (M3)."""
        raise NotImplementedError

    def receiveDPI(self, message: DPIMessage) -> None:
        """Receives DPI messages informing it of updated take-off time estimates (M1,2,3,10,15)."""
        raise NotImplementedError


@dataclass
class OffBlockTime(TimeQuantity):
    """The off-block time for the flight, held as SOBT, EOBT, TOBT or AOBT depending on its prefix.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15].
    """
    pass


@dataclass
class ReadyStatusMessage:
    """The Ready Status (RDY) message that may be sent instead of ARDT, confirming the flight follows the indicated TOBT.

    Package Messages, stereotype boundary, milestones [12].
    """
    pass


@dataclass
class ReadyTime(TimeQuantity):
    """The Actual Ready Time (ARDT), when the aircraft's doors are closed, boarding bridge removed, and push-back vehicle connected.

    Package Timings, stereotype entity, milestones [12].
    """
    pass


@dataclass
class StandGateManagement(AirportCDMPartner):
    """The party managing stand and gate allocation, which shares EOBT with ATC and Network Operations and is affected by stand/gate change decisions.

    Package Stakeholders, stereotype entity, milestones [9].
    """
    pass


@dataclass
class StartUpApprovalTime(TimeQuantity):
    """The start-up approval time for the flight, held as TSAT or ASAT depending on its prefix.

    Package Timings, stereotype entity, milestones [9, 10, 12, 13, 14].
    """
    pass


@dataclass
class StartUpRequestTime(TimeQuantity):
    """The Actual Start-Up Request Time (ASRT), when start-up is requested by the pilot.

    Package Timings, stereotype entity, milestones [13].
    """
    pass


@dataclass
class TakeOffTime(TimeQuantity):
    """The take-off time for the flight, held as ETOT, TTOT, CTOT or ATOT depending on its prefix.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 16].
    """

    def calculateTTOT(self, eibt: InBlockTime, mttt: MinimumTurnRoundTime, exot: TaxiOutTime, eobt: OffBlockTime, tobt: OffBlockTime) -> datetime:
        """Calculation basis for TTOT is EIBT+MTTT+EXOT, if later than EOBT+EXOT (M2); if EOBT is later than EIBT+MTTT, TTOT equals EOBT+EXOT (M3); if TOBT is available it overrules the EIBT+MTTT estimate, so TTOT equals TOBT+EXOT (M2,3)."""
        raise NotImplementedError


@dataclass
class TaxiInTime(TimeQuantity):
    """The estimated taxi-in time (EXIT), used with ELDT/ALDT to compute EIBT.

    Package Timings, stereotype entity, milestones [4, 6].
    """
    pass


@dataclass
class TaxiOutTime(TimeQuantity):
    """The Estimated Taxi-Out Time (EXOT), calculated by the ATC system.

    Package Timings, stereotype entity, milestones [2, 3, 9, 15].
    """
    pass


@dataclass
class TurnRound:
    """The aircraft turn-round, normally comprising an arriving flight and a related departing flight, analysed using the minimum turn-round time.

    Package Flights, stereotype entity, milestones [1, 4, 6, 7, 8].

    Relationship: composition 'arrival flight' -> Flight [0..1]

    Relationship: composition 'departure flight' -> Flight [0..1]

    Relationship: association 'has' -> MinimumTurnRoundTime [1]
    """
    minimumTurnRoundTime: MinimumTurnRoundTime | None = None
