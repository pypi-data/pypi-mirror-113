# Fix paths for imports to work in unit tests ----------------

if __name__ == "__main__":
    from _fix_paths import fix_paths
    fix_paths()

# ------------------------------------------------------------

# Load libraries ---------------------------------------------

from hyperopt import hp, Trials, fmin, tpe
from functools import partial
import numpy as np
import pickle
import json
import os
from timeit import default_timer as timer
import pathos.multiprocessing as mp
from datetime import datetime
import pandas as pd

# ------------------------------------------------------------


class HPTuner(object):

    def __init__(self, num_cores=4, save_all_evaluations=True, save_results=True):
        self.num_cores = num_cores
        self.save_all_evaluations = save_all_evaluations
        self.save_results = save_results

        self.evaluation_number = 0
        self.eval_iteration_results = pd.DataFrame(columns=["scenario_name", "result", "evaluation_number", "tuned_params"])
        self.tuning_time = None

    def tune_params(self, objective_function, tuning_settings, test_bed):
        self.tuning_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        start_time = timer()
        trials = Trials()

        evaluation_function = partial(self.evaluate_objective_function,
                                      objective_function,
                                      test_bed)

        for i in range(len(tuning_settings)):

            if i == 0:
                space = tuning_settings[i]["tuning_space"]
                best_param_set = fmin(evaluation_function, space=space, algo=tpe.suggest,
                                      max_evals=tuning_settings[i]["max_evals"], trials=trials)
            # else:
            #     for j in range(len(model_space)):
            #         space = prepare_space(model_space, j, tunable_params, best_param_set)
            #         best_param_set = fmin(objective_function, space=space, algo=tpe.suggest,
            #                               max_evals=max_evals[counter], trials=trials)
            #         counter += 1

        results = {"best_param_set": best_param_set,
                   "trials": trials}

        if self.save_results:
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "results", "{}".format(self.tuning_time))
            try:
                os.mkdir(path)
            except OSError:
                pass
            filename = ("{}_tuning_results.p".format(self.tuning_time))
            filename = os.path.join(path, filename)

            with open(filename, "wb") as fp:
                pickle.dump(results, fp, protocol=pickle.HIGHEST_PROTOCOL)

            filename = ("{}_tuning_results.txt".format(self.tuning_time))
            filename = os.path.join(path, filename)
            txt_results = results.copy()
            txt_results.pop("trials")
            with open(filename, "w") as fp:
                fp.write(json.dumps(txt_results))

        if self.save_all_evaluations:
            filename = ("{}_eval_iteration_results.p".format(self.tuning_time))
            filename = os.path.join(path, filename)
            with open(filename, "wb") as fp:
                pickle.dump(self.eval_iteration_results, fp, protocol=pickle.HIGHEST_PROTOCOL)

            filename = ("{}_eval_iteration_results.csv".format(self.tuning_time))
            filename = os.path.join(path, filename)
            self.eval_iteration_results.to_csv(filename, index=False)

        print("Done tuning in {:.2f} minutes".format((timer() - start_time) / 60))

        return results

    def evaluate_objective_function(self, objective_function, test_bed, *tuned_params):
        pool = mp.Pool(processes=self.num_cores)
        obj_func = partial(objective_function, *tuned_params)
        results = pool.starmap(obj_func, [(key, test_bed[key]) for key in test_bed])
        pool.close()
        pool.join()

        numerical_results = [result[1] for result in results]
        mean = np.mean(numerical_results)

        self.evaluation_number += 1
        if self.save_all_evaluations:
            # results = list(zip(results, [self.evaluation_number]*len(results)))
            results = [(x, y, v, z) for (x, y), v, z
                       in zip(results, [self.evaluation_number]*len(results), [*tuned_params]*len(results))]

            df = pd.DataFrame(results, columns=["scenario_name", "result", "evaluation_number", "tuned_params"])
            self.eval_iteration_results = self.eval_iteration_results.append(df)

            df = pd.DataFrame([("overall", mean, self.evaluation_number, *tuned_params)],
                              columns=["scenario_name", "result", "evaluation_number", "tuned_params"])
            self.eval_iteration_results = self.eval_iteration_results.append(df)

        return mean


if __name__ == "__main__":

    # Test case 1

    def objective_function(tuned_params, scenario_name, data):
        x = tuned_params["x"]
        return scenario_name, -data["a"] * x**2 - data["b"] * x - data["c"]

    tuning_settings = [
        {"tuning_space": {"x": hp.uniform("x", 0, 10)},
         "max_evals": 10}
    ]

    test_bed = {
        "case_1": {"a": 1, "b": 2, "c": 3},  # scenario_name, data (goes into objective_function)
        "case_2": {"a": 3, "b": 2, "c": 1},  # scenario_name, data
        "case_3": {"a": 1, "b": 1, "c": 1}   # scenario_name, data
    }

    hp_tuner = HPTuner()
    print(hp_tuner.tune_params(objective_function, tuning_settings, test_bed))

    # Test case 2 (multi param)

    def objective_function(tuned_params, scenario_name, data):
        x, y, z = tuned_params["x"], tuned_params["y"], tuned_params["z"]
        return scenario_name, -data["a"] * x**2 - data["b"] * x - data["c"] + y * z**2

    tuning_settings = [
        {"tuning_space": {"x": hp.uniform("x", 0, 10),
                          "y": hp.uniform("y", -1, 1),
                          "z": hp.uniform("z", 0, 2)},
         "max_evals": 10}
    ]

    test_bed = {
        "case_1": {"a": 1, "b": 2, "c": 3},  # scenario_name, data
        "case_2": {"a": 3, "b": 2, "c": 1},  # scenario_name, data
        "case_3": {"a": 1, "b": 1, "c": 1}   # scenario_name, data
    }

    hp_tuner = HPTuner()
    print(hp_tuner.tune_params(objective_function, tuning_settings, test_bed))
