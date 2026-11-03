"""Class stubs rendered from runs/single/run_03/model.json by src/generate/render_code.py; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from enum import Enum


class EventType(Enum):
    OFF_BLOCK = "Off-Block"
    IN_BLOCK = "In-Block"
    LANDING = "Landing"
    TAKE_OFF = "Take-Off"
    START_UP_APPROVAL = "Start-Up Approval"
    START_BOARDING = "Start-Boarding"
    READY = "Ready"
    START_UP_REQUEST = "Start-Up-Request"
    GROUND_HANDLING_START = "Ground-Handling-Start"


class FlightOperationalStatus(Enum):
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


@dataclass
class DpiMessage:
    """A Departure Planning Information message exchanged with Network Operations as part of the DPI process.

    Package Messages, stereotype boundary, milestones [1, 2, 3, 10, 15].
    """
    sentTime: datetime | None = None
    sender: str | None = None


@dataclass
class ADpiMessage(DpiMessage):
    """The A-DPI message that AOBT always triggers to Network Operations, and which carries updated TTOT thereafter.

    Package Messages, stereotype boundary, milestones [15].
    """
    pass


@dataclass
class Acars:
    """The Aircraft Communications Addressing and Reporting System that signals ON/OFF/IN/OUT events.

    Package Systems, stereotype boundary, milestones [6, 7, 15, 16].
    """

    def signalEvent(self, event: EventType) -> None:
        """Signals ACARS=ON (landing), ACARS=IN (in-block), ACARS=OUT (off-block), or ACARS=OFF (take-off)."""
        raise NotImplementedError


@dataclass
class TimeQuantity:
    """A named time quantity describing a flight's progress, combining a prefix (Scheduled, Estimated, Target, Actual, Calculated) with an event, kept as a history of successive values.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    quantityName: str | None = None
    event: EventType | None = None
    value: datetime | None = None
    originator: str | None = None
    accuracy: str | None = None
    updatedAt: datetime | None = None

    def update(self, newValue: datetime, originator: str) -> None:
        """Appends a new successive value with its originator and time of update, rather than overwriting, so a turn-round can be analysed afterwards."""
        raise NotImplementedError


@dataclass
class ActualTime(TimeQuantity):
    """An actual-prefix time quantity such as ATOT, ALDT, AIBT, ACGT, ASBT, ARDT, ASRT, ASAT, AOBT.

    Package Timings, stereotype entity, milestones [3, 6, 7, 8, 11, 12, 13, 14, 15, 16].
    """
    pass


@dataclass
class Aircraft:
    """The physical aircraft operating a flight, whose type and registration may be updated from the flight plan.

    Package Flights, stereotype entity, milestones [1].
    """
    registration: str | None = None
    type: str | None = None


@dataclass
class CdmPartner:
    """A party that takes part in the Airport CDM process and originates or receives information about a flight.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    name: str | None = None

    def receiveNotification(self, information: str) -> None:
        """Receives information relayed by a milestone process, e.g. 'inform all relevant Airport CDM Partners'."""
        raise NotImplementedError


@dataclass
class AircraftOperator(CdmPartner):
    """The airline that submits the ATC Flight Plan and provides estimates such as TOBT.

    Package Stakeholders, stereotype entity, milestones [1, 3, 6, 7, 8, 9, 11, 12, 13].

    Relationship: dependency 'submits' -> AtcFlightPlan
    """

    def submitFlightPlan(self, flightPlan: AtcFlightPlan) -> None:
        """Submits the ICAO ATC Flight Plan; the AO must provide correct information before the first E-DPI (Milestone 1)."""
        raise NotImplementedError

    def provideTobt(self, flight: Flight, value: datetime) -> None:
        """Provides the most accurate TOBT taking into account the operational situation, integrating own strategy to compute TOBT (Milestone 9)."""
        raise NotImplementedError


@dataclass
class Milestone:
    """One of the sixteen CDM events, each with its trigger, timing rule, effect on operational status, and procedure.

    Package Milestones, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'concerns' -> Flight [1]
    """
    milestoneNumber: int | None = None
    milestoneName: str | None = None
    definitionText: str | None = None
    triggeredBy: str | None = None
    operationalStatusChange: FlightOperationalStatus | None = None

    def recordOccurrence(self, time: datetime) -> None:
        """Records that the milestone has occurred for a flight, at the stated time."""
        raise NotImplementedError


@dataclass
class AircraftReady(Milestone):
    """Milestone 12: all doors closed, boarding bridge removed, push-back vehicle connected, ready to taxi (ARDT).

    Package Milestones, stereotype control, milestones [12].

    Relationship: dependency 'uses' -> ReadyStatusMessage
    """

    def informPartnersOfArdt(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of ARDT and that the aircraft is ready for start-up/push-back."""
        raise NotImplementedError

    def alertIfNoReadyStatus(self, flight: Flight) -> None:
        """At TOBT + tolerance, informs the AO/GH that TOBT has passed and no ARDT or Ready Status (RDY) has been received."""
        raise NotImplementedError


