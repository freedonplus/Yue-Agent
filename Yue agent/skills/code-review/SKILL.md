---
name: 代码审查
description: 代码审查清单、PR审查模式和反馈模板。当用户要求“审查这段代码”、“代码审查清单”、“PR审查模板”、“审查最佳实践”、“撰写审查反馈”或任何代码审查任务时使用。
---

# Code Review

Checklists, patterns, feedback techniques, and automation for effective code reviews.

---

## Review Checklist by Category

### Logic and Correctness
- [ ] Does the code do what the PR description says it does?
- [ ] Are edge cases handled (empty inputs, boundary values, concurrent access)?
- [ ] Are error conditions handled gracefully with appropriate error types?
- [ ] Are there off-by-one errors in loops, slices, or pagination?
- [ ] Are null/undefined/nil cases handled?
- [ ] Does the control flow match the intended behavior (early returns, fallthrough)?

### Security
- [ ] No hardcoded secrets, keys, tokens, or passwords
- [ ] Input validation on all user-supplied data (query params, body, headers)
- [ ] No SQL injection, XSS, or command injection vectors
- [ ] Authentication and authorization checks on every endpoint
- [ ] Sensitive data not logged, not in error messages, not exposed in responses
- [ ] CSRF protection on state-changing requests
- [ ] Rate limiting on sensitive endpoints (auth, password reset)

### Performance
- [ ] No N+1 database queries (queries inside loops)
- [ ] No memory leaks (event listeners, timers, subscriptions not cleaned up)
- [ ] Large datasets paginated, not loaded entirely into memory
- [ ] Expensive computations cached where appropriate
- [ ] No blocking operations on the main thread or event loop
- [ ] Database queries use indexes (check EXPLAIN plans for new queries)

### Readability and Maintainability
- [ ] Code is understandable without needing the author to explain it
- [ ] Functions have a single responsibility and a clear name
- [ ] No duplicated logic (DRY where it reduces coupling, not blindly)
- [ ] Naming conventions are consistent with the codebase
- [ ] No dead code, commented-out code, or unused imports
- [ ] Complex logic has comments explaining why, not what

### Testing
- [ ] Tests cover the primary success path
- [ ] Edge cases and error paths tested
- [ ] Tests are deterministic (no flaky tests introduced)
- [ ] Test names describe the behavior, not the implementation
- [ ] Mocks are minimal and realistic

---

## How to Give Constructive Feedback

The praise sandwich is patronizing and everyone sees through it. Be direct and kind. Critique the code, not the person.

### Principles
- Be specific. "This will throw if `user` is null on line 42" beats "handle errors better."
- Explain the why. Don't just say what to change -- explain the risk or benefit.
- Offer alternatives. If you flag a problem, suggest a solution or direction.
- Acknowledge tradeoffs. If a shortcut is reasonable given constraints, say so.
- Ask genuine questions. "What's the reasoning for X?" is valid when you don't understand.

### Prefixed Comments

```
[nit] Minor style issue, take or leave
[suggestion] Optional improvement idea
[question] Seeking understanding, not necessarily a change
[issue] Must be addressed before merge
[praise] Something done well worth calling out
[thought] Sharing context or perspective, no action needed
```

### Direct Feedback Examples

```
Instead of: "This is wrong"
Write: "This will fail when `items` is empty because `items[0]` returns undefined."

Instead of: "Why did you do it this way?"
Write: "Was there a performance reason for the manual loop? Array.filter would be more readable."

Instead of: "This is bad code"
Write: "This function handles validation, transformation, and persistence. Splitting would make each testable independently."
```

---

## PR Size Guidelines

```
Small (< 200 lines changed)   -> Review in 15-30 min. Ideal size.
Medium (200-400 lines)         -> Review in 30-60 min. Acceptable.
Large (400-800 lines)          -> Consider splitting.
Very large (> 800 lines)       -> Should almost always be split.
```

### When to Split

