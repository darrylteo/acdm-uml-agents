"""Class stubs rendered from runs/single/run_01/model.json by src/generate/render_code.py; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from enum import Enum


class FlightDirection(Enum):
    ARRIVAL = "ARRIVAL"
    DEPARTURE = "DEPARTURE"


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


@dataclass
class ACARS:
    """The aircraft communication system that can provide ALDT, AIBT, AOBT and ATOT (ON/IN/OUT/OFF).

    Package Systems, stereotype boundary, milestones [6, 7, 15, 16].

    Relationship: dependency 'provides ALDT for' -> LandedMilestone

    Relationship: dependency 'provides AIBT for' -> InBlockMilestone

    Relationship: dependency 'provides AOBT for' -> OffBlockMilestone

    Relationship: dependency 'provides ATOT for' -> TakeOffMilestone
    """
    pass


@dataclass
class Message:
    """A message exchanged between Airport CDM stakeholders and systems.

    Package Messages, stereotype boundary, milestones [1, 2, 3, 6, 10, 11, 12, 13, 14, 15, 16].
    """
    sender: str | None = None
    timestamp: datetime | None = None


@dataclass
class DPIMessage(Message):
    """A Departure Planning Information message sent to Network Operations at defined points in the DPI process.

    Package Messages, stereotype boundary, milestones [1, 2, 3, 10, 15].
    """
    pass


@dataclass
class ADPIMessage(DPIMessage):
    """The A-DPI message triggered by AOBT and sent to Network Operations when TTOT changes beyond tolerance.

    Package Messages, stereotype boundary, milestones [15].
    """
    pass


@dataclass
class TimeQuantity:
    """A time quantity that describes a flight's progress, with its originator, accuracy and tolerance; every successive value is kept rather than overwritten.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'originated by' -> AirportCDMPartner [1]
    """
    value: datetime | None = None
    originator: AirportCDMPartner | None = None
    timeOfUpdate: datetime | None = None
    accuracy: str | None = None

    def appendValue(self, newValue: datetime, originator: AirportCDMPartner) -> None:
        """Appends a new value with its originator and time of update rather than overwriting, so the turn-round can be analysed afterwards."""
        raise NotImplementedError


@dataclass
class AIBT(TimeQuantity):
    """Actual In-Block Time, the time an aircraft arrives in-blocks, accurate to +/- 1 minute.

    Package Timings, stereotype entity, milestones [7].
    """
    pass


@dataclass
class ALDT(TimeQuantity):
    """Actual Landing Time, the time an aircraft touches down, accurate to +/- 1 minute.

    Package Timings, stereotype entity, milestones [6].
    """
    pass


@dataclass
class AOBT(TimeQuantity):
    """Actual Off-Block Time, the moment the aircraft pushes back/vacates the parking position.

    Package Timings, stereotype entity, milestones [15].
    """
    pass


@dataclass
class ARDT(TimeQuantity):
    """Actual Ready Time, when doors are closed, bridge removed and push-back vehicle connected.

    Package Timings, stereotype entity, milestones [12].
    """
    pass


@dataclass
class ASAT(TimeQuantity):
    """Actual Start-up Approval Time, when the aircraft receives start-up approval.

    Package Timings, stereotype entity, milestones [14].
    """
    pass


@dataclass
class ASBT(TimeQuantity):
    """Actual Start Boarding Time, when the gate opens for passengers to physically board.

    Package Timings, stereotype entity, milestones [11].
    """
    pass


@dataclass
class ASRT(TimeQuantity):
    """Actual Start-up Request Time, when the pilot requests start-up.

    Package Timings, stereotype entity, milestones [13].
    """
    pass


@dataclass
class ATCFlightPlan:
    """The ICAO flight plan submitted by the Aircraft Operator and distributed by the IFPS, against which flight estimates are checked for consistency.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9].

    Relationship: dependency 'checked for consistency with' -> AirportSlot

    Relationship: dependency 'checked for consistency with' -> AirportFlightData
    """
    sobt: datetime | None = None
    departureAerodrome: str | None = None
    destinationAerodrome: str | None = None
    isRepetitive: bool | None = None


@dataclass
class AirportCDMPartner:
    """A party that takes part in the Airport CDM process and originates or receives process information.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    partnerId: str | None = None
    name: str | None = None


