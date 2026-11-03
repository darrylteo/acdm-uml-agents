"""Class stubs rendered from runs/multi/run_01/model.json by src/generate/render_code.py; do not edit by hand."""
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


class DurationType(Enum):
    TAXI_OUT_TIME = "TaxiOutTime"
    TAXI_IN_TIME = "TaxiInTime"
    MINIMUM_TURN_ROUND_TIME = "MinimumTurnRoundTime"
    ESTIMATED_TURN_ROUND_TIME = "EstimatedTurnRoundTime"


class FlightOperationalStatus(Enum):
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
    DEPARTED = "DEPARTED"


class NotificationType(Enum):
    ASBT = "ASBT"
    ARDT = "ARDT"
    ASRT = "ASRT"
    ASAT = "ASAT"
    AOBT = "AOBT"
    ATOT = "ATOT"
    TSAT = "TSAT"
    RDY = "RDY"
    FSA = "FSA"
    MVT = "MVT"
    AIRBORNE = "AIRBORNE"


class TimeEvent(Enum):
    OFF_BLOCK = "OffBlock"
    IN_BLOCK = "InBlock"
    LANDING = "Landing"
    TAKE_OFF = "TakeOff"
    START_UP_APPROVAL = "StartUpApproval"
    BOARDING = "Boarding"
    READY = "Ready"
    START_UP_REQUEST = "StartUpRequest"
    GROUND_HANDLING_START = "GroundHandlingStart"


class TimePrefix(Enum):
    SCHEDULED = "Scheduled"
    ESTIMATED = "Estimated"
    TARGET = "Target"
    ACTUAL = "Actual"
    CALCULATED = "Calculated"


@dataclass
class ACARS:
    """The aircraft reporting system that provides actual times such as ALDT, AIBT, AOBT and ATOT from equipped aircraft.

    Package Systems, stereotype boundary, milestones [6, 7, 15, 16].

    Relationship: dependency 'provides' -> TimeQuantity
    """

    def provideActualTime(self, flight: Flight, event: TimeEvent) -> TimeQuantity:
        """ACARS equipped aircraft provide actual times such as ALDT (ACARS=ON), AIBT (ACARS=IN), AOBT (ACARS=OUT) and ATOT (ACARS=OFF), available with an accuracy of +/- 1 minute (milestones 6, 7, 15, 16)."""
        raise NotImplementedError


@dataclass
class ATCSystem:
    """The ATC/radar system (including A-SMGCS and Tower FDPS) that detects flight position and provides milestone times such as ELDT, ALDT, AIBT, AOBT and ATOT.

    Package Systems, stereotype boundary, milestones [4, 5, 6, 7, 9, 15, 16].

    Relationship: dependency 'provides' -> TimeQuantity
    """

    def detectMilestoneEvent(self, flight: Flight, event: TimeEvent) -> TimeQuantity:
        """The ATC system (including A-SMGCS and Tower FDPS) or radar detects a flight based upon the assigned SSR code when it crosses a defined FIR/ATC boundary, range/position, or level, providing milestone times with an accuracy equal to that of the ATC system (milestones 4, 5, 6, 9, 15, 16)."""
        raise NotImplementedError


@dataclass
class CDMPartner:
    """A generalization of the parties that take part in the Airport CDM process and originate or receive its information.

    Package Stakeholders, stereotype entity, milestones [1, 10, 11, 12, 13, 14, 15, 16].
    """
    name: str | None = None


@dataclass
class AirTrafficControlUnit(CDMPartner):
    """The ATC unit (tower, approach, or area control centre) that detects flight progress, issues TSAT/ASAT and manages the pre-departure sequence.

    Package Stakeholders, stereotype entity, milestones [1, 4, 5, 9, 10, 13, 14, 16].

    Relationship: association 'confirms TSAT to' -> FlightCrew [1]

    Relationship: association 'controls' -> Flight [*]
    """

    def issueTSAT(self, flight: Flight, offsetMinutes: int) -> TimeQuantity:
        """ATC issues the Target Start Up Approval Time (TSAT) t-minutes before EOBT, where t is a parameter agreed locally (milestone 10)."""
        raise NotImplementedError

    def calculateEXOT(self, flight: Flight) -> DurationEstimate:
        """Following receipt of the TOBT, the ATC system calculates and provides the Estimated Taxi-Out Time (EXOT) based on the predicted traffic load, gate/stand location, runway in use, and waiting period at the Holding Position (milestone 9)."""
        raise NotImplementedError

    def recordASRT(self, flight: Flight) -> TimeQuantity:
        """ATC records the Actual Start up Request Time (ASRT), based on pilot request, available with an accuracy of +/- 1 minute (milestone 13)."""
        raise NotImplementedError

    def confirmTSATToPilot(self, flight: Flight) -> None:
        """ATC confirms TSAT to the pilot in order to maintain the aircraft in the pre-departure sequence (milestone 13)."""
        raise NotImplementedError

    def recordASAT(self, flight: Flight) -> TimeQuantity:
        """ATC provides the Actual start up Approval Time (ASAT) when the aircraft receives its start up approval, available with an accuracy of +/- 1 minute (milestone 14)."""
        raise NotImplementedError


