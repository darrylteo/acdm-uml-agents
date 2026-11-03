"""Class stubs rendered from runs/single_high/run_04/model.json by src/generate/render_code.py; do not edit by hand."""
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
    DEPARTED_TAKE_OFF = "DEPARTED/TAKE OFF"


@dataclass
class ACARS:
    """The aircraft reporting system (ACARS-equipped aircraft) that provides ON/OFF/IN/OUT signals for landing, in-block, off-block and take-off events.

    Package Systems, stereotype boundary, milestones [6, 7, 15, 16].

    Relationship: dependency 'reports actual times for' -> Flight
    """

    def reportEvent(self, flight: Flight) -> datetime:
        """Reports the actual time of a flight event (ALDT/ACARS=ON, AIBT/ACARS=IN, AOBT/ACARS=OUT, ATOT/ACARS=OFF) with an accuracy of +/-1 minute."""
        raise NotImplementedError


@dataclass
class TimeQuantity:
    """An abstract named time quantity (prefix and event) describing a flight's progress; every successive value is kept with its originator and time of update rather than overwritten.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    value: datetime | None = None
    originator: str | None = None
    accuracy: str | None = None
    timeOfUpdate: datetime | None = None


@dataclass
class ACGT(TimeQuantity):
    """Actual Commence of Ground Handling Time, accuracy +/-1 minute; considered to commence at AIBT for a normal turn-round.

    Package Timings, stereotype entity, milestones [7, 8].
    """
    pass


@dataclass
class AIBT(TimeQuantity):
    """Actual In-Block Time, the time an aircraft arrives in-blocks; ACGT is considered to commence at AIBT, accuracy +/-1 minute.

    Package Timings, stereotype entity, milestones [7].
    """
    pass


@dataclass
class ALDT(TimeQuantity):
    """Actual Landing Time, the time an aircraft touches down, equivalent to ATC ATA, accuracy +/-1 minute.

    Package Timings, stereotype entity, milestones [6].
    """
    pass


@dataclass
class AOBT(TimeQuantity):
    """Actual Off-Block Time, the time the aircraft pushes back or vacates the parking position, accuracy +/-1 minute.

    Package Timings, stereotype entity, milestones [15].
    """
    pass


@dataclass
class ARDT(TimeQuantity):
    """Actual Ready Time, when doors are closed, boarding bridge removed and the aircraft is ready to taxi, accuracy +/-1 minute.

    Package Timings, stereotype entity, milestones [12].
    """
    pass


@dataclass
class ASAT(TimeQuantity):
    """Actual Start-up Approval Time, the time an aircraft receives its start up approval, accuracy +/-1 minute.

    Package Timings, stereotype entity, milestones [14].
    """
    pass


@dataclass
class ASBT(TimeQuantity):
    """Actual Start Boarding Time, when the gate opens for passengers to physically start boarding, accuracy +/-1 minute.

    Package Timings, stereotype entity, milestones [11].
    """
    pass


@dataclass
class ASRT(TimeQuantity):
    """Actual Start-up Request Time, accuracy +/-1 minute.

    Package Timings, stereotype entity, milestones [13].
    """
    pass


@dataclass
class ATCSystem:
    """The ATC/airport detection systems (radar, A-SMGCS, automated docking systems, Tower FDPS) that detect and provide actual times for a flight.

    Package Systems, stereotype boundary, milestones [4, 5, 6, 7, 14, 15, 16].

    Relationship: dependency 'detects/provides actual times for' -> Flight
    """
    accuracy: str | None = None

    def detectFlight(self, flight: Flight) -> datetime:
        """Detects a flight based on the assigned SSR code when it crosses a defined FIR/ATC boundary, range/position, or predetermined level (M4, M5)."""
        raise NotImplementedError


@dataclass
class ATOT(TimeQuantity):
    """Actual Take-Off Time, the time an aircraft takes off from the runway, accuracy +/-1 minute.

    Package Timings, stereotype entity, milestones [3, 16].
    """
    pass


@dataclass
class Stakeholder:
    """An abstract party that takes part in the CDM process and originates or receives its information.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    name: str | None = None
    role: str | None = None


