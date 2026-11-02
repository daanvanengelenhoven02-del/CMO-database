# CMO database: setup

1. **Google Form**: create these questions with exactly these titles (they become the sheet's column headers):
   Title, Description, Link, Context, Mechanism, Outcome. Add the guiding prompts as question descriptions.
2. **Response sheet**: open it from the form, add a column named **Approved**. Type `yes` for entries that pass review.
3. **Publish the sheet as CSV**: File > Share > Publish to web > pick the responses tab > CSV > Publish. Copy the link.
   (Keep any email/name columns out of that tab, or move approved entries to a separate "Public" tab and publish that.)
4. **GitHub**: create a free account and a new public repository. Upload everything in this folder
   (including the hidden `.github` folder; drag-and-drop the whole folder works).
5. **Secret**: repository Settings > Secrets and variables > Actions > New secret. Name: `SHEET_CSV_URL`, value: the CSV link.
6. **Form link**: edit `index.html`, replace `PASTE_YOUR_GOOGLE_FORM_LINK_HERE` with your form's link.
7. **Build**: tab Actions > "Rebuild search data" > Run workflow. It now also runs daily by itself.
8. **Publish**: Settings > Pages > Source: "Deploy from a branch", branch `main`, folder `/ (root)`.
   Your site appears at `https://YOUR-USERNAME.github.io/REPO-NAME/`.

Adding approved entries later: set Approved to `yes`, then press "Run workflow" (or wait for the daily run).
