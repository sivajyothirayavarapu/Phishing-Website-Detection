# Phishing Website Detection — Project Report Outline

## 1. Title

**Phishing Website Detection Using Machine Learning**

## 2. Abstract

Phishing attacks commonly use deceptive URLs to redirect victims to pages that imitate trusted services. This project develops a defensive machine-learning baseline that classifies a URL as legitimate or phishing-like using lexical and structural URL features. A Random Forest classifier is trained on an educational dataset and deployed through a Flask web application and REST API. The system also provides human-readable warning signals so a learner can understand which URL characteristics influenced the assessment.

## 3. Problem Statement

Users often cannot recognize suspicious URLs by visual inspection alone. A lightweight automated detector can provide an additional warning layer by scoring URL characteristics before a user visits the site.

## 4. Objectives

1. Extract useful structural indicators from URLs.
2. Train a supervised machine-learning classifier.
3. Evaluate the classifier using standard classification metrics.
4. Expose predictions through a web interface.
5. Provide an API for programmatic use.
6. Explain simple warning signals without visiting the target URL.

## 5. Scope

### Included

- URL parsing
- lexical feature engineering
- Random Forest classification
- model serialization
- Flask UI/API
- unit tests
- Docker deployment

### Not included

- live website crawling
- browser rendering
- credential harvesting
- exploit execution
- automated page submission

## 6. Methodology

```text
Dataset
  ↓
Cleaning + de-duplication
  ↓
Feature extraction
  ↓
Stratified train/test split
  ↓
Random Forest training
  ↓
Evaluation
  ↓
Model persistence
  ↓
Flask inference
```

## 7. Features

See `detector/features.py` and the README feature table.

## 8. Model

The baseline model is `RandomForestClassifier` with 300 trees, class balancing, a fixed random seed, and parallel training.

## 9. Evaluation

The training script reports:

- accuracy
- precision
- recall
- F1 score
- ROC-AUC

For a serious research result, use an independently sourced dataset and a test protocol that prevents duplicate or near-duplicate URLs from crossing the train/test boundary.

## 10. Ethical and Safety Considerations

The application deliberately analyzes only the submitted URL string. It does not connect to the submitted site. Production use should add appropriate privacy, rate limiting, monitoring, and data-handling controls.

## 11. Future Work

- larger real-world datasets
- character-level deep learning
- model calibration
- temporal evaluation
- trusted threat-intelligence enrichment
- domain/DNS metadata in a sandboxed backend
- analyst feedback and continuous retraining
