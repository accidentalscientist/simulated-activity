// Archive task: Fast Line Counter
// Generated for 2022-06-21

pub fn count_lines(input: &str) -> usize {
    input.lines().count()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn counts_lines() {
        assert_eq!(count_lines("a\nb\nc"), 3);
    }
}
