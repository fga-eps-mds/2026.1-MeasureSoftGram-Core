# 2024-2 MeasureSoftGram-Core

## Badges

[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-Core&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-Core)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-Core&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-Core)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-Core&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-Core)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-Core&metric=bugs)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-Core)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-Core&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-Core)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-Core&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-Core)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-Core&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-Core)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-Core&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-Core)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-Core&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-Core)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-Core&metric=coverage)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-Core)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2023-1-MeasureSoftGram-Core&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2023-1-MeasureSoftGram-Core)

## What is it?

The MeasureSoftGram-Core is a Software system for continuous quality of product observation and multidimensional use in continuous design engineering software and is where you have the innovative mathematical models for software analysis.

## How to use MeasureSoftGram Core
-[How to use](https://fga-eps-mds.github.io/2021-2-MeasureSoftGram-Doc/docs/artifact/how_to_use)

## How to run Core

Made the container with :

```
docker-compose up
```

## How to run tests

Install this dependencies

```
pip install -r requirements.txt
```

We are using tox for the tests, so it is good to install the tox:

```
pip install tox
```

Then you can run the tests using

```
 tox 
```

if you want to especify the file use:
```
 tox <PACKAGE OR FILE>
```

If it does not work, you can try to run before: 
```
pip install pytest-mock
```

## Contribute

Do you want to contribute with our project? Access our [contribution guide](https://github.com/fga-eps-mds/2021-2-MeasureSoftGram-Core/blob/develop/CONTRIBUTING.md) where we explain how you do it. 

## License

AGPL-3.0 License

### Documentation

The documentation of this project can be accessed at this website: [Documentation](https://github.com/fga-eps-mds/2021-2-MeasureSoftGram-Doc).

## Another informations

Our services are available on [Docker Hub](https://hub.docker.com/):
- [Core](https://hub.docker.com/r/measuresoftgram/core)
- [Service](https://hub.docker.com/r/measuresoftgram/service)

### Wiki

For more informations, you can see our wiki:
- [Wiki](https://fga-eps-mds.github.io/2023-1-MeasureSoftGram-Doc/)

