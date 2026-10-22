# Automatic call exercise at expiry

One issued call contract from the section 8 example is expanded here:
spot 112, strike 105, multiplier 100, and expiry is today. The configured
exercise threshold is 1.00 per contract, a documented assumption. Intrinsic
value is 700, so the exchange exercises it automatically. In this concrete
trace the selected writer is the current writer; no re-pairing is needed.

```mermaid
sequenceDiagram
    participant Exchange
    participant OptionContract
    participant ClearingLedger
    participant Holder as holderAccount : Account
    participant Writer as writerAccount : Account

    Note over Exchange,OptionContract: Today is expiry, one open call, S=112, K=105, M=100
    Exchange->>Exchange: resolveAtExpiry(contract, market)
    Exchange->>OptionContract: assertOpenAtExpiry(market)
    Note over OptionContract: Delegate to current ContractState, OpenState checks expiry date, terminal states reject
    OptionContract-->>Exchange: authorized
    Exchange->>OptionContract: intrinsicValue(market)
    Note over OptionContract: Delegate to immutable Payoff, return 100 times max(112 minus 105, 0)
    OptionContract-->>Exchange: 700
    Exchange->>Exchange: shouldExercise(700)
    Exchange-->>Exchange: true
    Exchange->>ClearingLedger: selectWriter(contract)
    Note over ClearingLedger: AssignmentPolicy selects an eligible writer of the same definition
    ClearingLedger-->>Exchange: selectedWriter

    Exchange->>OptionContract: exerciseAtExpiry(selectedWriter, ledger, market)
    OptionContract->>OptionContract: assertOpenAtExpiry(market)
    OptionContract-->>OptionContract: authorized by current state
    OptionContract->>OptionContract: settlementPlan(selectedWriter, market)
    Note over OptionContract: Payoff supplies balanced stock and cash deltas without a call or put test
    OptionContract-->>OptionContract: balanced plan
    OptionContract->>ClearingLedger: exerciseAtomically(contract, selectedWriter, plan, market)
    ClearingLedger->>OptionContract: assertOpenAtExpiry(market)
    OptionContract-->>ClearingLedger: current state authorizes

    critical One indivisible balanced settlement
        Note over ClearingLedger,Writer: Validate the plan and owning authority before effects, internal steps have no observable partial balance
        ClearingLedger->>Holder: changePosition(contract, -1, ledger)
        Holder-->>ClearingLedger: long option unit removed
        ClearingLedger->>Writer: changePosition(contract, 1, ledger)
        Writer-->>ClearingLedger: short option unit removed
        ClearingLedger->>Writer: changePosition(underlying, -100, ledger)
        Writer-->>ClearingLedger: 100 shares delivered
        ClearingLedger->>Holder: changePosition(underlying, 100, ledger)
        Holder-->>ClearingLedger: 100 shares received
        ClearingLedger->>Holder: changeCash(-10500, ledger)
        Holder-->>ClearingLedger: strike payment debited
        ClearingLedger->>Writer: changeCash(10500, ledger)
        Writer-->>ClearingLedger: strike payment credited
        ClearingLedger->>ClearingLedger: recordAssignment(contract, selectedWriter, market)
        ClearingLedger-->>ClearingLedger: one Assignment with contractCount 1
        ClearingLedger->>OptionContract: finishExercise(ledger)
        OptionContract-->>ClearingLedger: current state becomes ExercisedState
    end
    ClearingLedger-->>OptionContract: committed Assignment
    OptionContract-->>Exchange: Assignment
```

The initial premium was transferred on acquisition and is not charged again.
The 700 is the exercise advantage, not the payment: the holder pays 10,500
for 100 shares. Option units close as +1 becomes 0 and -1 becomes 0. Share
deltas sum to zero and cash deltas sum to zero.

The critical fragment expresses the model's logical atomicity. It does not
specify locks, a database or a concurrency implementation. An invalid plan or
terminal-state rejection produces no changes. No other operation can observe
or commit a subset of these effects. recordAssignment is an internal step,
not a second independent assignment request.

For section 8's ten-contract example, resolve ten issued units. Aggregate
delivery is 1,000 shares and exercise cash is 105,000. Each unit's exercise
has one matching assignment of one contract. Bulk exercise allocation is a
recorded granularity limitation.
