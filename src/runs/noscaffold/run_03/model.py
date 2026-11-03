"""Class stubs rendered from runs/noscaffold/run_03/model.json by src/generate/render_code.py; do not edit by hand."""
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


class OperationalStatus(Enum):
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


@dataclass
class ATCFlightPlan:
    """The ICAO flight plan submitted by the Aircraft Operator and distributed by IFPS to all involved ATC units.

    Package FlightPlanning, stereotype entity, milestones [1].

    Relationship: association 'corresponds to' -> AirportSlot [0..1]

    Relationship: association 'checked against' -> AirportFlightData [1]
    """
    flightPlanId: str | None = None
    eobt: datetime | None = None
    estimatedElapsedTime: timedelta | None = None
    departureAerodrome: str | None = None
    destinationAerodrome: str | None = None
    aircraftType: str | None = None
    aircraftRegistration: str | None = None
    isRepetitive: bool | None = None
    submissionTime: datetime | None = None

    def checkConsistency(self, slot: AirportSlot, flightData: AirportFlightData) -> bool:
        """Checks consistency between the ATC Flight Plan, Airport Slot and Airport flight data before the first E-DPI is sent."""
        raise NotImplementedError


@dataclass
class AircraftOperator:
    """The airline or operator that submits the ATC Flight Plan and provides estimates (TOBT, ARDT, etc.) throughout the turn-round.

    Package Actors, stereotype entity, milestones [1, 2, 3, 4, 6, 7, 8, 9, 11, 12].

    Relationship: dependency 'submits' -> ATCFlightPlan [1..*]

    Relationship: association 'operates / provides estimates for' -> Flight [*]
    """
    operatorId: str | None = None
    name: str | None = None

    def submitFlightPlan(self, flightPlan: ATCFlightPlan) -> None:
        """Submits the ICAO flight plan for distribution by IFPS."""
        raise NotImplementedError

    def provideTobt(self, flight: Flight, tobt: datetime) -> None:
        """Provides or updates the Target Off-Block Time for the flight."""
        raise NotImplementedError


@dataclass
class AirportCDMPlatform:
    """The Airport CDM Platform that is initiated for a flight, processes all available information and orchestrates the milestone processes.

    Package Control, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'manages' -> Flight [*]

    Relationship: association 'executes' -> MilestoneProcess [1..*]
    """
    platformId: str | None = None

    def initiateFlight(self, flightPlan: ATCFlightPlan) -> None:
        """Initiates processing for a flight upon activation of its ATC Flight Plan, setting status to INITIATED."""
        raise NotImplementedError

    def notifyPartners(self, flight: Flight, event: str) -> None:
        """Informs all relevant Airport CDM Partners of an actual time event (e.g. ASBT, ARDT, ASRT, ASAT, AOBT, ATOT) as it occurs."""
        raise NotImplementedError

    def changeStatus(self, flight: Flight, newStatus: OperationalStatus) -> None:
        """Updates the operational status of a flight following a milestone occurrence."""
        raise NotImplementedError


@dataclass
class AirportFlightData:
    """Local airport flight data used together with the flight plan and slot to confirm the flight for further processing.

    Package FlightPlanning, stereotype entity, milestones [1].
    """
    sobt: datetime | None = None
    aircraftRegistration: str | None = None
    firstDestination: str | None = None


@dataclass
class AirportSlot:
    """The airport slot programme entry that the ATC Flight Plan is expected to correspond to.

    Package FlightPlanning, stereotype entity, milestones [1].
    """
    slotId: str | None = None
    scheduledTime: datetime | None = None
    isCoordinatedAirport: bool | None = None


@dataclass
class AtcUnit:
    """An Air Traffic Control unit (tower, ACC/Approach) that provides radar detections, TSAT, ASAT and other ATC-controlled milestone data.

    Package Actors, stereotype entity, milestones [1, 4, 5, 10, 13, 14, 16].

    Relationship: association 'receives flight plan / detects radar' -> Flight [*]

    Relationship: association 'issues TSAT for' -> Flight [*]

    Relationship: association 'approves start-up for' -> Flight [*]
    """
    unitId: str | None = None
    unitType: str | None = None

    def issueTsat(self, flight: Flight) -> datetime:
        """Issues the Target Start-Up Approval Time for the flight, sequencing it into the pre-departure sequence."""
        raise NotImplementedError

    def approveStartUp(self, flight: Flight) -> None:
        """Grants start-up/push-back clearance recorded as ASAT, checked against TSAT."""
        raise NotImplementedError


@dataclass
class DpiMessage:
    """A Departure Planning Information message exchanged between the Airport CDM Platform and Network Operations to communicate updated take-off time estimates.

    Package Messaging, stereotype entity, milestones [1, 2, 3, 4, 15].

    Relationship: dependency 'informs' -> NetworkOperations [1]

    Relationship: association 'has type' -> DpiMessageType [1]
    """
    messageType: DpiMessageType | None = None
    timestamp: datetime | None = None
    ttot: datetime | None = None