@dataclass
class AirTrafficControl(Stakeholder):
    """The ATC unit(s), including Tower, Approach Control and Area Control Centre, that issue TSAT, approve start-up and manage the pre-departure sequence.

    Package Stakeholders, stereotype entity, milestones [1, 9, 10, 12, 13, 14, 15, 16].

    Relationship: dependency 'issues' -> TSAT

    Relationship: dependency 'grants' -> ASAT
    """

    def issueTSAT(self, flight: Flight) -> TSAT:
        """Issues the Target Start-Up Approval Time t minutes before EOBT, a local parameter (M10)."""
        raise NotImplementedError

    def approveStartUp(self, flight: Flight) -> ASAT:
        """Grants start-up approval/push-back clearance following the pilot's request; if not granted by TSAT+tolerance, partners are informed and the flight is re-sequenced (M14)."""
        raise NotImplementedError


@dataclass
class AirborneMessage:
    """The airborne message generated at take off, after which the flight is removed from the departure sequence.

    Package Messages, stereotype boundary, milestones [16].

    Relationship: dependency 'reports airborne status of' -> Flight
    """
    generatedAt: datetime | None = None


@dataclass
class AircraftOperator(Stakeholder):
    """The airline responsible for a flight, who submits the ATC Flight Plan and provides/confirms TOBT and turn-round information.

    Package Stakeholders, stereotype entity, milestones [1, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13].

    Relationship: dependency 'submits' -> FlightPlan

    Relationship: dependency 'provides/confirms' -> TOBT
    """

    def submitATCFlightPlan(self, flight: Flight) -> None:
        """Submits the ICAO ATC Flight Plan for the flight; correct information must be provided before the first E-DPI, feeding SOBT, aircraft registration and first destination data (M1)."""
        raise NotImplementedError

    def provideTOBT(self, flight: Flight, tobt: TOBT) -> None:
        """Provides or updates the Target Off-Block Time, including the most accurate final TOBT t minutes before EOBT, integrating the AO's own strategy (M4-9)."""
        raise NotImplementedError


@dataclass
class Milestone:
    """The common behaviour of a CDM milestone process: checking TOBT consistency against the ATC Flight Plan and informing Network Operations when TTOT changes beyond the agreed tolerance.

    Package Milestones, stereotype control, milestones [2, 3, 4, 5, 6, 7, 8, 9, 15].

    Relationship: association 'applies to' -> Flight [1]

    Relationship: dependency 'triggers ACISP action on' -> AirportCDMPlatform
    """
    milestoneNumber: int | None = None
    triggerDescription: str | None = None
    operationalStatusChange: OperationalStatus | None = None

    def checkTOBTConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan, to verify feasibility of the ATC Flight Plan given the updated TOBT (M4-9)."""
        raise NotImplementedError

    def informNetworkOperationsOnTTOTChange(self, flight: Flight) -> None:
        """Informs Network Operations when the TTOT changes by more than the agreed TTOT tolerance, which is respected before informing (M2-9, M15)."""
        raise NotImplementedError


@dataclass
class AircraftReady(Milestone):
    """Milestone 12: ARDT, when all doors are closed, boarding bridge removed, push-back vehicle connected, ready to taxi upon TWR instructions.

    Package Milestones, stereotype control, milestones [12].

    Relationship: association 'records' -> ARDT [1]
    """

    def informPartnersOfARDT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of ARDT or Ready Status (RDY), confirming the flight follows the indicated TOBT, triggered by an input to the Airport CDM Platform."""
        raise NotImplementedError

    def checkReadyStatus(self, flight: Flight) -> bool:
        """At TOBT+tolerance, checks whether ARDT/RDY has been received and informs AO/GH that TOBT has passed without a ready status message."""
        raise NotImplementedError


@dataclass
class Aircrew(Stakeholder):
    """The flight crew who coordinate with the Ground Handler during turn-round and request start-up from ATC.

    Package Stakeholders, stereotype entity, milestones [9, 12, 14].
    """

    def requestStartUp(self, flight: Flight) -> None:
        """Requests start up (voice or DCL) just before TSAT, following coordination with the Ground Handler (M12, M14)."""
        raise NotImplementedError


