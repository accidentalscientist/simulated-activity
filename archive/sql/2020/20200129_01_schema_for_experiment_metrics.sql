-- Archive task: Schema For Experiment Metrics
-- Generated for 2020-01-29

CREATE TABLE experiment_metrics (
    experiment_id TEXT NOT NULL,
    variant TEXT NOT NULL,
    metric_date DATE NOT NULL,
    visitors INTEGER NOT NULL,
    conversions INTEGER NOT NULL,
    revenue NUMERIC(12, 2),
    PRIMARY KEY (experiment_id, variant, metric_date)
);
