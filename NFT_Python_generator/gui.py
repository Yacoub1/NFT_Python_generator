import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import pandas as pd
import numpy as np
from nft_gen_tool import *

blockchain_cryptocurrency_map = {
    "Ethereum": ["ETH"],
    "Polygon": ["MATIC"],
    "Binance Smart Chain": ["BNB"],
    "Solana": ["SOL"],
    "Avalanche": ["AVAX"],
    "Tezos": ["XTZ"],
    "Cardano": ["ADA"],
    "Flow": ["FLOW"],
    "Algorand": ["ALGO"],
    "Ripple (XRP Ledger)": ["XRP"],
    "Stellar": ["XLM"],
    "Tron": ["TRX"],
    "WAX": ["WAXP"],
    "Hedera": ["HBAR"]
}

cryptocurrencies = [
    "Ethereum",
    "Polygon",
    "Binance Smart Chain",
    "Solana",
    "Avalanche",
    "Tezos",
    "Cardano",
    "Flow",
    "Algorand",
    "Ripple (XRP Ledger)",
    "Stellar",
    "Tron",
    "WAX",
    "Hedera"
]

def adjust_prices_based_on_rarity():
    """
    Adjust the price column in the global DataFrame based on rarity.
    The highest rarity value from the rarity dictionary is used to determine the new price.
    """
    export_folder = export_folder_entry.get()
    export_folder = export_folder_entry.get()
    rare_meta_path = rare_svg_entry.get() if rare_var.get() else None
    
    df = pd.read_csv(export_folder+"/nft_collection_metadata.csv")
    
    if rare_meta_path:
        rare_df = df[df['rare NFT']==1]
        df = df[df['rare NFT']==0]
    try:
        df['rarity'] = df['rarity'].apply(
            lambda x: json.loads(x.replace("'", '"')) if isinstance(x, str) else x
        )
        # Extract the inverted rarity value for each NFT (average of inverted rarity scores)
        df['inverted_rarity'] = df['rarity'].apply(
            lambda rarity: 1/min(rarity.values()) if isinstance(rarity, dict) and len(rarity) > 0 else 0
        )

        # Ensure all relevant columns are numeric
        df['inverted_rarity'] = pd.to_numeric(df['inverted_rarity'], errors='coerce')
        df['price'] = pd.to_numeric(df['price'], errors='coerce')

        # Get the maximum price in the current DataFrame
        max_price = df['price'].max()

        # Adjust prices based on inverted rarity (scaling by rarity relative to the max)
        df['price'] = (df['inverted_rarity'] / df['inverted_rarity'].max()) * max_price
        # Drop the intermediate inverted_rarity column
        df.drop(columns=['inverted_rarity'], inplace=True)
        
        if rare_meta_path:
            df = pd.concat([df, rare_df], ignore_index=True)
            df.drop(columns=['rare NFT'], inplace=True)
        
        df.to_csv(os.path.join(export_folder, "nft_collection_metadata_rarity_price_.csv"), index=False,float_format="%.10f" )
        
        messagebox.showinfo("Success", "Prices adjusted successfully based on inverted rarity!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while adjusting prices: {str(e)}")


def toggle_rare_fields():
    """Enable or disable rare-related fields based on the checkbox."""
    if rare_var.get():
        rare_svg_entry.config(state="normal")
        rare_svg_browse_button.config(state="normal")
        rare_price_entry.config(state="normal")
        rare_royalty_entry.config(state="normal")
    else:
        rare_svg_entry.config(state="disabled")
        rare_svg_browse_button.config(state="disabled")
        rare_price_entry.config(state="disabled")
        rare_royalty_entry.config(state="disabled")
        
def toggle_supply_fields():
    """Enable or disable supply-related fields based on the checkbox."""
    if natural_dis_var.get():
        supply_mean_entry.config(state="normal")
        supply_std_entry.config(state="normal")
        supply_entry.config(state="disable")
    else:
        supply_mean_entry.config(state="disabled")
        supply_std_entry.config(state="disabled")
        supply_entry.config(state="normal")

def toggle_attributes_mapping_fields():
    """Enable or disable attributes-mapping-related fields based on the checkbox."""
    if attributes_mapping_var.get():
        attributes_map_entry.config(state="normal")
        attributes_map_browes_btn.config(state="normal")
    else:
        attributes_map_entry.config(state="disabled")
        attributes_map_browes_btn.config(state="disabled")

