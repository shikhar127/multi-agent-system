# Robots versus Robots — QA Checklist

Use before every deploy. Each item has an exact click-path and the expected UI text to verify.

---

## 1. Free Tier — OAuth Connect Flow

1. Load page → click **FREE FIGHTER**
2. Expected: key input hides; "CONNECT OPENROUTER →" button appears
3. Click **CONNECT OPENROUTER →**
4. Expected: new tab opens to OpenRouter OAuth page
5. Complete OAuth → return to page
6. Expected: button changes to "✓ CONNECTED" or shows model count note; "DISCONNECT" option appears
7. Click **DISCONNECT**
8. Expected: returns to "CONNECT OPENROUTER →" state; key cleared

---

## 2. Paid Tier — API Key Flow

1. Click **PAID FIGHTER**
2. Expected: API key input appears
3. Enter a valid OpenRouter key → click **START THE FIGHT →** (or type a question first)
4. Expected: "VALIDATING KEY…" appears briefly, then fight begins
5. Enter an invalid key → click **START THE FIGHT →**
6. Expected: error panel shows "Invalid API key" or similar; fight does not start

---

## 3. Full Fight Run (Paid Tier)

1. Enter question: `Should companies adopt a four-day work week?`
2. Click **START THE FIGHT →**
3. Expected sequence:
   - Loading panel appears with "READING YOUR QUESTION…"
   - If question is classified as non-answerable: reframe panel appears (see §6)
   - If ANSWERABLE or after reframe choice: "SOLVER IS BUILDING THE CASE…" + Round 1 card appears
   - Round 1 tag shows `IN PROGRESS` → changes to `POSITION: CONSTRUCTED` (or similar) after completion
   - "CLASH!!" divider appears
   - "CHALLENGER IS SHARPENING ITS ATTACK…" + Round 2 Challenger card, tag = `IN PROGRESS`
   - Challenger completes → `ATTACK: DELIVERED` (or similar); Scout starts (`IN PROGRESS`)
   - Scout completes → `SCAN: COMPLETE` (or similar)
   - "CONVERGENCE!!" divider appears
   - "SOLVER IS FORGING THE FINAL POSITION…" + Round 3 card, tag = `IN PROGRESS`
   - Round 3 completes → position delta block appears (POSITION HELD or POSITION UPDATED)
   - "THE SYNTHESIZER IS DELIVERING THE VERDICT…"
   - Verdict panel appears with: summary, full reasoning, action items, confidence badge, trace
4. After verdict: 3 next-question chips appear below
5. **ABORT** scenario: during any round, click **ABORT FIGHT** → all cards stop; failed/aborted tags appear; Try Again shown

---

## 4. Try Again + Question Preservation

1. Complete a fight
2. Click **TRY AGAIN**
3. Expected: all results hidden; original question is still in the input field

---

## 5. Next-Question Chips

1. After a completed fight, scroll down to suggestion chips
2. Expected: 3 chips with editable question text and "⚡ FIGHT THIS →" button
3. Click inside a chip → edit the question text
4. Click **⚡ FIGHT THIS →**
5. Expected: fight starts with the edited question

---

## 6. Reframe Panel

1. Enter a subjective/non-answerable question: `What is the best programming language?`
2. Click **START THE FIGHT →**
3. Expected: reframe panel appears with:
   - Warning label: `THIS QUESTION HAS NO SINGLE ANSWER` (or similar)
   - Explanation of why
   - Reframed question in amber left-bordered box
   - "FIGHT THE REAL QUESTION →" button and "KEEP MY ORIGINAL QUESTION →" button
4. Test each path:
   - **FIGHT THE REAL QUESTION →**: fight runs on reframed question; "REFRAMED FROM: [original]" notice appears above results
   - **KEEP MY ORIGINAL QUESTION →**: fight runs on original question; no reframe notice
   - **✕ CANCEL**: reframe panel hides; form returns to idle

---

## 7. More Options Panel

1. Click **MORE OPTIONS ▼**
2. Expected: panel opens showing model selects for Solver, Challenger, Scout
3. Change models, run a fight
4. Expected: fight uses selected models; selections persist after fight ends

---

## 8. Keyboard Navigation

1. Tab through all controls on page with keyboard only
2. Expected: visible yellow focus ring on every focusable element
3. Tab to **START THE FIGHT →** → press Enter → fight should start
4. When reframe panel appears: focus should auto-move to the primary CTA button

---

## 9. Mobile Layout (390px width)

1. Open DevTools → set viewport to 390px wide (iPhone 15)
2. Expected:
   - Nav subtitle hidden; wordmark visible
   - Form inputs full-width; fight button full-width
   - Robot character panels hidden
   - Round cards stack vertically
   - Reframe panel padding: 36px 20px
   - Position delta and attack-target blocks have reduced padding (10px 12px / 8px 12px)
   - Clash bars truncate correctly (last word hidden)

---

## 10. Copy Verdict

1. Complete a fight
2. Click **COPY VERDICT**
3. Expected: button text changes to "COPIED!" for ~2s; clipboard contains verdict summary + reasoning

---

## 11. Cmd+Enter Shortcut

1. Focus the question textarea → type a question
2. Press **Cmd+Enter**
3. Expected: fight starts (same as clicking START THE FIGHT →)

---

## Regression Baseline (Smoke Test)

Run items 3, 4, 6 on every deploy. If any of these fail, block the release.

| Test | Expected | Pass |
|---|---|---|
| Full fight run, paid tier | All rounds complete, verdict renders | ☐ |
| Try Again preserves question | Question not cleared | ☐ |
| Reframe panel — both paths | Correct question used in fight | ☐ |
| Abort mid-fight | Cards stop, ABORTED tags shown | ☐ |
| Mobile layout at 390px | No overflow, round cards stack | ☐ |
