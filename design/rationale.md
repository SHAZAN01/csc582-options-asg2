# Design rationale

This rationale describes the accompanying class and sequence diagrams. It is
an AI-assisted design draft that the student must review and be able to defend.
The requirements source is `OPTIONS-MARKETS.md`; decisions below are explicitly
distinguished from statements in that source.

## 1. What shares and options share, and its cost

`Asset` is an interface implemented by `Stock` and `OptionContract`. Both expose
`unitValue(market)` and `assertTradable(market)`. `Position` stores an Asset
reference and signed units; its value is units times the asset's unit value.
It never asks which concrete asset it holds. `Account.value` adds its cash
balance and position values. A short option position therefore has negative
current value; this is distinct from its eventual profit after premium.

The unit is deliberately asset-specific: one Stock unit is one share; one
OptionContract unit is one issued contract covering 100 shares. Callers need
not know that distinction to multiply by position units. The cost is that
generic Asset clients cannot exercise arbitrary assets. Exercise belongs to
the exchange's OptionContract protocol, not to Stock.

`OptionContract` is the concrete contract abstraction for this take-home. There
is no second required contract family, so an additional stateful Contract
superclass would add a level without sharing actual required behaviour.

## 2. Where the call/put difference lives

An immutable Payoff object belongs to each immutable OptionDefinition.
CallPayoff and PutPayoff inherit the three calculations from SignedVanillaPayoff.
Their constructors differ only in an immutable private arithmetic coefficient:
call uses +1; put uses -1. There is no public right tag or coefficient getter.

Let d denote that private coefficient, S spot, K strike, and M the multiplier.
The common intrinsic calculation is M times max(d times (S minus K), 0).
The common settlement plan changes the holder's stock by d times M and cash
by minus d times M times K; the writer receives the opposite changes.
These are arithmetic expressions, not tests of a kind. The shared model-value
calculation also uses one signed BSM expression, described under question 6.

The contract, state objects, exchange, positions, and ledger see only Payoff
operations and the resulting money or balanced plan. They do not read d.
Consequently valuation and settlement cannot consult inconsistent CALL/PUT
flags. A definition's Payoff and terms cannot change after construction.

This design uses interface realization for capabilities and ordinary
inheritance for shared signed-vanilla behaviour. It does not use multiple
inheritance or mixins: an option is not a Stock, its underlying is an
association, and its current lifecycle is composed state. Treating those
relationships as extra parent classes would give objects irrelevant members
and couple independent variation. The cost is more delegation operations.

## 3. Holder, writer, and consistency

An OptionDefinition is a reusable listed description; an OptionContract is
one issued unit with one holder and one current writer. This distinguishes
section 8's unowned listings from section 5's paired outstanding obligations.
The boundary interns definitions by underlying identity, strike, expiry,
multiplier and immutable Payoff identity, so equivalent listings share the
same definition rather than accidentally creating separate writer pools.
Issuing count n creates n contract objects. For each, ClearingLedger.registerPair
publishes the holder's +1 position and the writer's -1 position together and
transfers the agreed premium. Issuance requires a positive integer count,
nonnegative premium, multiplier 100, valid strike and parties, and a market
date no later than expiry. The external premium is per share; the boundary
converts it once to premium per contract using M=100.

Only the owning ClearingLedger may change positions, account cash, counterparties,
or lifecycle. Account.changePosition and changeCash, Position.changeUnits, and
the contract's transition hooks require that ledger authority. They are internal
operations, not public independent setters. Zero holdings are removed from the
account; audit records may remain in the ledger.

The exchange's AssignmentPolicy chooses a writer of the same definition. The
chosen policy selects the lowest account ID from the ledger's eligible set;
this deterministic choice is an assumption, not a rule stated in the domain.
It need not pick the contract's original writer. If another open contract
contains the selected short unit, the ledger exchanges equal-unit writer links
and their associated short positions before resolving the exercised unit.
Eligibility requires a feasible two-party re-pairing; the original writer is
always a valid fallback. This keeps every issued unit paired even before it ends.

Writer re-pairing, removal of the exercised long and short, stock/cash changes,
one completed Assignment, and the terminal state are one logical atomic commit.
Both the option position sum and each transfer's balance remain zero at every
observable model boundary. No concurrency or database implementation is claimed.

