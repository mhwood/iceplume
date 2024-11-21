# iceplume

I created this repository to store code and a few tools for implementing the iceplume package into MITgcm configurations. The iceplume package provides a parameterization for ice marginal plumes such as those found at the fronts of Greenland's glaciers.

The original code was developed by Tom Cowton and others, and is described in the following paper:

Cowton, T., Slater, D., Sole, A., Goldberg, D., & Nienow, P. (2015). [Modeling the impact of glacial runoff on fjord circulation and submarine melt rate using a new subgrid‐scale parameterization for glacial plumes]( https://doi.org/10.1002/2014JC010324). Journal of Geophysical Research: Oceans, 120(2), 796-812

The original code can be found on [Zenodo[(https://zenodo.org/records/7086069) and all modifications presented in the code here are from An Nguyen, Kiki Schulz, and me (Mike Wood). 

This code relies on the [ODEPACK](https://computing.llnl.gov/projects/odepack) package which was developed by Alan Hindmarsh at LLNL. 

## Notes:
- The opkd library uses implicit variable declarations (e.g. variables starting with n are assumed to be integers unless otherwise indicated). To ensure the compiler interprets this code correctly, be sure that the -fimplicit-none flag is not activated in your optfile (it is by default in some opt files!)
