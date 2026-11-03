"""Class stubs rendered from runs/noscaffold/run_02/model.json by src/generate/render_code.py; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from enum import Enum


class DPIMessageType(Enum):
    E_DPI = "E_DPI"
    T_DPI = "T_DPI"
    T_DPI_T = "T_DPI_t"
    T_DPI_S = "T_DPI_s"
    A_DPI = "A_DPI"


class OperationalStatus(Enum):
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
    DEPARTED = "DEPARTED"


@dataclass
class ATCUnit:
    """An air traffic control unit (Area Control Centre, Approach Control, Tower) that receives the flight plan, detects the flight by radar, and issues TSAT/start-up approval.

    Package Stakeholders, stereotype entity, milestones [1, 4, 5, 9, 10, 13, 14, 16].

    Relationship: association 'receives' -> FlightPlan [1]

    Relationship: association 'detects / issues TSAT for' -> Flight [*]
    """
    unitId: str | None = None
    unitType: str | None = None


@dataclass
class AircraftOperator:
    """The airline responsible for submitting the ATC Flight Plan and providing TOBT, ready and boarding information for its flights.

    Package Stakeholders, stereotype entity, milestones [1, 3, 6, 7, 8, 9, 11, 12].

    Relationship: dependency 'submits' -> FlightPlan [1..*]

    Relationship: association 'operates' -> Flight [*]
    """
    operatorId: str | None = None


@dataclass
class AirportCDMPlatform:
    """The central platform that is initiated for each flight, processes available information, performs consistency checks, records milestones, and triggers messaging to Network Operations.

    Package CDMProcess, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'manages' -> Flight [*]

    Relationship: dependency 'records' -> Milestone [*]

    Relationship: association 'sends' -> DPIMessage [*]
    """

    def checkConsistency(self, flight: Flight) -> bool:
        """Verifies consistency between the ATC Flight Plan, Airport Slot and Airport flight data before the first E-DPI is sent (M1)."""
        raise NotImplementedError

    def updateELDT(self, flight: Flight) -> None:
        """Updates ELDT based on FUM messages, ATOT plus elapsed time, or radar detection at FIR/Final Approach/Landing (M2-6)."""
        raise NotImplementedError

    def calculateTTOT(self, flight: Flight) -> datetime:
        """Calculates TTOT as EIBT+MTTT+EXOT, or EOBT+EXOT if later, or TOBT+EXOT if TOBT is manually input (M2,3)."""
        raise NotImplementedError

    def recordMilestone(self, flight: Flight, milestoneNumber: int) -> None:
        """Records the occurrence of a milestone against a flight and updates its operational status."""
        raise NotImplementedError

    def triggerDPI(self, flight: Flight, type: DPIMessageType) -> None:
        """Sends the appropriate DPI message to Network Operations when TTOT changes beyond the agreed tolerance."""
        raise NotImplementedError

    def checkTOBTUpdateCount(self, flight: Flight) -> bool:
        """Checks whether the number of TOBT updates after TSAT issue exceeds a locally defined threshold (M10)."""
        raise NotImplementedError


@dataclass
class AirportSlot:
    """The airport slot allocated to the flight, against which the ATC Flight Plan must be consistent, from the airport slot programme.

    Package FlightData, stereotype entity, milestones [1].
    """
    slotId: str | None = None
    scheduledTime: datetime | None = None


@dataclass
class DPIMessage:
    """A Departure Planning Information message (E-DPI, T-DPI, T-DPI-t, T-DPI-s, A-DPI) sent from the Airport CDM Platform to Network Operations with updated flight time estimates.

    Package Messaging, stereotype entity, milestones [1, 2, 3, 4, 10, 15].

    Relationship: association 'informs' -> NetworkOperations [1]
    """
    messageType: DPIMessageType | None = None
    sentTime: datetime | None = None


@dataclass
class Flight:
    """A single flight (arrival or departure leg) tracked through the CDM milestone process with all its estimated and actual times.

    Package FlightData, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'based on' -> FlightPlan [1]

    Relationship: association 'matched to' -> AirportSlot [1]

    Relationship: composition 'progresses through' -> Milestone [1..*]
    """
    flightId: str | None = None
    aircraftRegistration: str | None = None
    aircraftType: str | None = None
    isRegulated: bool | None = None
    operationalStatus: OperationalStatus | None = None
    eobt: datetime | None = None
    sobt: datetime | None = None
    tobt: datetime | None = None
    tsat: datetime | None = None
    ctot: datetime | None = None
    etot: datetime | None = None
    ttot: datetime | None = None
    exot: timedelta | None = None
    exit: timedelta | None = None
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


@dataclass
class FlightPlan:
    """The ICAO ATC Flight Plan submitted by the Aircraft Operator and distributed by IFPS, which the CDM platform checks for consistency against the airport slot and flight data.

    Package FlightData, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9].

    Relationship: association 'corresponds to' -> AirportSlot [0..1]
    """
    planId: str | None = None
    eobt: datetime | None = None
    firstDestination: str | None = None
    estimatedElapsedTime: timedelta | None = None
    isRepetitive: bool | None = None


@dataclass
class FlightUpdateMessage:
    """A Flight Update Message (FUM) sent by Network Operations providing progress updates for an inbound flight within 3 hours flying time of destination.

    Package Messaging, stereotype entity, milestones [2, 3].

    Relationship: dependency 'updates ELDT of' -> Flight [1]
    """
    sentTime: datetime | None = None


@dataclass
class GroundHandler:
    """The ground handling agent that manages the turn-round process and provides estimates such as TOBT, ARDT, ASBT, and ACGT.

    Package Stakeholders, stereotype entity, milestones [3, 6, 7, 8, 9, 11, 12].

    Relationship: association 'provides estimates for' -> Flight [*]

    Relationship: association 'manages' -> TurnRound [*]
    """
    handlerId: str | None = None


@dataclass
class IFPS:
    """The Integrated Initial Flight Plan Processing System that distributes the submitted ATC Flight Plan to all involved ATC units.

    Package Stakeholders, stereotype entity, milestones [1].

    Relationship: dependency 'distributes' -> FlightPlan [1..*]
    """
    pass


@dataclass
class Milestone:
    """One of the 16 defined CDM milestone events in a flight's life-cycle, each with a definition, timing, trigger, and resulting operational status change.

    Package CDMProcess, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    milestoneNumber: int | None = None
    name: str | None = None
    timestamp: datetime | None = None
    triggeredBy: str | None = None
    resultingStatus: OperationalStatus | None = None


@dataclass
class NetworkOperations:
    """The network management function that issues CTOT for regulated flights, monitors flight progress via ETFMS, and receives DPI/FUM messages.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 10, 15].

    Relationship: association 'sends' -> FlightUpdateMessage [*]

    Relationship: association 'issues CTOT to' -> Flight [*]
    """

    def issueCTOT(self, flight: Flight) -> datetime:
        """Issues a Calculated Take-Off Time to a regulated flight at EOBT-2h."""
        raise NotImplementedError


@dataclass
class TurnRound:
    """The turn-round linking an arriving flight and its related departing flight at a coordinated or non-coordinated airport.

    Package FlightData, stereotype entity, milestones [1, 6, 7, 8].

    Relationship: aggregation 'arrival flight' -> Flight [1]

    Relationship: aggregation 'departure flight' -> Flight [1]
    """
    mttt: timedelta | None = None