Each exercise here is exactly one issued unit and creates exactly one Assignment
whose contractCount is 1. Ten units are ten exercises and ten assignments. This
is a deliberate granularity choice, not a claim to represent one bulk exercise
of ten units with one assignment. The assignment quantity always matches the
quantity of the exercise represented by that event.

## 4. Contract life and prevention of invalid exercise

Only OptionContract composes ContractState. The abstract state supplies safe
defaults: value zero and rejection of trading, exercise authorization, exercise,
and expiry mutation. ExercisedState and ExpiredState inherit those terminal
defaults. OpenState alone supplies the permitted operations. No caller compares
displayLabel or asks which state class it has.

| Current state | Current value | Trading | Exercise |
|---|---|---|---|
| Open, before expiry | Model value | Permitted | Rejected |
| Open, on expiry | Intrinsic contract value | Permitted until resolution | Permitted |
| Exercised | Zero | Rejected | Rejected |
| Expired | Zero | Rejected | Rejected |

OpenState authorizes exercise only when market.asOf equals the definition's
expiry. The ledger repeats authorization against the contract's *current*
private state immediately before committing. Terminal state rejection therefore
prevents the settlement effect, rather than merely displaying a warning.
Public clients cannot replace the state, hold its mutable reference, directly
set balances, or manufacture completed assignments through the public protocol.
Internal hooks also require the owning ledger. Repeated requests cannot create
a second assignment or repeat delivery.

OpenState rejects trading after the expiry date. The design assumes the exchange
invokes resolution for every outstanding unit on its expiry date. Handling a
missed event and reconstructing historical expiry prices is a recorded limitation.

## 5. Who decides automatic exercise

Exchange owns the decision in resolveAtExpiry. It first requires an open contract
on its expiry date, asks for intrinsicValue through Payoff, and compares that money
amount with its configured threshold. The design assumes threshold 1.00 per
contract (equivalent to 0.01 per share for this domain), positive thresholds only,
and exercise when intrinsic is at least the threshold. The source supplies no
number or equality convention, so neither is presented as a sourced requirement.

On exercise, the exchange obtains the selected writer and invokes the guarded
exercise protocol. Otherwise it invokes the guarded expiry protocol, which removes
the paired option holdings, records ExpiredState, and transfers no stock or cash.
The holder may also request exercise through Exchange.exercise on the expiry date;
the caller must be the current holder. The threshold controls automatic
resolution only; the model does not invent a profitability restriction on a
holder's otherwise valid expiry-date request. The writer cannot invoke a refusal path.

Putting the *decision* in a payoff or state object would couple a financial right
or lifecycle mechanism to the exchange's configurable threshold. The option
supplies intrinsic value and enforces its lifetime; the exchange chooses policy.

## 6. Where valuation lives, and how it avoids kind tests

OpenState delegates current valuation to OptionContract.openValue, which delegates
to Payoff.modelValue. The vanilla implementation reads strike and multiplier from
the definition and spot, date, annual volatility, and rate from MarketContext.
T uses actual calendar days divided by 365; this convention is a design assumption.
Spot and rate inputs are supplied, not estimated by this model.

For T>0, positive S and K, and positive sigma, one signed expression demonstrates
that a CALL/PUT branch is unnecessary. With N the standard normal cumulative
distribution, a=(ln(S/K)+(r+sigma^2/2)T)/(sigma sqrt(T)) and b=a-sigma sqrt(T):

    value of one contract = M * d * (S*N(d*a) - K*exp(-r*T)*N(d*b))

Substitution of d=+1 gives the call expression; d=-1 gives the put expression.
This is a proposed common arithmetic organization, not an extra requirement
from the domain. The standard expressions were checked against the
[MIT OpenCourseWare option-pricing slides](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/d19208c017ada04f9261cfb41ab8d702_MIT18_S096F13_lecnote19.pdf).
The assignment requires a design, so no numerical implementation is supplied.

At T=0, use intrinsicValue instead. For zero volatility or zero spot, use the
deterministic limit M*max(d*(S-K*exp(-r*T)),0), avoiding log(0) or division by
zero. Negative spot, nonpositive strike, negative volatility, and an unresolved
past-expiry quote are invalid inputs. These are numeric/date checks, never
tests of option or asset kinds. Terminal states return zero without invoking BSM.

