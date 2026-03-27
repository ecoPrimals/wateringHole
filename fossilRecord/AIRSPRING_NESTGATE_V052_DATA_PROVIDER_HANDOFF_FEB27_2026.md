# airSpring → NestGate V0.5.2 Handoff: Agricultural Data Provider Pattern

**Date**: February 27, 2026
**From**: airSpring v0.5.2
**To**: NestGate team
**License**: AGPL-3.0-or-later

---

## Part 1: Executive Summary

airSpring needs autonomous data acquisition for agricultural weather and crop
data from three public APIs. NestGate already has live providers for NCBI,
Ensembl, HuggingFace, Open-Meteo, NOAA CDO, and USDA NASS — the API stubs
exist. This handoff specifies the exact data requirements so NestGate can
evolve its providers to serve airSpring's validated pipeline.

The current bottleneck is Open-Meteo API rate limiting: 80-year downloads for
100 Michigan stations take 4–5 days at the current pace. A NestGate provider
with download-once-store-with-provenance and rate-limit-aware scheduling would
eliminate this for all springs that need weather data.

---

## Part 2: Data Requirements

### Source 1: Open-Meteo ERA5 Archive (Primary)

**NestGate provider**: `open_meteo_live_provider.rs` (exists)
**API**: `https://archive-api.open-meteo.com/v1/archive`
**Auth**: None (free, rate-limited)
**Rate limit**: ~10 requests/minute, aggressive 429s on bursts

**Required daily variables**:
```
temperature_2m_max, temperature_2m_min, temperature_2m_mean,
relative_humidity_2m_max, relative_humidity_2m_min,
wind_speed_10m_max, wind_speed_10m_mean,
shortwave_radiation_sum, precipitation_sum,
et0_fao_evapotranspiration, pressure_msl,
sunshine_duration
```

**Column mapping to airSpring `WeatherDay`**:

| Open-Meteo Variable | CSV Column | airSpring Field | Unit |
|---------------------|-----------|----------------|------|
| `temperature_2m_max` | `tmax_c` | `tmax` | °C |
| `temperature_2m_min` | `tmin_c` | `tmin` | °C |
| `relative_humidity_2m_max` | `rh_max_pct` | `rh_max` | % |
| `relative_humidity_2m_min` | `rh_min_pct` | `rh_min` | % |
| (derived from 10m) | `wind_2m_m_s` | `wind_2m` | m/s |
| `shortwave_radiation_sum` | `solar_rad_mj_m2` | `solar_rad` | MJ/m²/day |
| `precipitation_sum` | `precip_mm` | `precipitation` | mm/day |
| `et0_fao_evapotranspiration` | `et0_openmeteo_mm` | (cross-validation) | mm/day |

**Wind conversion**: `wind_2m = wind_10m * 4.87 / ln(67.8 * 10 - 5.42)` (FAO-56 Eq. 47)

**Station coordinates**: `scripts/atlas_stations.json` has 100 Michigan stations
with `lat`, `lon`, `elevation_m`, `region`. Station IDs match CSV filenames.

**Download pattern**:
- Range: 1945-01-01 to 2024-12-31 per station
- ~29,220 rows per station (~4.5 MB CSV)
- Total: ~600 MB for 100 stations
- Rate-limit-aware: exponential backoff (30s → 600s) on HTTP 429
- Resume: skip stations already on disk

**Current state**: 12/100 stations downloaded via `scripts/download_atlas_80yr.py`
(background process running). The Python script handles rate limiting but is
not integrated with NestGate provenance or storage.

### Source 2: NOAA CDO (Supplementary)

**NestGate provider**: `noaa_cdo_live_provider.rs` (exists)
**API**: `https://www.ncdc.noaa.gov/cdo-web/api/v2/`
**Auth**: Free API token (request via web)

**Potential use**: GHCN-Daily station observations for cross-validation against
ERA5 reanalysis. Not currently consumed by airSpring — future extension.

### Source 3: USDA NASS Quick Stats (Supplementary)

**NestGate provider**: `usda_nass_live_provider.rs` (exists)
**API**: `https://quickstats.nass.usda.gov/api/`
**Auth**: Free API key

**Potential use**: County-level crop yield data for Stewart (1977) yield model
validation against real NASS observations. Exp 024 (`validate_nass_yield`)
currently uses synthetic data. NASS data would enable real yield validation.

---

## Part 3: NestGate Integration Architecture

### Desired Data Flow

```
NestGate Provider (rate-limit-aware download)
    ↓
Content-Addressed Blob Store (download once, store with provenance)
    ↓
biomeOS capability.call("data.weather.michigan.daily")
    ↓
airSpring AtlasStream (consumes WeatherDay structs)
    ↓
SeasonalPipeline → GPU orchestrators → Results
```

### Provenance Requirements

Each downloaded dataset should record:
- **Source**: API endpoint and parameters
- **Downloaded**: ISO 8601 timestamp
- **Checksum**: SHA-256 of raw response
- **Station metadata**: lat, lon, elevation, region
- **Date range**: start/end dates
- **Row count**: for integrity verification

This follows the pattern in `ncbi_live_provider.rs` where `get_metadata()`
returns provider metadata alongside data.

### Rate-Limit Strategy

The Open-Meteo archive API is free but aggressively rate-limited:
- 429 responses after ~10 rapid requests
- No documented rate limit; empirically ~5-10 req/min sustained
- Best strategy: 15-20s base delay, exponential backoff on 429 (max 600s)
- Resume support: check blob store before re-downloading

NestGate's `UniversalHttpProvider` should handle this generically so all
weather-consuming springs benefit.

---

## Part 4: What airSpring Provides

### Current Data Assets (for NestGate to ingest/manage)

| Asset | Location | Size | Status |
|-------|----------|------|--------|
| 12 station 80yr CSVs | `data/open_meteo/*_1945-01-01_2024-12-31_daily.csv` | ~55 MB | Downloaded |
| 100 station metadata | `scripts/atlas_stations.json` | 12 KB | Complete |
| Growing season CSVs | `data/open_meteo/*_2023-05-01_2023-09-30_daily.csv` | ~4 MB | Complete |
| Download script | `scripts/download_atlas_80yr.py` | 3 KB | Working |

### Validation Pipeline (consuming data)

```bash
# Real data through atlas stream (73/73 PASS)
cargo run --release --bin validate_atlas_stream

# Real data through original atlas (1393/1393 checks)
cargo run --release --bin validate_atlas
```

---

## Part 5: NestGate Evolution Path

```
Step 1: Wire Open-Meteo provider to download 80yr atlas data
        Input: atlas_stations.json (100 stations, lat/lon/elevation)
        Output: content-addressed CSVs with provenance metadata
        Benefit: Any spring consuming weather data gets it for free

Step 2: Expose via DataCapability for biomeOS graphs
        capability_type: "weather_data"
        Parameters: station_id, date_range, variables
        Returns: DataResponse with CSV path or streaming rows

Step 3: NOAA CDO cross-validation layer
        Same stations, overlapping date range, GHCN-Daily observations
        Enables ERA5 vs in-situ comparison

Step 4: USDA NASS yield data
        Michigan county-level crop yields (corn, soybean, wheat, etc.)
        Enables real Stewart model validation
```

**No airSpring code changes needed** — NestGate evolves its providers, and
airSpring discovers the data via biomeOS `capability.call` or direct filesystem
path (backward compatible).
