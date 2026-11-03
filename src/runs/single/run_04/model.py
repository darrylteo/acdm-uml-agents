"""Class stubs rendered from runs/single/run_04/model.json by src/generate/render_code.py; do not edit by hand."""
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


class TimeQuantityType(Enum):
    EOBT = "EOBT"
    TOBT = "TOBT"
    AOBT = "AOBT"
    SOBT = "SOBT"
    ELDT = "ELDT"
    EIBT = "EIBT"
    ALDT = "ALDT"
    AIBT = "AIBT"
    ETOT = "ETOT"
    TTOT = "TTOT"
    CTOT = "CTOT"
    ATOT = "ATOT"
    ASBT = "ASBT"
    ARDT = "ARDT"
    ASRT = "ASRT"
    ASAT = "ASAT"
    TSAT = "TSAT"
    ACGT = "ACGT"
    ETTT = "ETTT"
    EXOT = "EXOT"
    EXIT = "EXIT"
    MTTT = "MTTT"


@dataclass
class ACARS:
    """The ACARS aircraft reporting system that can provide actual times such as ATOT, ALDT, AIBT, and AOBT for equipped aircraft.

    Package Systems, stereotype boundary, milestones [3, 6, 7, 15, 16].

    Relationship: dependency 'provides actual value for' -> TimeQuantity
    """

    def reportActualTime(self, event: str) -> datetime:
        """Reports an actual time (ACARS=ON for landing, IN for in-block, OUT for off-block, OFF for take-off)."""
        raise NotImplementedError


@dataclass
class ATCFlightPlan:
    """The ICAO ATC Flight Plan submitted by the Aircraft Operator and distributed by the IFPS to all involved ATC units.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9].
    """
    departureAerodrome: str | None = None
    destinationAerodrome: str | None = None
    sobt: datetime | None = None
    estimatedElapsedTime: timedelta | None = None
    aircraftRegistration: str | None = None


@dataclass
class ATCSystem:
    """The ATC ground system (e.g. A-SMGCS, Tower FDPS) that detects milestones and calculates taxi time estimates.

    Package Systems, stereotype boundary, milestones [4, 5, 6, 7, 9, 15, 16].

    Relationship: dependency 'calculates EXOT for' -> TimeQuantity
    """
    accuracy: str | None = None

    def calculateEXOT(self, trafficLoad: str, gateLocation: str, runwayInUse: str, holdingWaitTime: timedelta) -> timedelta:
        """Following receipt of TOBT, the ATC system calculates and provides the Estimated Taxi-Out Time (EXOT) based on predicted traffic load, gate/stand location, runway in use, and waiting period at the Holding Position."""
        raise NotImplementedError


