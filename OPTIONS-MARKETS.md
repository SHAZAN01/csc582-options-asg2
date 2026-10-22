# Options Markets: The Domain You Will Model

## Why you are being asked to do this

**You write no code that simulates this market.** You will not build it. You will *model* it. The
only code you write is Mermaid script, which generates your UML diagrams.

This is the skill that comes before implementation. You take a system described in ordinary
language — like this document, written by someone who knows the business but not software — and
you turn it into a structure of objects.

Real requirements look like this. They arrive as prose. They contain things that vary, things that
cannot happen, and things that are true but never stated. Nobody gives you a list of classes.
Making that list, and defending it, is the work.

### What you will produce

**Take-home:** a UML class diagram of the part of this market described in §2 to §6 — what kinds
of thing exist, what each one knows, and how they relate — and two sequence diagrams that show
your objects at work. For each design decision, choose between:

- **inheritance**, when one kind of thing really *is* a kind of another;
- **interfaces or mixins**, when several unrelated kinds of thing share one capability;
- **multiple inheritance**, when one thing really is two things at once.

Each choice has a cost. A model that uses the same technique everywhere has not made a choice.

**In class:** you extend your own model with something else this document describes, with AI
assistants off.

Because there is no implementation, you cannot hide an unresolved decision. In code, a vague design
can be patched with a conditional and still run. In a diagram, it is visible.

---

## 0. How to read this

<!-- AI-ANNOTATION START -->
> **Annotation key and provenance.** The added blockquotes are AI-assisted notes
> prepared on October 22, 2026. Original source paragraphs remain unchanged.
> Student review is required; these notes do not claim an unaided reading pass.
>
> - **[VARIES]** identifies alternatives or changing data.
> - **[FIXED]** identifies a rule stated by the source.
> - **[IMPOSSIBLE]** identifies a forbidden situation.
> - **[DESIGN]** proposes a modelling consequence; it is not additional source text.
> - **[GAP]** identifies an ambiguity that needs a recorded decision.
> - **[CHECK]** identifies a worked example or consistency check to explain.
> - **[SCOPE]** distinguishes required take-home coverage from other material.
<!-- AI-ANNOTATION END -->

This document describes a **domain**. It is not a specification of a program: it has no class
names, no diagrams, and no advice about structure. Turning it into an object model is your job.

Read it like notes from an expert who knows the business well and knows nothing about software:

- **Mark what varies.** Words like "or", "either", and "it depends" show that something varies.
- **Mark what is fixed.** Rules that are always true are rules your design can rely on — and
  sometimes must enforce.
- **Mark what cannot happen.** Impossible things are as useful to know as possible ones.

Every term is explained when it first appears, and collected in the glossary at the end. No finance
background is needed. Where a formula matters, it is given.

---

## 1. What this market is

<!-- AI-ANNOTATION START -->
> **[FIXED]** A share and an agreement about that share are distinct assets.
> The agreement has its own price, parties, and end date.
>
> **[VARIES]** What is owned, how its value changes, and whether it has an expiry.
>
> **[SCOPE]** The take-home model covers the assets and contract behaviour in
> sections 2-6. Section 7 describes trading mechanisms that are not required
> as a complete take-home order-book model.
<!-- AI-ANNOTATION END -->

Most markets trade *things*. This market also trades **agreements about things**.

You can buy a share of a company. You can also buy an agreement that gives you the right to buy a
share of that company later, at a price fixed today. The agreement is not the share. It has its own
price and its own buyers and sellers, and it ends on a fixed date.

Three different things happen in this market:

1. **What exists** — the things that can be owned: shares, and agreements about shares (§2 to §6).
2. **How things are traded** — how a buyer and a seller find each other and agree on a price (§7).
3. **What happens over time** — agreements reach their end date, and are used or expire (§5).

---

## 2. Assets: things you can own