@dataclass
class ATCUnit(AirportCDMPartner):
    """An air traffic control unit (ATS, ACC, Approach, or Tower) that provides radar/ATC information and manages the pre-departure sequence.

    Package Stakeholders, stereotype entity, milestones [1, 4, 5, 6, 9, 10, 13, 14, 16].

    Relationship: association 'issues' -> TSAT [*]

    Relationship: association 'calculates' -> EXOT [*]
    """
    pass


@dataclass
class ATOT(TimeQuantity):
    """Actual Take-Off Time, the time an aircraft takes off, accurate to +/- 1 minute.

    Package Timings, stereotype entity, milestones [3, 16].
    """
    pass


@dataclass
class Aircraft:
    """The physical aircraft assigned to a flight, described by type and registration information carried in the ATC Flight Plan.

    Package Flights, stereotype entity, milestones [1].
    """
    registration: str | None = None
    aircraftType: str | None = None


@dataclass
class AircraftOperator(AirportCDMPartner):
    """The airline (AO) that operates the flight, submits the ATC Flight Plan and provides estimates such as TOBT.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12].

    Relationship: dependency 'submits' -> ATCFlightPlan

    Relationship: association 'provides' -> TOBT [*]
    """
    pass


@dataclass
class Milestone:
    """One of the sixteen CDM milestone events, each with a defined trigger, timing rule, effect and procedure that checks and updates flight estimates.

    Package Milestones, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'processes' -> Flight [*]
    """
    trigger: str | None = None
    newOperationalStatus: FlightOperationalStatus | None = None
    accuracy: str | None = None

    def changeOperationalStatus(self, flight: Flight) -> None:
        """Changes the flight's operational status as stated for this milestone."""
        raise NotImplementedError


@dataclass
class AircraftReadyMilestone(Milestone):
    """Milestone 12: all doors closed, boarding bridge removed and push-back vehicle connected, ready to taxi.

    Package Milestones, stereotype control, milestones [12].
    """

    def informPartnersOfARDT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of ARDT/RDY confirming the flight follows the indicated TOBT."""
        raise NotImplementedError

    def checkReadyStatusReceived(self, flight: Flight) -> bool:
        """At TOBT + tolerance, informs the AO/GH that TOBT has passed and no ready status message has yet been received."""
        raise NotImplementedError


@dataclass
class Aircrew(AirportCDMPartner):
    """The flight crew who coordinate with the Ground Handler and request start-up from ATC.

    Package Stakeholders, stereotype entity, milestones [12, 13, 14].
    """
    pass


@dataclass
class AirportCDMPlatform:
    """The central system, initiated for each flight, that holds all available flight information, performs the milestone checks and records the CDM Operation actions (ACISP).

    Package Systems, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'holds and processes information for' -> Flight [*]

    Relationship: association 'executes' -> Milestone [*]

    Relationship: dependency 'commences' -> DPIProcess
    """
    platformId: str | None = None

    def updateELDTAndEOBTData(self, flight: Flight) -> None:
        """M1 ACISP: updates ELDT and EIBT for an arrival, and EOBT and ETOT for a departure."""
        raise NotImplementedError

    def updateETOTTTOTCTOT(self, flight: Flight) -> None:
        """M2 ACISP: updates ETOT/TTOT/CTOT and marks appropriate fields as REGULATED."""
        raise NotImplementedError

    def updateAfterOutstationTakeOff(self, flight: Flight) -> None:
        """M3 ACISP: updates ELDT, EIBT, TOBT and TTOT."""
        raise NotImplementedError

    def updateAfterRadarDetection(self, flight: Flight) -> None:
        """M4 ACISP: updates ELDT, EIBT, TOBT and TTOT."""
        raise NotImplementedError

    def updateAfterFinalApproach(self, flight: Flight) -> None:
        """M5 ACISP: updates ELDT, EIBT, TOBT and TTOT."""
        raise NotImplementedError

    def updateAfterLanding(self, flight: Flight) -> None:
        """M6 ACISP: changes ELDT to ALDT and updates EIBT, TOBT and TTOT."""
        raise NotImplementedError

    def updateAfterInBlock(self, flight: Flight) -> None:
        """M7 ACISP: changes EIBT to AIBT and updates TOBT and TTOT."""
        raise NotImplementedError

    def updateAfterGroundHandlingStart(self, flight: Flight) -> None:
        """M8 ACISP: updates ETTT/TOBT and TTOT."""
        raise NotImplementedError

    def recordAOBT(self, flight: Flight) -> None:
        """M15 ACISP: records AOBT."""
        raise NotImplementedError

    def recordATOT(self, flight: Flight) -> None:
        """M16 ACISP: records ATOT."""
        raise NotImplementedError


@dataclass
class AirportFlightData:
    """The airport's own local flight data used together with the ATC Flight Plan and the Airport Slot to check consistency before the first E-DPI.

    Package Flights, stereotype entity, milestones [1].
    """
    data: str | None = None


@dataclass
class AirportSlot:
    """The airport slot programme entry with which the ATC Flight Plan and airport flight data must be consistent.

    Package Flights, stereotype entity, milestones [1].
    """
    slotTime: datetime | None = None


@dataclass
class BoardingStartsMilestone(Milestone):
    """Milestone 11: the gate opens for passengers to physically start boarding.

    Package Milestones, stereotype control, milestones [11].
    """

    def informPartnersOfASBT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of Actual Start Boarding Time when it occurs."""
        raise NotImplementedError

    def checkBoardingStatus(self, flight: Flight) -> bool:
        """At a locally defined time before TOBT, checks the boarding status and informs the AO/GH if TOBT needs updating."""
        raise NotImplementedError


