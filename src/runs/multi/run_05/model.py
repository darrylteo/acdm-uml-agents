"""Class stubs rendered from runs/multi/run_05/model.json by src/generate/render_code.py; do not edit by hand."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from enum import Enum


class DpiType(Enum):
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
class AcarsSystem:
    """The Aircraft Communications Addressing and Reporting System that provides ON/IN/OFF markers used for ALDT, AIBT, AOBT and ATOT.

    Package Systems, stereotype boundary, milestones [6, 7, 15, 16].

    Relationship: dependency 'provides' -> Aldt

    Relationship: dependency 'provides' -> Aibt

    Relationship: dependency 'provides' -> Aobt

    Relationship: dependency 'provides' -> Atot
    """
    pass


@dataclass
class TimeQuantity:
    """An abstract time value describing a flight's progress, identified by a prefix (Scheduled, Estimated, Target, Actual, Calculated) and an event, with an originator, accuracy and update history.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    value: datetime | None = None
    originator: str | None = None
    accuracy: timedelta | None = None
    recordedAt: datetime | None = None


@dataclass
class Acgt(TimeQuantity):
    """The Actual Commence of Ground Handling Time, considered equal to AIBT for a normal turn-round.

    Package Timings, stereotype entity, milestones [7, 8].
    """
    accuracy: timedelta | None = None

    def deriveFromAibt(self, aibt: Aibt) -> datetime:
        """ACGT is considered to commence at AIBT for a normal turn-round (milestone 7)."""
        raise NotImplementedError


@dataclass
class Aibt(TimeQuantity):
    """The Actual In-Block Time recorded when the aircraft arrives in-blocks, with an accuracy of plus or minus one minute.

    Package Timings, stereotype entity, milestones [7, 8].
    """
    accuracy: timedelta | None = None


@dataclass
class AirportCDMPartner:
    """An abstract party that takes part in the Airport CDM process, originating or receiving flight information.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    pass


@dataclass
class AirTrafficControlUnit(AirportCDMPartner):
    """An air traffic control unit, including ACC and Approach Control, that manages the aircraft's progress and issues clearances such as TSAT and start-up approval.

    Package Stakeholders, stereotype entity, milestones [1, 4, 5, 9, 10, 12, 13, 14, 15, 16].
    """
    pass


@dataclass
class AirborneMessage:
    """The message generated at take-off indicating the flight is airborne and to be removed from the departure sequence.

    Package Messages, stereotype boundary, milestones [16].
    """
    pass


@dataclass
class Aircraft:
    """The physical aircraft operating a flight, whose type and registration are recorded and used in flight plan consistency checks.

    Package Flights, stereotype entity, milestones [1].
    """
    aircraftType: str | None = None
    registration: str | None = None

    def updateAircraftType(self, aircraftType: str) -> None:
        """The flight plan may be used to update certain information such as type of aircraft (milestone 1)."""
        raise NotImplementedError


@dataclass
class AircraftOperator(AirportCDMPartner):
    """The airline responsible for a flight, which submits flight plan data and provides TOBT and turn-round information.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].

    Relationship: association 'submits' -> FlightPlan [*]
    """
    pass


@dataclass
class MilestoneEvent:
    """An abstract representation of one of the sixteen Airport CDM milestones, each with a trigger, timing rule, effect and procedure that updates a flight's status and timings.

    Package Milestones, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].
    """
    pass


@dataclass
class AircraftReadyCheck(MilestoneEvent):
    """The milestone in which the aircraft becomes ready for start-up (ARDT), refining the pre-departure sequence and alerting if TOBT has passed without a ready status.

    Package Milestones, stereotype control, milestones [12].

    Relationship: dependency 'uses' -> ReadyStatusMessage
    """
    toleranceOffset: timedelta | None = None

    def informPartnersOfArdt(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of Actual Ready Time (ARDT) in the Airport CDM Platform and that the aircraft is ready for start up/push-back (milestone 12)."""
        raise NotImplementedError

    def checkReadyStatusReceived(self, flight: Flight) -> bool:
        """At TOBT + tolerance the AO/GH are informed that TOBT has passed and there has not been a ready status message yet (milestone 12)."""
        raise NotImplementedError


@dataclass
class Aircrew(AirportCDMPartner):
    """The pilot and flight crew who request start-up and coordinate the turn-round and pre-departure sequence.

    Package Stakeholders, stereotype entity, milestones [9, 10, 12, 13, 14].
    """
    pass