@dataclass
class AirportCDMPlatform:
    """The central Airport CDM Platform, initiated for a flight, that processes available information and performs the ACISP action recorded at each milestone.

    Package Systems, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'processes' -> Flight [0..*]

    Relationship: dependency 'updates (appends new value)' -> TimeQuantity

    Relationship: dependency 'sends' -> DPIMessage
    """

    def processFlightInformation(self, flight: Flight) -> None:
        """Is initiated for the flight and processes all available information (M1)."""
        raise NotImplementedError

    def updateOperationalStatus(self, flight: Flight, status: OperationalStatus) -> None:
        """Updates the flight's operational status as recorded in the 'Operational Status (changes to)' field of each milestone."""
        raise NotImplementedError

    def updateTimeQuantity(self, flight: Flight, quantity: TimeQuantity) -> None:
        """Appends a new value for a time quantity (e.g. ELDT, EIBT, TOBT, TTOT, AOBT, ATOT) as recorded under each milestone's Action on CDM Operation; every successive value is kept rather than overwritten."""
        raise NotImplementedError

    def markAsRegulated(self, flight: Flight) -> None:
        """Marks appropriate fields of the flight as REGULATED when a CTOT is issued at EOBT-2hr (M2)."""
        raise NotImplementedError

    def commenceDPIProcess(self, flight: Flight) -> None:
        """Commences the DPI process with the correct messaging to Network Operations, if implemented (M1)."""
        raise NotImplementedError


@dataclass
class AirportSlot:
    """The airport slot programme entry that the ATC Flight Plan must correspond to.

    Package Flights, stereotype entity, milestones [1].
    """
    slotTime: datetime | None = None
    isCoordinated: bool | None = None