@dataclass
class AirportCdmPlatform:
    """The Airport CDM Platform that is initiated for a flight, processes all available information, and performs ACISP actions.

    Package Systems, stereotype control, milestones [1, 2, 4, 12].

    Relationship: association 'manages' -> Flight [1..*]
    """

    def initiateForFlight(self, flight: Flight) -> None:
        """Initiates the Airport CDM Platform for the flight and processes all available information (Milestone 1)."""
        raise NotImplementedError

    def markFieldsAsRegulated(self, flight: Flight) -> None:
        """Marks appropriate fields as REGULATED (Milestone 2)."""
        raise NotImplementedError

    def computeTobtAutomatically(self, flight: Flight) -> datetime:
        """Calculates a new TOBT automatically following an update of ELDT (Milestone 4)."""
        raise NotImplementedError

    def receiveInput(self, flight: Flight, input: str) -> None:
        """Receives an input to the Airport CDM Platform, triggering the Aircraft Ready procedure (Milestone 12)."""
        raise NotImplementedError


@dataclass
class AirportSlot:
    """The airport slot programme entry against which the ATC Flight Plan is checked for consistency.

    Package Flights, stereotype entity, milestones [1].
    """
    slotReference: str | None = None


@dataclass
class AtcFlightPlan:
    """The ICAO flight plan submitted by the Aircraft Operator and distributed by IFPS, corresponding to the airport slot programme.

    Package Flights, stereotype entity, milestones [1].
    """
    departureAerodrome: str | None = None
    destinationAerodrome: str | None = None
    estimatedElapsedTime: timedelta | None = None
    isRepetitive: bool | None = None


@dataclass
class AtcSystem:
    """The ATC/radar/A-SMGCS system that detects a flight and provides actual times such as ATOT, ALDT and AIBT.

    Package Systems, stereotype boundary, milestones [4, 5, 6, 7, 16].
    """
    systemType: str | None = None

    def detectFlight(self, ssrCode: str) -> None:
        """Detects a flight based upon the assigned SSR code when it crosses a defined FIR/ATC boundary or range/position/level (Milestones 4,5)."""
        raise NotImplementedError


@dataclass
class AtcUnit(CdmPartner):
    """An air traffic control unit (ACC, Approach, Tower) that receives the flight plan, issues TSAT, and approves start-up.

    Package Stakeholders, stereotype entity, milestones [1, 9, 10, 13, 14].

    Relationship: association 'issues TSAT for' -> Flight [0..*]

    Relationship: dependency 'receives flight plan from' -> Ifps
    """
    unitType: str | None = None

    def issueTsat(self, flight: Flight) -> None:
        """Issues the Target Start-Up Approval Time t-minutes before EOBT, t agreed locally (Milestone 10)."""
        raise NotImplementedError

    def confirmTsatToPilot(self, flight: Flight) -> None:
        """Confirms TSAT to the pilot in order to maintain the aircraft in the pre-departure sequence (Milestone 13)."""
        raise NotImplementedError

    def approveStartUp(self, flight: Flight) -> None:
        """Grants start-up approval / push-back clearance (Milestone 14)."""
        raise NotImplementedError


