# Namo Turn Detector

The Namo Turn Detector v1 utilizes a custom fine-tuned model from VideoSDK to accurately determine whether a user has finished speaking. This allows for precise management of conversation flow, especially in cascading pipeline setups. It can operate as a multilingual model or be configured for a specific language for optimized performance.

## Get Started

1. Add .env variables

```bash
DEEPGRAM_API_KEY=""
ELEVENLABS_API_KEY=""
OPENAI_API_KEY=""
VIDEOSDK_AUTH_TOKEN=""
```

2. Create the environment

- On MacOS/Linux

```bash
python3 -m venv .venv
```

- On Windows

Next, Activate it! Command differ based on your environment

```bash
source .venv/bin/activate
```

3. Installation Dependencies

```bash
python -m pip install -r requirements.txt
```

4. Run Agent Worker

```bash
python main.py
```

## Working - NAMO TURN DETECTOR

## Importing

```python
from videosdk.plugins.turn_detector import NamoTurnDetectorV1
```

## Example Usage

**1. For a specific language (e.g., English):**

```python
from videosdk.plugins.turn_detector import NamoTurnDetectorV1, pre_download_namo_turn_v1_model
from videosdk.agents import CascadingPipeline

# Pre-download the English model to avoid delays
pre_download_namo_turn_v1_model(language="en")

# Initialize the Turn Detector for English
turn_detector = NamoTurnDetectorV1(
  language="en",
  threshold=0.7
)

# Add the Turn Detector to a cascading pipeline
pipeline = CascadingPipeline(turn_detector=turn_detector)
```

**2. For multilingual support:**

If you don't specify a language, the detector will default to the multilingual model, which can handle various languages.

```python
from videosdk.plugins.turn_detector import NamoTurnDetectorV1, pre_download_namo_turn_v1_model
from videosdk.agents import CascadingPipeline

# Pre-download the multilingual model
pre_download_namo_turn_v1_model()

# Initialize the multilingual Turn Detector
turn_detector = NamoTurnDetectorV1(
    threshold=0.7
)

# Add the Turn Detector to a cascading pipeline
pipeline = CascadingPipeline(turn_detector=turn_detector)
```

## Configuration Options

- `language`: (Optional, `str`): Specifies the language for the turn detection model. If left as `None` (the default), it loads a multilingual model capable of handling all supported languages.

- `threshold`: (float) Confidence threshold for turn completion detection (0.0 to 1.0, default: `0.7`)

## Supported Languages

The `NamoTurnDetectorV1` supports a wide range of languages when you specify the corresponding language code. If no language is specified, the multilingual model will be used.

Here is a list of the supported languages and their codes:

| Language   | Code |
| :--------- | :--- |
| Arabic     | `ar` |
| Bengali    | `bn` |
| Chinese    | `zh` |
| Danish     | `da` |
| Dutch      | `nl` |
| English    | `en` |
| Finnish    | `fi` |
| French     | `fr` |
| German     | `de` |
| Hindi      | `hi` |
| Indonesian | `id` |
| Italian    | `it` |
| Japanese   | `ja` |
| Korean     | `ko` |
| Marathi    | `mr` |
| Norwegian  | `no` |
| Polish     | `pl` |
| Portuguese | `pt` |
| Russian    | `ru` |
| Spanish    | `es` |
| Turkish    | `tr` |
| Ukrainian  | `uk` |
| Vietnamese | `vi` |

## Pre-downloading Model

To avoid delays during agent initialization, you can pre-download the Hugging Face model:

You can pre-download a specific language model:

```python
from videosdk.plugins.turn_detector import pre_download_namo_turn_v1_model

# Download the English model before the agent runs
pre_download_namo_turn_v1_model(language="en")
```

Or pre-download the multilingual model:

```python
from videosdk.plugins.turn_detector import pre_download_namo_turn_v1_model

# Download the multilingual model
pre_download_namo_turn_v1_model()
```