@dataclass
class BoardingStarts(Milestone):
    """Milestone 11: the gate opens for passengers to physically start boarding.

    Package Milestones, stereotype control, milestones [11].

    Relationship: association 'records' -> ASBT [1]
    """

    def informPartnersOfASBT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of the Actual Start Boarding Time when it occurs."""
        raise NotImplementedError

    def checkBoardingStatus(self, flight: Flight) -> bool:
        """At a locally defined time before TOBT (e.g. per aircraft type), checks whether boarding starts in time to respect TOBT and informs AO/GH if TOBT needs updating."""
        raise NotImplementedError


@dataclass
class CTOT(TimeQuantity):
    """Calculated Take-Off Time issued by Network Operations at EOBT-2hr for regulated flights.

    Package Timings, stereotype entity, milestones [2].
    """
    pass


@dataclass
class DPIMessage:
    """A Departure Planning Information message (E-DPI, T-DPI, T-DPI-t, T-DPI-s, or A-DPI) sent to Network Operations with updated flight time estimates.

    Package Messages, stereotype boundary, milestones [1, 2, 3, 10, 15].

    Relationship: association 'sent to' -> NetworkOperations [1]
    """
    type: DPIMessageType | None = None
    timestamp: datetime | None = None


@dataclass
class EIBT(TimeQuantity):
    """Estimated In-Block Time, computed using ELDT+EXIT or ALDT+EXIT.

    Package Timings, stereotype entity, milestones [1, 3, 4, 5, 6, 7].
    """
    pass


@dataclass
class ELDT(TimeQuantity):
    """Estimated Landing Time, updated via FUM, radar detection and ALDT; its accuracy is particularly important at Local Radar Update.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6].
    """
    pass


@dataclass
class EOBT(TimeQuantity):
    """Estimated Off-Block Time, the reference point from which several milestones are timed (e.g. EOBT-3hr, EOBT-2hr).

    Package Timings, stereotype entity, milestones [1, 2, 3, 6, 9, 10].
    """
    pass


@dataclass
class EOBTMinus2Hours(Milestone):
    """Milestone 2: at EOBT-2hr most flights are known and all regulated flights receive a CTOT.

    Package Milestones, stereotype control, milestones [2].

    Relationship: association 'issued for' -> CTOT [0..1]
    """

    def checkFeasibility(self, flight: Flight) -> bool:
        """Checks whether AO/GH flight estimates are consistent with the ATC Flight Plan, verifying feasibility of EOBT at EOBT-2hrs, triggered by a time stamp at EOBT-2h."""
        raise NotImplementedError

    def calculateTTOT(self, flight: Flight) -> datetime:
        """Calculates TTOT taking into account EIBT+MTTT+EXOT if later than EOBT+EXOT; if TOBT is manually input it overrides the EIBT+MTTT estimate, so TTOT equals TOBT+EXOT."""
        raise NotImplementedError

    def sendTDPI(self, flight: Flight) -> None:
        """Informs Network Operations of the updated take-off time estimate via the first T-DPI message at EOBT-2hrs."""
        raise NotImplementedError


@dataclass
class ETFMS:
    """The system Network Operations uses to monitor the progress of a flight within 3hrs flying time of destination.

    Package Systems, stereotype boundary, milestones [3].

    Relationship: association 'used by' -> NetworkOperations [1]
    """

    def monitorFlightProgress(self, flight: Flight) -> None:
        """Monitors progress of the flight and provides updates enabling a Flight Update Message to be sent (M3)."""
        raise NotImplementedError


@dataclass
class ETOT(TimeQuantity):
    """Estimated Take-Off Time, updated for a departure at Flight Plan Activation and at EOBT-2hr.

    Package Timings, stereotype entity, milestones [1, 2].
    """
    pass


@dataclass
class FSAMessage:
    """An FSA message sent upon take off.

    Package Messages, stereotype boundary, milestones [16].

    Relationship: dependency 'reports on' -> Flight
    """
    pass


@dataclass
class FUMMessage:
    """A Flight Update Message sent by Network Operations providing updates of a flight's progress.

    Package Messages, stereotype boundary, milestones [2, 3].

    Relationship: association 'sent by' -> NetworkOperations [1]

    Relationship: dependency 'updates ELDT for' -> Flight
    """
    timestamp: datetime | None = None


@dataclass
class FinalApproach(Milestone):
    """Milestone 5: the flight enters the Final Approach phase at the destination airport, usually 2 to 5 minutes from landing.

    Package Milestones, stereotype control, milestones [5].
    """

    def updateELDTAndTOBT(self, flight: Flight) -> None:
        """Commences the TOBT process on update of ELDT, prompting partners to start moving resources such as parking marshal and ground handling services."""
        raise NotImplementedError


@dataclass
class FinalConfirmationOfTOBT(Milestone):
    """Milestone 9: the time the AO/GH provide their most accurate TOBT, t minutes before EOBT, taking into account the operational situation.

    Package Milestones, stereotype control, milestones [9].

    Relationship: association 'confirms' -> TOBT [1]
    """

    def confirmTOBT(self, flight: Flight) -> None:
        """Confirms TOBT prior to TSAT issue at a predefined local time [EOBT-t minutes]; triggered by a new TOBT or TTOT update, with no need to confirm an existing TOBT manually modified before."""
        raise NotImplementedError

    def calculateEXOT(self, flight: Flight) -> timedelta:
        """The ATC system calculates the Estimated Taxi-Out Time based on predicted traffic load, gate/stand location, runway in use and waiting period at the Holding Position."""
        raise NotImplementedError

    def introduceToPreDepartureSequence(self, flight: Flight) -> None:
        """Introduces the flight into the pre-departure sequence following receipt of TOBT."""
        raise NotImplementedError


@dataclass
class Flight:
    """A single flight leg (arrival or departure) tracked through the CDM process from flight plan activation to take-off.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'described by' -> FlightPlan [0..1]

    Relationship: association 'records' -> TimeQuantity [0..*]
    """
    flightNumber: str | None = None
    aircraftRegistration: str | None = None
    aircraftType: str | None = None
    departureAerodrome: str | None = None
    destinationAerodrome: str | None = None
    direction: str | None = None
    operationalStatus: OperationalStatus | None = None
    isRegulated: bool | None = None
    estimatedElapsedTime: timedelta | None = None
    exot: timedelta | None = None
    exit: timedelta | None = None


@dataclass
class FlightPlan:
    """The ICAO ATC Flight Plan submitted for a flight and distributed by IFPS to involved ATC units.

    Package Flights, stereotype entity, milestones [1].

    Relationship: association 'corresponds to' -> AirportSlot [0..1]
    """
    sobt: SOBT | None = None
    isRepetitive: bool | None = None
    firstDestination: str | None = None


@dataclass
class FlightPlanActivation(Milestone):
    """Milestone 1: the ICAO flight plan is submitted to ATC and the Airport CDM Platform is initiated for the flight.

    Package Milestones, stereotype control, milestones [1].

    Relationship: dependency 'checks consistency of' -> FlightPlan

    Relationship: dependency 'checks consistency of' -> AirportSlot
    """

    def checkConsistency(self, flightPlan: FlightPlan, airportSlot: AirportSlot) -> bool:
        """Checks consistency between the ATC Flight Plan, Airport Slot and Airport flight data before the first E-DPI is sent; triggered by first activation (earliest EOBT-3hr) or new/late/revised submissions."""
        raise NotImplementedError

    def confirmFlightToNetworkOperations(self, flight: Flight) -> None:
        """Confirms the flight to Network Operations and allows further local processing of the flight."""
        raise NotImplementedError

    def sendFirstEDPI(self, flight: Flight) -> None:
        """Sends the first E-DPI with consistent SOBT, aircraft registration and first destination data; should not be sent if information is missing or inconsistent."""
        raise NotImplementedError


@dataclass
class GroundHandler(Stakeholder):
    """The ground handling party that, with the Aircraft Operator, manages the turn-round and provides TOBT and ground status updates.

    Package Stakeholders, stereotype entity, milestones [3, 4, 5, 6, 7, 8, 9, 11, 12].

    Relationship: dependency 'provides/confirms' -> TOBT
    """

    def provideTOBT(self, flight: Flight, tobt: TOBT) -> None:
        """Provides or updates TOBT taking into account the operational situation (M4-9)."""
        raise NotImplementedError

    def reportGroundHandlingStatus(self, flight: Flight) -> None:
        """Reports the commencement of ground handling operations (ACGT) and aircraft readiness (ARDT) (M8, M12)."""
        raise NotImplementedError


@dataclass
class GroundHandlingStarted(Milestone):
    """Milestone 8: ACGT, the commencement of ground handling operations, specific to first-of-day or long-term parked flights.

    Package Milestones, stereotype control, milestones [8].

    Relationship: association 'records' -> ACGT [1]
    """

    def calculateTOBT(self, flight: Flight) -> None:
        """Triggers update of TOBT, automatically or manually by AO/GH, calculated on the basis of the estimated turn-round period for the departing flight."""
        raise NotImplementedError


@dataclass
class IFPS:
    """The system that distributes the submitted ATC Flight Plan to all involved ATC units.

    Package Systems, stereotype boundary, milestones [1].

    Relationship: dependency 'distributes' -> FlightPlan
    """

    def distributeFlightPlan(self, flightPlan: FlightPlan) -> None:
        """Distributes the ATC Flight Plan to all involved ATC units, including departure and destination aerodromes (M1)."""
        raise NotImplementedError


@dataclass
class InBlock(Milestone):
    """Milestone 7: AIBT, the time an aircraft arrives in-blocks; ACGT is considered to commence at AIBT.

    Package Milestones, stereotype control, milestones [7].

    Relationship: association 'records' -> AIBT [1]
    """

    def calculateTOBTAndTTOT(self, flight: Flight) -> None:
        """Triggers update of TOBT and TTOT, automatically or manually by AO/GH, calculated on the basis of the estimated turn-round period for the departing flight."""
        raise NotImplementedError


@dataclass
class Landed(Milestone):
    """Milestone 6: ALDT, the time an aircraft touches down on the runway.

    Package Milestones, stereotype control, milestones [6].

    Relationship: association 'records' -> ALDT [1]
    """

    def calculateEIBT(self, flight: Flight) -> datetime:
        """Updates EIBT according to ALDT+EXIT."""
        raise NotImplementedError

    def calculateTOBTAndTTOT(self, flight: Flight) -> None:
        """Triggers update of TOBT and TTOT, automatically or manually by AO/GH, calculated on the basis of the defined turn-round period for the departing flight."""
        raise NotImplementedError


@dataclass
class LocalRadarUpdate(Milestone):
    """Milestone 4: the flight enters the FIR or local airspace of the destination airport, detected by radar based on assigned SSR code.

    Package Milestones, stereotype control, milestones [4].
    """

    def calculateEIBT(self, flight: Flight) -> datetime:
        """Computes EIBT using the ELDT and the estimated taxi-in time (EXIT)."""
        raise NotImplementedError

    def triggerTOBTUpdate(self, flight: Flight) -> None:
        """Commences the TOBT process: update of ELDT triggers a new TOBT to be entered by AO/GH or calculated automatically; any change to stand/gate is not preferred after ELDT-30'."""
        raise NotImplementedError