@dataclass
class Aircraft:
    """The physical aircraft operating a flight, identified by type and registration, which the ATC Flight Plan may be used to update.

    Package Flights, stereotype entity, milestones [1].
    """
    registration: str | None = None
    aircraftType: str | None = None


@dataclass
class AircraftOperator(CDMPartner):
    """The airline or its representative that submits the ATC Flight Plan, provides TOBT and other estimates, and manages the turn-round.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 6, 7, 8, 9, 11, 12, 13, 15].

    Relationship: dependency 'submits' -> FlightPlan

    Relationship: association 'operates' -> Flight [*]
    """

    def submitFlightPlan(self, flightPlan: FlightPlan) -> None:
        """The ATC Flight Plan is submitted by the Aircraft Operator, normally 3 hours before EOBT although it may be later, or as a repetitive flight plan (RFPL) covering daily or weekly flights (milestone 1)."""
        raise NotImplementedError

    def provideFinalTOBT(self, flight: Flight, tobt: TimeQuantity, offsetMinutes: int) -> None:
        """The Aircraft Operator/Ground Handler provides their most accurate TOBT taking into account the operational situation, t minutes before EOBT where t is a locally agreed parameter (milestone 9)."""
        raise NotImplementedError


@dataclass
class AirportCDMPlatform:
    """The Airport CDM Platform that is initiated for each flight, holds all available flight information, and performs the ACISP checks, updates and notifications defined for each milestone.

    Package Systems, stereotype boundary, milestones [1, 4, 9, 10, 12, 13, 14, 15].

    Relationship: dependency 'sends' -> DPIMessage

    Relationship: association 'manages' -> Flight [1..*]
    """

    def initiateForFlight(self, flight: Flight) -> None:
        """The Airport CDM Platform is initiated for this flight, and all available information is processed (milestone 1)."""
        raise NotImplementedError

    def updateEstimatesOnActivation(self, flight: Flight, isArrival: bool) -> None:
        """For an arrival, ELDT and EIBT are updated; for a departure, EOBT and ETOT are updated (milestone 1)."""
        raise NotImplementedError

    def markRegulated(self, flight: Flight) -> None:
        """ETOT/TTOT/CTOT are updated and appropriate fields are marked as REGULATED (milestone 2)."""
        raise NotImplementedError

    def updateEstimatesAfterOutstationTakeOff(self, flight: Flight) -> None:
        """ELDT, EIBT, TOBT and TTOT are updated following take off from outstation (milestone 3)."""
        raise NotImplementedError

    def updateEstimatesAfterRadarUpdate(self, flight: Flight) -> None:
        """ELDT, EIBT, TOBT and TTOT are updated following local radar detection of the flight (milestone 4)."""
        raise NotImplementedError

    def updateEstimatesAfterFinalApproach(self, flight: Flight) -> None:
        """ELDT, EIBT, TOBT and TTOT are updated following detection of final approach (milestone 5)."""
        raise NotImplementedError

    def updateEstimatesAfterLanding(self, flight: Flight, aldt: TimeQuantity) -> None:
        """ELDT changes to ALDT, and EIBT, TOBT and TTOT are updated (milestone 6)."""
        raise NotImplementedError

    def updateEstimatesAfterInBlock(self, flight: Flight, aibt: TimeQuantity) -> None:
        """EIBT changes to AIBT, and TOBT and TTOT are updated (milestone 7)."""
        raise NotImplementedError

    def updateEstimatesAfterGroundHandlingStart(self, flight: Flight) -> None:
        """ETTT/TOBT and TTOT are updated (milestone 8)."""
        raise NotImplementedError

    def updateTTOTAfterTSAT(self, flight: Flight) -> None:
        """TTOT is updated following TSAT issue (milestone 10)."""
        raise NotImplementedError

    def recordAOBT(self, flight: Flight, aobt: TimeQuantity) -> None:
        """AOBT is recorded in the Airport CDM Platform (milestone 15)."""
        raise NotImplementedError

    def recordATOT(self, flight: Flight, atot: TimeQuantity) -> None:
        """ATOT is recorded in the Airport CDM Platform (milestone 16)."""
        raise NotImplementedError


