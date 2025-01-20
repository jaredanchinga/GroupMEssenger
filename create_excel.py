import pandas as pd

def create_groupme_excel(filename='groupme.xlsx'):
    """Create Excel file with required sheets for GroupMe processing"""
    
    # Create a Excel writer object
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Create empty DataFrames for each sheet
        pd.DataFrame(columns=['Links']).to_excel(writer, sheet_name='links', index=False)
        pd.DataFrame(columns=['Links']).to_excel(writer, sheet_name='open', index=False)
        pd.DataFrame(columns=['Links']).to_excel(writer, sheet_name='closed', index=False)
        pd.DataFrame(columns=['Links']).to_excel(writer, sheet_name='question', index=False)
    
    print(f"Created {filename} with sheets: links, open, closed, question")

if __name__ == "__main__":
    create_groupme_excel() 