@dataclass
class BoardingStarts(Milestone):
    """Milestone 11: the gate is open for passengers to physically start boarding.

    Package Milestones, stereotype control, milestones [11].
    """

    def informPartnersOfAsbt(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of Actual Start Boarding Time (ASBT)."""
        raise NotImplementedError

    def checkBoardingStatus(self, flight: Flight) -> bool:
        """At a locally defined time before TOBT, checks whether boarding starts in time to respect TOBT and informs the AO/GH if TOBT needs updating."""
        raise NotImplementedError


@dataclass
class CalculatedTime(TimeQuantity):
    """A calculated-prefix time quantity such as CTOT.

    Package Timings, stereotype entity, milestones [2].
    """
    pass


@dataclass
class EDpiMessage(DpiMessage):
    """The first E-DPI message, sent only if consistent SOBT, aircraft registration and first destination data have been provided.

    Package Messages, stereotype boundary, milestones [1].
    """
    pass


@dataclass
class Eobt2HrCheck(Milestone):
    """Milestone 2: at EOBT-2hr, flights are known as regulated or not and receive a CTOT if regulated.

    Package Milestones, stereotype control, milestones [2].

    Relationship: dependency 'sends' -> TDpiMessage

    Relationship: dependency 'uses' -> FumMessage
    """

    def checkFlightEstimatesConsistency(self, flight: Flight) -> bool:
        """Checks whether AO/GH flight estimates are consistent with the ATC Flight Plan at EOBT-2hrs, before or after take-off from outstation."""
        raise NotImplementedError

    def calculateTtot(self, flight: Flight) -> datetime:
        """Calculates TTOT taking into account EIBT+MTTT+EXOT if later than EOBT+EXOT; if TOBT is manually input it overrides, so TTOT equals TOBT+EXOT."""
        raise NotImplementedError

    def markAsRegulated(self, flight: Flight) -> None:
        """Marks appropriate fields as REGULATED for a flight receiving a CTOT."""
        raise NotImplementedError


@dataclass
class EstimatedTime(TimeQuantity):
    """An estimated-prefix time quantity such as EOBT, ELDT, EIBT, ETOT.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5].
    """
    pass


@dataclass
class Etfms:
    """The system Network Operations uses to monitor a flight's progress within 3 hours flying time of the destination airport.

    Package Systems, stereotype boundary, milestones [3].
    """

    def monitorProgress(self, flight: Flight) -> None:
        """Monitors progress of the flight and triggers sending of a Flight Update Message (FUM) with updates of the flight's progress."""
        raise NotImplementedError