<!-- AI-ANNOTATION START -->
> **[FIXED]** An asset can be owned and has a value. A position identifies an
> asset and a quantity held by an owner.
>
> **[VARIES]** Spot changes over time. Different positions can hold different
> assets and quantities.
>
> **[DESIGN]** Keep the shared asset separate from an owner's position. Quantity
> belongs to the holding, not to the stock description shared by many owners.
> Give positions a common way to request value without inspecting asset kinds.
>
> **[GAP]** State the unit of every valuation operation. A stock's spot is per
> share; a position's value covers its entire quantity.
<!-- AI-ANNOTATION END -->

An **asset** is anything that can be owned and has a value.

The basic asset in this market is a **share** of a company, also called a **stock**. Owning one
share means owning a small part of the company. Shares can be handed from one owner to another.
Each share has a price in the market, and the price changes all the time. The current price is
called the **spot** price.

An owner's holding of an asset is a **position**: which asset, and how many units. A trader might
hold a position of 300 shares of XYZ.

---

## 3. Contracts are assets too

<!-- AI-ANNOTATION START -->
> **[FIXED]** A contract is an asset. A position can hold a contract through
> the same ownership abstraction used for shares.
>
> **[VARIES]** Contract lifecycle state: Open, Exercised, or Expired.
>
> **[FIXED]** Exactly one lifecycle state applies at a time.
>
> **[IMPOSSIBLE]** An expired contract cannot be traded or exercised. A share
> cannot be expired. An ended contract cannot simultaneously remain Open.
>
> **[DESIGN]** Put lifecycle behaviour on the contract abstraction rather than
> on every asset. Stock should not inherit meaningless exercise operations.
>
> **[CROSS-REFERENCE]** Open is necessary for exercise; section 5 also restricts
> exercise to the expiry date. This table alone does not authorize early exercise.
<!-- AI-ANNOTATION END -->

A **contract** is an agreement between two parties, with written terms, that obliges at least one
of them to do something.

**A contract is itself an asset.** When you buy an option (§4), you own it. It appears in your
account next to your shares. It has a market value that changes every minute, and you can sell it
to someone else. So a position can hold a contract in exactly the same way as it holds shares.

There is one important difference: **a contract has a life, and a share does not.** A share exists
for as long as the company does. A contract is created, it runs for a while, and then it ends —
it is **exercised** (used) or it **expires** (its time runs out). At any moment, a contract is in
exactly one of these states:

| State | Meaning |
|---|---|
| **Open** | The contract exists, and can still be traded or exercised |
| **Exercised** | The holder has used the right, and the contract has ended |
| **Expired** | The expiry date passed without exercise, and the contract has ended |

What may be done with a contract depends on its state. An expired contract cannot be exercised or
traded. A share is never "expired".

---

## 4. Options: calls and puts

<!-- AI-ANNOTATION START -->
> **[FIXED]** The underlying is stock. Strike and expiry are contractual terms;
> the multiplier is always 100 shares per contract in this domain.
>
> **[VARIES]** The right is to buy or sell. Underlying stock, strike, and expiry
> can differ across listed options; premium changes with the market.
>
> **[DESIGN]** Store the call/put distinction in one behaviour-bearing place.
> A separate right tag that valuation or settlement inspects would violate the
> handout's no-kind-tests rule outside the construction boundary.
>
> **[FIXED]** Premium is not a fixed contractual term. Keep the original paid
> premium distinct from a later current value when discussing profit.
<!-- AI-ANNOTATION END -->

An **option** is a contract that gives its owner the **right, but not the obligation**, to buy or
sell a fixed number of shares at a fixed price, on a fixed date.

Every option has these terms:

| Term | Meaning |
|---|---|
| **Underlying** | The stock that the option is about |
| **Right** | **Call**: the right to buy. **Put**: the right to sell |
| **Strike price** | The fixed price at which the shares may be bought or sold |
| **Expiry date** | The date on which the right can be used; after it, the option no longer exists |
| **Multiplier** | How many shares one contract covers — in this market, always 100 |