@dataclass
class CTOT(TimeQuantity):
    """Calculated Take-Off Time issued by Network Operations at EOBT-2h for regulated flights.

    Package Timings, stereotype entity, milestones [2, 3].
    """
    pass


@dataclass
class DPIProcess:
    """The Departure Planning Information process that commences correct messaging with Network Operations if implemented.

    Package Systems, stereotype control, milestones [1, 2, 3, 10, 15].

    Relationship: dependency 'sends messages to' -> NetworkOperations
    """

    def sendEDPI(self, flight: Flight) -> None:
        """Sends the first E-DPI message, not sent if no or inconsistent information is provided; feeds Network Operations with consistent SOBT, aircraft registration and first destination."""
        raise NotImplementedError

    def sendTDPI(self, flight: Flight) -> None:
        """At EOBT-2hrs, informs Network Operations through the first T-DPI message with the updated take-off time estimate."""
        raise NotImplementedError

    def sendTDPIt(self, flight: Flight) -> None:
        """Informs Network Operations about updated take-off time estimates using a T-DPI-t message after outstation take-off, if TTOT tolerance exceeded."""
        raise NotImplementedError

    def sendTDPIs(self, flight: Flight) -> None:
        """Informs Network Operations with a T-DPI-s for non-regulated flights when TSAT is issued."""
        raise NotImplementedError

    def sendADPI(self, flight: Flight) -> None:
        """AOBT always triggers an A-DPI message to Network Operations, or a new A-DPI when TTOT changes beyond tolerance."""
        raise NotImplementedError


@dataclass
class EDPIMessage(DPIMessage):
    """The first E-DPI message, feeding Network Operations with consistent SOBT, aircraft registration and first destination data as early as possible.

    Package Messages, stereotype boundary, milestones [1].
    """
    pass


@dataclass
class EIBT(TimeQuantity):
    """Estimated In-Block Time, computed using ELDT (or ALDT) and the Estimated Taxi-In Time (EXIT).

    Package Timings, stereotype entity, milestones [1, 4, 6, 7].
    """
    pass