@dataclass
class AirportCDMPlatform:
    """The central Airport CDM system that processes flight information, performs the consistency checks and calculations of each milestone, and triggers CDM Operation actions.

    Package Systems, stereotype control, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: dependency 'processes information for' -> Flight
    """

    def initiateForFlight(self, flight: Flight) -> None:
        """The Airport CDM Platform is initiated for this flight, and all available information is processed (milestone 1)."""
        raise NotImplementedError

    def commenceDpiProcess(self, flight: Flight) -> None:
        """The DPI process commences the correct messaging with Network Operations (if implemented) (milestone 1)."""
        raise NotImplementedError

    def calculateTobtFromEldt(self, eldt: Eldt) -> Tobt:
        """Update of the ELDT can trigger a new TOBT to be entered by the AO/GH, or calculated automatically by the Airport CDM Platform (milestone 4)."""
        raise NotImplementedError


@dataclass
class AirportFlightData:
    """The local airport data describing a flight, checked for consistency against the ATC Flight Plan and Airport Slot.

    Package Flights, stereotype entity, milestones [1].
    """
    pass


@dataclass
class AirportSlot:
    """The airport slot programme entry against which the ATC Flight Plan's consistency is checked.

    Package Flights, stereotype entity, milestones [1].
    """
    pass


@dataclass
class Aldt(TimeQuantity):
    """The Actual Landing Time recorded when the aircraft touches down, with an accuracy of plus or minus one minute.

    Package Timings, stereotype entity, milestones [6].
    """
    accuracy: timedelta | None = None


@dataclass
class Aobt(TimeQuantity):
    """The Actual Off-Block Time recorded when the aircraft pushes back or vacates the parking position.

    Package Timings, stereotype entity, milestones [15].
    """
    accuracy: timedelta | None = None


@dataclass
class Ardt(TimeQuantity):
    """The Actual Ready Time, recorded when the aircraft is ready to taxi upon reception of TWR instructions.

    Package Timings, stereotype entity, milestones [12].
    """
    accuracy: timedelta | None = None


@dataclass
class Asat(TimeQuantity):
    """The Actual Start-up Approval Time, recorded when the aircraft receives its start-up approval.

    Package Timings, stereotype entity, milestones [14].
    """
    accuracy: timedelta | None = None


@dataclass
class Asbt(TimeQuantity):
    """The Actual Start Boarding Time, recorded when the gate opens for passengers to physically board.

    Package Timings, stereotype entity, milestones [11].
    """
    accuracy: timedelta | None = None


@dataclass
class Asrt(TimeQuantity):
    """The Actual Start-up Request Time, recorded when the pilot requests start-up.

    Package Timings, stereotype entity, milestones [13].
    """
    accuracy: timedelta | None = None


@dataclass
class AtcSystem:
    """The air traffic control technical system (including tower FDPS and A-SMGCS) that detects flight events, calculates EXOT and provides actual times such as ALDT, AIBT and ATOT.

    Package Systems, stereotype boundary, milestones [1, 4, 5, 6, 7, 9, 15, 16].

    Relationship: dependency 'calculates' -> Exot

    Relationship: dependency 'provides' -> Aldt

    Relationship: dependency 'provides' -> Aibt

    Relationship: dependency 'provides' -> Aobt

    Relationship: dependency 'provides' -> Atot
    """

    def provideActualLandingTime(self, flight: Flight) -> Aldt:
        """ALDT is provided by ATC system or by ACARS from equipped aircraft (milestone 6)."""
        raise NotImplementedError

    def provideActualInBlockTime(self, flight: Flight) -> Aibt:
        """AIBT is provided by ACARS equipped aircraft or automated docking systems or ATC systems (e.g. A-SMGCS) or by manual input (milestone 7)."""
        raise NotImplementedError

    def calculateExot(self, trafficLoad: str, gateStandLocation: str, runwayInUse: str, holdingPositionWait: timedelta) -> Exot:
        """Following the receipt of the TOBT, the ATC system will calculate and provide the Estimated Taxi-Out Time (EXOT) based on the predicted traffic load, gate/stand location, runway in use, and waiting period at the Holding Position (milestone 9)."""
        raise NotImplementedError

    def provideActualOffBlockTime(self, flight: Flight) -> Aobt:
        """AOBT is provided by ACARS equipped aircraft or automated docking systems or ATC systems (e.g. A-SMGCS) or by manual input (milestone 15)."""
        raise NotImplementedError

    def provideActualTakeOffTime(self, flight: Flight) -> Atot:
        """ATOT is provided by ATC system or from ACARS equipped aircraft (milestone 16)."""
        raise NotImplementedError