@dataclass
class FinalApproach(Milestone):
    """Milestone 5: the flight enters the Final Approach phase at the destination airport.

    Package Milestones, stereotype control, milestones [5].

    Relationship: dependency 'detected by' -> AtcSystem
    """

    def checkTobtConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT."""
        raise NotImplementedError

    def informNetworkOperationsIfTtotChanges(self, flight: Flight) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class FinalConfirmationOfTobt(Milestone):
    """Milestone 9: the time the Aircraft Operator/Ground Handler provides its most accurate TOBT.

    Package Milestones, stereotype control, milestones [9].
    """
    localParameterT: timedelta | None = None

    def checkTobtConsistency(self, flight: Flight) -> bool:
        """Performed at a predefined local time to confirm TOBT prior to TSAT issue and verify feasibility of ATC Flight Plan estimates given the updated TOBT."""
        raise NotImplementedError

    def calculateExot(self, trafficLoad: str, gateLocation: str, runwayInUse: str, holdingPeriod: timedelta) -> timedelta:
        """ATC calculates and provides EXOT based on predicted traffic load, gate/stand location, runway in use, and waiting period at the Holding Position."""
        raise NotImplementedError


@dataclass
class Flight:
    """An arriving or departing flight tracked through the CDM process, carrying its operational status and time quantities.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'described by' -> AtcFlightPlan [1]

    Relationship: association 'corresponds to' -> AirportSlot [0..1]

    Relationship: association 'operated by' -> Aircraft [1]

    Relationship: association 'records' -> TimeQuantity [0..*]
    """
    flightId: str | None = None
    direction: str | None = None
    operationalStatus: FlightOperationalStatus | None = None
    exot: timedelta | None = None
    exit: timedelta | None = None
    sobt: ScheduledTime | None = None
    eobt: EstimatedTime | None = None
    tobt: TargetTime | None = None
    aobt: ActualTime | None = None
    eldt: EstimatedTime | None = None
    aldt: ActualTime | None = None
    eibt: EstimatedTime | None = None
    aibt: ActualTime | None = None
    etot: EstimatedTime | None = None
    ttot: TargetTime | None = None
    ctot: CalculatedTime | None = None
    atot: ActualTime | None = None
    acgt: ActualTime | None = None
    asbt: ActualTime | None = None
    ardt: ActualTime | None = None
    asrt: ActualTime | None = None
    asat: ActualTime | None = None


@dataclass
class FlightPlanActivation(Milestone):
    """Milestone 1: the ICAO flight plan is submitted to ATC and the Airport CDM Platform is initiated for the flight.

    Package Milestones, stereotype control, milestones [1].

    Relationship: dependency 'flight plan distributed by' -> Ifps

    Relationship: dependency 'sends' -> EDpiMessage
    """

    def checkConsistency(self, flightPlan: AtcFlightPlan, slot: AirportSlot, flight: Flight) -> bool:
        """Checks consistency between the ATC Flight Plan, Airport Slot and Airport flight data before the first E-DPI is sent."""
        raise NotImplementedError

    def updateEstimates(self, flight: Flight) -> None:
        """Updates ELDT and EIBT for an arrival, and ETOT for a departure."""
        raise NotImplementedError

    def sendFirstEdpi(self, flight: Flight) -> None:
        """Sends the first E-DPI only if consistent information has been provided; not sent if information is missing or inconsistent."""
        raise NotImplementedError


@dataclass
class FsaMessage:
    """The FSA message sent at Take-Off.

    Package Messages, stereotype boundary, milestones [16].
    """
    pass


@dataclass
class FumMessage:
    """The Flight Update Message sent by Network Operations providing updates of the flight's progress.

    Package Messages, stereotype boundary, milestones [2, 3].
    """
    pass


@dataclass
class GroundHandler(CdmPartner):
    """The party that undertakes ground handling operations and provides ready and TOBT-related information.

    Package Stakeholders, stereotype entity, milestones [3, 6, 7, 8, 9, 11, 12].
    """

    def commenceGroundHandling(self, flight: Flight) -> None:
        """Provides the Actual Commence of Ground Handling time (ACGT) (Milestone 8)."""
        raise NotImplementedError

    def provideArdt(self, flight: Flight) -> None:
        """Provides the Actual Ready Time when the aircraft is ready for start up/push-back (Milestone 12)."""
        raise NotImplementedError


@dataclass
class GroundHandlingStarted(Milestone):
    """Milestone 8: commencement of ground handling operations (ACGT), specific to first-of-day or long-parked flights.

    Package Milestones, stereotype control, milestones [8].
    """

    def checkTobtConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT or ATC Flight Plan."""
        raise NotImplementedError

    def updateTobtTtot(self, flight: Flight) -> None:
        """Updates TOBT, calculated on the basis of the estimated turn-round period for the departing flight."""
        raise NotImplementedError


@dataclass
class Ifps:
    """The Integrated Initial Flight Plan Processing System that distributes the ATC Flight Plan to all involved ATC units.

    Package Systems, stereotype boundary, milestones [1].
    """

    def distributeFlightPlan(self, flightPlan: AtcFlightPlan) -> None:
        """Distributes the ATC Flight Plan submitted by the Aircraft Operator to all involved ATC units including departure and destination aerodromes."""
        raise NotImplementedError


