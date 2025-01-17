Settings
========

The settings of the model are defined in the :code:`settings.py` script.

The table below summarizes available settings.

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - Setting
     - Possible values
     - Description
   * - AGGREGATE
     - :code:`True` / :code:`False`
     - Flag if results for model pointsshould be aggregated.
   * - ID_COLUMN
     - a string
     - The name of the column which contains identificators of the model points.
   * - MULTIPROCESSING
     - :code:`True` / :code:`False`
     - Flag if multiple CPUs should be used for the calculations.
   * - OUTPUT_COLUMNS
     - empty list of list of strings
     - List of variables to be included in the output. If empty list, all variables are included.
   * - SAVE_OUTPUT
     - :code:`True` / :code:`False`
     - Flag if csv output files should be created.
   * - SAVE_RUNTIME
     - :code:`True` / :code:`False`
     - Flag if an additional file should be created which contains runtime of variables.
   * - T_CALCULATION_MAX
     - integer
     - The maximal month for calculation.
   * - T_OUTPUT_MAX
     - integer
     - The maximal month for output files.


Aggregate
---------

The :code:`AGGREGATE` setting is a flag if the results should be aggregated for model points.

If the setting is set to :code:`False`, the results will be on the individual level:

..  code-block::
    :caption: <timestamp>_fund.csv

    t,r,fund_value
    0,1,15000.0
    1,1,15030.0
    2,1,15060.06
    3,1,15090.18
    0,1,3000.0
    1,1,3006.0
    2,1,3012.01
    3,1,3018.03
    0,2,9000.0
    1,2,9018.0
    2,2,9036.04
    3,2,9054.11

There are results for 2 model points and 1 of them has two records (record is in column :code:`r`).

If the AGGREGATE setting is set to :code:`True`, the results will aggregated:

..  code-block::
    :caption: <timestamp>_fund.csv

    t,fund_value
    0,27000.0
    1,27054.0
    2,27108.11
    3,27162.32

There is only one set of results which is the sum of all results.

Aggregated results make sense for some but not for all variables.
You can choose the relevant output columns in the :code:`OUTPUT_COLUMNS` setting.

.. WARNING::
   Aggregated results for some variables may not make sense.

|

ID column
---------

Each model point must have a column with a key column used for identification.
This column is also used to connect records in case of multiple model point.

By default, the column must be named :code:`id`.
The value can be changed using the :code:`ID_COLUMN` setting.

.. WARNING::
   Column names are case-sensitive. :code:`id` is something else than :code:`ID`.

|

The default value for the :code:`ID_COLUMN` setting is :code:`id`.

..  code-block:: python
    :caption: settings.py

    settings = {
        ...
        "ID_COLUMN": "id",
        ...
    }

The model point must have a column with this name.

..  code-block:: python
    :caption: input.py

    from cashflower import ModelPointSet

    main = ModelPointSet(data=pd.DataFrame({"id": [1, 2]}))

|

The key column might have other name.

..  code-block:: python
    :caption: settings.py

    settings = {
        ...
        "ID_COLUMN": "policy_number",
        ...
    }

The model point must have a column with this name.

..  code-block:: python
    :caption: input.py

    from cashflower import ModelPointSet

    main = ModelPointSet(data=pd.DataFrame({"policy_number": [1, 2]}))

|

Multiprocessing
---------------

By default, the model is evaluated for each model point one after another in a linear process.
If the computer has multiple cores, it's possible to perform calculations in parallel.

.. image:: https://acturtle.com/static/img/28/multiprocessing.png
   :align: center

If :code:`MULTIPROCESSING` is turned on, the model will split all model points into several parts (as many as the number of cores).
It will calculate them in parallel on separate cores and then merge together into a single output.

Thanks to that, the runtime will be decreased. The more cores, the faster calculation.

It is recommended to use :code:`MULTIPROCESSING`  when the model is stable because the log message are more vague.
For the development phase, it is recommended to use single core.

|

Output columns
--------------

By default, the model outputs all variables.
If you do not need all of them, provide the list of variables that should be in the output.

The default value of the :code:`OUTPUT_COLUMNS` setting is the empty list (:code:`[]`).
All variables are saved in the output.

..  code-block:: python
    :caption: settings.py

    settings = {
        ...
        "OUTPUT_COLUMNS": [],
        ...
    }

If the model has 3 variables, all of them will be in the output.

..  code-block:: python
    :caption: model.py

    from cashflower import assign, ModelVariable

    a = ModelVariable()
    b = ModelVariable()
    c = ModelVariable()

    @assign(a)
    def a_formula(t):
        return 1*t

    @assign(b)
    def b_formula(t):
        return 2*t

    @assign(c)
    def c_formula(t):
        return 3*t