- Refactoring mixed with feature changes. Ship the refactor first.
- Infrastructure changes mixed with business logic.
- Database migrations with application code. Migrate first, then use.
- Multiple independent features or fixes bundled together.

### When Large PRs Are Acceptable

- Generated code (protobuf, OpenAPI, migration boilerplate).
- Bulk renames or automated reformatting.
- Initial project setup or deleting large amounts of dead code.

---

## Review Speed and Turnaround

Slow reviews kill velocity. Fast reviews compound into fast teams.

- **Target**: First-pass review within 4 business hours.
- **Unblocking**: If a PR blocks other work, prioritize it. Say so in the review request.
- **Async norms**: "I'll review by end of day" is better than silence.
- **Re-reviews**: After feedback is addressed, re-review within 2 hours. Focus on the diff, don't restart.
- **Don't batch**: Review PRs as they come in. End-of-day batching creates bottlenecks.
- **Stale PRs**: Unreviewed for 24+ hours? Escalate or reassign.

---

## Automated Review Tools

Automate what machines do better than humans. Save reviewers for logic and design.

### GitHub Actions

```yaml
name: PR Checks
on: [pull_request]
jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test -- --coverage
```

### Danger.js

```javascript
import { danger, warn, fail } from 'danger';

if (danger.github.pr.additions + danger.github.pr.deletions > 500) {
  warn('This PR is large. Consider splitting.');
}
if (!danger.github.pr.body || danger.github.pr.body.length < 20) {
  fail('Please add a meaningful PR description.');
}
const sensitive = danger.git.modified_files.filter(f =>
  f.includes('migration') || f.includes('.env') || f.includes('auth')
);
if (sensitive.length > 0) {
  warn(`Sensitive files changed: ${sensitive.join(', ')}`);
}
```

### Other Tools
- **CodeRabbit** -- AI-powered review summaries and inline suggestions
- **SonarQube / SonarCloud** -- static analysis for bugs, smells, security hotspots
- **Codacy / CodeClimate** -- automated code quality scoring
- **Reviewbot / Prow** -- bot-driven labeling, assignment, merge gating
- **Codecov / Coveralls** -- test coverage tracking and PR comments

---

## Security-Focused Review

Check against OWASP Top 10 patterns most likely to appear in application code.

- **Injection**: User input reaching queries, commands, or templates without parameterization.
- **Broken auth**: Missing auth checks on new endpoints. Tokens that don't expire.
- **Data exposure**: PII in logs, error messages, or API responses. Secrets in client code.
- **Access control**: Can user A access user B's resources? Admin routes unprotected?
- **Misconfiguration**: Debug mode in production. Default credentials. Verbose errors.
- **XSS**: User input rendered without encoding in HTML or JavaScript contexts.
- **SSRF**: Server requests using user-controlled URLs without allowlist validation.

### Auth Review Specifics
- Session tokens regenerated after login.
- Password reset tokens are single-use and time-limited.
- JWT validation checks signature, expiration, issuer, and audience.
- API keys scoped to minimum necessary permissions.

---

## Performance Review Patterns

### N+1 Queries

```javascript
// BAD: one query per iteration
for (const post of posts) {
  post.author = await db.query('SELECT * FROM users WHERE id = $1', [post.author_id]);
}
// GOOD: batch
const authorIds = [...new Set(posts.map(p => p.author_id))];
const authors = await db.query('SELECT * FROM users WHERE id = ANY($1)', [authorIds]);
```

### Memory Leaks
- Event listeners without cleanup on unmount/destroy.
- Intervals/timeouts not cleared. Subscriptions not unsubscribed.
- Growing caches without eviction. Closures holding references to large objects.

### Unnecessary Renders (React)
- Objects or arrays created inline in JSX props (new reference every render).
- Missing `useMemo`/`useCallback` for expensive computations or callback props.
- Context providers with unmemoized object values.

---

## Reviewing Database Migrations

Migrations deserve extra scrutiny because they're hard to reverse in production.

