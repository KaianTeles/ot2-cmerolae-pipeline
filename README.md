# ot2-cmerolae-pipeline

This repository contains Python protocols for the Opentrons OT-2 liquid handler automating *Cyanidioschyzon merolae* nuclear transformations. The workflow covers PEG-mediated transformation, serial dilution of recovered transformants, automated starch-bed pouring with plate-weight–dependent Z-offset calibration, colony plating, and colony PCR screening.

## Before running any protocol

Every protocol in this repository requires labware calibration in the Opentrons App before its first run.

Calibration is tied to a specific labware definition in a specific deck slot. The same plate type in a different slot counts as a different calibration, and a different plate type in the same slot does too. Changing the deck layout of a protocol therefore means calibrating the new combinations.

Once a labware/slot combination has been calibrated, the offset is stored by the robot and reapplied automatically on every later run. You do not need to repeat it, unless you move the robot, recalibrate the pipettes, or change the deck layout.

First-time setup, in order:

1. **Robot calibration** — deck calibration, tip length calibration and pipette offset calibration must be complete for the pipettes used. These are done once per robot and pipette, not per protocol.
2. **Custom labware** — any protocol using a custom definition needs the `.json` imported first, through Labware → Import in the Opentrons App. The definition must be present before the protocol will load, and it is stored on the computer running the App, not inside the `.py` file.
3. **Labware Position Check** — when setting up a run, step through Labware Position Check for each piece of labware on the deck. Jog the pipette until the tip sits centred over the well, both in X and Y, and then bring it down to roughly 1 mm above the rim of the labware. Read the position from the front and from the side before accepting it, since a tip that looks centred from one angle is often off from the other. Save the offsets when prompted.

Protocols here dispense at tightly defined Z heights — 0.1 mm above the well bottom for cell transfers, plate-weight–derived offsets for starch plating. An uncalibrated or stale offset will crash the tip into the plate or dispense into air, so do not skip this step on a new deck layout.

# For PEG4000 transformation

*C. merolae* PEG-Mediated Transformation Protocol
Protocol Name: Transformation C.Merolae with PEG4000
OT-2 Script: Transformation_C_merolae_with_PEG4000.py (Opentrons API v2.19)
Purpose: Automate the PEG4000 addition and post-transformation dilution steps for up to four groups of transformations, with all liquid handling confined to a single 2 mL deep-well plate held at 42 °C on a temperature module.

1. OT-2 Setup

| Slot | Labware / Module | Description |
|------|------------------|-------------|
| 1 | `opentrons_96_tiprack_300ul` | Tip rack for P300 |
| 5 | `temperature module gen2` + `nest_96_wellplate_2ml_deep` | Reaction plate, held at 42 °C |
| — | `p300_multi_gen2` (right mount) | For all liquid handling |

Hardware Requirements

Opentrons OT-2 (API v2.19+) – Main automation platform
P300 Multi GEN2 (right mount) – Pipetting transformation reagents
Temperature Module GEN2 (Slot 5) – Holds the reaction plate at 42 °C
NEST 2 mL Deep-Well Plate (on module, slot 5) – Holds cells, PEG and MA2G
Tip Rack 300 µL (Slot 1) – One tip column consumed per group

- In the Opentrons App, select the number of groups to transform (1–4).
  - Each group corresponds to a set of three columns:
    - Group 1: columns 1–3
    - Group 2: columns 4–6
    - Group 3: columns 7–9
    - Group 4: columns 10–12
- Within each group, the three columns have fixed roles:
  - First column — transformation mix (cells + DNA)
  - Second column — PEG4000 solution
  - Third column — MA2G for dilution

2. Reagent Preparation and Manual Assembly (Deep-Well Plate)

- Pellet the cells at OD ~0.6 to 0.8 by centrifugation at 2000 × g for 10 minutes.
- Carefully save the supernatant to prepare MA2G later, if needed.
- Resuspend the cell pellet in 1 mL of 1X MA I medium.
- Spin down again and resuspend the entire pellet in a final volume of 200 µL of 1X MA I.
- Dispense 25 µL of the resuspended cells into the first column of each group.
- Cover the plate with parafilm and incubate at room temperature or in a 42 °C incubator until ready to proceed.

- In the second column of each group, add 200 µL of PEG4000 solution (0.9 g of PEG4000 dissolved in 750 µL of 1X MA I). The protocol withdraws 125 µL; the remainder covers dead volume.

