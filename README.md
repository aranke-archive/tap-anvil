# tap-anvil

`tap-anvil` is a Singer tap for [Anvil](https://www.useanvil.com/), a tool for programmatically filling out PDF forms.

## Installation

```bash
pipx install tap-anvil
```

## Configuration

The only config option is an Anvil API key which can be set up using [these instructions](https://www.useanvil.com/docs/api/getting-started#api-key).
When running in production, make sure to use the production API key to avoid throttling.

`tap-anvil` accepts this config option using the `TAP_ANVIL_API_KEY` environment variable.

## Usage

```bash
TAP_ANVIL_API_KEY=xxx tap-anvil --config=ENV
```

## References

* [Anvil GraphQL API](https://www.useanvil.com/docs/api/graphql/reference/)
* [Meltano SDK Developer Guide](https://sdk.meltano.com/en/latest/dev_guide.html)
* [Singer Spec](https://hub.meltano.com/singer/spec/)

## Local Development

### Installation

```bash
pipx install poetry
poetry install
```

### Download Data

```bash
pipx install tap-jsonl
rm -rf output/*.jsonl && TAP_ANVIL_API_KEY=xxx tap-anvil --config=ENV | target-jsonl -c output/target-jsonl-config.json
```

### Testing

```bash
poetry run pytest
```

### Running a GraphQL query locally

Use the Anvil Postman collection here: https://www.postman.com/useanvil/workspace/anvil/overview.