@dataclass
class Atot(TimeQuantity):
    """The Actual Take-Off Time recorded at take-off from an outstation or at the home airport, with an accuracy of plus or minus one minute.

    Package Timings, stereotype entity, milestones [3, 16].
    """
    accuracy: timedelta | None = None


@dataclass
class AutomatedDockingSystem:
    """An automated docking system at the stand that can provide AIBT and AOBT.

    Package Systems, stereotype boundary, milestones [7, 15].

    Relationship: dependency 'provides' -> Aibt

    Relationship: dependency 'provides' -> Aobt
    """
    pass


@dataclass
class BoardingStartCheck(MilestoneEvent):
    """The milestone in which boarding starts (ASBT) and boarding status is checked against TOBT.

    Package Milestones, stereotype control, milestones [11].
    """
    triggerOffset: timedelta | None = None

    def informPartnersOfAsbt(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of Actual Start Boarding Time (ASBT) when it occurs (milestone 11)."""
        raise NotImplementedError

    def checkBoardingStatus(self, flight: Flight) -> bool:
        """At a certain time before TOBT (local variable e.g. corresponding to aircraft type) a check shall be performed to check the boarding status and inform the AO/GH in case TOBT needs to be updated (milestone 11)."""
        raise NotImplementedError


@dataclass
class Ctot(TimeQuantity):
    """The Calculated Take-Off Time issued by Network Operations to a regulated flight at EOBT-2hr.

    Package Timings, stereotype entity, milestones [2, 13].
    """
    pass


@dataclass
class DatalinkClearanceMessage:
    """The DCL message by which flight crew may request start-up.

    Package Messages, stereotype boundary, milestones [14].
    """
    pass


@dataclass
class DepartureSequence:
    """The pre-departure and departure sequence into which a flight is placed after TOBT confirmation and TSAT issue, and from which it is removed at take-off.

    Package Flights, stereotype entity, milestones [9, 10, 12, 13, 16].

    Relationship: association 'sequences' -> Flight [0..*]
    """

    def addFlight(self, flight: Flight) -> None:
        """The flight is introduced into the pre-departure sequence following receipt of TOBT (milestone 9)."""
        raise NotImplementedError

    def resequenceFlight(self, flight: Flight) -> None:
        """In case the start up approval is not granted at TSAT + tolerance, the flight will be re-sequenced (milestone 14)."""
        raise NotImplementedError

    def removeFlight(self, flight: Flight) -> None:
        """An airborne message is generated and the flight is removed from the departure sequence (milestone 16)."""
        raise NotImplementedError


@dataclass
class DpiMessage:
    """A Departure Planning Information message exchanged with Network Operations, of a type (E-DPI, T-DPI, T-DPI-t, T-DPI-s, A-DPI) determined by the triggering milestone.

    Package Messages, stereotype boundary, milestones [1, 2, 3, 10, 15].
    """
    dpiType: DpiType | None = None


@dataclass
class Eibt(TimeQuantity):
    """The Estimated In-Block Time of an arriving flight, computed from ELDT or ALDT plus the estimated taxi-in time (EXIT).

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 6, 7].
    """

    def calculateFromEldt(self, eldt: Eldt, exit: Exit) -> datetime:
        """An estimated in-block time (EIBT) is computed using the ELDT and the estimated taxi-in time (milestone 4)."""
        raise NotImplementedError

    def updateFromAldt(self, aldt: Aldt, exit: Exit) -> datetime:
        """The EIBT can be updated according to the ALDT+EXIT (milestone 6)."""
        raise NotImplementedError


@dataclass
class Eldt(TimeQuantity):
    """The Estimated Landing Time of an arriving flight, updated progressively from flight plan activation through final approach.

    Package Timings, stereotype entity, milestones [1, 2, 3, 4, 5, 6].

    Relationship: dependency 'updates from' -> FlightUpdateMessage
    """

    def updateFromFum(self, fum: FlightUpdateMessage) -> None:
        """For inbound flights, ELDT is updated based on information provided by the FUM messages, taking into account the actual progress of the flight (milestone 2)."""
        raise NotImplementedError

    def calculateFromAtot(self, atot: Atot, estimatedElapsedTime: timedelta) -> datetime:
        """If the departure airport is more than 3hrs flying time from the destination airport, using the ATOT an ELDT can be calculated using the Estimated Elapsed Time on the FPL (milestone 3)."""
        raise NotImplementedError


@dataclass
class Eobt(TimeQuantity):
    """The Estimated Off-Block Time of a flight, used as the reference point for milestone triggers such as EOBT-3hr and EOBT-2hr.

    Package Timings, stereotype entity, milestones [1, 2, 3, 9, 10].
    """
    pass


@dataclass
class EobtMinus2HourCheck(MilestoneEvent):
    """The milestone at EOBT-2hr in which regulated flights receive a CTOT and estimates are checked against the ATC Flight Plan before informing Network Operations by T-DPI.

    Package Milestones, stereotype control, milestones [2].
    """
    triggerOffset: timedelta | None = None

    def checkFlightEstimatesConsistency(self, flight: Flight) -> bool:
        """Checks whether AO/GH flight estimates are consistent with the ATC Flight Plan, before or after take off from outstation, to verify feasibility of the ATC Flight Plan estimated off block time at EOBT-2 hrs (milestone 2)."""
        raise NotImplementedError

    def informNetworkOperationsWithTDpi(self, flight: Flight) -> None:
        """At EOBT-2 hrs Network Operations is informed through the first T-DPI message about the updated take off time estimate (milestone 2)."""
        raise NotImplementedError

    def markAsRegulated(self, flight: Flight) -> None:
        """ETOT/TTOT/CTOT are updated and appropriate fields are marked as REGULATED (milestone 2)."""
        raise NotImplementedError


@dataclass
class EtfmsSystem:
    """The Network Operations system (ETFMS) that monitors a flight's progress within three hours of the destination and sends Flight Update Messages.

    Package Systems, stereotype boundary, milestones [3].

    Relationship: dependency 'sends' -> FlightUpdateMessage
    """

    def monitorFlightProgress(self, flight: Flight) -> None:
        """If the flight is within 3hrs flying time of the destination airport, Network Operations monitors progress of the flight using the ETFMS (milestone 3)."""
        raise NotImplementedError

    def sendFlightUpdateMessage(self, flight: Flight) -> FlightUpdateMessage:
        """Network Operations sends a Flight Update Message (FUM) that provides updates of the flight's progress (milestone 3)."""
        raise NotImplementedError


