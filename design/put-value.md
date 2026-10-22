# A put's value before expiry

The caller requests the current value of one issued put contract, while its
state is Open and the valuation date is strictly before expiry. Payoff is a
PutPayoff instance, using the inherited SignedVanillaPayoff calculation.

```mermaid
sequenceDiagram
    actor Caller
    participant OptionContract
    participant OpenState
    participant Payoff
    participant MarketContext

    Caller->>OptionContract: unitValue(market)
    OptionContract->>OpenState: unitValue(contract, market)
    OpenState->>OptionContract: openValue(market)
    OptionContract->>Payoff: modelValue(terms, market)
    Payoff->>MarketContext: spot(underlying)
    MarketContext-->>Payoff: spot per share
    Payoff->>MarketContext: yearsTo(expiry)
    MarketContext-->>Payoff: T greater than zero
    Note over Payoff,MarketContext: Read fixed annual volatility and rate, use immutable strike and multiplier
    Note over Payoff: One signed BSM expression, private direction -1, no CALL or PUT comparison
    Payoff-->>OptionContract: current model value for one contract
    OptionContract-->>OpenState: current model value for one contract
    OpenState-->>OptionContract: current model value for one contract
    OptionContract-->>Caller: current model value for one contract
```

The multiplier is applied inside Payoff.modelValue exactly once. A Position
then multiplies this unit value by its signed units. The returned number is
neither intrinsic value alone nor profit after the historical premium.
No fabricated numerical BSM result is reported for unspecified inputs.
