# 2026.1 MeasureSoftGram-Core

[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2026.1-MeasureSoftGram-Core&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2026.1-MeasureSoftGram-Core)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2026.1-MeasureSoftGram-Core&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2026.1-MeasureSoftGram-Core)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2026.1-MeasureSoftGram-Core&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2026.1-MeasureSoftGram-Core)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2026.1-MeasureSoftGram-Core&metric=bugs)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2026.1-MeasureSoftGram-Core)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2026.1-MeasureSoftGram-Core&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2026.1-MeasureSoftGram-Core)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2026.1-MeasureSoftGram-Core&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2026.1-MeasureSoftGram-Core)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2026.1-MeasureSoftGram-Core&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2026.1-MeasureSoftGram-Core)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2026.1-MeasureSoftGram-Core&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2026.1-MeasureSoftGram-Core)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2026.1-MeasureSoftGram-Core&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2026.1-MeasureSoftGram-Core)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2026.1-MeasureSoftGram-Core&metric=coverage)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2026.1-MeasureSoftGram-Core)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=fga-eps-mds_2026.1-MeasureSoftGram-Core&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=fga-eps-mds_2026.1-MeasureSoftGram-Core)

## What is it?

The MeasureSoftGram-Core is a software system for continuous quality of product observation and multidimensional use in continuous design engineering software, and is where the innovative mathematical models for software analysis live.

## How to use MeasureSoftGram Core

- [How to use](https://fga-eps-mds.github.io/2026.1-MeasureSoftGram-DOC/docs/artifact/how_to_use)

## How to run Core

```bash
docker compose up
```

## How to run tests

Install dependencies:

```bash
pip install -r requirements.txt
```

We use `tox` for tests:

```bash
pip install tox
tox
```

To run a specific package or file:

```bash
tox <PACKAGE OR FILE>
```

If it doesn't work, try first:

```bash
pip install pytest-mock
```

## Contribute

Do you want to contribute with our project? Access our [contribution guide](./CONTRIBUTING.md) where we explain how you do it.

## Code of Conduct

We follow a [Code of Conduct](./CODE_OF_CONDUCT.md) — please read it before contributing.

## License

[GNU AGPL-3.0 License](./LICENSE)

## Documentation

The documentation of this project can be accessed at: [Documentation](https://github.com/fga-eps-mds/2026.1-MeasureSoftGram-DOC).

## Another informations

Our services are available on [Docker Hub](https://hub.docker.com/):
- [Core](https://hub.docker.com/r/measuresoftgram/core)
- [Service](https://hub.docker.com/r/measuresoftgram/service)

## Wiki

For more information, see our [wiki](https://fga-eps-mds.github.io/2026.1-MeasureSoftGram-DOC/).