The result contains all columns.

..  code-block::
    :caption: <timestamp>_policy.csv

    t,r,a,b,c
    0,1,0,0,0
    1,1,1,2,3
    2,1,2,4,6
    3,1,3,6,9
    0,1,0,0,0
    1,1,1,2,3
    2,1,2,4,6
    3,1,3,6,9

The user can choose a subset of columns.


..  code-block:: python
    :caption: settings.py

    settings = {
        ...
        "OUTPUT_COLUMNS": ["a", "c"],
        ...
    }

Only the chosen columns are in the output.

..  code-block::
    :caption: <timestamp>_policy.csv

    t,r,a,c
    0,1,0,0
    1,1,1,3
    2,1,2,6
    3,1,3,9
    0,1,0,0
    1,1,1,3
    2,1,2,6
    3,1,3,9

|

Save output
-----------

The :code:`SAVE_OUTPUT` setting is a flag if the model should save results to the csv files.

By default, the setting has a value :code:`True`.
After the run, the results are saved to the :code:`output` folder, for example:

..  code-block::

    .
    └── output/
        └── <timestamp>_main.csv
        └── <timestamp>_fund.csv
        └── <timestamp>_coverage.csv

|

If you change the :code:`SAVE_OUTPUT` setting to :code:`False`, no files will be created.

You can use this setting to create a custom output files or do whatever you want with the results (e.g. save to the database).

To create custom output, you can use the :code:`output` variable in the :code:`run.py` script.

..  code-block:: python
    :caption: run.py

    if __name__ == "__main__":
    output = start("example", settings, sys.argv)

    for model_point_set_name, data_frame in output.items():
        data_frame.to_csv(f"results/my-{model_point_set_name}.csv", index=False)

The :code:`output` variable holds a dictionary, where keys are names of model point sets and values are data frames with results.
The above code, will create csv files in the :code:`results` folder:

..  code-block::

    .
    └── results/
        └── my_main.csv
        └── my_fund.csv
        └── my_coverage.csv

|

Save runtime
------------

The :code:`SAVE_RUNTIME` setting is a flag if the model should save information on the runtime of variables.

|

By default, the setting has a value :code:`False`.

..  code-block:: python
    :caption: settings.py

    settings = {
        ...
        "SAVE_RUNTIME": False,
        ...
    }

No additional output is created.

..  code-block::

    .
    └── output/
        └── <timestamp>_main.csv

|

If set to :code:`True`, the model will additionally output the file with the runtime of each variable.

..  code-block:: python
    :caption: settings.py

    settings = {
        ...
        "SAVE_RUNTIME": True,
        ...
    }


The file is called :code:`<timestamp>_runtime.csv`.

..  code-block::

    .
    └── output/
        └── <timestamp>_policy.csv
        └── <timestamp>_runtime.csv

The file contains the number of seconds the model needed to evaluate each of the variables.

..  code-block::
    :caption: <timestamp>_runtime.csv

    component,runtime
    a,5.4
    b,2.7
    c,7.1

The file can help to find variables that are the evaluated the longest and to optimize them.

Measuring runtime is not possible using multiprocessing.

.. WARNING::
   The runtime will not be saved if the :code:`MULTIPROCESSING` setting is set to :code:`True`.


|

Maximal calculation time
------------------------

The :code:`T_CALCULATION_MAX` is the maximal month of the calculation.

The model will calculate results for all time periods from :code:`0` to :code:`T_CALCULATION_MAX`.

By default, the setting is set to :code:`1200` months (:code:`100` years).

|

Maximal output time
-------------------

The :code:`T_OUTPUT_MAX` is the maximal month in the output file.

By default, the model will save results for :code:`1200` months.

..  code-block:: python
    :caption: settings.py

    settings = {
        ...
        "T_OUTPUT_MAX": 1200,
        ...
    }

If the setting gets changed, then the number of rows in the output file will change.

..  code-block:: python
    :caption: settings.py

    settings = {
        ...
        "T_OUTPUT_MAX": 3,
        ...
    }

The file saves only results for the first 3 months.

..  code-block::
    :caption: <timestamp>_fund.csv

    t,fund_value
    0,27000.0
    1,27054.0
    2,27108.11
    3,27162.32

:code:`T_OUTPUT_MAX` can't be greater than :code:`T_CALCULATION_MAX`.

.. WARNING::
    :code:`T_OUTPUT_MAX` will always output :code:`min(T_OUTPUT_MAX, T_CALCULATION_MAX)` periods.