@dataclass
class AirportSlot:
    """The airport slot programme entry that the ATC Flight Plan must correspond to for consistency checking at coordinated airports.

    Package Flights, stereotype entity, milestones [1].
    """
    assignedTime: datetime | None = None


@dataclass
class CDMPartnerNotification:
    """A notification sent to all relevant Airport CDM Partners informing them of an actual time (e.g. ASBT, ARDT, ASRT, ASAT, AOBT, ATOT), a ready status, or a departure message (FSA, MVT, airborne).

    Package Messages, stereotype boundary, milestones [10, 11, 12, 13, 14, 15, 16].

    Relationship: dependency 'informs' -> CDMPartner

    Relationship: dependency 'concerns' -> Flight
    """
    type: NotificationType | None = None
    timestamp: datetime | None = None


@dataclass
class DPIMessage:
    """A Departure Planning Information message (E-DPI, T-DPI, T-DPI-t, T-DPI-s, or A-DPI) exchanged between the Airport CDM Platform and Network Operations to convey flight and take-off time estimates.

    Package Messages, stereotype boundary, milestones [1, 2, 3, 10, 15].
    """
    type: DPIType | None = None
    scheduledOffBlockTime: datetime | None = None
    aircraftRegistration: str | None = None
    destination: str | None = None
    takeOffTimeEstimate: datetime | None = None


@dataclass
class DurationEstimate:
    """A calculated time interval such as the Estimated Taxi-Out Time (EXOT), Estimated Taxi-In Time (EXIT), Minimum Turn-round Time (MTTT) or Estimated Turn-round Time (ETTT), used as input to compute event-based time quantities.

    Package Timings, stereotype entity, milestones [2, 3, 4, 6, 8, 9].
    """
    durationType: DurationType | None = None
    value: timedelta | None = None


@dataclass
class ETFMS:
    """The system used by Network Operations to monitor flight progress and issue Flight Update Messages when a flight is close to its destination.

    Package Systems, stereotype boundary, milestones [2, 3].

    Relationship: dependency 'monitors progress of' -> Flight
    """
    pass


@dataclass
class Flight:
    """A single arriving or departing operation of an aircraft, tracked through the sixteen milestones and carrying an operational status.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'is described by' -> FlightPlan [1..2]

    Relationship: association 'is operated by' -> Aircraft [1]

    Relationship: association 'is assigned to' -> ParkingPosition [0..1]

    Relationship: composition 'records' -> TimeQuantity [0..*]

    Relationship: aggregation 'uses' -> DurationEstimate [0..*]
    """
    operationalStatus: FlightOperationalStatus | None = None
    isRegulated: bool | None = None
    offBlockTime: TimeQuantity | None = None
    inBlockTime: TimeQuantity | None = None
    landingTime: TimeQuantity | None = None
    takeOffTime: TimeQuantity | None = None
    startUpApprovalTime: TimeQuantity | None = None
    boardingTime: TimeQuantity | None = None
    readyTime: TimeQuantity | None = None
    startUpRequestTime: TimeQuantity | None = None
    groundHandlingStartTime: TimeQuantity | None = None
    taxiOutTime: DurationEstimate | None = None
    taxiInTime: DurationEstimate | None = None
    minimumTurnRoundTime: DurationEstimate | None = None
    estimatedTurnRoundTime: DurationEstimate | None = None
    parkingPosition: ParkingPosition | None = None

    def updateOperationalStatus(self, newStatus: FlightOperationalStatus) -> None:
        """The flight's operational status changes to the value defined by each milestone as it occurs, e.g. INITIATED (milestone 1), AIRBORNE (milestone 3), FIR (milestone 4), FINAL (milestone 5), LANDED (milestone 6), IN-BLOCK (milestones 7, 8, 9), SEQUENCED (milestone 10), BOARDING (milestone 11), READY (milestone 12), OFF-BLOCK (milestone 15), DEPARTED/TAKE OFF (milestone 16)."""
        raise NotImplementedError

    def calculateEIBT(self, eldt: TimeQuantity, taxiInTime: DurationEstimate) -> TimeQuantity:
        """An estimated in-block time (EIBT) is computed using the ELDT and the estimated taxi-in time (milestone 4); the EIBT can be updated according to the ALDT+EXIT (milestone 6)."""
        raise NotImplementedError


