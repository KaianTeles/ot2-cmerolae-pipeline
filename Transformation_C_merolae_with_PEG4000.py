from opentrons import protocol_api

metadata = {
    'protocolName': 'Transformation C.Merolae with PEG4000',
    'author': 'Kaian Teles',
    'description': 'Transformation protocol for C.Merolae with PEG4000 - Multi-group processing',
    'source': 'Kaian Teles'
}

requirements = {
    'robotType': 'OT-2',
    'apiLevel': '2.19'
}

def add_parameters(parameters):
    parameters.add_int(
        variable_name="group_count",
        display_name="Number of Groups",
        description="Select number of groups to process (each group = 3 columns)",
        default=1,
        minimum=1,
        maximum=4
    )

def run(protocol: protocol_api.ProtocolContext):
    # Access runtime parameter
    GROUP_COUNT = protocol.params.group_count
    
    # Load modules
    temp_module_rxn = protocol.load_module('temperature module gen2', 5)
    
    temp_module_rxn.set_temperature(42)
    
    # Load labware
    reservoir = temp_module_rxn.load_labware('nest_96_wellplate_2ml_deep')
    
    # Load tip racks for OT-2
    tiprack_200_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 1)

    
    # Load OT-2 pipette
    p300_multi = protocol.load_instrument(
        'p300_multi_gen2', 
        'right', 
        tip_racks=[tiprack_200_1]
    )
    

    
    # Process each group
    for group in range(GROUP_COUNT):
        protocol.comment(f"Processing group {group + 1}")
        
        # Calculate column indices for this group (3 columns per group)
        col_1 = group * 3      # First column of group
        col_2 = group * 3 + 1  # Second column of group  
        col_3 = group * 3 + 2  # Third column of group
        
        # Pick up tip once per group
        p300_multi.pick_up_tip()
        
        # Step 1: Transfer 125 µL from second row to first row of the group
        # Set slow flow rates for viscous liquid
        p300_multi.flow_rate.aspirate = 25
        p300_multi.flow_rate.dispense = 25
        
        p300_multi.aspirate(125, reservoir.columns()[col_2][0].bottom(1))
        protocol.delay(seconds=5)
        p300_multi.dispense(125, reservoir.columns()[col_1][0].bottom(1))
        protocol.delay(seconds=5)
        p300_multi.mix(3,150,reservoir.columns()[col_1][0].bottom(1))
        
        
        # Step 3: Transfer 1 mL from third row to first row in batches (300 µL x 3 + 100 µL)
        # Set flow rates for transfer
        p300_multi.flow_rate.aspirate = 94
        p300_multi.flow_rate.dispense = 94
        
        # First three transfers of 300 µL each
        p300_multi.aspirate(200, reservoir.columns()[col_3][0].bottom(1))
        p300_multi.dispense(200, reservoir.columns()[col_1][0].bottom(1))
        p300_multi.aspirate(200, reservoir.columns()[col_3][0].bottom(1))
        p300_multi.dispense(200, reservoir.columns()[col_1][0].bottom(1))
        p300_multi.aspirate(200, reservoir.columns()[col_3][0].bottom(1))
        p300_multi.dispense(200, reservoir.columns()[col_1][0].bottom(1))
        p300_multi.aspirate(200, reservoir.columns()[col_3][0].bottom(1))
        p300_multi.dispense(200, reservoir.columns()[col_1][0].bottom(1))
        p300_multi.aspirate(200, reservoir.columns()[col_3][0].bottom(1))
        p300_multi.dispense(200, reservoir.columns()[col_1][0].bottom(1))
        

        p300_multi.drop_tip()
        
        protocol.comment(f"Group {group + 1} processing complete")
    protocol.comment(f"All {GROUP_COUNT} groups processed successfully")