- [ ] Is the migration reversible? Does the rollback function work?
- [ ] Will it lock tables? Adding a column with default on large tables locks in some databases.
- [ ] Are new columns nullable or have defaults? Non-nullable without default fails on existing rows.
- [ ] Indexes added concurrently where possible (`CREATE INDEX CONCURRENTLY`)?
- [ ] Data migration separated from schema migration?
- [ ] Is the migration idempotent (safe to run twice)?
- [ ] Estimated run time tested against production-sized data?
- [ ] Dropping columns has a deprecation path (stop reading first, then drop)?

---

## Common Antipatterns in Reviews

**Nitpicking** -- Commenting on formatting and cosmetics a linter should catch. If you're debating semicolons, add a linter rule.

**Rubber-Stamping** -- "LGTM" on a 500-line PR after 2 minutes. If you can't review properly, let someone else.

**Bike-Shedding** -- Long debates on trivial matters while ignoring real issues. Keep comments proportional to impact.

**Gatekeeper Mentality** -- Blocking PRs over personal style preferences not in the team's style guide. Enforce shared standards, not individual taste.

**Drive-By Reviews** -- One vague comment ("this seems off") then disappearing. Either review thoroughly or don't start.

---

## Review Templates by PR Type

### Feature PR
```markdown
- [ ] Requirements from the issue/spec are met
- [ ] Edge cases identified and handled
- [ ] Tests cover happy path and failure cases
- [ ] No security regressions (auth, input validation)
- [ ] Performance acceptable (no new N+1, no blocking calls)
- [ ] Documentation updated if public API changed
```

### Bugfix PR
```markdown
- [ ] Root cause identified (not just symptoms patched)
- [ ] Regression test added that fails without the fix
- [ ] Fix doesn't introduce new edge cases
- [ ] Related code checked for same class of bug
```

### Refactor PR
```markdown
- [ ] Behavior unchanged (no functional changes mixed in)
- [ ] Existing tests pass without modification
- [ ] Code is measurably better (simpler, fewer dependencies, more testable)
- [ ] Performance characteristics unchanged or improved
```

### Dependency Update PR
```markdown
- [ ] Changelog reviewed for breaking changes
- [ ] Major version bumps justified and tested
- [ ] Lock file changes are consistent (no unexpected additions)
- [ ] No new vulnerabilities introduced
- [ ] Bundle size impact acceptable
```

---

## Code Ownership and CODEOWNERS

```
# .github/CODEOWNERS
*                       @org/platform-team
/src/components/        @org/frontend-team
/src/api/               @org/backend-team
/src/auth/              @org/security-team
/db/migrations/         @org/dba-team
/terraform/             @org/devops-team
/.github/workflows/     @org/devops-team
```

- Keep ownership granular. One team owning everything defeats the purpose.
- Review CODEOWNERS quarterly. Remove departed members. Update assignments.
- Use for mandatory review, not as a notification mechanism.
- Combine with branch protection rules requiring CODEOWNERS approval.

---

## Pair Review vs Async Review

### Pair Review (Synchronous)
**Best for**: Complex architecture, unfamiliar codebases, onboarding, contentious designs.
- Faster resolution. No async back-and-forth.
- Higher bandwidth catches design issues written comments miss.
- Time-expensive. Reserve for PRs where async would take 3+ rounds.

### Async Review (Standard)
**Best for**: Routine changes, well-understood domains, distributed teams.
- Reviewer reads at their own pace. More thoughtful.
- Written feedback creates searchable record.
- Risk of miscommunication. Tone is hard in text.

### When to Switch from Async to Pair
- More than 2 rounds of back-and-forth on the same issue.
- Reviewer and author disagree and comments aren't resolving it.
- The PR touches unfamiliar territory needing a walkthrough.

---

## When to Request Changes vs Approve with Comments

### Request Changes
- Bug that will break production.
- Security vulnerability (injection, auth bypass, data leak).
- PR doesn't do what the description says.
- Tests missing for critical paths.
- Change will cause data loss or corruption.