The **premium** is the price of the option itself. It is not one of the terms: the market sets it,
it changes all the time, and the order book of §7 exists to find it.

### 4.1 Two sides

<!-- AI-ANNOTATION START -->
> **[VARIES]** Holder and writer are different roles. The holder has the right;
> the writer has the corresponding obligation. One account may occupy different
> roles in different contracts, so these roles need not be permanent person types.
>
> **[FIXED]** Long and short positions are created together and end together.
> Premium flows from holder to writer when the option is acquired.
>
> **[IMPOSSIBLE]** A writer cannot refuse performance after a valid assignment.
> An outstanding contract cannot have an unpaired holder or writer.
>
> **[DESIGN]** Identify one owner of paired position updates. Independent public
> updates that can expose only half the pair would fail the section 5 invariant.
<!-- AI-ANNOTATION END -->

Every option has a buyer and a seller, and their positions are different.

The **buyer** — the **holder**, who is **long** the option — pays the premium and gets the right.
The holder decides whether to use it. The worst case for the holder is losing the premium.

The **seller** — the **writer**, who is **short** the option — receives the premium and takes on an
**obligation**: if the holder uses the right, the writer must do the other side of the trade. The
writer has no choice. The writer's worst case can be much worse than the premium.

<!-- figure: short-call -->
![Profit or loss of the writer of a call with strike 105 and premium 2.50, per contract of 100 units, against the price of the underlying at expiry from 95 to 120. The line is flat at a profit of 250, the premium received, up to the strike of 105, then falls one for one. It crosses zero at 107.50 and reaches a loss of 1,250 at 120, and it keeps falling as the price rises.](figures/short-call.svg)
<!-- /figure -->

*The writer of the call in §4.2 (strike 105, premium 2.50). The most the writer can make is the
premium; the possible loss has no limit.*

For every option that exists, one party holds it and another party wrote it. The two positions are
created together, and they end together.

### 4.2 Calls and puts, with numbers

<!-- AI-ANNOTATION START -->
> **[VARIES]** A call transfers shares from writer to holder and cash in the
> opposite direction; a put reverses those flows. Common terms should not be
> duplicated to represent that directional difference.
>
> **[CHECK]** Call example: 100 shares, strike 105, spot 120. Exercise cash is
> 10,500; share-value advantage is 1,500; profit after premium 250 is 1,250.
> The exercise payment is not merely the 1,500 advantage.
>
> **[CHECK]** Put example: strike 95, spot 80. Exercise cash is 9,500 from writer
> to holder, with 100 shares moving to the writer. The advantage is 1,500;
> profit after premium 200 is 1,300.
<!-- AI-ANNOTATION END -->

A **call** is the right to *buy* at the strike. The holder of a call wants the price to go up.

> XYZ trades at 100. You buy a call with a strike of 105 that expires in one month. The premium is
> 2.50 per share. One contract covers 100 shares, so it costs 250.
>
> - XYZ rises to 120. You exercise: you buy 100 shares at 105 that are worth 120. That is 15 per
>   share, 1,500 in total. After the 250 you paid, your profit is 1,250.
> - XYZ ends at 103. The right to buy at 105 is worth nothing, because you could buy at 103 in the
>   market. You let it expire. You lost the 250.

<!-- figure: long-call -->
![Profit or loss of a long call with strike 105 and premium 2.50, per contract of 100 units, against the price of the underlying at expiry from 95 to 120. The line is flat at a loss of 250, the premium paid, up to the strike of 105, then rises one for one. It crosses zero at the breakeven of 107.50 and reaches a profit of 1,250 at 120.](figures/long-call.svg)
<!-- /figure -->

*A call, strike 105, premium 2.50. The loss is limited to the premium; the gain has no limit.*

A **put** is the right to *sell* at the strike. The holder of a put wants the price to go down.