@dataclass
class FlightCrew(CDMPartner):
    """The pilot and cockpit crew who request start-up and push-back and coordinate with the Ground Handler around TSAT.

    Package Stakeholders, stereotype entity, milestones [12, 13, 14].

    Relationship: association 'requests start-up for' -> Flight [1]
    """
    pass


@dataclass
class FlightPlan:
    """The ICAO/ATC Flight Plan submitted by the Aircraft Operator and distributed by IFPS, including repetitive flight plans (RFPL), against which flight estimates are checked for consistency.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 9].

    Relationship: association 'must correspond to' -> AirportSlot [0..1]

    Relationship: dependency 'may update' -> Aircraft
    """
    isRepetitive: bool | None = None
    destination: str | None = None
    estimatedElapsedTime: timedelta | None = None


@dataclass
class FlightUpdateMessage:
    """The FUM sent by Network Operations providing updates of an inbound flight's progress and estimated landing time.

    Package Messages, stereotype boundary, milestones [1, 3].
    """
    estimatedLandingTime: datetime | None = None


@dataclass
class GroundHandler(CDMPartner):
    """The party that performs ground handling operations and, together with the Aircraft Operator, provides turn-round related times such as ACGT, ARDT and TOBT.

    Package Stakeholders, stereotype entity, milestones [6, 7, 8, 9, 11, 12, 13, 15].

    Relationship: association 'handles' -> Flight [*]
    """

    def recordACGT(self, flight: Flight, acgt: TimeQuantity) -> None:
        """The Aircraft Operator/Ground Handler provides the Actual Commence of Ground Handling time (ACGT), available with an accuracy of +/- 1 minute (milestone 8)."""
        raise NotImplementedError

    def recordARDT(self, flight: Flight, ardt: TimeQuantity) -> None:
        """The Ground Handler provides the Actual Ready Time (ARDT) when all doors are closed, boarding bridge removed and push back vehicle connected, ready to taxi immediately upon reception of TWR instructions (milestone 12)."""
        raise NotImplementedError

    def recordASBT(self, flight: Flight, asbt: TimeQuantity) -> None:
        """ASBT is provided automatically from the airport system or by manual input by the Aircraft Operator/Ground Handler when the gate opens for passengers to physically start boarding (milestone 11)."""
        raise NotImplementedError


@dataclass
class IFPS:
    """The Integrated Initial Flight Plan Processing System that distributes the submitted ATC Flight Plan to all involved ATC units.

    Package Systems, stereotype boundary, milestones [1].

    Relationship: dependency 'distributes' -> FlightPlan

    Relationship: association 'distributes flight plan to' -> AirTrafficControlUnit [*]
    """

    def distributeFlightPlan(self, flightPlan: FlightPlan, atcUnits: list[AirTrafficControlUnit]) -> None:
        """The ATC Flight Plan is submitted by the Aircraft Operator and distributed by the IFPS; all involved ATC units receive the flight plan, including departure and destination aerodromes (milestone 1)."""
        raise NotImplementedError


@dataclass
class Milestone:
    """A generalization of the sixteen defined events in the CDM turn-round process, each with its trigger, timing rule, effect and procedure applied over the flight's entity classes.

    Package Milestones, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: dependency 'processes' -> Flight
    """
    number: int | None = None
    resultingStatus: FlightOperationalStatus | None = None
    ttotTolerance: timedelta | None = None


@dataclass
class MilestoneAircraftReady(Milestone):
    """Milestone 12: the aircraft is ready for start-up/push-back (ARDT); partners are informed and, past TOBT plus tolerance without a ready status, the Aircraft Operator/Ground Handler is alerted.

    Package Milestones, stereotype control, milestones [12].

    Relationship: dependency 'informs partners of ARDT' -> CDMPartnerNotification
    """
    readyTolerance: timedelta | None = None

    def informPartnersOfARDT(self, flight: Flight, ardt: TimeQuantity) -> None:
        """All relevant Airport CDM Partners are informed of Actual Ready Time (ARDT) in the Airport CDM Platform and that the aircraft is ready for start up/push-back (milestone 12)."""
        raise NotImplementedError

    def checkReadyStatusReceived(self, flight: Flight, tolerance: timedelta) -> bool:
        """At TOBT + tolerance the AO/GH are informed that TOBT has passed and there has not been a ready status message (ARDT or RDY) yet (milestone 12)."""
        raise NotImplementedError