@dataclass
class ELDT(TimeQuantity):
    """Estimated Landing Time, updated at flight-plan activation, EOBT-2h, take-off, radar detection and final approach.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6].
    """
    pass


@dataclass
class EOBT(TimeQuantity):
    """Estimated Off-Block Time, the reference against which TOBT and other estimates are compared.

    Package Timings, stereotype entity, milestones [1, 2, 9, 10].
    """
    pass


@dataclass
class EOBTMinus2hMilestone(Milestone):
    """Milestone 2: at EOBT-2hr regulated flights receive a CTOT and estimates are checked against the ATC Flight Plan.

    Package Milestones, stereotype control, milestones [2].
    """

    def checkEstimatesConsistency(self, flight: Flight) -> bool:
        """Checks whether AO/GH flight estimates are consistent with the ATC Flight Plan, verifying feasibility of the estimated off-block time at EOBT-2hrs."""
        raise NotImplementedError

    def calculateTTOT(self, flight: Flight) -> datetime:
        """Calculates TTOT from EIBT+MTTT+EXOT if later than EOBT+EXOT, or TOBT+EXOT if TOBT was manually input, overriding the EIBT+MTTT estimate."""
        raise NotImplementedError

    def markAsRegulated(self, flight: Flight) -> None:
        """Marks appropriate fields as REGULATED for flights that receive a CTOT."""
        raise NotImplementedError


@dataclass
class ETFMS:
    """The Network Operations system that monitors flight progress and generates Flight Update Messages when within 3 hours flying time of destination.

    Package Systems, stereotype boundary, milestones [3].

    Relationship: dependency 'sends' -> FUMMessage
    """

    def monitorProgress(self, flight: Flight) -> None:
        """Monitors progress of the flight and sends a FUM providing updates of the flight's progress."""
        raise NotImplementedError


@dataclass
class ETOT(TimeQuantity):
    """Estimated Take-Off Time, updated for a departure at flight-plan activation.

    Package Timings, stereotype entity, milestones [1, 2].
    """
    pass


@dataclass
class EXIT(TimeQuantity):
    """Estimated Taxi-In Time, used with ELDT/ALDT to compute EIBT and to determine the stand/gate change deadline.

    Package Timings, stereotype entity, milestones [4, 6].
    """
    pass


@dataclass
class EXOT(TimeQuantity):
    """Estimated Taxi-Out Time, calculated by the ATC system from predicted traffic load, gate/stand location, runway in use and holding-position waiting period.

    Package Timings, stereotype entity, milestones [2, 3, 4, 9].
    """
    pass


@dataclass
class FSAMessage(Message):
    """The FSA message sent after take-off.

    Package Messages, stereotype boundary, milestones [16].
    """
    pass


@dataclass
class FUMMessage(Message):
    """The Flight Update Message sent by Network Operations providing updates of the flight's progress, used to update ELDT for inbound flights.

    Package Messages, stereotype boundary, milestones [2, 3].
    """
    pass