> The same stock is at 100. You buy a put with a strike of 95 for a premium of 2.00, so it
> costs 200.
>
> - XYZ falls to 80. You exercise: you sell 100 shares at 95 that are worth 80. That is 15 per
>   share, 1,500. After the premium, your profit is 1,300.
> - XYZ ends at 97. The put is worth nothing. You lost the 200.

<!-- figure: long-put -->
![Profit or loss of a long put with strike 95 and premium 2.00, per contract of 100 units, against the price of the underlying at expiry from 80 to 102. The line falls from a profit of 1,300 at 80, crosses zero at the breakeven of 93, and is flat at a loss of 200, the premium paid, from the strike of 95 upward.](figures/long-put.svg)
<!-- /figure -->

*A put, strike 95, premium 2.00. It is the mirror image of the call. Its gain is limited, because
the price cannot fall below zero.*

A call and a put have the same terms. They differ in one thing only: which way the shares and the
cash move when the right is used.

### 4.3 Where an option stands

<!-- AI-ANNOTATION START -->
> **[VARIES]** Moneyness depends on the current spot and strike. It is a derived
> condition, not an independent permanent kind of option.
>
> **[FIXED]** Intrinsic value is nonnegative and the formulas here are per share.
> Multiply by 100 for one contract, then by the held quantity for a position.
>
> **[DESIGN]** Do not treat intrinsic value as the entire pre-expiry value.
> Do not subtract the historical premium to obtain current intrinsic value;
> that subtraction belongs to profit/loss reasoning.
>
> **[GAP]** The phrase "at, or very near" does not specify a numerical tolerance.
> Section 5's automatic-exercise threshold is also unspecified. Record any
> chosen comparison rule rather than silently inventing a source requirement.
<!-- AI-ANNOTATION END -->

Comparing the spot price with the strike shows where an option stands:

- **In the money** — exercising now would be profitable: a call when the spot is above the strike,
  a put when the spot is below it.
- **At the money** — the spot is at, or very near, the strike.
- **Out of the money** — exercising now would make no sense.

The **intrinsic value** is what the option would be worth if it were exercised now, per share:

```
call intrinsic value = max(spot − strike, 0)
put  intrinsic value = max(strike − spot, 0)
```

It is never negative, because the holder can always choose not to use the right. On the expiry
date, an option is worth exactly its intrinsic value times the multiplier. Before that date it is
usually worth more, because the price still has time to move (§6).

---

## 5. Exercise and expiry

<!-- AI-ANNOTATION START -->
> **[FIXED]** Exercise is permitted only on the expiry date and while the
> contract is Open. Every still-open option is resolved at expiry.
>
> **[IMPOSSIBLE]** Early exercise, repeat exercise, or exercise/trading after
> expiry. A share must not be subjected to option-expiry processing.
>
> **[FIXED]** Exercise causes physical share delivery and strike-price cash
> payment. Each exercise has exactly one assignment for the same quantity;
> the exchange selects the writer, who has no refusal right.
>
> **[FIXED]** Across all accounts, signed positions in an option sum to zero
> at every observable moment, not merely after a batch is repaired.
>
> **[DESIGN]** Model settlement as one consistent change of both option sides,
> shares, cash, and lifecycle. The final sequence diagram must identify the
> operation responsible for this change and for preventing a repeat settlement.
> Concurrency and persistence mechanisms are outside the handout's scope.
>
> **[VARIES]** Exchange resolution can exercise or expire the contract. The
> automatic-exercise threshold is an exchange rule rather than a call/put tag.
>
> **[GAP]** The document does not give a threshold value, equality convention,
> writer-selection algorithm, or handling of insufficient shares/cash. Record
> an assumption or an explicit limitation for each behaviour the model needs.
> Do not add a margin system, which section 10 excludes.
>
> **[GAP]** A listed option description is not necessarily an already issued
> contract with parties. Section 8 lists six descriptions before anyone holds
> them. Distinguishing a listed series from issued obligations is one possible
> resolution; the final model must explain its chosen interpretation.
>
> **[DESIGN]** The expiry sequence must delegate directional settlement behaviour
> without asking whether the option is a call or a put.
>
> **[MODEL REVIEW, October 22 — AI-assisted]** The chosen model represents
> each issued unit separately. For an open unit c, the holder position is +1,
> the current writer position is -1, and other accounts hold zero units of c.
> After resolution all positions in c are zero. This is a design refinement
> of the source's paired-ownership invariant, not a new market rule.
>
> **[CHECK]** Share and cash *transfer deltas* sum to zero in settlement.
> This does not mean all outstanding stock holdings must sum to zero. The
> source's signed-position invariant concerns option obligations.
>
> **[MODEL REVIEW]** A rejected or repeated exercise must produce no delivery,
> no new assignment and no lifecycle change. The ledger checks the current
> private state before committing, so a cached earlier OpenState permission
> cannot authorize a later settlement. See rationale question 3 and audit.md.
<!-- AI-ANNOTATION END -->

