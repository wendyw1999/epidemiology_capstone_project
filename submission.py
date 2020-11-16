{
    "config": ["config/data-params.json", "config/eda-params.json", "config/analysis-params.json"],
    "build": "run.py",
    "library": ["src",'all_function.py'], # analysis/analysis.py, data/etl.py, model/predict_model.py, model/train_model.py
    "notebook": ["notebooks/Stimulation2.ipynb"],
    "targets": ["data", "eda", "model"] 
}