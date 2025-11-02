from opentrons import protocol_api

metadata = {
    'protocolName': 'Cell plating on Starch',
    'author': 'Kaian Teles',
    'description': 'Plates up to 6 transformants on starch plates'
}

requirements = {
    "robotType": "OT-2",
    "apiLevel": "2.19"
}

def add_parameters(parameters):

    parameters.add_int(
        variable_name="plate_count",
        display_name="# of Plates (3 or 6 plates)",
        description="Use multiples of 3 — round your actual number up to the next multiple of 3",
        default=6,
        minimum=3,
        maximum=6
    )

    parameters.add_int(
        variable_name="dilution_plate_count",
        display_name="# of Dilution Plates",
        description="How many source plates with diluted cells? (1–2) positions 3 and 4",
        default=2,
        minimum=1,
        maximum=2
    )


    parameters.add_float(
        variable_name="Z_offset_plate_1",
        display_name="Plate in position 5",
        description="Insert plate weight in grams",
        default=50,
        minimum=0,
        maximum=100
    )

    parameters.add_float(
        variable_name="Z_offset_plate_2",
        display_name="Plate in position 6",
        description="Insert plate weight in grams",
        default=50,
        minimum=0,
        maximum=100
    )

    parameters.add_float(
        variable_name="Z_offset_plate_3",
        display_name="Plate in position 7",
        description="Insert plate weight in grams",
        default=50,
        minimum=0,
        maximum=100
    )

    parameters.add_float(
        variable_name="Z_offset_plate_4",
        display_name="Plate in position 8",
        description="Insert plate weight in grams",
        default=50,
        minimum=0,
        maximum=100
    )

    parameters.add_float(
        variable_name="Z_offset_plate_5",
        display_name="Plate in position 9",
        description="Insert plate weight in grams",
        default=50,
        minimum=0,
        maximum=100
    )

    parameters.add_float(
        variable_name="Z_offset_plate_6",
        display_name="Plate in position 10",
        description="Insert plate weight in grams",
        default=50,
        minimum=0,
        maximum=100
    )

def get_plate_slot_list(num_plates):
    """Returns a list of slot strings based on how many plates the user selected."""
    slot_order = ['5', '6', '7', '8', '9', '10']
    return slot_order[:num_plates]

def run(protocol: protocol_api.ProtocolContext):


    PLATE1 = protocol.params.Z_offset_plate_1
    PLATE2 = protocol.params.Z_offset_plate_2
    PLATE3 = protocol.params.Z_offset_plate_3
    PLATE4 = protocol.params.Z_offset_plate_4
    PLATE5 = protocol.params.Z_offset_plate_5
    PLATE6 = protocol.params.Z_offset_plate_6

    GellanGumVolume=10567.2*0.001028

    PLATEADJUSTED1 = PLATE1 / (GellanGumVolume)
    PLATEADJUSTED2 = PLATE2 / (GellanGumVolume)
    PLATEADJUSTED3 = PLATE3 / (GellanGumVolume)
    PLATEADJUSTED4 = PLATE4 / (GellanGumVolume)
    PLATEADJUSTED5 = PLATE5 / (GellanGumVolume)
    PLATEADJUSTED6 = PLATE6 / (GellanGumVolume)
    

    NUM_DILUTION_PLATES = protocol.params.dilution_plate_count

    plate_slots = get_plate_slot_list(protocol.params.plate_count)
    # Load labware
    tip_racks_20 = [
        protocol.load_labware('opentrons_96_filtertiprack_20ul', slot)
        for slot in ['1', '2'] 
    ]
    tip_rack_300 = protocol.load_labware('opentrons_96_tiprack_300ul', '11')
    
    # Load source plates (diluted cells)
    source_plates = []
    for i in range(NUM_DILUTION_PLATES):
        source_plates.append(protocol.load_labware('corning_96_wellplate_360ul_flat', str(3+i)))
    
    # Load destination plates (starch plates)
    dest_plates = [
        protocol.load_labware('corning_96_wellplate_360ul_flat', slot) 
        for slot in plate_slots
    ]

    # Load pipettes
    p20_multi = protocol.load_instrument('p20_multi_gen2', 'left', tip_racks=tip_racks_20)
    p300_multi = protocol.load_instrument('p300_multi_gen2', 'right', tip_racks=[tip_rack_300])

    # Set default speeds
    p20_multi.default_speed = 400
    p300_multi.default_speed = 400

    # Define z-offsets for each destination plate
    plate_z_offsets = [
    PLATEADJUSTED1,
    PLATEADJUSTED2,
    PLATEADJUSTED3,
    PLATEADJUSTED4,
    PLATEADJUSTED5,
    PLATEADJUSTED6,
    ]

    # Define source column z-offsets
    source_z_offsets = {
        3: 3.3,  # A4
        2: 2.1,  # A3
        1: 2.1,  # A2
        0: 0.7,  # A1
        7: 3.3,  # A8
        6: 2.1,  # A7
        5: 2.1,  # A6
        4: 0.7,  # A5
        11: 3.3, # A12
        10: 2.1, # A11
        9: 2.1,  # A10
        8: 0.7   # A9
    }

    def batch_mix_columns(source_plate, columns):
        """Mix a batch of 4 columns with P300"""
        p300_multi.pick_up_tip()
        for col in reversed(columns):
            source_well = source_plate.columns()[col][0]
            p300_multi.mix(4, 60, source_well.bottom(z=1), rate=2.0)
        p300_multi.drop_tip()

    def transfer_to_columns(source_well, source_col, dest_plate, dest_cols, z_offset):
        """Helper function to transfer to multiple destination columns"""
        p20_multi.pick_up_tip()
        for dest_col in dest_cols:
            dest_well = dest_plate.columns()[dest_col][0]
            p20_multi.aspirate(10, source_well.bottom(z=source_z_offsets[source_col]), rate=2.0)
            p20_multi.dispense(10, dest_well.bottom(z=z_offset), rate=2.0)
        p20_multi.drop_tip()

    def process_four_columns(source_plate, start_col, dest_plate, z_offset):
        """Process a group of 4 columns from source to destination plate"""
        # First mix all 4 columns in batch with P300
        batch_mix_columns(source_plate, range(start_col-3, start_col+1))
        
        # Then do the transfers with P20
        transfer_to_columns(source_plate.columns()[start_col][0], 
                          start_col,
                          dest_plate, [1, 2], z_offset)
        
        transfer_to_columns(source_plate.columns()[start_col-1][0], 
                          start_col-1,
                          dest_plate, [3, 4, 5], z_offset)
        
        transfer_to_columns(source_plate.columns()[start_col-2][0], 
                          start_col-2,
                          dest_plate, [6, 7, 8], z_offset)
        
        transfer_to_columns(source_plate.columns()[start_col-3][0], 
                          start_col-3,
                          dest_plate, [9, 10, 11], z_offset)

    # Process each source plate
    for plate_idx in range(NUM_DILUTION_PLATES):
        source_plate = source_plates[plate_idx]
        starch_plate_offset = plate_idx * 3
        
        # Process first group: A4-A1
        process_four_columns(source_plate, 3, dest_plates[starch_plate_offset], 
                           plate_z_offsets[starch_plate_offset])
        
        # Process second group: A8-A5
        process_four_columns(source_plate, 7, dest_plates[starch_plate_offset + 1], 
                           plate_z_offsets[starch_plate_offset + 1])
        
        # Process third group: A12-A9
        process_four_columns(source_plate, 11, dest_plates[starch_plate_offset + 2], 
                           plate_z_offsets[starch_plate_offset + 2])