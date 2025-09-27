import typer
import requests
from biothings_client import get_client
import matplotlib.pyplot as plt
import pandas as pd
import ast
import numpy as np
import warnings
import sys

warnings.filterwarnings("ignore")

def visualize(processed_data: dict, target: str) -> None:
    """
    This function is to visualize the number of targets and adjusted LLR by scatter plot.
    Input: processed data by dictionary format
    Output: an image file for a scatter plot 
    """

    plt.scatter(processed_data.iloc[:,0], processed_data.iloc[:,1], c='red', edgecolors='grey', alpha=0.8)
    plt.xlabel('Number of Targets')
    plt.ylabel('Adjusted LLR')
    plt.title(target)
    plt.grid(True)
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.savefig(f"{target}-{ensembl_to_hugo(target)}_scatter_targets-AE_LLR.png")


    

def convert_result_to_df(response_in_json: dict, input_in_df: pd.DataFrame) -> pd.DataFrame:
    """
    This function is to convert the retrieved data from the database to a pandas DataFrame
    Input: datasets in dictionary format
    Output: Pandas dataframe.
    """

    # Generate header information 
    header=list(input_in_df.columns)+ast.literal_eval(response_in_json['header'])
    
    contents=response_in_json['content']

    # Convert the DataFrame of extracted results to dictionary format
    input_in_dict_raw=input_in_df.to_dict(orient="index")
    input_in_dict={key: list(value.values()) for key, value in input_in_dict_raw.items()}

    # Merge the extracted results with the retrieved contents
    content_dict={} # {DrugID: content list}
    for content in contents:
        content_dict[content[1]]=input_in_dict[content[1]]+content[2].split("_|_")

    # Convert the dictionary format data to DataFrame
    df_contents=pd.DataFrame.from_dict(content_dict, orient="index")
    df_contents.columns=header
    df_contents_sorted=df_contents.sort_values(by="rankingScore")
    
    return df_contents_sorted