@dataclass
class MilestoneBoardingStarts(Milestone):
    """Milestone 11: boarding of passengers begins; partners are informed of ASBT and boarding status is checked against TOBT.

    Package Milestones, stereotype control, milestones [11].

    Relationship: dependency 'informs partners of ASBT' -> CDMPartnerNotification
    """
    boardingCheckOffset: timedelta | None = None

    def informPartnersOfASBT(self, flight: Flight, asbt: TimeQuantity) -> None:
        """All relevant Airport CDM Partners are informed of the Actual Start Boarding Time (ASBT) when it occurs (milestone 11)."""
        raise NotImplementedError

    def checkBoardingStatus(self, flight: Flight) -> bool:
        """At a certain time before TOBT (local variable e.g. corresponding to aircraft type) a check shall be performed to check the boarding status, checking whether boarding starts in time to respect TOBT, and to inform the AO/GH in case TOBT needs to be updated (milestone 11)."""
        raise NotImplementedError


@dataclass
class MilestoneEOBTMinus2Hours(Milestone):
    """Milestone 2: at EOBT-2 hours, regulated flights receive a CTOT and estimates are checked against the ATC Flight Plan before informing Network Operations via the first T-DPI.

    Package Milestones, stereotype control, milestones [2].

    Relationship: dependency 'sends T-DPI' -> DPIMessage
    """
    offsetBeforeEOBT: timedelta | None = None

    def checkEstimatesConsistency(self, flight: Flight, flightPlan: FlightPlan) -> bool:
        """A check shall be performed to verify feasibility of the ATC Flight Plan estimated off block time at EOBT-2 hrs, checking whether AO/GH flight estimates are consistent with the ATC Flight Plan (milestone 2)."""
        raise NotImplementedError

    def informNetworkOperationsViaTDPI(self, flight: Flight) -> None:
        """At EOBT-2 hrs Network Operations is informed through the first T-DPI message of the updated take off time estimate (milestone 2)."""
        raise NotImplementedError

    def calculateTTOT(self, eibt: TimeQuantity, mttt: DurationEstimate, exot: DurationEstimate, eobt: TimeQuantity, tobt: TimeQuantity) -> TimeQuantity:
        """Calculation basis for the TTOT shall take into account EIBT+MTTT+EXOT, if later than EOBT+EXOT. In the case of manual input of TOBT, this estimate overrides the EIBT+MTTT estimate, hence TTOT equals TOBT+EXOT (milestone 2)."""
        raise NotImplementedError


@dataclass
class TOBTConsistencyMilestone(Milestone):
    """An abstract generalization of the milestones (Local Radar Update, Final Approach, Landed, In-Block, Ground Handling Started, Final Confirmation of the TOBT) that each check TOBT consistency against the ATC Flight Plan and notify Network Operations when TTOT changes beyond the agreed tolerance.

    Package Milestones, stereotype control, milestones [4, 5, 6, 7, 8, 9].
    """

    def checkTOBTConsistency(self, flight: Flight, flightPlan: FlightPlan) -> bool:
        """A check shall be performed to verify feasibility of the ATC Flight Plan given the updated TOBT, checking whether the AO/GH TOBT is consistent with the ATC Flight Plan (milestones 4, 5, 6, 7, 8, 9)."""
        raise NotImplementedError

    def notifyNetworkOperationsIfTTOTExceedsTolerance(self, flight: Flight, tolerance: timedelta) -> None:
        """Network Operations is informed when the TTOT changes by more than the agreed TTOT tolerance (milestones 4, 5, 6, 7, 8, 9)."""
        raise NotImplementedError


@dataclass
class MilestoneFinalApproach(TOBTConsistencyMilestone):
    """Milestone 5: detection of the flight entering Final Approach, commencing the TOBT process and checking TOBT feasibility against the ATC Flight Plan.

    Package Milestones, stereotype control, milestones [5].
    """
    pass


@dataclass
class MilestoneFinalTOBTConfirmation(TOBTConsistencyMilestone):
    """Milestone 9: the Aircraft Operator/Ground Handler provides their most accurate TOBT before EOBT, which is checked against the ATC Flight Plan prior to TSAT issue.

    Package Milestones, stereotype control, milestones [9].
    """
    confirmationOffset: timedelta | None = None