- In the first column of each group, when the protocol is ready to run, bring the transformation mix to a final volume of 100 µL:
  - 25 µL of resuspended cells (already in the well)
  - 2 pmol of target DNA
  - 10 µL of 10X MA I
  - Nuclease-free water to reach 100 µL total volume.

3. Dilution Reservoir Setup

- Assemble the temperature module with the metal adapter and the NEST 2 mL deep-well plate in slot 5.
- Add 1.2 mL of MA2G medium to each well of the third column of each group: column 3 for group 1, column 6 for group 2, column 9 for group 3, column 12 for group 4. The protocol withdraws 1 mL in five 200 µL steps; the remainder covers dead volume.

4. Running the OT-2 Protocol

- Load the prepared plate onto the temperature module and the tip rack in slot 1.
- Select the appropriate number of groups in the Opentrons App.
- Start the protocol. For each group, the OT-2 will:
  - Set the module to 42 °C.
  - Transfer 125 µL of PEG4000 into the first column at reduced flow rate (25 µL/s), with 5 s pauses on aspiration and dispense to allow the viscous solution to settle.
  - Mix 3 × 150 µL in the first column.
  - Add 1 mL of MA2G in five 200 µL steps at standard flow rate.
  - Use one tip column per group.

5. Post-Transformation Handling

- Final volume in each first column is approximately 1.2 mL.
- Once the OT-2 protocol is complete, transfer the entire contents of each first column to an individual flask containing 49 mL of MA2G pre-warmed to 42 °C.
- Continue incubation as required for recovery or proceed with plating on selective media.

# For 3X Cell Dilution

*C. merolae* Serial Dilution Protocol
Protocol Name: 3X Cell Dilution Protocol
OT-2 Script: 3X cell dilutions.py (Opentrons API v2.19)
Purpose: Perform automated 3× serial dilutions of three transformants per 96-well plate, in three series starting at columns 1, 5 and 9, across up to 7 plates. The method pre-loads diluent to the destination wells, then transfers a fixed volume forward to achieve ~3× dilution at each step.

1. OT-2 Setup

| Slot | Labware / Module | Description |
|------|------------------|-------------|
| 1 | `opentrons_96_tiprack_300ul` | Tip rack 1 |
| 2 | `opentrons_96_tiprack_300ul` | Tip rack 2 |
| 3–9 | `corning_96_wellplate_360ul_flat` | Source/destination plates (up to 7) |
| 11 | `axygen_1_reservoir_90ml` | Diluent reservoir |
| — | `p300_multi_gen2` (right mount) | For dilution transfers |

> **Deck layout guidance:** Three dilution series per plate start at columns 1, 5, and 9 — spanning four columns per series (1→4, 5→8, 9→12). Plates occupy consecutive slots from 3 upward, so two plates are slots 3–4 and seven plates are slots 3–9.

Hardware Requirements

Opentrons OT-2 (API v2.19+) – Automated liquid handling
P300 Multi GEN2 (right mount) – Perform serial dilutions
Tip Rack 300 µL (×2, Slots 1–2) – Up to 22 tip columns consumed at 7 plates
96-well Plates (Slots 3–9) – Dilution sequence plates
Reservoir 90 mL (Slot 11) – Contains MA2G or other diluent

2. Reagent & Sample Preparation (Manual)

  1. Prepare diluent (e.g., MA2G) and load A1 of the reservoir (slot 11).
  2. Prepare cells: After 48 h recovery, resuspend each *C. merolae* transformant in 2.7 mL of MA2G (or as per your culture SOP).
  3. Plate loading (starting wells):
   - For each plate in use, pipette 200 µL of transformant into A1, A5, A9 (start wells for the three series).

3. What the Protocol Does (Automated Steps)

The script performs a 4-column, 3-step 3× dilution for three series per plate:
- Diluent pre-load: Adds 133 µL diluent to every destination well, skipping the three starting columns (1, 5 and 9). One tip column is used for all plates.
- Serial transfers: Mixes 5 × 100 µL in the starting well, then moves 67 µL forward to the next column, mixing 3 × 100 µL in the destination after each transfer. One tip column per series.
- Dilution math: 67 µL sample + 133 µL diluent = 200 µL total → ~3× dilution.
- Series layout: 1→4, 5→8, 9→12 per plate.
- Plates processed: Up to 7, selected via the `plate_count` run parameter.