@dataclass
class MVTMessage:
    """An MVT message sent upon take off.

    Package Messages, stereotype boundary, milestones [16].

    Relationship: dependency 'reports on' -> Flight
    """
    pass


@dataclass
class NetworkOperations(Stakeholder):
    """The network management party that issues CTOT for regulated flights, distributes flight plan information and receives DPI/FUM messages.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 10, 15].

    Relationship: dependency 'issues' -> CTOT
    """

    def issueCTOT(self, flight: Flight) -> CTOT:
        """Issues the CTOT to relevant ATS units and the departure aerodrome at EOBT-2hr for regulated flights, which take priority over unregulated flights (M2)."""
        raise NotImplementedError

    def monitorFlightProgress(self, flight: Flight) -> None:
        """Monitors progress of a flight within 3hrs flying time of destination using ETFMS and sends a Flight Update Message (M3)."""
        raise NotImplementedError


@dataclass
class OffBlock(Milestone):
    """Milestone 15: AOBT, the time the aircraft pushes back or vacates the parking position.

    Package Milestones, stereotype control, milestones [15].

    Relationship: association 'records' -> AOBT [1]
    """

    def informPartnersOfAOBT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of AOBT when it occurs, that push-back/taxi from parking has commenced."""
        raise NotImplementedError

    def sendADPI(self, flight: Flight) -> None:
        """AOBT always triggers an A-DPI message to Network Operations, or in case of remote holding, at a defined time prior to TTOT."""
        raise NotImplementedError

    def checkTTOTChange(self, flight: Flight) -> bool:
        """After the first A-DPI is sent, checks TTOT updates against the TTOT tolerance before Network Operations is informed with a new A-DPI of the updated TTOT."""
        raise NotImplementedError


@dataclass
class ReadyStatusMessage:
    """A Ready Status (RDY) message confirming that the flight follows the indicated TOBT.

    Package Messages, stereotype boundary, milestones [12].

    Relationship: dependency 'confirms readiness of' -> Flight
    """
    timestamp: datetime | None = None


@dataclass
class SOBT(TimeQuantity):
    """Scheduled Off-Block Time carried on the flight plan and fed to Network Operations via the first E-DPI.

    Package Timings, stereotype entity, milestones [1].
    """
    pass


@dataclass
class StartUpApproved(Milestone):
    """Milestone 14: ASAT, the time an aircraft receives its start up approval.

    Package Milestones, stereotype control, milestones [14].

    Relationship: association 'records' -> ASAT [1]
    """

    def informPartnersOfASAT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of ASAT when it occurs, that the aircraft has received start-up/push-back clearance."""
        raise NotImplementedError

    def checkASATAgainstTSAT(self, flight: Flight) -> bool:
        """Checks if ASAT is in accordance with TSAT; if start-up approval is not granted by TSAT+tolerance, partners are informed and the flight is re-sequenced."""
        raise NotImplementedError