@dataclass
class FinalApproachMilestone(Milestone):
    """Milestone 5: the flight enters the Final Approach phase at the destination airport, typically 2 to 5 minutes from landing.

    Package Milestones, stereotype control, milestones [5].
    """

    def commenceTOBTProcess(self, flight: Flight) -> None:
        """Commences the TOBT process and checks whether AO/GH TOBT is consistent with the ATC Flight Plan given updated ELDT."""
        raise NotImplementedError

    def informNetworkOperationsIfTolerated(self, flight: Flight) -> None:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class FinalTOBTConfirmationMilestone(Milestone):
    """Milestone 9: the time at which AO/GH provide their most accurate TOBT, t minutes before EOBT, prior to TSAT issue.

    Package Milestones, stereotype control, milestones [9].
    """

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Checks whether AO/GH TOBT is consistent with the ATC Flight Plan at the predefined local time before TSAT issue, triggered by a new TOBT or TTOT update."""
        raise NotImplementedError

    def calculateEXOT(self, flight: Flight) -> datetime:
        """Following receipt of TOBT, the ATC system calculates EXOT based on predicted traffic load, gate/stand location, runway in use and holding-position waiting period."""
        raise NotImplementedError

    def informNetworkOperationsIfTolerated(self, flight: Flight) -> None:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class Flight:
    """An arriving or departing operation of an aircraft turn-round, tracked through the sixteen CDM milestones with its operational status and time quantities.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'operated with' -> Aircraft [1]

    Relationship: association 'corresponds to' -> ATCFlightPlan [1..*]
    """
    flightId: str | None = None
    direction: FlightDirection | None = None
    operationalStatus: FlightOperationalStatus | None = None
    regulated: bool | None = None
    eobt: EOBT | None = None
    tobt: TOBT | None = None
    aobt: AOBT | None = None
    eldt: ELDT | None = None
    eibt: EIBT | None = None
    aldt: ALDT | None = None
    aibt: AIBT | None = None
    etot: ETOT | None = None
    ttot: TTOT | None = None
    ctot: CTOT | None = None
    atot: ATOT | None = None
    asbt: ASBT | None = None
    ardt: ARDT | None = None
    asrt: ASRT | None = None
    asat: ASAT | None = None
    tsat: TSAT | None = None
    exot: EXOT | None = None
    exit: EXIT | None = None
    mttt: MTTT | None = None


@dataclass
class FlightPlanActivatedMilestone(Milestone):
    """Milestone 1: the ATC Flight Plan is submitted and the Airport CDM Platform is initiated for the flight.

    Package Milestones, stereotype control, milestones [1].
    """

    def checkConsistency(self, flightPlan: ATCFlightPlan, slot: AirportSlot, flightData: AirportFlightData) -> bool:
        """Checks consistency between the ATC Flight Plan, Airport Slot and Airport flight data before the first E-DPI is sent."""
        raise NotImplementedError

    def confirmFlightToNetworkOperations(self, flight: Flight) -> None:
        """Confirms the flight to Network Operations and allows further local processing, triggered by first activation (earliest EOBT-3hr) or new/late submissions after cancellation or revised EOBT."""
        raise NotImplementedError


@dataclass
class GroundHandler(AirportCDMPartner):
    """The Ground Handler (GH) that, with the Aircraft Operator, manages the turn-round and provides estimates such as TOBT and ARDT.

    Package Stakeholders, stereotype entity, milestones [4, 6, 7, 8, 9, 11, 12].

    Relationship: association 'provides' -> TOBT [*]
    """
    pass


@dataclass
class GroundHandlingStartedMilestone(Milestone):
    """Milestone 8: ACGT, the commencement of ground handling operations, specific to first-of-day or long-term-parked flights, triggers an update of TOBT.

    Package Milestones, stereotype control, milestones [8].
    """

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Checks whether AO/GH TOBT is consistent with the ATC Flight Plan given ACGT."""
        raise NotImplementedError

    def informNetworkOperationsIfTolerated(self, flight: Flight) -> None:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class IFPS:
    """The system that distributes the submitted ATC Flight Plan to all involved ATC units.

    Package Systems, stereotype boundary, milestones [1].

    Relationship: dependency 'distributes' -> ATCFlightPlan
    """

    def distributeFlightPlan(self, flightPlan: ATCFlightPlan) -> None:
        """Distributes the ATC Flight Plan submitted by the Aircraft Operator to all involved ATC units."""
        raise NotImplementedError