### Approve with Comments
- Suggestions are improvements but code works correctly as-is.
- Style preferences not in the team's style guide.
- Minor refactoring opportunities that aren't urgent.
- Questions driven by curiosity, not blockers.

**The rule**: If the PR shipped right now, would it cause harm? Request changes. If it works but could be better? Approve with comments. Trust the author to address optional feedback.

---

## Review Workflow

```
1. Read the PR description and linked issue
2. Understand context: what problem, why now?
3. Check PR size. If too large, ask to split before reviewing
4. Review test files first to understand expected behavior
5. Review main changes with the checklist for the PR type
6. Check correctness, security, performance, readability
7. Run locally if the change is complex or risky
8. Leave feedback using prefixed comments
9. Summarize with overall assessment and clear status
```

---

## Tools

- **Danger.js** -- programmable PR review rules and warnings
- **CodeRabbit** -- AI-powered review summaries and inline suggestions
- **SonarQube / SonarCloud** -- static analysis for bugs, smells, security hotspots
- **GitHub Actions** -- CI checks, linting, test coverage gates
- **Codecov / Coveralls** -- test coverage tracking and PR comments

## References

- Google Engineering Practices -- Code Review Guide: https://google.github.io/eng-practices/review/
- Conventional Comments: https://conventionalcomments.org/
- OWASP Code Review Guide: https://owasp.org/www-project-code-review-guide/

---

## 参考资料：references/CODE-PATTERNS.md

# Common Code Review Patterns

## Pattern: Extract Function
When a function is too long or has multiple responsibilities, extract into smaller functions.

**Before:**
```python
def process_user_data(user_data):
    # Validate email
    if '@' not in user_data['email']:
        raise ValueError("Invalid email")
    
    # Validate age
    if user_data['age'] < 18:
        raise ValueError("User must be 18+")
    
    # Process data
    name = user_data['name'].strip().title()
    email = user_data['email'].lower()
    
    return {
        'name': name,
        'email': email,
        'age': user_data['age']
    }
```

**After:**
```python
def validate_user_data(user_data):
    validate_email(user_data['email'])
    validate_age(user_data['age'])

def validate_email(email):
    if '@' not in email:
        raise ValueError("Invalid email")

def validate_age(age):
    if age < 18:
        raise ValueError("User must be 18+")

def normalize_user_data(user_data):
    return {
        'name': user_data['name'].strip().title(),
        'email': user_data['email'].lower(),
        'age': user_data['age']
    }

def process_user_data(user_data):
    validate_user_data(user_data)
    return normalize_user_data(user_data)
```

## Pattern: Replace Magic Numbers
Replace unexplained numbers with named constants.

**Before:**
```python
if user.age > 21:
    tax_rate = 0.125
```

**After:**
```python
LEGAL_DRINKING_AGE = 21
SALES_TAX_RATE = 0.125

if user.age > LEGAL_DRINKING_AGE:
    tax_rate = SALES_TAX_RATE
```

## Pattern: Add Type Hints
Make code more readable and enable IDE support.

**Before:**
```python
def calculate_discount(price, quantity):
    if quantity > 10:
        return price * 0.9
    return price
```

**After:**
```python
def calculate_discount(price: float, quantity: int) -> float:
    if quantity > 10:
        return price * 0.9
    return price
```

## Pattern: Use Composition over Inheritance
Prefer composition for more flexible code.

**Before:**
```python
class Animal:
    def eat(self): pass
    def sleep(self): pass

class Dog(Animal):
    def eat(self): print("Eating dog food")
    def bark(self): print("Woof!")
```

**After:**
```python
class Eater:
    def eat(self): pass

class Sleeper:
    def sleep(self): pass

class Dog:
    def __init__(self):
        self.eater = Eater()
        self.sleeper = Sleeper()
    
    def bark(self):
        print("Woof!")
```

