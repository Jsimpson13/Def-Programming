==================================================
           Floral Pirates - User Manual

PREREQUISITES
--------------------------------------------------
Before running the program, ensure the following:
- The entire 'Def-Programming' folder MUST be located on your Desktop.
- Ensure the 'prereq.sh' and 'start-program.sh' files have the correct permissions (chmod u+x <file>)

--------------------------------------------------
INITIAL SETUP (Run once)
--------------------------------------------------
1. Open a terminal window.

2. Navigate to the Def-Programming folder:
   cd ~/Desktop/Def-Programming

3. Run the prerequisites setup script:
   ./prereq.sh

   This will install required dependencies and perform any necessary configuration.

--------------------------------------------------
STARTING THE PROGRAM
--------------------------------------------------
IMPORTANT: Before starting the program, make sure any previous client or server terminal windows are CLOSED.

1. In a terminal, go to the Def-Programming folder if you're not already there:
   cd ~/Desktop/Def-Programming

2. Run the start script:
   ./start-program.sh

3. Give it a few seconds

   This will launch the secure server and begin handling messages.

--------------------------------------------------
TROUBLESHOOTING
--------------------------------------------------
- Make sure no server or client terminal is open before launching.
- Ensure all scripts have the correct permissions (chmod +x).
- If you move the folder from the Desktop, paths may break.
- If the database is deleted or corrupted, run the 'fix-db.sh' script
   IMPORTANT: This will delete all newly created user profiles and will reset the database to its original state

--------------------------------------------------
You're all set! Enjoy using Floral Pirates.
==================================================

