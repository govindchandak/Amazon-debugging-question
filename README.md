# Amazon Debugging Round: Practice Repo

Small web apps with planted bugs, in all three stacks Amazon offers (Django, Spring Boot, Node.js). Your job: **fix the code until every test passes.** This is the same kind of task as the repository round in the Amazon SDE online assessment.

**Study guide (read this first):** https://claude.ai/artifact/7QJHdELhxxMc3JgbBnoRDe

## Questions

| # | App | Stack | Level | Bugs | Time |
|---|---|---|---|---|---|
| Sample | [HelpDesk (worked example)](sample-helpdesk) | Django, Spring Boot, Node.js | Example | 9 | 60 min |
| Q1 | [Wishlist](q1-django-wishlist) | Django | Easy | 3 | 30 min |
| Q2 | [Parcel Locker](q2-django-parcel-locker) | Django | Medium | 4 | 45 min |
| Q3 | [Task Board](q3-spring-task-board) | Spring Boot | Easy | 3 | 30 min |
| Q4 | [Returns Desk](q4-spring-returns-desk) | Spring Boot | Medium | 4 | 45 min |
| Q5 | [Gift Card Wallet](q5-node-gift-wallet) | Node.js (Express) | Easy | 3 | 30 min |
| Q6 | [Gym Class Booking](q6-node-gym-booking) | Node.js (Express) | Medium | 5 | 50 min |

Start with the worked example in your stack (the guide walks through all 9 bugs), then the Easy and Medium questions. Each folder's README is the task.

## Setup

You need Git and VS Code, plus your stack: Python 3.10+ (Django), Java 17+ with Maven or IntelliJ IDEA (Spring Boot), or Node.js 18+ (Node).

```bash
git clone https://github.com/govindchandak/Amazon-debugging-question.git
cd Amazon-debugging-question

# Django questions (once)
python -m venv venv
venv\Scripts\activate            # Windows
source venv/bin/activate         # Mac / Linux
pip install -r q1-django-wishlist/requirements.txt
```

| Stack | Run the tests |
|---|---|
| Django | `cd q1-django-wishlist` then `python manage.py test` |
| Spring Boot | `cd q3-spring-task-board` then `mvn test` (or Run the test class in IntelliJ) |
| Node.js | `cd q5-node-gift-wallet` then `npm install` and `npm test` |

## The AI coach

This repo turns your AI assistant into a coach that gives hints and **will not fix the bugs for you**.

- **VS Code + GitHub Copilot:** loads `.github/copilot-instructions.md` by itself. Use **Ask** mode, not Agent.
- **Cursor:** loads `.cursor/rules/debug-coach.mdc` by itself.
- **Anything else:** paste [AI_COACH_PROMPT.md](AI_COACH_PROMPT.md) as your first message.

## Rules

1. Do not edit the tests. They define what correct means.
2. Make the smallest change that fixes the bug.
3. After every fix, run **all** the tests again.
4. Check `git diff` before you finish: only real fixes should be in it.

Start a question over: `git checkout -- q1-django-wishlist`