## Pattern: Guard Clauses
Use early returns to reduce nesting.

**Before:**
```python
def process_order(order):
    if order is not None:
        if order.items:
            total = 0
            for item in order.items:
                total += item.price
            return total
    return None
```

**After:**
```python
def process_order(order):
    if order is None:
        return None
    
    if not order.items:
        return None
    
    return sum(item.price for item in order.items)
```

---

## 参考资料：references/CODE-REVIEW-GUIDE.md

# Code Review Best Practices

## Purpose of Code Reviews
- Catch bugs and security issues early
- Share knowledge across team
- Maintain code quality standards
- Improve code readability and maintainability
- Foster collaboration and learning

## What to Review

### Correctness
- Does the code do what it's supposed to do?
- Are edge cases handled?
- Are there potential bugs or race conditions?
- Are error cases handled properly?

### Performance
- Will this code scale?
- Are there unnecessary loops or operations?
- Are algorithms optimal?
- Are resources (memory, CPU) used efficiently?

### Security
- Are inputs validated?
- Is sensitive data protected?
- Are SQL injection risks mitigated?
- Are authentication/authorization correct?
- Are dependencies up-to-date?

### Maintainability
- Is the code readable and understandable?
- Are variable and function names descriptive?
- Is documentation adequate?
- Is the code DRY (Don't Repeat Yourself)?
- Are design patterns applied appropriately?

### Testing
- Is test coverage adequate?
- Do tests cover edge cases?
- Are tests maintainable and clear?
- Is mocking used appropriately?

## Code Review Checklist

### Before Submitting
- [ ] Code follows project style guide
- [ ] No hardcoded values or credentials
- [ ] Tests are written and passing
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No debug code or console.log statements
- [ ] Performance impact assessed

### During Review
- [ ] Code is readable and well-structured
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] Security best practices followed
- [ ] No breaking changes without discussion
- [ ] Performance is acceptable
- [ ] Tests adequately cover functionality

## Communication Guidelines

### Constructive Feedback
✓ "This could be more efficient using a Set instead of an array"
✗ "Your code is inefficient"

✓ "Consider extracting this into a separate function for readability"
✗ "This is too long"

✓ "Have you considered this edge case?"
✗ "You didn't handle this case"

### Approve When
- [ ] All feedback been addressed
- [ ] Code quality meets standards
- [ ] Tests are adequate
- [ ] Documentation is complete
- [ ] No outstanding concerns

### Request Changes When
- [ ] Security issues found
- [ ] Major bugs identified
- [ ] Architecture concerns
- [ ] Test coverage inadequate
- [ ] Documentation missing

## Review Example

### Code Submission
```python
def calculate_total(items):
    total = 0
    for item in items:
        total = total + item['price'] * item['quantity']
    return total
```

### Review Comment
```
Great implementation! A few suggestions:

1. Prefer += operator: `total += item['price'] * item['quantity']`
2. Consider using sum() with a generator expression for more Pythonic code:
   ```python
   return sum(item['price'] * item['quantity'] for item in items)
   ```
3. Add docstring and type hints:
   ```python
   from typing import List, Dict
   
   def calculate_total(items: List[Dict]) -> float:
       """Calculate total price from items list."""
       return sum(item['price'] * item['quantity'] for item in items)
   ```
4. Add error handling for missing keys

This is a good optimization!
```

## Common Issues Found in Code Reviews

### Style & Formatting
- Inconsistent indentation
- Line too long (>100 chars)
- Missing whitespace for readability
- Unused imports
- Unused variables

### Functionality
- Off-by-one errors
- Missing null/error checks
- Incomplete error handling
- Logic errors

### Security
- SQL injection risks
- XSS vulnerabilities
- Hardcoded secrets
- Insecure deserialization

### Performance
- N+1 queries
- Inefficient algorithms
- Memory leaks
- Unnecessary deep copies

### Maintainability
- Magic numbers
- Unclear variable names
- Missing documentation
- Code duplication
- Complex nested logic