@dataclass
class Etot(TimeQuantity):
    """The Estimated Take-Off Time of a flight, updated at flight plan activation and at EOBT-2hr.

    Package Timings, stereotype entity, milestones [1, 2].
    """
    pass


@dataclass
class Ettt(TimeQuantity):
    """The estimated turn-round time on which TOBT is calculated after ground handling starts.

    Package Timings, stereotype entity, milestones [8].
    """
    value: timedelta | None = None


@dataclass
class Exit(TimeQuantity):
    """The estimated taxi-in time used together with ELDT or ALDT to compute EIBT.

    Package Timings, stereotype entity, milestones [4, 6].
    """
    value: timedelta | None = None


@dataclass
class Exot(TimeQuantity):
    """The Estimated Taxi-Out Time calculated by the ATC system from traffic load, gate/stand location, runway in use and holding position, used in TTOT calculation.

    Package Timings, stereotype entity, milestones [2, 3, 9, 15].
    """
    value: timedelta | None = None


@dataclass
class TobtConsistencyCheck(MilestoneEvent):
    """An abstract milestone procedure common to the events following radar detection, landing and ground handling, that checks TOBT consistency with the ATC Flight Plan and notifies Network Operations of TTOT changes beyond tolerance.

    Package Milestones, stereotype control, milestones [4, 5, 6, 7, 8, 9].
    """

    def checkTobtConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH TOBT is consistent with the ATC Flight Plan, to verify feasibility of the ATC Flight Plan given the updated TOBT (milestones 4,5,6,7,8,9)."""
        raise NotImplementedError

    def checkTtotToleranceAndNotify(self, flight: Flight) -> None:
        """Network Operations is informed when the TTOT changes by more than the agreed TTOT tolerance; the TTOT tolerance is respected before Network Operations is informed of updated TTOT (milestones 4,5,6,7,8,9)."""
        raise NotImplementedError


@dataclass
class FinalApproachCheck(TobtConsistencyCheck):
    """The milestone in which the flight enters final approach, triggering the TOBT process and update of ELDT, EIBT, TOBT and TTOT.

    Package Milestones, stereotype control, milestones [5].

    Relationship: dependency 'triggered by detection from' -> RadarSystem
    """
    pass


@dataclass
class Flight:
    """A single scheduled arrival or departure operation of an aircraft, tracked through the sixteen milestones with an operational status.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16].

    Relationship: composition 'records successive values of' -> TimeQuantity [0..*]

    Relationship: association 'operated by' -> Aircraft [1]

    Relationship: association 'described by' -> FlightPlan [1]
    """
    operationalStatus: OperationalStatus | None = None
    direction: str | None = None
    regulated: bool | None = None
    readinessDeadlineOffset: timedelta | None = None
    eobt: Eobt | None = None
    tobt: Tobt | None = None
    aobt: Aobt | None = None
    etot: Etot | None = None
    ttot: Ttot | None = None
    ctot: Ctot | None = None
    eldt: Eldt | None = None
    aldt: Aldt | None = None
    eibt: Eibt | None = None
    aibt: Aibt | None = None
    atot: Atot | None = None
    exot: Exot | None = None
    exit: Exit | None = None
    mttt: Mttt | None = None
    ettt: Ettt | None = None
    acgt: Acgt | None = None
    tsat: Tsat | None = None
    asbt: Asbt | None = None
    ardt: Ardt | None = None
    asrt: Asrt | None = None
    asat: Asat | None = None


@dataclass
class FlightPlan:
    """The ICAO ATC Flight Plan submitted for a flight, possibly as part of a repetitive flight plan, used to check consistency with slot and airport data.

    Package Flights, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9].
    """
    repetitive: bool | None = None
    scheduledOffBlockTime: Sobt | None = None
    firstDestination: str | None = None


@dataclass
class FlightPlanActivation(MilestoneEvent):
    """The milestone in which the ATC Flight Plan is submitted and checked for consistency with the Airport Slot and Airport Flight Data before initiating the Airport CDM Platform for the flight.

    Package Milestones, stereotype control, milestones [1].

    Relationship: dependency 'checks consistency of' -> FlightPlan

    Relationship: dependency 'checks consistency against' -> AirportSlot

    Relationship: dependency 'checks consistency against' -> AirportFlightData
    """
    earliestTriggerOffset: timedelta | None = None

    def checkConsistency(self, flightPlan: FlightPlan, airportSlot: AirportSlot, airportFlightData: AirportFlightData) -> bool:
        """Checks consistency between the ATC Flight Plan, Airport Slot and Airport flight data before the first E-DPI is sent (milestone 1)."""
        raise NotImplementedError

    def confirmFlightToNetworkOperations(self, flight: Flight) -> None:
        """Confirms the flight to Network Operations and allows further local processing of the flight (milestone 1)."""
        raise NotImplementedError

    def sendFirstEDpi(self, flight: Flight) -> bool:
        """The E-DPI message should not be sent if no or inconsistent information is provided; the AO must provide correct information before this message, feeding Network Operations with consistent SOBT, aircraft registration and first destination data as early as possible (milestone 1)."""
        raise NotImplementedError

    def initiateOutboundFlight(self, flight: Flight) -> None:
        """For non coordinated airports, the flight plan is used to initiate the outbound flight (milestone 1)."""
        raise NotImplementedError

    def checkFlightReadiness(self, flight: Flight) -> bool:
        """The flight is ready not later than 15 minutes after the planned EOBT (milestone 1)."""
        raise NotImplementedError

    def updateArrivalTimings(self, eldt: Eldt, eibt: Eibt) -> None:
        """ELDT and EIBT updated for an arrival (milestone 1)."""
        raise NotImplementedError

    def updateDepartureTimings(self, eobt: Eobt, etot: Etot) -> None:
        """EOBT and ETOT updated for a departure (milestone 1)."""
        raise NotImplementedError


@dataclass
class FlightUpdateMessage:
    """The FUM message sent by Network Operations providing updates of a flight's progress used to update ELDT.

    Package Messages, stereotype boundary, milestones [1, 2, 3].
    """
    pass


@dataclass
class FsaMessage:
    """The Flight Status Advisory message sent upon take-off.

    Package Messages, stereotype boundary, milestones [16].
    """
    pass


@dataclass
class GroundHandler(AirportCDMPartner):
    """The party performing ground handling operations on behalf of the Aircraft Operator, providing TOBT, ready and boarding information.

    Package Stakeholders, stereotype entity, milestones [3, 4, 5, 6, 7, 8, 9, 10, 11, 12].
    """
    pass


@dataclass
class GroundHandlingStartedCheck(TobtConsistencyCheck):
    """The milestone in which ground handling commences (ACGT) for first-of-day or long-parked flights, triggering updates to TOBT and TTOT.

    Package Milestones, stereotype control, milestones [8].
    """
    pass


@dataclass
class IfpsSystem:
    """The Integrated Initial Flight Plan Processing System that distributes the submitted ATC Flight Plan to all involved ATC units.

    Package Systems, stereotype boundary, milestones [1].

    Relationship: dependency 'distributes' -> FlightPlan
    """

    def distributeFlightPlan(self, flightPlan: FlightPlan) -> None:
        """The ATC Flight Plan is submitted by the Aircraft Operator and distributed by the IFPS; all involved ATC units receive the flight plan, including departure and destination aerodromes (milestone 1)."""
        raise NotImplementedError


@dataclass
class InBlockCheck(TobtConsistencyCheck):
    """The milestone in which AIBT is recorded, triggering updates to TOBT and TTOT based on the estimated turn-round period.

    Package Milestones, stereotype control, milestones [7].
    """
    pass


@dataclass
class LandedCheck(TobtConsistencyCheck):
    """The milestone in which ALDT is recorded, triggering updates to EIBT, TOBT and TTOT based on the turn-round period.

    Package Milestones, stereotype control, milestones [6].
    """
    pass


@dataclass
class LocalRadarUpdate(TobtConsistencyCheck):
    """The milestone in which the flight is detected entering the FIR or local airspace, triggering the TOBT process and update of ELDT, EIBT, TOBT and TTOT.

    Package Milestones, stereotype control, milestones [4].

    Relationship: dependency 'triggered by detection from' -> RadarSystem
    """
    pass


@dataclass
class Mttt(TimeQuantity):
    """The minimum turn-round time used with EIBT to calculate TTOT.

    Package Timings, stereotype entity, milestones [2, 3].
    """
    value: timedelta | None = None


@dataclass
class MvtMessage:
    """The movement message sent upon take-off.

    Package Messages, stereotype boundary, milestones [16].
    """
    pass


@dataclass
class NetworkOperations(AirportCDMPartner):
    """The Network Management function that issues CTOT, monitors flight progress via ETFMS, and receives DPI and FUM messages.

    Package Stakeholders, stereotype entity, milestones [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15].

    Relationship: association 'receives' -> DpiMessage [*]

    Relationship: dependency 'issues' -> Ctot
    """

    def issueCtot(self, flight: Flight) -> Ctot:
        """If the flight is regulated, a CTOT is issued by Network Operations at EOBT-2h and is sent to relevant ATS units as well as the departure aerodrome (milestone 2)."""
        raise NotImplementedError


@dataclass
class OffBlockCheck(MilestoneEvent):
    """The milestone in which AOBT is recorded, triggering an A-DPI message and TTOT update checked against tolerance.

    Package Milestones, stereotype control, milestones [15].
    """

    def informPartnersOfAobt(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of Actual Off-Block Time (AOBT) in the Airport CDM Platform and that the aircraft has commenced push-back/taxi from parking position, when it occurs (milestone 15)."""
        raise NotImplementedError

    def sendADpi(self, flight: Flight) -> DpiMessage:
        """AOBT always triggers an A-DPI message to Network Operations or, in the case of remote holding, at a defined time prior to TTOT (milestone 15)."""
        raise NotImplementedError

    def checkTtotToleranceAndNotify(self, flight: Flight) -> None:
        """After a first A-DPI is sent, checks TTOT updates against the TTOT tolerance before Network Operations is informed, with a new A-DPI, of the updated TTOT (milestone 15)."""
        raise NotImplementedError