Values are per issued contract and already include M once. A Position applies its
signed units once afterward. The put-value sequence returns a current model value,
not intrinsic value alone, acquisition premium, or realised profit.

The distributed section names BSM but displays only put-call parity. This source
gap is recorded in the annotations. Parity is a consistency relationship, not
a replacement for an independent valuation formula. Market quotes used at
acquisition are distinguished from this theoretical model value.

## 7. What the option knows about the underlying

OptionDefinition holds one Stock reference. Payoff needs its identity to request
the corresponding market spot and to identify the asset delivered in settlement.
It does not need the stock's shareholder list, order book, price-estimation
algorithm, account balances, or another option's concrete class.

Stock gets its spot from MarketContext. It has no contract state, expiry, strike,
writer, or exercise operation. Definition interning also keeps assignment pools consistent. Definition sharing
avoids copying mutable market prices into every option. All calculations within one operation use the same
immutable context so their dates and inputs agree.

## 8. Adding a fixed-cash option

A future FixedCashPayoff would implement Payoff directly, rather than inherit
SignedVanillaPayoff. It would own its payout amount and condition, provide its
own intrinsic and model values per contract, and return a cash-only SettlementPlan
with an empty asset-delta map. It would still return balanced holder/writer cash
changes. It must supply its own suitable valuation expression. All current Money values
are in one assumed currency; currency conversion is not modelled.

Register that immutable Payoff under a new external label in ConstructionBoundary.
The boundary looks up that label once when building a definition. This is a registry
data addition, not a new switch in any existing domain class. Existing Asset,
Position, Account, OptionContract, states, exchange, ledger, and plan interfaces
need no source change. The payout amount is configured when registering that immutable prototype;
ListingDescription.rightText selects the configured registration. Thus the
existing listing class need not gain a payout field for this fixed-amount kind.
Accepting arbitrary payout amounts in each external listing would require a
richer boundary input schema; that more general extension is not claimed here.
The current take-home does not claim to have implemented or drawn this extension.

## Rejected alternatives

1. **A right enum plus switches in pricing and settlement.** It is compact, but
   duplicates the distinction and violates the handout outside the boundary.
   Independent flags could make valuation disagree with delivery direction.
2. **CallOption and PutOption overriding every calculation.** It repeats common
   lifecycle and term handling and gives three places to change one distinction.
   Private signed arithmetic within one Payoff family shares those operations.
3. **A universal Asset base with exercise and expiry methods.** It gives Stock
   operations that do not make sense. The common interface instead contains only
   valuation and trading permission.
4. **Separate public updates to the holder and writer.** They expose unbalanced
   intermediate positions. A single clearing commit owns both sides and delivery.
5. **Multiple inheritance from Stock and Contract, or from state classes.** The
   option has an underlying Stock and a current state; it is not those things.
   Composition expresses the relationships and permits state replacement.

## Misfits, scope limits, and assumptions

- **Granularity:** the model represents individual issued units. Large holdings
  require many positions and assignments, rather than the document's convenient
  aggregate quantities. A production aggregate-allocation design would need an
  explicit split/merge model; none is claimed here.
- **Assignment allocation:** deterministic eligible writer selection and feasible
  equal-unit re-pairing are chosen because the document leaves selection open.
  Random pooled assignment, account netting, and self-matches are not modelled.
- **Clock and missed expiry:** an on-time exchange event is assumed. Delayed event
  recovery and reconstructing an earlier closing spot are not specified.
- **Threshold:** value and equality convention are chosen, not supplied. A small
  positive theoretical intrinsic value can still expire below the threshold;
  the threshold approximates exercise cost, which is not separately accounted.
- **Funding and delivery:** participants are assumed able to perform. Default,
  borrowing, margin, and failed-delivery procedures are not modelled.
- **Quotes and ownership transfer:** the model includes valuation, acquisition
  pairing and permissions, but not a secondary-market matching engine or complete
  generic sale protocol. Section 7's order types remain extension context.
- **Valuation inputs:** one supplied context and fixed volatility/rate suffice;
  estimation, dividends, real data, concurrency and persistence are outside scope.

These costs are part of the proposed design. They are not hidden claims that the
unfamiliar domain is fully captured, and the student may revise them after review.
