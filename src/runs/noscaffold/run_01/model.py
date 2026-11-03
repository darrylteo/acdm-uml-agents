"""Class stubs rendered from runs/noscaffold/run_01/model.json by src/generate/render_code.py; do not edit by hand."""
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
    DEPARTED_TAKE_OFF = "DEPARTED_TAKE_OFF"


@dataclass
class ACARSSystem:
    """The ACARS-equipped aircraft or automated docking/ATC systems that report actual times such as landing, in-block, off-block and take off.

    Package Sensing Systems, stereotype boundary, milestones [6, 7, 15, 16].

    Relationship: dependency 'reports actual times of' -> Flight [*]
    """

    def reportActualTime(self, flight: Flight, eventType: str) -> datetime:
        """Reports an actual time (ALDT/AIBT/AOBT/ATOT) with +/-1 minute accuracy via ACARS ON/IN/OUT/OFF signals."""
        raise NotImplementedError


@dataclass
class ATCFlightPlan:
    """The ICAO flight plan submitted by the Aircraft Operator and distributed by IFPS, used to check consistency and update flight data.

    Package Flight Management, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9].
    """
    flightPlanId: str | None = None
    submissionTime: datetime | None = None
    isRepetitive: bool | None = None
    eobt: datetime | None = None
    aircraftType: str | None = None

    def isConsistentWith(self, slot: AirportSlot, flight: Flight) -> bool:
        """Checks consistency between the ATC Flight Plan, Airport Slot and Airport flight data before the first E-DPI is sent."""
        raise NotImplementedError


@dataclass
class ATCUnit:
    """The Air Traffic Control unit (ACC, Approach, or Tower) responsible for radar detection, TSAT issue, and start-up approval.

    Package External Actors, stereotype entity, milestones [2, 4, 5, 9, 10, 13, 14, 16].

    Relationship: association 'issues TSAT/ASAT to' -> Flight [*]
    """
    name: str | None = None

    def issueTSAT(self, flight: Flight) -> datetime:
        """Issues the Target Start Up Approval Time based on the confirmed TOBT."""
        raise NotImplementedError

    def approveStartUp(self, flight: Flight) -> datetime:
        """Grants start-up/push-back approval (ASAT) to the flight."""
        raise NotImplementedError


@dataclass
class AircraftOperator:
    """The airline operating the flight, responsible for submitting the flight plan and providing TOBT and other estimates.

    Package External Actors, stereotype entity, milestones [1, 3, 6, 7, 8, 9, 10, 11, 12].

    Relationship: dependency 'submits' -> ATCFlightPlan [1..*]

    Relationship: association 'provides TOBT/estimates for' -> Flight [*]
    """
    name: str | None = None

    def submitFlightPlan(self, flightPlan: ATCFlightPlan) -> None:
        """Submits the ICAO flight plan for distribution by IFPS."""
        raise NotImplementedError

    def provideTOBT(self, flight: Flight, tobt: datetime) -> None:
        """Provides or updates the Target Off-Block Time, taking into account the operational situation."""
        raise NotImplementedError


@dataclass
class AircraftTurnRound:
    """The turn-round of one aircraft comprising a related arriving and departing flight pair.

    Package Flight Management, stereotype entity, milestones [1].

    Relationship: composition 'comprises arriving and departing' -> Flight [2]
    """
    turnRoundId: str | None = None
    minimumTurnRoundTime: timedelta | None = None


@dataclass
class AirportCDMPlatform:
    """The central Airport Collaborative Decision Making system that is initiated for each flight, processes information and executes the milestone procedures.

    Package CDM Process, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: aggregation 'manages' -> Flight [*]

    Relationship: composition 'executes' -> MilestoneProcess [16]

    Relationship: dependency 'sends' -> DPIMessage [*]

    Relationship: dependency 'generates' -> MovementMessage [*]
    """

    def initiateFlight(self, flightPlan: ATCFlightPlan) -> Flight:
        """Initiates the Airport CDM Platform for a flight on activation of the ATC Flight Plan, processing all available information."""
        raise NotImplementedError

    def processMilestone(self, milestoneNumber: int, flight: Flight) -> None:
        """Executes the procedures and status updates defined for the given milestone against the flight."""
        raise NotImplementedError

    def notifyPartners(self, flight: Flight, message: str) -> None:
        """Informs all relevant Airport CDM Partners of an actual time or status change (e.g., ASBT, ARDT, ASRT, ASAT, AOBT)."""
        raise NotImplementedError