@dataclass
class RadarSystem:
    """The radar system that detects a flight by its assigned SSR code when crossing FIR, TMA or final approach boundaries.

    Package Systems, stereotype boundary, milestones [4, 5].
    """

    def detectFlightBySsr(self, ssrCode: str) -> None:
        """The radar system is able to detect a flight based upon the assigned SSR code when the flight crosses a defined FIR/ATC boundary (milestone 4)."""
        raise NotImplementedError

    def detectFinalApproach(self, flight: Flight) -> None:
        """The radar system detects a flight based upon the assigned SSR code and identifies when the flight crosses either a defined range/position or passes/leaves a predetermined level (milestone 5)."""
        raise NotImplementedError


@dataclass
class ReadyStatusMessage:
    """The RDY message confirming the aircraft is ready for start-up when ARDT has not itself been recorded.

    Package Messages, stereotype boundary, milestones [12].
    """
    pass


@dataclass
class Sobt(TimeQuantity):
    """The Scheduled Off-Block Time fed to Network Operations before the first E-DPI message.

    Package Timings, stereotype entity, milestones [1].
    """
    pass


@dataclass
class StandGateManagement(AirportCDMPartner):
    """The stakeholder responsible for allocating and managing stands and gates for arriving and departing aircraft.

    Package Stakeholders, stereotype entity, milestones [4, 9].
    """

    def checkStandGateChangeAllowed(self, eldt: Eldt, exit: Exit) -> bool:
        """Taking into account the taxi-in time (EXIT), any change to a stand or gate is not preferred after ELDT-30' (milestone 4)."""
        raise NotImplementedError


