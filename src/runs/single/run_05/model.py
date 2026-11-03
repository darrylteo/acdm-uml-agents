"""Class stubs rendered from runs/single/run_05/model.json by src/generate/render_code.py; do not edit by hand."""
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
    DEPARTED_TAKE_OFF = "DEPARTED/TAKE OFF"


@dataclass
class ACARS:
    """The aircraft communication system that reports ACARS timestamps (ON, IN, OUT, OFF) equivalent to ALDT, AIBT, AOBT and ATOT.

    Package Systems, stereotype boundary, milestones [6, 7, 15, 16].
    """
    pass


@dataclass
class TimeQuantity:
    """An abstract time quantity (a prefix such as Scheduled, Estimated, Target, Actual, or Calculated applied to an event) that keeps every successive value with its originator and time of update.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    value: datetime | None = None
    originator: str | None = None
    updateTime: datetime | None = None
    accuracy: str | None = None

    def recordUpdate(self, newValue: datetime, originator: str, updateTime: datetime) -> None:
        """Appends a new value rather than overwriting the previous one, so a turn-round can be analysed afterwards."""
        raise NotImplementedError


@dataclass
class ACGT(TimeQuantity):
    """Actual Commence of Ground Handling Time, provided by the Aircraft Operator/Ground Handler with accuracy of +/- 1 minute, applicable to first-of-day or long-parked flights.

    Package Timings, stereotype entity, milestones [8].
    """
    pass


@dataclass
class AIBT(TimeQuantity):
    """Actual In-Block Time, the time the aircraft arrives in-blocks, available with accuracy of +/- 1 minute; ACGT is considered to commence at AIBT for normal turn-rounds.

    Package Timings, stereotype entity, milestones [7, 8].
    """
    pass


@dataclass
class ALDT(TimeQuantity):
    """Actual Landing Time, the time the aircraft touches down, available with accuracy of +/- 1 minute.

    Package Timings, stereotype entity, milestones [6].
    """
    pass


@dataclass
class AOBT(TimeQuantity):
    """Actual Off-Block Time, the time the aircraft pushes back/vacates the parking position, available with accuracy of +/- 1 minute.

    Package Timings, stereotype entity, milestones [15].
    """
    pass


@dataclass
class ARDT(TimeQuantity):
    """Actual Ready Time, when doors are closed, boarding bridge removed and push-back vehicle connected, provided by the Aircraft Operator/Ground Handler with accuracy of +/- 1 minute.

    Package Timings, stereotype entity, milestones [12, 13].
    """
    pass


@dataclass
class ASAT(TimeQuantity):
    """Actual Start-up Approval Time, the time the aircraft receives its start-up approval, available with accuracy of +/- 1 minute.

    Package Timings, stereotype entity, milestones [14, 15].
    """
    pass


@dataclass
class ASBT(TimeQuantity):
    """Actual Start Boarding Time, the time the gate opens for physical boarding, available with accuracy of +/- 1 minute.

    Package Timings, stereotype entity, milestones [11].
    """
    pass


@dataclass
class ASRT(TimeQuantity):
    """Actual Start-up Request Time, the time start-up is requested by the pilot, available with accuracy of +/- 1 minute.

    Package Timings, stereotype entity, milestones [13, 14].
    """
    pass


@dataclass
class ATCSystem:
    """The ATC system (e.g. A-SMGCS, Tower FDPS) that detects milestones such as landing, in-block, and take off, and provides data at the accuracy of the ATC system.

    Package Systems, stereotype boundary, milestones [4, 5, 6, 7, 16].
    """
    pass


@dataclass
class Stakeholder:
    """An abstract party that takes part in the Airport CDM process and originates or receives its information.

    Package Stakeholders, stereotype entity, milestones [1].
    """
    name: str | None = None
    role: str | None = None


@dataclass
class ATCUnit(Stakeholder):
    """An Air Traffic Control unit that receives the flight plan, issues TSAT, grants start-up approval, and detects milestones via ATC systems.

    Package Stakeholders, stereotype entity, milestones [1, 2, 4, 5, 9, 10, 12, 13, 14, 16].

    Relationship: association 'receives' -> FlightPlan [1]

    Relationship: association 'issues' -> TSAT [*]

    Relationship: association 'grants' -> ASAT [*]

    Relationship: association 'operates' -> ATCSystem [1]

    Relationship: association 'uses' -> RadarSystem [1]
    """
    pass


@dataclass
class ATOT(TimeQuantity):
    """Actual Take-Off Time, provided by ATC or ACARS at take-off from the outstation or from this airport, with accuracy of +/- 1 minute.

    Package Timings, stereotype entity, milestones [3, 16].
    """
    pass


@dataclass
class Aerodrome:
    """A departure or destination aerodrome, which may be coordinated (slot-controlled) or non-coordinated.

    Package Flights, stereotype entity, milestones [1].
    """
    icaoCode: str | None = None
    coordinated: bool | None = None


@dataclass
class Aircraft:
    """The physical aircraft operating a flight, whose type and registration may be updated from the flight plan.

    Package Flights, stereotype entity, milestones [1].

    Relationship: association 'equipped with' -> ACARS [0..1]
    """
    registration: str | None = None
    type: str | None = None


@dataclass
class AircraftCrew(Stakeholder):
    """The pilot and crew who request start-up and coordinate with the Ground Handler during the turn-round.

    Package Stakeholders, stereotype entity, milestones [12, 13, 14].

    Relationship: association 'requests' -> ASRT [*]
    """
    pass


@dataclass
class AircraftOperator(Stakeholder):
    """The airline or operator that submits the ATC Flight Plan and provides TOBT and other operational inputs for a flight.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13].

    Relationship: dependency 'submits' -> FlightPlan

    Relationship: association 'provides' -> TOBT [*]
    """
    pass


@dataclass
class Milestone:
    """An abstract CDM milestone event with its trigger, timing rule, effect, and procedure.

    Package Milestones, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'applies to' -> Flight [1..*]
    """
    trigger: str | None = None
    timingRule: str | None = None
    effect: str | None = None
    resultingStatus: FlightStatus | None = None


@dataclass
class AircraftReady(Milestone):
    """Milestone 12: doors closed, boarding bridge removed, push-back vehicle connected, ready to taxi (ARDT).

    Package Milestones, stereotype control, milestones [12].
    """

    def informPartnersOfARDT(self) -> None:
        """Informs all relevant Airport CDM Partners of ARDT/RDY in the Airport CDM Platform, confirming the flight follows the indicated TOBT."""
        raise NotImplementedError

    def checkReadyStatusReceived(self) -> bool:
        """At TOBT + tolerance, checks whether ARDT/RDY has been received and informs the AO/GH that TOBT has passed if not."""
        raise NotImplementedError


@dataclass
class AirportCDMPlatform:
    """The Airport CDM Platform that is initiated for each flight, processes all available information, and carries out the ACISP actions defined at each milestone.

    Package Systems, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 16].

    Relationship: association 'processes information for' -> Flight [*]

    Relationship: dependency 'sends' -> DPIMessage

    Relationship: dependency 'receives' -> FUM

    Relationship: dependency 'sends' -> MVTMessage

    Relationship: dependency 'sends' -> FSAMessage

    Relationship: association 'executes' -> Milestone [1..*]
    """

    def processFlightInformation(self, flight: Flight) -> None:
        """Initiates the platform for the flight and processes all available information (m1)."""
        raise NotImplementedError

    def updateELDTAndEIBTForArrival(self, flight: Flight) -> None:
        """Updates ELDT and EIBT for an arrival and ETOT for a departure (m1)."""
        raise NotImplementedError

    def markAsRegulated(self, flight: Flight) -> None:
        """Marks the appropriate fields as REGULATED and updates ETOT/TTOT/CTOT at EOBT-2hr (m2)."""
        raise NotImplementedError

    def updateTimingsOnProgress(self, flight: Flight) -> None:
        """Updates ELDT, EIBT, TOBT and TTOT following take-off from outstation, local radar update, and final approach (m3,4,5)."""
        raise NotImplementedError

    def updateOnLanding(self, flight: Flight) -> None:
        """Changes ELDT to ALDT and updates EIBT, TOBT and TTOT on landing (m6)."""
        raise NotImplementedError

    def updateOnInBlock(self, flight: Flight) -> None:
        """Changes EIBT to AIBT and updates TOBT and TTOT on in-block (m7)."""
        raise NotImplementedError

    def updateOnGroundHandlingStart(self, flight: Flight) -> None:
        """Updates ETTT/TOBT and TTOT on commencement of ground handling (m8)."""
        raise NotImplementedError

    def updateTTOTOnTSAT(self, flight: Flight) -> None:
        """Updates TTOT when TSAT is issued (m10)."""
        raise NotImplementedError

    def recordAOBT(self, flight: Flight) -> None:
        """Records AOBT on off-block (m15)."""
        raise NotImplementedError

    def recordATOT(self, flight: Flight) -> None:
        """Records ATOT on take off (m16)."""
        raise NotImplementedError


@dataclass
class AirportSlot:
    """The airport slot programme entry with which the ATC Flight Plan and airport flight data must be consistent.

    Package Flights, stereotype entity, milestones [1].
    """
    programmeReference: str | None = None


@dataclass
class BoardingStarts(Milestone):
    """Milestone 11: the gate opens for passengers to physically start boarding.

    Package Milestones, stereotype control, milestones [11].
    """

    def informPartnersOfASBT(self) -> None:
        """Informs all relevant Airport CDM Partners of the Actual Start Boarding Time when it occurs."""
        raise NotImplementedError

    def checkBoardingStatus(self) -> bool:
        """At a locally defined time before TOBT, checks whether boarding starts in time to respect TOBT and informs the AO/GH if TOBT needs updating."""
        raise NotImplementedError


@dataclass
class CTOT(TimeQuantity):
    """Calculated Take-Off Time issued by Network Operations to regulated flights at EOBT-2hr.

    Package Timings, stereotype entity, milestones [2].
    """
    pass


@dataclass
class DPIMessage:
    """A Departure Planning Information message (E-DPI, T-DPI, T-DPI-t, T-DPI-s, or A-DPI) exchanged between the Airport CDM Platform and Network Operations.

    Package Messages, stereotype boundary, milestones [1, 2, 3, 10, 15].
    """
    type: DPIMessageType | None = None
    sentTime: datetime | None = None


@dataclass
class EIBT(TimeQuantity):
    """Estimated In-Block Time, computed from ELDT plus the estimated taxi-in time (EXIT), or ALDT plus EXIT after landing.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7].
    """
    pass


@dataclass
class ELDT(TimeQuantity):
    """Estimated Landing Time, whose accuracy is particularly important since downstream decisions depend on it; stand/gate changes are not preferred after ELDT-30'.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6].
    """
    pass


@dataclass
class EOBT(TimeQuantity):
    """Estimated Off-Block Time on the ATC Flight Plan, the reference point for milestone timings such as EOBT-3hr, EOBT-2hr and EOBT-t minutes.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 6, 9, 10].
    """
    pass


@dataclass
class EOBTMinus2hr(Milestone):
    """Milestone 2: at EOBT-2hr regulated flights receive a CTOT and estimates are checked against the ATC Flight Plan.

    Package Milestones, stereotype control, milestones [2].
    """

    def checkEstimatesConsistency(self) -> bool:
        """Checks whether AO/GH flight estimates are consistent with the ATC Flight Plan at EOBT-2hrs."""
        raise NotImplementedError

    def sendTDPI(self) -> None:
        """Informs Network Operations of the updated take-off time estimate using a T-DPI message at EOBT-2hrs."""
        raise NotImplementedError

    def calculateTTOT(self) -> datetime:
        """Calculates TTOT taking into account EIBT+MTTT+EXOT if later than EOBT+EXOT; a manually input TOBT overrides this, so TTOT equals TOBT+EXOT."""
        raise NotImplementedError


@dataclass
class ETFMS:
    """The system by which Network Operations monitors the progress of a flight within 3 hours flying time of the destination airport.

    Package Systems, stereotype boundary, milestones [3].
    """
    pass


@dataclass
class ETOT(TimeQuantity):
    """Estimated Take-Off Time, updated for a departure at ATC Flight Plan activation.

    Package Timings, stereotype entity, milestones [1, 2].
    """
    pass


@dataclass
class EXIT(TimeQuantity):
    """Estimated Taxi-In Time, used together with ELDT or ALDT to compute EIBT.

    Package Timings, stereotype entity, milestones [4, 6].
    """
    pass


@dataclass
class EXOT(TimeQuantity):
    """Estimated Taxi-Out Time, calculated by the ATC system from TOBT based on predicted traffic load, gate/stand location, runway in use and waiting period at the holding position.

    Package Timings, stereotype entity, milestones [2, 3, 9].
    """
    pass


@dataclass
class FSAMessage:
    """A flight status/airborne message sent on take off.

    Package Messages, stereotype boundary, milestones [16].
    """
    pass


@dataclass
class FUM:
    """The Flight Update Message sent by Network Operations, providing updates of a flight's progress, including ATOT and ELDT information.

    Package Messages, stereotype boundary, milestones [2, 3].
    """
    pass


@dataclass
class FinalApproach(Milestone):
    """Milestone 5: the flight enters the Final Approach phase, updating ELDT and triggering a new TOBT.

    Package Milestones, stereotype control, milestones [5].
    """

    def commenceTOBTProcess(self) -> None:
        """Commences the TOBT process and checks whether the AO/GH TOBT is consistent with the ATC Flight Plan."""
        raise NotImplementedError

    def informNetworkOperationsIfTTOTChanged(self) -> None:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class FinalConfirmationOfTOBT(Milestone):
    """Milestone 9: the Aircraft Operator/Ground Handler provides their most accurate TOBT, t minutes before EOBT, prior to TSAT issue.

    Package Milestones, stereotype control, milestones [9].
    """

    def checkTOBTConsistency(self) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan; triggered by a new TOBT or TTOT update."""
        raise NotImplementedError

    def confirmTOBT(self) -> None:
        """Performed at a predefined local time to confirm TOBT prior to TSAT issue; no need to confirm an existing TOBT if manually modified before."""
        raise NotImplementedError

    def informNetworkOperationsIfTTOTChanged(self) -> None:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError

    def calculateEXOT(self) -> datetime:
        """Calculates the Estimated Taxi-Out Time based on predicted traffic load, gate/stand location, runway in use and waiting period at the Holding Position."""
        raise NotImplementedError


