# src/autoclean/tasks/template_task.py
"""Template for implementing new EEG processing tasks.

This template provides a starting point for implementing new EEG processing tasks.
It includes detailed documentation and examples for each required component.

Task Implementation Guide:
1. Copy this template to create your new task file (e.g., my_paradigm.py)
2. Replace TemplateTask with your task name (e.g., MyParadigmTask)
3. Implement the required methods

Key Components:
1. Task Configuration:
   - Define processing steps in autoclean_config.yaml
   - Each step has enabled/disabled flag and parameters
   - Configure artifact rejection policies
   
2. Required Methods:
   - __init__: Initialize task state
   - run: Main processing pipeline
   - _generate_reports: Create quality control visualizations
   - _validate_task_config: Validate task settings

3. Processing Flow:
   a. Data Import:
      - Load raw EEG data
      - Apply montage
      - Basic validation
   b. Preprocessing:
      - Resampling
      - Filtering
      - Bad channel detection
   c. Artifact Rejection:
      - ICA decomposition
      - Component classification
      - Bad segment detection
   d. Task-Specific Processing:
      - Epoching
      - Baseline correction
      - Additional analyses
   e. Quality Control:
      - Generate reports
      - Save processed data
      - Update processing log

4. Best Practices:
   - Use type hints for all methods
   - Add comprehensive docstrings
   - Include error handling
   - Log processing steps
   - Save intermediate results
   - Generate quality control reports
"""

# Standard library imports
from pathlib import Path
from typing import Any, Dict, Optional

# Third-party imports
import mne
import numpy as np
import matplotlib.pyplot as plt

# Local imports
from autoclean.core.task import Task
from autoclean.step_functions.continuous import (
    step_create_bids_path,
    step_pre_pipeline_processing,
    step_run_ll_rejection_policy,
    step_run_pylossless,
)
from autoclean.io.import_ import import_eeg
from autoclean.io.export import save_epochs_to_set, save_raw_to_set
from autoclean.utils.logging import message


