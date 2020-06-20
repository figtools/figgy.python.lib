# figgy.python.lib
Contains a public python library that may be used be Figgy users to simply application config management.

Start using figgy today: https://www.figgy.dev

Check out the detailed docs: https://www.figgy.dev/docs/

Demonstration & Walkthrough of how to use this library: https://github.com/mancej/figgy.python-reference

## Using figgy.lib

This library greatly simplifies the process of fetching / using configurations from ParameterStore. It is designed
to be used alongside the larger figgy ecosystem and will help you. For more details on what Figgy offers check out 
the [Figgy Website.](https://www.figgy.dev)


To the this lib to import parameters from parameter store:

### Define your configurations
[What's a Fig?](https://www.figgy.dev/docs/getting-started/concepts.html)
```python

# config.py
from figgy.figs import *
from figgy.fig_store import FigStore

# All PS configurations are defined in our FigStore
class Figs(FigStore):
    # Twig = Application's namespace
    TWIG: str = "/app/foo-service"

    # Custom Figs specific to my application (app figs)
    SECRET_ADMIRER = AppFig("secret-admirer")   # Expected to be found at /app/foo-service/secret-admirer
    ADMIRED_PERSON = AppFig("admired-person")   # Expected to be found at /app/foo-service/admired-person
    SQL_DB_NAME = AppFig("db-name", default="SecretAdmirerDB")

    # Figs shared by secret owners (shared figs)
    SQL_USER = SharedFig("replicated/sql/user")   # Expected to be found at /app/foo-service/replicated/sql/user
    SQL_PASSWORD = SharedFig("replicated/sql/password")

    # Global figs used by many services that we need to use (replicated figs)
    SQL_HOSTNAME = ReplicatedFig(source="/shared/resources/dbs/fig-db/dns", name="replicated/sql/hostname")
    SQL_PORT = ReplicatedFig(source="/shared/resources/dbs/fig-db/port", name="replicated/sql/port")

    # Merged Connection URL (merged figs)
    SQL_CONNECTION_STRING = MergeFig(
        name="replicated/sql-connection",
        pattern=["mysql://", SQL_USER, ":", SQL_PASSWORD, "@", SQL_HOSTNAME, ":", SQL_PORT, "/", SQL_DB_NAME]
    )
```


### Import the library

```python

# main.py

import boto3
from figgy import FigService, ConfigWriter
from config import Figs

ssm = boto3.client('ssm', region_name='us-east-1')
svc = FigService(ssm)
FIGS = Figs(svc, lazy_load=False)   # Lazy-load will fetch figs from PS as needed instead of at application bootstrap

# Optional, but recommended. Have your `figgy.json` written to your run-directory. This will keep your application's
# used configs in sync with remote configurations.
ConfigWriter().write(FIGS)
    
## Use a configuration
print(f"Hello {FIGS.ADMIRED_PERSON}, {FIGS.SECRET_ADMIRER} is admiring you!")

print(f"Found Merged SQL Connection String: {FIGS.SQL_CONNECTION_STRING}")

```

If you run your APP and receive an error indicating a parameter is missing, run `figgy config sync --config figgy.json` where
the `figgy.json` is the path to the generated `figgy.json` file. 

### Override with ENV variables
Any and all configurations can be overridden locally through ENV variables.

Suppose your:
TWIG = '/app/foo'
FIG1 = 'fig1'
DB_PASS = 'replicated/db/password'

To override these values with the follow ENV variables. The `TWIG` (namespace) should be left out of the fig name:

```console
    export FIG1=foobar
    export REPLICATED_DB_PASSWORD=p@ssw0rd!!
```

These will automatically take precedent during configuration resolution. ParameterStore will never be queried for these parameters.