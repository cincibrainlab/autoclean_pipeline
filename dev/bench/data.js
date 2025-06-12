window.BENCHMARK_DATA = {
  "lastUpdate": 1749755430094,
  "repoUrl": "https://github.com/cincibrainlab/autoclean_pipeline",
  "entries": {
    "Benchmark": [
      {
        "commit": {
          "author": {
            "email": "gavingoomoh@gmail.com",
            "name": "ggammoh",
            "username": "ggammoh"
          },
          "committer": {
            "email": "gavingoomoh@gmail.com",
            "name": "ggammoh",
            "username": "ggammoh"
          },
          "distinct": true,
          "id": "006f14f413ef7e049995f7b623e10e68e5df42fb",
          "message": "Fix PowerShell syntax and prevent git conflicts in CI workflows",
          "timestamp": "2025-05-29T07:35:43-04:00",
          "tree_id": "469aa60f154b7837615053fb0058220bfd4f84d6",
          "url": "https://github.com/cincibrainlab/autoclean_pipeline/commit/006f14f413ef7e049995f7b623e10e68e5df42fb"
        },
        "date": 1748518739535,
        "tool": "pytest",
        "benches": [
          {
            "name": "performance/benchmark_eeg_processing.py::TestEEGProcessingBenchmarks::test_synthetic_data_generation_performance",
            "value": 6.091115924994302,
            "unit": "iter/sec",
            "range": "stddev: 0.0017132620442705095",
            "extra": "mean: 164.17352950000463 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gammohgb@mail.uc.edu",
            "name": "Gavin Gammoh",
            "username": "ggammoh"
          },
          "committer": {
            "email": "gammohgb@mail.uc.edu",
            "name": "Gavin Gammoh",
            "username": "ggammoh"
          },
          "distinct": true,
          "id": "537fb2da98e97d48faed26edc63f78cf4ee0eaa1",
          "message": "Cleanup",
          "timestamp": "2025-05-29T08:06:18-04:00",
          "tree_id": "380a39210942e85ac860a4bfd5525eeb3a7d8706",
          "url": "https://github.com/cincibrainlab/autoclean_pipeline/commit/537fb2da98e97d48faed26edc63f78cf4ee0eaa1"
        },
        "date": 1748520527320,
        "tool": "pytest",
        "benches": [
          {
            "name": "performance/benchmark_eeg_processing.py::TestEEGProcessingBenchmarks::test_synthetic_data_generation_performance",
            "value": 6.08260406855772,
            "unit": "iter/sec",
            "range": "stddev: 0.000656279313761158",
            "extra": "mean: 164.4032701666731 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gavingoomoh@gmail.com",
            "name": "ggammoh",
            "username": "ggammoh"
          },
          "committer": {
            "email": "gavingoomoh@gmail.com",
            "name": "ggammoh",
            "username": "ggammoh"
          },
          "distinct": true,
          "id": "54332719ed34169beec634e450a0b83db40a027d",
          "message": "Fix integration test MockOperations and method name errors\n\n- Add missing mock methods to MockOperations: mock_ica, mock_apply_ica, mock_autoreject, mock_apply_autoreject, mock_ransac\n- Fix incorrect method names in integration tests: apply_ica → apply_iclabel_rejection\n- Fix class name typo: AutorejectEpochsMixin → AutoRejectEpochsMixin\n- Remove patches for non-existent run_autoreject method\n\nResolves AttributeError exceptions in CI integration tests.",
          "timestamp": "2025-05-29T08:13:39-04:00",
          "tree_id": "dbfd9f50f83ea6b5fdf9c461027af57be357ebda",
          "url": "https://github.com/cincibrainlab/autoclean_pipeline/commit/54332719ed34169beec634e450a0b83db40a027d"
        },
        "date": 1748521000090,
        "tool": "pytest",
        "benches": [
          {
            "name": "performance/benchmark_eeg_processing.py::TestEEGProcessingBenchmarks::test_synthetic_data_generation_performance",
            "value": 6.151381345363389,
            "unit": "iter/sec",
            "range": "stddev: 0.000533643039586219",
            "extra": "mean: 162.56511242856877 msec\nrounds: 7"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gammohgb@mail.uc.edu",
            "name": "Gavin Gammoh",
            "username": "ggammoh"
          },
          "committer": {
            "email": "gammohgb@mail.uc.edu",
            "name": "Gavin Gammoh",
            "username": "ggammoh"
          },
          "distinct": true,
          "id": "2ad53e21147764331c8691bb97ae56a2c5a872f3",
          "message": "Fix failed to find bids info in json summary",
          "timestamp": "2025-05-29T14:09:16-04:00",
          "tree_id": "9162af5e111524736649d1ef378a0bcd34b7765d",
          "url": "https://github.com/cincibrainlab/autoclean_pipeline/commit/2ad53e21147764331c8691bb97ae56a2c5a872f3"
        },
        "date": 1748542303215,
        "tool": "pytest",
        "benches": [
          {
            "name": "performance/benchmark_eeg_processing.py::TestEEGProcessingBenchmarks::test_synthetic_data_generation_performance",
            "value": 6.062044663407491,
            "unit": "iter/sec",
            "range": "stddev: 0.0008920047652318285",
            "extra": "mean: 164.96084333332797 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gammohgb@mail.uc.edu",
            "name": "Gavin Gammoh",
            "username": "ggammoh"
          },
          "committer": {
            "email": "gammohgb@mail.uc.edu",
            "name": "Gavin Gammoh",
            "username": "ggammoh"
          },
          "distinct": false,
          "id": "1860977ce7c124ed5bec24b6c901d27555a7dcaf",
          "message": "Add epoch support for import and bids creation",
          "timestamp": "2025-06-02T12:41:38-04:00",
          "tree_id": "32700d5081f8e674cbf27ee1d9025bd0937a863a",
          "url": "https://github.com/cincibrainlab/autoclean_pipeline/commit/1860977ce7c124ed5bec24b6c901d27555a7dcaf"
        },
        "date": 1748882663076,
        "tool": "pytest",
        "benches": [
          {
            "name": "performance/benchmark_eeg_processing.py::TestEEGProcessingBenchmarks::test_synthetic_data_generation_performance",
            "value": 5.998644438327438,
            "unit": "iter/sec",
            "range": "stddev: 0.006129980369954735",
            "extra": "mean: 166.7043296666577 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gammohgb@mail.uc.edu",
            "name": "Gavin Gammoh",
            "username": "ggammoh"
          },
          "committer": {
            "email": "gammohgb@mail.uc.edu",
            "name": "Gavin Gammoh",
            "username": "ggammoh"
          },
          "distinct": true,
          "id": "012cdbd6801a9c6d1ac13296b1107db3b9af4fff",
          "message": "Add statistical learning support",
          "timestamp": "2025-06-03T15:36:58-04:00",
          "tree_id": "f1f1b6c4d5f8558f1e8c569bd5ea00a54fe5dda4",
          "url": "https://github.com/cincibrainlab/autoclean_pipeline/commit/012cdbd6801a9c6d1ac13296b1107db3b9af4fff"
        },
        "date": 1748979557074,
        "tool": "pytest",
        "benches": [
          {
            "name": "performance/benchmark_eeg_processing.py::TestEEGProcessingBenchmarks::test_synthetic_data_generation_performance",
            "value": 6.125070427590718,
            "unit": "iter/sec",
            "range": "stddev: 0.0011060069555218033",
            "extra": "mean: 163.26342885715152 msec\nrounds: 7"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gammohgb@mail.uc.edu",
            "name": "Gavin Gammoh",
            "username": "ggammoh"
          },
          "committer": {
            "email": "gammohgb@mail.uc.edu",
            "name": "Gavin Gammoh",
            "username": "ggammoh"
          },
          "distinct": true,
          "id": "cf1e9632b64153b2cf91fec434fc6d7f6a2409c4",
          "message": "Misc Updates",
          "timestamp": "2025-06-09T09:25:59-04:00",
          "tree_id": "e703d150b856a46e67afef528be2dc6d5cc4b909",
          "url": "https://github.com/cincibrainlab/autoclean_pipeline/commit/cf1e9632b64153b2cf91fec434fc6d7f6a2409c4"
        },
        "date": 1749475727247,
        "tool": "pytest",
        "benches": [
          {
            "name": "performance/benchmark_eeg_processing.py::TestEEGProcessingBenchmarks::test_synthetic_data_generation_performance",
            "value": 6.0240721017573025,
            "unit": "iter/sec",
            "range": "stddev: 0.0008731660899108858",
            "extra": "mean: 166.00066916667325 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "100084533+ggammoh@users.noreply.github.com",
            "name": "Gavin Gammoh",
            "username": "ggammoh"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "c5395c00d46e29501b3ff8c2a5e8ae48dc87a08d",
          "message": "Merge pull request #31 from cincibrainlab/Refactor-User-Experience\n\nRefactor user experience",
          "timestamp": "2025-06-12T13:09:20-04:00",
          "tree_id": "f4286bf8ecc60d117d355ab9807c1ba8329f48b8",
          "url": "https://github.com/cincibrainlab/autoclean_pipeline/commit/c5395c00d46e29501b3ff8c2a5e8ae48dc87a08d"
        },
        "date": 1749748281397,
        "tool": "pytest",
        "benches": [
          {
            "name": "performance/benchmark_eeg_processing.py::TestEEGProcessingBenchmarks::test_synthetic_data_generation_performance",
            "value": 6.0227965620358885,
            "unit": "iter/sec",
            "range": "stddev: 0.002445472851630422",
            "extra": "mean: 166.0358256666683 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "100084533+ggammoh@users.noreply.github.com",
            "name": "Gavin Gammoh",
            "username": "ggammoh"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "62362fd5ac687e414cc8e4e7bf274f294e813da5",
          "message": "Remove legacy configs",
          "timestamp": "2025-06-12T13:14:38-04:00",
          "tree_id": "32cfe7c2db9f3c6679d759252f248faa3ac3487c",
          "url": "https://github.com/cincibrainlab/autoclean_pipeline/commit/62362fd5ac687e414cc8e4e7bf274f294e813da5"
        },
        "date": 1749748603650,
        "tool": "pytest",
        "benches": [
          {
            "name": "performance/benchmark_eeg_processing.py::TestEEGProcessingBenchmarks::test_synthetic_data_generation_performance",
            "value": 6.102549654908596,
            "unit": "iter/sec",
            "range": "stddev: 0.00080206633324209",
            "extra": "mean: 163.86593416665582 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "100084533+ggammoh@users.noreply.github.com",
            "name": "Gavin Gammoh",
            "username": "ggammoh"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "aee3dbe0cdc9106932dc538f176fd948fcec1a2b",
          "message": "Delete .DS_Store",
          "timestamp": "2025-06-12T13:15:59-04:00",
          "tree_id": "5ce4248d1205bf5c6085b47c295dce3065f645c6",
          "url": "https://github.com/cincibrainlab/autoclean_pipeline/commit/aee3dbe0cdc9106932dc538f176fd948fcec1a2b"
        },
        "date": 1749748677187,
        "tool": "pytest",
        "benches": [
          {
            "name": "performance/benchmark_eeg_processing.py::TestEEGProcessingBenchmarks::test_synthetic_data_generation_performance",
            "value": 6.080647167331386,
            "unit": "iter/sec",
            "range": "stddev: 0.0007484486306170512",
            "extra": "mean: 164.45617916667743 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gammohgb@mail.uc.edu",
            "name": "Gavin Gammoh",
            "username": "ggammoh"
          },
          "committer": {
            "email": "gammohgb@mail.uc.edu",
            "name": "Gavin Gammoh",
            "username": "ggammoh"
          },
          "distinct": true,
          "id": "862b3e60a975d46a976bf31b2fb0065b0079cf4f",
          "message": "Merge branch 'main' of https://github.com/cincibrainlab/autoclean_pipeline",
          "timestamp": "2025-06-12T13:30:41-04:00",
          "tree_id": "4ce45aa81576c21072068bd3184b7d2c8b17ea3d",
          "url": "https://github.com/cincibrainlab/autoclean_pipeline/commit/862b3e60a975d46a976bf31b2fb0065b0079cf4f"
        },
        "date": 1749749609340,
        "tool": "pytest",
        "benches": [
          {
            "name": "performance/benchmark_eeg_processing.py::TestEEGProcessingBenchmarks::test_synthetic_data_generation_performance",
            "value": 6.047881866965814,
            "unit": "iter/sec",
            "range": "stddev: 0.0008114491256905633",
            "extra": "mean: 165.3471449999889 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gavingoomoh@gmail.com",
            "name": "ggammoh",
            "username": "ggammoh"
          },
          "committer": {
            "email": "gavingoomoh@gmail.com",
            "name": "ggammoh",
            "username": "ggammoh"
          },
          "distinct": true,
          "id": "7770c3ae0a09211b1085393c9e29ca201d51ea27",
          "message": "Fix Sphinx documentation build by adding missing xarray mock import\n\nProblem: Documentation build was failing with error:\n\"no module named autoclean.mixins.signal_processing.segment_rejection\"\n\nRoot Cause: The segment_rejection module imports xarray, but xarray\nwas not included in the autodoc_mock_imports list, causing Sphinx\nto fail when trying to import the module for documentation generation.\n\nSolution:\n- Added 'xarray' to autodoc_mock_imports list in docs/conf.py\n- Updated version number to 2.0.0 in documentation configuration\n\nThis allows Sphinx to mock the xarray import during documentation\ngeneration, resolving the build failure while maintaining proper\nAPI documentation for the SegmentRejectionMixin class.",
          "timestamp": "2025-06-12T13:43:30-04:00",
          "tree_id": "15ec1bccb35e4f21cbccb265272379a29669c4fd",
          "url": "https://github.com/cincibrainlab/autoclean_pipeline/commit/7770c3ae0a09211b1085393c9e29ca201d51ea27"
        },
        "date": 1749750414141,
        "tool": "pytest",
        "benches": [
          {
            "name": "performance/benchmark_eeg_processing.py::TestEEGProcessingBenchmarks::test_synthetic_data_generation_performance",
            "value": 5.939978901076322,
            "unit": "iter/sec",
            "range": "stddev: 0.0018062254540816573",
            "extra": "mean: 168.35076633332827 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gavingoomoh@gmail.com",
            "name": "ggammoh",
            "username": "ggammoh"
          },
          "committer": {
            "email": "gavingoomoh@gmail.com",
            "name": "ggammoh",
            "username": "ggammoh"
          },
          "distinct": true,
          "id": "fb7c6d8982cf0d90729e5be0dc1dcb229476f409",
          "message": "Improve documentation tone and focus on built-in tasks\n\nMajor improvements to documentation:\n\nContent Changes:\n- Removed excessive emoji usage throughout documentation\n- Eliminated condescending language and overly simplified explanations\n- Balanced focus between built-in tasks and custom tasks\n- Emphasized built-in task capabilities and variety\n- Streamlined section organization with less fragmentation\n\nTone Improvements:\n- Professional, technical writing appropriate for researchers\n- Removed \"beginner-friendly\" assumptions that could be patronizing\n- Direct, informative explanations without excessive hand-holding\n- Clear technical information without oversimplification\n\nStructure Changes:\n- Reorganized getting_started.rst to highlight built-in tasks first\n- Updated first_time_processing.rst with cleaner, more focused content\n- Removed separate \"non-technical\" and \"technical\" user sections\n- Consolidated installation and setup procedures\n\nThe documentation now presents AutoClean as a professional tool\nsuitable for researchers while maintaining accessibility for new users.",
          "timestamp": "2025-06-12T14:35:52-04:00",
          "tree_id": "967898dcc501707c65f2342c4cd2b8bc7b3d8ed9",
          "url": "https://github.com/cincibrainlab/autoclean_pipeline/commit/fb7c6d8982cf0d90729e5be0dc1dcb229476f409"
        },
        "date": 1749753721307,
        "tool": "pytest",
        "benches": [
          {
            "name": "performance/benchmark_eeg_processing.py::TestEEGProcessingBenchmarks::test_synthetic_data_generation_performance",
            "value": 6.03727871086888,
            "unit": "iter/sec",
            "range": "stddev: 0.0005740839768509858",
            "extra": "mean: 165.63754100000475 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gavingoomoh@gmail.com",
            "name": "ggammoh",
            "username": "ggammoh"
          },
          "committer": {
            "email": "gavingoomoh@gmail.com",
            "name": "ggammoh",
            "username": "ggammoh"
          },
          "distinct": true,
          "id": "2024ac706fe268df701f728a6425639a71d2cb53",
          "message": "Fix benchmark script import path and API compatibility\n\nProblem: Performance benchmark script failing with:\n- ModuleNotFoundError: No module named 'tests'\n- TypeError: Pipeline.__init__() got unexpected keyword argument 'autoclean_dir'\n\nSolutions:\n1. Import Path Fix:\n   - Added project root to Python path in benchmark script\n   - Enables direct execution of benchmark_eeg_processing.py\n   - Resolves module import issues when run outside pytest context\n\n2. API Compatibility:\n   - Updated Pipeline initialization to use output_dir parameter\n   - Removed autoclean_config parameter (no longer supported in v2.0.0)\n   - Maintains benchmark functionality with new API\n\nThe performance benchmark can now be executed directly without\nimport errors and is compatible with the v2.0.0 API changes.",
          "timestamp": "2025-06-12T14:50:21-04:00",
          "tree_id": "5cfcefe7d4bc19f7ec9a8bc649458ed283ff122b",
          "url": "https://github.com/cincibrainlab/autoclean_pipeline/commit/2024ac706fe268df701f728a6425639a71d2cb53"
        },
        "date": 1749755371792,
        "tool": "pytest",
        "benches": [
          {
            "name": "performance/benchmark_eeg_processing.py::TestEEGProcessingBenchmarks::test_synthetic_data_generation_performance",
            "value": 5.987997328814156,
            "unit": "iter/sec",
            "range": "stddev: 0.000834159832559648",
            "extra": "mean: 167.0007425000032 msec\nrounds: 6"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "gavingoomoh@gmail.com",
            "name": "ggammoh",
            "username": "ggammoh"
          },
          "committer": {
            "email": "gavingoomoh@gmail.com",
            "name": "ggammoh",
            "username": "ggammoh"
          },
          "distinct": true,
          "id": "fa6455e996a9c642f17d38807ffd61a7070379a6",
          "message": "Refocus documentation on Python API and GUI navigation workflow\n\nMajor shift in documentation approach:\n\nPython-First Workflow:\n- Emphasized Python API as primary interface over command line\n- Added file manager integration for navigation and path finding\n- Provided complete Python examples for common workflows\n- Integrated subprocess calls for setup within Python environment\n\nConfig Wizard Integration:\n- Prominently featured AutoClean Config Wizard web tool\n- Added step-by-step guide for creating custom tasks via web interface\n- Emphasized drop-and-go workflow for task files\n- Linked to https://cincibrainlab.github.io/Autoclean-ConfigWizard/\n\nGUI-Based File Management:\n- Focused on system file manager (Finder/File Explorer/Files)\n- Removed command-line navigation requirements\n- Added instructions for copying paths from file manager\n- Integrated result viewing through file manager\n\nDrop-and-Go Task Management:\n- Highlighted automatic task discovery in workspace/tasks/ folder\n- Simplified task addition process (drag and drop)\n- Emphasized no registration or configuration needed\n- Clear workspace structure explanation\n\nThe documentation now presents a workflow that combines Python's\npower with familiar GUI tools, making EEG processing more accessible\nwhile leveraging the Config Wizard for custom task creation.",
          "timestamp": "2025-06-12T15:07:23-04:00",
          "tree_id": "c4772107abe6145543fdae52d1409a96cf150b1a",
          "url": "https://github.com/cincibrainlab/autoclean_pipeline/commit/fa6455e996a9c642f17d38807ffd61a7070379a6"
        },
        "date": 1749755429033,
        "tool": "pytest",
        "benches": [
          {
            "name": "performance/benchmark_eeg_processing.py::TestEEGProcessingBenchmarks::test_synthetic_data_generation_performance",
            "value": 6.067585045956892,
            "unit": "iter/sec",
            "range": "stddev: 0.0011064221193770967",
            "extra": "mean: 164.81021566666718 msec\nrounds: 6"
          }
        ]
      }
    ]
  }
}