@dataclass
class InBlock(Milestone):
    """Milestone 7: AIBT, the time an aircraft arrives in-blocks; ACGT is considered to commence at AIBT.

    Package Milestones, stereotype control, milestones [7].

    Relationship: dependency 'provided by' -> Acars
    """

    def checkTobtConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT or ATC Flight Plan."""
        raise NotImplementedError

    def updateTobtTtot(self, flight: Flight) -> None:
        """Updates TOBT and TTOT, calculated on the basis of the estimated turn-round period for the departing flight."""
        raise NotImplementedError


@dataclass
class Landed(Milestone):
    """Milestone 6: ALDT, the time an aircraft touches down on a runway.

    Package Milestones, stereotype control, milestones [6].

    Relationship: dependency 'provided by' -> AtcSystem
    """

    def checkTobtConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT or ATC Flight Plan."""
        raise NotImplementedError

    def updateEibt(self, aldt: datetime, exit: timedelta) -> datetime:
        """Updates EIBT according to ALDT + EXIT."""
        raise NotImplementedError

    def informNetworkOperationsIfTtotChanges(self, flight: Flight) -> None:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class LocalRadarUpdate(Milestone):
    """Milestone 4: the flight enters the FIR or local airspace of the destination airport.

    Package Milestones, stereotype control, milestones [4].

    Relationship: dependency 'detected by' -> AtcSystem
    """

    def checkTobtConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given the updated TOBT."""
        raise NotImplementedError

    def computeEibt(self, eldt: datetime, exit: timedelta) -> datetime:
        """Computes EIBT using the ELDT and the estimated taxi-in time (EXIT)."""
        raise NotImplementedError

    def informNetworkOperationsIfTtotChanges(self, flight: Flight) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class MvtMessage:
    """The MVT message sent at Take-Off.

    Package Messages, stereotype boundary, milestones [16].
    """
    pass


@dataclass
class NetworkOperations(CdmPartner):
    """The network management function that issues CTOT, receives DPI messages, and monitors flight progress.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 15].

    Relationship: association 'issues CTOT for' -> Flight [0..*]

    Relationship: dependency 'receives' -> DpiMessage
    """

    def issueCtot(self, flight: Flight) -> datetime:
        """Issues a CTOT at EOBT-2hr to relevant ATS units and the departure aerodrome for regulated flights (Milestone 2)."""
        raise NotImplementedError

    def confirmFlight(self, flight: Flight) -> None:
        """Confirms the flight following consistency checking, allowing further local processing (Milestone 1)."""
        raise NotImplementedError


@dataclass
class OffBlock(Milestone):
    """Milestone 15: AOBT, the time the aircraft pushes back/vacates the parking position.

    Package Milestones, stereotype control, milestones [15].

    Relationship: dependency 'sends' -> ADpiMessage

    Relationship: dependency 'provided by' -> Acars
    """

    def informPartnersOfAobt(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of AOBT and that the aircraft has commenced push-back/taxi from parking position."""
        raise NotImplementedError

    def checkTtotAgainstTolerance(self, flight: Flight) -> None:
        """AOBT always triggers an A-DPI message; after the first A-DPI, checks TTOT updates against the TTOT tolerance before Network Operations is informed with a new A-DPI."""
        raise NotImplementedError


@dataclass
class Outstation(CdmPartner):
    """The departure aerodrome (ADEP) of an inbound flight, which provides the ATOT for that flight.

    Package Stakeholders, stereotype entity, milestones [3].

    Relationship: dependency 'tracked by' -> Etfms
    """

    def provideAtot(self, flight: Flight) -> datetime:
        """Provides the ATOT from the outstation, available with accuracy +/- 1 minute (Milestone 3)."""
        raise NotImplementedError


@dataclass
class ReadyStatusMessage:
    """The Ready Status (RDY) message confirming that the flight follows the indicated TOBT.

    Package Messages, stereotype boundary, milestones [12].
    """
    pass


@dataclass
class ScheduledTime(TimeQuantity):
    """A scheduled-prefix time quantity such as SOBT.

    Package Timings, stereotype entity, milestones [1, 9].
    """
    pass


