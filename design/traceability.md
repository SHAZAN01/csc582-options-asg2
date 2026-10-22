# Requirements traceability

The domain source is OPTIONS-MARKETS.md. A source rule and a chosen design
mechanism are different: this map identifies both without extending the
required take-home into the section 7 trading subsystem.

## Required coverage

| Source and required behavior | Structural responsibility | Observable trace or rationale |
|---|---|---|
| Sections 2-3: positions own and value shares and contracts uniformly | Asset, Stock, OptionContract, Position, Account | Position.value multiplies signed units by Asset.unitValue; rationale 1 |
| Section 4: underlying, strike, expiry, multiplier and right | OptionDefinition, Stock, Payoff | Immutable terms and one behavior reference; rationale 2 and 7 |
| Section 4.1: holder's right and writer's obligation | OptionContract's two Account associations and ClearingLedger | +1/-1 publication and removal; expiry sequence and rationale 3 |
| Sections 3 and 5: open, exercised, expired and their permissions | Composed ContractState, OpenState, terminal states | Current-state authorization prevents repeated delivery; rationale 4 |
| Section 5: automatic exercise, assignment and physical strike settlement | Exchange, AssignmentPolicy, ClearingLedger, Assignment, SettlementPlan | Expiry sequence explicitly shows option closure, shares, cash, assignment and state |
| Sections 4.3 and 6: intrinsic and pre-expiry value | Payoff and SignedVanillaPayoff, MarketContext | Expiry trace requests intrinsic; put trace requests modelValue; rationale 6 |
| Handout section 4, item 7: an external construction boundary | ListingDescription and ConstructionBoundary | One external-label interpretation, cached stock/definitions and issued paired units; rationale 3 and 8 |

## Eight rationale questions

| Question | Decision and cost to explain |
|---|---|
| 1. Common asset abstraction | An interface permits common valuation/holding, but exercise is available only through the option protocol. |
| 2. One right distinction | Private immutable payoff direction drives shared arithmetic; no second CALL/PUT flag exists. |
| 3. Two consistent sides | Individual issued units make pairing explicit, at the cost of many objects and restricted writer re-pairing. |
| 4. Contract life | State delegates permissions, contract coordinates, ledger rechecks before an indivisible effect. Stock has no expiry. |
| 5. Automatic exercise | Exchange owns the threshold policy; Payoff supplies value and the contract supplies lifetime checks. |
| 6. Formula placement | Payoff computes per-contract value from consistent inputs, applying multiplier once and using no right-kind branch. |
| 7. Underlying knowledge | A stock identity supplies spot lookup and delivered asset identity, without order-book or account knowledge. |
| 8. New fixed-cash right | A new configured Payoff can return a balanced cash-only plan; arbitrary new listing fields are a separate scope cost. |

## Concrete sequence evidence

In expiry.md, spot 112, strike 105 and multiplier 100 imply intrinsic 700.
The holder's +1 option unit and writer's -1 unit both close. The holder gains
100 shares and pays 10,500; the writer has opposite changes. A single assignment
for one issued contract and the Exercised state are part of that same domain
operation. The original acquisition premium is not charged a second time.

In put-value.md, the request follows OptionContract, OpenState, openValue,
Payoff.modelValue and MarketContext. Pricing is neither intrinsic alone nor
profit after premium. The multiplier enters Payoff once and signed position
quantity enters Position once. Unspecified inputs are not given invented values.

The construction exception permits recognizing external descriptions once.
Identity comparisons, date conditions, numeric limits and balanced-delta checks
are not classifications of asset or option kinds. The operation audit examines
that distinction for every operation family in the model.

## Declared limitations

rationale.md records individual-unit granularity, restricted assignment swaps,
on-time resolution, a chosen threshold and day count, assumed funding/delivery,
and omitted secondary-market matching. The design is a specification of these
responsibilities, not a market implementation or proof that executable code
would enforce the invariants.