@dataclass
class Flight:
    """A single arrival or departure operation of an aircraft, tracked through the sixteen milestones with an operational status and associated time quantities.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: association 'described by' -> FlightPlan [1]

    Relationship: association 'operated by' -> Aircraft [1]

    Relationship: association 'corresponds to' -> AirportSlot [0..1]

    Relationship: association 'departs from' -> Aerodrome [1]

    Relationship: association 'arrives at' -> Aerodrome [1]

    Relationship: association 'has history of' -> EOBT [*]

    Relationship: association 'has history of' -> TOBT [*]

    Relationship: association 'has history of' -> AOBT [*]

    Relationship: association 'has history of' -> ELDT [*]

    Relationship: association 'has history of' -> ALDT [*]

    Relationship: association 'has history of' -> EIBT [*]

    Relationship: association 'has history of' -> AIBT [*]

    Relationship: association 'has history of' -> ETOT [*]

    Relationship: association 'has history of' -> TTOT [*]

    Relationship: association 'has history of' -> CTOT [*]

    Relationship: association 'has history of' -> ATOT [*]

    Relationship: association 'has history of' -> ASBT [*]

    Relationship: association 'has history of' -> ARDT [*]

    Relationship: association 'has history of' -> ASRT [*]

    Relationship: association 'has history of' -> ASAT [*]

    Relationship: association 'has history of' -> TSAT [*]

    Relationship: association 'has history of' -> ACGT [*]

    Relationship: association 'has history of' -> EXOT [*]

    Relationship: association 'has history of' -> EXIT [*]
    """
    flightNumber: str | None = None
    direction: FlightDirection | None = None
    operationalStatus: FlightStatus | None = None
    regulated: bool | None = None