@dataclass
class Stakeholder:
    """A party that takes part in the CDM process and originates or receives flight or timing information.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    name: str | None = None
    role: str | None = None


@dataclass
class AirTrafficControl(Stakeholder):
    """ATC, including Area Control Centre, Approach Control, and Tower units, which issues TSAT, ASAT, and detects milestones via radar.

    Package Stakeholders, stereotype entity, milestones [1, 4, 5, 9, 10, 12, 13, 14, 15, 16].
    """
    pass


@dataclass
class Aircraft:
    """The physical aircraft operating a flight, identified by registration and type, which may be updated from the flight plan.

    Package Flights, stereotype entity, milestones [1].
    """
    registration: str | None = None
    type: str | None = None


@dataclass
class AircraftOperator(Stakeholder):
    """The Aircraft Operator (AO), who submits the ATC Flight Plan and provides TOBT, ready status, and other flight information.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13].

    Relationship: association 'operates' -> Flight [1..*]
    """
    pass


@dataclass
class MilestoneEvent:
    """One of the sixteen defined events in the CDM process, each with its own trigger, timing rule, effect, and procedure.

    Package Milestones, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: dependency 'applies to' -> Flight
    """
    milestoneNumber: int | None = None
    name: str | None = None
    definition: str | None = None
    trigger: str | None = None
    timingRule: str | None = None
    effect: str | None = None
    operationalStatusChange: FlightOperationalStatus | None = None


@dataclass
class AircraftReadyMilestone(MilestoneEvent):
    """Milestone 12: the time all doors are closed, boarding bridge removed, push-back vehicle connected, ready to taxi (ARDT).

    Package Milestones, stereotype control, milestones [12].
    """

    def informReady(self) -> None:
        """Informs all relevant Airport CDM Partners of Actual Ready Time (ARDT) or Ready Status (RDY), confirming the flight follows the indicated TOBT."""
        raise NotImplementedError

    def alertIfNoReadyStatus(self) -> None:
        """At TOBT plus tolerance, informs the AO/GH that TOBT has passed and no ready status message has been received yet."""
        raise NotImplementedError


@dataclass
class AirportCDMPlatform:
    """The Airport CDM Platform, initiated for each flight, which processes available information and performs the CDM operation actions (ACISP) recorded at each milestone.

    Package Systems, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 16].

    Relationship: association 'is initiated for and processes' -> Flight [1..*]

    Relationship: aggregation 'executes procedure of' -> MilestoneEvent [1..*]
    """
    status: str | None = None

    def initiateForFlight(self, flight: Flight) -> None:
        """Initiates the Airport CDM Platform for the flight and processes all available information (Milestone 1)."""
        raise NotImplementedError

    def updateArrivalAndDepartureEstimates(self, flight: Flight) -> None:
        """ELDT and EIBT updated for an arrival, EOBT and ETOT updated for a departure (Milestone 1 ACISP)."""
        raise NotImplementedError

    def markRegulated(self, flight: Flight) -> None:
        """Updates ETOT/TTOT/CTOT and marks appropriate fields as REGULATED (Milestone 2 ACISP)."""
        raise NotImplementedError

    def updateTimingsAfterOutstationTakeOff(self, flight: Flight) -> None:
        """ELDT, EIBT, TOBT and TTOT updated after take off from outstation (Milestone 3 ACISP)."""
        raise NotImplementedError

    def updateTimingsAfterRadarOrApproach(self, flight: Flight) -> None:
        """ELDT, EIBT, TOBT and TTOT updated at Local Radar Update and Final Approach (Milestones 4 and 5 ACISP)."""
        raise NotImplementedError

    def changeELDTToALDT(self, flight: Flight) -> None:
        """ELDT changes to ALDT and EIBT, TOBT, TTOT updated on landing (Milestone 6 ACISP)."""
        raise NotImplementedError

    def changeEIBTToAIBT(self, flight: Flight) -> None:
        """EIBT changes to AIBT and TOBT, TTOT updated on in-block (Milestone 7 ACISP)."""
        raise NotImplementedError

    def updateAfterGroundHandlingStart(self, flight: Flight) -> None:
        """ETTT/TOBT and TTOT updated when ground handling starts (Milestone 8 ACISP)."""
        raise NotImplementedError

    def updateTTOTAfterTSAT(self, flight: Flight) -> None:
        """TTOT updated after TSAT is issued (Milestone 10 ACISP)."""
        raise NotImplementedError

    def recordAOBT(self, flight: Flight, aobt: datetime) -> None:
        """Records AOBT on off-block (Milestone 15 ACISP)."""
        raise NotImplementedError

    def recordATOT(self, flight: Flight, atot: datetime) -> None:
        """Records ATOT on take off (Milestone 16 ACISP)."""
        raise NotImplementedError

    def commenceDPIProcess(self, flight: Flight) -> None:
        """The DPI process commences the correct messaging with Network Operations, if implemented (Milestone 1)."""
        raise NotImplementedError


@dataclass
class AirportSlot:
    """The airport slot allocated to a flight, against which the ATC Flight Plan and airport flight data must be consistent.

    Package Flights, stereotype entity, milestones [1].
    """
    slotTime: datetime | None = None
    coordinated: bool | None = None


@dataclass
class BoardingStartsMilestone(MilestoneEvent):
    """Milestone 11: the gate is opened for passengers to physically start boarding.

    Package Milestones, stereotype control, milestones [11].
    """

    def informASBT(self) -> None:
        """Informs all relevant Airport CDM Partners of the Actual Start Boarding Time (ASBT) when it occurs."""
        raise NotImplementedError

    def checkBoardingStatus(self) -> None:
        """At a certain time before TOBT (local variable, e.g. by aircraft type) checks the boarding status and informs the AO/GH in case TOBT needs to be updated."""
        raise NotImplementedError


@dataclass
class DPIMessage:
    """A Departure Planning Information message exchanged with Network Operations at defined points in the process.

    Package Messages, stereotype boundary, milestones [1, 2, 3, 10, 15].

    Relationship: association 'is sent to' -> NetworkOperations [1]
    """
    type: DPIType | None = None
    sentTo: str | None = None
    timestamp: datetime | None = None


@dataclass
class EOBTMinus2HourMilestone(MilestoneEvent):
    """Milestone 2: at EOBT-2hr most flights are known and all regulated flights receive a CTOT from Network Operations.

    Package Milestones, stereotype control, milestones [2].
    """

    def checkEstimatesConsistency(self) -> bool:
        """Checks whether AO/GH flight estimates are consistent with the ATC Flight Plan at EOBT-2hrs."""
        raise NotImplementedError

    def sendFirstTDPI(self) -> None:
        """Informs Network Operations at EOBT-2hrs through the first T-DPI message of the updated take-off time estimate."""
        raise NotImplementedError


@dataclass
class ETFMS:
    """The system used by Network Operations to monitor the progress of a flight within 3 hours flying time of the destination airport.

    Package Systems, stereotype boundary, milestones [3].

    Relationship: dependency 'is basis for' -> FlightUpdateMessage
    """

    def monitorFlightProgress(self, flight: Flight) -> None:
        """Monitors progress of the flight and provides the basis for sending Flight Update Messages (FUM)."""
        raise NotImplementedError


@dataclass
class FinalApproachMilestone(MilestoneEvent):
    """Milestone 5: the flight enters the Final Approach phase at the destination airport, usually 2 to 5 minutes from landing.

    Package Milestones, stereotype control, milestones [5].
    """

    def commenceTOBTProcess(self) -> None:
        """Commences the TOBT process and checks whether the AO/GH TOBT is consistent with the ATC Flight Plan."""
        raise NotImplementedError

    def informNetworkOperationsIfTTOTExceedsTolerance(self) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class FinalTOBTConfirmationMilestone(MilestoneEvent):
    """Milestone 9: the time the Aircraft Operator or Ground Handler provides its most accurate TOBT, taking into account the operational situation, t minutes before EOBT.

    Package Milestones, stereotype control, milestones [9].
    """

    def confirmTOBT(self) -> None:
        """Performed at a predefined local time to confirm TOBT prior to TSAT issue and verify feasibility of the ATC Flight Plan estimates; no need to confirm an existing TOBT if it has been manually modified before."""
        raise NotImplementedError

    def checkTOBTConsistency(self) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan; informs Network Operations when TTOT changes by more than the agreed tolerance."""
        raise NotImplementedError