## Review Time Guidelines
- Small changes (< 100 lines): 10-15 minutes
- Medium changes (100-500 lines): 20-30 minutes
- Large changes (> 500 lines): 60+ minutes

**Pro tip**: Keep PR sizes small (<400 lines) for faster, more thorough reviews

## Tools for Code Review
- GitHub/GitLab/Bitbucket Reviews
- Gerrit for detailed review
- Reviewboard for documentation
- Crucible for distributed teams
- CodeStream IDE integration

---

## 参考资料：references/anti-patterns.md

# Code Review Anti-patterns

## Mistakes Reviewers Make

### 1. Nitpicking Style
```
❌ Bad: "Variable name should be camelCase not snake_case"
✓ Better: Use automated linting for style issues
```

### 2. Not Understanding Context
```
❌ Bad: Requesting change without understanding why
✓ Better: Ask questions first before suggesting changes
```

### 3. Reviewing Too Fast
```
❌ Bad: Approve without really reading code
✓ Better: Spend adequate time understanding logic
```

### 4. Reviewing Too Slow
```
❌ Bad: Delay PRs for days with detailed nitpicks
✓ Better: Balance thoroughness with team velocity
```

### 5. Being Harsh
```
❌ Bad: "This code is terrible"
✓ Better: "Good attempt. Here's how we could improve..."
```

## Mistakes Authors Make

### 1. Large PRs
```
❌ 500+ line PR
✓ < 200 lines per PR
```

### 2. Vague Descriptions
```
❌ "Fixed stuff"
✓ "Fixed login race condition where simultaneous requests created duplicate accounts"
```

### 3. Defensive Responses
```
❌ "This is fine, you don't understand"
✓ "Good point. Let me refactor this."
```

### 4. Ignoring Feedback
```
❌ Approve anyway ignoring suggestions
✓ Address or discuss feedback
```

## Effective Review Workflow

```
Author: Create small, focused PR
        ↓
Reviewer: Read description
          Review code in depth
          Leave thoughtful feedback
        ↓
Author: Address feedback
        ↓
Reviewer: Approve and merge
          (or request changes if significant)
```

Cycle time: 4-24 hours for typical PR

---

## 参考资料：references/checklists.md

# Code Review Checklists by Type

## API Endpoint Review

```
[ ] Input validation on all parameters
[ ] Authentication check
[ ] Authorization (role/permission) check
[ ] Rate limiting applied
[ ] Request size limits
[ ] Response includes only necessary data
[ ] Error responses don't leak internal details
[ ] HTTP status codes are correct
[ ] Pagination for list endpoints
[ ] API versioning considered
[ ] OpenAPI/Swagger spec updated
[ ] Integration test added
```

## Database Migration Review

```
[ ] Migration is reversible (has down migration)
[ ] No data loss for existing records
[ ] Default values for new NOT NULL columns
[ ] Indexes added for new query patterns
[ ] Large table changes use concurrent operations
[ ] Data backfill in separate migration
[ ] Tested on copy of production-like data
[ ] Migration is idempotent (can run twice safely)
[ ] Foreign keys have ON DELETE behavior
[ ] No full table locks on large tables
```

## Frontend/UI Review

```
[ ] Responsive on mobile, tablet, desktop
[ ] Keyboard navigation works
[ ] Screen reader accessible (aria labels)
[ ] Loading states shown
[ ] Error states handled and displayed
[ ] Empty states handled
[ ] Form validation with helpful messages
[ ] No layout shifts (CLS)
[ ] Images have alt text
[ ] No memory leaks (useEffect cleanup)
[ ] Internationalization considered
```

## Security Review

```
[ ] No secrets in code or config files
[ ] User input sanitized before use
[ ] SQL queries parameterized
[ ] HTML output properly escaped (XSS)
[ ] File uploads validated (type, size)
[ ] CORS configured correctly
[ ] CSRF protection on state-changing endpoints
[ ] Authentication tokens expire
[ ] Sensitive data encrypted at rest
[ ] Audit logging for sensitive operations
[ ] Dependencies checked for known vulnerabilities
```

