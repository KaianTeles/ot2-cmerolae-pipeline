from opentrons import protocol_api

metadata = {
    'protocolName': 'PCR Colony Picks with Replication',
    'author': 'Kaian Teles',
    'description': 'Colony PCR assembly with duplicate reactions, 1 to 4 groups of three columns, up to two 96 well plates'
}

requirements = {
    "robotType": "OT-2",
    "apiLevel": "2.19"
}

def add_parameters(parameters):

    parameters.add_int(
        variable_name="group_count",
        display_name="Number of Groups",
        description="Each group = 3 source columns. 1 = half a plate, 2 = one full plate, 4 = two plates",
        default=4,
        minimum=1,
        maximum=4
    )

def get_destination_plate_count(num_groups):
    """Returns how many destination PCR plates are needed. Two groups fill one plate."""
    return (num_groups + 1) // 2

def get_destination_slot_list(num_plates):
    """Returns a list of slot strings based on how many destination plates are needed."""
    slot_order = ['3', '5']
    return slot_order[:num_plates]

def run(protocol: protocol_api.ProtocolContext):

    # Access runtime parameter
    GROUP_COUNT = protocol.params.group_count

    DEST_PLATE_COUNT = get_destination_plate_count(GROUP_COUNT)
    dest_slots = get_destination_slot_list(DEST_PLATE_COUNT)

    # Volumes
    CELL_MIX_REPS = 5
    CELL_MIX_VOLUME = 10
    CELL_ASPIRATE_VOLUME = 2
    CELL_DISPENSE_VOLUME = 1
    MASTERMIX_VOLUME = 9

    # Dispensing heights
    SOURCE_Z = 1
    CELL_DISPENSE_Z = 0.1
    MASTERMIX_DISPENSE_Z = 12

    # Load tip racks. The second rack is only needed from three groups onward
    # (five tip columns per group, twelve columns per rack).
    tipracks = [protocol.load_labware('opentrons_96_tiprack_20ul', '1')]
    if GROUP_COUNT >= 3:
        tipracks.append(protocol.load_labware('opentrons_96_tiprack_20ul', '4'))

    # Load labware
    cell_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '2')
    reserv_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr', '6')

    # Load destination PCR plates
    dest_plates = [
        protocol.load_labware('abgenepcr_96_wellplate_200ul', slot)
        for slot in dest_slots
    ]

    # Load pipette
    p20_multi = protocol.load_instrument(
        'p20_multi_gen2',
        'left',
        tip_racks=tipracks
    )

    protocol.comment(f"Processing {GROUP_COUNT} group(s) onto {DEST_PLATE_COUNT} destination plate(s) in slot(s) {', '.join(dest_slots)}")

    # Step 1: Transfer cells (2 µL aspirate, 1 µL dispensed into each of two replicates)
    for group in range(GROUP_COUNT):
        protocol.comment(f"Group {group + 1}: distributing cells")

        source_start = group * 3           # First source column of the group
        dest_plate = dest_plates[group // 2]
        dest_start = (group % 2) * 6       # First destination column of the group

        for i in range(3):
            source = cell_plate.columns()[source_start + i]
            dest1 = dest_plate.columns()[dest_start + i]
            dest2 = dest_plate.columns()[dest_start + i + 3]   # Column 3 positions away
            p20_multi.pick_up_tip()
            p20_multi.mix(CELL_MIX_REPS, CELL_MIX_VOLUME, source[0].bottom(z=SOURCE_Z))
            p20_multi.aspirate(CELL_ASPIRATE_VOLUME, source[0].bottom(z=SOURCE_Z))
            p20_multi.dispense(CELL_DISPENSE_VOLUME, dest1[0].bottom(z=CELL_DISPENSE_Z))
            p20_multi.dispense(CELL_DISPENSE_VOLUME, dest2[0].bottom(z=CELL_DISPENSE_Z))
            p20_multi.drop_tip()

    # Step 2: Transfer master mixes (9 µL)
    # Each group uses two mastermix columns: Left homology, then Right homology.
    for group in range(GROUP_COUNT):
        protocol.comment(f"Group {group + 1}: distributing master mixes")

        dest_plate = dest_plates[group // 2]
        dest_start = (group % 2) * 6

        for half in range(2):
            side = "Left" if half == 0 else "Right"
            mastermix_well = reserv_plate.columns()[group * 2 + half][0]
            mastermix_cols = range(dest_start + half * 3, dest_start + half * 3 + 3)

            protocol.comment(f"Group {group + 1}: {side} homology mastermix from column {group * 2 + half + 1}")

            p20_multi.pick_up_tip()
            for col in mastermix_cols:
                target = dest_plate.columns()[col][0]
                p20_multi.aspirate(MASTERMIX_VOLUME, mastermix_well)
                p20_multi.dispense(MASTERMIX_VOLUME, target.bottom(z=MASTERMIX_DISPENSE_Z))
                p20_multi.blow_out(target.bottom(z=MASTERMIX_DISPENSE_Z))
                p20_multi.blow_out(target.bottom(z=MASTERMIX_DISPENSE_Z))
                p20_multi.touch_tip()
            p20_multi.drop_tip()

    protocol.comment(f"Protocol complete! {GROUP_COUNT * 48} reactions assembled across {DEST_PLATE_COUNT} plate(s).")