@dataclass
class AirportSlot:
    """The airport slot programme entry that the ATC Flight Plan must correspond to.

    Package Flight Management, stereotype entity, milestones [1].
    """
    slotId: str | None = None
    scheduledTime: datetime | None = None
    isCoordinatedAirport: bool | None = None


@dataclass
class ConsistencyCheck:
    """The recurring check that verifies the feasibility/consistency of the ATC Flight Plan, TOBT or TTOT at a given milestone before informing Network Operations.

    Package CDM Process, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9].

    Relationship: dependency 'verifies' -> ATCFlightPlan [1]

    Relationship: dependency 'verifies' -> AirportSlot [1]

    Relationship: dependency 'verifies TOBT/TTOT of' -> Flight [1]
    """
    toleranceValue: timedelta | None = None

    def checkConsistency(self, flightPlan: ATCFlightPlan, slot: AirportSlot, flight: Flight) -> bool:
        """Checks consistency between the ATC Flight Plan, Airport Slot and Airport flight data, or between TOBT/TTOT and the ATC Flight Plan at the relevant milestone."""
        raise NotImplementedError


@dataclass
class DPIMessage:
    """A Departure Planning Information message sent to Network Operations to communicate updated take-off time estimates.

    Package Messaging, stereotype entity, milestones [1, 2, 3, 4, 10, 15].

    Relationship: association 'informs' -> NetworkOperations [1]
    """
    messageType: DPIMessageType | None = None
    sentTime: datetime | None = None
    ttot: datetime | None = None


@dataclass
class Flight:
    """An individual flight (arrival or departure leg) tracked through the Airport CDM Platform from flight-plan activation to take off.

    Package Flight Management, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'based on' -> ATCFlightPlan [1]

    Relationship: association 'corresponds to' -> AirportSlot [1]
    """
    flightId: str | None = None
    callSign: str | None = None
    aircraftRegistration: str | None = None
    aircraftType: str | None = None
    departureAerodrome: str | None = None
    destinationAerodrome: str | None = None
    eobt: datetime | None = None
    sobt: datetime | None = None
    tobt: datetime | None = None
    tsat: datetime | None = None
    ctot: datetime | None = None
    etot: datetime | None = None
    ttot: datetime | None = None
    atot: datetime | None = None
    eldt: datetime | None = None
    eibt: datetime | None = None
    aldt: datetime | None = None
    aibt: datetime | None = None
    acgt: datetime | None = None
    ardt: datetime | None = None
    asrt: datetime | None = None
    asat: datetime | None = None
    aobt: datetime | None = None
    exot: timedelta | None = None
    exit: timedelta | None = None
    mttt: timedelta | None = None
    estimatedElapsedTime: timedelta | None = None
    isRegulated: bool | None = None
    operationalStatus: OperationalStatus | None = None

    def computeEIBT(self) -> datetime:
        """Computes EIBT using ELDT (or ALDT) plus the estimated taxi-in time (EXIT)."""
        raise NotImplementedError

    def computeTTOT(self) -> datetime:
        """Calculates TTOT as EIBT+MTTT+EXOT if later than EOBT+EXOT; overridden by TOBT+EXOT when TOBT is manually input."""
        raise NotImplementedError

    def computeELDTFromATOT(self) -> datetime:
        """Calculates ELDT using the ATOT from the outstation and the Estimated Elapsed Time from the FPL."""
        raise NotImplementedError

    def updateOperationalStatus(self, newStatus: OperationalStatus) -> None:
        """Updates the flight's operational status as prescribed by the current milestone."""
        raise NotImplementedError

    def exceedsTTOTTolerance(self, newTTOT: datetime) -> bool:
        """Checks whether a proposed TTOT change exceeds the agreed TTOT tolerance, requiring Network Operations to be informed."""
        raise NotImplementedError