@dataclass
class InBlockMilestone(Milestone):
    """Milestone 7: AIBT, the time an aircraft arrives in-blocks, triggers an update of downstream estimates.

    Package Milestones, stereotype control, milestones [7].
    """

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Checks whether AO/GH TOBT is consistent with the ATC Flight Plan given AIBT."""
        raise NotImplementedError

    def informNetworkOperationsIfTolerated(self, flight: Flight) -> None:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class LandedMilestone(Milestone):
    """Milestone 6: ALDT, the time an aircraft touches down, triggers an update of downstream estimates.

    Package Milestones, stereotype control, milestones [6].
    """

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Checks whether AO/GH TOBT is consistent with the ATC Flight Plan given ALDT."""
        raise NotImplementedError

    def calculateEIBT(self, aldt: ALDT, exit: EXIT) -> datetime:
        """Updates EIBT according to ALDT+EXIT."""
        raise NotImplementedError

    def informNetworkOperationsIfTolerated(self, flight: Flight) -> None:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class LocalRadarUpdateMilestone(Milestone):
    """Milestone 4: the flight enters the FIR or local airspace, detected by radar via the assigned SSR code.

    Package Milestones, stereotype control, milestones [4].
    """

    def commenceTOBTProcess(self, flight: Flight) -> None:
        """Commences the TOBT process and checks whether AO/GH TOBT is consistent with the ATC Flight Plan, given updated ELDT/EIBT."""
        raise NotImplementedError

    def checkStandGateChangeDeadline(self, flight: Flight) -> bool:
        """Checks that, taking into account EXIT, any stand or gate change is not preferred after ELDT-30 minutes."""
        raise NotImplementedError

    def informNetworkOperationsIfTolerated(self, flight: Flight) -> None:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class MTTT(TimeQuantity):
    """The (minimum/estimated) turn-round period used as the basis for TOBT and TTOT calculation after landing/in-block/ground-handling milestones.

    Package Timings, stereotype entity, milestones [2, 3, 6, 7, 8].
    """
    pass


@dataclass
class MVTMessage(Message):
    """The MVT (movement) message sent after take-off.

    Package Messages, stereotype boundary, milestones [16].
    """
    pass


@dataclass
class NetworkOperations(AirportCDMPartner):
    """The network management function that issues CTOT, receives DPI messages and monitors flight progress via ETFMS.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 15].

    Relationship: association 'issues' -> CTOT [*]

    Relationship: dependency 'monitors flight via' -> ETFMS
    """
    pass


@dataclass
class OffBlockMilestone(Milestone):
    """Milestone 15: AOBT, the time the aircraft pushes back/vacates the parking position.

    Package Milestones, stereotype control, milestones [15].
    """

    def informPartnersOfAOBT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of AOBT and that push-back/taxi has commenced; AOBT always triggers an A-DPI message to Network Operations, or at a defined time prior to TTOT in case of remote holding."""
        raise NotImplementedError

    def checkTTOTToleranceAndInform(self, flight: Flight) -> bool:
        """After the first A-DPI is sent, checks TTOT updates against the TTOT tolerance before Network Operations is informed, with a new A-DPI, of the updated TTOT."""
        raise NotImplementedError


@dataclass
class RadarSystem:
    """The ATC radar system that detects a flight by its assigned SSR code at defined FIR/TMA boundaries or on final approach.

    Package Systems, stereotype boundary, milestones [4, 5].

    Relationship: dependency 'detects flight for' -> LocalRadarUpdateMilestone

    Relationship: dependency 'detects flight for' -> FinalApproachMilestone
    """

    def detectFlight(self, flight: Flight) -> None:
        """Detects the flight crossing a defined FIR/ATC boundary, range/position, or level."""
        raise NotImplementedError


@dataclass
class StartUpApprovedMilestone(Milestone):
    """Milestone 14: ASAT, the time an aircraft receives its start-up approval.

    Package Milestones, stereotype control, milestones [14].
    """

    def informPartnersOfASAT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of Actual Start-up Approval Time and that push-back clearance has been received."""
        raise NotImplementedError

    def checkASATAgainstTSAT(self, flight: Flight) -> bool:
        """Checks if ASAT is in accordance with TSAT; if not granted at TSAT + tolerance, all relevant partners are informed and the flight is re-sequenced."""
        raise NotImplementedError