@dataclass
class FlightPlan:
    """The ATC Flight Plan submitted by the Aircraft Operator and distributed by IFPS, describing SOBT, aircraft, and destination data for a flight.

    Package Flights, stereotype entity, milestones [1].

    Relationship: association 'has history of' -> SOBT [*]
    """
    firstDestination: str | None = None
    isRFPL: bool | None = None


@dataclass
class FlightPlanActivation(Milestone):
    """Milestone 1: the ICAO ATC Flight Plan is submitted and the Airport CDM Platform is initiated for the flight.

    Package Milestones, stereotype control, milestones [1].
    """

    def checkConsistency(self, flightPlan: FlightPlan, slot: AirportSlot) -> bool:
        """Checks consistency between ATC Flight Plan, Airport Slot and Airport flight data before the first E-DPI is sent."""
        raise NotImplementedError

    def confirmFlightToNetworkOperations(self) -> None:
        """Confirms the flight to Network Operations and allows further local processing of the flight."""
        raise NotImplementedError

    def sendEDPI(self) -> None:
        """Sends the first E-DPI message, feeding Network Operations with consistent SOBT, aircraft registration and first destination data; should not be sent if information is missing or inconsistent."""
        raise NotImplementedError

    def checkFlightReadyWithin15Minutes(self) -> bool:
        """Checks that the flight is ready not later than 15 minutes after the planned EOBT."""
        raise NotImplementedError