@dataclass
class StartUpApprovalCheck(MilestoneEvent):
    """The milestone in which ATC grants start-up approval (ASAT), checked against TSAT and re-sequencing the flight if approval is not granted in time.

    Package Milestones, stereotype control, milestones [14].

    Relationship: dependency 'resequences flight in' -> DepartureSequence

    Relationship: dependency 'triggered by' -> DatalinkClearanceMessage
    """
    toleranceOffset: timedelta | None = None

    def informPartnersOfAsat(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of Actual start up approval Time (ASAT) in the Airport CDM Platform and that the aircraft has received start up approval/push-back clearance, when it occurs (milestone 14)."""
        raise NotImplementedError

    def checkAsatAgainstTsat(self, flight: Flight) -> bool:
        """Checks if ASAT is in accordance to TSAT and alerts all relevant Airport CDM Partners when no start up has been granted; in case the start up approval is not granted at TSAT + tolerance, all relevant partners should be informed (milestone 14)."""
        raise NotImplementedError


@dataclass
class StartUpRequestCheck(MilestoneEvent):
    """The milestone in which start-up is requested (ASRT), with an alert if the request is not made within the TSAT tolerance window.

    Package Milestones, stereotype control, milestones [13].
    """
    toleranceWindow: timedelta | None = None

    def informPartnersOfAsrt(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners of Actual Start up Request Time (ASRT) in the Airport CDM Platform when it occurs (milestone 13)."""
        raise NotImplementedError

    def checkStartUpRequestedInTime(self, flight: Flight) -> bool:
        """If the start up request is not made by TSAT + tolerance, the AO/GH is informed that no start up has been requested, and should update TOBT (milestone 13)."""
        raise NotImplementedError


@dataclass
class TakeOffFromOutstationCheck(MilestoneEvent):
    """The milestone at take-off from an outstation in which estimated landing time consistency is checked and Network Operations informed via T-DPI-t if needed.

    Package Milestones, stereotype control, milestones [3].
    """

    def checkLandingEstimateConsistency(self, flight: Flight) -> bool:
        """Checks whether the AO/GH estimated landing time after take off from outstation are consistent with the outbound ATC Flight Plan, to verify feasibility of the ATC Flight Plan at take off from outstation (milestone 3)."""
        raise NotImplementedError

    def informNetworkOperationsWithTDpiT(self, flight: Flight) -> None:
        """When needed, informs Network Operations about the updated take off time estimates using a T-DPI-t Message; a TTOT tolerance of 5 minutes is respected before Network Operations is informed of the updated TTOT (milestone 3)."""
        raise NotImplementedError


@dataclass
class TakeOffNotification(MilestoneEvent):
    """The milestone in which ATOT is recorded, generating FSA and MVT messages and removing the flight from the departure sequence.

    Package Milestones, stereotype control, milestones [16].

    Relationship: dependency 'sends' -> FsaMessage

    Relationship: dependency 'sends' -> MvtMessage

    Relationship: dependency 'generates' -> AirborneMessage

    Relationship: dependency 'removes flight from' -> DepartureSequence
    """

    def informPartnersOfTakeOff(self, flight: Flight) -> None:
        """Informs all relevant Airport CDM Partners about the actual take off (milestone 16)."""
        raise NotImplementedError

    def generateAirborneMessage(self, flight: Flight) -> AirborneMessage:
        """An airborne message is generated (milestone 16)."""
        raise NotImplementedError

    def sendFsaAndMvt(self, flight: Flight) -> None:
        """FSA and MVT messages are sent (milestone 16)."""
        raise NotImplementedError


@dataclass
class Tobt(TimeQuantity):
    """The Target Off-Block Time provided or updated by the Aircraft Operator/Ground Handler, checked for consistency against the ATC Flight Plan at every downstream milestone.

    Package Timings, stereotype entity, milestones [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13].
    """
    accuracy: timedelta | None = None
    updateCount: int | None = None


@dataclass
class TobtFinalConfirmation(TobtConsistencyCheck):
    """The milestone at which the Aircraft Operator/Ground Handler provides the most accurate TOBT before TSAT issue, checked for consistency with the ATC Flight Plan.

    Package Milestones, stereotype control, milestones [9].

    Relationship: dependency 'introduces flight into' -> DepartureSequence
    """
    confirmationOffset: timedelta | None = None

    def confirmTobtPriorToTsat(self, flight: Flight) -> bool:
        """The confirmed TOBT prior to TSAT has special status, where AO/GH check the quality of TOBT before TSAT issue; no need to confirm an existing TOBT if it has been manually modified before (milestone 9)."""
        raise NotImplementedError


@dataclass
class Tsat(TimeQuantity):
    """The Target Start-Up Approval Time issued by ATC, stabilising the flight in the pre-departure sequence.

    Package Timings, stereotype entity, milestones [9, 10, 11, 12, 13, 14].
    """
    accuracy: timedelta | None = None


@dataclass
class TsatIssuance(MilestoneEvent):
    """The milestone in which ATC issues TSAT to stabilise the flight in the pre-departure sequence and checks the number of subsequent TOBT updates.

    Package Milestones, stereotype control, milestones [10].

    Relationship: dependency 'stabilises flight into' -> DepartureSequence
    """
    issuanceOffset: timedelta | None = None
    updateCountThreshold: int | None = None

    def issueTsat(self, flight: Flight) -> Tsat:
        """ATC issues TSAT t-minutes before EOBT, where t is a parameter agreed locally (milestone 10)."""
        raise NotImplementedError

    def informPartnersOfTsat(self, flight: Flight) -> None:
        """Informs all relevant partners of the TSAT that has been allocated to the flight; the TSAT will indicate to the partners the time when the start up approval can be expected (milestone 10)."""
        raise NotImplementedError

    def sendTDpiS(self, flight: Flight) -> DpiMessage:
        """Network Operations is informed by a T-DPI-s for non regulated flights; no check is performed for this step (milestone 10)."""
        raise NotImplementedError

    def checkTobtUpdateCount(self, flight: Flight) -> bool:
        """Checks whether the number of TOBT updates exceeds a tolerance defined locally, after TSAT has been issued; in case the number exceeds a threshold, the TOBT input should be processed according to local procedure (milestone 10)."""
        raise NotImplementedError


@dataclass
class Ttot(TimeQuantity):
    """The Target/Calculated Take-Off Time, computed from EIBT+MTTT+EXOT or TOBT+EXOT and reported to Network Operations when it changes beyond tolerance.

    Package Timings, stereotype entity, milestones [2, 3, 4, 5, 6, 7, 8, 9, 10, 15].
    """
    toleranceThreshold: timedelta | None = None

    def calculateAtEobtMinus2Hr(self, eibt: Eibt, mttt: Mttt, exot: Exot, eobt: Eobt, tobt: Tobt) -> datetime:
        """Calculation basis for the TTOT shall take into account EIBT+MTTT+EXOT, if later than EOBT+EXOT. In the case of manual input of TOBT, this estimate will override the EIBT+MTTT estimate, hence TTOT equals TOBT+EXOT (milestone 2)."""
        raise NotImplementedError

    def calculateAtTakeOffFromOutstation(self, eibt: Eibt, mttt: Mttt, exot: Exot, eobt: Eobt, tobt: Tobt) -> datetime:
        """Calculation basis for the TTOT shall take into account EIBT+MTTT+EXOT. In case EOBT is later than EIBT+MTTT, TTOT equals EOBT+EXOT. In the case where TOBT is available this prediction will overrule the EIBT+MTTT estimate, hence TTOT equals TOBT+EXOT (milestone 3)."""
        raise NotImplementedError

    def updateConsideringExot(self, exot: Exot) -> datetime:
        """TTOT updated considering the EXOT (milestone 15)."""
        raise NotImplementedError


@dataclass
class TurnRound:
    """The aircraft turn-round linking an arriving flight and its related departing flight at an airport.

    Package Flights, stereotype entity, milestones [1, 6, 7, 8].

    Relationship: aggregation 'arriving flight' -> Flight [1]

    Relationship: aggregation 'departing flight' -> Flight [1]
    """
    turnRoundType: str | None = None

    def calculateDepartingFlightTimings(self, turnRoundPeriod: timedelta) -> None:
        """TOBT and TTOT are updated automatically or inserted manually by the Aircraft Operator/Ground Handler, calculated on the basis of the defined or estimated turn-round period for the departing flight (milestones 6, 7, 8)."""
        raise NotImplementedError