def extractResult(target_data: dict, target_id: str, num_cases: int, weight: float) -> None:
    """
    Extract drug data using EnsemblID and rank the minimal targets and adverse effect
    The results are displayed here, and output files are generated here.
    Input: Retrived values of target number and adjustedLLR, EnssemblID, number of cases to be displayed, and a weight value
    Output: Two CSV files for drug information of the target and one image file for scatter plot
    """

    # Convert string format of dictionary data to dictionary format
    target_dict=ast.literal_eval(target_data)

    # Convert the dictionary data to DataFrame
    df_target=pd.DataFrame.from_dict(target_dict, orient='index')
    df_target.columns=["numTargets", "adjustedLLR"]

    # Extract data that does NOT contain not determined (nd) values
    df_no_nd_target=df_target[df_target.iloc[:,1] !="nd"]

    # Calculate ranking score by distance between (0,0) and the coordinate of each data.
    df_no_nd_target["rankingScore"]=(df_no_nd_target["numTargets"]*(1-weight))**2+(df_no_nd_target["adjustedLLR"]*weight)**2
    df_no_nd_target["rankingScore"] = list(map(lambda x: np.sqrt(x), np.array(df_no_nd_target["rankingScore"].values)))
    df_no_nd_target_sorted=df_no_nd_target.sort_values(by="rankingScore")

    #<------- print sorted drugs----------->
    
    print("_"*106)
    print(f"\n<<<<   The followings are sorted drug list based on the weight {round(1-weight,1)} for targets and {weight} for adjusted LLR of adverse effect   >>>>\n\n")    
    print(df_no_nd_target_sorted)
    print("="*106)


    # Extract data that contains nd values
    df_nd_target=df_target[df_target.iloc[:,1] =="nd"]

    # Replace nd to 0 to calculate the ranking score
    df_nd_to_zero_target=df_nd_target.replace("nd",0, inplace=False)

    # Calculate ranking score
    df_nd_target["rankingScore"]=(df_nd_to_zero_target["numTargets"]*(1-weight))**2+(df_nd_to_zero_target["adjustedLLR"]*weight)**2
    df_nd_target["rankingScore"] = list(map(lambda x: np.sqrt(x), np.array(df_nd_target["rankingScore"].values)))
    df_nd_target_sorted=df_nd_target.sort_values(by="rankingScore")
    
    #<------- print sorted drugs----------->
    print("_"*106)
    print(f"\n<<<<   The followings are sorted drug list that has missing info in target number or adverse effect   >>>>")    
    print(f"(The ranking score was calculated by putting nd as 0)\n\n")    
    print(df_nd_target_sorted)
    print("="*106)
    
    # Generate a scatter plot with the data that has no 'nd'
    visualize(df_no_nd_target, target_id) ### =======================> visualize()

    # Retrieve drug information that does not contain nd in data from the database
    target="__".join(df_no_nd_target_sorted.index.values)

    response = requests.get(f"http://localhost:8000/drugs/{target}")
    if response.ok:
        extracted_results=response.json()
    else:
        typer.echo("\n### Warning: The Query drug list is not in the Database ###\n")
        sys.exit()

    # Convert the retrieved drug information to a DataFrame
    df_no_nd_target_extracted_drugs=convert_result_to_df(extracted_results, df_no_nd_target_sorted) ### =======================> convert_result_to_df()
    # Save the DataFrame as a csv file.
    df_no_nd_target_extracted_drugs.to_csv(f"{target_id}-{ensembl_to_hugo(target_id)}_Weight-{weight}_drug_info_main.csv", index=True)

    # Adjust the num_cases to be displayed if the number of data is smaller.
    if num_cases>len(list(df_no_nd_target_extracted_drugs.index.values)):
        num_cases=len(list(df_no_nd_target_extracted_drugs.index.values))

    # Display brief result in the terminal
    df_no_nd_target_extracted_drugs_row_parsed=df_no_nd_target_extracted_drugs.iloc[0:num_cases]
    print("_"*106)
    print(f"\n<<<<   Brief information of the top {num_cases} drug(s)   >>>>\n\n")    
    print(df_no_nd_target_extracted_drugs_row_parsed[["numTargets","adjustedLLR","rankingScore","name","maximumClinicalTrialPhase","isApproved","tradeNames","description"]])
    print("\n\n *** Please refer to the output files in this folder for detailed information. ***\n")
    print("="*106)
    print("\n\n")


    # Retrieve drug information that contains nd in data from the database    
    target="__".join(df_nd_target_sorted.index.values)

    response = requests.get(f"http://localhost:8000/drugs/{target}")
    if response.ok:
        extracted_results=response.json()
    else:
        typer.echo("\n### Warning: The Query drug list is not in the Database ###\n")
        sys.exit()

    # Convert the retrieved drug information to a DataFrame
    df_nd_target_extracted_drugs=convert_result_to_df(extracted_results, df_nd_target_sorted) ### =======================> convert_result_to_df()
    # Save the DataFrame as a csv file.
    df_nd_target_extracted_drugs.to_csv(f"{target_id}-{ensembl_to_hugo(target_id)}_Weight-{weight}_drug_info_missing.csv", index=True)




def ensembl_to_hugo(ensembl_id: str) -> str:
    """
    Fundtion to convert EnssemblID to Hugo format
    Input: EnssemblID
    Output: Hugo
    """
    convert = get_client("gene")
    result = convert.getgene(ensembl_id)
    # print(result)
    return result.get("symbol")


    
def processing(search_result: dict, target: str, num_cases: int, weight: float) -> None:
    """
    To initialize the search process
    """
    print("\n\n")
    print("_"*106)
    print(f"\nInput EnsemblID: {search_result['target']}  ===>  Hugo gene symbol: {ensembl_to_hugo(search_result['target'])}")
    values=search_result['value']

    extractResult(values, target, num_cases, weight)


    

app = typer.Typer()


@app.command()
def search(
    target: str = typer.Option(None, help="EnsemblID of the target (ex: ENSG00000081248)"),
    num_cases: int = typer.Option(10, help="Number of most specific and safe drugs to be shown. Default is 10."),
    weight: float = typer.Option(0.5, help="Float between 0 to 1. 0 is only for number of targets and 1 is only for degree of Adverse Effect. Default is 0.5")
):
    if "CHEMBL" not in target:
        response = requests.get(f"http://localhost:8000/targets/{target}")
        if response.ok:
            processing(response.json(), target, num_cases, weight)
        else:
            typer.echo("\n### Warning: The Query EnsemblID is not in the Database ###\n")
    else:
        response = requests.get(f"http://localhost:8000/drugs/{target}")
        if response.ok:
            return response.json()
        else:
            typer.echo("\n### Warning: The Query drug list is not in the Database ###\n")
            

if __name__ == "__main__":
    app()
    