@dataclass
class FlightUpdateMessage:
    """The FUM message sent by Network Operations via ETFMS providing updates on an inbound flight's progress and ELDT.

    Package Messaging, stereotype entity, milestones [2, 3].

    Relationship: association 'updates ELDT of' -> Flight [1]
    """
    sentTime: datetime | None = None
    updatedELDT: datetime | None = None


@dataclass
class GroundHandler:
    """The ground handling agent that, together with the Aircraft Operator, manages the turn-round and provides estimates such as TOBT.

    Package External Actors, stereotype entity, milestones [3, 6, 7, 8, 9, 10, 11, 12].

    Relationship: association 'provides TOBT/estimates for' -> Flight [*]
    """
    name: str | None = None

    def provideTOBT(self, flight: Flight, tobt: datetime) -> None:
        """Provides or updates the Target Off-Block Time based on the estimated turn-round period."""
        raise NotImplementedError


@dataclass
class IFPS:
    """The Integrated Initial Flight Plan Processing System that distributes the ATC Flight Plan to all involved ATC units.

    Package External Actors, stereotype entity, milestones [1].

    Relationship: dependency 'distributes' -> ATCFlightPlan [1..*]
    """

    def distributeFlightPlan(self, flightPlan: ATCFlightPlan) -> None:
        """Distributes the submitted ATC Flight Plan to all involved ATC units, including departure and destination aerodromes."""
        raise NotImplementedError


@dataclass
class MilestoneProcess:
    """One of the sixteen defined milestone procedures, each with a trigger, a consistency check, resulting operational status change and CDM actions.

    Package CDM Process, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'performs' -> ConsistencyCheck [0..1]
    """
    milestoneNumber: int | None = None
    name: str | None = None
    trigger: str | None = None
    resultingStatus: OperationalStatus | None = None

    def execute(self, flight: Flight) -> None:
        """Performs the milestone's consistency check, updates flight estimates, changes operational status and notifies partners/Network Operations as prescribed."""
        raise NotImplementedError


@dataclass
class MovementMessage:
    """The FSA and MVT messages generated on actual take off to inform all relevant Airport CDM Partners.

    Package Messaging, stereotype entity, milestones [16].

    Relationship: association 'reports take off of' -> Flight [1]
    """
    messageType: str | None = None
    sentTime: datetime | None = None


@dataclass
class NetworkOperations:
    """The network management function that issues CTOT, monitors flight progress via ETFMS and receives DPI/FUM messages.

    Package External Actors, stereotype entity, milestones [1, 2, 3, 4, 10, 15].

    Relationship: association 'issues CTOT to' -> Flight [*]

    Relationship: dependency 'sends' -> FlightUpdateMessage [*]
    """
    name: str | None = None

    def issueCTOT(self, flight: Flight) -> datetime:
        """Issues a Calculated Take Off Time to a regulated flight at EOBT-2hr."""
        raise NotImplementedError

    def receiveDPI(self, message: DPIMessage) -> None:
        """Receives a DPI message informing it of an updated take off time estimate."""
        raise NotImplementedError


@dataclass
class RadarSystem:
    """The ATC radar system that detects a flight by its assigned SSR code crossing FIR/TMA boundaries or entering Final Approach.

    Package Sensing Systems, stereotype boundary, milestones [4, 5, 6].

    Relationship: dependency 'detects' -> Flight [*]
    """

    def detectFlight(self, flight: Flight) -> None:
        """Detects the flight crossing the FIR/ATC boundary, entering the TMA, or entering Final Approach, or landing."""
        raise NotImplementedError