4. Running the OT-2 Protocol

  1. Load labware to the deck as in Section 1.
  2. In the Opentrons App, select Number of plates (`plate_count`, default 2, max 7).
  3. Place starting samples (200 µL) in A1, A5, A9 of each plate.
  4. Start the run. The robot will:
   - Pre-fill destination wells with 133 µL diluent.
   - Execute three forward transfers of 67 µL per series with mixing after each transfer.
  5. At completion, the app will display "Protocol complete! 3X dilutions performed for all plates, three series per plate."

5. Expected Layout & Volumes

For each plate (row A addressed with the multichannel, so all eight rows are processed):

| Series | Columns | Start vol (µL) | Diluent pre-load (µL) | Transfer (µL) | Final vol (µL) | Fold |
|:------:|:--------:|:--------------:|:---------------------:|:--------------:|:---------------:|:----:|
| 1 | 1–4 | 200 | 133 | 67 | 200 | ~3× |
| 2 | 5–8 | 200 | 133 | 67 | 200 | ~3× |
| 3 | 9–12 | 200 | 133 | 67 | 200 | ~3× |

The starting well of each series ends at 133 µL, since 67 µL is removed and not replaced. Every other well ends at 200 µL.

6. Post-Run Handling

- Seal plates or proceed to downstream steps (plating, OD measurement, screening).
- For plating, maintain consistent pipetting heights and mixing.

# For Starch Bed plating in Gellan Gum

*C. merolae* Starch-Bed Pouring Protocol
Protocol Name: Starch Solution Dispensing with Z-offset Adjustment
OT-2 Script: Starch plating.py (Opentrons API v2.19)
Purpose: Automate the pouring of starch-based plating medium across up to 8 plates using plate-weight–dependent Z-axis height calibration. This ensures even distribution and prevents premature solidification due to the high viscosity and fast-gelling nature of starch-gellan mixtures.

1. OT-2 Setup

| Slot | Labware / Module | Description |
|------|------------------|-------------|
| 1 | `heaterShakerModuleV1` + `agilent_1_reservoir_290ml` | Contains 25 mL 20% starch solution |
| 3, 5–11 | `corning_96_wellplate_360ul_flat` | PlusPlates, up to 8 — see note below |
| 4 | `opentrons_96_tiprack_20ul` | Tip rack |
| — | `p20_multi_gen2` (left mount) | Dispensing starch |
| — | HEPA Filter Attachment | Turn ON during pouring |

> **On the destination plate definition.** The plates used here are PlusPlates (Singer Instruments): single-well, SBS-footprint plates with no wells, poured with ~50 mL of gellan medium to give one flat surface. They are loaded in the protocols as `corning_96_wellplate_360ul_flat` purely as a coordinate map — the definition hands the OT-2 a standard 8 × 12 grid so the multichannel can address an array of positions across the flat agar. No Corning plate is involved and the 360 µL well volume is irrelevant. Calibrate this labware against the actual PlusPlate sitting in each slot, not against a 96-well plate.

Hardware Requirements

Opentrons OT-2 (API v2.19+) – Automated dispensing
Heater-Shaker Module V1 (Slot 1) – Keeps starch homogeneous
P20 Multi GEN2 (left mount) – Dispenses 10 µL per column
Tip Rack 20 µL (Slot 4) – One tip column per plate, 8 columns at full capacity
290 mL Reservoir (on heater-shaker, slot 1) – Contains starch-gellan mix
PlusPlates (×8, Slots 3, 5–11) – Pouring destinations, loaded as a 96-well definition
HEPA Filter Unit – Dry spots faster

2. Preparation of Gellan Gum

- Dissolve 3.5 g of Gellan Gum in 584.5 mL of distilled water.
- Autoclave the solution to sterilize it completely.

3. Preparation of 3× MA2G

Refer to "Stock solutions preparation.docx" for detailed stock recipes.
Combine the following components:
- Solution I: 58.5 mL
- Solution II: 5.850 mL
- Solution III: 0.585 mL
- Solution IV: 2.330 mL
- Glycerol (37.5%): 7.6 mL
- Distilled water: 100 mL
Filter sterilize the final mixture before use.