@dataclass
class StartUpRequestedMilestone(Milestone):
    """Milestone 13: ATC records the time that start-up is requested, based on pilot request.

    Package Milestones, stereotype control, milestones [13].
    """

    def informPartnersOfASRT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of Actual Start-up Request Time when it occurs."""
        raise NotImplementedError

    def alertIfNoStartUpRequest(self, flight: Flight) -> bool:
        """If start-up request is not made by TSAT + tolerance, alerts partners and informs AO/GH that TOBT should be updated."""
        raise NotImplementedError


@dataclass
class TDPIMessage(DPIMessage):
    """The T-DPI message informing Network Operations of the updated take-off time estimate at EOBT-2hrs.

    Package Messages, stereotype boundary, milestones [2].
    """
    pass


@dataclass
class TDPIsMessage(DPIMessage):
    """The T-DPI-s message informing Network Operations of TSAT for non-regulated flights.

    Package Messages, stereotype boundary, milestones [10].
    """
    pass


@dataclass
class TDPItMessage(DPIMessage):
    """The T-DPI-t message informing Network Operations of updated take-off time estimates after outstation take-off.

    Package Messages, stereotype boundary, milestones [3].
    """
    pass


@dataclass
class TOBT(TimeQuantity):
    """Target Off-Block Time provided or confirmed by the AO/GH, used as the basis for TTOT calculation.

    Package Timings, stereotype entity, milestones [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13].
    """
    pass


@dataclass
class TSAT(TimeQuantity):
    """Target Start-Up Approval Time issued by ATC t-minutes before EOBT.

    Package Timings, stereotype entity, milestones [10].
    """
    pass


@dataclass
class TSATIssuedMilestone(Milestone):
    """Milestone 10: ATC issues the Target Start-Up Approval Time, t minutes before EOBT.

    Package Milestones, stereotype control, milestones [10].
    """

    def informPartnersOfTSAT(self, flight: Flight) -> None:
        """Informs all relevant partners of the TSAT allocated to the flight; Network Operations is informed by a T-DPI-s for non-regulated flights."""
        raise NotImplementedError

    def checkTOBTUpdateCount(self, flight: Flight) -> bool:
        """Checks whether the number of TOBT updates after TSAT has been issued exceeds a locally defined tolerance; if exceeded, TOBT input is processed per local procedure."""
        raise NotImplementedError


@dataclass
class TTOT(TimeQuantity):
    """Target Take-Off Time, recalculated at each milestone from EIBT+MTTT+EXOT (or EOBT+EXOT) unless overridden by TOBT+EXOT, and reported to Network Operations when it changes beyond tolerance.

    Package Timings, stereotype entity, milestones [2, 3, 4, 5, 6, 7, 8, 9, 10, 15].
    """
    pass


@dataclass
class TakeOffFromOutstationMilestone(Milestone):
    """Milestone 3: the ATOT from the outstation (ADEP) is provided to Network Operations and the Aircraft Operator.

    Package Milestones, stereotype control, milestones [3].
    """

    def checkEstimatedLandingConsistency(self, flight: Flight) -> bool:
        """Checks whether AO/GH estimated landing time after outstation take-off is consistent with the outbound ATC Flight Plan."""
        raise NotImplementedError

    def calculateELDT(self, atot: ATOT) -> datetime:
        """Calculates ELDT using ATOT and the Estimated Elapsed Time on the FPL."""
        raise NotImplementedError

    def checkTTOTTolerance(self, flight: Flight) -> bool:
        """Respects a TTOT tolerance of 5 minutes before Network Operations is informed of updated TTOT."""
        raise NotImplementedError


@dataclass
class TakeOffMilestone(Milestone):
    """Milestone 16: ATOT, the time an aircraft takes off from the runway.

    Package Milestones, stereotype control, milestones [16].

    Relationship: dependency 'sends' -> FSAMessage

    Relationship: dependency 'sends' -> MVTMessage
    """

    def informPartnersOfATOT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners about the actual take-off, generates an airborne message, and removes the flight from the departure sequence."""
        raise NotImplementedError


@dataclass
class TurnRound:
    """The aircraft turn-round, normally comprising a related arriving and departing flight, analysed afterwards using the recorded successive time values.

    Package Flights, stereotype entity, milestones [1].

    Relationship: composition 'comprises arriving and departing flight' -> Flight [2]
    """
    turnRoundId: str | None = None
