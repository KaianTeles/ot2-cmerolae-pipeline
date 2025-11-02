from opentrons import protocol_api

metadata = {
    'protocolName': 'PCR Colony Picks with Replication for two plates',
    'author': 'Kaian Teles',
    'description': 'PCR protocol for colony picks with 22 replicates per sample, makes two 96 well plates'
}

requirements = {
    "robotType": "OT-2",
    "apiLevel": "2.19"
}

def run(protocol: protocol_api.ProtocolContext):
    # Load labware
    tiprack_20_1 = protocol.load_labware('opentrons_96_tiprack_20ul', '1')
    tiprack_20_2 = protocol.load_labware('opentrons_96_tiprack_20ul', '4')
    cell_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '2')
    reserv_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '6')
    #stock_plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '5')
    
    # Load aluminum block adapter and PCR plate
    dest_plate = protocol.load_labware('abgenepcr_96_wellplate_200ul', '3')
    dest_plate2 = protocol.load_labware('abgenepcr_96_wellplate_200ul', '5')


    
    # Load pipettes
    p20_multi = protocol.load_instrument('p20_multi_gen2', 'left', tip_racks=[tiprack_20_1, tiprack_20_2])
    

    # Step 2: Transfer cells (2 µL aspirate, 1 µL dispense)
    # First set: Columns 1-3
    for i in range(3):
        source = cell_plate.columns()[i]
        dest1 = dest_plate.columns()[i]
        dest2 = dest_plate.columns()[i + 3]  # Column 3 positions away
        p20_multi.pick_up_tip()
        p20_multi.mix(5,10, source[0].bottom(z=1))
        p20_multi.aspirate(2, source[0].bottom(z=1))
        p20_multi.dispense(1, dest1[0].bottom(z=0.1))
        p20_multi.dispense(1, dest2[0].bottom(z=0.1))
        #p20_multi.dispense(10, stock_plate.columns()[i][0].bottom(z=stockoZofsset))
        p20_multi.drop_tip()
    
    # Second setdest2: Columns 4-6
    for i in range(3):
        source = cell_plate.columns()[i + 3]  # Start from column 4 (index 3)
        dest1 = dest_plate.columns()[i + 6]   # Start from column 7 (index 6)
        dest2 = dest_plate.columns()[i + 9]   # Start from column 10 (index 9)
        p20_multi.pick_up_tip()
        p20_multi.mix(5,10, source[0].bottom(z=1))
        p20_multi.aspirate(2, source[0].bottom(z=1))
        p20_multi.dispense(1, dest1[0].bottom(z=0.1))
        p20_multi.dispense(1, dest2[0].bottom(z=0.1))
        #p20_multi.dispense(10, stock_plate.columns()[i + 3][0].bottom(z=stockoZofsset))
        p20_multi.drop_tip()

    for i in range(3):
        source = cell_plate.columns()[ i+ 6]
        dest1 = dest_plate2.columns()[i]
        dest2 = dest_plate2.columns()[i + 3]  # Column 3 positions away
        p20_multi.pick_up_tip()
        p20_multi.mix(5,10, source[0].bottom(z=1))
        p20_multi.aspirate(2, source[0].bottom(z=1))
        p20_multi.dispense(1, dest1[0].bottom(z=0.1))
        p20_multi.dispense(1, dest2[0].bottom(z=0.1))
        #p20_multi.dispense(10, stock_plate.columns()[i][0].bottom(z=stockoZofsset))
        p20_multi.drop_tip()
    
    # Second set: Columns 4-6
    for i in range(3):
        source = cell_plate.columns()[i + 9]  # Start from column 4 (index 3)
        dest1 = dest_plate2.columns()[i + 6]   # Start from column 7 (index 6)
        dest2 = dest_plate2.columns()[i + 9]   # Start from column 10 (index 9)
        p20_multi.pick_up_tip()
        p20_multi.mix(5,10, source[0].bottom(z=1))
        p20_multi.aspirate(2, source[0].bottom(z=1))
        p20_multi.dispense(1, dest1[0].bottom(z=0.1))
        p20_multi.dispense(1, dest2[0].bottom(z=0.1))
        #p20_multi.dispense(10, stock_plate.columns()[i + 3][0].bottom(z=stockoZofsset))
        p20_multi.drop_tip()


     # Step 1: Transfer master mixes (9 µL)
    # First mastermix for all first positions (Left homology set 1)
    first_mastermix_cols = [0, 1, 2]  # Columns 1-3
    p20_multi.pick_up_tip()
    for col in first_mastermix_cols:
        p20_multi.aspirate(9, reserv_plate['A1'])
        p20_multi.dispense(9, dest_plate.columns()[col][0].bottom(z=12))
        p20_multi.blow_out(dest_plate.columns()[col][0].bottom(z=12))
        p20_multi.blow_out(dest_plate.columns()[col][0].bottom(z=12))
        p20_multi.touch_tip()
    p20_multi.drop_tip()
    # Second mastermix for all first positions (Right homology set 1)
    second_mastermix_cols = [3, 4, 5]  # Columns 4-6
    p20_multi.pick_up_tip()
    for col in second_mastermix_cols:
        p20_multi.aspirate(9, reserv_plate['A2'])
        p20_multi.dispense(9, dest_plate.columns()[col][0].bottom(z=12))
        p20_multi.blow_out(dest_plate.columns()[col][0].bottom(z=12))
        p20_multi.blow_out(dest_plate.columns()[col][0].bottom(z=12))
        p20_multi.touch_tip()
    p20_multi.drop_tip()
    
    # Third mastermix for all second positions (Left homology set 2)
    third_mastermix_cols = [6, 7, 8]  # Columns 7-9
    p20_multi.pick_up_tip()
    for col in third_mastermix_cols:
        p20_multi.aspirate(9, reserv_plate['A3'])
        p20_multi.dispense(9, dest_plate.columns()[col][0].bottom(z=12))
        p20_multi.blow_out(dest_plate.columns()[col][0].bottom(z=12))
        p20_multi.blow_out(dest_plate.columns()[col][0].bottom(z=12))
        p20_multi.touch_tip()
    p20_multi.drop_tip()

        # Fourth mastermix for all second positions (Right homology set 2)
    fourth_mastermix_cols = [9, 10, 11]  # Columns 10-12
    p20_multi.pick_up_tip()
    for col in fourth_mastermix_cols:
        p20_multi.aspirate(9, reserv_plate['A4'])
        p20_multi.dispense(9, dest_plate.columns()[col][0].bottom(z=12))
        p20_multi.blow_out(dest_plate.columns()[col][0].bottom(z=12))
        p20_multi.blow_out(dest_plate.columns()[col][0].bottom(z=12))
        p20_multi.touch_tip()
    p20_multi.drop_tip()

    # First mastermix for all first positions (Left homology set 1)
    first_mastermix2_cols = [0, 1, 2]  # Columns 1-3
    p20_multi.pick_up_tip()
    for col in first_mastermix2_cols:
        p20_multi.aspirate(9, reserv_plate['A5'])
        p20_multi.dispense(9, dest_plate2.columns()[col][0].bottom(z=12))
        p20_multi.blow_out(dest_plate2.columns()[col][0].bottom(z=12))
        p20_multi.blow_out(dest_plate2.columns()[col][0].bottom(z=12))
        p20_multi.touch_tip()
    p20_multi.drop_tip()
    # Second mastermix for all first positions (Right homology set 1)
    second_mastermix2_cols = [3, 4, 5]  # Columns 4-6
    p20_multi.pick_up_tip()
    for col in second_mastermix2_cols:
        p20_multi.aspirate(9, reserv_plate['A6'])
        p20_multi.dispense(9, dest_plate2.columns()[col][0].bottom(z=12))
        p20_multi.blow_out(dest_plate2.columns()[col][0].bottom(z=12))
        p20_multi.blow_out(dest_plate2.columns()[col][0].bottom(z=12))
        p20_multi.touch_tip()
    p20_multi.drop_tip()
    
    # Third mastermix for all second positions (Left homology set 2)
    third_mastermix2_cols = [6, 7, 8]  # Columns 7-9
    p20_multi.pick_up_tip()
    for col in third_mastermix2_cols:
        p20_multi.aspirate(9, reserv_plate['A7'])
        p20_multi.dispense(9, dest_plate2.columns()[col][0].bottom(z=12))
        p20_multi.blow_out(dest_plate2.columns()[col][0].bottom(z=12))
        p20_multi.blow_out(dest_plate2.columns()[col][0].bottom(z=12))
        p20_multi.touch_tip()
    p20_multi.drop_tip()

        # Fourth mastermix for all second positions (Right homology set 2)
    fourth_mastermix2_cols = [9, 10, 11]  # Columns 10-12
    p20_multi.pick_up_tip()
    for col in fourth_mastermix2_cols:
        p20_multi.aspirate(9, reserv_plate['A8'])
        p20_multi.dispense(9, dest_plate2.columns()[col][0].bottom(z=12))
        p20_multi.blow_out(dest_plate2.columns()[col][0].bottom(z=12))
        p20_multi.blow_out(dest_plate2.columns()[col][0].bottom(z=12))
        p20_multi.touch_tip()
    p20_multi.drop_tip()




    