4. Starch Preparation

  1. In a 50 mL Falcon tube, add starch to the 30 mL mark.
  2. Add water up to 45 mL and vortex thoroughly.
  3. Centrifuge at 5,000 rpm for 30 seconds and discard supernatant.
  4. Repeat washing twice with water.
  5. Wash once with 75% ethanol, discard the supernatant.
  6. Add ethanol to yield a 50% slurry and store at 4 °C.
  7. Before use, vortex the 50% slurry and take 10 mL.
  8. Repeat two water washes (centrifuge at 5,000 rpm for 30 s each) and discard the supernatant.
  9. Resuspend to a final volume of 25 mL in MA2G.

5. Pre-Incubation Step

Before pouring, incubate both the autoclaved Gellan Gum and the sterile 3× MA2G solutions at 42 °C for at least one hour. This prevents the Gellan Gum from solidifying too quickly when mixed.

6. Plate Preparation

- Prepare the number of plates you wish to pour in advance. The amounts above make ~760 mL, enough for about 15 plates at 50 mL each.
- If using chloramphenicol as antibiotic, add 1.9 mL of 100 mg/mL in ethanol stock to the 3× MA2G and homogenize.
- Mix the warmed Gellan Gum and 3× MA2G thoroughly.
- Using a sterile 50 mL Falcon tube, aliquot ~50 mL and pour into each plate inside a biosafety cabinet.
- After solidification, weigh each plate and label the lid with the plate weight.

7. Parameters and Calibration

Each plate's weight (g) is recorded before the run and entered in the OT-2 interface, under the run parameter naming that plate's deck position. The protocol converts plate weight into a Z-offset using:

    Z_offset_adjusted = (Plate_weight) / (10,567.2 × 0.001028)

Each calculated Z-offset compensates for height variation from plate to plate, ensuring precise pipetting depth. A 50 g plate gives an offset of about 4.6 mm above the well bottom.

8. Automated Steps

  1. The heater-shaker is engaged to mix the starch solution (2,000 rpm for 10 s) before the first plate.
  2. For each plate:
   - Pick up one tip column.
   - Aspirate 20 µL of starch from the reservoir (A1), 2 mm above the bottom.
   - Dispense 10 µL into each of two adjacent columns (1–2, then 3–4, and so on), using that plate's Z-offset.
   - After the first six columns, the heater-shaker mixes again (2,000 rpm, 10 s).
   - Drop the tip after finishing the plate.
  3. Between plates, the heater-shaker repeats the mixing step to prevent settling.

9. Running the OT-2 Protocol

  1. Load the heater-shaker with the starch reservoir, close the latch, and confirm placement when the protocol pauses.
  2. Load the destination plates (up to 8) in slots 3, 5–11.
  3. Enter plate weights under "Run Parameters."
  4. Confirm pipette calibration and shaking settings.
  5. Start the run. The OT-2 will automatically dispense starch with plate-specific Z-offset adjustments.
  6. After 8 plates, refill the reservoir to 25 mL before restarting the next batch.

10. Expected Results

- Each column receives 10 µL, so 120 µL per plate per channel and about 7.7 mL of starch across 8 full plates.
- The starch surface should appear uniform and centered.
- Z-offset calibration compensates for varying plate heights, preventing overflow or shallow deposition.

11. Post-Run Handling

- Allow plates to cool and solidify on a level surface for 10 minutes.

# Cell Plating on Starch

*C. merolae* Cell Plating on Starch Protocol
Protocol Name: Cell plating on Starch
OT-2 Script: CellPlatingOnStarch.py (Opentrons API v2.19)
Purpose: Automate the plating of diluted *C. merolae* cells onto starch-containing solid media plates following the "3X Cell Dilution Protocol." The script uses weight-based Z-offset calibration to ensure even plating height across up to six destination plates.

1. Overview

This protocol is executed immediately after the "3X Cell Dilution Protocol."
The diluted *C. merolae* cultures should be positioned in slots 3 and 4 of the OT-2 deck. These serve as source plates for automated plating onto starch media plates located in slots 5–10.

Each source plate feeds three starch plates. Set the plate counts to match: one dilution plate with three starch plates, or two dilution plates with six. Selecting three starch plates together with two dilution plates will stop the run partway through, because the second source plate has no destinations assigned to it.

2. OT-2 Setup