@dataclass
class MilestoneFlightPlanActivation(Milestone):
    """Milestone 1: submission and activation of the ATC Flight Plan, initiating the Airport CDM Platform for the flight and checking consistency between the ATC Flight Plan, Airport Slot and Airport flight data before the first E-DPI.

    Package Milestones, stereotype control, milestones [1].

    Relationship: dependency 'checks' -> FlightPlan

    Relationship: dependency 'checks' -> AirportSlot

    Relationship: dependency 'sends E-DPI' -> DPIMessage
    """
    activationOffset: timedelta | None = None
    readinessOffset: timedelta | None = None

    def checkFlightPlanConsistency(self, flight: Flight, flightPlan: FlightPlan, airportSlot: AirportSlot) -> bool:
        """A check shall be performed to verify the consistency between the ATC Flight Plan, Airport Slot and Airport flight data before the first E-DPI is sent (milestone 1)."""
        raise NotImplementedError

    def confirmFlightToNetworkOperations(self, flight: Flight) -> None:
        """The process confirms the flight to the Network Operations and allows further local processing of the flight, feeding Network Operations with consistent SOBT, aircraft registration and first destination data as early as possible (milestone 1)."""
        raise NotImplementedError

    def sendEDPI(self, flight: Flight) -> None:
        """The E-DPI message should not be sent if no or inconsistent information is provided by the AO before this first E-DPI message (milestone 1)."""
        raise NotImplementedError


@dataclass
class MilestoneGroundHandlingStarted(TOBTConsistencyMilestone):
    """Milestone 8: the actual commencement of ground handling (ACGT) triggers a TOBT update based on the estimated turn-round period and checks TOBT feasibility against the ATC Flight Plan.

    Package Milestones, stereotype control, milestones [8].
    """
    pass


@dataclass
class MilestoneInBlock(TOBTConsistencyMilestone):
    """Milestone 7: the actual in-block time (AIBT) triggers updates to TOBT and TTOT based on the estimated turn-round period and checks TOBT feasibility against the ATC Flight Plan.

    Package Milestones, stereotype control, milestones [7].
    """
    pass


@dataclass
class MilestoneLanded(TOBTConsistencyMilestone):
    """Milestone 6: the actual landing time (ALDT) triggers updates to TOBT and TTOT based on the defined turn-round period and checks TOBT feasibility against the ATC Flight Plan.

    Package Milestones, stereotype control, milestones [6].
    """
    pass


@dataclass
class MilestoneLocalRadarUpdate(TOBTConsistencyMilestone):
    """Milestone 4: detection of the flight entering the FIR or local airspace, commencing the TOBT process and checking TOBT feasibility against the ATC Flight Plan.

    Package Milestones, stereotype control, milestones [4].
    """
    pass


@dataclass
class MilestoneOffBlock(Milestone):
    """Milestone 15: the actual off-block time (AOBT) is recorded, TTOT is updated considering EXOT, and an A-DPI is sent to Network Operations, with further A-DPIs if TTOT changes beyond tolerance.

    Package Milestones, stereotype control, milestones [15].

    Relationship: dependency 'sends A-DPI' -> DPIMessage

    Relationship: dependency 'informs partners of AOBT' -> CDMPartnerNotification
    """

    def informPartnersOfAOBT(self, flight: Flight, aobt: TimeQuantity) -> None:
        """All relevant Airport CDM Partners are informed of Actual Off-Block Time (AOBT) in the Airport CDM Platform and that the aircraft has commenced push-back/taxi from parking position, when it occurs (milestone 15)."""
        raise NotImplementedError

    def sendADPI(self, flight: Flight) -> None:
        """AOBT always triggers an A-DPI message to Network Operations, or in the case of remote holding at a defined time prior to TTOT (milestone 15)."""
        raise NotImplementedError

    def checkTTOTAfterAOBT(self, flight: Flight, tolerance: timedelta) -> None:
        """After a first A-DPI is sent this check shall be performed to check TTOT updates against the TTOT tolerance before Network Operations is informed, with a new A-DPI, of the updated TTOT (milestone 15)."""
        raise NotImplementedError


