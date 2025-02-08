from xml.dom.minidom import parse, parseString
import xml.etree.ElementTree as ET
import os
import copy
import sys
import json
import itertools
import cairosvg
import argparse 
import pandas as pd
import numpy as np

def getLayerList(fileName,baseLayer="Layer 1",rare=False):
    '''
    getLayerList() reads an svg (xml) file
    Input:
    * fileName: svg file name
    Output:
        * tree: xml tree
        * listoflayers: list contains the names of all layers in the svg file
    '''
    tree = ET.parse(fileName)
    root = tree.getroot()
    
    listoflayers=[]
    for g in root.findall('{http://www.w3.org/2000/svg}g'):
        name = g.get('{http://www.inkscape.org/namespaces/inkscape}label')
        if name != None:
            listoflayers.append(name)
    if rare:
        listoflayers = [x for x in listoflayers if (("rare" in x) or (baseLayer in x))]
    else:
        listoflayers = [x for x in listoflayers if (not("rare" in x) or (baseLayer in x))]
        
    return tree, listoflayers

def get_rarity(lst_of_combination):
    '''
    get_rarity(lst_of_combination) calculates the rarity of a property in the NFT collection.
    Input:
        * lst_of_combination: list of the attributes combinations
    '''
    properties = []
    probability = []
    lst_all_element = []
    for i in range(len(lst_of_combination)):
        lst_all_element= lst_all_element+list(lst_of_combination[i])
        
    unique_ele = set(lst_all_element)
    
    for i in unique_ele:
        properties.append(i)
        probability.append(np.round(((lst_all_element.count(i))/len(lst_all_element))*100,decimals=2))
    
    data = pd.DataFrame({"property":properties,"probability (%)":probability})
    return data

def get_properties(feature_lst,list_of_combination):
    '''
    get_properties(feature_lst,list_of_combination) this function returns a Pandas dataframe of NFT properties.
    Input:
        * feature_lst: the list of attributes.
        * list of combinations: the attributes compinations.
    Output:
        * proprities: pandas datafarme of the NFT attributes.
    '''
    proprities = pd.DataFrame({})
    for i in range(len(feature_lst)):
        exec(feature_lst[i]+"=[]")
        for j in range(len(list_of_combination)):
             exec(feature_lst[i]+".append(list_of_combination[j][i])")
        exec("proprities[feature_lst[i]] = "+feature_lst[i])
    return proprities

def removeLayer(listoflayers,layerName):
    '''
    removeLayer(listoflayers,layerName) this function removes a layer from the layer list.
    Input:
        * listoflayers: list of layers
        * layerName: the layer name to be removed
    Output:
        * listoflayers: list of layers afetr removing one layer
    '''
    try:
        listoflayers.remove(layerName)
        return listoflayers
    except ValueError:
        print("ValeError: "+layerName +" does not exist")     

def get_layers_groups(layerslist,groups_list):
    '''
    get_layers_groups(layerslist,groups_list)
    '''
    layers_groups = []
    for g in groups_list:
        exec(g+"=[]")
        for i in layerslist:
            if g.lower() in i.lower():
                exec(g+".append(i)")
        layers_groups.append(eval(g))
    return layers_groups
def getCombinations(listOfLayers,base_lyr):
    '''
    getCombinations(listOfLayers,base_lyr) returns a list of combinations of a given attributes.
    Input:
        * ListOfLayers: list of layers
    Output:
        * base_lyr: base layer to be removed
    '''
    unique_lyrs = []
    
    if " " in base_lyr:
        base_lyr_var = base_lyr.replace(" ","_")
    else:
        base_lyr_var = base_lyr
        
    for j in listOfLayers:
        try:
            unique_lyrs.append(''.join([i for i in j if not i.isdigit()]))
        except:
            print ("Error: layer names must be letters followed up by a digit without space!")
        

    lyrs_vn = list(set(unique_lyrs))

    lyrs_vn.sort()

    for j in lyrs_vn:
        lst = [sl for sl in listOfLayers if (j in sl)]
        exec(j+" = lst")

    lyrs_vn.append(base_lyr_var)
    exec(base_lyr_var+"=[base_lyr]")
    
    combined = []

    for xx in itertools.product(*eval(",".join(lyrs_vn))):
        combined.append(xx)
    
    return combined