def generate_supply_in_dataframe(df, mean=20, std_dev=5, min_supply=1):
    """
    Generate supply values for NFTs using a Gaussian distribution and update them in the DataFrame.

    Args:
        df (pd.DataFrame): The metadata DataFrame containing the NFT collection.
        mean (float): Mean value for the Gaussian distribution.
        std_dev (float): Standard deviation for the Gaussian distribution.
        min_supply (int): Minimum supply for any NFT.

    Returns:
        pd.DataFrame: Updated DataFrame with modified supply values.
    """
    # Generate supplies based on Gaussian distribution
    nft_count = len(df)
    supplies = np.random.normal(mean, std_dev, nft_count)
    
    # Ensure that supply values are above the minimum supply
    supplies = np.clip(supplies, min_supply, None).astype(int)
    
    # Update the 'supply' column in the DataFrame
    df["supply"] = supplies
    
    return df

def open_help_window():
    """Open a new window with instructions on how to use the GUI."""
    help_window = tk.Toplevel(root)  # Create a new window
    help_window.title("Help")
    help_window.geometry("600x400")
    help_window.configure(bg="white")  # Set the background color to white
    
    # Instructions text
    instructions = """
    Welcome to the NFT Generator Tool!
    
    Instructions:
    1. Meta SVG File:
       - Browse and select the meta SVG file that contains all the layers.
    
    2. Base Layer:
       - Specify the name of the base layer in the SVG file.
    
    3. Export Folder:
       - Choose the folder where the generated NFTs and metadata will be saved.
    
    4. Collection Details:
       - Specify the collection name, cryptocurrency, and sale type.
       - Set the collection price and royalty percentage.

    5. Rarity and Supply:
       - You can use the "Create Supply (Natural Distribution)" option to generate
         supply values based on a Gaussian distribution (mean and std. deviation).
       - If unchecked, you can manually set a fixed supply value.

    6. Rare SVG:
       - (Optional) If you have a rare SVG file, check the box, browse for the file, and set its price. 
       - Make sure that the layer names of the rare NFT meta file match the corresponding layer names 
         in the normal meta NFT file if they are identical.
       - For new layers in the rare NFT, ensure that their names follow the sequence from the original meta NFT.
         Example:
         - If the original meta NFT has "mouth1", "mouth2", ..., "mouth5", and you add a new mouth layer in 
           the rare NFT, it should be named "mouth6", "mouth7", etc., to maintain consistency.

    7. Attributes Mapping:
       - If you have a JSON file for mapping attributes, enable the option,
         browse for the file, and it will be applied during generation.

    8. Generate NFTs:
       - After filling in all the fields, click the "Generate NFTs" button to
         create the collection.

    9. Adjust Prices:
       - Use the "Adjust Prices" button (if available) to modify prices
         based on rarity.

    For additional support, visit the GitHub Repo.
    """
    
    # Add a Text widget to display the instructions
    text_widget = tk.Text(help_window, wrap="word", bg="white", fg="black", font=("Arial", 12))
    text_widget.insert("1.0", instructions)
    text_widget.config(state="disabled")  # Make the text widget read-only
    text_widget.pack(fill="both", expand=True, padx=10, pady=10)