@dataclass
class Flight:
    """An arriving or departing flight tracked through the CDM process from ATC Flight Plan activation to take-off.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'is described by' -> ATCFlightPlan [1..2]

    Relationship: association 'corresponds to' -> AirportSlot [0..1]

    Relationship: association 'operated by aircraft' -> Aircraft [1]

    Relationship: composition 'carries successive values of' -> TimeQuantity [1..*]
    """
    flightId: str | None = None
    direction: str | None = None
    operationalStatus: FlightOperationalStatus | None = None
    regulated: bool | None = None

    def isReadyWithinTolerance(self) -> bool:
        """The flight is ready not later than 15 minutes after the planned EOBT (Milestone 1 effect)."""
        raise NotImplementedError


@dataclass
class FlightPlanActivationMilestone(MilestoneEvent):
    """Milestone 1: the ICAO flight plan is submitted to ATC and the Airport CDM Platform is initiated for the flight.

    Package Milestones, stereotype control, milestones [1].
    """

    def checkConsistency(self, flightPlan: ATCFlightPlan, airportSlot: AirportSlot) -> bool:
        """Checks consistency between the ATC Flight Plan, Airport Slot, and Airport flight data before the first E-DPI is sent."""
        raise NotImplementedError

    def sendEDPI(self) -> None:
        """Confirms the flight to Network Operations with consistent SOBT, aircraft registration, and first destination data; the E-DPI should not be sent if no or inconsistent information is provided."""
        raise NotImplementedError


@dataclass
class FlightUpdateMessage:
    """A Flight Update Message (FUM) sent by Network Operations that provides updates of the flight's progress and is used to update ELDT.

    Package Messages, stereotype boundary, milestones [2, 3].

    Relationship: association 'is sent by' -> NetworkOperations [1]

    Relationship: dependency 'updates ELDT of' -> Flight
    """
    updatedELDT: datetime | None = None


@dataclass
class GroundHandler(Stakeholder):
    """The Ground Handler (GH), who together with the Aircraft Operator provides TOBT, ready status, and manages the turn-round process.

    Package Stakeholders, stereotype entity, milestones [2, 3, 4, 5, 6, 7, 8, 9, 11, 12].

    Relationship: association 'handles turn-round of' -> Flight [1..*]
    """
    pass