@dataclass
class StartUpRequested(Milestone):
    """Milestone 13: ASRT, the time that start up is requested, based on pilot request.

    Package Milestones, stereotype control, milestones [13].

    Relationship: association 'records' -> ASRT [1]
    """

    def informPartnersOfASRT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of ASRT when it occurs."""
        raise NotImplementedError

    def checkStartUpRequestTimeliness(self, flight: Flight) -> bool:
        """Alerts partners when no start-up has been requested inside the locally agreed TSAT tolerance window; if not requested by TSAT+tolerance, AO/GH is informed to update TOBT."""
        raise NotImplementedError


@dataclass
class TOBT(TimeQuantity):
    """Target Off-Block Time provided and updated by the AO/GH; a final confirmed TOBT is given t minutes before EOBT and is the basis for TSAT.

    Package Timings, stereotype entity, milestones [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13].
    """
    pass


@dataclass
class TSAT(TimeQuantity):
    """Target Start-Up Approval Time, issued by ATC t minutes before EOBT.

    Package Timings, stereotype entity, milestones [10].
    """
    pass


@dataclass
class TSATIssued(Milestone):
    """Milestone 10: the time ATC issues the Target Start-Up Approval Time.

    Package Milestones, stereotype control, milestones [10].

    Relationship: association 'issues' -> TSAT [1]
    """

    def informPartnersOfTSAT(self, flight: Flight) -> None:
        """Informs all relevant partners of the TSAT allocated to the flight, stabilising it into the pre-departure sequence."""
        raise NotImplementedError

    def sendTDPIs(self, flight: Flight) -> None:
        """Informs Network Operations with a T-DPI-s for non-regulated flights."""
        raise NotImplementedError

    def checkTOBTUpdateCount(self, flight: Flight) -> bool:
        """Checks whether the number of TOBT updates after TSAT issue exceeds a locally defined tolerance; if exceeded, TOBT input is processed according to local procedure."""
        raise NotImplementedError


@dataclass
class TTOT(TimeQuantity):
    """Target/calculated Take-Off Time, calculated from EIBT+MTTT+EXOT or TOBT+EXOT, monitored against a tolerance before Network Operations is informed.

    Package Timings, stereotype entity, milestones [2, 3, 4, 5, 6, 7, 8, 9, 10, 15].
    """
    pass


@dataclass
class TakeOff(Milestone):
    """Milestone 16: ATOT, the time an aircraft takes off from the runway.

    Package Milestones, stereotype control, milestones [16].

    Relationship: association 'records' -> ATOT [1]
    """

    def informPartnersOfATOT(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners about the actual take off, triggered by Tower FDPS, A-SMGCS/Radar detection or ACARS."""
        raise NotImplementedError

    def generateAirborneMessage(self, flight: Flight) -> None:
        """Generates an airborne message and removes the flight from the departure sequence."""
        raise NotImplementedError

    def sendFSAAndMVT(self, flight: Flight) -> None:
        """Sends FSA and MVT messages."""
        raise NotImplementedError


