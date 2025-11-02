# ot2-cmerolae-pipeline
This repository contains Python protocols for the Opentrons OT-2 liquid handler automating Cyanidioschyzon merolae nuclear transformations. The workflow includes automated starch-bed pouring with real-time Z-offset calibration, PEG-mediated transformation routines, and colony plating compatible with the PIXL picker.

All labware needs to be first calibrated using Opentrons software

# For PEG4000 transformation

Protocol Name: Transformation_C_merolae_with_PEG4000.py
1. OT-2 Setup

| Slot | Labware / Module | Description |
|------|------------------|-------------|
| 1 | `opentrons_96_tiprack_200ul` | Tip rack for P300 |
| 2 | `biorad_96_wellplate_200ul_pcr` | Transformation plate |
| 5 | `heaterShakerModuleV1` + `2mL_deepwell_plate` | PEG mixing and incubation |
| — | `P300_single_gen2` (right mount) | For all liquid handling |

Hardware Requirements

Opentrons OT-2 (API v2.19+) – Main automation platform
P300 Single GEN2 (right mount) – Pipetting transformation reagents
Heater-Shaker Module V1 (Slot 5) – PEG incubation/mixing
2 mL Deep-Well Plate (on module, slot 5) – MA2G medium for recovery
Tip Rack 200 µL (Slot 1) – Transformation pipetting
Bio-Rad PCR Plate (Slot 2) – Reaction plate for transformation
- In the Opentrons app, select the number of groups to transform (1–4).
  - Each group corresponds to a set of three columns:
    - Group 1: columns 1–3
    - Group 2: columns 4–6
    - Group 3: columns 7–9
    - Group 4: columns 10–12

2. Reagent Preparation and Manual Assembly (PCR Plate)

- Pellet the cells in OD~ 0.6 to 0.8 by centrifugation at 2000 × g for 10 minutes.
- Carefully save the supernatant to prepare MA2G-C later, if needed.
- Resuspend the cell pellet in 1 mL of 1X MA I medium.
- Spin down again and resuspend the entire pellet in a final volume of 200 µL of 1X MA I.
- Dispense 25 µL of the resuspended cells into the first column of each group.
- Cover the plate with parafilm and incubate at room temperature or in a 42°C incubator until ready to proceed.

- In the third column of each group, add 200 µL of PEG4000 (0.9g of PEG4000 in 750uL of MA-I) solution diluted in 1X MA I.

- In the second column of each group, prepare the transformation mix as follows (final volume: 100 µL):
  - 1 pmol of target DNA
  - 6 µL of salmon sperm DNA
  - 10 µL of 10X MA I
  - Add nuclease-free water to reach 100 µL total volume.

3. Dilution Reservoir Setup

- Assemble the heater-shaker module with the metal adapter and a 2 mL deep-well plate in position 5.
- Add 1 mL of MA2G medium to each well in the first column of the deep-well plate: position 1 for group 1, position 4 for group 2, position 7 for group 3, and position 10 for group


4. Running the OT-2 Protocol

- Load the prepared plate onto the OT-2 deck.
- Select the appropriate number of groups in the Opentrons app.
- Start the protocol. The OT-2 will handle mixing and incubation steps for the transformation reaction.

5. Post-Transformation Handling

- Once the OT-2 protocol is complete, transfer the entire contents from each first column (per group) to individual flask for each well used containing 49 mL of MA2G medium pre-warmed to 42°C.
- Continue incubation as required for recovery or proceed with plating on selective media.


# For 3X Cell Dilution
Protocol Name: 3X cell dilutions.py
OT-2 Script: 3X cell dilutions.py (Opentrons API v2.19)
Purpose: Perform automated 3× serial dilutions of three transformants per 96-well plate (rows A/E/I; columns grouped 1–4, 5–8, 9–12) across up to 7 plates. The method pre-loads diluent to destination wells, then transfers a fixed volume forward to achieve ~3× dilution at each step.
1. OT-2 Setup

| Slot | Labware / Module | Description |
|------|------------------|-------------|
| 1 | `opentrons_96_tiprack_300ul` | Tip rack 1 |
| 2 | `opentrons_96_tiprack_300ul` | Tip rack 2 |
| 3–9 | `corning_96_wellplate_360ul_flat` | Source/destination plates (up to 7) |
| 11 | `axygen_1_reservoir_90ml` | Diluent reservoir |
| — | `p300_multi_gen2` (right mount) | For dilution transfers |

