from datetime import datetime
from typing import Any, Dict, Tuple, Union

import mne
from mne_bids import read_raw_bids
import pylossless as ll
import yaml
from autoclean.io.export import save_ica_to_fif
from autoclean.utils.logging import message
from autoclean.mixins.signal_processing.reference import ReferenceMixin



class PyLosslessMixin:
    """Mixin class providing PyLossless functionality for autoclean tasks."""

    def step_custom_pylossless_pipeline(self, config: Dict[str, Any],
                                   eog_channel: Union[str, None] = "E25", stage_name: str = "post_pylossless") -> Tuple[Any, mne.io.Raw]:
        """Run PyLossless pipeline on the data.

        This method runs the PyLossless pipeline on the input data.
        It includes steps for filtering, flagging bad channels, and flagging bad epochs.

        Parameters
        ----------
        config : dict
            The configuration dictionary for the autoclean pipeline.
        eog_channel : str | None, optional
            The channel name of the EOG channel. Default is "E25". This parameter is used to specify the channel referenced for eog specific ICA. 
            If None, no EOG channel will be used.
        stage_name : str, optional
            The name of the stage for saving and metadata. Default is "post_pylossless".

        Returns
        -------
        pipeline : instance of ll.LosslessPipeline
            The PyLossless pipeline object.
        pipeline.raw : instance of mne.io.Raw
            The raw data object with PyLossless processing applied.

        Notes
        -----
        This method is a wrapper around the PyLossless pipeline.
        It includes a mixture of Pylossless and Autoclean functions in order to provide a comprehensive pipeline.

        See Also
        --------
        :py:class:`pylossless.LosslessPipeline` : For more information on the PyLossless pipeline

        """
        message("header", "Running PyLossless pipeline")

        message("debug", f"Running PyLossless pipeline with config: {config}")

        pipeline = self.step_get_pylossless_pipeline(config)

        original_raw = pipeline.raw.copy()

        message("debug", "performing pylossless filtering")

        pipeline.filter()

        #Flag bad channels
        message("debug", "flagging noisy channels")
        pipeline.flag_noisy_channels()

        data_r_ch = pipeline.flag_uncorrelated_channels()

        pipeline.flag_bridged_channels(data_r_ch)

        pipeline.flag_rank_channel(data_r_ch, message="Flagging the rank channel")

        message("info", "Removing eog channels from flagged bads")
        bads = pipeline.flags['ch'].get_flagged()
        noisy_channels = list(pipeline.flags['ch']['noisy'])
        uncorrelated_channels = list(pipeline.flags['ch']['uncorrelated'])
        bridged_channels = list(pipeline.flags['ch']['bridged'])
        rank_channels = list(pipeline.flags['ch']['rank'])
        task = config["task"]
        try:
            eogs = config["tasks"][task]["settings"]["eog_step"]["value"]
        except Exception as e:
            message("warning", f"Failed to get eog channel (run_custom_pylossless_pipeline)")
            eogs = []

        message("debug", f"Removing eog channels from flagged bads: {eogs}")

        bads = [b for b in bads if b not in eogs]

        message("debug", f"Interpolating bad channels: {bads}")

        pipeline.raw.info['bads'] = bads
        pipeline.raw.interpolate_bads(reset_bads=True)
        pipeline.flags['ch'].clear()

        if len(bads)/self.raw.info['nchan'] > self.BAD_CHANNEL_THRESHOLD:
            self.flagged = True
            warning = f"WARNING: {len(bads)/self.raw.info['nchan']:.2%} bad channels detected"
            self.flagged_reasons.append(warning)
            message("warning", f"Flagging: {warning}")

        pipeline.raw.bad_channels = bads

        message("debug", "referencing data")
        pipeline.raw = ReferenceMixin.set_eeg_reference(self, pipeline.raw)

        #Flag Bad Epochs 
        message("debug", "flagging noisy epochs")
        pipeline.flag_noisy_epochs(message="Flagging Noisy Epochs")

        pipeline.flag_uncorrelated_epochs(message="Flagging Uncorrelated epochs")

        pre_ica_raw = pipeline.raw.copy()



        # #Run ICA
        message("header", "Running ICA")
        if pipeline.config["ica"] is not None:
            message("debug", "running initial ICA")
            pipeline.run_ica("run1", message="Running Initial ICA")
            if eog_channel is not None:
                message("info", f"Running first EOG detection on {eog_channel}")
                eog_indices, eog_scores = pipeline.ica1.find_bads_eog(pipeline.raw, ch_name=eog_channel)
                pipeline.ica1.exclude = eog_indices
                pipeline.ica1.apply(pipeline.raw)

            message("debug", "running final ICA")
            pipeline.run_ica("run2", message="Running Final ICA and ICLabel.")
            if eog_channel is not None:
                message("info", f"Running second EOG detection on {eog_channel}")
                eog_indices, eog_scores = pipeline.ica2.find_bads_eog(pipeline.raw, ch_name=eog_channel)
                pipeline.ica2.exclude = eog_indices
                pipeline.ica2.apply(pipeline.raw)

            message("debug", "flagging noisy ICs")
            pipeline.flag_noisy_ics(message="Flagging time periods with noisy IC's.")

            save_ica_to_fif(pipeline, self.config, pre_ica_raw)

        metadata = {
            "creationDateTime": datetime.now().isoformat(),
            "channelCount": len(pipeline.raw.ch_names),
            "durationSec": int(pipeline.raw.n_times) / pipeline.raw.info["sfreq"],
            "numberSamples": int(pipeline.raw.n_times),
            "bads": bads,
            "noisy_channels": noisy_channels,
            "uncorrelated_channels": uncorrelated_channels,
            "bridged_channels": bridged_channels,
            "rank_channels": rank_channels,
        }

        self._update_metadata("step_custom_pylossless_pipeline", metadata)

        self._save_raw_result(pipeline.raw, stage_name)

        self._update_instance_data(original_raw, pipeline.raw)

        return pipeline, pipeline.raw


    def step_get_pylossless_pipeline(self, autoclean_dict: Dict[str, Any]) -> Tuple[Any, mne.io.Raw]:
        """Create a PyLossless pipeline object.

        Parameters
        ----------
        autoclean_dict : dict
            The configuration dictionary for the autoclean pipeline.

        Returns
        -------
        pipeline : instance of ll.LosslessPipeline
            The PyLossless pipeline object.

        Notes
        -----
        This method is used as the first step in creating a custom PyLossless pipeline. 
        It will read the raw data in the BIDS path and create a PyLossless pipeline object. 
        So it is important that the save_to_bids step is run before this step.

        See Also
        --------
        :py:class:`pylossless.LosslessPipeline` : For more information on the PyLossless pipeline
        """
        message("header", "Creating PyLossless Pipeline Object")
        task = autoclean_dict["task"]
        bids_path = autoclean_dict["bids_path"]
        config_path = autoclean_dict["tasks"][task]["lossless_config"]
        derivative_name = "pylossless"

        try:
            raw = read_raw_bids(bids_path, verbose="ERROR", extra_params={"preload": True})

            pipeline = ll.LosslessPipeline(config_path)

            pipeline.raw = raw

            derivatives_path = pipeline.get_derivative_path(bids_path, derivative_name)


        except Exception as e:
            message("error", f"Failed to run pylossless: {str(e)}")
            raise e

        try:
            pylossless_config = yaml.safe_load(open(config_path))

            metadata = {
                "creationDateTime": datetime.now().isoformat(),
                "derivativeName": derivative_name,
                "derivativePath": derivatives_path,
                "configFile": str(config_path),
                "pylossless_config": pylossless_config,
            }
            self._update_metadata("step_get_pylossless_pipeline", metadata)

        except Exception as e:
            message("error", f"Failed to load pylossless config: {str(e)}")
            raise e

        return pipeline