def genrate_collection(file_name,baselayer='Layer 1',export_folder = 'exported_svgs',nft_names=[],
                       collection_name = "",blockchain="Polygon",sale_typ="Timed Auction",
                       attribute_map=None, price=0.001, royalty=0.00001,rare=False):
    '''
    genrate_collection(file_name,baselayer='Layer 1',export_folder = 'exported_svgs',nft_names=[],
    collection_name = "",blockchain="Polygon",sale_typ="Timed Auction")
    
    This function generate NFTs collection after generating the NFT collections.
    Input:
        * file_name: The meta-svg file that contains all the layers.
        * list_of_combination: Attributes combinations.
        * baselayer: Base layer 
        * export_folder: Directory name where to export the colection.
        * nft_names: List of files names.
        * collection_name: NFT collection name
        * blockchain
        * sale_typ
        * royalty
    Output:
        * metaData: Pandas dataframe with the info of the generated NFT
        * lst_of_combination: the attributes combinations.
    '''
    
    cols = ["file_path", 
    "nft_name", 
    "external_link", 
    "description", 
    "collection", 
    "attributes",
    "levels", 
    "stats",   
    "unlockable_content", 
    "explicit_and_sensitive_content", 
    "supply", 
    "blockchain", 
    "sale_type", 
    "price",
    "method", 
    "duration", 
    "specific_buyer", 
    "quantity",
    "royalty"
           ]

    file_path = []
    nft_name = []
    external_link = []
    description = []
    collection = []
    properties = []
    levels = []
    stats = []
    unlockable_content = []
    explicit_and_sensitive_content = []
    supply = []
    blockchain_lst = []
    sale_type_lst = []
    price_lst = []
    method = []
    duration = []
    specific_buyer = []
    quantity = []
    royalty_lst = []
    
    tree, listoflayers = getLayerList(file_name)
    listoflayers_nbl = copy.copy(listoflayers)
    listoflayers_nbl.remove(baselayer)
    
    if royalty < 0 or royalty > 1:
        raise ValueError("Royalty must be between 0 and 1.")
    if price <= 0:
        raise ValueError("Price must be greater than 0.")
    
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
     
    svg_folder = os.path.join(export_folder, 'SVG')
    png_folder = os.path.join(export_folder, 'PNG')
    
    if not os.path.exists(svg_folder):
        os.makedirs(svg_folder)
    if not os.path.exists(png_folder):
        os.makedirs(png_folder)
    
    #listoflayers =  listoflayers
    list_of_combination = list(getCombinations(listoflayers_nbl,baselayer))#list(itertools.product(*listoflayers))
    unique_lyrs = []
    for j in listoflayers_nbl:
        unique_lyrs.append(''.join([i for i in j if not i.isdigit()]))
    unique_lyrs = list(np.unique(unique_lyrs))
    
    prop_df = get_properties(feature_lst=unique_lyrs,list_of_combination=list_of_combination)
    count = 0

    comb_svg = []    
    for counterl in range(len(list_of_combination)):
        comb_svg.append(list_of_combination[counterl])
        lname = ' '.join(list_of_combination[counterl]).replace(' ','_')
        james = []
        for i in range(len(listoflayers)):
            james.append(listoflayers[i][:])
        temp_tree = copy.deepcopy(tree)

        [james.remove(x) for  x in list_of_combination[counterl]] 
        temp_root = temp_tree.getroot()
        #print (lname)
        for g in temp_root.findall('{http://www.w3.org/2000/svg}g'):
            name = g.get('{http://www.inkscape.org/namespaces/inkscape}label')
            if name in james:
                temp_root.remove(g)
            else:
                style = g.get('style')
                if type(style) is str:
                    style = style.replace( 'display:none', 'display:inline' )
                    g.set('style', style)
        name = '0'*(4-len(str(count))) + str(count)
        if rare:
            name = name +'_rare'
                                                       
        temp_tree.write( os.path.join( svg_folder, name +'.svg' ) )
        cairosvg.svg2png(url=os.path.join( svg_folder, name +'.svg' ),write_to=os.path.join( png_folder, name +'.png' ),dpi=100)
        
        file_path.append(export_folder+'/'+name+'.json')
        if len(nft_names) ==0:
            nft_name.append(name)
        else:
            nft_name.append(nft_names)
            
        external_link.append(" ")
        # Translate attributes using the map
        attributes = list_of_combination[counterl]
        translated_attributes = []

        if attribute_map:
            for attr in attributes:
                # Ensure the mapping works by checking against the dictionary
                if attr in attribute_map:
                    translated_attributes.append(attribute_map[attr])
                else:
                    # Fallback to the original attribute if no match is found
                    translated_attributes.append(attr)
        else:
            # If no mapping is provided, use the original attributes
            translated_attributes = attributes

        # Generate a dynamic description
        if len(translated_attributes) >= 3:
            description_template = f"This NFT showcases {translated_attributes[0]} with {translated_attributes[1]} details and a striking {translated_attributes[2]} finish."
        elif len(translated_attributes) == 2:
            description_template = f"A stylish NFT combining {translated_attributes[0]} and {translated_attributes[1]} elements."
        elif len(translated_attributes) == 1:
            description_template = f"A unique NFT highlighting the {translated_attributes[0]} design."
        else:
            description_template = "A one-of-a-kind piece from this exclusive NFT collection."

        description.append(description_template)
            
        collection.append(collection_name)
        properties.append(prop_df.iloc[count].to_json())
        levels.append(" ")
        stats.append(" ")
        unlockable_content.append("False")
        explicit_and_sensitive_content.append("False")
        supply.append("1")
        blockchain_lst.append(blockchain)
        sale_type_lst.append(sale_typ)
        price_lst.append(price)
        method.append("price")
        duration.append(" ")
        specific_buyer.append(" ")
        quantity.append(" ")
        royalty_lst.append(royalty)
        count += 1

    metaData = pd.DataFrame({ "file_path":file_path ,  "nft_name":nft_name , 
        "external_link":external_link ,    
        "description":description ,     
        "collection":collection ,     
        "attributes":properties ,    
        "levels":levels ,     
        "stats":stats ,       
        "unlockable_content":unlockable_content ,     
        "explicit_and_sensitive_content":explicit_and_sensitive_content ,     
        "supply":supply ,     
        "blockchain":blockchain_lst ,     
        "sale_type":sale_type_lst ,     
        "price":price_lst ,    
        "method":method ,     
        "duration":duration ,     
        "specific_buyer":specific_buyer ,     
        "quantity":quantity,
        "royalty":royalty_lst})
    
    
    # Use apply function to replace attribute values in the DataFrame
    if attribute_map:
        def replace_attributes(attr_str):
            attr_dict = json.loads(attr_str)
            for key, value in attr_dict.items():
                if value in attribute_map:
                    attr_dict[key] = attribute_map[value]
            return json.dumps(attr_dict)
        
        metaData["attributes"] = metaData["attributes"].apply(replace_attributes)
    return metaData,list_of_combination

