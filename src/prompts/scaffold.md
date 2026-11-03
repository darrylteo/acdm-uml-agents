# Scaffold

Given verbatim to every agent in both conditions and used for the ground truth.

## Purpose

The class diagram is the basis of software for this process: data analysis, modelling, optimisation, simulation. It is judged by whether a software engineer could implement it. Therefore:

- Every quantity, value, status, or identifier the document names is a typed attribute on the class that holds it.
- Every rule, calculation, check, tolerance, trigger, update, or notification the document describes is an operation, with parameters and return type, on the class the document says performs it. The description carries the document's formula or condition.
- Things the document treats as kinds of one thing share a superclass, and their common attributes and operations are declared once, on the superclass.

## Document structure

Sixteen milestones, each described by the same eight fields: Definition, Origin and priority, Timing, Data Quality, Effect, Procedures, Operational Status, Action on CDM Operation. Time quantities are named by a prefix (Scheduled, Estimated, Target, Actual, Calculated) and an event (Off-Block, In-Block, Landing, Take-Off, Start-Up Approval, and others): TOBT, EOBT, and AOBT are the target, estimated, and actual values of one event.

## Stereotypes

Every class carries exactly one of Jacobson's (1992) analysis stereotypes, as used in the Rational Unified Process:

- `entity`: holds information that persists across the process and outlives any single procedure.
- `boundary`: models an interface between the system and something outside it: a stakeholder, an external system, or a message.
- `control`: holds the logic of a procedure: sequencing, checking, and computation over entity classes.

Stakeholders are `entity` classes: the model records who they are and what they originate.

## Packages

Every class and enumeration belongs to exactly one package. Six are given:

- `Stakeholders`: the parties that take part in the process and originate or receive its information.
- `Flights`: the flight, turn-round, aircraft, and the flight plan and slot that describe them, including the flight's operational status.
- `Timings`: the time quantities that describe a flight's progress, each with its origin, accuracy, and tolerance.
- `Milestones`: the sixteen events, each with its trigger, timing rule, effect, and procedure.
- `Systems`: the technical systems that hold, compute, and display the process information, including the CDM platform and its actions.
- `Messages`: the messages exchanged between stakeholders and systems.

Add a package only if a class or enumeration fits none of the six; give it a name and a one-sentence description.

## Placement rules

- An operation sits on the class the document names as performing it: a CDM platform action on the platform class, a procedure stated under a milestone on that milestone.
- Information about a flight (flight plan, slot, status) lives in `Flights`; exchanging it is a message class in `Messages` or an operation on the sender.
- Each time quantity is a class in `Timings`. The flight or milestone that carries it has an attribute typed by that class. Every successive value is kept, with its originator and time of update, so a turn-round can be analysed afterwards; an update appends rather than overwrites.
- A status is an enumeration placed with the class whose state it describes.

## Grounding

Every element must be grounded in the document; record the milestone numbers whose text supports it. Do not introduce elements the document does not support.
