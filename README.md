# Python NFT Generator Tool

![Python NFT Generator Logo](/NFT_Python_generator/figures/tool_logo.png)

The Python NFT Generator Tool is an intuitive GUI-based Python application for generating NFT collections from SVG files. It supports rarity calculations, natural supply distribution, and easy attribute mapping to create diverse and unique NFT collections.

## Features

- **Meta SVG Handling:** Create NFT collections from SVG files with layers.
- **Rarity Integration:** Calculate rarity percentages and use them to adjust NFT prices.
- **Supply Distribution:** Use natural distribution (Gaussian) to create supplies for your NFTs or set a fixed supply.
- **Attributes Mapping:** Map layer attributes to human-readable or custom-defined names using a JSON file.
- **Rare Attributes:** Add rare SVGs to your collection, keeping layer consistency with the base collection.
- **Cross-Blockchain Support:** Works with multiple blockchains like Ethereum, Polygon, and Solana.
- **Easy to Use:** GUI-based application with straightforward workflows.

## GUI Overview

![NFT Generator Tool GUI](/NFT_Python_generator/figures/nft_gen_gui.png)

The GUI provides all necessary fields for generating NFTs, including meta SVG file paths, export folders, rarity calculations, and supply adjustments.

## Example Outputs

### Crazy Candles Collection
![Crazy Candles Example GIF](/NFT_Python_generator/figures/squared_face_collection.gif)

### Square Face Collection
![Square Face Example GIF](/NFT_Python_generator/figures/crazycandles_collection.gif)

## Installation

### Requirements

- Python 3.7 or higher
- Required libraries listed in `requirements.txt`

### Installation Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repository-url/NFT_Python_Generator.git
   cd NFT_Python_Generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install the package:
   ```bash
   python setup.py install
   ```

4. Run the GUI:
   ```bash
   python -m NFT_Python_Generator.nft_gen_tool
   ```

## Usage

## Usage

1. **Launch the GUI application.**
2. **Fill in the required fields**:
   - **Meta SVG File Path**: The meta SVG file must contain all possible combinations of layers.
   - **Base Layer Name**: Specify the base layer used in the meta SVG.
   - **Export Folder**: Choose the folder where the NFTs and metadata will be saved.
   - **Collection Details**: Provide the collection price, royalty, name, cryptocurrency, and sale type.
3. **Important Notes**:
   - **Layer Naming Convention**:
     - Layers in the meta SVG must follow a naming convention: `XXX#`, where `XXX` is a name (letters only) and `#` is a number (digits only).
     - There must be **no spaces or underscores** in layer names.
   - **Rare Meta SVGs**:
     - If using a rare meta SVG file, the layers in the rare file **must match the original layer names** for existing layers.
     - **New layers in the rare SVG must follow continuous numbering**. For example, if the original SVG contains `mouth1` to `mouth5`, a new layer in the rare SVG must begin with `mouth6` and continue sequentially. **Failure to follow this convention will result in errors.**
4. (Optional) Add rare SVGs or attributes mapping for custom rarity settings.
5. **Generate NFTs**:
   - Click **Generate NFTs** to create the collection.
   - Once completed, you can further adjust prices using rarity with the **Adjust Prices Based on Rarity** button.

## Contributing

If you want to contribute to this project, feel free to fork this repository, make changes, and submit a pull request.

## Support

For support, create an issue in this repository.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## 💡 Support This Project  
If you are using this tool for commercial purposes and would like to support its development,  
consider contributing here: [PayPal Donation](https://www.paypal.com/donate/?hosted_button_id=MQSW5283NCXCJ).