| Slot | Labware / Module | Description |
|------|------------------|-------------|
| 1 | `opentrons_96_filtertiprack_20ul` | Filter tip rack #1 (P20) |
| 2 | `opentrons_96_filtertiprack_20ul` | Filter tip rack #2 (P20) |
| 3 | `corning_96_wellplate_360ul_flat` | Source plate #1 (diluted cells) |
| 4 | `corning_96_wellplate_360ul_flat` | Source plate #2 (optional) |
| 5–7 | `corning_96_wellplate_360ul_flat` | PlusPlates, destinations for the source in slot 3 |
| 8–10 | `corning_96_wellplate_360ul_flat` | PlusPlates, destinations for the source in slot 4 |
| 11 | `opentrons_96_tiprack_300ul` | Tip rack for P300 mixing |
| — | `p20_multi_gen2` (left mount) | Dispensing cell aliquots |
| — | `p300_multi_gen2` (right mount) | Mixing before plating |

The destination plates are the PlusPlates poured in the previous protocol, again loaded as `corning_96_wellplate_360ul_flat` for its 8 × 12 coordinate grid. The source plates in slots 3 and 4 are real Corning 96-well plates carrying the dilution series.

Hardware Requirements

Opentrons OT-2 (API v2.19+) – Automated plating
P20 Multi GEN2 (left mount) – Dispensing diluted cells
P300 Multi GEN2 (right mount) – Mixing source wells
Filter Tip Racks 20 µL (×2, Slots 1–2) – 24 tip columns consumed with two source plates, so both racks must be full
Tip Rack 300 µL (Slot 11) – 6 tip columns for P300 mixing
Corning 96-well Plates (×2, Slots 3–4) – Diluted cells
PlusPlates (×6, Slots 5–10) – Starch plating destinations, loaded as a 96-well definition

3. Parameters and Z-Offset Calibration

Before execution, specify the following in the Opentrons App:
- Number of destination starch plates (3 or 6)
- Number of dilution plates (1 or 2; slots 3 and 4)
- Weight of each starch plate (g) for Z-offset calibration

Each Z-offset is calculated as:

    Z_offset_adjusted = (Plate_weight) / (10,567.2 × 0.001028)

Offsets ensure consistent pipetting height across plates poured with variable starch-bed thickness.

4. Automated Plating Steps

  1. The robot loads source plates (diluted cells) and destination starch plates according to the selected parameters.
  2. Each dilution plate is processed independently:
   - The first dilution plate (slot 3) corresponds to starch plates in slots 5–7.
   - The second dilution plate (slot 4) corresponds to starch plates in slots 8–10.
  3. Mixing and transfer are handled in structured column groups:
   - Source columns 1–4 → first starch plate (slot 5 or 8)
   - Source columns 5–8 → second starch plate (slot 6 or 9)
   - Source columns 9–12 → third starch plate (slot 7 or 10)
  4. For each group, the P300 multichannel resuspends all four source columns (4 × 60 µL at double speed) before any transfer.
  5. The P20 multichannel then aspirates and dispenses 10 µL aliquots into the destination columns at the plate's Z-offset. Aspiration height within each source column is fixed to match the expected liquid level, from 0.7 mm in the first column of a series up to 3.3 mm in the fourth.
  6. The process repeats for all plates, using fresh tips for each source column.

5. Dilution Mapping and Layout

Column-to-dilution mapping follows the standard plating scheme:

| Destination columns | Source column | Dilution factor |
|---------------------|---------------|-----------------|
| 1 | — | Negative control (untransformed cells, pipetted manually) |
| 2–3 | 4 (or 8, 12) | 81× dilution |
| 4–6 | 3 (or 7, 11) | 27× dilution |
| 7–9 | 2 (or 6, 10) | 9× dilution |
| 10–12 | 1 (or 5, 9) | 3× dilution |

Dilution factors count the initial resuspension in MA2G as the first 3× step, so the starting well of each dilution series is already at 3×.

Each destination plate receives the full dilution range from its respective source plate.

6. Customizing Plate Count

Users can define the number of destination plates (3 or 6) and the number of dilution plates (1 or 2). Use three starch plates with one dilution plate, or six with two. If only one dilution plate is used, the robot processes starch plates in slots 5–7 only.

7. Expected Results

- Even distribution of cell spots across all destination plates.
- Uniform Z-height for deposition, minimizing pipette contact with starch surface.
- Clearly distinguishable dilution gradients (3× to 81×).

8. Post-Run Handling

- Allow plated starch plates to dry for 10–15 minutes before incubation.
- Seal and incubate at 42 °C under 5% CO₂ and continuous light (~100 µmol photons m⁻² s⁻¹).
- Discard tips and clean OT-2 deck with 70% ethanol after completion.

