"""
Helper file for the NFT Generator Tool package.

This file provides information about the package, its functionality, and usage examples.
"""

def show_overview():
    """
    Displays an overview of the NFT Generator Tool package.

    Returns:
        str: A string containing an overview of the package.
    """
    overview = """
    NFT Generator Tool - Overview

    This Python package allows you to:
    1. Generate NFT collections from meta-SVG files.
    2. Calculate rarity for NFT attributes.
    3. Manage metadata efficiently, including export to CSV.
    4. Support rare NFTs with custom layers.
    5. Adjust NFT prices based on rarity.

    For more information, use the other help functions in this module.
    """
    return overview


def show_usage_examples():
    """
    Displays usage examples for the NFT Generator Tool package.

    Returns:
        str: A string containing usage examples.
    """
    examples = """
    Usage Examples:

    1. Generate an NFT collection:
        ```python
        from NFT_Python_generator.nft_gen_tool import genrate_collection
        
        df, combinations = genrate_collection(
            file_name='meta_file.svg',
            baselayer='Layer 1',
            export_folder='output_folder',
            collection_name='My NFT Collection',
            blockchain='Polygon',
            price=0.05,
            royalty=0.01
        )
        ```

    2. Calculate rarity for NFTs with supply:
        ```python
        from NFT_Python_generator.nft_gen_tool import calculate_rarity_with_supply

        df = calculate_rarity_with_supply(
            df, attribute_column="attributes", supply_column="supply"
        )
        ```

    3. Load an attribute map:
        ```python
        from NFT_Python_generator.nft_gen_tool import load_attribute_map

        attribute_map = load_attribute_map("attribute_map.json")
        ```

    4. Generate supply values using Gaussian distribution:
        ```python
        from NFT_Python_generator.nft_gen_tool import generate_supply_in_dataframe

        df = generate_supply_in_dataframe(df, mean=20, std_dev=5, min_supply=1)
        ```
    """
    return examples


def show_function_details():
    """
    Displays detailed information about each function in the package.

    Returns:
        str: A string containing details about the functions.
    """
    function_details = """
    Function Details:

    1. genrate_collection:
        - Description: Generates an NFT collection and saves metadata.
        - Parameters:
            * file_name (str): Path to the meta-SVG file.
            * baselayer (str): Name of the base layer in the SVG.
            * export_folder (str): Folder where the generated files will be saved.
            * collection_name (str): Name of the NFT collection.
            * blockchain (str): Blockchain to be used (e.g., 'Polygon').
            * price (float): Base price for the NFTs.
            * royalty (float): Royalty percentage for the NFTs.
        - Returns:
            * DataFrame: A DataFrame containing metadata for the NFTs.
            * list: A list of attribute combinations.

    2. calculate_rarity_with_supply:
        - Description: Calculates rarity for NFT attributes, considering supply.
        - Parameters:
            * df (DataFrame): DataFrame containing NFT metadata.
            * attribute_column (str): Column containing attributes.
            * supply_column (str): Column containing supply values.
        - Returns:
            * DataFrame: Updated DataFrame with rarity values.

    3. load_attribute_map:
        - Description: Loads an attribute map from a JSON file.
        - Parameters:
            * attribute_map_path (str): Path to the JSON file.
        - Returns:
            * dict: A dictionary mapping original layer names to mapped names.

    4. generate_supply_in_dataframe:
        - Description: Generates supply values for NFTs using a Gaussian distribution.
        - Parameters:
            * df (DataFrame): DataFrame containing NFT metadata.
            * mean (float): Mean of the distribution.
            * std_dev (float): Standard deviation of the distribution.
            * min_supply (int): Minimum supply for any NFT.
        - Returns:
            * DataFrame: Updated DataFrame with supply values.

    """
    return function_details


def print_help():
    """
    Prints all available help content, including an overview, usage examples, and function details.
    """
    print(show_overview())
    print(show_usage_examples())
    print(show_function_details())


if __name__ == "__main__":
    # Example: Print all help content
    print_help()