In this market, an option can be exercised **only on its expiry date**.

**Exercise.** When a holder exercises, shares and cash change hands at the strike price. Exercising
one call with a strike of 105 means: 100 shares move from the writer to the holder, and 10,500 in
cash moves from the holder to the writer. Exercising a put moves them the other way: the holder
delivers the shares and receives the cash.

**Assignment.** When a holder exercises, a writer of the same option must perform. The exchange
chooses which writer, by **assignment**. The writer does not choose and gets no warning. Every
exercise creates exactly one assignment, for the same number of contracts.

**Expiry.** On the expiry date, every option that is still open is resolved. Options in the money
are **exercised automatically** by the exchange. There is a small threshold: an option in the money
by a tiny amount may not be worth the cost of exercising it. Options out of the money expire, worth
nothing. After expiry the contract no longer exists: it cannot be traded or exercised.

> **A rule that always holds.** Every contract in existence has exactly one holder and one writer.
> Added up across all accounts, the positions in any option always come to zero: +10 for the
> holders means −10 for the writers. This is true at every moment, not only at the end of the day.

---

## 6. What an option is worth before expiry

<!-- AI-ANNOTATION START -->
> **[VARIES]** Spot and time to expiry change. Volatility and interest rate are
> inputs, but their estimation is excluded; section 10 permits fixed values.
>
> **[FIXED]** Put-call parity applies to a call and put with the same underlying,
> strike, and expiry. The displayed premiums are per share; contract values
> require the multiplier. Time T is in years and must use consistent units.
>
> **[DESIGN]** Locate the valuation responsibility explicitly in the class model.
> The put-value sequence must show where inputs come from and how the relevant
> behaviour is selected polymorphically. Adding a CALL/PUT switch to a pricing
> service would not satisfy the handout rule.
>
> **[GAP]** This copy names Black-Scholes-Merton and says the formula is supplied,
> but prints only put-call parity. Parity alone does not determine both premiums
> without one additional value. Treat the named formula as a valuation dependency
> and record the missing explicit expression; do not claim that parity by itself
> is a complete independent pricing formula.
>
> **[DESIGN]** Explain how valuation handles the expiry boundary and terminal
> contracts rather than applying a pre-expiry calculation indiscriminately.
> A market quote and a model-calculated value should have clearly stated roles.
<!-- AI-ANNOTATION END -->

The premium of an option depends on:

- **the spot price**, compared with the strike;
- **the time left** until expiry — more time means more chance for the price to move;
- **volatility** — how much the price moves around. More movement means a higher premium;
- **interest rates**, because the strike is paid in the future.

A formula for these options exists — the **Black–Scholes–Merton** formula — and it is given to
you. You do not need to derive it or to understand its mathematics. Where the formula belongs in
your model is a design question.

One relationship between a call and a put on the same stock, with the same strike and expiry, is
always true:

```
call premium − put premium = spot − strike × e^(−r × T)
```

