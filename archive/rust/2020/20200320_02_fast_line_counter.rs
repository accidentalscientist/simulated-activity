// Archive task: Fast Line Counter
// Generated for 2020-03-20

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
