// Archive task: Graph Traversal
// Generated for 2021-10-12

use std::collections::{HashMap, HashSet, VecDeque};

pub fn reachable(graph: &HashMap<&str, Vec<&str>>, start: &str) -> HashSet<String> {
    let mut seen = HashSet::new();
    let mut queue = VecDeque::from([start]);
    while let Some(node) = queue.pop_front() {
        if seen.insert(node.to_string()) {
            if let Some(neighbours) = graph.get(node) {
                queue.extend(neighbours.iter().copied());
            }
        }
    }
    seen
}