Here `r` is the interest rate and `T` is the time to expiry, in years. This is called **put–call
parity**. Because it is exactly true, it is a useful way to check a calculation.

---

## 7. How trading happens

<!-- AI-ANNOTATION START -->
> **[SCOPE]** This section is retained and marked for domain understanding.
> A full matching/order-book subsystem is outside the seven required take-home
> coverage items. Do not claim to know the undisclosed in-class extension.
>
> **[FIXED]** There is one book per traded thing; stock and option books must
> not require different ownership representations.
<!-- AI-ANNOTATION END -->

Options and shares are traded on an **order book**: one book for each thing that is traded. The
book holds everyone's open offers to buy and to sell.

### 7.1 Orders

<!-- AI-ANNOTATION START -->
> **[VARIES]** Buy/sell, quantity, and market/limit instructions.
>
> **[FIXED]** A limit order supplies a price bound; a market order supplies no
> limit price. Do not invent a numeric sentinel as a source-specified market price.
<!-- AI-ANNOTATION END -->

An **order** says: buy or sell, which contract, how many, and on what terms.

A **limit order** names the worst price you will accept — "buy 10 at no more than 2.50". If nobody
will trade at that price now, the order **rests** in the book and waits.

A **market order** names no price. It trades immediately, at whatever price the book offers.

Resting orders to buy are **bids**; resting orders to sell are **asks**. The highest bid and the
lowest ask are the **best bid** and the **best ask**, and the difference between them is the
**spread**.

### 7.2 Matching

<!-- AI-ANNOTATION START -->
> **[FIXED]** Matching follows price first, then arrival time. Execution uses
> the resting order's price. A crossed book must not persist after resolution.
>
> **[VARIES]** An order can fill fully, partly, or not at all.
>
> **[DESIGN]** If trading is later modelled, separate matching responsibilities
> from asset valuation, contract lifecycle, and physical settlement.
<!-- AI-ANNOTATION END -->

When an arriving order can trade with a resting order, the exchange **matches** them, and a
**trade** happens. The rule is **price-time priority**:

1. **Price first.** Better prices trade first. For bids, higher is better; for asks, lower is
   better.
2. **Time second.** At the same price, the order that arrived first trades first.

Two results that are easy to get wrong:

- **An arriving order can trade at a better price than it asked for.** If you bid 2.55 and an ask
  rests at 2.50, you trade at **2.50**, the resting order's price. The improvement goes to the
  arriving order, never to the resting one.
- **An order can fill partly.** An order for 50, with 30 available, trades 30 now and has 20 left.
  What happens to the 20 depends on §7.3.

The book should never stay **crossed**, with a bid at or above the best ask. Orders like that should
already have traded.

### 7.3 Time in force

<!-- AI-ANNOTATION START -->
> **[VARIES]** Day, good till cancelled, immediate or cancel, and fill or kill.
>
> **[FIXED]** Fill-or-kill needs a whole-quantity availability check before any
> execution. A policy applied only after a partial fill cannot express that rule.
> This is an extension consideration, not an extra take-home diagram requirement.
<!-- AI-ANNOTATION END -->

Each order says what happens to any part of it that does not fill:

- **Day** — rest until the end of the day, then cancel.
- **Good till cancelled** — rest until cancelled.
- **Immediate or cancel** — trade what is available now, and cancel the rest.
- **Fill or kill** — trade the *whole* quantity now, or trade nothing.

Fill-or-kill is different in kind from the others. Day, good-till-cancelled, and immediate-or-cancel
can be applied after matching: match first, then decide what to do with the rest. Fill-or-kill
cannot. Whether the order may trade at all depends on the whole quantity being available *before*
any of it trades.

### 7.4 A worked example

<!-- AI-ANNOTATION START -->
> **[CHECK]** The fill order is A, then B, then part of C. Quantities are
> 20 + 5 + 5 = 30; the remaining ask at 2.55 is 20. The premium-per-share
> weighted average is approximately 2.5083; with multiplier 100, the total
> premium is 7,525. Keep the share/contract units explicit.
<!-- AI-ANNOTATION END -->

