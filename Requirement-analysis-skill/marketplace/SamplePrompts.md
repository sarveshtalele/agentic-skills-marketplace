# Sample Prompts

Copy-paste prompts to try once the skill is installed. Grouped by the kind of change
you're planning.

---

## Adding a new field or endpoint

```
Add a discount_code field to the Order model and expose it on the orders API
```
```
I want to add a "remember me" checkbox to the login form
```
```
Add rate limiting to all public API endpoints
```

## Fixing a bug

```
Plan the changes needed to fix the expired-token bug in the auth endpoint
```
```
Where's the right place to fix the login endpoint rejecting valid passwords?
```

## Modifying existing behavior

```
Where should I implement dark mode for the settings page?
```
```
Modify the checkout flow to support partial refunds
```

## Removing something

```
What files do I need to touch to remove the legacy XML export feature?
```

## Asking "where" before "how"

```
What files do I need to update for 2FA on login?
What's the right place to add a new payment provider?
Where should I make this change: reject orders over $10,000 without manager approval?
```

## Controlling output

```
Plan this change but don't save anything — just show me
```
```
Plan the discount_code change and save the output to ./reports/
```
```
Give me the top 10 candidate files, not just 5, for adding audit logging
```

---

## Tips

- You don't need to say "using requirement-analysis" — the description in `SKILL.md`
  triggers automatically on phrases like "I want to add...", "where should I...", "what
  files do I need to...", or "plan this change".
- Mention exact names when you know them — `OrderService`, `discount_code`,
  `src/api/orders.py` — entity extraction sharply improves match quality when the
  requirement text contains real identifiers.
- If every candidate file scores low, the engine flags low confidence rather than
  guessing — add a more specific name or file path and re-run.
- After implementing the change, run
  [`change-impact-analysis-skill`](../../change-impact-analysis-skill/) on the files this
  plan pointed you at to see the deployment risk score before you merge.
