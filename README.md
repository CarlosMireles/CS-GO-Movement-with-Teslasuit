# TeslaSuit CS:GO Motion Control

This project creates a bridge between the Teslasuit full-body haptic VR suit and Counter-Strike: Global Offensive (CS:GO), allowing players to control in-game movements through real-world body motions. Using machine learning, the system recognizes specific body poses and translates them into game commands.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [File Structure](#file-structure)
- [Motion Poses](#motion-poses)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [License](#license)

## Overview

The TeslaSuit CS:GO Motion Control project creates an immersive gaming experience by allowing players to control their in-game character using natural body movements. The system uses machine learning to recognize specific poses and translates them into game commands, enabling a more intuitive and engaging way to play CS:GO.

## Features

- **Motion-based game control**: Control your CS:GO character using real-world body movements
- **Machine learning pose recognition**: Uses Random Forest algorithm to classify body positions
- **Real-time processing**: Continuously monitors body position and sends commands to the game
- **Customizable pose set**: Includes predefined poses for common game actions
- **Telnet integration**: Connects directly to CS:GO's console via Telnet
- **Full TeslaSuit integration**: Takes advantage of the suit's motion capture capabilities

## System Requirements

- **Python 3.10+**
- **TeslaSuit and associated hardware**
- **Counter-Strike: Global Offensive**
- **TeslaSuit SDK Python API**
- **Libraries**: 
  - numpy
  - scikit-learn
  - telnetlib3
  - asyncio

## Installation

1. **Install required Python libraries**:
   ```bash
   pip install numpy scikit-learn telnetlib3 asyncio
   ```

2. **Set up TeslaSuit SDK**:
   - Install the TeslaSuit SDK from the official website
   - Set the environment variable for the Python API path:
   ```bash
   export TESLASUIT_PYTHON_API_PATH="/path/to/teslasuit_sdk"
   ```

3. **Configure CS:GO for Telnet**:
   - Add the launch parameter `-netconport 2121` to CS:GO
   - This allows the game to accept commands via Telnet on port 2121

4. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/teslasuit-csgo-control.git
   cd teslasuit-csgo-control
   ```

## Usage

1. **Connect your TeslaSuit** and ensure it's properly calibrated.

2. **Launch CS:GO** with the Telnet parameter:
   ```
   -netconport 2121
   ```

3. **Run the main script**:
   ```bash
   python main.py
   ```

4. **Training phase**:
   - The system will guide you through a series of poses
   - Follow the on-screen instructions to assume each pose
   - Hold each pose for a few seconds while the system collects data

5. **Gameplay phase**:
   - After training, the system will begin translating your movements into game commands
   - Move naturally according to the trained poses to control your character

## How It Works

The system operates in two main phases:

### 1. Training Phase
1. Connects to the TeslaSuit and CS:GO
2. Guides the user through a series of poses (forward, backward, turn left, etc.)
3. Collects skeletal data for each pose
4. Trains a Random Forest classifier on the collected data

### 2. Real-time Control Phase
1. Continuously collects skeletal data from the TeslaSuit
2. Processes the data through the trained classifier
3. Predicts which pose the user is currently making
4. Sends the corresponding command to CS:GO via Telnet
5. Provides real-time feedback on detected poses

## File Structure

- **`main.py`**: Entry point that initializes the TeslaSuit connection and launches the application
- **`LoadTeslaSuit.py`**: Handles connection to the TeslaSuit and provides access to its sensors
- **`BoneStructureLoader.py`**: Manages the skeletal data from the TeslaSuit
- **`CSControl.py`**: Handles Telnet communication with CS:GO
- **`BodyMovementRandomForestClassifier.py`**: Core ML component that trains on and recognizes poses

## Motion Poses

The system recognizes the following poses by default:

| Pose | In-Game Action |
|------|----------------|
| `avanzar` | Move forward |
| `retroceder` | Move backward |
| `girar_izquierda` | Turn left |
| `girar_derecha` | Turn right |
| `disparar` | Shoot |
| `apuntar` | Aim/Zoom |
| `neutral` | No action |

Additional poses (`agacharse` - crouch, `saltar` - jump) are implemented in the code but commented out in the default training set.

## Troubleshooting

### Common Issues

**"No se puede obtener los datos del esqueleto"**
- Ensure the TeslaSuit is properly connected and calibrated
- Check that the TeslaSuit SDK is correctly installed

**"No se pudo conectar a CS:GO"**
- Verify CS:GO is running with the `-netconport 2121` launch parameter
- Check if another application is using port 2121

**Poor pose recognition**
- Try retraining the system with more exaggerated poses
- Ensure good lighting conditions for optimal TeslaSuit tracking
- Make sure poses are distinct from one another

### Debugging

The `BoneStructureLoader` class includes a `debug_print` method that can be used to troubleshoot skeletal data issues. Uncomment debug prints in the code for more detailed logging.

## License

[MIT License](LICENSE)

## Acknowledgements

- TeslaSuit for their SDK and hardware
- Valve for CS:GO console functionality
- The scikit-learn team for their machine learning tools

---

Created by Carlos Mireles Rodríguez - carlosmirelesrodriguez1@gmail.com
