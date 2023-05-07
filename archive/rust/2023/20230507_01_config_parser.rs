// Archive task: Config Parser
// Generated for 2023-05-07

pub fn parse_pairs(input: &str) -> Vec<(&str, &str)> {
    input
        .lines()
        .filter_map(|line| line.split_once('='))
        .map(|(key, value)| (key.trim(), value.trim()))
        .collect()
}
