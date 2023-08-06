import yaml
import importlib_resources as res

def load_params(fname):
    with res.open_binary('demo_configs', fname) as stream:
        file = yaml.load(stream, Loader = yaml.Loader)
    return file

xgb_config = load_params('xgboost.yml')
cb_config = load_params('catboost.yml')
lgbm_config = load_params('lightgbm.yml')