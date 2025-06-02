window.BENCHMARK_DATA = {
  "lastUpdate": 1748882664297,
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
      }
    ]
  }
}