def load_attribute_map(attribute_map_path):
    """
    Load the attribute map from a JSON file.

    Args:
        attribute_map_path (str): Path to the JSON file containing the attribute mapping.

    Returns:
        dict: A dictionary with original layer names as keys and their mapped names as values.
    """
    try:
        with open(attribute_map_path, "r") as file:
            attribute_map = json.load(file)
        return attribute_map
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON file: {e}")
        return {}
    except Exception as e:
        print(f"Error loading attribute map: {e}")
        return {}
    
def calculate_rarity_with_supply(df, attribute_column="attributes", supply_column="supply"):
    """
    Calculate rarity based on human-readable attributes and supply in a globally consistent manner.

    Args:
        df (pd.DataFrame): Dataframe containing NFT metadata.
        attribute_column (str): Column containing attributes (JSON strings or dictionaries).
        supply_column (str): Column containing supply values.

    Returns:
        pd.DataFrame: Updated dataframe with a rarity dictionary for mapped attribute values
                      and globally adjusted rarity values.
    """

    # Step 1: Ensure the attributes column is in dictionary format
    def ensure_dict(value):
        if isinstance(value, str):  # If it's a string, parse it into a dictionary
            return json.loads(value.replace("'", "\""))  # Fix single quotes issue
        elif isinstance(value, dict):  # If it's already a dictionary, return as-is
            return value
        else:
            raise ValueError(f"Unexpected data type in attributes column: {type(value)}")

    df[attribute_column] = df[attribute_column].apply(ensure_dict)

    # Step 2: Ensure the supply column is numeric
    df[supply_column] = pd.to_numeric(df[supply_column], errors="coerce")

    # Step 3: Count occurrences of each attribute value (considering supply)
    attribute_counts = {}
    total_supply = df[supply_column].sum()  # Total supply across all NFTs

    for _, row in df.iterrows():
        attributes = row[attribute_column]
        supply = row[supply_column]
        for trait_type, trait_value in attributes.items():  # Example: {"eyes": "BigBlueEyes"}
            if trait_type not in attribute_counts:
                attribute_counts[trait_type] = {}
            if trait_value not in attribute_counts[trait_type]:
                attribute_counts[trait_type][trait_value] = 0
            attribute_counts[trait_type][trait_value] += supply  # Add the supply for this NFT

    # Step 4: Calculate global rarity percentages for each attribute value
    rarity_dict = {
        trait_type: {
            trait_value: round(count / total_supply, 5)  # Rarity as a percentage of total supply
            for trait_value, count in trait_values.items()
        }
        for trait_type, trait_values in attribute_counts.items()
    }

    # Step 5: Add a rarity column to map each NFT's attributes to the global rarity values
    def map_global_rarity(attributes):
        rarity_scores = {}
        for trait_type, trait_value in attributes.items():
            # Fetch the global rarity percentage
            rarity_scores[trait_value] = rarity_dict.get(trait_type, {}).get(trait_value, 0)
        return rarity_scores

    df["rarity"] = df[attribute_column].apply(map_global_rarity)

    return df
 

def main():
    """Command-line interface for NFT generation."""
    parser = argparse.ArgumentParser(description="NFT Python Generator")
    
    parser.add_argument("-m", "--meta-svg", type=str, required=True, help="Path to the meta SVG file")
    parser.add_argument("-b", "--base-layer", type=str, default="Layer 1", help="Base layer name")
    parser.add_argument("-o", "--output", type=str, default="exported_svgs", help="Output folder")
    parser.add_argument("-c", "--collection", type=str, default="My NFT Collection", help="NFT collection name")
    parser.add_argument("-p", "--price", type=float, default=0.001, help="NFT price")
    parser.add_argument("-r", "--royalty", type=float, default=0.01, help="Royalty percentage")

    args = parser.parse_args()

    if not os.path.exists(args.meta_svg):
        print("Error: Meta SVG file not found!")
        return
    
    print(f"Generating NFTs from {args.meta_svg}...")
    metadata, combinations = genrate_collection(
        file_name=args.meta_svg,
        baselayer=args.base_layer,
        export_folder=args.output,
        collection_name=args.collection,
        price=args.price,
        royalty=args.royalty
    )
    print(f"NFT Collection saved to {args.output}/")

if __name__ == "__main__":
    main()