The asks resting in the book for one contract, in the order they arrived:

- order **A**: sell 20 at 2.50, arrived 09:31:02;
- order **B**: sell 5 at 2.50, arrived 09:31:40;
- order **C**: sell 25 at 2.55.

The bids are 20 at 2.45 and 35 at 2.40. An order arrives: **buy 30, limit 2.55, day**.

- The best ask is 2.50, with 25 available across two orders. The arriving order will pay up to
  2.55, so it trades.
- Order A arrived first at that price, so it fills completely: **20 at 2.50**.
- Order B fills next: **5 at 2.50**. The 2.50 level is now empty.
- 5 remain. The next level is 2.55, within the limit: **5 at 2.55**.
- Nothing remains. The order is complete, at an average price of 2.5083.

If the order had been fill-or-kill, the exchange would have had to check that all 30 were
available before trading any of them. If it had been immediate-or-cancel with only 25 available,
25 would have traded and the other 5 would have been cancelled instead of resting.

<!-- figure: order-book -->
Buy 30, limit 2.55, arrives. The book for one contract, before and after:

| price | bids before | asks before | bids after | asks after |
|---:|---:|---:|---:|---:|
| 2.55 | — | 25 | — | 20 |
| 2.50 | — | 25 | — | — |
| 2.45 | 20 | — | 20 | — |
| 2.40 | 35 | — | 35 | — |

A fills 20 at 2.50, then B fills 5 at 2.50, then C fills 5 at 2.55. 30 bought for 7,525, an average of 2.5083 per unit.
<!-- /figure -->

### 7.5 Other order types

<!-- AI-ANNOTATION START -->
> **[SCOPE]** These descriptions are explicitly WIP awareness material.
> Do not silently treat their missing details as complete required behaviour.
<!-- AI-ANNOTATION END -->

⚠ **WIP.** Listed here for awareness only:

- **Stop order** — waits until the price reaches a trigger, then becomes a market order.
- **Stop-limit order** — the same, but becomes a limit order.
- **Iceberg order** — shows only part of its size, and shows more as it fills.

---

## 8. One example, from listing to expiry

<!-- AI-ANNOTATION START -->
> **[CHECK]** Ten contracts cover 1,000 shares. Initial premium is 2,500.
> At expiry, delivery is 1,000 shares and cash is 105,000. At spot 112 the
> exercise advantage is 7,000, and profit after premium is 4,500.
>
> **[FIXED]** Both option positions disappear together after resolution.
> The acquired stock position remains distinct from the ended option holding.
>
> **[GAP]** "Six contracts" at listing means six listed term/right combinations
> before issuance in this example. Explain how the model reconciles this with
> the exactly-one-holder-and-writer rule for existing issued contracts.
<!-- AI-ANNOTATION END -->

**Listing.** The exchange lists options on XYZ, which trades at 100: calls and puts at strikes of
95, 100, and 105, all expiring in 30 days, each covering 100 shares. That is six contracts. Nobody
holds any of them yet.

**Trading.** A market maker offers the 105 call at 2.50. A trader buys 10 of them and pays 2,500.
The trader now holds +10, and the market maker has written −10. The positions add up to zero.

**The price moves.** Over three weeks, XYZ rises to 112. The 105 call is now 7 in the money, so its
intrinsic value is 700 per contract. It trades at about 7.60: the extra 0.60 is the value of the
time left.

**Expiry.** On the expiry date, XYZ is still at 112. The 105 call is in the money, so it is
exercised automatically, and the exchange assigns the market maker. 1,000 shares move from the
market maker to the trader, and 105,000 in cash moves the other way. The trader now holds shares
worth 112,000, for which they paid 105,000 plus the 2,500 premium.

