use rand::SeedableRng;
use rand_xoshiro::Xoshiro256Plus;

fn naive() {
    let seed = 123456789;
    let rng = Xoshiro256Plus::seed_from_u64(seed);
}

struct NaiveMultiBinaryMeasure {
    population_proportion: f64,
    specificity: f64,
    sensitivity: f64,
}