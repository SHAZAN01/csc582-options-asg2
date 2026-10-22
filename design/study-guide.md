# Explain this model in your own words

These are take-home preparation notes. AI assistance is off during the monitored
in-class session. The actual Part B task is unknown; these notes do not claim to
predict it or provide answers to a live exam.

## Start with these six points

1. **A position is a holding, not the thing held.** Stock and OptionContract
   both implement Asset. Position asks for unitValue and multiplies by units.
2. **A listing is not an issued obligation.** OptionDefinition has reusable
   terms; each OptionContract has an actual holder, writer, and lifecycle.
3. **The right changes one arithmetic direction.** CallPayoff fixes +1;
   PutPayoff fixes -1. Shared payoff methods calculate value and delivery.
   No other class reads a CALL/PUT flag.
4. **The exchange chooses policy.** It compares intrinsic contract value with
   its threshold. The option supplies the economic value and guards its life.
5. **Only the ledger changes financial ownership.** The long, short, stock,
   cash, assignment and terminal state change as one coherent operation.
6. **Terminal state prevents the effect.** An exercise request reaches the
   current state; an ended contract has no authorized route to settlement.

## Understand the numbers

For one call with strike 105 and spot 112, the multiplier is 100. Intrinsic
value is 700. The holder receives 100 shares and pays 10,500 cash. If the
original premium was 2.50 per share, it was 250 per contract and was already
paid at acquisition. The holder's resulting advantage after that premium is
450. For ten units, multiply these amounts by ten; there are ten individual
exercise/assignment events in this design.

For a put with strike 95 and spot 80, the holder delivers 100 shares and
receives 9,500 cash. The intrinsic advantage is 1,500. A historical premium
of 200 reduces profit to 1,300. The delivery cash is not merely 1,500.

## Trace the files

- In model.md, follow Position -> Asset, then the Stock and OptionContract
  realizations. Explain why Stock has no exercise operation.
- In expiry.md, follow Exchange through guarded contract resolution, then identify
  each Account update and the single assignment inside the clearing commit.
- In put-value.md, explain why the state is consulted before modelValue and
  where the multiplier is applied.
- In rationale.md, read question 3 carefully: the one-unit design and writer
  re-pairing are real choices with costs, not details to improvise in class.
- In audit.md, locate the seven required coverage items and each operation's
  defence against kind tests.

## Practise answering without reading a prepared paragraph

- Why is the private coefficient arithmetic data rather than a disguised
  CALL/PUT switch? Point to the shared expressions and absence of comparisons.
- What can an expired contract's public protocol actually do?
- Why is the threshold in Exchange rather than Payoff?
- What happens if the selected writer differs from the original writer?
- Why does the model use many individual contracts instead of one quantity-10
  contract object? What does this make simpler, and what does it make awkward?
- Which facts came from the domain, and which were chosen assumptions?
- Which class would change for a fixed-cash payoff? Which existing classes
  would continue working through the same interfaces?

If an answer feels unclear, revise the model and rationale together. Do not
memorize a defence for a diagram you cannot trace.


## Eight preparation explanations tied to this model

These are assistant-authored study explanations, not an assessment of the
student's understanding. Practise explaining the same choices without reading.

1. **Common ownership.** Asset means “can supply a unit value and trading
   permission.” Position stores units and an Asset reference. A share's unit
   is one share and an issued option's unit is one contract. Position uses
   the same multiplication for both. The cost is that generic Asset clients
   cannot exercise everything; exercise belongs to the option protocol.
2. **One place for direction.** OptionDefinition references an immutable
   Payoff. The vanilla family uses a private coefficient: +1 for a call,
   -1 for a put. That coefficient participates in common arithmetic; no
   operation compares it to classify a right. It is never exposed for
   another class to inspect. Pricing and delivery use the same behavior.
3. **Two consistent sides.** An issued OptionContract references one holder
   and one current writer. The ledger creates +1 and -1 option positions
   together. Exercise removes both, applies balanced delivery and cash,
   records one assignment and ends the contract in one domain operation.
   A failure cannot publish only one side. Reassignment requires a feasible
   exchange of equal-unit writer bindings with another open contract.
4. **Life belongs to the contract.** Stock has no expiry state. An option's
   current state supplies permissions. OpenState accepts resolution only
   on expiry; terminal states reject authorization. OptionContract must
   obtain that authorization before requesting settlement, and the ledger
   checks again against current state. A repeated request has no financial
   effect. State labels are never used as conditionals.
5. **Automatic exercise is exchange policy.** Exchange compares intrinsic
   money with a configured threshold. Payoff supplies intrinsic value;
   the state enforces lifetime; the ledger applies the authorized effect.
   Keeping the threshold out of Payoff lets exchange policy vary without
   changing the financial meaning of the right.
6. **Pricing belongs to behavior.** Before expiry, unitValue delegates through
   OpenState and OptionContract.openValue to Payoff.modelValue. The vanilla
   family evaluates the signed BSM expression in the rationale. Numeric
   limits handle zero time/volatility. The multiplier is applied once there,
   and Position applies signed units afterward. Historical premium is not
   subtracted from a current model value.
7. **Underlying knowledge is narrow.** OptionDefinition holds one Stock
   identity. Payoff uses it to obtain the spot and identify delivered shares.
   It does not need a stock order book, shareholder list, or price prediction
   algorithm. MarketContext supplies consistent inputs during one operation.
8. **A new fixed-cash right.** A new class implements Payoff's three operations.
   Its settlement plan contains balanced cash changes and no share changes.
   Register a configured immutable prototype under a new boundary label.
   Current positions, states, contract coordination and clearing use the
   same interfaces. A new listing-specific payout field would need a richer
   external schema; that broader change is not promised by this design.

## Distinguish source rules from chosen assumptions

Source rules include multiplier 100, expiry-date-only exercise, paired parties,
physical strike settlement, automatic exchange exercise, and zero-sum holdings.
Chosen assumptions include a 1.00-per-contract threshold with equality included,
ACT/365 time, lowest eligible account ID for assignment, and on-time resolution.
The individual-unit representation is a design choice with an explicit cost.

## Quick numerical explanation

For the call example, 112 minus 105 is 7 per share. Multiplying by 100 gives
700 intrinsic value. Actual strike cash is 105 times 100, or 10,500. The
holder receives shares worth 11,200. The 700 advantage is therefore not an
additional cash payment. A premium of 250 paid earlier leaves 450 net payoff
at expiry, ignoring costs. The writer has the opposite option payoff.

For the put, use the other direction: at spot 80 and strike 95, the holder
hands over 100 shares and receives 9,500 cash. The exercise advantage is 1,500,
not the strike cash itself. Neither example requires an exchange CALL/PUT test.
