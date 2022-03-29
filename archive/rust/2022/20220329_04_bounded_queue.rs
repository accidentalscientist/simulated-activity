// Archive task: Bounded Queue
// Generated for 2022-03-29

use std::collections::VecDeque;

pub struct BoundedQueue<T> {
    limit: usize,
    values: VecDeque<T>,
}

impl<T> BoundedQueue<T> {
    pub fn new(limit: usize) -> Self {
        Self { limit, values: VecDeque::new() }
    }

    pub fn push(&mut self, value: T) {
        if self.values.len() == self.limit {
            self.values.pop_front();
        }
        self.values.push_back(value);
    }
}