> **Deck layout guidance:** Three dilution series per plate start at columns 1, 5, and 9 — spanning four columns per series (1→4, 5→8, 9→12).


Hardware Requirements

Opentrons OT-2 (API v2.19+) – Automated liquid handling
P300 Multi GEN2 (right mount) – Perform serial dilutions
Tip Rack 300 µL (×2, Slots 1–2) – For dilution steps
96-well Plates (Slots 3–9) – Dilution sequence plates
Reservoir 90 mL (Slot 11) – Contains MA2G-C or other diluent

2. Reagent & Sample Preparation (Manual)

  1. Prepare diluent (e.g., MA2G-C) and load A1 of the reservoir (slot 11).
  2. Prepare cells: After 48 h recovery, resuspend each C. merolae transformant in 2.7 mL of MA2G-C (or as per your culture SOP).
  3. Plate loading (starting wells):
   - For each plate in use, pipette 200 µL of transformant into A1, A5, A9 (start wells for the three series).


3. What the Protocol Does (Automated Steps)

The script performs a 4-column, 3-step 3× dilution for three series per plate:
- Diluent pre-load: Adds 133 µL diluent to all destination wells in each series, skipping the first column.
- Serial transfers: Moves 67 µL from the current well to the next well, then mixes in the destination (3×100 µL).
- Dilution math: 67 µL sample + 133 µL diluent = 200 µL total → ~3× dilution.
- Series layout: 1→4, 5→8, 9→12 per plate.
- Plates processed: Up to 7, selected via parameter plate_count in the protocol.

4. Running the OT-2 Protocol

  1. Load labware to the deck as in Section 1.
  2. In the Opentrons App, select Number of plates (plate_count, default 2, max 7).
  3. Place starting samples (200 µL) in A1, A5, A9 of each plate.
  4. Start the run. The robot will:
   - Pre-fill destination wells with 133 µL diluent.
   - Execute three forward transfers of 67 µL per series with mixing after each transfer.
  5. At completion, the app will display “Protocol complete! 3X dilutions performed for all plates, three series per plate.”

5. Expected Layout & Volumes

For each plate (row A with multichannel):
| Series | Columns | Start vol (µL) | Diluent pre-load (µL) | Transfer (µL) | Final vol (µL) | Fold |
|:------:|:--------:|:--------------:|:---------------------:|:--------------:|:---------------:|:----:|
| 1 | 1–4 | 200 | 133 | 67 | 200 | ~3× |
| 2 | 5–8 | 200 | 133 | 67 | 200 | ~3× |
| 3 | 9–12 | 200 | 133 | 67 | 200 | ~3× |


6. Post-Run Handling

- Seal plates or proceed to downstream steps (plating, OD measurement, screening).
- For plating, maintain consistent pipetting heights and mixing.

# For Starch Bed plating in Gellan Gum
C. merolae Starch-Bed Pouring Protocol
Protocol Name: Starch Solution Dispensing with Z-Offset Adjustment
OT-2 Script: Startch plating.py (Opentrons API v2.19)
Purpose: Automate the pouring of starch-based plating medium across up to 8 plates using plate-weight–dependent Z-axis height calibration. This ensures even distribution and prevents premature solidification due to the high viscosity and fast-gelling nature of starch-gellan mixtures.

1.OT-2 Setup

| Slot | Labware / Module | Description |
|------|------------------|-------------|
| 1 | `heaterShakerModuleV1` + `agilent_1_reservoir_290ml` | Contains 25 mL 20% starch solution |
| 3, 5–11 | `corning_96_wellplate_360ul_flat` | Destination plates (up to 8) |
| 4 | `opentrons_96_tiprack_20ul` | Tip rack |
| — | `p20_multi_gen2` (left mount) | Dispensing starch |
| — | HEPA Filter Attachment | Turn ON during pouring |


Hardware Requirements

Opentrons OT-2 (API v2.19+) – Automated dispensing
Heater-Shaker Module V1 (Slot 1) – Keeps starch homogeneous
P20 Multi GEN2 (left mount) – Dispenses 10 µL per column pair
Tip Rack 20 µL (Slot 4) – Dispensing tips
290 mL Reservoir (on heater-shaker, slot 1) – Contains starch-gellan mix
96-well Plates (×8, Slots 3, 5–11) – Pouring destinations
HEPA Filter Unit – Dry spots faster



2. Preparation of Gellan Gum