# For Colony PCR Screening with Duplicate Reactions

*C. merolae* Colony PCR Protocol
Protocol Name: PCR Colony Picks with Replication
OT-2 Script: ColonyPCR.py (Opentrons API v2.19)
Custom Labware: abgenepcr_96_wellplate_200ul.json
Purpose: Automate the assembly of colony PCR reactions from a plate of colony picks, splitting each pick into two reactions so that every transformant is screened with a left-junction and a right-junction primer pair in the same run. Output is one or two Abgene 96-well PCR plates ready for thermocycling.

1. Overview

This protocol is executed after colony picking, and follows the same group layout as the "PEG4000 transformation" protocol. Colony picks in the source plate are divided into groups of three columns, and each group is screened with its own Left and Right primer-pair mastermix. Each colony therefore produces two 10 µL reactions.

| Transformation group | Source columns | Mastermix columns | Destination |
|----------------------|----------------|-------------------|-------------|
| Group 1 | 1–3 | 1 (Left), 2 (Right) | Plate 1, columns 1–3 and 4–6 |
| Group 2 | 4–6 | 3 (Left), 4 (Right) | Plate 1, columns 7–9 and 10–12 |
| Group 3 | 7–9 | 5 (Left), 6 (Right) | Plate 2, columns 1–3 and 4–6 |
| Group 4 | 10–12 | 7 (Left), 8 (Right) | Plate 2, columns 7–9 and 10–12 |

2. Run Parameters

The number of groups is selected in the Opentrons App before the run. Two groups fill one destination plate, so the group count also sets how much labware goes on the deck:

| Groups | Source columns used | Destination plates | Tip racks | Reactions |
|:------:|:-------------------:|:------------------:|:---------:|:---------:|
| 1 | 1–3 | 1 (slot 3, half filled) | 1 (slot 1) | 48 |
| 2 | 1–6 | 1 (slot 3, full) | 1 (slot 1) | 96 |
| 3 | 1–9 | 2 (slots 3 and 5) | 2 (slots 1 and 4) | 144 |
| 4 | 1–12 | 2 (slots 3 and 5) | 2 (slots 1 and 4) | 192 |

Each group consumes five tip columns — three for cells, two for mastermix — so the second tip rack is only loaded from three groups onward. Slots 4 and 5 are left empty below that, and the protocol does not ask for them to be calibrated.

3. OT-2 Setup

| Slot | Labware / Module | Description |
|------|------------------|-------------|
| 1 | `opentrons_96_tiprack_20ul` | Tip rack #1 (P20) |
| 2 | `biorad_96_wellplate_200ul_pcr` | Source plate — colony picks |
| 3 | `abgenepcr_96_wellplate_200ul` | Destination plate #1 (custom labware) |
| 4 | `opentrons_96_tiprack_20ul` | Tip rack #2 (P20) — three or four groups only |
| 5 | `abgenepcr_96_wellplate_200ul` | Destination plate #2 — three or four groups only |
| 6 | `biorad_96_wellplate_200ul_pcr` | Mastermix plate — two columns per group |
| — | `p20_multi_gen2` (left mount) | All liquid handling |

Hardware Requirements

Opentrons OT-2 (API v2.19+) – Automated reaction assembly
P20 Multi GEN2 (left mount) – Cell and mastermix transfers
Tip Racks 20 µL (×1 or ×2, Slots 1 and 4) – Five tip columns per group
Bio-Rad PCR Plate (Slot 2) – Colony picks resuspended in water or MA2G
Bio-Rad PCR Plate (Slot 6) – Primer-pair mastermixes, two columns per group
Abgene PCR Plates (×1 or ×2, Slots 3 and 5) – Destination reaction plates
Thermocycler – Downstream, off-deck

4. Custom Labware Installation

The Abgene destination plates are not part of the Opentrons default library and must be added before the protocol will load.

  1. Download `abgenepcr_96_wellplate_200ul.json` from this repository.
  2. In the Opentrons App, go to Labware → Import, and select the JSON file.
  3. Confirm the entry "Abgene PCR 96 Well Plate 200 µL" appears in the custom labware list.
  4. Calibrate the labware in slot 3, and in slot 5 as well if running three or four groups, before the first run.

The definition describes a 96-well V-bottom plate, 200 µL per well, 20.5 mm well depth. The `loadName` inside the JSON is `abgenepcr_96_wellplate_200ul`, which is the string the protocol calls — renaming the file does not change it.