**After.** The 105 call contracts no longer exist. Both positions are gone, and everything still
adds up to zero. The other five contracts are resolved in the same way: those in the money are
exercised, and the rest expire, worth nothing.

---

## 9. Questions worth answering on purpose

<!-- AI-ANNOTATION START -->
> **[DESIGN]** Use these questions as a reading checklist. The deliverable
> rationale must answer all eight questions in handout section 7, not merely
> these five domain questions. Explain rejected alternatives and actual misfits
> of the chosen diagrams rather than repeating generic design-pattern claims.
<!-- AI-ANNOTATION END -->

None of these has a single right answer, and this document does not give one. Each is a decision
you will be asked to explain.

1. A share and an option can both be owned, held in a position, and valued. What do they have in
   common in your model, and where does that live?
2. A call and a put differ in only one way (§4.2). How does your model express that difference
   without repeating everything else?
3. A contract has a life, and a share does not (§3). What does that require of your model?
4. Exercise and assignment always happen together, and positions always add up to zero (§5). What
   do these two facts require of the way positions change?
5. Where this document is silent on something your design needs, what did you decide, and why?

---

## 10. What this document leaves out

<!-- AI-ANNOTATION START -->
> **[SCOPE]** Keep the take-home limited to stock options with expiry-date
> exercise and physical delivery. Margin, fees, volatility estimation, other
> underlyings, and alternative settlement rules are not required subsystems.
>
> **[DESIGN]** Distinguish omitted features from genuine gaps in required
> behaviour. Record assumptions about threshold, units, lifecycle, construction,
> and paired ownership wherever the model depends on them. An extension hook
> can be explained without pretending the extension is already implemented.
<!-- AI-ANNOTATION END -->

**Left out on purpose**, because you do not need it:

- Other kinds of contract: options on other things than stocks, options that pay in other ways,
  combinations of options, futures, and bonds.
- Other rules for when an option may be exercised, and settlement in cash instead of shares.
- How volatility and interest rates are estimated. Assume one fixed number for each.
- Auctions, multiple exchanges, fees, regulation, and taxes.
- Margin: what a writer must deposit to cover the obligation.

**Not finished yet, and not on purpose** — marked ⚠ above:

- Other order types (§7.5).

**When this document is silent, decide and record.** If your design needs something that this
document does not give you, make a sensible choice, write down what you chose and why, and
continue. That record is part of what you hand in.

---

## Glossary

| Term | Meaning |
|---|---|
| **Ask** | A resting order to sell; the best ask is the lowest |
| **Assignment** | Being chosen to perform on a written option when a holder exercises |
| **At the money** | The spot price is at, or very near, the strike |
| **Bid** | A resting order to buy; the best bid is the highest |
| **Call** | An option giving the right to buy |
| **Contract** | An agreement with written terms; a contract is also an asset |
| **Exercise** | Using the right that an option gives |
| **Expiry date** | The date on which the right can be used; after it, the option no longer exists |
| **Holder** | The buyer of an option, who has the right; also called long |
| **In the money** | Exercising now would be profitable |
| **Intrinsic value** | What an option would be worth if exercised now; never negative |
| **Limit order** | An order that names the worst price its owner will accept |
| **Market order** | An order that takes whatever price is available |
| **Multiplier** | The number of shares one contract covers |
| **Order book** | The list of resting orders to buy and sell one thing |
| **Out of the money** | Exercising now would make no sense |
| **Position** | An owner's holding of an asset: which asset, and how many units |
| **Premium** | The market price of an option |
| **Price-time priority** | Better prices trade first; at the same price, earlier orders trade first |
| **Put** | An option giving the right to sell |
| **Share** | A small part of a company; also called a stock |
| **Spot** | The current price of the underlying stock |
| **Spread** | The difference between the best bid and the best ask |
| **Strike** | The fixed price at which the right may be used |
| **Underlying** | The stock that an option is about |
| **Volatility** | How much a price moves around; it raises the premium |
| **Writer** | The seller of an option, who has the obligation; also called short |