## Performance Review

```
[ ] Database queries optimized (no N+1)
[ ] Appropriate indexes exist
[ ] Expensive operations cached
[ ] Pagination for large datasets
[ ] Images/assets optimized
[ ] Lazy loading for non-critical resources
[ ] No blocking operations on main thread
[ ] Memory usage bounded (streams for large data)
[ ] Appropriate timeouts on external calls
[ ] Connection pooling configured
```

## Infrastructure/DevOps Review

```
[ ] Terraform plan reviewed
[ ] No hardcoded IPs or credentials
[ ] Resource limits and quotas set
[ ] Health checks configured
[ ] Logging and monitoring in place
[ ] Backup strategy defined
[ ] Rollback procedure documented
[ ] Scaling policy appropriate
[ ] Network security groups minimal
[ ] Cost implications assessed
```

## PR Description Checklist

```markdown
## PR Checklist (for authors)

- [ ] Code compiles without errors
- [ ] All tests pass
- [ ] New code has tests
- [ ] Documentation updated if needed
- [ ] Breaking changes documented
- [ ] PR title follows conventional commits
- [ ] Self-reviewed the diff
- [ ] Linked related issue(s)
```

---

## 参考资料：references/review-guide.md

# Code Review Best Practices

## Before the Review

1. **Run tests locally** - Verify nothing breaks
2. **Build successfully** - No compilation errors
3. **Check CI/CD** - All automated checks pass
4. **Read the PR description** - Understand intent
5. **Look at file diff** - Get overview of changes

## During the Review

### Focus Areas

1. **Correctness**
   - Does it do what PR says?
   - Are edge cases handled?
   - Any potential bugs?

2. **Readability**
   - Is code clear?
   - Variable names make sense?
   - Comments explain why, not what?

3. **Performance**
   - Any O(n²) algorithms?
   - N+1 query problems?
   - Memory leaks possible?

4. **Security**
   - Input validation?
   - Authentication checks?
   - Secrets hardcoded?
   - SQL injection risk?

5. **Testing**
   - Test coverage?
   - Edge cases tested?
   - Positive and negative tests?

### Review Techniques

**Ask Questions**:
- "Why did you choose X over Y?"
- "What if this value is null?"
- "How does this behave under load?"

**Suggest, Don't Demand**:
- ✓ "Consider using a Set for O(1) lookups"
- ✗ "Why are you using an Array?"

**Praise Good Work**:
- "Love how you handled this edge case"
- "Great optimization"
- "Clean refactoring"

## Approval Criteria

Before approving:
- [ ] Code style consistent with project
- [ ] Logic is clear and correct
- [ ] Tests are adequate
- [ ] No security issues
- [ ] Performance acceptable
- [ ] Documentation updated

## Common Issues to Catch

```javascript
// ❌ N+1 queries
for (const user of users) {
  const orders = db.query('SELECT * FROM orders WHERE user_id = ?', user.id);
}

// ✓ Better
const orders = db.query('SELECT * FROM orders WHERE user_id IN (?)', userIds);

// ❌ Hardcoded secret
const apiKey = "sk_live_abc123xyz";

// ✓ Better
const apiKey = process.env.API_KEY;

// ❌ Missing error handling
const result = await fetch(url);
const data = await result.json();  // What if fetch fails?

// ✓ Better
try {
  const result = await fetch(url);
  if (!result.ok) throw new Error(`HTTP ${result.status}`);
  const data = await result.json();
} catch (error) {
  logger.error('Failed to fetch:', error);
}
```

## Review Time

- **Small PR (< 200 lines)**: 15-30 minutes
- **Medium PR (200-500 lines)**: 30-60 minutes
- **Large PR (> 500 lines)**: Request to split into smaller PRs

Longer reviews → More bugs missed