def generate_nft_collection():
    """Generate the NFT collection based on the user inputs."""
    # Get input values from the GUI
    meta_svg_path = meta_svg_entry.get()
    base_layer = base_layer_entry.get()
    export_folder = export_folder_entry.get()
    collection_price = float(price_entry.get()) if price_entry.get() else 0.001
    rare_meta_path = rare_svg_entry.get() if rare_var.get() else None
    rare_price = float(rare_price_entry.get()) if rare_price_entry.get() and rare_var.get() else 0.1
    rare_royalty = float(rare_royalty_entry.get()) if rare_royalty_entry.get() and rare_var.get() else 0.01
    collection_name = collection_name_entry.get()
    cryptocurrency = cryptocurrency_combobox.get()
    sale_typ = sale_type_combobox.get()
    royalty = float(royalty_entry.get())
    supply_value = int(supply_var.get()) if supply_var.get().isdigit() else 1
    mean = float(supply_mean_entry.get()) if natural_dis_var.get() else None
    std_dev = float(supply_std_entry.get()) if natural_dis_var.get() else None
    attribute_map_dict = load_attribute_map(attributes_map_entry.get()) if attributes_mapping_var.get() else None
   
    
    if not os.path.exists(meta_svg_path):
        messagebox.showerror("Error", "Meta SVG file does not exist.")
        return

    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    try:
        # Call the main function to generate NFT collection
        df, combinations = genrate_collection(
            file_name=meta_svg_path,
            baselayer=base_layer,
            export_folder=export_folder,
            collection_name=collection_name,
            blockchain=blockchain_cryptocurrency_map.get(cryptocurrency, []),
            sale_typ=sale_typ,
            price=collection_price,
            royalty=royalty,
            attribute_map=attribute_map_dict
        )
        

        if rare_meta_path:
            # If rare checkbox is ticked, generate rare NFTs
            rare_df, rare_combinations = genrate_collection(
                file_name=rare_meta_path,
                baselayer=base_layer,
                export_folder=export_folder,
                collection_name=collection_name,
                blockchain=blockchain_cryptocurrency_map.get(cryptocurrency, []),
                sale_typ=sale_typ,
                price=rare_price,
                royalty=rare_royalty,
                attribute_map=attribute_map_dict,
                rare=True
                
            )
            
            

        # Add supply to the data
        if natural_dis_var.get():
            df = generate_supply_in_dataframe(df, mean=mean, std_dev=std_dev, min_supply=1)
        else:
            df['supply'] = supply_value * np.ones(len(df))
        
        if rare_meta_path:
            df["rare NFT"] = np.zeros(len(df))
            rare_df["rare NFT"] = np.ones(len(rare_df))
            
            df = pd.concat([df, rare_df], ignore_index=True)
    
        # Calculate rarity and save to file
        df = calculate_rarity_with_supply(df, attribute_column="attributes")
        df.to_csv(os.path.join(export_folder, "nft_collection_metadata.csv"), index=False,float_format="%.10f" )
        # activate price adjustment btn
        adjust_price_button.config(state="normal")
                                   
        messagebox.showinfo("Success", "NFT collection generated successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Initialize the GUI window
root = tk.Tk()
root.title("NFT Generator Tool")


# Add a logo to the tool
try:
    logo_image = Image.open("tool_logo.png")  
    logo_image = logo_image.resize((200, 100), Image.ANTIALIAS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    tk.Label(root, image=logo_photo).grid(row=0, column=0, columnspan=3, pady=10)
except FileNotFoundError:
    tk.Label(root, text="NFT Generator Tool", font=("Arial", 20, "bold")).grid(row=0, column=0, columnspan=3, pady=10)

# Input fields for meta SVG file
tk.Label(root, text="Meta SVG File Path:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
meta_svg_entry = tk.Entry(root, width=50)
meta_svg_entry.grid(row=1, column=1, padx=10, pady=5)

def browse_meta_svg():
    meta_svg_path = filedialog.askopenfilename(filetypes=[("SVG Files", "*.svg")])
    meta_svg_entry.insert(0, meta_svg_path)

tk.Button(root, text="Browse", command=browse_meta_svg).grid(row=1, column=2, padx=10, pady=5)

# Input fields for base layer
tk.Label(root, text="Base Layer Name:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
base_layer_entry = tk.Entry(root, width=50)
base_layer_entry.grid(row=2, column=1, padx=10, pady=5)

# Input fields for export folder
tk.Label(root, text="Export Folder:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
export_folder_entry = tk.Entry(root, width=50)
export_folder_entry.grid(row=3, column=1, padx=10, pady=5)

def browse_export_folder():
    export_folder_path = filedialog.askdirectory()
    export_folder_entry.insert(0, export_folder_path)

tk.Button(root, text="Browse", command=browse_export_folder).grid(row=3, column=2, padx=10, pady=5)

# Input fields for collection price
tk.Label(root, text="Collection Price:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
price_entry = tk.Entry(root, width=15)
price_entry.grid(row=4, column=1, padx=10, pady=5)

# Input fields for collection royalty
tk.Label(root, text="Collection royalty:").grid(row=4, column=2, padx=10, pady=5, sticky="w")
royalty_entry = tk.Entry(root, width=15)
royalty_entry.grid(row=4, column=3, padx=10, pady=5)

# Input fields for collection name
tk.Label(root, text="Collection Name:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
collection_name_entry = tk.Entry(root, width=50)
collection_name_entry.grid(row=5, column=1, padx=10, pady=5)

# Dropdown menu for cryptocurrency

tk.Label(root, text="Cryptocurrency:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
cryptocurrency_combobox = ttk.Combobox(root, values=cryptocurrencies, state="readonly")
cryptocurrency_combobox.set("Ethereum")
cryptocurrency_combobox.grid(row=6, column=1, padx=10, pady=5)

# Checkbox for rare SVG file
rare_var = tk.IntVar()
tk.Checkbutton(root, text="Include Rare SVG", variable=rare_var, command=toggle_rare_fields).grid(row=7, column=0, padx=10, pady=5, sticky="w")

# Input fields for rare SVG file
tk.Label(root, text="Rare SVG File Path:").grid(row=8, column=0, padx=10, pady=5, sticky="w")
rare_svg_entry = tk.Entry(root, width=50, state="disabled")
rare_svg_entry.grid(row=8, column=1, padx=10, pady=5)

def browse_rare_svg():
    rare_svg_path = filedialog.askopenfilename(filetypes=[("SVG Files", "*.svg")])
    rare_svg_entry.insert(0, rare_svg_path)

rare_svg_browse_button = tk.Button(root, text="Browse", command=browse_rare_svg, state="disabled")
rare_svg_browse_button.grid(row=8, column=2, padx=10, pady=5)

# Input fields for rare NFT price
tk.Label(root, text="Rare NFT Price:").grid(row=9, column=0, padx=10, pady=5, sticky="w")
rare_price_entry = tk.Entry(root, width=20, state="disabled")
rare_price_entry.grid(row=9, column=1, padx=10, pady=5)

# Input fields for rare NFTs royalty
tk.Label(root, text="Rare NFT royalty:").grid(row=9, column=2, padx=10, pady=5, sticky="w")
rare_royalty_entry = tk.Entry(root, width=15,state="disable")
rare_royalty_entry.grid(row=9, column=3, padx=10, pady=5)


# Add a dropdown menu for Sale Type
sale_types = ["Fixed Price", "Auction", "Timed Auction"]
tk.Label(root, text="Sale Type:").grid(row=10, column=0, padx=10, pady=5, sticky="w")
sale_type_combobox = ttk.Combobox(root, values=sale_types, state="readonly")
sale_type_combobox.set("Fixed Price")
sale_type_combobox.grid(row=10, column=1, padx=10, pady=5)

#Checkbox for natural distribution for supply
natural_dis_var = tk.IntVar()
tk.Checkbutton(root, text="Create Supply (Natural Distribution)", variable=natural_dis_var, command=toggle_supply_fields).grid(row=11, column=0, padx=10, pady=5, sticky="w")

# Input fields for mean and standard deviation
tk.Label(root, text="Mean:").grid(row=12, column=0, padx=10, pady=5, sticky="w")
supply_mean_entry = tk.Entry(root, width=15, state="disabled")
supply_mean_entry.grid(row=12, column=1, padx=10, pady=5)

tk.Label(root, text="Std Dev:").grid(row=12, column=2, padx=10, pady=5, sticky="w")
supply_std_entry = tk.Entry(root, width=15, state="disabled")
supply_std_entry.grid(row=12, column=3, padx=10, pady=5)

# Input fields for manual supply
tk.Label(root, text="Supply:").grid(row=13, column=0, padx=10, pady=5, sticky="w")
supply_var = tk.StringVar(value="1")  # Default value is 1
supply_entry = tk.Entry(root, textvariable=supply_var, width=15)
supply_entry.grid(row=13, column=1, padx=10, pady=5)

#Checkbox for attributes mapping
attributes_mapping_var = tk.IntVar()
tk.Checkbutton(root, text="Attributes mapping", variable=attributes_mapping_var, command=toggle_attributes_mapping_fields).grid(row=14, column=0, padx=10, pady=5, sticky="w")

def browse_attribute_map():
    """Browse and select an attribute map json file."""
    attribute_map_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    attributes_map_entry.insert(0, attribute_map_path)

# Input fields for export folder
tk.Label(root, text="Attributes map:").grid(row=15, column=0, padx=10, pady=5, sticky="w")
attributes_map_entry = tk.Entry(root, width=50, state="disabled")
attributes_map_entry.grid(row=15, column=1, padx=10, pady=5)

# Button to browse for attribute mappint text file
attributes_map_browes_btn = tk.Button(root, text="Browse", command=browse_attribute_map, state="disabled")
attributes_map_browes_btn.grid(row=15, column=2, padx=10, pady=5)

# Button to generate NFTs
tk.Button(root, text="Generate NFTs", command=generate_nft_collection, bg="green", fg="white").grid(row=20, column=1, padx=10, pady=20)

# Button to adjust NFTs prices based on rarity
adjust_price_button = tk.Button(
    root, text="Adjust Prices Based on Rarity", 
    command=adjust_prices_based_on_rarity, 
    state="disabled",  # Disabled initially
    bg="blue", fg="white"
)
adjust_price_button.grid(row=21, column=1, padx=10, pady=20)

# Add the Help button to the main window
help_button = tk.Button(root, text="Help!", command=open_help_window, bg="blue", fg="white", font=("Arial", 12, "bold"))
help_button.grid(row=1, column=3, padx=10, pady=20)
                                                                                  
root.geometry("1000x750")
root.resizable(False,False)
# Run the GUI loop
root.mainloop()