@dataclass
class GroundHandlingStartedMilestone(MilestoneEvent):
    """Milestone 8: the commencement of ground handling operations (ACGT), specific to first flights of the day or long-parked aircraft.

    Package Milestones, stereotype control, milestones [8].
    """

    def checkTOBTConsistency(self) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT or ATC Flight Plan."""
        raise NotImplementedError

    def informNetworkOperationsIfTTOTExceedsTolerance(self) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class IFPS:
    """The Integrated Initial Flight Plan Processing System that distributes the ATC Flight Plan to all involved ATC units.

    Package Systems, stereotype boundary, milestones [1].

    Relationship: dependency 'distributes' -> ATCFlightPlan
    """

    def distributeFlightPlan(self, flightPlan: ATCFlightPlan) -> None:
        """Distributes the submitted ATC Flight Plan to all involved ATC units, including departure and destination aerodromes."""
        raise NotImplementedError


@dataclass
class InBlockMilestone(MilestoneEvent):
    """Milestone 7: AIBT, the time an aircraft arrives in-blocks; ACGT is considered to commence at AIBT.

    Package Milestones, stereotype control, milestones [7].
    """

    def checkTOBTConsistency(self) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT or ATC Flight Plan."""
        raise NotImplementedError

    def informNetworkOperationsIfTTOTExceedsTolerance(self) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class LandedMilestone(MilestoneEvent):
    """Milestone 6: ALDT, the time an aircraft touches down on a runway.

    Package Milestones, stereotype control, milestones [6].
    """

    def checkTOBTConsistency(self) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT or ATC Flight Plan."""
        raise NotImplementedError

    def informNetworkOperationsIfTTOTExceedsTolerance(self) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class LocalRadarUpdateMilestone(MilestoneEvent):
    """Milestone 4: the flight enters the FIR or local airspace of the destination airport, detected by radar via the assigned SSR code.

    Package Milestones, stereotype control, milestones [4].
    """

    def commenceTOBTProcess(self) -> None:
        """Commences the TOBT process and checks whether the AO/GH TOBT is consistent with the ATC Flight Plan."""
        raise NotImplementedError

    def informNetworkOperationsIfTTOTExceedsTolerance(self) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class MovementMessage:
    """A movement (MVT) message sent on actual take off, along with an FSA message and an airborne message.

    Package Messages, stereotype boundary, milestones [16].
    """
    actualTakeOffTime: datetime | None = None


@dataclass
class NetworkOperations(Stakeholder):
    """Network Operations, which issues CTOT, monitors flight progress via ETFMS, and receives DPI messages.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 9, 10, 15].

    Relationship: association 'monitors and issues CTOT to' -> Flight [1..*]
    """
    pass


@dataclass
class OffBlockMilestone(MilestoneEvent):
    """Milestone 15: AOBT, the time an aircraft pushes back/vacates the parking position.

    Package Milestones, stereotype control, milestones [15].

    Relationship: dependency 'triggers A-DPI' -> DPIMessage
    """

    def informAOBT(self) -> None:
        """Informs all relevant Airport CDM Partners of Actual Off-Block Time (AOBT) when it occurs; AOBT always triggers an A-DPI message to Network Operations, or at a defined time prior to TTOT in the case of remote holding."""
        raise NotImplementedError

    def checkTTOTAfterAOBT(self) -> bool:
        """After the first A-DPI is sent, checks TTOT updates against the TTOT tolerance before Network Operations is informed, with a new A-DPI, of the updated TTOT."""
        raise NotImplementedError


@dataclass
class Pilot(Stakeholder):
    """The flight crew who request start-up and coordinate with the Ground Handler around TSAT.

    Package Stakeholders, stereotype entity, milestones [12, 13, 14].
    """
    pass


@dataclass
class RadarSystem:
    """The radar system associated with an airport that detects a flight based on its assigned SSR code.

    Package Systems, stereotype boundary, milestones [4, 5].

    Relationship: dependency 'detects' -> Flight
    """

    def detectFlight(self, ssrCode: str) -> bool:
        """Detects a flight based upon the assigned SSR code when it crosses a defined FIR/ATC boundary, range/position, or passes/leaves a predetermined level."""
        raise NotImplementedError


@dataclass
class RepetitiveFlightPlan(ATCFlightPlan):
    """A repetitive flight plan (RFPL), a flight plan covering daily or weekly flights, submitted in some cases instead of a one-off flight plan.

    Package Flights, stereotype entity, milestones [1].
    """
    frequency: str | None = None


@dataclass
class StartUpApprovedMilestone(MilestoneEvent):
    """Milestone 14: ASAT, the time an aircraft receives its start-up approval from ATC.

    Package Milestones, stereotype control, milestones [14].
    """

    def informASAT(self) -> None:
        """Informs all relevant Airport CDM Partners of Actual Start-up Approval Time (ASAT) when it occurs, indicating start-up/push-back clearance."""
        raise NotImplementedError

    def checkASATAgainstTSAT(self) -> bool:
        """Checks if ASAT is in accordance with TSAT; if start-up approval is not granted at TSAT plus tolerance, all relevant partners are informed and the flight is re-sequenced."""
        raise NotImplementedError


@dataclass
class StartUpRequestedMilestone(MilestoneEvent):
    """Milestone 13: the time start-up is requested by the pilot to ATC (ASRT).

    Package Milestones, stereotype control, milestones [13].
    """

    def informASRT(self) -> None:
        """Informs all relevant Airport CDM Partners of Actual Start-up Request Time (ASRT) when it occurs."""
        raise NotImplementedError

    def alertIfNoStartUpRequested(self) -> None:
        """If no start-up request is made by TSAT plus the locally agreed tolerance window, informs the AO/GH that no start-up has been requested and that TOBT should be updated."""
        raise NotImplementedError


@dataclass
class TSATIssuedMilestone(MilestoneEvent):
    """Milestone 10: the time ATC issues the Target Start Up Approval Time (TSAT), t minutes before EOBT.

    Package Milestones, stereotype control, milestones [10].
    """

    def informPartnersOfTSAT(self) -> None:
        """Informs all relevant partners of the TSAT allocated to the flight; Network Operations is informed by a T-DPI-s for non-regulated flights; no check is performed for this step."""
        raise NotImplementedError

    def checkTOBTUpdateCount(self) -> bool:
        """Checks whether the number of TOBT updates after TSAT has been issued exceeds a locally defined tolerance; if exceeded, the TOBT input is processed according to local procedure."""
        raise NotImplementedError


@dataclass
class TakeOffFromOutstationMilestone(MilestoneEvent):
    """Milestone 3: the ATOT from the outstation (ADEP) is provided to Network Operations and the Aircraft Operator.

    Package Milestones, stereotype control, milestones [3].
    """

    def checkLandingEstimateConsistency(self) -> bool:
        """Checks whether AO/GH estimated landing times after take off from outstation are consistent with the outbound ATC Flight Plan."""
        raise NotImplementedError

    def sendTDPIt(self) -> None:
        """Informs Network Operations about updated take off time estimates using a T-DPI-t message, respecting a 5-minute TTOT tolerance."""
        raise NotImplementedError


@dataclass
class TakeOffMilestone(MilestoneEvent):
    """Milestone 16: ATOT, the time an aircraft takes off from the runway.

    Package Milestones, stereotype control, milestones [16].

    Relationship: dependency 'triggers sending of' -> MovementMessage
    """

    def informActualTakeOff(self) -> None:
        """Informs all relevant Airport CDM Partners about the actual take off."""
        raise NotImplementedError

    def generateAirborneMessage(self) -> None:
        """Generates an airborne message and removes the flight from the departure sequence; FSA and MVT messages are sent."""
        raise NotImplementedError


@dataclass
class TimeQuantity:
    """A named time quantity (prefixed Scheduled, Estimated, Target, Actual, or Calculated, for an event such as Off-Block, In-Block, Landing, or Take-Off) that describes a flight's progress, with its origin, accuracy, and tolerance; every successive value is kept, an update appends rather than overwrites.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    type: TimeQuantityType | None = None
    value: datetime | None = None
    originator: str | None = None
    accuracy: str | None = None
    tolerance: str | None = None
    recordedAt: datetime | None = None

    def calculateTTOT(self, eibt: datetime, mttt: timedelta, exot: timedelta, eobt: datetime, tobt: datetime) -> datetime:
        """Calculation basis for TTOT takes into account EIBT+MTTT+EXOT if later than EOBT+EXOT; if TOBT is manually input it overrides EIBT+MTTT, so TTOT equals TOBT+EXOT."""
        raise NotImplementedError

    def calculateELDT(self, atot: datetime, estimatedElapsedTime: timedelta) -> datetime:
        """ELDT is calculated using ATOT and the Estimated Elapsed Time on the FPL."""
        raise NotImplementedError

    def calculateEIBT(self, eldt: datetime, exit: timedelta) -> datetime:
        """EIBT is computed using ELDT (or ALDT) and the estimated/actual taxi-in time (EXIT)."""
        raise NotImplementedError

    def exceedsTolerance(self, newValue: datetime) -> bool:
        """Checks whether a new value changes by more than the agreed tolerance, triggering notification of Network Operations or Airport CDM Partners."""
        raise NotImplementedError


@dataclass
class TurnRound:
    """The turn-round of an aircraft, normally comprising a related arriving flight and departing flight.

    Package Flights, stereotype entity, milestones [1].

    Relationship: aggregation 'comprises arrival and departure flight' -> Flight [0..2]
    """
    turnRoundPeriod: timedelta | None = None
