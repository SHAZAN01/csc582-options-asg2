# Coverage and operation audit

This audit is about the submitted design, not an implementation or a market
simulation. It must be rerun after substantive diagram or rationale edits.

## Seven required coverage items

| Handout section 4 item | Where the model expresses it |
|---|---|
| 1. Owned and valued assets, including contracts | Asset is implemented by Stock and OptionContract; one Position class holds either through that interface. |
| 2. Calls, puts, and complete terms | OptionDefinition has underlying Stock, strike, expiry and multiplier; Payoff supplies one shared signed-vanilla behaviour with call/put constructor coefficients. |
| 3. Holder and writer | Each issued OptionContract has exactly one of each; the ledger publishes their paired positions and acquisition premium together. |
| 4. Lifecycle and permissions | ContractState defaults reject mutation; OpenState permits appropriate date-checked operations; ExercisedState and ExpiredState are terminal. |
| 5. Exercise, assignment, automatic expiry | Exchange chooses threshold policy; AssignmentPolicy chooses an eligible writer; ClearingLedger commits assignment, paired closure, physical delivery and lifecycle together. |
| 6. Intrinsic and pre-expiry value | Payoff.intrinsicValue and modelValue return per-contract money; the put sequence reaches the latter through current-state delegation. |
| 7. External construction boundary | ConstructionBoundary reads ListingDescription and its external right label, resolves Stock, selects one Payoff prototype, builds terms and issues paired units. |

## Operation families and the no-kind-tests rule

| Operations | Required information | Why no asset/right kind test is needed |
|---|---|---|
| Stock.unitValue / assertTradable | MarketContext and Stock identity | Read this stock's spot or allow trading; no expiry behaviour exists here. |
| Position.value | Asset.unitValue and signed units | One multiplication through an interface. |
| Position.changeUnits | Integer delta and ledger authority | Arithmetic plus authority validation, independent of asset class. |
| Account.value | Cash and positions | Sum cash and each Position.value. |
| Account.changePosition / changeCash | Asset identity, signed deltas, authority | Map lookup, arithmetic and zero-position removal; asset identity is not asset kind. |
| MarketContext.spot / yearsTo | Stock key and dates | Read a quote or calculate a year fraction. |
| OptionContract.unitValue / assertTradable / assertOpenAtExpiry | Current private ContractState | Polymorphic delegation; no state-label or asset-kind comparison. |
| OptionContract.openValue | Immutable terms and Payoff | Delegate per-contract valuation. |
| OptionContract.intrinsicValue / settlementPlan | Immutable terms and Payoff | Delegate economic behaviour without reading a right tag. |
| OptionContract.exerciseAtExpiry / expireAtExpiry | Current state, ledger and context | Dispatch through current state; terminal states reject. |
| replaceWriter / finishExercise / finishExpiry | Owning ledger authority and validated commit | Apply an already-authorized invariant-preserving change; never classify a right. |
| ContractState default operations | Contract and context | Return zero or reject. No classification is required. |
| OpenState permissions / exercise / expire | Dates, delegated plan and ledger | Compare dates, then delegate the permitted effect. |
| CallPayoff / PutPayoff constructors | One fixed coefficient | Establish the mathematical right once, during construction. |
| SignedVanillaPayoff.intrinsicValue | Private coefficient and numeric terms | Shared signed arithmetic and max; no comparison against a kind value. |
| SignedVanillaPayoff.modelValue | Private coefficient, numeric market inputs | One signed BSM expression with numeric boundary cases. |
| SignedVanillaPayoff.settlementPlan | Private coefficient, parties and terms | Balanced signed stock/cash deltas. No settlement switch elsewhere. |
| ClearingLedger.registerPair | Known issued unit, parties, acquisition price | Publish equal and opposite holdings and premium cash movement together. |
| ClearingLedger.selectWriter / eligibleWriters | Active-unit index and definition identity | Delegate selection among open matching obligations; no CALL/PUT test. |
| AssignmentPolicy.selectWriter | Eligible accounts and account IDs | Deterministic ordering over domain data. |
| ClearingLedger.exerciseAtomically / expireAtomically | Current-state authorization, balances and plan | Validate and commit the complete effect, including terminal state. |
| SettlementPlan.validateBalance | Typed asset/cash delta maps | Sum cash and sum units separately for each Asset identity. |
| Exchange.resolveAtExpiry / exercise | Dates, holder identity, intrinsic and threshold | Policy compares dates, identities and money; never option kinds. |
| Exchange.shouldExercise | Intrinsic money and positive configured threshold | One numeric comparison. |
| ConstructionBoundary.buildDefinition | External right label and symbols | The named, permitted exception: interpret descriptions and select behaviour once. |
| ConstructionBoundary.registerPayoff / issue | Registry entries or known definitions | Register an immutable capability, or issue paired units without decoding the kind again. |

No operation outside the boundary is specified to compare CALL/PUT, use an
instanceof-style asset test, or switch on a concrete asset class. The private
direction coefficient is never exposed as a classification API. This claim
depends on preserving the operation contracts in the rationale; a diagram
cannot prove a future implementation will obey them.

## Lifecycle checks to explain in class

| Trigger | Required result |
|---|---|
| Exercise requested before expiry | OpenState rejects before plan application. |
| Exercise requested after resolution | Current terminal state rejects; no new assignment or transfer. |
| Trading requested after expiry | Date or terminal-state permission rejects. |
| Above-threshold call on expiry | Select eligible writer; transfer M shares and M*K cash in opposite directions; close both option holdings; create one assignment. |
| Below-threshold or out-of-money option | Expire atomically, close both option holdings, move no shares/cash. |
| At-the-money option | Intrinsic zero is below the positive configured threshold, so it expires. |
| Put value requested before expiry | OpenState reaches Payoff.modelValue and returns one contract's current theoretical value. |
| Stock valued or traded | Use Asset operations; no contract state is consulted. |

## Sequence/source consistency

The sequence files contain exactly one Mermaid sequenceDiagram each and no
more than five participants. Calls must resolve to operations declared in
model.md (including inherited operations). Dashed return arrows carry values,
not additional method calls. Notes summarize effects inside the named atomic
operation; they do not introduce an unmodelled external participant.

The supplied validation checks parse the three diagram sources and resolve
each sequence call to a model operation. No executable market code or market
test framework is included. Visual readability and student understanding
remain separate checks from parsing.
