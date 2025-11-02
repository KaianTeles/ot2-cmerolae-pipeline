from opentrons import protocol_api

metadata = {
    'protocolName': 'Starch Solution Dispensing with Z-offset Adjustment',
    'author': 'Kaian Teles', 
    'description': 'Makes up to 8 plates with starch spots'
}

requirements = {
    "robotType": "OT-2",
    "apiLevel": "2.19"
}

def add_parameters(parameters):

    parameters.add_int(
        variable_name="plate_count",
        display_name="Number of Plates",
        description="How many plates do you want to use? (1–8)",
        default=8,
        minimum=1,
        maximum=8
    )


    parameters.add_float(
        variable_name="Z_offset_plate_1",
        display_name="Plate in position 3",
        description="Insert plate weight in grams",
        default=50,
        minimum=0,
        maximum=100
    )

    parameters.add_float(
        variable_name="Z_offset_plate_2",
        display_name="ZPlate in position 5",
        description="Insert plate weight in grams",
        default=50,
        minimum=0,
        maximum=100
    )

    parameters.add_float(
        variable_name="Z_offset_plate_3",
        display_name="Plate in position 6",
        description="Insert plate weight in grams",
        default=50,
        minimum=0,
        maximum=100
    )

    parameters.add_float(
        variable_name="Z_offset_plate_4",
        display_name="Plate in position 7",
        description="Insert plate weight in grams",
        default=50,
        minimum=0,
        maximum=100
    )

    parameters.add_float(
        variable_name="Z_offset_plate_5",
        display_name="Plate in position 8",
        description="Insert plate weight in grams",
        default=50,
        minimum=0,
        maximum=100
    )

    parameters.add_float(
        variable_name="Z_offset_plate_6",
        display_name="Plate in position 9",
        description="Insert plate weight in grams",
        default=50,
        minimum=0,
        maximum=100
    )
    parameters.add_float(
        variable_name="Z_offset_plate_7",
        display_name="Plate in position 10",
        description="Insert plate weight in grams",
        default=50,
        minimum=0,
        maximum=100
    )
    parameters.add_float(
        variable_name="Z_offset_plate_8",
        display_name="Plate in position 11",
        description="Insert plate weight in grams",
        default=50,
        minimum=0,
        maximum=100
    )
def get_plate_slot_list(num_plates):
    """Returns a list of slot strings based on how many plates the user selected."""
    slot_order = ['3', '5', '6', '7', '8', '9', '10', '11']
    return slot_order[:num_plates]

def run(protocol: protocol_api.ProtocolContext):


    # Plate selection
    
    plate_slots = get_plate_slot_list(protocol.params.plate_count)

    # Z-offset adjustments for each plate (in mm)
    # Modify these values before running the protocol
    PLATE1 = protocol.params.Z_offset_plate_1
    PLATE2 = protocol.params.Z_offset_plate_2
    PLATE3 = protocol.params.Z_offset_plate_3
    PLATE4 = protocol.params.Z_offset_plate_4
    PLATE5 = protocol.params.Z_offset_plate_5
    PLATE6 = protocol.params.Z_offset_plate_6
    PLATE7 = protocol.params.Z_offset_plate_7
    PLATE8 = protocol.params.Z_offset_plate_8

    GellanGumVolume=10567.2*0.001028

    PLATEADJUSTED1 = PLATE1 / (GellanGumVolume)
    PLATEADJUSTED2 = PLATE2 / (GellanGumVolume)
    PLATEADJUSTED3 = PLATE3 / (GellanGumVolume)
    PLATEADJUSTED4 = PLATE4 / (GellanGumVolume)
    PLATEADJUSTED5 = PLATE5 / (GellanGumVolume)
    PLATEADJUSTED6 = PLATE6 / (GellanGumVolume)
    PLATEADJUSTED7 = PLATE7 / (GellanGumVolume)
    PLATEADJUSTED8 = PLATE8 / (GellanGumVolume)


    plate_z_offsets = [
    PLATEADJUSTED1,
    PLATEADJUSTED2,
    PLATEADJUSTED3,
    PLATEADJUSTED4,
    PLATEADJUSTED5,
    PLATEADJUSTED6,
    PLATEADJUSTED7,
    PLATEADJUSTED8,
    ]
    
    # Load modules in slot 1
    heater_shaker = protocol.load_module('heaterShakerModuleV1', '1')
    
    # Open latch, load reservoir, and close latch
    heater_shaker.open_labware_latch()
    reservoir = heater_shaker.load_labware('agilent_1_reservoir_290ml')
    protocol.pause("Please ensure reservoir is properly placed on heater-shaker module.")
    heater_shaker.close_labware_latch()
    
    # Load destination plates avoiding slots adjacent to heater-shaker
    dest_plates = [
        protocol.load_labware('corning_96_wellplate_360ul_flat', slot) 
        for slot in plate_slots
    ]
    
    # Load tiprack
    tiprack_20 = protocol.load_labware('opentrons_96_tiprack_20ul', '4')

    # Load pipette
    p20_multi = protocol.load_instrument(
        'p20_multi_gen2',
        'left',
        tip_racks=[tiprack_20]
    )
    
    # Pick up tip once at the start
    
    # Initial shake
    heater_shaker.set_and_wait_for_shake_speed(rpm=2000)
    protocol.delay(seconds=10)
    heater_shaker.deactivate_shaker()
    protocol.delay(seconds=1)  # Brief pause to ensure complete stop
    
    # Process each plate
    for i, plate in enumerate(dest_plates):
        p20_multi.pick_up_tip()
        # Process all columns in current plate using the corresponding Z-offset
        for col_idx in range(0, 12, 2):
            if col_idx + 1 < 12:
                p20_multi.aspirate(20, reservoir['A1'].bottom(z= 2))
                # Dispense to first column with plate-specific offset
                p20_multi.dispense(10, plate.columns()[col_idx][0].bottom(z=plate_z_offsets[i]))
                # Dispense to second column with same offset
                p20_multi.dispense(10, plate.columns()[col_idx + 1][0].bottom(z=plate_z_offsets[i]))
            
            # Shake after every 6 columns (3 cycles since we process 2 columns at a time)
            if (col_idx + 2) % 6 == 0 and col_idx < 10:
                heater_shaker.set_and_wait_for_shake_speed(rpm=2000)
                protocol.delay(seconds=10)
                heater_shaker.deactivate_shaker()
                protocol.delay(seconds=1)  # Brief pause to ensure complete stop

        p20_multi.drop_tip()
        # After plate is complete, shake if there are more plates to process
        if i < len(dest_plates) - 1:
            heater_shaker.set_and_wait_for_shake_speed(rpm=2000)
            protocol.delay(seconds=10)
            heater_shaker.deactivate_shaker()
            protocol.delay(seconds=1)
    
    # Drop tip at the very end

