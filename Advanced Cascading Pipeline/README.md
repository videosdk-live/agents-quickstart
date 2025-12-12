# Advanced Cascading Pipeline

This Example showcases an advanced cascading pipeline with enhanced features for End-of-Utterance (EOU) handling, improved interruption detection, interruptible speech support, and false-interruption handling.

## Features

### 1. Enhanced End-of-Utterance (EOU) Handling

The pipeline offers flexible EOU handling to accurately determine when a user has finished speaking.

**Modes:**
- **Default:** Utilizes fixed `min_speech_wait_timeout` or `max_speech_wait_timeout` thresholds based on EOU probability.
- **Adaptive:** Dynamically computes a delay timeout using a proportional scale derived from confidence scores, bounded by `min_speech_wait_timeout` and `max_speech_wait_timeout`.

**Parameters:**
- `min_max_speech_wait_timeout`: A tuple `(min_speech_wait_timeout, max_speech_wait_timeout)` specifying:
    - `min_speech_wait_timeout`: Minimum duration to wait for additional speech before determining the user has finished speaking.
    - `max_speech_wait_timeout`: Maximum duration to wait for additional speech, after which the user turn is forcibly ended, regardless of confidence scores.

**Usage Example:**

```python
pipeline = CascadingPipeline(
    # ...
    eou_config=EOUConfig(
        mode='ADAPTIVE',
        min_max_speech_wait_timeout=[0.5, 0.8],
    )
    # ...
)
```

### 2. Improved Interruption Detection (VAD + STT Combined)

Introduces new modes for more granular control over interruption detection, combining Voice Activity Detection (VAD) and Speech-to-Text (STT).

**Modes:**
- **HYBRID:** Combines both VAD and STT for interruption detection.
- **VAD_ONLY:** Relies solely on Voice Activity Detection for interruptions.
- **STT_ONLY:** Relies solely on Speech-to-Text for interruptions.

**Parameters:**
- `min_interruption_duration`: Triggers an interruption if the user speaks continuously for this specified duration.
- `min_interruption_words`: Triggers an interruption if the Automatic Speech Recognition (ASR) transcribes at least this number of words.

**Usage Example:**

```python
pipeline = CascadingPipeline(
    # ...
    interrupt_config=InterruptConfig(
        mode="HYBRID",
        interrupt_min_duration=0.2,
        interrupt_min_words=2
    )
    # ...
)
```

### 3. Interruptible Speech Support

The `say()` and `reply()` methods now accept an `interruptible` flag, providing control over agent speech interruptions.

**`interruptible` flag:**
- `True` (default): Allows users to interrupt the agent's speech.
- `False`: Makes the agent's speech non-interruptible.

**Usage Example:**

```python
await self.session.say("This message can be interrupted.", interruptible=True)
await self.session.say("This message cannot be interrupted.", interruptible=False)
```

### 4. False-Interruption Handling

Introduces a mechanism to detect and gracefully handle brief or accidental user sounds, preventing premature interruptions.

**Parameters:**
- `false_interrupt_pause_duration`: The duration of time used to detect accidental/false interruptions. If the user does not continue speaking within this timeout, the agent resumes speaking.
- `resume_on_false_interrupt`: A boolean flag determining whether the agent should automatically resume TTS after a smart pause timeout when no real interruption occurred.

**Usage Example:**

```python
pipeline = CascadingPipeline(
    # ...
    interrupt_config=InterruptConfig(
        # ...
        false_interrupt_pause_duration=2.0,
        resume_on_false_interrupt=True,
        # ...
    )
    # ...
)
```

## Running the Example

To run the advanced cascading pipeline example, execute the `advanced_cascading_pipeline.py` script:

```bash
python advanced_cascading_pipeline.py
```
