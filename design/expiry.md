# Automatic call exercise at expiry

One issued call contract from the section 8 example is expanded here:
spot 112, strike 105, multiplier 100, and expiry is today. The exchange uses
the documented design assumption of a 1.00-per-contract exercise threshold.
The call's intrinsic value is 700, so it is exercised automatically.

```mermaid
sequenceDiagram
    participant Exchange
    participant OptionContract
    participant OpenState
    participant ClearingLedger
    participant Payoff

    Note over Exchange,OptionContract: Expiry date, one open call, spot 112, strike 105, multiplier 100
    Exchange->>Exchange: resolveAtExpiry(contract, market)
    Exchange->>OptionContract: assertOpenAtExpiry(market)
    OptionContract->>OpenState: assertOpenAtExpiry(contract, market)
    OpenState-->>OptionContract: authorized
    OptionContract-->>Exchange: authorized

    Exchange->>OptionContract: intrinsicValue(market)
    OptionContract->>Payoff: intrinsicValue(terms, market)
    Payoff-->>OptionContract: 700
    OptionContract-->>Exchange: 700
    Exchange->>Exchange: shouldExercise(700)
    Exchange-->>Exchange: true

    Exchange->>ClearingLedger: selectWriter(contract)
    Note over ClearingLedger: AssignmentPolicy selects an eligible writer of the same definition
    ClearingLedger-->>Exchange: selectedWriter
    Exchange->>OptionContract: exerciseAtExpiry(selectedWriter, ledger, market)
    OptionContract->>OpenState: exercise(contract, selectedWriter, ledger, market)
    OpenState->>OpenState: assertOpenAtExpiry(contract, market)
    OpenState->>OptionContract: settlementPlan(selectedWriter, market)
    OptionContract->>Payoff: settlementPlan(terms, holder, selectedWriter, market)
    Payoff-->>OptionContract: balanced plan
    OptionContract-->>OpenState: balanced plan

    OpenState->>ClearingLedger: exerciseAtomically(contract, selectedWriter, plan, market)
    ClearingLedger->>OptionContract: assertOpenAtExpiry(market)
    OptionContract->>OpenState: assertOpenAtExpiry(contract, market)
    OpenState-->>OptionContract: authorized
    OptionContract-->>ClearingLedger: authorized
    Note over ClearingLedger: ONE COMMIT: any writer re-pairing, remove paired option positions, transfer shares and cash, record one assignment, finish lifecycle
    Note over ClearingLedger: Holder +100 shares and -10500 cash, writer -100 shares and +10500 cash
    ClearingLedger->>OptionContract: finishExercise(ledger)
    Note over OptionContract: current state becomes ExercisedState inside the same commit
    OptionContract-->>ClearingLedger: transitioned
    ClearingLedger-->>OpenState: Assignment with contractCount 1
    OpenState-->>OptionContract: Assignment
    OptionContract-->>Exchange: Assignment
```

The initial premium was transferred when the holding was acquired. It is not
charged again during exercise. The 700 is the value advantage, not the cash
payment: the physical exercise pays 10,500 for 100 shares.

For the ten-contract section 8 example, resolve ten issued units. Each
exercise has one assignment of one contract. Aggregate delivery is 1,000
shares and aggregate exercise cash is 105,000. This design deliberately does
not claim that ten one-contract assignments are one ten-contract assignment.
