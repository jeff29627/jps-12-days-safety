# JPS Anderson — 12 Days of Safety (2026)

A static GitHub Pages website that automatically shows the scheduled challenge in **America/New_York**. The website does **not** collect personal data or select winners. Microsoft Forms + Power Automate + Excel Online handle entries and drawings.

## Files
- `index.html`, `style.css`, `app.js`: website and Enplug-friendly TV mode.
- `config.js`: edit form URL, site URL, and optional published winner names.
- `power-automate/draw-winner-office-script.ts`: Excel Online Office Script for winner selection.
- `.nojekyll`: tells GitHub Pages to serve static files as-is.

## 1. Create the Microsoft Form (one form, one permanent link)
1. Go to https://forms.office.com, create a **New Form** named `JPS Anderson — 12 Days of Safety 2026`.
2. Add **required** questions, with these EXACT labels:
   - `EmployeeID` — Text. Use a company-issued employee identifier; do not ask for SSNs.
   - `EmployeeName` — Text.
   - `Shift` — Choice: `1st`, `2nd`, `3rd`.
   - `Day` — Choice: `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`.
   - `Answer` — Choice: `A`, `B`, `C`.
3. In the description: `Read today's question on the JPS Christmas Safety website. Select today's Day and your answer (A, B or C). Only entries submitted during that day's official window qualify. One entry per employee per day. Winners may only win once.`
4. Configure the form to accept all eligible employees, including those without a company login if needed. If using **Anyone can respond**, Microsoft Forms cannot itself authenticate the respondent; the draw script deduplicates employee IDs but HR/EHS must verify identities and eligibility. Do not enable 'One response per person' if you want one submission each of 12 days.
5. In **Collect responses**, copy the **response** URL (not the edit URL).
6. Paste it into `config.js` as `formUrl`.
7. NOTE: The question/answer is shown on the website; the Form records only the letter. Employees must select the correct Day. The draw script enforces both the Day and the submission window. If you prefer to hide the correct answer from all website visitors, leave it only in the private Office Script.

## 2. Create a private Excel workbook
Create `JPS_Christmas_Safety_Entries.xlsx` in a restricted SharePoint/OneDrive location accessible to the Power Automate connection. Make two worksheets with Excel **tables** (Insert > Table) named exactly `Entries` and `Winners`.

**Entries table headers, exact order:**
`SubmittedAt | Day | EmployeeID | EmployeeName | Shift | Answer`

**Winners table headers, exact order:**
`Day | Date | EmployeeID | EmployeeName | Shift | Prize | DrawnAt`

The workbook must remain **private**. Never commit it to GitHub Pages.

## 3. Power Automate flow A — save submissions
Create an **Automated cloud flow**:
1. Trigger: **Microsoft Forms — When a new response is submitted**. Select your game Form.
2. Action: **Microsoft Forms — Get response details**, using the Response Id from the trigger.
3. Action: **Excel Online (Business) — Add a row into a table**, pointing to the private workbook and `Entries` table.
4. Map:
   - `SubmittedAt` = expression `utcNow()` (UTC ISO timestamp).
   - `Day` = the `Day` answer from Forms.
   - `EmployeeID` = the `EmployeeID` answer.
   - `EmployeeName` = the `EmployeeName` answer.
   - `Shift` = the `Shift` answer.
   - `Answer` = the `Answer` answer.
5. Save and test a sample entry. Check the Excel table for the exact values and an ISO UTC timestamp.

## 4. Power Automate flow B — draw one winner each business day
1. In Excel for the web, open the workbook, choose **Automate > New Script**, paste `power-automate/draw-winner-office-script.ts`, and save as `JPS Draw Winner`.
2. Create a **Scheduled cloud flow** with **Recurrence**: every 1 week, Monday through Friday, **7:10 AM**, time zone **Eastern Time (US & Canada)** (or the equivalent time-zone identifier shown in your tenant). Set the start date before December 3, 2026.
3. Action: **Excel Online (Business) — Run script**. Choose the workbook and `JPS Draw Winner`.
4. For script input `nowUtc`, use expression `utcNow()`.
5. Optional: Add a Teams/email notification to EHS/HR with the script result. **Verify employee eligibility before publicly posting a name.**
6. The script waits until a game day closes, chooses the oldest undrawn day, filters entries to the correct time window and answer, removes duplicates and previous winners, and appends one winner to the `Winners` table.
7. If the flow misses multiple days, **rerun manually** until caught up. It will never intentionally draw a day twice. Do not run concurrently; set the recurrence trigger concurrency to 1 if available.
8. For no eligible entries, the script leaves the day undrawn for EHS/HR review rather than inventing a winner.

**Important:** Automatic drawing is not automatic public posting. EHS/HR can manually update the optional `winners` field in `config.js` with approved first name/initial or an anonymized message, then commit the file. This keeps the employee roster private.

## 5. Publish on GitHub Pages
1. GitHub > New repository: `jps-12-days-safety`. Make it **Public** only if approved for a public employee-facing site. Pages sites can be publicly accessible; do not include employee data or internal confidential information.
2. Upload the website files (`index.html`, `style.css`, `app.js`, `config.js`, `.nojekyll`). The `power-automate` folder can be stored in the repo because it contains no employee data or credentials, but keep Excel data private.
3. Repository **Settings > Pages > Build and deployment**: Source `Deploy from a branch`; Branch `main`, folder `/ (root)`; Save.
4. Wait for GitHub Pages to publish. Your URL should resemble `https://YOUR-USERNAME.github.io/jps-12-days-safety/`.
5. Set `siteUrl` in `config.js` to that exact URL. Commit.
6. Test both `https://YOUR-USERNAME.github.io/jps-12-days-safety/` and `...?tv=1`.

## 6. QR code and Enplug TV
- The website shows a QR code for the permanent `siteUrl` using a third-party QR image service. The URL is sent to that service, so if external services are restricted, replace this with a locally generated QR image (see below).
- To make an offline/static QR PNG after you know your final URL, on your computer run `python -m pip install qrcode[pil]`, then `python make_qr.py https://YOUR-USERNAME.github.io/jps-12-days-safety/`. This creates `jps-game-qr.png` for posters/TVs.
- Add the TV-mode URL (`https://YOUR-USERNAME.github.io/jps-12-days-safety/?tv=1`) as a website/webpage item in your Enplug content playlist. Confirm your Enplug device supports live webpages, auto refresh and internet access.
- TV mode intentionally hides the Forms entry button. Display the QR image separately on a slide or poster so employees can scan it in an approved area.
- The page checks the Eastern time every 30 seconds, and changes the question at 7:00 AM Eastern when the player remains running.

## 7. Dates and draw windows
The website opens the following days at **7:00 AM ET**: Dec 3, 4, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18 (2026).
Entries close at **7:00 AM ET on the next scheduled game day**; the last closes **Dec 21, 2026 at 7:00 AM ET**. Drawings run at **7:10 AM ET on the closing day**. No weekend changes.

## 8. Testing and security
- Use a private test copy of the Form and workbook before going live. Test one correct and one incorrect answer, duplicate employee IDs, a previous winner, and an entry outside the window.
- The Office Script uses `Math.random()` to choose an eligible row. This is suitable for an informal workplace giveaway but is not a cryptographically auditable raffle. HR should approve the contest and eligibility rules.
- Do not put personal employee IDs, response exports, Microsoft authentication tokens, or private Forms edit links in the public repo.
- The website is display-only and uses the viewer's device clock to determine the current date/time; make sure Enplug player clocks are correct. The private draw script independently enforces UTC submission windows.
- Review corporate rules about prizes, employee data retention, accessibility, and public website hosting.
