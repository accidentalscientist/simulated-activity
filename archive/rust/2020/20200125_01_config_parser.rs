// Archive task: Config Parser
// Generated for 2020-01-25

pub fn bounded_sum(values: &[i64], limit: i64) -> i64 {
    values
        .iter()
        .copied()
        .filter(|value| *value <= limit)
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn sums_values_under_limit() {
        assert_eq!(bounded_sum(&[2, 5, 8, 13], 8), 15);
    }
}
