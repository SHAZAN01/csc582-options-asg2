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
- In expiry.md, follow the actual calls from Exchange to the state guard,
  payoff calculation, writer selection and atomic clearing operation.
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
