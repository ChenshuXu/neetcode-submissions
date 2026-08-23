# Stripe OA 2024–2026 — LeetCode and Runnable Custom Map

This catalog covers every named problem family in:

```text
/Users/Newton/Documents/job search/projects/context/Interview/stripe/
stripe-hackerrank-challenge-oa-question-bank-2024-2026.md
```

`Close` means LeetCode directly trains the central mechanic. `Partial + custom` means LeetCode covers
only a subproblem and the local runnable exercise covers the recovered multi-part contract. `Alias`
reuses another row's practice. `Low-evidence pattern` means the bank itself has only a title or partial
signal; the mapping must not be mistaken for a recovered original prompt.

## Main question families

| Bank family | Coverage | LeetCode practice | Runnable custom / note |
|---|---|---|---|
| Linked Merchant / Entity Clustering | Partial + custom | [721 Accounts Merge](https://leetcode.com/problems/accounts-merge/); [2092 Find All People With Secret](https://leetcode.com/problems/find-all-people-with-secret/) | [`linked_merchant_clustering`](../linked_merchant_clustering/) |
| Join Two Datasets | Partial + custom | [175 Combine Two Tables](https://leetcode.com/problems/combine-two-tables/) | [`join_two_datasets`](../join_two_datasets/) |
| Merchant Fraud Score | Partial + custom | [1396 Design Underground System](https://leetcode.com/problems/design-underground-system/) | [`merchant_fraud_score`](../merchant_fraud_score/) |
| WebSocket Load Balancer | Partial + custom | [1606 Find Servers That Handled Most Number of Requests](https://leetcode.com/problems/find-servers-that-handled-most-number-of-requests/); [1882 Process Tasks Using Servers](https://leetcode.com/problems/process-tasks-using-servers/) | [`websocket_load_balancer`](../websocket_load_balancer/) |
| Datacenter Request Routing | Partial + custom | [973 K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) | [`datacenter_request_routing`](../datacenter_request_routing/) |
| Catch Me If You Can / Merchant Fraud Thresholds | Partial + custom | [2043 Simple Bank System](https://leetcode.com/problems/simple-bank-system/) | [`merchant_fraud_thresholds`](../merchant_fraud_thresholds/) |
| Credit Card Validation / Luhn | Custom | No meaningful equivalent | [`credit_card_validation`](../credit_card_validation/) |
| Transaction Log Queue Processor | Close mechanics; original contract incomplete | [362 Design Hit Counter](https://leetcode.com/problems/design-hit-counter/); [1348 Tweet Counts Per Frequency](https://leetcode.com/problems/tweet-counts-per-frequency/) | No invented Stripe contract; use the two timestamp/window problems |
| Generic Multi-Entity State Machine | Close pattern | [1603 Design Parking System](https://leetcode.com/problems/design-parking-system/); [1797 Design Authentication Manager](https://leetcode.com/problems/design-authentication-manager/); [2043 Simple Bank System](https://leetcode.com/problems/simple-bank-system/) | No extra custom needed |

## Reserve, aliases, and partially recovered families

| Bank family | Coverage | Practice decision |
|---|---|---|
| Chat Billing | Low-evidence pattern | [1396 Design Underground System](https://leetcode.com/problems/design-underground-system/) for paired events and aggregate billing inputs |
| Six Degrees of Collusion | Close graph pattern | [721 Accounts Merge](https://leetcode.com/problems/accounts-merge/) and [547 Number of Provinces](https://leetcode.com/problems/number-of-provinces/) |
| Registry with REGISTER / SET_HEALTHY | Alias | Reuse [`datacenter_request_routing`](../datacenter_request_routing/) |
| Card Range Obfuscation | Alias | Reuse [`credit_card_validation`](../credit_card_validation/) redaction part |
| Stripe Payment Card Validation System | Alias | Reuse [`credit_card_validation`](../credit_card_validation/) |
| Store Closing Time Penalty | Close | [2483 Minimum Penalty for a Shop](https://leetcode.com/problems/minimum-penalty-for-a-shop/) |
| Subscription / Email Notification Scheduler | Close scheduling patterns | [1834 Single-Threaded CPU](https://leetcode.com/problems/single-threaded-cpu/) and [621 Task Scheduler](https://leetcode.com/problems/task-scheduler/) |
| Atlas Company Name Check | Low-evidence pattern | [49 Group Anagrams](https://leetcode.com/problems/group-anagrams/) for canonicalization/grouping; exact bank contract unavailable |
| Aggregation Transactions | Close aggregation pattern | [1741 Find Total Time Spent by Each Employee](https://leetcode.com/problems/find-total-time-spent-by-each-employee/) |
| Bracket Expansion | Close | [394 Decode String](https://leetcode.com/problems/decode-string/) |
| Accept-Language Header Parser | Custom | [`accept_language_parser`](../accept_language_parser/) |
| KYC / Business Account Data Verification | Close validation pattern | [36 Valid Sudoku](https://leetcode.com/problems/valid-sudoku/) for multi-index validation; domain contract remains screen-specific |
| Authorization Request / Fraud Reporting | Alias | Reuse [`merchant_fraud_thresholds`](../merchant_fraud_thresholds/) |
| Accounts, Users, and Roles | Close state/auth patterns | [1797 Design Authentication Manager](https://leetcode.com/problems/design-authentication-manager/) and [2043 Simple Bank System](https://leetcode.com/problems/simple-bank-system/) |
| Currency Conversion System | Close | [399 Evaluate Division](https://leetcode.com/problems/evaluate-division/) |
| Payment Reconciliation | Partial + custom | [350 Intersection of Two Arrays II](https://leetcode.com/problems/intersection-of-two-arrays-ii/); [`payment_reconciliation`](../payment_reconciliation/) |
| Transaction Fee | Close parsing/calculation pattern | [2288 Apply Discount to Prices](https://leetcode.com/problems/apply-discount-to-prices/) |
| Email-domain matching | Close domain/index patterns | [811 Subdomain Visit Count](https://leetcode.com/problems/subdomain-visit-count/) and [721 Accounts Merge](https://leetcode.com/problems/accounts-merge/) |

## Local verification

The nine runnable custom packs were checked with temporary reference implementations, then restored to
intentional starter state:

| Pack | Visible reference verification |
|---|---:|
| Linked Merchant / Entity Clustering | 9/9 |
| Join Two Datasets | 7/7 |
| Merchant Fraud Score | 7/7 |
| WebSocket Load Balancer | 9/9 |
| Datacenter Request Routing | 8/8 |
| Merchant Fraud Thresholds | 8/8 |
| Credit Card Validation / Luhn | 6/6 |
| Accept-Language Header Parser | 9/9 |
| Payment Reconciliation | 8/8 |
| **Total** | **71/71** |

Run any pack from the repository root with:

```bash
python3 custom_practice/stripe/<pack_name>/run_tests.py
```

Every Notion `code` database page selected by this map must carry the `stripe` value in its
`from list` property, including existing pages reused rather than duplicated.

## Notion sync

Destination: [code database](https://app.notion.com/p/6d07ce0d2a724cc0925de42d5df264cb)

- 24 selected LeetCode notes: 10 existing pages reused, 14 missing pages created.
- 9 runnable custom notes created.
- Final audit: 33/33 selected pages have `stripe` in `from list`; no selected title is duplicated.

Custom pages:

- [Linked Merchant / Entity Clustering](https://app.notion.com/p/3c1d741a7f40817bbba9ff07c73de529)
- [Join Two Datasets](https://app.notion.com/p/3c1d741a7f4081baa6cadfbccd6514ea)
- [Merchant Fraud Score](https://app.notion.com/p/3c1d741a7f408199af3ae6e2da791bfe)
- [WebSocket Load Balancer](https://app.notion.com/p/3c1d741a7f4081288c85c144d817e531)
- [Datacenter Request Routing](https://app.notion.com/p/3c1d741a7f40813d9ef3ce5f635b8e28)
- [Merchant Fraud Thresholds](https://app.notion.com/p/3c1d741a7f4081bb95f2cac85ba55df9)
- [Credit Card Validation / Luhn](https://app.notion.com/p/3c1d741a7f40819788add1b4582d1868)
- [Accept-Language Header Parser](https://app.notion.com/p/3c1d741a7f4081dea905d08272da3a4c)
- [Payment Reconciliation](https://app.notion.com/p/3c1d741a7f408103a73cfa1a8cb59fb8)
