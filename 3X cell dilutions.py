from opentrons import protocol_api

metadata = {
    'protocolName': '3X Cell Dilution Protocol', 
    'author': 'Kaian Teles',
    'description': 'Serial dilution with 3X dilutions, three series per plate starting from column 1, 5, and 9'
}

requirements = {
    "robotType": "OT-2",
    "apiLevel": "2.19"
}

def add_parameters(parameters):
    parameters.add_int(
        variable_name="plate_count",
        display_name="Number of plates",
        description="Select number of plates to process (each plate = 3 transfromants)",
        default=2,
        minimum=1,
        maximum=7
    )


def run(protocol: protocol_api.ProtocolContext):
    # User-definable number of plates
    num_plates = protocol.params.plate_count
    
    # Load labware
    tiprack_300ul_1 = protocol.load_labware('opentrons_96_tiprack_300ul', '1')
    tiprack_300ul_2 = protocol.load_labware('opentrons_96_tiprack_300ul', '2')
    
    
    # Plates and reservoir
    plates = [
        protocol.load_labware('corning_96_wellplate_360ul_flat', str(i))
        for i in range(3, 3 + num_plates)
    ]
    
    media_reservoir = protocol.load_labware('axygen_1_reservoir_90ml', '11')
    
    
    p300 = protocol.load_instrument(
        'p300_multi_gen2', 
        'right', 
        tip_racks=[tiprack_300ul_2, tiprack_300ul_1]
    )

    # Step 1: Transfer media to all plates
    p300.pick_up_tip()
    for plate in plates:
        for col_idx in range(1, 12):  # Skip first column of each series
            if col_idx not in [0, 4, 8]:  # Skip starting columns
                p300.transfer(
                    133,
                    media_reservoir['A1'],
                    plate.rows()[0][col_idx],
                    new_tip='never'
                )
    p300.drop_tip()

    # Step 2: Perform 5X dilutions
    for plate in plates:
        # Process three dilution series per plate
        start_columns = [0, 4, 8]  # Starting columns A1, E1, I1
        
        for start_col in start_columns:
            p300.pick_up_tip()
            # Mix the starting material
            p300.mix(5, 100, plate.rows()[0][start_col])
            
            # Perform dilutions
            for dilution in range(3):  # Three dilutions for each series
                p300.transfer(
                    67,
                    plate.rows()[0][start_col + dilution],
                    plate.rows()[0][start_col + dilution + 1],
                    mix_after=(3, 100),
                    new_tip='never'
                )
            p300.drop_tip()

    protocol.comment("Protocol complete! 3X dilutions performed for all plates, three series per plate.")