class TemplateTask(Task):
    """Template class for implementing new EEG processing tasks.

    This class demonstrates how to implement a new task type in the autoclean package.
    Each task must implement these key methods:
    1. __init__ - Initialize task state and validate config
    2. run - Main processing pipeline
    3. _generate_reports - Create quality control visualizations
    4. _validate_task_config - Validate task-specific settings

    The task should handle a specific EEG paradigm (e.g., resting state, ASSR, MMN)
    and implement appropriate processing steps for that paradigm.

    Attributes:
        raw (mne.io.Raw): Raw EEG data that gets progressively cleaned through the pipeline
        pipeline (Any): PyLossless pipeline instance after preprocessing
        epochs (mne.Epochs): Epoched data after processing
        config (Dict[str, Any]): Task configuration dictionary containing all settings
        original_raw (mne.io.Raw): Original unprocessed raw data, preserved for comparison

    Example:
        To use this template:

        1. Create your configuration in autoclean_config.yaml:
        ```yaml
        # autoclean_config.yaml
        tasks:
          my_paradigm:
            settings:
              resample_step:
                enabled: true
                value: 250
              # ... other settings ...
        ```

        2. Initialize and run your task:
        ```python
        >>> from autoclean import Pipeline
        >>> pipeline = Pipeline("output/", "autoclean_config.yaml")
        >>> pipeline.process_file("data.raw", "my_paradigm")
        ```
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize a new task instance.

        Args:
            config: Configuration dictionary containing all settings.
                   See class docstring for configuration example.

        Note:
            The parent class handles basic initialization and validation.
            Task-specific setup should be added here if needed.
            
        Raises:
            ValueError: If required configuration fields are missing
            TypeError: If configuration fields have incorrect types
        """
        # Initialize instance variables
        self.raw: Optional[mne.io.Raw] = None
        self.pipeline: Optional[Any] = None
        self.epochs: Optional[mne.Epochs] = None
        self.original_raw: Optional[mne.io.Raw] = None

        # Call parent initialization with validated config
        super().__init__(config)

    def run(self) -> None:
        """Run the complete processing pipeline for this task.

        This method orchestrates the complete processing sequence:
        1. Import raw data
        2. Run preprocessing steps
        3. Apply task-specific processing
        4. Generate quality control reports

        The results are automatically saved at each stage according to
        the stage_files configuration.

        Processing Steps:
        1. Import and validate raw data
        2. Resample data to target frequency
        3. Apply preprocessing pipeline (filtering, etc.)
        4. Create BIDS-compliant paths
        5. Run PyLossless pipeline for artifact detection
        6. Clean bad channels
        7. Apply rejection policy for artifact removal
        8. Create event-based epochs
        9. Prepare epochs for ICA
        10. Apply GFP-based cleaning to epochs
        11. Generate quality control reports
        12. Save processed data

        Raises:
            FileNotFoundError: If input file doesn't exist
            RuntimeError: If any processing step fails or if data hasn't been imported

        Note:
            Progress and errors are automatically logged and tracked in
            the database. You can monitor progress through the logging
            messages and final report.
        """
        # Import raw data using standard function
        self.import_raw()
        
        # Store a copy of the original raw data for comparison in reports
        self.original_raw = self.raw.copy()


        # Apply preprocessing steps (filtering, etc.)
        self.raw = step_pre_pipeline_processing(self.raw, self.config)
        save_raw_to_set(raw = self.raw, autoclean_dict = self.config, stage = "post_prepipeline", flagged = self.flagged)

        # Create BIDS-compliant paths and filenames
        self.raw, self.config = step_create_bids_path(self.raw, self.config)

        # Run PyLossless pipeline for artifact detection and save result
        self.pipeline, self.raw = self.step_custom_pylossless_pipeline(self.config)
        save_raw_to_set(raw = self.raw, autoclean_dict = self.config, stage = "post_pylossless", flagged = self.flagged)

        # Clean bad channels (from mixins.signal_processing.channels)
        self.clean_bad_channels(cleaning_method="interpolate")

        self.pipeline.raw = self.raw
        # Apply PyLossless Rejection Policy for artifact removal
        self.pipeline, self.raw = step_run_ll_rejection_policy(
            self.pipeline, self.config
        )
        self.raw = self.pipeline.raw

        # Create event-based epochs (from mixins.signal_processing.eventid_epochs)
        self.create_eventid_epochs()

        # Prepare epochs for ICA (from mixins.signal_processing.prepare_epochs_ica)
        self.prepare_epochs_for_ica()

        # Apply GFP-based cleaning to epochs (from mixins.signal_processing.gfp_clean_epochs)
        self.gfp_clean_epochs()

        # Generate visualization reports
        self._generate_reports()

        # Save final cleaned data
        save_raw_to_set(self.raw, self.config, "post_clean_raw")


    def _generate_reports(self) -> None:
        """Generate quality control visualizations and reports.

        Creates standard visualization reports including:
        1. Raw vs cleaned data overlay - Shows the effect of preprocessing
        2. ICA components - Displays the independent components extracted
        3. ICA details - Shows detailed information about ICA components
        4. PSD topography - Power spectral density across the scalp

        The reports are saved in the debug directory specified
        in the configuration, with standardized naming conventions.

        Note:
            This is automatically called by run() method.
            Override this method if you need custom visualizations.
            
        Returns:
            None: Reports are saved to disk, nothing is returned.
            
        Raises:
            RuntimeError: If pipeline or raw is None (silently returns instead)
        """
        # Skip report generation if required data is missing
        if self.pipeline is None or self.raw is None or self.original_raw is None:
            return

        # Plot raw vs cleaned overlay using mixin method
        self.plot_raw_vs_cleaned_overlay(
            self.original_raw, self.raw, self.pipeline, self.config
        )

        # Plot ICA components using mixin method
        self.plot_ica_full(self.pipeline, self.config)

        # Generate ICA reports using mixin method
        self.generate_ica_reports(self.pipeline, self.config)

        # Create PSD topography figure using mixin method
        self.psd_topo_figure(
            self.original_raw, self.raw, self.pipeline, self.config
        )

    def _validate_task_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate task-specific configuration settings.

        This method checks that all required settings for the task
        are present and valid. The validation includes:
        - Required fields exist
        - Field types are correct
        - Stage files configuration is properly structured
        
        Args:
            config: Configuration dictionary that has passed common validation.
                   Contains all standard fields plus task-specific settings.

        Returns:
            Dict[str, Any]: The validated configuration dictionary.
                           You can add derived settings or defaults here.

        Raises:
            ValueError: If any required settings are missing or invalid
            TypeError: If settings are of wrong type

        Example:
            ```python
            def _validate_task_config(self, config):
                required_fields = {
                    'eeg_system': str,
                    'settings': dict,
                }
                for field, field_type in required_fields.items():
                    if field not in config:
                        raise ValueError(f"Missing required field: {field}")
                    if not isinstance(config[field], field_type):
                        raise TypeError(f"Field {field} must be {field_type}")
                return config
            ```
        """
        # Define required fields and their expected types
        required_fields = {
            "task": str,
            "eeg_system": str,
            "tasks": dict,
        }

        # Validate required fields exist and have correct types
        for field, field_type in required_fields.items():
            if field not in config:
                raise ValueError(f"Missing required field: {field}")
            if not isinstance(config[field], field_type):
                raise TypeError(f"Field {field} must be {field_type}")

        # Validate stage_files structure
        # These are the processing stages where data can be saved
        required_stages = [
            "post_import",
            "post_prepipeline",
            "post_pylossless",
            "post_rejection_policy",
        ]

        # Check each required stage has proper configuration
        for stage in required_stages:
            if stage not in config["stage_files"]:
                raise ValueError(f"Missing stage in stage_files: {stage}")
            stage_config = config["stage_files"][stage]
            if not isinstance(stage_config, dict):
                raise ValueError(f"Stage {stage} configuration must be a dictionary")
            if "enabled" not in stage_config:
                raise ValueError(f"Stage {stage} must have 'enabled' field")
            if "suffix" not in stage_config:
                raise ValueError(f"Stage {stage} must have 'suffix' field")

        return config
        