<h1>To run this API, run the following steps:</h1>

<h3>1. Generate and activate a virtual environment using python=3.13.2:</h3>
   conda create -n restAPI_test python=3.13.2<br>
   conda activate restAPI_test<br>
   
<h3>3. Install requirements:</h3>
   pip install -r requirements.txt<br>

<h3>5. Open ETL.ipynb and run all the codes in the cells</h3>

<h3>7. Run z1_build_db.py (To build SQLite database):</h3>
   python z1_build_db.py<br>

<h3>9. Run z2_runAPI.py (To start API):</h3>
   python z2_runAPI.py<br>

<h3>11. Open another terminal</h3>

<h3>13. Run z3_CLI_interface.py (To search drug info using API):</h3>
   python z3_CLI_interface.py --help<br>
   or<br>
   python z3_CLI_interface.py --target ENSG00000081248 --num-cases 10 --weight 0.5

