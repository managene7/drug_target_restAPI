To run this API, run the following steps:

1. Generate and activate a virtual environment using python=3.13.2:
   conda create -n restAPI_test python=3.13.2
   conda activate restAPI_test
   
3. Install requirements:
   pip install -r requirements.txt

5. Open ETL.ipynb and run all the codes in the cells

7. Run z1_build_db.py (To build SQLite database):
   python z1_build_db.py

9. Run z2_runAPI.py (To start API):
   python z2_runAPI.py

11. Open another terminal

13. Run z3_CLI_interface.py (To search drug info using API):
   python z3_CLI_interface.py --help
   or
   python z3_CLI_interface.py --target ENSG00000081248 --num-cases 10 --weight 0.5

