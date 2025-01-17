Input
=====

Input for the cash flow model is defined in the :code:`input.py` script.

There are three types of the model's inputs:

* model point sets,
* assumptions,
* runplan.

Model point sets
----------------

Model point sets contain model points. Model points represent objects for which the model is calculated.
The model point can be, for example, a policyholder or a financial instrument.

.. image:: https://acturtle.com/static/img/25/multiple_model_point_sets.png
   :align: center

|

We can define:

* **model point set** - a group of model points; data can be read from a file or a database query result,
* **model point** - one or multiple records that contain data on the given object (e.g. policyholder or financial asset),
* **record** - a single row of data.

|

The model point set is defined using the :code:`ModelPointSet` class.

..  code-block:: python
    :caption: input.py

    from cashflower import ModelPointSet

    main = ModelPointSet(data=pd.DataFrame({"id": [1, 2, 3]}))


The cash flow model will calculate results for each of the model points in the model point set.

|

Create a model point set
^^^^^^^^^^^^^^^^^^^^^^^^

The data for the model point set might be stored in a csv file.

..  code-block::
    :caption: data-policy.csv

    id,age,sex,premium
    X149,45,F,100
    A192,57,M,130
    D32,18,F,50


To create a model point set, use :code:`ModelPointSet` class and pass a data frame in the :code:`data` parameter.
The primary model point set must be called :code:`main`.

..  code-block:: python
    :caption: input.py

    from cashflower import ModelPointSet

    main = ModelPointSet(data=pd.read_csv("data-policy.csv"))



A model can have multiple model point sets but at least one of them must be assigned to a variable :code:`main`.
The :code:`main` model point set must have unique keys.

By default, the identifiers of model points are stored in the column named :code:`id`.
The column name can be changed using the :code:`ID_COLUMN` setting in the :code:`settings.py` script.

|

Multiple model point sets
^^^^^^^^^^^^^^^^^^^^^^^^^

The model can have multiple model point sets. The :code:`main` model point set must have one record per model point.
The other model point sets might have multiple records for each model point.

For example, the policyholder holds multiple funds. Each fund has its own record.

..  code-block::
    :caption: data-fund.csv

    id,fund_code,fund_value
    X149,10,15000
    A192,10,3000
    A192,12,9000
    D32,8,12500
    D32,14,12500

Policyholder X149 has one fund and policyholders A192 and D32 have two funds each.

Data on these funds are stored in the :code:`fund` model point set.

..  code-block:: python
    :caption: input.py

    from cashflower import ModelPointSet

    main = ModelPointSet(data=pd.read_csv("data-policy.csv"))
    fund = ModelPointSet(data=pd.read_csv("data-fund.csv"))

Model point sets link with each other by the :code:`id` column.

|

Get value from a model point
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To read a value from a model point, use the :code:`get()` method of the :code:`ModelPointSet` class.

..  code-block:: python

        main.get("age")

|

The model variable will read the value of the record which is currently calculated.

..  code-block:: python
    :caption: model.py

    from cashflower import assign, ModelVariable
    from example.input import assumption, main

    mortality_rate = ModelVariable()


    @assign(mortality_rate)
    def mortality_rate_formula(t):
        age = main.get("age")
        sex = main.get("sex")
        return assumption["mortality"].loc[age, sex]["rate"]


Read from other model point set
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can read model point's data from another set. For example:

..  code-block:: python
    :caption: model.py

    expected_coverage_benefit(t=10, r=1)

This code reads the value for the 10th period and the second model point's record.

The :code:`model_point_size` attribute of the model point set returns the number of records for the current model point.
This attribute can be used to calculate the total values of all records.

..  code-block:: python
    :caption: model.py

    @assign(expected_benefit)
    def expected_benefit_formula(t):
        result = 0
        for r in range(coverage.model_point_size):
            result += expected_coverage_benefit(t, r)
        return result


Assumptions
-----------

Assumptions contain data for predicting the future.

..  code-block:: python
    :caption: input.py

    import pandas as pd

    assumption = dict()
    assumption["mortality"] = pd.read_csv("input/mortality.csv", index_col="AGE")
    assumption["interest_rates"] = pd.read_csv("input/interest_rates.csv", index_col="T")


Assumptions for life insurance can include:

* underwriting - mortality, lapses, expenses,
* market - interest rates, inflation,
* product's characteristics.

Assumptions are stored in a tabelaric form.

..  code-block::
    :caption: mortality.csv

    AGE,MALE,FEMALE
    0,0.003890,0.003150
    1,0.000280,0.000190
    2,0.000190,0.000140
    3,0.000150,0.000110
    4,0.000120,0.000090
    5,0.000100,0.000080
    [...]

..  code-block::
    :caption: interest_rates.csv

    T,VALUE
    1,0.00736
    2,0.01266
    3,0.01449
    4,0.01610
    5,0.01687
    [...]

Assumptions are stored as a dictionary. Each item in the dictionary is a data frame.

..  code-block:: python
    :caption: input.py

    import pandas as pd

    assumption = dict()
    assumption["mortality"] = pd.read_csv("mortality.csv", index_col="AGE")
    assumption["interest_rates"] = pd.read_csv("interest_rates.csv", index_col="T")

To add new assumptions, create a new key in the :code:`assumption` dictionary and assing a data frame to it.

Runplan
-------

Runplan is a list of runs which the model should perform.

..  code-block:: python
    :caption: input.py

    import pandas as pd
    from cashflower import Runplan, ModelPointSet

    runplan = Runplan(data=pd.DataFrame({
        "version": [1, 2, 3],
        "shock": [0, 0.05, -0.05]
    }))

You can use different run versions, to calculate different scenarios.

To get data from runplan, use:

..  code-block:: python

    runplan.get("my-column")

For example:

..  code-block:: python
    :caption: model.py

    import pandas as pd
    from example.input import main, runplan

    mortality_rate = ModelVariable(model_point_set=main)
    shocked_mortality_rate = ModelVariable(model_point_set=main)

    @assign(mortality_rate)
    def mortality_rate_formula(t):
        ...

    @assign(shocked_mortality_rate)
    def shocked_mortality_rate_formula(t):
        return mortality_rate(t) * (1+runplan.get("shock"))

To run model with the chosen version, source the :code:`run.py` and add the version number.

For example, to run the model with the version :code:`2` , use:

..  code-block::
    :caption: terminal

    python run.py 2

The model will take data from runplan for the version 2.