@dataclass
class TakeOffFromOutstation(Milestone):
    """Milestone 3: the ATOT from the outstation (ADEP).

    Package Milestones, stereotype control, milestones [3].

    Relationship: association 'records' -> ATOT [1]
    """

    def checkFeasibility(self, flight: Flight) -> bool:
        """Checks whether AO/GH estimated landing time after take off from outstation is consistent with the outbound ATC Flight Plan; a TTOT tolerance of 5 minutes is respected before informing Network Operations."""
        raise NotImplementedError

    def calculateTTOT(self, flight: Flight) -> datetime:
        """Calculates TTOT from EIBT+MTTT+EXOT; if EOBT is later than EIBT+MTTT, TTOT=EOBT+EXOT; if TOBT is available it overrules the EIBT+MTTT estimate, so TTOT=TOBT+EXOT."""
        raise NotImplementedError

    def sendTDPIt(self, flight: Flight) -> None:
        """Informs Network Operations of updated take-off time estimates using a T-DPI-t Message, triggered by take off from outstation."""
        raise NotImplementedError

    def calculateELDT(self, flight: Flight) -> datetime:
        """Calculates ELDT using ATOT and the Estimated Elapsed Time on the FPL, when the departure airport is more than 3hrs flying time from the destination."""
        raise NotImplementedError


@dataclass
class TurnRound:
    """The aircraft turn-round linking an arriving flight and a departing flight of the same aircraft.

    Package Flights, stereotype entity, milestones [1, 2, 3, 6, 7, 8].

    Relationship: aggregation 'arriving flight' -> Flight [0..1]

    Relationship: aggregation 'departing flight' -> Flight [0..1]
    """
    turnRoundPeriod: timedelta | None = None
    mttt: timedelta | None = None