@dataclass
class MilestoneStartUpApproved(Milestone):
    """Milestone 14: ATC records the actual start-up approval time (ASAT), checks it against TSAT, and alerts and re-sequences the flight if approval is not granted within tolerance.

    Package Milestones, stereotype control, milestones [14].

    Relationship: dependency 'informs partners of ASAT' -> CDMPartnerNotification
    """
    approvalTolerance: timedelta | None = None

    def informPartnersOfASAT(self, flight: Flight, asat: TimeQuantity) -> None:
        """All relevant Airport CDM Partners are informed of Actual start up approval Time (ASAT) in the Airport CDM Platform and that the aircraft has received start up approval/push-back clearance when it occurs (milestone 14)."""
        raise NotImplementedError

    def checkASATAgainstTSAT(self, flight: Flight) -> bool:
        """A check shall be performed to see if ASAT is in accordance with TSAT (milestone 14)."""
        raise NotImplementedError

    def alertAndResequenceIfNoApproval(self, flight: Flight, tolerance: timedelta) -> None:
        """In case the start up approval is not granted at TSAT + tolerance, all relevant partners are informed and the flight will be re-sequenced (milestone 14)."""
        raise NotImplementedError


@dataclass
class MilestoneStartUpRequested(Milestone):
    """Milestone 13: ATC records the actual start-up request time (ASRT) and alerts partners if no request is made within the TSAT tolerance window.

    Package Milestones, stereotype control, milestones [13].

    Relationship: dependency 'informs partners of ASRT' -> CDMPartnerNotification
    """
    requestTolerance: timedelta | None = None

    def informPartnersOfASRT(self, flight: Flight, asrt: TimeQuantity) -> None:
        """All relevant Airport CDM Partners are informed of Actual Start up Request Time (ASRT) in the Airport CDM Platform when it occurs (milestone 13)."""
        raise NotImplementedError

    def alertIfNoStartUpRequested(self, flight: Flight, tolerance: timedelta) -> None:
        """If the start up request is not made by TSAT + tolerance, all relevant Airport CDM Partners are alerted and the AO/GH is informed that no start up has been requested and should update TOBT (milestone 13)."""
        raise NotImplementedError


@dataclass
class MilestoneTSATIssued(Milestone):
    """Milestone 10: ATC issues the TSAT, informs partners and Network Operations, and checks the number of TOBT updates after TSAT against a local tolerance.

    Package Milestones, stereotype control, milestones [10].

    Relationship: dependency 'sends T-DPI-s' -> DPIMessage

    Relationship: dependency 'informs partners of TSAT' -> CDMPartnerNotification
    """
    issueOffset: timedelta | None = None
    tobtUpdateThreshold: int | None = None

    def informPartnersOfTSAT(self, flight: Flight) -> None:
        """All relevant partners are informed of the TSAT that has been allocated to the flight; Network Operations is informed by a T-DPI-s for non regulated flights (milestone 10)."""
        raise NotImplementedError

    def checkTOBTUpdatesAfterTSAT(self, flight: Flight, threshold: int) -> bool:
        """A check shall be performed to see the number of TOBT updates after TSAT has been issued against a tolerance defined locally; in case the number of TOBT updates exceeds this threshold, the TOBT input should be processed according to local procedure (milestone 10)."""
        raise NotImplementedError


@dataclass
class MilestoneTakeOff(Milestone):
    """Milestone 16: the actual take-off time (ATOT) is recorded, FSA and MVT messages are sent, and the flight is removed from the departure sequence.

    Package Milestones, stereotype control, milestones [16].

    Relationship: dependency 'informs partners of take off' -> CDMPartnerNotification
    """

    def informPartnersOfTakeOff(self, flight: Flight) -> None:
        """All relevant Airport CDM Partners are informed about the actual take off (milestone 16)."""
        raise NotImplementedError

    def generateAirborneMessage(self, flight: Flight) -> None:
        """An airborne message is generated and FSA and MVT messages are sent (milestone 16)."""
        raise NotImplementedError

    def removeFromDepartureSequence(self, flight: Flight) -> None:
        """The flight is removed from the departure sequence following take off (milestone 16)."""
        raise NotImplementedError