- Dissolve 3.5 g of Gellan Gum in 584.5 mL of distilled water.
- Autoclave the solution to sterilize it completely.

3. Preparation of 3× MA2G

Refer to “Stock solutions preparation.docx” for detailed stock recipes.
Combine the following components:
- Solution I: 58.5 mL
- Solution II: 5.850 mL
- Solution III: 0.585 mL
- Solution IV: 2.330 mL
- Glycerol (37.5%): 7.6 mL
- Distilled water: 100 mL
Filter sterilize the final mixture before use.

4. Preparation of MA2G-C

  1. In a vented culture flask with MA2G medium, dilute *C. merolae* cells to OD 0.2 and incubate overnight at 42 °C, 5% CO₂, under continuous light   (~100 µmol photons m⁻² s⁻¹).
  2. Once the culture reaches OD ~0.8, harvest cells by centrifugation at 2,000 × g for 10 minutes at room temperature.
  3. Collect the supernatant, filter-sterilize using a 0.22 µm filter, and store at room temperature.

5. Starch Preparation

  1. In a 50 mL Falcon tube, add starch to the 30 mL mark.
  2. Add water up to 45 mL and vortex thoroughly.
  3. Centrifuge at 5,000 rpm for 30 seconds and discard supernatant.
  4. Repeat washing twice with water.
  5. Wash once with 75% ethanol, discard the supernatant.
  6. Add ethanol to yield a 50% slurry and store at 4 °C.
  7. Before use, vortex the 50% slurry and take 10 mL.
  8. Repeat two water washes (centrifuge at 5,000 rpm for 30 s each) and discard the supernatant.
  9. Resuspend to a final volume of 25 mL in MA2G-C.

6. Pre-Incubation Step

Before pouring, incubate both the autoclaved Gellan Gum and the sterile 3× MA2G solutions at 42 °C for at least one hour. This prevents the Gellan Gum from solidifying too quickly when mixed.

7. Plate Preparation

- Prepare the number of plates you wish to pour in advance. The amounts above make up to ~14 plates.
- If using chloramphenicol as antibiotic, add 1.9 mL of 100 mg/mL in ethanol stock to the 3× MA2G and homogenize.
- Mix the warmed Gellan Gum and 3× MA2G thoroughly.
- Using a sterile 50 mL Falcon tube, aliquot ~50 mL and pour into each plate inside a biosafety cabinet.
- After solidification, weigh each plate and label the lid with the plate weight.


8. Parameters and Calibration

Each plate’s weight (g) is recorded before the run and entered in the OT-2 interface. 
The protocol converts plate weight into a Z-offset using:
    Z_offset_adjusted = (Plate_weight) / (10,567.2 × 0.001028)
Each calculated Z-offset compensates for height variation from plate-to-plate, ensuring precise pipetting depth.

9. Automated Steps

  1. The heater-shaker is engaged to mix the starch solution (2,000 rpm for 10 s).
  2. The OT-2 picks up a 20 µL tip.
  3. For each plate:
   - Aspirate 20 µL of starch from the reservoir (A1).
   - Dispense 10 µL into two adjacent columns per step (columns 1–2, 3–4, etc.), using that plate’s Z-offset.
   - After every three dispensing cycles (6 columns total), the heater-shaker mixes again (2,000 rpm, 10 s).
   - Drop the tip after finishing the plate.
  4. Before proceeding to the next plate, the heater-shaker repeats the mixing step to prevent settling.

10. Running the OT-2 Protocol

  1. Load the heater-shaker with the starch reservoir, close the latch, and confirm placement.
  2. Load the destination plates (up to 8) in slots 3, 5–11.
  3. Enter plate weights under “Run Parameters.”
  4. Confirm pipette calibration and shaking settings.
  5. Start the run. The OT-2 will automatically dispense starch with plate-specific Z-offset adjustments.
  6. After 8 plates, refill the reservoir to 25 mL before restarting the next batch.

11. Expected Results

- Each well pair receives 20 µL total (10 µL per column).
- The starch surface should appear uniform and centered.
- Z-offset calibration compensates for varying plate heights, preventing overflow or shallow deposition.

12. Post-Run Handling

- Allow plates to cool and solidify on a level surface for 10 minutes.

