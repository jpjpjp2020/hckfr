## Anon feedback web service:

### Status:

- Std reg and auth work.
- Linking employer and oversight accounts works.
- Can create and manage feedback rounds.
- Can send and receive and read/monitor specific feedback.
- No email verification integrations.
- No encryption yet between senders and receivers.
- Pretty much missing anything that makes sense to be integrated vs developed.

### Build logic:

- Removing anything that could be used to indentify sender if it were IRL SaaS (for ex: feedback sender accounts cannot be set up with email+pw; only with username+pw).
- Main end user needs to set up a secondary different (oversight) account which also gets all the same raw feedback, reducing the possiility to skew feedback in aggregate.
- There is a minimum sending window of 7 days from feedback round creation, which can be extended and only 1 round can receive feedback at the same time - eliminating the possibility to send targeted/not anon feedback links.
- Feedback round creation generates a random code, which can be used to send feedback.
- Using the code to send feedback sends it both to the round creatr and to the oversight account.
- There is a data retention period (37d by default), which can be extended globally or later by account type/tier - hopefully reducing the db load and offering logical upgrade options as SaaS.
- Feedback forms do not have any setup for questions and scoring, as this would be the best way to skew data in aggregate - announcing a topic should be enough for v.1 to get raw feedback.

### UI

- Mobile first only atm.
- Tailwind CSS
- Very minimalist, as mainly would be  text-based service