@dataclass
class GroundHandler(Stakeholder):
    """The party that carries out ground handling operations and, jointly with or in place of the Aircraft Operator, provides TOBT, ARDT and other turn-round inputs.

    Package Stakeholders, stereotype entity, milestones [6, 7, 8, 9, 10, 11, 12, 13].

    Relationship: association 'reports' -> ARDT [*]

    Relationship: association 'provides' -> TOBT [*]
    """
    pass


@dataclass
class GroundHandlingStarted(Milestone):
    """Milestone 8: commencement of ground handling operations (ACGT), triggering a TOBT update for first-of-day or long-parked flights.

    Package Milestones, stereotype control, milestones [8].
    """

    def checkTOBTConsistency(self) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given ACGT."""
        raise NotImplementedError

    def informNetworkOperationsIfTTOTChanged(self) -> None:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class IFPS:
    """The system that distributes the submitted ATC Flight Plan to all involved ATC units.

    Package Systems, stereotype boundary, milestones [1].

    Relationship: dependency 'distributes' -> FlightPlan
    """
    pass


@dataclass
class InBlock(Milestone):
    """Milestone 7: AIBT is recorded, triggering an automatic or manual update of TOBT and TTOT.

    Package Milestones, stereotype control, milestones [7].
    """

    def checkTOBTConsistency(self) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given AIBT."""
        raise NotImplementedError

    def informNetworkOperationsIfTTOTChanged(self) -> None:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError


@dataclass
class Landed(Milestone):
    """Milestone 6: ALDT is recorded, triggering an update of downstream estimates.

    Package Milestones, stereotype control, milestones [6].
    """

    def checkTOBTConsistency(self) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan given ALDT."""
        raise NotImplementedError

    def informNetworkOperationsIfTTOTChanged(self) -> None:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError

    def updateEIBT(self) -> datetime:
        """Updates EIBT according to ALDT + EXIT."""
        raise NotImplementedError


@dataclass
class LocalRadarUpdate(Milestone):
    """Milestone 4: the flight enters the FIR or local airspace of the destination airport, triggering a TOBT update.

    Package Milestones, stereotype control, milestones [4].
    """

    def commenceTOBTProcess(self) -> None:
        """Commences the TOBT process and checks whether the AO/GH TOBT is consistent with the ATC Flight Plan."""
        raise NotImplementedError

    def informNetworkOperationsIfTTOTChanged(self) -> None:
        """Informs Network Operations when TTOT changes by more than the agreed TTOT tolerance."""
        raise NotImplementedError

    def computeEIBT(self) -> datetime:
        """Computes EIBT using ELDT and the estimated taxi-in time (EXIT)."""
        raise NotImplementedError


@dataclass
class MTTT(TimeQuantity):
    """The (minimum/estimated) turn-round period used, together with EIBT and EXOT, to calculate TTOT and TOBT for the departing flight.

    Package Timings, stereotype entity, milestones [2, 3, 6, 7, 8].
    """
    pass


@dataclass
class MVTMessage:
    """A movement message sent on take off.

    Package Messages, stereotype boundary, milestones [16].
    """
    pass


@dataclass
class NetworkOperations(Stakeholder):
    """The network management function (e.g. via IFPS/ETFMS) that issues the CTOT, monitors flight progress, and receives DPI/FUM messages.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 10, 15].

    Relationship: association 'issues' -> CTOT [*]

    Relationship: dependency 'receives' -> DPIMessage

    Relationship: dependency 'sends' -> FUM

    Relationship: association 'monitors flight via' -> ETFMS [1]
    """
    pass


@dataclass
class OffBlock(Milestone):
    """Milestone 15: AOBT, the time the aircraft pushes back/vacates the parking position.

    Package Milestones, stereotype control, milestones [15].
    """

    def informPartnersOfAOBT(self) -> None:
        """Informs all relevant Airport CDM Partners of AOBT when it occurs."""
        raise NotImplementedError

    def sendADPI(self) -> None:
        """AOBT always triggers an A-DPI message to Network Operations, or at a defined time prior to TTOT in case of remote holding."""
        raise NotImplementedError

    def checkTTOTChangeExceedsTolerance(self) -> bool:
        """After the first A-DPI is sent, checks TTOT updates against the TTOT tolerance before Network Operations is informed with a new A-DPI."""
        raise NotImplementedError


@dataclass
class RadarSystem:
    """The radar system that detects a flight based on its assigned SSR code when it crosses a defined FIR/ATC boundary, range/position, or level.

    Package Systems, stereotype boundary, milestones [4, 5].
    """
    pass


@dataclass
class SOBT(TimeQuantity):
    """Scheduled Off-Block Time, part of the consistent flight plan data (SOBT, aircraft registration, first destination) fed to Network Operations before the first E-DPI.

    Package Timings, stereotype entity, milestones [1].
    """
    pass


@dataclass
class StartUpApproved(Milestone):
    """Milestone 14: the time the aircraft receives its start-up approval (ASAT).

    Package Milestones, stereotype control, milestones [14].
    """

    def informPartnersOfASAT(self) -> None:
        """Informs all relevant Airport CDM Partners of ASAT when it occurs, confirming start-up/push-back clearance."""
        raise NotImplementedError

    def checkASATConsistencyWithTSAT(self) -> bool:
        """Checks if ASAT is in accordance with TSAT; if not granted at TSAT + tolerance, all relevant partners are informed and the flight is re-sequenced."""
        raise NotImplementedError


@dataclass
class StartUpRequested(Milestone):
    """Milestone 13: the time start-up is requested by the pilot (ASRT).

    Package Milestones, stereotype control, milestones [13].
    """

    def informPartnersOfASRT(self) -> None:
        """Informs all relevant Airport CDM Partners of ASRT when it occurs."""
        raise NotImplementedError

    def checkStartUpRequestedInTime(self) -> bool:
        """Alerts all relevant Airport CDM Partners when no start-up has been requested inside the locally agreed TSAT tolerance window; the AO/GH is informed to update TOBT."""
        raise NotImplementedError


@dataclass
class TOBT(TimeQuantity):
    """Target Off-Block Time provided or updated by the Aircraft Operator/Ground Handler, checked for consistency with the ATC Flight Plan at every milestone and confirmed before TSAT issue.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13].
    """
    pass


@dataclass
class TSAT(TimeQuantity):
    """Target Start-Up Approval Time issued by ATC t minutes before EOBT, with locally agreed accuracy, stabilising the flight into the pre-departure sequence.

    Package Timings, stereotype entity, milestones [10, 11, 12, 13, 14].
    """
    pass


@dataclass
class TSATIssued(Milestone):
    """Milestone 10: ATC issues the Target Start-Up Approval Time, stabilising the flight into the pre-departure sequence.

    Package Milestones, stereotype control, milestones [10].
    """

    def informPartnersOfTSAT(self) -> None:
        """Informs all relevant partners of the TSAT allocated to the flight; Network Operations is informed by a T-DPI-s for non-regulated flights."""
        raise NotImplementedError

    def checkTOBTUpdateCount(self) -> bool:
        """Checks whether the number of TOBT updates after TSAT issue exceeds a locally defined tolerance; if exceeded, the TOBT input is processed per local procedure."""
        raise NotImplementedError


@dataclass
class TTOT(TimeQuantity):
    """Target Take-Off Time, calculated on the basis of EIBT+MTTT+EXOT (or TOBT+EXOT when TOBT is available), monitored against an agreed tolerance before Network Operations is informed.

    Package Timings, stereotype entity, milestones [2, 3, 4, 5, 6, 7, 8, 9, 10, 15].
    """
    pass


@dataclass
class TakeOff(Milestone):
    """Milestone 16: ATOT, the time the aircraft takes off from the runway.

    Package Milestones, stereotype control, milestones [16].
    """

    def informPartnersOfATOT(self) -> None:
        """Informs all relevant Airport CDM Partners about the actual take off."""
        raise NotImplementedError

    def generateAirborneMessage(self) -> None:
        """Generates an airborne message and sends FSA and MVT messages."""
        raise NotImplementedError

    def removeFromDepartureSequence(self) -> None:
        """Removes the flight from the departure sequence."""
        raise NotImplementedError


@dataclass
class TakeOffFromOutstation(Milestone):
    """Milestone 3: the ATOT from the outstation (ADEP), used to update landing and take-off estimates.

    Package Milestones, stereotype control, milestones [3].
    """

    def checkLandingTimeConsistency(self) -> bool:
        """Checks whether AO/GH estimated landing times after take-off from outstation are consistent with the outbound ATC Flight Plan."""
        raise NotImplementedError

    def sendTDPIt(self) -> None:
        """Informs Network Operations about updated take-off time estimates using a T-DPI-t message when a TTOT tolerance of 5 minutes is exceeded."""
        raise NotImplementedError

    def calculateTTOT(self) -> datetime:
        """Calculates TTOT from EIBT+MTTT+EXOT; if EOBT is later than EIBT+MTTT, TTOT equals EOBT+EXOT; if TOBT is available it overrules, so TTOT equals TOBT+EXOT."""
        raise NotImplementedError


@dataclass
class TurnRound:
    """The aircraft turn-round comprising the arriving and the departing flight of the same aircraft, used to analyse the process afterwards.

    Package Flights, stereotype entity, milestones [1].

    Relationship: composition 'comprises arriving and departing flight' -> Flight [2]

    Relationship: association 'has history of' -> MTTT [*]
    """
    pass