@dataclass
class MilestoneTakeOffFromOutstation(Milestone):
    """Milestone 3: the ATOT from the outstation is used to check estimated landing time consistency with the outbound ATC Flight Plan and, if the TTOT tolerance is exceeded, inform Network Operations via a T-DPI-t.

    Package Milestones, stereotype control, milestones [3].

    Relationship: dependency 'sends T-DPI-t' -> DPIMessage
    """

    def checkLandingEstimateConsistency(self, flight: Flight, outboundFlightPlan: FlightPlan) -> bool:
        """A check shall be performed to verify feasibility of the ATC Flight Plan at take off from outstation, checking whether the AO/GH estimated landing time is consistent with the outbound ATC Flight Plan (milestone 3)."""
        raise NotImplementedError

    def notifyNetworkOperationsIfTTOTExceedsTolerance(self, flight: Flight, toleranceMinutes: int) -> None:
        """A TTOT tolerance of 5 minutes is respected before Network Operations is informed of the updated TTOT using a T-DPI-t Message (milestone 3)."""
        raise NotImplementedError

    def calculateTTOT(self, eibt: TimeQuantity, mttt: DurationEstimate, exot: DurationEstimate, eobt: TimeQuantity, tobt: TimeQuantity) -> TimeQuantity:
        """Calculation basis for the TTOT shall take into account EIBT+MTTT+EXOT. In case EOBT is later than EIBT+MTTT, TTOT equals EOBT+EXOT. Where TOBT is available this prediction overrules the EIBT+MTTT estimate, hence TTOT equals TOBT+EXOT (milestone 3)."""
        raise NotImplementedError

    def calculateELDTFromATOT(self, atot: TimeQuantity, estimatedElapsedTime: timedelta) -> TimeQuantity:
        """Using the ATOT an ELDT can be calculated by using the Estimated Elapsed Time on the FPL, if the departure airport is more than 3hrs flying time from the destination airport (milestone 3)."""
        raise NotImplementedError


@dataclass
class NetworkOperations(CDMPartner):
    """The Network Manager function that issues CTOT, monitors flight progress and receives DPI messages to coordinate the flight with the wider ATM network.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15].

    Relationship: dependency 'receives' -> DPIMessage

    Relationship: dependency 'sends' -> FlightUpdateMessage

    Relationship: aggregation 'uses' -> ETFMS [1]

    Relationship: association 'coordinates' -> Flight [*]
    """

    def issueCTOT(self, flight: Flight) -> TimeQuantity:
        """The CTOT is issued by the Network Operations at EOBT-2h if the flight is regulated, and is sent to relevant ATS units as well as the departure aerodrome (milestone 2)."""
        raise NotImplementedError

    def monitorFlightProgress(self, flight: Flight) -> None:
        """If the flight is within 3hrs flying time of the destination airport, Network Operations monitors progress of the flight using the ETFMS (milestone 3)."""
        raise NotImplementedError

    def sendFlightUpdateMessage(self, flight: Flight) -> FlightUpdateMessage:
        """Network Operations sends a Flight Update Message (FUM) that provides updates of the flight's progress, used to update ELDT (milestones 1, 3)."""
        raise NotImplementedError


@dataclass
class ParkingPosition:
    """The stand or gate assigned to a flight, changes to which are discouraged after ELDT-30 minutes.

    Package Flights, stereotype entity, milestones [4].
    """
    identifier: str | None = None


@dataclass
class StandGateManagement(CDMPartner):
    """The stakeholder responsible for stand and gate allocation who shares EOBT information with ATC and Network Operations.

    Package Stakeholders, stereotype entity, milestones [9].

    Relationship: dependency 'shares EOBT with' -> Flight
    """
    pass


@dataclass
class TimeQuantity:
    """A named time value describing a flight's progress toward a milestone event, distinguished by a prefix (Scheduled, Estimated, Target, Actual, Calculated) and an event (e.g. Off-Block, In-Block, Landing, Take-Off, Start-Up Approval, Boarding, Ready, Start-Up Request, Ground Handling Start); every successive value is appended with its originator and time of update rather than overwritten.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'originator' -> CDMPartner [1]
    """
    prefix: TimePrefix | None = None
    event: TimeEvent | None = None
    value: datetime | None = None
    accuracy: timedelta | None = None
    originator: CDMPartner | None = None
    recordedAt: datetime | None = None


@dataclass
class TurnRound:
    """The aircraft turn-round linking an arriving flight and its related departing flight for the purpose of estimating and analysing turn-round times.

    Package Flights, stereotype entity, milestones [1, 6, 7, 8].

    Relationship: composition 'comprises arriving and departing flight' -> Flight [2]

    Relationship: composition 'period' -> DurationEstimate [1]
    """
    period: DurationEstimate | None = None

    def calculateTOBTFromTurnRoundPeriod(self, referenceTime: TimeQuantity, period: DurationEstimate) -> TimeQuantity:
        """TOBT for the departing flight is updated automatically or inserted manually by the Aircraft Operator/Ground Handler, calculated on the basis of the defined or estimated turn-round period, following ALDT (milestone 6), AIBT (milestone 7) or ACGT (milestone 8)."""
        raise NotImplementedError
