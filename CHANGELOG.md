# CHANGELOG



## v3.0.0 (2023-09-21)

### Breaking

* feat: make types covariant (#18)

BREAKING CHANGE: Types of both Either and Maybe are now covariant ([`17a90b5`](https://github.com/edeckers/pyella/commit/17a90b5203ff48bf6e7aebe4553b6918ab4fa3cc))


## v2.1.0 (2023-09-16)

### Chore

* chore: create poetry env in project root ([`091e3d5`](https://github.com/edeckers/pyella/commit/091e3d54b8ce2523d92586fb5bdde8c69fd9e5de))

### Feature

* feat: add py.typed (#17)

* feat: add py.typed marker

* fix(deps): update poetry.lock ([`cda0be8`](https://github.com/edeckers/pyella/commit/cda0be876ae0e8251320fd395f03267e04e60244))


## v2.0.0 (2023-08-30)

### Breaking

* fix: drop support for Python &lt;= 3.7

BREAKING CHANGE: drop support for Python &lt;= 3.7 ([`3bc3ef2`](https://github.com/edeckers/pyella/commit/3bc3ef2530bb297c800015ca95767108416fbea3))

### Documentation

* docs: fix a few typos (#16)

* docs: rename variable in Either-example

* docs: repair backtick in README.md ([`348c466`](https://github.com/edeckers/pyella/commit/348c46670bc0b2da19ad9480253ceabaa2120d37))

### Fix

* fix(deps): bump python-semantic-release to 8.0.8 ([`57b4053`](https://github.com/edeckers/pyella/commit/57b40533ed68edd3ac32561b92a62a37f9cb0777))

* fix(deps): bump dependencies ([`244bbaa`](https://github.com/edeckers/pyella/commit/244bbaa5dcca0d941cdc65c973da52fc7745928c))


## v1.4.0 (2023-05-03)

### Documentation

* docs: include README.md in ReadTheDocs (#14) ([`440bf30`](https://github.com/edeckers/pyella/commit/440bf3077cc78a8fdbb84a960d39d7da2738c20d))

* docs: expand README.md and repair some docstrings (#13)

* docs: repair some links and add class docstrings

* docs: expand README.md ([`70233d5`](https://github.com/edeckers/pyella/commit/70233d5388a7683fcf2e35516180e0f892af13b0))

* docs: add ReadTheDocs configuration (#11) ([`11d1283`](https://github.com/edeckers/pyella/commit/11d12833bf03881764e10df86c03c5cdbf55e107))

### Feature

* feat: add PyDocs, and add chain and discard to Maybe (#10)

* docs: add some doc strings to Maybe

* docs: add some doc strings to Either

* feat: add chain and discard to Maybe ([`0886935`](https://github.com/edeckers/pyella/commit/0886935b65252badc21063004b36da18b151a857))

### Fix

* fix(docs): include docstrings in release (#15) ([`9673aea`](https://github.com/edeckers/pyella/commit/9673aea621fbb8990a497037ce537bbae9542e13))


## v1.3.0 (2023-04-30)

### Feature

* feat: add to_optional and increase code coverage (#9)

* test: cover 100% of code

* refactor(lint): apply some linter suggestions ([`4071c32`](https://github.com/edeckers/pyella/commit/4071c3294330f16937e4f26654fb4bbf02373b35))


## v1.2.0 (2023-04-18)

### Feature

* feat: add replace function (#8) ([`5cca8b0`](https://github.com/edeckers/pyella/commit/5cca8b07b97e950ed400d9a9ac9ccefc6afc6f07))


## v1.1.2 (2023-02-10)

### Fix

* fix(deps): bump all dependencies ([`6cb129a`](https://github.com/edeckers/pyella/commit/6cb129a539c0188d69a2850f1aeb8a997c441049))


## v1.1.1 (2023-01-07)

### Chore

* chore(deps): bump certifi from 2022.9.24 to 2022.12.7 (#5)

Bumps [certifi](https://github.com/certifi/python-certifi) from 2022.9.24 to 2022.12.7.
- [Release notes](https://github.com/certifi/python-certifi/releases)
- [Commits](https://github.com/certifi/python-certifi/compare/2022.09.24...2022.12.07)

---
updated-dependencies:
- dependency-name: certifi
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`37602ef`](https://github.com/edeckers/pyella/commit/37602ef76d4583213726e58d758fb6dceba18f31))

### Ci

* ci: change &#39;files&#39; to &#39;junit_files&#39; ([`399ccb8`](https://github.com/edeckers/pyella/commit/399ccb89a8b5c63076a3fc98475857a1774cf0c3))

* ci: bump publish-unit-test-result-action to v2 ([`717709a`](https://github.com/edeckers/pyella/commit/717709ade255fa600081a3de22a8f3dcc2bee3c5))

* ci: bump actions/setup-python to v4 ([`d22164c`](https://github.com/edeckers/pyella/commit/d22164ca07b2ff7bcec25648427df1083b97d5e0))

* ci: bump actions/checkout to v3 ([`54cae5b`](https://github.com/edeckers/pyella/commit/54cae5be3122acbfdf604ea2830048601b7b8dae))

* ci: add permissions for publishing coverage results ([`8af397d`](https://github.com/edeckers/pyella/commit/8af397d7ee761304220b514e2c98beaa091a7189))

### Fix

* fix(deps): bump gitpython from 3.1.29 to 3.1.30 (#6)

Bumps [gitpython](https://github.com/gitpython-developers/GitPython) from 3.1.29 to 3.1.30.
- [Release notes](https://github.com/gitpython-developers/GitPython/releases)
- [Changelog](https://github.com/gitpython-developers/GitPython/blob/main/CHANGES)
- [Commits](https://github.com/gitpython-developers/GitPython/compare/3.1.29...3.1.30)

---
updated-dependencies:
- dependency-name: gitpython
  dependency-type: indirect
...

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;

Signed-off-by: dependabot[bot] &lt;support@github.com&gt;
Co-authored-by: dependabot[bot] &lt;49699333+dependabot[bot]@users.noreply.github.com&gt; ([`9cf00d8`](https://github.com/edeckers/pyella/commit/9cf00d894a5a69b75a36477db4b8785fb344b1f7))


## v1.1.0 (2022-11-28)

### Feature

* feat: re-add support Python 3.7 (#3) ([`630118e`](https://github.com/edeckers/pyella/commit/630118e270a433c7e4634ac36a5abd707bc90437))

### Fix

* fix: ignore make install target when possible ([`b8f5853`](https://github.com/edeckers/pyella/commit/b8f58535f917400709527e40e11f7184e35d8222))


## v1.0.0 (2022-10-29)

### Breaking

* fix: enable major version bump

BREAKING CHANGE: bump to major version ([`45e12b3`](https://github.com/edeckers/pyella/commit/45e12b3ab73fba06bcfb0d2f5bfaefd89698ccc1))

### Feature

* feat: add either.map_left ([`a0b8286`](https://github.com/edeckers/pyella/commit/a0b82867c46e72fc7d859a992d28f9435a78a906))

### Fix

* fix(deps): update all dependencies ([`5ff6194`](https://github.com/edeckers/pyella/commit/5ff61948530a0b9c32b17ad837da721dc8add735))


## v0.1.0 (2022-10-15)

### Feature

* feat: add either and maybe monads ([`d822aa2`](https://github.com/edeckers/pyella/commit/d822aa2220b7fcce05f4c6f317366e96f22bbf06))