5. Reagent and Sample Preparation (Manual)

Source plate (slot 2)

- Pick single colonies from selective starch plates into the corresponding well of the Bio-Rad plate, filling three columns per group from column 1 onward.
- Resuspend each pick in 50 µL of nuclease-free water. The protocol mixes 5 × 10 µL before aspirating, so wells must hold at least 30 µL.
- Keep the plate on ice or at room temperature until the run starts.

Mastermix plate (slot 6)

- Prepare two PCR mastermixes per group at 1.11× concentration, so that 9 µL plus 1 µL of cell suspension gives a 10 µL reaction at 1×.
- Load each mastermix across all eight wells of one column, 35–40 µL per well. Each column is aspirated three times at 9 µL, so 27 µL per well is consumed and the remainder covers dead volume.
- Fill only the columns the selected group count uses; the rest stay empty.

| Mastermix column | Contents | Destination |
|------------------|----------|-------------|
| 1 | Group 1 — Left homology primer pair | Plate 1, columns 1–3 |
| 2 | Group 1 — Right homology primer pair | Plate 1, columns 4–6 |
| 3 | Group 2 — Left homology primer pair | Plate 1, columns 7–9 |
| 4 | Group 2 — Right homology primer pair | Plate 1, columns 10–12 |
| 5 | Group 3 — Left homology primer pair | Plate 2, columns 1–3 |
| 6 | Group 3 — Right homology primer pair | Plate 2, columns 4–6 |
| 7 | Group 4 — Left homology primer pair | Plate 2, columns 7–9 |
| 8 | Group 4 — Right homology primer pair | Plate 2, columns 10–12 |

6. What the Protocol Does (Automated Steps)

All cells are dispensed first, into the empty destination wells, and the mastermix is added on top afterwards. The tip serving a source column visits two destination columns that carry different mastermixes, so cells cannot be dispensed into mastermix without carrying one primer pair into the other's wells. That is why the order is fixed.

  1. Cell distribution — for each source column in the selected groups:
   - Mix 5 × 10 µL at 1 mm from the well bottom to resuspend the pick.
   - Aspirate 2 µL at 1 mm from the bottom.
   - Dispense 1 µL into the first destination column, at 0.1 mm from the bottom.
   - Dispense 1 µL into the paired destination column, at 0.1 mm from the bottom.
   - Drop the tip. One tip column per source column, three per group.
  2. Mastermix distribution — for each mastermix in the selected groups:
   - Pick up one tip.
   - Aspirate 9 µL and dispense into each of its three destination columns at 12 mm from the bottom, so the tip never touches the cell droplet.
   - Blow out twice and touch tip after each dispense.
   - Drop the tip. One tip column per mastermix, two per group.

Final reaction volume is 10 µL: 9 µL mastermix plus 1 µL cell suspension.

7. Expected Layout and Volumes

| Item | Value |
|------|-------|
| Colony picks processed | 24 per group |
| Reactions assembled | 48 per group (2 per colony) |
| Reaction volume | 10 µL |
| Cell suspension per reaction | 1 µL |
| Mastermix per reaction | 9 µL |
| Mastermix consumed per column | 27 µL per well |
| Tip columns consumed | 5 per group (3 cells + 2 mastermix) |

8. Running the OT-2 Protocol

  1. Load the deck as in Section 3, leaving out the labware the selected group count does not use.
  2. Confirm that the custom labware is imported and calibrated for the destination slots in use.
  3. In the Opentrons App, select Number of Groups (`group_count`, default 4, max 4).
  4. Load the mastermix plate last, immediately before starting, to limit time at room temperature.
  5. Start the run. Tip racks must be full at the start.

Cells sit as exposed 1 µL droplets until the mastermix step reaches their column, which at four groups is several minutes after the first colonies are dispensed. If evaporation is a concern, run fewer groups per batch or keep the destination plate on a chilled block.

9. Post-Run Handling

- Seal the destination plates, spin down briefly to collect the reactions and remove bubbles.
- Transfer to the thermocycler and run the cycling program for the primer pairs in use.
- A left-junction and a right-junction product for the same colony indicates integration at the intended locus; a single product indicates one-sided integration or a non-specific product.
- Analyse by gel electrophoresis, keeping the plate map from Section 1 to trace each well back to its colony.