@dataclass
class Flight:
    """An individual arriving or departing flight tracked through its operational milestones on the Airport CDM Platform.

    Package CDMCore, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'corresponds to' -> ATCFlightPlan [1]

    Relationship: association 'has status' -> OperationalStatus [1]
    """
    flightId: str | None = None
    callsign: str | None = None
    isRegulated: bool | None = None
    operationalStatus: OperationalStatus | None = None
    eobt: datetime | None = None
    tobt: datetime | None = None
    tsat: datetime | None = None
    ttot: datetime | None = None
    ctot: datetime | None = None
    eldt: datetime | None = None
    eibt: datetime | None = None
    aldt: datetime | None = None
    aibt: datetime | None = None
    acgt: datetime | None = None
    asbt: datetime | None = None
    ardt: datetime | None = None
    asrt: datetime | None = None
    asat: datetime | None = None
    aobt: datetime | None = None
    atot: datetime | None = None
    exot: timedelta | None = None
    exit: timedelta | None = None
    aircraftType: str | None = None
    aircraftRegistration: str | None = None

    def updateEldt(self, source: str) -> None:
        """Updates the Estimated Landing Time based on FUM messages, ATOT plus estimated elapsed time, or radar detections."""
        raise NotImplementedError

    def updateTobt(self, newTobt: datetime) -> None:
        """Records a new or updated Target Off-Block Time entered by the AO/GH or calculated automatically by the platform."""
        raise NotImplementedError

    def computeTtot(self) -> datetime:
        """Calculates TTOT as EIBT+MTTT+EXOT, or TOBT+EXOT if a manual TOBT is available and later, or EOBT+EXOT if EOBT is later than EIBT+MTTT."""
        raise NotImplementedError

    def checkTtotTolerance(self, previousTtot: datetime) -> bool:
        """Checks whether the TTOT has changed by more than the agreed tolerance, triggering notification to Network Operations."""
        raise NotImplementedError


@dataclass
class FumMessage:
    """A Flight Update Message sent by Network Operations to provide updates on the actual progress of an inbound flight.

    Package Messaging, stereotype entity, milestones [2, 3].

    Relationship: dependency 'updates ELDT of' -> Flight [1]
    """
    timestamp: datetime | None = None
    updatedEldt: datetime | None = None


@dataclass
class GroundHandler:
    """The ground handling company that manages turn-round operations and reports actual times such as ACGT, ASBT and ARDT.

    Package Actors, stereotype entity, milestones [3, 4, 5, 6, 7, 8, 9, 11, 12].

    Relationship: association 'handles / provides estimates for' -> Flight [*]
    """
    handlerId: str | None = None
    name: str | None = None

    def reportReady(self, flight: Flight, ardt: datetime) -> None:
        """Reports the Actual Ready Time confirming the aircraft is ready for start-up/push-back."""
        raise NotImplementedError


@dataclass
class MilestoneProcess:
    """A per-milestone process that checks consistency/feasibility of estimates against the ATC Flight Plan and triggers messaging to Network Operations when tolerances are exceeded.

    Package Control, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: dependency 'issues' -> DpiMessage [0..*]

    Relationship: dependency 'checks/updates' -> Flight [1]
    """
    milestoneNumber: int | None = None
    triggerCondition: str | None = None
    tolerance: timedelta | None = None

    def execute(self, flight: Flight) -> None:
        """Performs the milestone-specific consistency/feasibility check and issues the associated DPI or FUM message and status change if required."""
        raise NotImplementedError


@dataclass
class NetworkOperations:
    """The network management function (Network Operations / ETFMS) that issues CTOT for regulated flights and receives DPI and FUM messages.

    Package Actors, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 10, 15].

    Relationship: association 'issues CTOT to' -> Flight [*]

    Relationship: dependency 'sends' -> FumMessage [0..*]
    """
    eventId: str | None = None

    def issueCtot(self, flight: Flight) -> datetime:
        """Issues the Calculated Take-Off Time to relevant ATS units and the departure aerodrome at EOBT-2hr for regulated flights."""
        raise NotImplementedError

    def receiveDpi(self, message: DpiMessage) -> None:
        """Receives a DPI message updating the flight's estimated or actual take-off time."""
        raise NotImplementedError

    def sendFum(self, flight: Flight) -> FumMessage:
        """Sends a Flight Update Message providing updates on the flight's progress once within 3 hours flying time of destination."""
        raise NotImplementedError


@dataclass
class TurnRound:
    """The turn-round of an aircraft comprising the related arriving and departing flight and the ground handling period between them.

    Package CDMCore, stereotype entity, milestones [1, 4, 6, 7, 8].

    Relationship: aggregation 'comprises arrival and departure flight' -> Flight [2]
    """
    mttt: timedelta | None = None
    estimatedTurnRoundPeriod: timedelta | None = None

    def linkFlights(self, arrival: Flight, departure: Flight) -> None:
        """Associates the arriving and departing flight plans belonging to the same aircraft turn-round."""
        raise NotImplementedError
