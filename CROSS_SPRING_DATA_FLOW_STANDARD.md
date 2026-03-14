# Cross-Spring Time Series Exchange Format

**Purpose**: Standard format for Springs to exchange time series data via `capability.call`.

---

## 1. Purpose

This document defines a canonical format for time series data exchanged between Springs through the Neural API `capability.call` mechanism. Springs can pass environmental drivers, sensor readings, or derived quantities to other Springs without format negotiation.

---

## 2. Format (JSON)

```json
{
  "schema": "ecoPrimals/time-series/v1",
  "variable": "soil_moisture_vol",
  "unit": "m3/m3",
  "source": {
    "spring": "airSpring",
    "experiment": "exp022",
    "capability": "ecology.water_balance"
  },
  "timestamps": ["2023-05-01T00:00:00Z", "2023-05-02T00:00:00Z"],
  "values": [0.32, 0.29],
  "metadata": {
    "location": "optional",
    "sensor": "optional"
  }
}
```

---

## 3. Required Fields

| Field       | Type     | Description                                      |
|-------------|----------|--------------------------------------------------|
| `schema`    | string   | Must be `ecoPrimals/time-series/v1`              |
| `variable`  | string   | Variable name (snake_case)                       |
| `unit`      | string   | SI unit or documented unit string               |
| `timestamps`| string[] | ISO 8601 UTC timestamps                         |
| `values`    | number[] | f64 array, same length as timestamps            |

---

## 4. Optional Fields

| Field    | Type   | Description                                      |
|----------|--------|--------------------------------------------------|
| `source` | object | Origin spring, experiment, capability           |
| `metadata` | object | Extensible (location, sensor, etc.)           |

---

## 5. Conventions

- **Timestamps**: ISO 8601 UTC (e.g. `2023-05-01T00:00:00Z`)
- **Values**: f64 array, same length as `timestamps`
- **Units**: SI preferred; document with each variable
- **Variable names**: snake_case (e.g. `soil_moisture_vol`, `player_heart_rate`)

---

## 6. Example Exchanges

| From        | To          | Variable                    | Unit          |
|-------------|-------------|-----------------------------|---------------|
| airSpring   | wetSpring   | soil_moisture_vol           | m3/m3         |
| ludoSpring  | healthSpring| player_heart_rate           | bpm           |
| wetSpring   | airSpring   | microbial_diversity_index   | dimensionless |

---

## 7. Integration with capability.call

Time series data is passed as an argument to capability operations:

```json
{
  "capability": "science",
  "operation": "analyze_diversity",
  "args": {
    "time_series": {
      "schema": "ecoPrimals/time-series/v1",
      "variable": "soil_moisture_vol",
      "unit": "m3/m3",
      "source": {
        "spring": "airSpring",
        "experiment": "exp022",
        "capability": "ecology.water_balance"
      },
      "timestamps": ["2023-05-01T00:00:00Z", "2023-05-02T00:00:00Z"],
      "values": [0.32, 0.29],
      "metadata": {}
    }
  }
}
```

---

## 8. Provenance

When time series data flows through the trio (airSpring → wetSpring → ToadStool), the `source` field becomes a **sweetGrass braid reference**. Provenance tracking preserves the chain of transformations and original data origin.