@dataclass
class StartUpApproved(Milestone):
    """Milestone 14: ASAT, the time an aircraft receives its start-up approval.

    Package Milestones, stereotype control, milestones [14].
    """

    def informPartnersOfAsat(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of ASAT and that the aircraft has received start-up approval/push-back clearance."""
        raise NotImplementedError

    def checkAsatAgainstTsat(self, flight: Flight) -> bool:
        """Checks if ASAT is in accordance with TSAT; if start-up approval is not granted at TSAT + tolerance, all partners are informed and the flight is re-sequenced."""
        raise NotImplementedError


@dataclass
class StartUpRequested(Milestone):
    """Milestone 13: the time that start-up is requested (ASRT), based on pilot request.

    Package Milestones, stereotype control, milestones [13].
    """

    def informPartnersOfAsrt(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of Actual Start-up Request Time (ASRT)."""
        raise NotImplementedError

    def alertIfNoStartUpRequested(self, flight: Flight) -> None:
        """If start-up request is not made by TSAT + tolerance, informs the AO/GH that no start-up has been requested, who should update TOBT."""
        raise NotImplementedError


@dataclass
class TDpiMessage(DpiMessage):
    """The T-DPI message informing Network Operations of the updated take-off time estimate at EOBT-2hr.

    Package Messages, stereotype boundary, milestones [2].
    """
    pass


@dataclass
class TDpiSMessage(DpiMessage):
    """The T-DPI-s message informing Network Operations of the TSAT for non-regulated flights.

    Package Messages, stereotype boundary, milestones [10].
    """
    pass


@dataclass
class TDpiTMessage(DpiMessage):
    """The T-DPI-t message informing Network Operations of updated take-off time estimates at take-off from outstation.

    Package Messages, stereotype boundary, milestones [3].
    """
    pass


@dataclass
class TakeOff(Milestone):
    """Milestone 16: ATOT, the time an aircraft takes off from the runway.

    Package Milestones, stereotype control, milestones [16].

    Relationship: dependency 'sends' -> FsaMessage

    Relationship: dependency 'sends' -> MvtMessage

    Relationship: dependency 'detected by' -> AtcSystem
    """

    def informPartnersOfAtot(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners about the actual take-off."""
        raise NotImplementedError

    def removeFromDepartureSequence(self, flight: Flight) -> None:
        """An airborne message is generated and the flight is removed from the departure sequence."""
        raise NotImplementedError


@dataclass
class TakeOffFromOutstation(Milestone):
    """Milestone 3: the ATOT from the outstation (ADEP) is recorded.

    Package Milestones, stereotype control, milestones [3].

    Relationship: dependency 'sends' -> TDpiTMessage

    Relationship: dependency 'uses' -> FumMessage

    Relationship: dependency 'monitored by' -> Etfms
    """

    def checkLandingEstimateConsistency(self, flight: Flight) -> bool:
        """Checks whether AO/GH estimated landing time after take-off from outstation is consistent with the outbound ATC Flight Plan."""
        raise NotImplementedError

    def calculateEldt(self, atot: datetime, estimatedElapsedTime: timedelta) -> datetime:
        """Calculates ELDT using ATOT and the Estimated Elapsed Time on the FPL."""
        raise NotImplementedError

    def calculateTtot(self, flight: Flight) -> datetime:
        """Calculates TTOT as EIBT+MTTT+EXOT, or EOBT+EXOT if EOBT is later than EIBT+MTTT, or TOBT+EXOT if TOBT is available, respecting a TTOT tolerance of 5 minutes before informing Network Operations."""
        raise NotImplementedError


@dataclass
class TargetTime(TimeQuantity):
    """A target-prefix time quantity such as TOBT, TTOT, TSAT.

    Package Timings, stereotype entity, milestones [2, 3, 4, 5, 6, 7, 8, 9, 10].
    """
    pass


@dataclass
class TsatIssued(Milestone):
    """Milestone 10: the time ATC issues the Target Start-Up Approval Time.

    Package Milestones, stereotype control, milestones [10].

    Relationship: dependency 'sends' -> TDpiSMessage
    """
    localParameterT: timedelta | None = None
    tobtUpdateThreshold: int | None = None

    def informPartnersOfTsat(self, flight: Flight) -> None:
        """Informs all relevant partners of the TSAT allocated to the flight; Network Operations is informed by a T-DPI-s for non-regulated flights."""
        raise NotImplementedError

    def checkTobtUpdateCount(self, flight: Flight) -> bool:
        """Checks whether the number of TOBT updates after TSAT has been issued exceeds a locally defined tolerance."""
        raise NotImplementedError


@dataclass
class TurnRound:
    """An aircraft turn-round normally including an arriving and a departing flight, each with two related flight plans.

    Package Flights, stereotype entity, milestones [1].

    Relationship: composition 'comprises arrival/departing flight' -> Flight [1..2]
    """
    mttt: timedelta | None = None