# Cell Plating on Starch
C. merolae Cell Plating on Starch Protocol 
Protocol Name: Cell Plating on Starch
OT-2 Script: CellPlatingOnStartch.py (Opentrons API v2.19)
Purpose: This protocol automates the plating of diluted *Cyanidioschyzon merolae* cells onto starch-containing solid media plates following the “3X Cell Dilution Protocol.” 
The script uses weight-based Z-offset calibration to ensure even plating height across up to six destination plates.

1. Overview

This protocol is executed immediately after the “3X Cell Dilution Protocol.”
The diluted *C. merolae* cultures should be positioned in slots 3 and 4 of the OT-2 deck. These serve as source plates for automated plating onto starch media plates located in slots 5–10.

2. OT-2 Setup

| Slot | Labware / Module | Description |
|------|------------------|-------------|
| 1 | `opentrons_96_tiprack_20ul` | Tip rack #1 (P20) |
| 2 | `opentrons_96_tiprack_20ul` | Tip rack #2 (backup) |
| 3 | `corning_96_wellplate_360ul_flat` | Source plate #1 (diluted cells) |
| 4 | `corning_96_wellplate_360ul_flat` | Source plate #2 (optional) |
| 5–7 | `corning_96_wellplate_360ul_flat` | Destination plates (for source 3) |
| 8–10 | `corning_96_wellplate_360ul_flat` | Destination plates (for source 4) |
| 11 | `opentrons_96_tiprack_200ul` | Tip rack for P300 mixing |
| — | `p20_multi_gen2` (left mount) | Dispensing cell aliquots |
| — | `p300_multi_gen2` (right mount) | Mixing before plating |



Hardware Requirements

Opentrons OT-2 (API v2.19+) – Automated plating
P20 Multi GEN2 (left mount) – Dispensing diluted cells
P300 Multi GEN2 (right mount) – Mixing source wells
Tip Racks 20 µL (×2, Slots 1–2) – For plating transfers
Tip Rack 200 µL (Slot 11) – For P300 mixing
Source Plates (×2, Slots 3–4) – Diluted cells
Destination Plates (×6, Slots 5–10) – Starch plating



3. Parameters and Z-Offset Calibration

Before execution, specify the following in the Opentrons App:
- Number of destination starch plates (3 or 6)
- Number of dilution plates (1 or 2; slots 3 and 4)
- Weight of each starch plate (g) for Z-offset calibration

Each Z-offset is calculated as:
    Z_offset_adjusted = (Plate_weight) / (10,567.2 × 0.001028)

Offsets ensure consistent pipetting height across plates poured with variable starch-bed thickness.

4. Automated Plating Steps

  1. The robot loads source plates (diluted cells) and destination starch plates according to selected parameters.
  2. Each dilution plate is processed independently:
   - The first dilution plate (slot 3) corresponds to starch plates in slots 5–7.
   - The second dilution plate (slot 4) corresponds to starch plates in slots 8–10.
  3. Mixing and transfer are handled in structured column groups:
   - Columns A1–A4 → first starch plate (slot 5 or 8)
   - Columns A5–A8 → second starch plate (slot 6 or 9)
   - Columns A9–A12 → third starch plate (slot 7 or 10)
  4. The P300 multi-channel pipette resuspend before transfers.
  5. The P20 multi-channel pipette aspirates and dispenses 10 µL aliquots from each source well into specific destination wells at the corresponding    Z-offset.
  6. The process repeats for all plates, using fresh tips for each batch.

5. Dilution Mapping and Layout

Column-to-dilution mapping follows standard plating scheme:

| Columns | Dilution Factor |
|----------|-----------------|
| 1 | Negative control (untransformed cells, pipetted manually)|
| 2–3 | 81× dilution |
| 4–6 | 27× dilution |
| 7–9 | 9× dilution |
| 10–12 | 3× dilution |

Each destination plate receives the full dilution range from its respective source plate.

6. Customizing Plate Count

Users can define the number of destination plates (3 or 6). 
The script automatically assigns plating destinations to ensure balanced use of source material. 
If only one dilution plate is used, the robot processes starch plates in slots 5–7 only.

7. Expected Results

- Even distribution of cell spots across all destination plates.
- Uniform Z-height for deposition, minimizing pipette contact with starch surface.
- Clearly distinguishable dilution gradients (3× to 81×).

8. Post-Run Handling

- Allow plated starch plates to dry for 10–15 minutes before incubation.
- Seal and incubate at 42°C under 5% CO₂ and continuous light (~100 µmol photons m⁻² s⁻¹).
- Discard tips and clean OT-2 deck with 70% ethanol after completion.



